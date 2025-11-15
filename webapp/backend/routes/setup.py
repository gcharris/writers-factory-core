"""
Project Setup API Routes - Sprint 14 Phase B

Endpoints for the Project Setup Wizard:
- POST /api/setup/analyze-voice - Analyze voice from example passages
- POST /api/setup/generate-skills - Generate 6 custom skills
- POST /api/setup/test-skill - Test a generated skill
- POST /api/setup/create-project - Create complete project structure
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import sys
import os
from pathlib import Path
from anthropic import Anthropic

# Add factory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from factory.core.voice_extractor import VoiceProfileExtractor, VoiceProfile
from factory.core.skill_generator import SkillGenerator, GeneratedSkill
from factory.core.project_creator import ProjectCreator
from factory.integrations.notebooklm_setup import NotebookLMSetupIntegration
from factory.core.skill_orchestrator import SkillOrchestrator, SkillRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/setup", tags=["setup"])


# Helper to get Anthropic client
def get_anthropic_client() -> Anthropic:
    """Get Anthropic API client with key from environment."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY environment variable not set"
        )
    return Anthropic(api_key=api_key)


# Request/Response Models
class AnalyzeVoiceRequest(BaseModel):
    examplePassages: List[str]
    uploadedDocs: List[Dict[str, str]] = []  # [{"filename": "...", "content": "..."}]
    notebooklmUrls: List[str] = []
    styleGuide: str = ""
    genre: str = "literary"


class VoiceProfileResponse(BaseModel):
    voiceProfile: Dict[str, Any]


class GenerateSkillsRequest(BaseModel):
    name: str
    genre: str
    examplePassages: List[str]
    uploadedDocs: List[Dict[str, str]] = []
    notebooklmUrls: List[str] = []
    voiceProfile: Dict[str, Any]


class GenerateSkillsResponse(BaseModel):
    skills: Dict[str, Any]


class TestSkillRequest(BaseModel):
    projectId: str
    skillType: str
    testScene: str


class TestSkillResponse(BaseModel):
    overall_score: Optional[int] = None
    quality_tier: Optional[str] = None
    category_scores: Optional[Dict[str, int]] = None
    analysis: Optional[str] = None


class CreateProjectRequest(BaseModel):
    name: str
    genre: str
    examplePassages: List[str]
    uploadedDocs: List[Dict[str, str]] = []
    notebooklmUrls: List[str] = []
    voiceProfile: Dict[str, Any]
    generatedSkills: Dict[str, Any]
    goals: str = ""


class CreateProjectResponse(BaseModel):
    projectId: str
    projectPath: str
    skills: List[str]


# Endpoints

@router.post("/analyze-voice", response_model=VoiceProfileResponse)
async def analyze_voice(request: AnalyzeVoiceRequest):
    """
    Analyze writing voice from example passages.

    Uses Phase A VoiceProfileExtractor to extract:
    - Voice name and primary characteristics
    - Sentence structure patterns
    - POV style and depth
    - Metaphor domains
    - Anti-patterns
    - Quality criteria
    """
    try:
        logger.info(f"Analyzing voice from {len(request.examplePassages)} passages")

        # Initialize extractor with Anthropic client
        client = get_anthropic_client()
        extractor = VoiceProfileExtractor(client)

        # Extract voice profile
        voice_profile = await extractor.extract_voice_profile(
            example_passages=request.examplePassages,
            uploaded_docs=request.uploadedDocs,
            notebooklm_context=None  # TODO: Add NotebookLM support
        )

        if not voice_profile:
            raise HTTPException(
                status_code=500,
                detail="Voice analysis failed to extract profile"
            )

        # Convert to dict for JSON response using built-in method
        profile_dict = voice_profile.to_dict()

        logger.info(f"Voice profile extracted: {voice_profile.voice_name}")

        return VoiceProfileResponse(voiceProfile=profile_dict)

    except Exception as e:
        logger.error(f"Voice analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Voice analysis failed: {str(e)}"
        )


@router.post("/generate-skills", response_model=GenerateSkillsResponse)
async def generate_skills(request: GenerateSkillsRequest):
    """
    Generate 6 custom skills for the project.

    Uses Phase A SkillGenerator to create:
    - scene-analyzer-[project]
    - scene-enhancer-[project]
    - character-validator-[project]
    - scene-writer-[project]
    - scene-multiplier-[project]
    - scaffold-generator-[project]
    """
    try:
        logger.info(f"Generating skills for project: {request.name}")

        # Reconstruct VoiceProfile from dict
        voice_profile = _dict_to_voice_profile(request.voiceProfile)

        # Extract knowledge context from NotebookLM if provided
        knowledge_context = ""
        if request.notebooklmUrls:
            try:
                notebooklm = NotebookLMSetupIntegration()
                knowledge_data = await notebooklm.extract_project_knowledge(
                    notebook_urls=request.notebooklmUrls
                )
                knowledge_context = knowledge_data.get('summary', '')
            except Exception as e:
                logger.warning(f"NotebookLM extraction failed: {e}")
                knowledge_context = ""

        # Initialize skill generator with Anthropic client
        client = get_anthropic_client()
        generator = SkillGenerator(client)

        # Generate all 6 skills
        skills = await generator.generate_all_skills(
            project_name=request.name,
            voice_profile=voice_profile,
            knowledge_context=knowledge_context
        )

        # Convert to dict for JSON response
        skills_dict = {}
        for skill_type, skill in skills.items():
            skills_dict[skill_type] = {
                "skillName": skill.skill_name,
                "skillType": skill.skill_type,
                "skillMd": skill.skill_md,
                "references": skill.references
            }

        logger.info(f"Generated {len(skills_dict)} skills successfully")

        return GenerateSkillsResponse(skills=skills_dict)

    except Exception as e:
        logger.error(f"Skill generation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Skill generation failed: {str(e)}"
        )


@router.post("/test-skill", response_model=TestSkillResponse)
async def test_skill(request: TestSkillRequest):
    """
    Test a generated skill on a sample scene.

    Currently supports testing scene-analyzer.
    Uses Phase A SkillOrchestrator to execute the skill.
    """
    try:
        logger.info(f"Testing {request.skillType} for project {request.projectId}")

        # Initialize orchestrator
        orchestrator = SkillOrchestrator()

        # Build skill request
        skill_request = SkillRequest(
            skill_name=f"{request.skillType}-{request.projectId}",
            input_data={
                "scene_content": request.testScene,
                "mode": "detailed",
                "phase": "phase2"
            },
            context={"project_id": request.projectId}
        )

        # Execute skill
        result = await orchestrator.execute_skill(
            skill_request,
            project_id=request.projectId
        )

        # Parse results
        if not result.success:
            raise HTTPException(
                status_code=500,
                detail=f"Skill execution failed: {result.error}"
            )

        # Extract scores from result data
        data = result.data or {}

        response = TestSkillResponse(
            overall_score=data.get("overall_score"),
            quality_tier=data.get("quality_tier"),
            category_scores=data.get("category_scores"),
            analysis=data.get("analysis", "")
        )

        logger.info(f"Skill test complete. Score: {response.overall_score}/100")

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Skill test failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Skill test failed: {str(e)}"
        )


@router.post("/create-project", response_model=CreateProjectResponse)
async def create_project(request: CreateProjectRequest):
    """
    Create complete project structure with custom skills.

    Uses Phase A ProjectCreator to:
    - Create project directory structure
    - Save generated skills to .claude/skills/
    - Create knowledge base in knowledge/craft/
    - Generate config.json and README.md
    """
    try:
        logger.info(f"Creating project: {request.name}")

        # Reconstruct VoiceProfile
        voice_profile = _dict_to_voice_profile(request.voiceProfile)

        # Reconstruct GeneratedSkills
        generated_skills = {}
        for skill_type, skill_data in request.generatedSkills.items():
            generated_skills[skill_type] = GeneratedSkill(
                skill_name=skill_data["skillName"],
                skill_type=skill_data["skillType"],
                skill_md=skill_data["skillMd"],
                references=skill_data["references"]
            )

        # Extract knowledge context from NotebookLM
        knowledge_context = ""
        if request.notebooklmUrls:
            try:
                notebooklm = NotebookLMSetupIntegration()
                knowledge_data = await notebooklm.extract_project_knowledge(
                    notebook_urls=request.notebooklmUrls
                )
                knowledge_context = knowledge_data.get('summary', '')
            except Exception as e:
                logger.warning(f"NotebookLM extraction failed: {e}")
                knowledge_context = ""

        # Initialize project creator
        creator = ProjectCreator(projects_root=Path("./projects"))

        # Create project
        project_path = await creator.create_project(
            project_name=request.name,
            voice_profile=voice_profile,
            generated_skills=generated_skills,
            genre=request.genre,
            knowledge_context=knowledge_context,
            uploaded_docs=request.uploadedDocs
        )

        # Register skills with orchestrator
        orchestrator = SkillOrchestrator()
        orchestrator.register_project_skills(
            project_id=request.name,
            skills=generated_skills
        )

        logger.info(f"Project created at: {project_path}")

        return CreateProjectResponse(
            projectId=request.name,
            projectPath=str(project_path),
            skills=list(generated_skills.keys())
        )

    except Exception as e:
        logger.error(f"Project creation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Project creation failed: {str(e)}"
        )


# Helper Functions

def _dict_to_voice_profile(profile_dict: Dict[str, Any]) -> VoiceProfile:
    """Convert dictionary back to VoiceProfile object."""
    from factory.core.voice_extractor import MetaphorDomain, AntiPattern, QualityCriteria

    # Reconstruct metaphor domains
    metaphor_domains = []
    for md in profile_dict.get("metaphorDomains", []):
        metaphor_domains.append(
            MetaphorDomain(
                name=md["name"],
                percentage=md["percentage"],
                keywords=md.get("keywords", []),
                examples=md.get("examples", [])
            )
        )

    # Reconstruct anti-patterns
    anti_patterns = []
    for ap in profile_dict.get("antiPatterns", []):
        anti_patterns.append(
            AntiPattern(
                pattern=ap["pattern"],
                reason=ap["reason"],
                examples=ap.get("examples", [])
            )
        )

    # Reconstruct quality criteria
    quality_criteria = []
    for qc in profile_dict.get("qualityCriteria", []):
        quality_criteria.append(
            QualityCriteria(
                category=qc["category"],
                criteria=qc["criteria"],
                weight=qc.get("weight", 10)
            )
        )

    return VoiceProfile(
        voice_name=profile_dict.get("voiceName", "Unknown Voice"),
        primary_characteristics=profile_dict.get("primaryCharacteristics", []),
        sentence_structure=profile_dict.get("sentenceStructure", {}),
        pov_style=profile_dict.get("povStyle", {}),
        vocabulary=profile_dict.get("vocabulary", {}),
        dialogue_patterns=profile_dict.get("dialoguePatterns", {}),
        metaphor_domains=metaphor_domains,
        anti_patterns=anti_patterns,
        quality_criteria=quality_criteria
    )
