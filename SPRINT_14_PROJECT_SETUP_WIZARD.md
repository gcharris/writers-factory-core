# Sprint 14: Project Setup Wizard & Skill Generation System

**Status:** Ready for Implementation
**Priority:** CRITICAL - BLOCKING
**Estimated Effort:** 25-30 hours
**Dependencies:** Sprint 11 (NotebookLM), Sprint 12 (Skill Orchestration)

---

## Executive Summary

**THE Problem:**
Sprint 12 hardcoded skills for The Explants project only. Writers Factory needs to support ANY writer's project with CUSTOM skills generated during setup.

**THE Solution:**
Build a Project Setup Wizard that:
1. Collects project inputs (NotebookLM links, uploaded docs, voice samples)
2. Uses LLM + NotebookLM to analyze and extract voice profile
3. GENERATES 6 custom skills for this specific project
4. Creates project-specific knowledge base and file structure

**THE Result:**
Every writer can set up their novel with AI-generated skills tailored to THEIR voice, genre, and style.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  PROJECT SETUP WIZARD                        │
│                                                              │
│  Step 1: Project Details                                    │
│  ├─ Project name, genre, goals                              │
│  └─ Writer preferences                                      │
│                                                              │
│  Step 2: Voice Input Collection                             │
│  ├─ Paste example passages (3-5 scenes)                     │
│  ├─ Upload previous drafts (DOCX/PDF/MD)                    │
│  └─ Link NotebookLM notebooks                               │
│                                                              │
│  Step 3: Reference Materials                                │
│  ├─ Upload style guide                                      │
│  ├─ Upload character sheets                                 │
│  ├─ Upload world bible                                      │
│  └─ Specify anti-patterns to avoid                          │
│                                                              │
│  Step 4: AI Analysis ⚡                                      │
│  ├─ Voice Profile Extraction (LLM)                          │
│  ├─ NotebookLM Knowledge Extraction                         │
│  ├─ Quality Criteria Derivation (from genre)                │
│  ├─ Metaphor Domain Identification                          │
│  └─ Anti-Pattern Detection                                  │
│                                                              │
│  Step 5: Skill Generation ⚡⚡                               │
│  ├─ Generate scene-analyzer-[project]                       │
│  ├─ Generate scene-enhancer-[project]                       │
│  ├─ Generate character-validator-[project]                  │
│  ├─ Generate scene-writer-[project]                         │
│  ├─ Generate scene-multiplier-[project]                     │
│  └─ Generate scaffold-generator-[project]                   │
│                                                              │
│  Step 6: Review & Test                                      │
│  ├─ Preview generated skills                                │
│  ├─ Test on sample scene                                    │
│  ├─ Adjust parameters if needed                             │
│  └─ Finalize and save                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              PROJECT STRUCTURE CREATED                       │
│                                                              │
│  projects/[project-name]/                                    │
│  ├─ .claude/                                                │
│  │   └─ skills/                                             │
│  │       ├─ scene-analyzer-[project]/                       │
│  │       │   ├─ SKILL.md (custom prompt)                    │
│  │       │   └─ references/                                 │
│  │       │       ├─ voice-profile.md                        │
│  │       │       ├─ anti-patterns.md                        │
│  │       │       ├─ metaphor-domains.md                     │
│  │       │       └─ quality-criteria.md                     │
│  │       ├─ scene-enhancer-[project]/                       │
│  │       ├─ character-validator-[project]/                  │
│  │       ├─ scene-writer-[project]/                         │
│  │       ├─ scene-multiplier-[project]/                     │
│  │       └─ scaffold-generator-[project]/                   │
│  ├─ knowledge/                                              │
│  │   └─ craft/ (project-specific knowledge)                 │
│  ├─ scenes/ (manuscript storage)                            │
│  └─ config.json (project metadata)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase A: Backend - Skill Generation Engine (15-18h)

### Task 14-01: Voice Profile Extractor (4-5h)

**Purpose:** Analyze example passages and uploaded docs to extract voice characteristics.

**Implementation:**

**File:** `factory/core/voice_extractor.py`

```python
from typing import List, Dict, Any
from anthropic import Anthropic
import json

class VoiceProfileExtractor:
    """
    Extracts voice profile from example passages using LLM analysis.

    Analyzes:
    - Sentence structure (short/long, compressed/flowing)
    - Vocabulary (formal/casual, technical/simple)
    - Metaphor style (direct/complex, domains)
    - POV handling (deep/shallow, filter words)
    - Dialogue patterns
    - Internal monologue style
    """

    def __init__(self, anthropic_client: Anthropic):
        self.client = anthropic_client

    async def extract_voice_profile(
        self,
        example_passages: List[str],
        uploaded_docs: List[Dict[str, Any]],
        notebooklm_context: str = None
    ) -> VoiceProfile:
        """
        Extract comprehensive voice profile from inputs.

        Args:
            example_passages: 3-5 scene excerpts (500-1000 words each)
            uploaded_docs: Previous drafts, style guides
            notebooklm_context: Knowledge from NotebookLM notebook

        Returns:
            VoiceProfile with extracted characteristics
        """

        # Step 1: Analyze each passage individually
        passage_analyses = []
        for i, passage in enumerate(example_passages):
            analysis = await self._analyze_single_passage(passage, i+1)
            passage_analyses.append(analysis)

        # Step 2: Synthesize across all passages
        voice_profile = await self._synthesize_voice_profile(
            passage_analyses,
            uploaded_docs,
            notebooklm_context
        )

        # Step 3: Extract specific elements
        voice_profile.metaphor_domains = await self._extract_metaphor_domains(
            example_passages
        )
        voice_profile.anti_patterns = await self._identify_anti_patterns(
            example_passages,
            uploaded_docs
        )
        voice_profile.quality_criteria = await self._derive_quality_criteria(
            voice_profile,
            genre=voice_profile.genre
        )

        return voice_profile

    async def _analyze_single_passage(
        self,
        passage: str,
        passage_num: int
    ) -> Dict[str, Any]:
        """
        Deep analysis of a single passage.

        Returns characteristics:
        - sentence_length_avg, sentence_length_variance
        - compression_level (1-10)
        - metaphor_density, metaphor_complexity
        - filter_word_count
        - pov_depth (shallow/medium/deep)
        - vocabulary_level (simple/moderate/complex)
        - dialogue_ratio
        """

        prompt = f"""Analyze this passage from a novel and extract detailed voice characteristics.

PASSAGE {passage_num}:
{passage}

Provide JSON analysis with these fields:

{{
  "sentence_structure": {{
    "avg_length": <number of words>,
    "variance": "high|medium|low",
    "compression_style": "compressed|flowing|mixed",
    "fragment_usage": "frequent|occasional|rare"
  }},
  "vocabulary": {{
    "formality": "formal|neutral|casual",
    "complexity": "simple|moderate|complex",
    "jargon_domains": ["domain1", "domain2"],
    "distinctive_words": ["word1", "word2", "word3"]
  }},
  "metaphor_style": {{
    "frequency": "high|medium|low",
    "directness": "direct|extended|mixed",
    "primary_domains": ["domain1", "domain2"],
    "examples": ["metaphor1", "metaphor2"]
  }},
  "pov_handling": {{
    "depth": "shallow|medium|deep",
    "filter_words": {{
      "saw": <count>,
      "heard": <count>,
      "felt": <count>,
      "noticed": <count>,
      "thought": <count>,
      "wondered": <count>,
      "realized": <count>
    }},
    "thought_tags": <count of "she thought", "he wondered", etc>,
    "consciousness_immersion": "high|medium|low"
  }},
  "dialogue": {{
    "dialogue_to_narrative_ratio": "<percentage>",
    "dialogue_style": "sparse|balanced|heavy",
    "tag_style": "minimal|standard|varied"
  }},
  "distinctive_traits": [
    "trait 1",
    "trait 2",
    "trait 3"
  ]
}}

Be precise and analytical. This will be used to generate writing quality criteria."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = json.loads(response.content[0].text)
        return analysis

    async def _synthesize_voice_profile(
        self,
        passage_analyses: List[Dict[str, Any]],
        uploaded_docs: List[Dict[str, Any]],
        notebooklm_context: str
    ) -> VoiceProfile:
        """
        Synthesize individual passage analyses into unified voice profile.
        """

        prompt = f"""Given these {len(passage_analyses)} passage analyses, synthesize a unified voice profile.

PASSAGE ANALYSES:
{json.dumps(passage_analyses, indent=2)}

UPLOADED DOCUMENTS:
{json.dumps([doc.get('summary', '') for doc in uploaded_docs], indent=2)}

NOTEBOOKLM CONTEXT:
{notebooklm_context or 'Not provided'}

Create a comprehensive voice profile:

{{
  "voice_name": "<descriptive name for this voice>",
  "genre": "<detected genre>",
  "primary_characteristics": [
    "characteristic 1 (consistent across all passages)",
    "characteristic 2",
    "characteristic 3"
  ],
  "sentence_structure": {{
    "typical_length": "<avg words>",
    "compression_level": "1-10 scale",
    "preferred_patterns": ["pattern1", "pattern2"]
  }},
  "vocabulary": {{
    "formality_level": "formal|neutral|casual",
    "complexity": "simple|moderate|complex",
    "distinctive_domains": ["domain1", "domain2"]
  }},
  "pov_style": {{
    "depth": "shallow|medium|deep",
    "consciousness_mode_percentage": "<estimated %>",
    "filter_word_tolerance": "strict|moderate|lenient"
  }},
  "voice_consistency_notes": [
    "What's consistent across passages",
    "What varies and why",
    "Potential anti-patterns"
  ]
}}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        profile_data = json.loads(response.content[0].text)
        return VoiceProfile.from_dict(profile_data)

    async def _extract_metaphor_domains(
        self,
        example_passages: List[str]
    ) -> Dict[str, MetaphorDomain]:
        """
        Identify primary metaphor domains and their usage patterns.

        Returns:
            {
                "domain_name": MetaphorDomain(
                    max_percentage=25,
                    keywords=["word1", "word2"],
                    examples=["metaphor1", "metaphor2"]
                )
            }
        """

        all_text = "\n\n".join(example_passages)

        prompt = f"""Identify the primary metaphor domains in this writing.

TEXT:
{all_text}

For each domain, provide:
1. Domain name (e.g., "gambling", "medical", "nature")
2. Frequency (% of metaphors from this domain)
3. Key vocabulary
4. Example metaphors

Return JSON:
{{
  "domains": [
    {{
      "name": "domain_name",
      "frequency_percentage": <number>,
      "max_recommended_percentage": <suggested limit>,
      "keywords": ["word1", "word2", ...],
      "examples": ["full metaphor 1", "full metaphor 2"]
    }}
  ]
}}

Only include domains with 10%+ usage."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = json.loads(response.content[0].text)

        metaphor_domains = {}
        for domain in result["domains"]:
            metaphor_domains[domain["name"]] = MetaphorDomain(
                max_percentage=domain["max_recommended_percentage"],
                keywords=domain["keywords"],
                examples=domain["examples"]
            )

        return metaphor_domains

    async def _identify_anti_patterns(
        self,
        example_passages: List[str],
        uploaded_docs: List[Dict[str, Any]]
    ) -> List[AntiPattern]:
        """
        Identify patterns this writer wants to AVOID.

        Analyzes:
        - Patterns present in style guide as "don't do this"
        - Inconsistencies across passages (writer correcting themselves)
        - Common craft issues (filter words, weak similes, etc)
        """

        # Check for style guide in uploaded docs
        style_guide_content = ""
        for doc in uploaded_docs:
            if "style" in doc.get("filename", "").lower():
                style_guide_content = doc.get("content", "")

        all_text = "\n\n".join(example_passages)

        prompt = f"""Identify anti-patterns this writer should avoid.

EXAMPLE PASSAGES:
{all_text}

STYLE GUIDE (if provided):
{style_guide_content or "Not provided"}

Analyze for:
1. Patterns explicitly forbidden in style guide
2. Common craft issues (filter words, thought tags, weak constructions)
3. Voice-specific issues (e.g., similes in compressed prose)
4. Inconsistencies that suggest writer is self-correcting

Return JSON:
{{
  "anti_patterns": [
    {{
      "pattern_id": "snake_case_id",
      "name": "Human-readable name",
      "description": "What this pattern is",
      "why_avoid": "Why it's problematic for THIS voice",
      "detection_method": "regex|keyword|llm",
      "regex": "<if regex detection>",
      "keywords": ["if", "keyword", "detection"],
      "severity": "high|medium|low",
      "examples_from_text": ["example1", "example2"]
    }}
  ]
}}

Be specific to THIS writer's voice."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = json.loads(response.content[0].text)

        anti_patterns = []
        for ap in result["anti_patterns"]:
            anti_patterns.append(AntiPattern(
                pattern_id=ap["pattern_id"],
                name=ap["name"],
                description=ap["description"],
                why_avoid=ap["why_avoid"],
                detection_method=ap["detection_method"],
                regex=ap.get("regex"),
                keywords=ap.get("keywords", []),
                severity=ap["severity"],
                examples=ap["examples_from_text"]
            ))

        return anti_patterns

    async def _derive_quality_criteria(
        self,
        voice_profile: VoiceProfile,
        genre: str
    ) -> QualityCriteria:
        """
        Derive scoring criteria based on voice + genre.

        Different genres have different priorities:
        - Literary fiction: Voice (40%), Character (25%), Craft (20%)
        - Thriller: Pacing (30%), Tension (25%), Voice (20%)
        - Romance: Emotional beats (30%), Tension (25%), Voice (20%)
        """

        prompt = f"""Given this voice profile and genre, derive quality scoring criteria.

VOICE PROFILE:
{voice_profile.to_json()}

GENRE: {genre}

Create a 100-point scoring system with 5-7 categories.

Return JSON:
{{
  "total_points": 100,
  "categories": [
    {{
      "category_id": "voice_authenticity",
      "name": "Voice Authenticity",
      "points": 30,
      "description": "How well the scene maintains this specific voice",
      "sub_criteria": [
        {{
          "name": "Sentence compression",
          "points": 10,
          "check": "What to evaluate"
        }},
        ...
      ]
    }},
    ...
  ]
}}

Tailor to THIS voice and genre."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        criteria_data = json.loads(response.content[0].text)
        return QualityCriteria.from_dict(criteria_data)


class VoiceProfile:
    """Complete voice profile for a project."""

    def __init__(
        self,
        voice_name: str,
        genre: str,
        primary_characteristics: List[str],
        sentence_structure: Dict[str, Any],
        vocabulary: Dict[str, Any],
        pov_style: Dict[str, Any],
        metaphor_domains: Dict[str, 'MetaphorDomain'] = None,
        anti_patterns: List['AntiPattern'] = None,
        quality_criteria: 'QualityCriteria' = None
    ):
        self.voice_name = voice_name
        self.genre = genre
        self.primary_characteristics = primary_characteristics
        self.sentence_structure = sentence_structure
        self.vocabulary = vocabulary
        self.pov_style = pov_style
        self.metaphor_domains = metaphor_domains or {}
        self.anti_patterns = anti_patterns or []
        self.quality_criteria = quality_criteria

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceProfile':
        return cls(
            voice_name=data["voice_name"],
            genre=data["genre"],
            primary_characteristics=data["primary_characteristics"],
            sentence_structure=data["sentence_structure"],
            vocabulary=data["vocabulary"],
            pov_style=data["pov_style"]
        )

    def to_json(self) -> str:
        return json.dumps({
            "voice_name": self.voice_name,
            "genre": self.genre,
            "primary_characteristics": self.primary_characteristics,
            "sentence_structure": self.sentence_structure,
            "vocabulary": self.vocabulary,
            "pov_style": self.pov_style
        }, indent=2)


class MetaphorDomain:
    """A metaphor domain with usage limits."""

    def __init__(
        self,
        max_percentage: int,
        keywords: List[str],
        examples: List[str]
    ):
        self.max_percentage = max_percentage
        self.keywords = keywords
        self.examples = examples


class AntiPattern:
    """A pattern to avoid in this voice."""

    def __init__(
        self,
        pattern_id: str,
        name: str,
        description: str,
        why_avoid: str,
        detection_method: str,
        severity: str,
        examples: List[str],
        regex: str = None,
        keywords: List[str] = None
    ):
        self.pattern_id = pattern_id
        self.name = name
        self.description = description
        self.why_avoid = why_avoid
        self.detection_method = detection_method
        self.severity = severity
        self.examples = examples
        self.regex = regex
        self.keywords = keywords or []


class QualityCriteria:
    """Scoring criteria for this voice/genre."""

    def __init__(self, total_points: int, categories: List[Dict[str, Any]]):
        self.total_points = total_points
        self.categories = categories

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QualityCriteria':
        return cls(
            total_points=data["total_points"],
            categories=data["categories"]
        )
```

**Success Criteria:**
- [ ] Can analyze 3-5 example passages
- [ ] Extracts voice characteristics (sentence structure, vocabulary, POV)
- [ ] Identifies metaphor domains with frequency
- [ ] Detects anti-patterns from style guide
- [ ] Derives genre-appropriate quality criteria
- [ ] Returns comprehensive VoiceProfile object

---

### Task 14-02: Skill Generator (6-7h)

**Purpose:** Generate 6 custom skills for a project using VoiceProfile.

**Implementation:**

**File:** `factory/core/skill_generator.py`

```python
from typing import Dict, List, Any
from pathlib import Path
import json

class SkillGenerator:
    """
    Generates custom Claude Code skills for a project.

    For each skill type, generates:
    - SKILL.md with project-specific prompts
    - references/ directory with voice profile, anti-patterns, etc.
    """

    def __init__(self, anthropic_client: Anthropic):
        self.client = anthropic_client
        self.templates_dir = Path("factory/knowledge/templates")

    async def generate_project_skills(
        self,
        project_name: str,
        voice_profile: VoiceProfile,
        notebooklm_context: str = None
    ) -> Dict[str, GeneratedSkill]:
        """
        Generate all 6 skills for a project.

        Skills generated:
        1. scene-analyzer-[project]
        2. scene-enhancer-[project]
        3. character-validator-[project]
        4. scene-writer-[project]
        5. scene-multiplier-[project]
        6. scaffold-generator-[project]

        Returns:
            Dictionary mapping skill_type -> GeneratedSkill
        """

        skills = {}

        # Generate each skill type
        skills["scene-analyzer"] = await self._generate_scene_analyzer(
            project_name, voice_profile
        )

        skills["scene-enhancer"] = await self._generate_scene_enhancer(
            project_name, voice_profile
        )

        skills["character-validator"] = await self._generate_character_validator(
            project_name, voice_profile
        )

        skills["scene-writer"] = await self._generate_scene_writer(
            project_name, voice_profile, notebooklm_context
        )

        skills["scene-multiplier"] = await self._generate_scene_multiplier(
            project_name, voice_profile
        )

        skills["scaffold-generator"] = await self._generate_scaffold_generator(
            project_name, voice_profile, notebooklm_context
        )

        return skills

    async def _generate_scene_analyzer(
        self,
        project_name: str,
        voice_profile: VoiceProfile
    ) -> GeneratedSkill:
        """
        Generate scene-analyzer-[project] skill.

        This skill scores scenes 0-100 using project-specific criteria.
        """

        skill_name = f"scene-analyzer-{project_name}"

        # Generate SKILL.md
        skill_prompt = await self._generate_analyzer_prompt(voice_profile)

        # Generate reference files
        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile),
            "anti-patterns.md": self._format_anti_patterns_md(voice_profile.anti_patterns),
            "quality-criteria.md": self._format_quality_criteria_md(voice_profile.quality_criteria),
            "metaphor-domains.md": self._format_metaphor_domains_md(voice_profile.metaphor_domains)
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="scene-analyzer",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    async def _generate_analyzer_prompt(
        self,
        voice_profile: VoiceProfile
    ) -> str:
        """
        Generate custom SKILL.md prompt for scene analyzer.
        """

        # Load base template
        template = (self.templates_dir / "scene-analyzer-template.md").read_text()

        # Use LLM to customize template for this voice
        customization_prompt = f"""Customize this scene analyzer skill template for a specific voice.

BASE TEMPLATE:
{template}

VOICE PROFILE:
{voice_profile.to_json()}

QUALITY CRITERIA:
{json.dumps(voice_profile.quality_criteria.__dict__, indent=2)}

ANTI-PATTERNS:
{json.dumps([ap.__dict__ for ap in voice_profile.anti_patterns], indent=2)}

Generate a complete SKILL.md that:
1. Uses the base template structure
2. Customizes scoring criteria for THIS voice (total 100 points)
3. Includes voice-specific anti-patterns in detection
4. Provides voice-specific examples
5. References the project's voice-profile.md, anti-patterns.md, etc.

Return ONLY the complete SKILL.md content (markdown format)."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8000,
            messages=[{"role": "user", "content": customization_prompt}]
        )

        return response.content[0].text

    async def _generate_scene_enhancer(
        self,
        project_name: str,
        voice_profile: VoiceProfile
    ) -> GeneratedSkill:
        """
        Generate scene-enhancer-[project] skill.

        This skill makes surgical fixes to match the voice profile.
        """

        skill_name = f"scene-enhancer-{project_name}"

        # Load template
        template = (self.templates_dir / "scene-enhancer-template.md").read_text()

        # Customize for voice
        customization_prompt = f"""Customize this scene enhancer skill for a specific voice.

BASE TEMPLATE:
{template}

VOICE PROFILE:
{voice_profile.to_json()}

ANTI-PATTERNS TO FIX:
{json.dumps([ap.__dict__ for ap in voice_profile.anti_patterns], indent=2)}

Generate SKILL.md that:
1. Uses 8-pass ritual structure (Read, Voice Auth, Fix 1-5, Final Check)
2. Focuses on THIS voice's anti-patterns
3. Maintains THIS voice's characteristics
4. Includes voice-specific fix examples

Return complete SKILL.md (markdown)."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8000,
            messages=[{"role": "user", "content": customization_prompt}]
        )

        skill_prompt = response.content[0].text

        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile),
            "anti-patterns.md": self._format_anti_patterns_md(voice_profile.anti_patterns),
            "fix-patterns.md": self._format_fix_patterns_md(voice_profile)
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="scene-enhancer",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    async def _generate_character_validator(
        self,
        project_name: str,
        voice_profile: VoiceProfile
    ) -> GeneratedSkill:
        """
        Generate character-validator-[project] skill.
        """

        skill_name = f"character-validator-{project_name}"

        template = (self.templates_dir / "character-validator-template.md").read_text()

        # This skill is less voice-dependent, more about consistency
        skill_prompt = template.replace("{{PROJECT_NAME}}", project_name)

        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile)
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="character-validator",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    async def _generate_scene_writer(
        self,
        project_name: str,
        voice_profile: VoiceProfile,
        notebooklm_context: str
    ) -> GeneratedSkill:
        """
        Generate scene-writer-[project] skill.

        This writes NEW scenes in the project's voice.
        """

        skill_name = f"scene-writer-{project_name}"

        template = (self.templates_dir / "scene-writer-template.md").read_text()

        customization_prompt = f"""Customize this scene writer skill for a specific voice.

BASE TEMPLATE:
{template}

VOICE PROFILE:
{voice_profile.to_json()}

NOTEBOOKLM CONTEXT (story world, characters):
{notebooklm_context or "Not provided"}

Generate SKILL.md that:
1. Writes scenes in THIS specific voice
2. Uses voice characteristics (compression, metaphors, POV depth)
3. Avoids anti-patterns
4. Incorporates story world knowledge from NotebookLM

Return complete SKILL.md."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8000,
            messages=[{"role": "user", "content": customization_prompt}]
        )

        skill_prompt = response.content[0].text

        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile),
            "anti-patterns.md": self._format_anti_patterns_md(voice_profile.anti_patterns),
            "story-context.md": notebooklm_context or "# Story Context\n\nTo be populated during project work."
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="scene-writer",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    async def _generate_scene_multiplier(
        self,
        project_name: str,
        voice_profile: VoiceProfile
    ) -> GeneratedSkill:
        """
        Generate scene-multiplier-[project] skill.

        Creates 5 variations of a scene using verbalized sampling.
        """

        skill_name = f"scene-multiplier-{project_name}"

        template = (self.templates_dir / "scene-multiplier-template.md").read_text()

        customization_prompt = f"""Customize this scene multiplier for a specific voice.

BASE TEMPLATE:
{template}

VOICE PROFILE:
{voice_profile.to_json()}

Generate SKILL.md that:
1. Creates 5 variations using verbalized sampling
2. Each variation maintains THIS voice
3. Each explores different narrative choices
4. All avoid anti-patterns

Return complete SKILL.md."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8000,
            messages=[{"role": "user", "content": customization_prompt}]
        )

        skill_prompt = response.content[0].text

        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile)
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="scene-multiplier",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    async def _generate_scaffold_generator(
        self,
        project_name: str,
        voice_profile: VoiceProfile,
        notebooklm_context: str
    ) -> GeneratedSkill:
        """
        Generate scaffold-generator-[project] skill.

        Transforms minimal outlines into detailed scaffolds.
        """

        skill_name = f"scaffold-generator-{project_name}"

        template = (self.templates_dir / "scaffold-generator-template.md").read_text()

        customization_prompt = f"""Customize this scaffold generator for a project.

BASE TEMPLATE:
{template}

VOICE PROFILE:
{voice_profile.to_json()}

NOTEBOOKLM CONTEXT:
{notebooklm_context or "Not provided"}

Generate SKILL.md that:
1. Expands outlines using NotebookLM knowledge
2. Generates scaffolds appropriate for THIS voice
3. Includes voice requirements in success criteria

Return complete SKILL.md."""

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8000,
            messages=[{"role": "user", "content": customization_prompt}]
        )

        skill_prompt = response.content[0].text

        references = {
            "voice-profile.md": self._format_voice_profile_md(voice_profile),
            "story-context.md": notebooklm_context or "# Story Context\n\nTo be populated."
        }

        return GeneratedSkill(
            skill_name=skill_name,
            skill_type="scaffold-generator",
            skill_prompt=skill_prompt,
            references=references,
            voice_profile=voice_profile
        )

    # Helper methods for formatting reference files

    def _format_voice_profile_md(self, voice_profile: VoiceProfile) -> str:
        """Format voice profile as markdown reference file."""

        md = f"""# Voice Profile: {voice_profile.voice_name}

**Genre:** {voice_profile.genre}

## Primary Characteristics

{chr(10).join(f"- {char}" for char in voice_profile.primary_characteristics)}

## Sentence Structure

- **Typical Length:** {voice_profile.sentence_structure.get('typical_length', 'N/A')}
- **Compression Level:** {voice_profile.sentence_structure.get('compression_level', 'N/A')}/10
- **Preferred Patterns:** {', '.join(voice_profile.sentence_structure.get('preferred_patterns', []))}

## Vocabulary

- **Formality:** {voice_profile.vocabulary.get('formality_level', 'N/A')}
- **Complexity:** {voice_profile.vocabulary.get('complexity', 'N/A')}
- **Distinctive Domains:** {', '.join(voice_profile.vocabulary.get('distinctive_domains', []))}

## POV Style

- **Depth:** {voice_profile.pov_style.get('depth', 'N/A')}
- **Consciousness Mode:** {voice_profile.pov_style.get('consciousness_mode_percentage', 'N/A')}
- **Filter Word Tolerance:** {voice_profile.pov_style.get('filter_word_tolerance', 'N/A')}

## Usage

This voice profile defines the target voice for all writing in this project.
Use it to evaluate authenticity and guide revisions.
"""
        return md

    def _format_anti_patterns_md(self, anti_patterns: List[AntiPattern]) -> str:
        """Format anti-patterns as markdown."""

        md = "# Anti-Patterns to Avoid\n\n"

        for ap in anti_patterns:
            md += f"## {ap.name}\n\n"
            md += f"**Severity:** {ap.severity.upper()}\n\n"
            md += f"**Description:** {ap.description}\n\n"
            md += f"**Why Avoid:** {ap.why_avoid}\n\n"

            if ap.regex:
                md += f"**Detection (Regex):** `{ap.regex}`\n\n"
            if ap.keywords:
                md += f"**Detection (Keywords):** {', '.join(ap.keywords)}\n\n"

            if ap.examples:
                md += "**Examples from your writing:**\n"
                for ex in ap.examples:
                    md += f"- _{ex}_\n"
                md += "\n"

            md += "---\n\n"

        return md

    def _format_quality_criteria_md(self, criteria: QualityCriteria) -> str:
        """Format quality criteria as markdown."""

        md = f"# Quality Criteria ({criteria.total_points} points)\n\n"

        for cat in criteria.categories:
            md += f"## {cat['name']} ({cat['points']} points)\n\n"
            md += f"{cat['description']}\n\n"

            if 'sub_criteria' in cat:
                md += "**Sub-criteria:**\n\n"
                for sub in cat['sub_criteria']:
                    md += f"- **{sub['name']}** ({sub['points']} pts): {sub['check']}\n"
                md += "\n"

            md += "---\n\n"

        return md

    def _format_metaphor_domains_md(self, domains: Dict[str, MetaphorDomain]) -> str:
        """Format metaphor domains as markdown."""

        md = "# Metaphor Domains\n\n"

        for name, domain in domains.items():
            md += f"## {name.title()}\n\n"
            md += f"**Max Recommended:** {domain.max_percentage}% of metaphors\n\n"
            md += f"**Keywords:** {', '.join(domain.keywords)}\n\n"
            md += "**Examples from your writing:**\n"
            for ex in domain.examples:
                md += f"- _{ex}_\n"
            md += "\n---\n\n"

        return md

    def _format_fix_patterns_md(self, voice_profile: VoiceProfile) -> str:
        """Format fix patterns for enhancer."""

        md = "# Fix Patterns\n\n"
        md += "Common fixes to apply during enhancement:\n\n"

        for ap in voice_profile.anti_patterns:
            md += f"## Fix: {ap.name}\n\n"
            md += f"**Detection:** {ap.detection_method}\n\n"
            md += f"**Fix Strategy:** Remove or rewrite to avoid {ap.description.lower()}\n\n"
            md += "---\n\n"

        return md


class GeneratedSkill:
    """A generated skill with all its files."""

    def __init__(
        self,
        skill_name: str,
        skill_type: str,
        skill_prompt: str,
        references: Dict[str, str],
        voice_profile: VoiceProfile
    ):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.skill_prompt = skill_prompt
        self.references = references
        self.voice_profile = voice_profile

    def save_to_disk(self, project_dir: Path):
        """
        Save skill to project directory.

        Creates:
        projects/{project_name}/.claude/skills/{skill_name}/
        ├─ SKILL.md
        └─ references/
            ├─ voice-profile.md
            ├─ anti-patterns.md
            └─ ...
        """

        skill_dir = project_dir / ".claude" / "skills" / self.skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        (skill_dir / "SKILL.md").write_text(self.skill_prompt)

        # Write references
        ref_dir = skill_dir / "references"
        ref_dir.mkdir(exist_ok=True)

        for filename, content in self.references.items():
            (ref_dir / filename).write_text(content)
```

**Success Criteria:**
- [ ] Generates 6 skills from VoiceProfile
- [ ] Each skill has custom SKILL.md with project-specific prompts
- [ ] Each skill has references/ with voice-profile.md, anti-patterns.md, etc.
- [ ] Skills saved to correct project directory structure
- [ ] Skills reference project-specific knowledge

---

### Task 14-03: NotebookLM Integration (3-4h)

**Purpose:** Extract knowledge from user's NotebookLM notebooks during setup.

**Implementation:**

**File:** `factory/integrations/notebooklm_setup.py`

```python
from factory.integrations.notebooklm_client import NotebookLMClient

class NotebookLMSetupIntegration:
    """
    Integrates NotebookLM knowledge extraction into project setup.
    """

    def __init__(self):
        self.nlm_client = NotebookLMClient()

    async def extract_project_knowledge(
        self,
        notebooklm_urls: List[str]
    ) -> str:
        """
        Extract relevant knowledge from NotebookLM notebooks.

        Args:
            notebooklm_urls: List of NotebookLM notebook URLs

        Returns:
            Consolidated knowledge context string
        """

        if not notebooklm_urls:
            return ""

        # Queries to extract knowledge
        queries = [
            "Summarize the main characters, their traits, relationships, and arcs.",
            "Describe the story world, settings, and key locations.",
            "What are the main plot threads and themes?",
            "What voice or writing style characteristics are evident?",
            "What are the key metaphors, symbols, or recurring motifs?"
        ]

        knowledge_sections = []

        for url in notebooklm_urls:
            notebook_id = self._extract_notebook_id(url)

            for query in queries:
                response = await self.nlm_client.query(
                    notebook_id=notebook_id,
                    query=query
                )

                knowledge_sections.append(f"## {query}\n\n{response}\n")

        return "\n".join(knowledge_sections)

    def _extract_notebook_id(self, url: str) -> str:
        """Extract notebook ID from NotebookLM URL."""
        # URL format: https://notebooklm.google.com/notebook/{id}
        return url.split("/")[-1]
```

**Success Criteria:**
- [ ] Can extract knowledge from NotebookLM URLs
- [ ] Queries for characters, world, plot, voice, themes
- [ ] Returns consolidated context string
- [ ] Used in voice analysis and skill generation

---

### Task 14-04: Project Structure Creator (2-3h)

**Purpose:** Create complete project directory structure with all files.

**Implementation:**

**File:** `factory/core/project_creator.py`

```python
from pathlib import Path
import json
from typing import Dict, List
from .skill_generator import GeneratedSkill
from .voice_extractor import VoiceProfile

class ProjectCreator:
    """
    Creates complete project structure for a new novel project.
    """

    def __init__(self, projects_root: Path):
        self.projects_root = projects_root

    def create_project(
        self,
        project_name: str,
        voice_profile: VoiceProfile,
        generated_skills: Dict[str, GeneratedSkill],
        notebooklm_context: str = "",
        uploaded_docs: List[Dict] = None
    ) -> Path:
        """
        Create complete project structure.

        Creates:
        projects/{project_name}/
        ├─ .claude/
        │   └─ skills/
        │       ├─ scene-analyzer-{project}/
        │       ├─ scene-enhancer-{project}/
        │       └─ ... (4 more)
        ├─ knowledge/
        │   └─ craft/
        │       └─ voice-gold-standard.md (project-specific)
        ├─ scenes/
        ├─ config.json
        └─ README.md
        """

        project_dir = self.projects_root / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create .claude/skills/
        for skill_type, skill in generated_skills.items():
            skill.save_to_disk(project_dir)

        # Create knowledge/
        self._create_knowledge_base(project_dir, voice_profile, notebooklm_context)

        # Create scenes/
        (project_dir / "scenes").mkdir(exist_ok=True)

        # Create config.json
        self._create_config(project_dir, project_name, voice_profile, generated_skills)

        # Create README.md
        self._create_readme(project_dir, project_name, voice_profile)

        # Copy uploaded docs
        if uploaded_docs:
            self._save_uploaded_docs(project_dir, uploaded_docs)

        return project_dir

    def _create_knowledge_base(
        self,
        project_dir: Path,
        voice_profile: VoiceProfile,
        notebooklm_context: str
    ):
        """Create project-specific knowledge base."""

        kb_dir = project_dir / "knowledge" / "craft"
        kb_dir.mkdir(parents=True, exist_ok=True)

        # voice-gold-standard.md (project-specific)
        voice_gold_standard = f"""# {voice_profile.voice_name} - Voice Gold Standard

## Core Principle: Voice Authenticity

This project's voice is: **{voice_profile.voice_name}**

{chr(10).join(f"- {char}" for char in voice_profile.primary_characteristics)}

## Voice Characteristics

### Sentence Structure
{voice_profile.sentence_structure}

### Vocabulary
{voice_profile.vocabulary}

### POV Style
{voice_profile.pov_style}

## Voice Consistency Tests

Use the scene-analyzer-{project_dir.name} skill to check voice authenticity.
"""
        (kb_dir / "voice-gold-standard.md").write_text(voice_gold_standard)

        # story-context.md (from NotebookLM)
        if notebooklm_context:
            (kb_dir / "story-context.md").write_text(
                f"# Story Context\n\n{noteboomlm_context}"
            )

    def _create_config(
        self,
        project_dir: Path,
        project_name: str,
        voice_profile: VoiceProfile,
        generated_skills: Dict[str, GeneratedSkill]
    ):
        """Create project config.json."""

        config = {
            "project_name": project_name,
            "project_id": project_name,
            "created_at": datetime.now().isoformat(),
            "voice_profile": {
                "name": voice_profile.voice_name,
                "genre": voice_profile.genre
            },
            "skills": {
                skill_type: skill.skill_name
                for skill_type, skill in generated_skills.items()
            },
            "directory_structure": {
                "skills": ".claude/skills/",
                "knowledge": "knowledge/",
                "scenes": "scenes/"
            }
        }

        (project_dir / "config.json").write_text(json.dumps(config, indent=2))

    def _create_readme(
        self,
        project_dir: Path,
        project_name: str,
        voice_profile: VoiceProfile
    ):
        """Create project README.md."""

        readme = f"""# {project_name}

**Voice:** {voice_profile.voice_name}
**Genre:** {voice_profile.genre}

## Custom Skills

This project has 6 custom AI skills generated specifically for your voice:

- `scene-analyzer-{project_name}`: Score scenes 0-100 using your quality criteria
- `scene-enhancer-{project_name}`: Make surgical fixes to match your voice
- `character-validator-{project_name}`: Check character consistency
- `scene-writer-{project_name}`: Write new scenes in your voice
- `scene-multiplier-{project_name}`: Generate 5 variations of a scene
- `scaffold-generator-{project_name}`: Expand outlines using your story knowledge

## Usage

Access skills through Writers Factory Craft Panel or Claude Code:

```bash
claude skill scene-analyzer-{project_name} "path/to/scene.md"
```

## Project Structure

- `.claude/skills/` - Your 6 custom skills
- `knowledge/` - Voice profile, story context
- `scenes/` - Your manuscript scenes
"""
        (project_dir / "README.md").write_text(readme)

    def _save_uploaded_docs(self, project_dir: Path, uploaded_docs: List[Dict]):
        """Save uploaded reference documents."""

        docs_dir = project_dir / "references"
        docs_dir.mkdir(exist_ok=True)

        for doc in uploaded_docs:
            filename = doc["filename"]
            content = doc["content"]
            (docs_dir / filename).write_text(content)
```

**Success Criteria:**
- [ ] Creates complete project directory structure
- [ ] Saves all 6 generated skills
- [ ] Creates project-specific knowledge base
- [ ] Generates config.json with project metadata
- [ ] Creates helpful README.md

---

### Task 14-05: Skill Registry Updates (2-3h)

**Purpose:** Update skill registry to support project-specific skills.

**Implementation:**

**File:** `factory/core/skill_orchestrator.py` (updates)

```python
class SkillOrchestrator:
    """
    Routes skill requests to correct provider.
    NOW supports project-specific skills.
    """

    def __init__(self):
        self.global_skills = {}  # Global/template skills
        self.project_skills = {}  # project_id -> {skill_type -> skill_instance}
        self.providers = [
            MCPSkillBridge(),
            NativeSkillProvider()
        ]

    def register_project_skills(
        self,
        project_id: str,
        skills: Dict[str, GeneratedSkill]
    ):
        """
        Register project-specific skills.

        Args:
            project_id: Project identifier
            skills: Dictionary of skill_type -> GeneratedSkill
        """

        if project_id not in self.project_skills:
            self.project_skills[project_id] = {}

        for skill_type, skill in skills.items():
            self.project_skills[project_id][skill_type] = skill

    async def execute_skill(
        self,
        skill_type: str,
        input_data: Dict[str, Any],
        project_id: str = None
    ) -> Dict[str, Any]:
        """
        Execute a skill.

        Args:
            skill_type: "scene-analyzer", "scene-enhancer", etc.
            input_data: Skill input
            project_id: Optional project ID for project-specific skills

        Returns:
            Skill execution result
        """

        # Route to project-specific skill if project_id provided
        if project_id and project_id in self.project_skills:
            if skill_type in self.project_skills[project_id]:
                return await self._execute_project_skill(
                    project_id,
                    skill_type,
                    input_data
                )

        # Fall back to global skills
        return await self._execute_global_skill(skill_type, input_data)

    async def _execute_project_skill(
        self,
        project_id: str,
        skill_type: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute project-specific skill."""

        skill = self.project_skills[project_id][skill_type]

        # Use Claude Code to execute the skill
        # (Skills are Claude Code skills stored in project .claude/skills/)

        result = subprocess.run(
            ["claude", "skill", skill.skill_name, json.dumps(input_data)],
            capture_output=True,
            text=True
        )

        return json.loads(result.stdout)

    def list_project_skills(self, project_id: str) -> List[Dict[str, Any]]:
        """List all skills for a project."""

        if project_id not in self.project_skills:
            return []

        skills = []
        for skill_type, skill in self.project_skills[project_id].items():
            skills.append({
                "skill_name": skill.skill_name,
                "skill_type": skill_type,
                "voice_profile": skill.voice_profile.voice_name
            })

        return skills
```

**Success Criteria:**
- [ ] Skill orchestrator supports project_id parameter
- [ ] Routes to project-specific skills when project_id provided
- [ ] Falls back to global skills if no project_id
- [ ] Can list all skills for a project
- [ ] Integration with existing Sprint 12 infrastructure

---

## Phase B: Frontend - Setup Wizard UI (10-12h)

### Task 14-06: Wizard UI Components (5-6h)

**Purpose:** Multi-step wizard interface for project setup.

**Implementation:**

**File:** `webapp/frontend-v2/src/features/setup/SetupWizard.jsx`

```jsx
import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Button, Box } from '@mui/material';

const STEPS = [
  'Project Details',
  'Voice Input',
  'Reference Materials',
  'AI Analysis',
  'Review & Test',
  'Finalize'
];

export function SetupWizard() {
  const [activeStep, setActiveStep] = useState(0);
  const [projectData, setProjectData] = useState({
    name: '',
    genre: '',
    goals: '',
    examplePassages: [],
    uploadedDocs: [],
    notebooklmUrls: [],
    styleGuide: '',
    antiPatterns: []
  });

  const handleNext = () => {
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return <ProjectDetailsStep data={projectData} setData={setProjectData} />;
      case 1:
        return <VoiceInputStep data={projectData} setData={setProjectData} />;
      case 2:
        return <ReferenceMaterialsStep data={projectData} setData={setProjectData} />;
      case 3:
        return <AIAnalysisStep data={projectData} />;
      case 4:
        return <ReviewStep data={projectData} />;
      case 5:
        return <FinalizeStep data={projectData} />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ width: '100%', p: 4 }}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {STEPS.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Box sx={{ mt: 4, minHeight: '400px' }}>
        {renderStepContent(activeStep)}
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
        >
          Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={activeStep === STEPS.length - 1}
        >
          {activeStep === STEPS.length - 2 ? 'Create Project' : 'Next'}
        </Button>
      </Box>
    </Box>
  );
}
```

**Step 1: Project Details**

```jsx
function ProjectDetailsStep({ data, setData }) {
  return (
    <Box>
      <TextField
        label="Project Name"
        value={data.name}
        onChange={(e) => setData({ ...data, name: e.target.value })}
        fullWidth
        sx={{ mb: 2 }}
      />

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Genre</InputLabel>
        <Select
          value={data.genre}
          onChange={(e) => setData({ ...data, genre: e.target.value })}
        >
          <MenuItem value="literary">Literary Fiction</MenuItem>
          <MenuItem value="thriller">Thriller</MenuItem>
          <MenuItem value="romance">Romance</MenuItem>
          <MenuItem value="scifi">Science Fiction</MenuItem>
          <MenuItem value="fantasy">Fantasy</MenuItem>
          <MenuItem value="mystery">Mystery</MenuItem>
          <MenuItem value="other">Other</MenuItem>
        </Select>
      </FormControl>

      <TextField
        label="Project Goals"
        value={data.goals}
        onChange={(e) => setData({ ...data, goals: e.target.value })}
        multiline
        rows={4}
        fullWidth
        placeholder="What are you trying to achieve with this novel?"
      />
    </Box>
  );
}
```

**Step 2: Voice Input**

```jsx
function VoiceInputStep({ data, setData }) {
  const [currentPassage, setCurrentPassage] = useState('');

  const addPassage = () => {
    if (currentPassage.trim()) {
      setData({
        ...data,
        examplePassages: [...data.examplePassages, currentPassage]
      });
      setCurrentPassage('');
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Provide 3-5 Example Passages (500-1000 words each)
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Paste scenes from your novel that best represent your voice.
      </Typography>

      <TextField
        value={currentPassage}
        onChange={(e) => setCurrentPassage(e.target.value)}
        multiline
        rows={10}
        fullWidth
        placeholder="Paste a scene excerpt here..."
        sx={{ mb: 2 }}
      />

      <Button onClick={addPassage} variant="outlined">
        Add Passage ({data.examplePassages.length}/5)
      </Button>

      {data.examplePassages.length > 0 && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1">Added Passages:</Typography>
          {data.examplePassages.map((passage, i) => (
            <Chip
              key={i}
              label={`Passage ${i + 1} (${passage.split(' ').length} words)`}
              onDelete={() => {
                setData({
                  ...data,
                  examplePassages: data.examplePassages.filter((_, idx) => idx !== i)
                });
              }}
              sx={{ mr: 1, mt: 1 }}
            />
          ))}
        </Box>
      )}

      <Divider sx={{ my: 4 }} />

      <Typography variant="h6" gutterBottom>
        NotebookLM Integration (Optional)
      </Typography>
      <TextField
        label="NotebookLM Notebook URL"
        placeholder="https://notebooklm.google.com/notebook/..."
        fullWidth
        onBlur={(e) => {
          if (e.target.value) {
            setData({
              ...data,
              notebooklmUrls: [...data.notebooklmUrls, e.target.value]
            });
            e.target.value = '';
          }
        }}
      />
    </Box>
  );
}
```

**Step 3: Reference Materials**

```jsx
function ReferenceMaterialsStep({ data, setData }) {
  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (event) => {
        setData({
          ...data,
          uploadedDocs: [
            ...data.uploadedDocs,
            {
              filename: file.name,
              content: event.target.result,
              type: file.type
            }
          ]
        });
      };
      reader.readAsText(file);
    });
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Upload Reference Materials (Optional)
      </Typography>

      <Button
        variant="outlined"
        component="label"
        sx={{ mb: 2 }}
      >
        Upload Files
        <input
          type="file"
          hidden
          multiple
          accept=".md,.txt,.docx,.pdf"
          onChange={handleFileUpload}
        />
      </Button>

      {data.uploadedDocs.length > 0 && (
        <List>
          {data.uploadedDocs.map((doc, i) => (
            <ListItem key={i}>
              <ListItemText primary={doc.filename} secondary={doc.type} />
              <IconButton onClick={() => {
                setData({
                  ...data,
                  uploadedDocs: data.uploadedDocs.filter((_, idx) => idx !== i)
                });
              }}>
                <DeleteIcon />
              </IconButton>
            </ListItem>
          ))}
        </List>
      )}

      <Divider sx={{ my: 4 }} />

      <TextField
        label="Style Guide / Anti-Patterns"
        value={data.styleGuide}
        onChange={(e) => setData({ ...data, styleGuide: e.target.value })}
        multiline
        rows={6}
        fullWidth
        placeholder="Describe patterns you want to AVOID in your writing..."
      />
    </Box>
  );
}
```

**Step 4: AI Analysis**

```jsx
function AIAnalysisStep({ data }) {
  const [analyzing, setAnalyzing] = useState(false);
  const [voiceProfile, setVoiceProfile] = useState(null);

  useEffect(() => {
    analyzeVoice();
  }, []);

  const analyzeVoice = async () => {
    setAnalyzing(true);

    const response = await fetch('/api/setup/analyze-voice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        examplePassages: data.examplePassages,
        uploadedDocs: data.uploadedDocs,
        notebooklmUrls: data.notebooklmUrls,
        styleGuide: data.styleGuide,
        genre: data.genre
      })
    });

    const result = await response.json();
    setVoiceProfile(result.voice_profile);
    setAnalyzing(false);
  };

  if (analyzing) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Analyzing your voice...
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This may take 1-2 minutes
        </Typography>
      </Box>
    );
  }

  if (!voiceProfile) return null;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Voice Profile: {voiceProfile.voice_name}
      </Typography>

      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6">Primary Characteristics</Typography>
          <List>
            {voiceProfile.primary_characteristics.map((char, i) => (
              <ListItem key={i}>
                <ListItemText primary={char} />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Sentence Structure</Typography>
              <Typography>Length: {voiceProfile.sentence_structure.typical_length}</Typography>
              <Typography>Compression: {voiceProfile.sentence_structure.compression_level}/10</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">POV Style</Typography>
              <Typography>Depth: {voiceProfile.pov_style.depth}</Typography>
              <Typography>Consciousness: {voiceProfile.pov_style.consciousness_mode_percentage}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6">Metaphor Domains</Typography>
          {Object.entries(voiceProfile.metaphor_domains).map(([name, domain]) => (
            <Box key={name} sx={{ mb: 1 }}>
              <Typography variant="subtitle2">{name}: {domain.max_percentage}%</Typography>
              <Typography variant="caption" color="text.secondary">
                {domain.keywords.join(', ')}
              </Typography>
            </Box>
          ))}
        </CardContent>
      </Card>
    </Box>
  );
}
```

**Step 5: Review & Test**

```jsx
function ReviewStep({ data }) {
  const [generatingSkills, setGeneratingSkills] = useState(false);
  const [generatedSkills, setGeneratedSkills] = useState(null);
  const [testScene, setTestScene] = useState('');
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    generateSkills();
  }, []);

  const generateSkills = async () => {
    setGeneratingSkills(true);

    const response = await fetch('/api/setup/generate-skills', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    setGeneratedSkills(result.skills);
    setGeneratingSkills(false);
  };

  const testAnalyzer = async () => {
    const response = await fetch('/api/setup/test-skill', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: data.name,
        skill_type: 'scene-analyzer',
        test_scene: testScene
      })
    });

    const result = await response.json();
    setTestResult(result);
  };

  if (generatingSkills) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Generating your 6 custom skills...
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This may take 2-3 minutes
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Skills Generated!
      </Typography>

      <List>
        {Object.entries(generatedSkills).map(([type, skill]) => (
          <ListItem key={type}>
            <ListItemIcon>
              <CheckCircleIcon color="success" />
            </ListItemIcon>
            <ListItemText
              primary={skill.skill_name}
              secondary={`${type} - Ready to use`}
            />
          </ListItem>
        ))}
      </List>

      <Divider sx={{ my: 4 }} />

      <Typography variant="h6" gutterBottom>
        Test Your Scene Analyzer
      </Typography>

      <TextField
        value={testScene}
        onChange={(e) => setTestScene(e.target.value)}
        multiline
        rows={8}
        fullWidth
        placeholder="Paste a scene to test..."
        sx={{ mb: 2 }}
      />

      <Button onClick={testAnalyzer} variant="outlined" disabled={!testScene}>
        Test Analyzer
      </Button>

      {testResult && (
        <Card sx={{ mt: 2 }}>
          <CardContent>
            <Typography variant="h6">Score: {testResult.total_score}/100</Typography>
            <Typography variant="subtitle1">Quality: {testResult.quality_tier}</Typography>
            {/* Display detailed results */}
          </CardContent>
        </Card>
      )}
    </Box>
  );
}
```

**Success Criteria:**
- [ ] 6-step wizard with clear progress indicator
- [ ] Step 1: Collect project details and genre
- [ ] Step 2: Collect voice input (passages, NotebookLM links)
- [ ] Step 3: Upload reference materials
- [ ] Step 4: Display AI analysis results
- [ ] Step 5: Show generated skills and test analyzer
- [ ] Step 6: Finalize and create project
- [ ] Clean, professional UI using Material-UI

---

### Task 14-07: Backend API Endpoints (3-4h)

**Purpose:** API endpoints for setup wizard workflow.

**Implementation:**

**File:** `webapp/backend/setup_api.py`

```python
from fastapi import APIRouter, UploadFile, File
from typing import List
from factory.core.voice_extractor import VoiceProfileExtractor
from factory.core.skill_generator import SkillGenerator
from factory.core.project_creator import ProjectCreator
from factory.integrations.notebooklm_setup import NotebookLMSetupIntegration

router = APIRouter(prefix="/api/setup", tags=["setup"])

@router.post("/analyze-voice")
async def analyze_voice(request: dict):
    """
    Analyze voice from example passages and uploaded docs.

    Request body:
    {
      "examplePassages": ["passage1", "passage2", ...],
      "uploadedDocs": [{"filename": "...", "content": "..."}],
      "notebooklmUrls": ["url1", "url2"],
      "styleGuide": "...",
      "genre": "literary"
    }

    Returns:
    {
      "voice_profile": {...}
    }
    """

    extractor = VoiceProfileExtractor(anthropic_client)

    # Extract NotebookLM context
    notebooklm_context = ""
    if request.get("notebooklmUrls"):
        nlm_integration = NotebookLMSetupIntegration()
        notebooklm_context = await nlm_integration.extract_project_knowledge(
            request["notebooklmUrls"]
        )

    # Extract voice profile
    voice_profile = await extractor.extract_voice_profile(
        example_passages=request["examplePassages"],
        uploaded_docs=request.get("uploadedDocs", []),
        notebooklm_context=notebooklm_context
    )

    return {
        "voice_profile": voice_profile.__dict__
    }


@router.post("/generate-skills")
async def generate_skills(request: dict):
    """
    Generate 6 custom skills for project.

    Request body:
    {
      "name": "project-name",
      "genre": "literary",
      "examplePassages": [...],
      "uploadedDocs": [...],
      "notebooklmUrls": [...],
      ...
    }

    Returns:
    {
      "skills": {
        "scene-analyzer": {...},
        "scene-enhancer": {...},
        ...
      }
    }
    """

    # Re-extract voice profile (or retrieve from cache)
    extractor = VoiceProfileExtractor(anthropic_client)

    notebooklm_context = ""
    if request.get("notebooklmUrls"):
        nlm_integration = NotebookLMSetupIntegration()
        notebooklm_context = await nlm_integration.extract_project_knowledge(
            request["notebooklmUrls"]
        )

    voice_profile = await extractor.extract_voice_profile(
        example_passages=request["examplePassages"],
        uploaded_docs=request.get("uploadedDocs", []),
        notebooklm_context=notebooklm_context
    )

    # Generate skills
    generator = SkillGenerator(anthropic_client)
    skills = await generator.generate_project_skills(
        project_name=request["name"],
        voice_profile=voice_profile,
        notebooklm_context=notebooklm_context
    )

    return {
        "skills": {
            skill_type: {
                "skill_name": skill.skill_name,
                "skill_type": skill.skill_type
            }
            for skill_type, skill in skills.items()
        }
    }


@router.post("/test-skill")
async def test_skill(request: dict):
    """
    Test a generated skill on sample scene.

    Request body:
    {
      "project_id": "my-novel",
      "skill_type": "scene-analyzer",
      "test_scene": "scene content..."
    }

    Returns:
    {
      "total_score": 85,
      "quality_tier": "Professional",
      ...
    }
    """

    orchestrator = get_skill_orchestrator()

    result = await orchestrator.execute_skill(
        skill_type=request["skill_type"],
        input_data={"scene_content": request["test_scene"]},
        project_id=request["project_id"]
    )

    return result


@router.post("/create-project")
async def create_project(request: dict):
    """
    Finalize and create project structure.

    Creates:
    - projects/{project_name}/ directory
    - All 6 skills
    - Knowledge base
    - Config files

    Returns:
    {
      "project_id": "my-novel",
      "project_path": "/path/to/projects/my-novel",
      "skills": [...]
    }
    """

    # Re-generate everything (or retrieve from temp storage)
    extractor = VoiceProfileExtractor(anthropic_client)
    generator = SkillGenerator(anthropic_client)
    creator = ProjectCreator(projects_root=Path("projects"))

    # Extract voice
    notebooklm_context = ""
    if request.get("notebooklmUrls"):
        nlm_integration = NotebookLMSetupIntegration()
        notebooklm_context = await nlm_integration.extract_project_knowledge(
            request["notebooklmUrls"]
        )

    voice_profile = await extractor.extract_voice_profile(
        example_passages=request["examplePassages"],
        uploaded_docs=request.get("uploadedDocs", []),
        notebooklm_context=notebooklm_context
    )

    # Generate skills
    skills = await generator.generate_project_skills(
        project_name=request["name"],
        voice_profile=voice_profile,
        notebooklm_context=notebooklm_context
    )

    # Create project
    project_dir = creator.create_project(
        project_name=request["name"],
        voice_profile=voice_profile,
        generated_skills=skills,
        notebooklm_context=notebooklm_context,
        uploaded_docs=request.get("uploadedDocs", [])
    )

    # Register skills with orchestrator
    orchestrator = get_skill_orchestrator()
    orchestrator.register_project_skills(
        project_id=request["name"],
        skills=skills
    )

    return {
        "project_id": request["name"],
        "project_path": str(project_dir),
        "skills": [skill.skill_name for skill in skills.values()]
    }
```

**Success Criteria:**
- [ ] POST /api/setup/analyze-voice endpoint
- [ ] POST /api/setup/generate-skills endpoint
- [ ] POST /api/setup/test-skill endpoint
- [ ] POST /api/setup/create-project endpoint
- [ ] All endpoints integrated with Phase A backend
- [ ] Error handling and validation

---

### Task 14-08: Template Skills (2h)

**Purpose:** Create base templates for skill generation.

**Implementation:**

Create generic templates that LLM customizes:

**File:** `factory/knowledge/templates/scene-analyzer-template.md`

```markdown
# Scene Analyzer - {{PROJECT_NAME}}

**Version:** 1.0
**Voice:** {{VOICE_NAME}}
**Genre:** {{GENRE}}

## Purpose

Analyzes scenes from {{PROJECT_NAME}} and scores them 0-100 using project-specific quality criteria.

## Scoring Criteria (100 points total)

{{QUALITY_CRITERIA}}

## Voice Profile

{{VOICE_CHARACTERISTICS}}

## Anti-Patterns

Detect and flag these patterns:

{{ANTI_PATTERNS}}

## Metaphor Domains

Monitor metaphor distribution:

{{METAPHOR_DOMAINS}}

## Analysis Process

1. **Read scene completely**
2. **Voice authentication**: Does this sound like {{VOICE_NAME}}?
3. **Score each category** using criteria above
4. **Detect anti-patterns**
5. **Check metaphor distribution**
6. **Generate fixes** for issues found
7. **Assign quality tier**: Learning (0-59), Professional (60-79), Publication-Ready (80-89), Gold Standard (90-100)

## Output Format

```json
{
  "total_score": 85,
  "quality_tier": "Professional",
  "category_scores": {...},
  "anti_patterns_found": [...],
  "metaphor_distribution": {...},
  "fixes": [...]
}
```

## References

- `references/voice-profile.md` - Complete voice profile
- `references/anti-patterns.md` - Full anti-pattern list
- `references/quality-criteria.md` - Detailed scoring rubric
- `references/metaphor-domains.md` - Metaphor guidelines
```

Similar templates for other 5 skills:
- `scene-enhancer-template.md`
- `character-validator-template.md`
- `scene-writer-template.md`
- `scene-multiplier-template.md`
- `scaffold-generator-template.md`

**Success Criteria:**
- [ ] 6 template SKILL.md files created
- [ ] Templates have placeholders for customization
- [ ] Templates follow Claude Code skill format
- [ ] LLM can successfully customize templates

---

## Testing & Validation (2-3h)

### Task 14-09: End-to-End Testing

**Test Cases:**

1. **Create The Explants Project (Migration)**
   - Run setup wizard using existing Explants materials
   - Verify 6 skills generated correctly
   - Compare with original hardcoded skills
   - Ensure feature parity

2. **Create Romance Novel Project**
   - Different genre, different voice
   - Upload romance style guide
   - Verify skills customized for romance conventions

3. **Create Thriller Project**
   - Test with minimal inputs (no NotebookLM, no uploads)
   - Verify wizard handles sparse data gracefully

**Success Criteria:**
- [ ] Can create projects for all genres
- [ ] Generated skills work correctly
- [ ] Voice analysis accurate
- [ ] Skills properly registered and routable
- [ ] No conflicts between project-specific skills

---

## Documentation (1-2h)

### Task 14-10: User Documentation

**Create:**

1. **Setup Wizard Guide** (`docs/setup-wizard.md`)
   - Step-by-step walkthrough
   - Best practices for voice input
   - Tips for NotebookLM integration

2. **Project Structure Documentation** (`docs/project-structure.md`)
   - Explain directory layout
   - How to update skills
   - How to add reference materials

3. **Video Tutorial** (optional)
   - Screen recording of setup process
   - 5-10 minutes

**Success Criteria:**
- [ ] Complete setup wizard guide
- [ ] Project structure documented
- [ ] Examples for multiple genres

---

## Sprint 14 Completion Checklist

**Phase A: Backend (15-18h)**
- [ ] Task 14-01: Voice Profile Extractor working
- [ ] Task 14-02: Skill Generator creating 6 skills
- [ ] Task 14-03: NotebookLM integration functional
- [ ] Task 14-04: Project Creator building correct structure
- [ ] Task 14-05: Skill Registry supporting project_id routing

**Phase B: Frontend (10-12h)**
- [ ] Task 14-06: 6-step wizard UI complete
- [ ] Task 14-07: API endpoints functional
- [ ] Task 14-08: Template skills created

**Testing & Docs (3-5h)**
- [ ] Task 14-09: E2E tests passing for 3+ projects
- [ ] Task 14-10: Documentation complete

**Final Validation:**
- [ ] Created The Explants project via wizard (migration test)
- [ ] Created Romance project via wizard
- [ ] Created Thriller project via wizard
- [ ] All 3 projects have 6 working skills
- [ ] Skills correctly differentiated by voice/genre
- [ ] January students can use wizard to set up their novels

---

## Integration with Existing Sprints

**Dependencies:**
- Sprint 11 (NotebookLM): ✅ Complete
- Sprint 12 (Skill Orchestration): ✅ Complete

**Updates Required:**
- Sprint 12 Skill Orchestrator: Add project_id routing (Task 14-05)
- Sprint 13 Novel Intelligence: Use project-specific skills when analyzing

**Migration Path:**
- Existing Explants skills remain as fallback
- New projects created via wizard
- Eventually migrate Explants to wizard-created structure

---

## Success Metrics

**Quantitative:**
- 6 skills generated per project
- < 5 minutes total setup time
- Voice analysis accuracy > 90% (subjective but testable)
- Zero skill conflicts between projects

**Qualitative:**
- Writers feel skills match their voice
- Skills provide useful feedback
- Setup process intuitive
- Students can complete setup without help

---

## Post-Sprint 14: What's Now Possible

✅ **January students** can set up novels with custom skills
✅ **Multi-project support** - unlimited concurrent projects
✅ **Genre flexibility** - works for any fiction genre
✅ **Voice authenticity** - skills match each writer's voice
✅ **Platform scalability** - foundation for thousands of writers
✅ **Skill marketplace** - writers can share templates (future)

---

## Let's Build This NOW!

This is THE critical piece. Without it, Writers Factory is a single-user tool. With it, it's a PLATFORM.

Cloud Agent: Start with Task 14-01 (Voice Profile Extractor).

Everything you need is in this spec. Let's make Writers Factory work for EVERY writer, not just The Explants.

🚀 **GO!** 🚀
