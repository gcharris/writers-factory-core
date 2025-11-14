"""Simplified FastAPI backend for Writers Factory web interface.

Now connected to real AI agents (Phase 3).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel
import sys

# Add factory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from factory.core.config.loader import load_agent_config, get_enabled_agents
from webapp.backend.agent_integration import get_bridge
from factory.core.manuscript import Manuscript, ManuscriptStorage
from factory.agents.ollama_agent import OllamaAgent
from factory.agents.character_analyzer import (
    analyze_character_depth,
    analyze_protagonist_dimensionality
)
from factory.research.notebooklm_client import (
    NotebookLMClient,
    AuthenticationError,
    NotebookNotFoundError,
    QueryTimeoutError
)
from factory.core.skill_orchestrator import (
    SkillOrchestrator,
    SkillRequest,
    SkillProvider,
    SkillStatus
)
import json
import uuid
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Writers Factory",
    description="Multi-model AI novel writing system",
    version="0.3.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
project_path = Path.cwd() / "project"
project_path.mkdir(parents=True, exist_ok=True)

# Manuscript cache
_manuscript_cache = {}

# Session cost tracking
_session_cost = {"total": 0.0, "by_model": [], "savings": 0.0}

# NotebookLM client (Sprint 11)
notebooklm_client = NotebookLMClient()

# Skill Orchestrator (Sprint 12)
skill_orchestrator = SkillOrchestrator(
    user_tier="premium",  # TODO: Get from user session
    knowledge_path=project_path / "knowledge"
)


# Economy Mode Helper
def select_agent_for_task(task_type: str, economy_mode: bool = False) -> str:
    """Select the best agent for a task based on economy mode.

    Args:
        task_type: Type of task ('draft', 'polish', 'dialogue', 'brainstorm', 'enhance')
        economy_mode: If True, prefer local models for cost savings

    Returns:
        Agent name (model ID)
    """
    agents = get_enabled_agents()

    # Get local and cloud models
    local_models = [name for name, config in agents.items() if config.get("is_local", False)]
    cloud_models = [name for name, config in agents.items() if not config.get("is_local", False)]

    if economy_mode and local_models:
        # Prefer local models for economy mode
        if task_type in ["draft", "brainstorm", "dialogue"]:
            # Use fastest local model for drafts/brainstorming
            return local_models[0] if local_models else cloud_models[0]
        elif task_type in ["enhance", "polish"]:
            # Use best local model (mistral if available)
            for model in local_models:
                if "mistral" in model.lower():
                    return model
            return local_models[0] if local_models else cloud_models[0]

    # Default to best cloud model for quality
    if task_type == "polish":
        # Use best quality for polish
        for model in cloud_models:
            if "opus" in model.lower() or "sonnet-4.5" in model.lower():
                return model

    # Default to first available cloud model
    return cloud_models[0] if cloud_models else (local_models[0] if local_models else "claude-sonnet-4.5")


# Request/Response Models
class WizardStartRequest(BaseModel):
    project_name: str


class ModelComparisonRequest(BaseModel):
    prompt: str
    models: List[str]


# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.3.0",
        "project_path": str(project_path)
    }


# Wizard Endpoints (Simplified - returns mock data for now)
@app.post("/api/wizard/start")
async def wizard_start(request: WizardStartRequest):
    """Start a new creation wizard session."""
    try:
        wizard_project_path = project_path / request.project_name
        wizard_project_path.mkdir(parents=True, exist_ok=True)

        # Return first question
        return {
            "success": True,
            "project_name": request.project_name,
            "current_phase": "foundation",
            "question": "What genre is your story? (e.g., science fiction, fantasy, thriller, literary fiction)",
            "progress": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start wizard: {str(e)}")


@app.post("/api/wizard/answer")
async def wizard_answer(request: dict):
    """Submit an answer to the wizard."""
    # Simplified - just return next question
    return {
        "success": True,
        "complete": False,
        "question": "What is the central theme or message of your story?",
        "current_phase": "foundation",
        "progress": 10
    }


@app.get("/api/wizard/progress")
async def wizard_progress():
    """Get current wizard progress."""
    return {
        "active": False
    }


# Manuscript Endpoints
@app.get("/api/manuscript/tree")
async def get_manuscript_tree():
    """Get hierarchical manuscript structure."""
    try:
        manuscript_path = project_path / ".manuscript" / "explants-v1"

        # Check if manuscript exists
        if not manuscript_path.exists():
            return {"acts": []}

        # Load manuscript
        storage = ManuscriptStorage(manuscript_path)
        manuscript = storage.load()

        if not manuscript:
            return {"acts": []}

        # Cache it
        _manuscript_cache['current'] = manuscript

        # Return tree structure
        return {
            "title": manuscript.title,
            "acts": [
                {
                    "id": act.id,
                    "title": act.title,
                    "chapters": [
                        {
                            "id": chapter.id,
                            "title": chapter.title,
                            "scenes": [
                                {
                                    "id": scene.id,
                                    "title": scene.title,
                                    "word_count": scene.word_count
                                }
                                for scene in chapter.scenes
                            ]
                        }
                        for chapter in act.chapters
                    ]
                }
                for act in manuscript.acts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load manuscript: {str(e)}")


@app.get("/api/scene/{scene_id}")
async def get_scene(scene_id: str):
    """Get specific scene content."""
    try:
        manuscript = _manuscript_cache.get('current')

        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find scene by ID
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    if scene.id == scene_id:
                        return {
                            "id": scene.id,
                            "title": scene.title,
                            "content": scene.content,
                            "word_count": scene.word_count,
                            "notes": scene.notes,
                            "metadata": scene.metadata
                        }

        raise HTTPException(status_code=404, detail="Scene not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/scene/{scene_id}")
async def update_scene(scene_id: str, request: dict):
    """Update scene content (for autosave).

    NEW BEHAVIOR (Sprint 9): Writes directly to .md file
    """
    try:
        content = request.get("content", "")

        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Update content directly to file (Sprint 9)
        manuscript_path = project_path / ".manuscript" / "explants-v1"
        storage = ManuscriptStorage(manuscript_path)
        success = storage.save_scene(manuscript, scene_id, content)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save scene to file")

        # Get updated scene for word count
        scene = manuscript.get_scene(scene_id)
        if not scene:
            raise HTTPException(status_code=404, detail="Scene not found")

        return {
            "success": True,
            "word_count": scene.word_count,
            "saved_at": "now"
        }

        raise HTTPException(status_code=404, detail="Scene not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Model Comparison Endpoints
@app.post("/api/compare")
async def compare_models(request: ModelComparisonRequest):
    """Compare multiple models on the same prompt."""
    try:
        if len(request.models) < 2:
            raise HTTPException(status_code=400, detail="At least 2 models required")

        if len(request.models) > 4:
            raise HTTPException(status_code=400, detail="Maximum 4 models allowed")

        # Get agent bridge
        bridge = get_bridge(project_path)

        # Run real comparison
        result = await bridge.compare_models(
            prompt=request.prompt,
            models=request.models,
        )

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Comparison failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/available")
async def get_available_models():
    """Get list of all available models."""
    try:
        agents = get_enabled_agents()
        models = []

        for agent_name, agent_config in agents.items():
            models.append({
                "id": agent_name,
                "provider": agent_config.get("provider"),
                "description": agent_config.get("description"),
                "cost_input": agent_config.get("cost_per_1k_input"),
                "cost_output": agent_config.get("cost_per_1k_output"),
                "strengths": agent_config.get("strengths", []),
                "is_local": agent_config.get("is_local", False),  # NEW
                "endpoint": agent_config.get("endpoint")
            })

        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load models: {str(e)}")


@app.get("/api/models/groups")
async def get_model_groups():
    """Get predefined model groups."""
    try:
        config = load_agent_config()
        groups = config.get("agent_groups", {})
        return {"groups": groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load groups: {str(e)}")


# Scene Operations Endpoints
@app.post("/api/scene/generate")
async def generate_scene(request: dict):
    """Generate a new scene."""
    try:
        prompt = request.get("prompt")
        model = request.get("model", "claude-sonnet-4.5")
        context = request.get("context")

        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # Get agent bridge
        bridge = get_bridge(project_path)

        # Generate scene
        result = await bridge.generate_scene(
            prompt=prompt,
            model=model,
            context=context,
        )

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scene/enhance")
async def enhance_scene(request: dict):
    """Enhance an existing scene."""
    try:
        scene_text = request.get("scene_text")
        focus = request.get("focus", "overall")
        model = request.get("model", "claude-sonnet-4.5")
        voice_sample = request.get("voice_sample")

        if not scene_text:
            raise HTTPException(status_code=400, detail="Scene text is required")

        # Get agent bridge
        bridge = get_bridge(project_path)

        # Enhance scene
        result = await bridge.enhance_scene(
            scene_text=scene_text,
            focus=focus,
            model=model,
            voice_sample=voice_sample,
        )

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Enhancement failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge Router Endpoints
@app.post("/api/knowledge/query")
async def knowledge_query(request: dict):
    """Ask a question to the knowledge base."""
    try:
        question = request.get("question")
        notebook_id = request.get("notebook_id")
        source = request.get("source")

        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        # Get agent bridge
        bridge = get_bridge(project_path)

        # Query knowledge base
        result = await bridge.query_knowledge(
            question=question,
            notebook_id=notebook_id,
            source=source,
        )

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Query failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Session Management Endpoints
@app.get("/api/session/status")
async def session_status():
    """Get current session status."""
    return {
        "active": True,
        "session_id": "demo-session",
        "total_cost": _session_cost["total"],
        "stage": "creation",
        "last_save": None
    }


@app.get("/api/session/cost")
async def session_cost():
    """Get detailed cost breakdown for current session."""
    return {
        "total_cost": _session_cost["total"],
        "by_model": _session_cost["by_model"],
        "savings": _session_cost["savings"],
        "local_generations": sum(1 for m in _session_cost["by_model"] if m.get("is_local", False)),
        "cloud_generations": sum(1 for m in _session_cost["by_model"] if not m.get("is_local", False))
    }


@app.post("/api/session/save")
async def session_save():
    """Manually save session."""
    return {"success": True}


# Creation Wizard Endpoints
@app.post("/api/wizard/complete")
async def wizard_complete(request: dict):
    """Complete the creation wizard and generate initial manuscript structure.

    Args:
        request: Dictionary containing wizard form data with keys:
            - title, genre, premise, themes (foundation)
            - protagonist, antagonist, supportingCast (characters)
            - setting, worldRules, atmosphere (world)
            - actStructure, targetLength, pacing (structure)

    Returns:
        Success status and project metadata
    """
    try:
        # Extract wizard data
        title = request.get('title', 'Untitled Story')
        genre = request.get('genre', 'fiction')

        # TODO: Generate initial manuscript structure based on wizard inputs
        # For now, return success with project metadata

        return {
            "success": True,
            "project": {
                "title": title,
                "genre": genre,
                "created_at": "2025-11-14",
                "manuscript_id": "demo-manuscript"
            },
            "message": "Project created successfully! Starting manuscript generation..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/manuscript/import")
async def manuscript_import(file: dict):
    """Import an existing manuscript file.

    Args:
        file: File upload data (placeholder for now)

    Returns:
        Success status and imported manuscript metadata
    """
    try:
        # TODO: Implement actual file import logic
        # Parse uploaded file (txt, md, docx)
        # Create manuscript structure
        # Extract scenes and chapters

        return {
            "success": True,
            "manuscript": {
                "title": "Imported Manuscript",
                "scenes_count": 0,
                "word_count": 0
            },
            "message": "Import functionality coming soon!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/example/load")
async def load_example_project():
    """Load the example project (The Explants excerpt)."""
    try:
        import json

        # Load example data
        example_path = Path(__file__).parent / "example_project.json"
        with open(example_path, 'r') as f:
            example_data = json.load(f)

        # Convert to Manuscript object
        manuscript = Manuscript.from_dict(example_data)

        # Save to storage
        manuscript_path = project_path / ".manuscript" / "explants-v1"
        storage = ManuscriptStorage(manuscript_path)
        storage.save(manuscript)

        # Cache as current manuscript
        _manuscript_cache['current'] = manuscript

        return {
            "success": True,
            "message": "Example project loaded successfully",
            "manuscript": {
                "title": manuscript.title,
                "acts": len(manuscript.acts),
                "chapters": sum(len(act.chapters) for act in manuscript.acts),
                "scenes": sum(len(chapter.scenes) for act in manuscript.acts for chapter in act.chapters),
                "word_count": manuscript.total_word_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ollama Management Endpoints
@app.get("/api/ollama/status")
async def ollama_status():
    """Check if Ollama is running and list models."""
    try:
        is_running = OllamaAgent.is_available()

        if not is_running:
            return {
                "available": False,
                "models": [],
                "message": "Ollama not running. Start with: brew services start ollama"
            }

        models = OllamaAgent.list_models()
        return {
            "available": True,
            "models": models,
            "endpoint": "http://localhost:11434"
        }
    except Exception as e:
        return {
            "available": False,
            "models": [],
            "error": str(e)
        }


# Character Analysis Endpoints
@app.get("/api/manuscript/{manuscript_id}/characters")
async def get_characters(manuscript_id: str):
    """Get all characters in manuscript."""
    try:
        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            # Try to load from storage
            manuscript_path = project_path / ".manuscript" / manuscript_id
            if manuscript_path.exists():
                storage = ManuscriptStorage(manuscript_path)
                manuscript = storage.load()
                _manuscript_cache['current'] = manuscript

        if not manuscript or not hasattr(manuscript, 'characters'):
            return {"characters": []}

        # Return character data
        return {
            "characters": [
                {
                    "id": char.id,
                    "name": char.name,
                    "role": char.role,
                    "core_traits": char.core_traits,
                    "observable_traits": char.observable_traits,
                    "values": char.values,
                    "fears": char.fears,
                    "fatal_flaw": char.fatal_flaw,
                    "mistaken_belief": char.mistaken_belief,
                    "reveals_protagonist_dimension": char.reveals_protagonist_dimension,
                    "serves_protagonist_goal": char.serves_protagonist_goal
                }
                for char in manuscript.characters
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/character/{character_id}/analyze")
async def analyze_character(character_id: str):
    """Analyze character for dimensional depth."""
    try:
        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find character
        character = None
        for char in manuscript.characters:
            if char.id == character_id:
                character = char
                break

        if not character:
            raise HTTPException(status_code=404, detail="Character not found")

        # Convert to dict for analyzer
        character_data = {
            "id": character.id,
            "name": character.name,
            "role": character.role,
            "core_traits": character.core_traits,
            "observable_traits": character.observable_traits,
            "values": character.values,
            "fears": character.fears,
            "fatal_flaw": character.fatal_flaw,
            "mistaken_belief": character.mistaken_belief,
            "reveals_protagonist_dimension": character.reveals_protagonist_dimension,
            "serves_protagonist_goal": character.serves_protagonist_goal
        }

        # Run analysis
        results = analyze_character_depth(character_data)

        # If protagonist, also check dimensionality vs supporting cast
        if character.role == "protagonist":
            supporting_cast = [
                {
                    "id": c.id,
                    "name": c.name,
                    "core_traits": c.core_traits,
                    "observable_traits": c.observable_traits,
                    "values": c.values,
                    "fears": c.fears,
                    "fatal_flaw": c.fatal_flaw,
                    "mistaken_belief": c.mistaken_belief,
                    "reveals_protagonist_dimension": c.reveals_protagonist_dimension
                }
                for c in manuscript.characters if c.role == "supporting"
            ]

            if supporting_cast:
                dimensionality_results = analyze_protagonist_dimensionality(
                    character_data,
                    supporting_cast
                )

                # Add protagonist-specific flags
                if not dimensionality_results["is_most_dimensional"]:
                    results["flags"].extend(dimensionality_results["flags"])

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# Sprint 11: Research / NotebookLM Endpoints
# ==============================================================================

@app.post("/api/research/query")
async def query_research(request: dict):
    """Query a NotebookLM notebook (Sprint 11).

    Request:
        {
            "question": str,
            "notebook_id": str (optional - auto-selects if omitted),
            "project_id": str
        }

    Response:
        {
            "success": bool,
            "answer": str,
            "sources": list,
            "notebook_name": str,
            "notebook_id": str,
            "timestamp": str
        }
    """
    try:
        question = request.get("question")
        notebook_id = request.get("notebook_id")
        project_id = request.get("project_id", "explants-v1")

        if not question:
            raise HTTPException(400, "Question required")

        # Load project notebooks
        notebooks = _load_project_notebooks(project_id)

        # Select notebook
        if notebook_id:
            notebook = next((nb for nb in notebooks if nb["id"] == notebook_id), None)
            if not notebook:
                raise HTTPException(404, "Notebook not found")
        else:
            # Auto-select based on tags/relevance
            notebook = _auto_select_notebook(question, notebooks)
            if not notebook:
                raise HTTPException(400, "No notebooks available. Add a notebook first.")

        # Query NotebookLM
        result = await notebooklm_client.query(question, notebook["url"])

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"],
            "notebook_name": result["notebook_name"],
            "notebook_id": notebook["id"],
            "timestamp": result["timestamp"]
        }

    except AuthenticationError:
        raise HTTPException(401, "Not authenticated. Please connect NotebookLM first.")
    except NotebookNotFoundError as e:
        raise HTTPException(404, f"Notebook not accessible: {str(e)}")
    except QueryTimeoutError as e:
        raise HTTPException(408, f"Query timed out: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Query failed: {str(e)}")


@app.get("/api/research/notebooks")
async def list_notebooks(project_id: str = "explants-v1"):
    """List all notebooks for a project (Sprint 11).

    Query params:
        project_id: Project identifier

    Response:
        {
            "notebooks": [
                {
                    "id": str,
                    "name": str,
                    "url": str,
                    "description": str,
                    "tags": list,
                    "created_at": str
                }
            ]
        }
    """
    try:
        notebooks = _load_project_notebooks(project_id)
        return {"notebooks": notebooks}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/api/research/notebooks")
async def add_notebook(request: dict):
    """Add a notebook to a project (Sprint 11).

    Request:
        {
            "project_id": str,
            "name": str,
            "url": str,
            "description": str (optional),
            "tags": list (optional)
        }
    """
    try:
        project_id = request.get("project_id", "explants-v1")
        name = request.get("name")
        url = request.get("url")
        description = request.get("description", "")
        tags = request.get("tags", [])

        if not all([name, url]):
            raise HTTPException(400, "name and url required")

        # Validate URL
        if not url.startswith("https://notebooklm.google.com/notebook/"):
            raise HTTPException(400, "Invalid NotebookLM URL. Must start with https://notebooklm.google.com/notebook/")

        # Load existing notebooks
        notebooks = _load_project_notebooks(project_id)

        # Create new notebook entry
        notebook = {
            "id": str(uuid.uuid4()),
            "name": name,
            "url": url,
            "description": description,
            "tags": tags,
            "created_at": datetime.now().isoformat()
        }

        notebooks.append(notebook)

        # Save
        _save_project_notebooks(project_id, notebooks)

        return {"success": True, "notebook": notebook}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.put("/api/research/notebooks/{notebook_id}")
async def update_notebook(notebook_id: str, request: dict):
    """Update a notebook's metadata (Sprint 11)."""
    try:
        project_id = request.get("project_id", "explants-v1")
        notebooks = _load_project_notebooks(project_id)

        notebook = next((nb for nb in notebooks if nb["id"] == notebook_id), None)
        if not notebook:
            raise HTTPException(404, "Notebook not found")

        # Update fields
        if "name" in request:
            notebook["name"] = request["name"]
        if "description" in request:
            notebook["description"] = request["description"]
        if "tags" in request:
            notebook["tags"] = request["tags"]

        _save_project_notebooks(project_id, notebooks)

        return {"success": True, "notebook": notebook}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/api/research/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str, project_id: str = "explants-v1"):
    """Delete a notebook from a project (Sprint 11)."""
    try:
        notebooks = _load_project_notebooks(project_id)
        notebooks = [nb for nb in notebooks if nb["id"] != notebook_id]
        _save_project_notebooks(project_id, notebooks)

        return {"success": True}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/research/auth/status")
async def get_auth_status():
    """Check if NotebookLM is authenticated (Sprint 11)."""
    try:
        is_authenticated = await notebooklm_client._is_authenticated()
        return {
            "authenticated": is_authenticated,
            "service": "NotebookLM"
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/api/research/auth/login")
async def initiate_auth():
    """Initiate NotebookLM authentication flow (Sprint 11)."""
    try:
        success = await notebooklm_client.authenticate()
        return {
            "success": success,
            "message": "Authentication complete" if success else "Authentication failed"
        }
    except Exception as e:
        raise HTTPException(500, f"Authentication failed: {str(e)}")


# Helper Functions for Research Endpoints

def _load_project_notebooks(project_id: str) -> list:
    """Load notebooks for a project."""
    # Support both old and new path structures
    notebooks_file = project_path / ".manuscript" / project_id / "notebooks.json"

    # Fallback to root project path
    if not notebooks_file.exists():
        notebooks_file = project_path / project_id / "notebooks.json"

    if not notebooks_file.exists():
        return []

    with open(notebooks_file, "r") as f:
        return json.load(f)


def _save_project_notebooks(project_id: str, notebooks: list):
    """Save notebooks for a project."""
    # Use manuscript directory
    project_dir = project_path / ".manuscript" / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    notebooks_file = project_dir / "notebooks.json"

    with open(notebooks_file, "w") as f:
        json.dump(notebooks, f, indent=2)


def _auto_select_notebook(question: str, notebooks: list) -> dict:
    """Auto-select most relevant notebook based on question.

    Simple implementation: return first notebook.
    Advanced: Use embedding similarity or keyword matching.
    """
    if not notebooks:
        return None

    # Simple: return first notebook
    # TODO: Implement smart selection based on tags/keywords
    return notebooks[0]


# ==============================================================================
# Sprint 12: Universal Skill System Endpoints
# ==============================================================================

@app.post("/api/skills/execute")
async def execute_skill(request: dict):
    """Execute any skill via orchestrator (Sprint 12).

    Request:
        {
            "skill_name": str,  # e.g., "scene-analyzer", "scene-enhancer"
            "input_data": dict,  # Skill-specific input
            "context": dict (optional),  # Additional context
            "allow_fallback": bool (default: true),  # Allow fallback providers
            "preferred_provider": str (optional)  # Force specific provider
        }

    Response:
        {
            "status": "success" | "error" | "fallback",
            "data": {...},  # Skill output
            "metadata": {
                "provider": str,
                "skill_name": str,
                "execution_time_ms": int,
                "cost_estimate": float
            },
            "error": {...}  # If status == "error"
        }
    """
    try:
        skill_name = request.get("skill_name")
        input_data = request.get("input_data", {})
        context = request.get("context")
        allow_fallback = request.get("allow_fallback", True)
        preferred_provider = request.get("preferred_provider")

        if not skill_name:
            raise HTTPException(400, "skill_name required")

        # Create skill request
        skill_request = SkillRequest(
            skill_name=skill_name,
            input_data=input_data,
            context=context,
            allow_fallback=allow_fallback,
            preferred_provider=SkillProvider(preferred_provider) if preferred_provider else None
        )

        # Execute via orchestrator
        response = await skill_orchestrator.execute_skill(skill_request)

        # Return response
        return {
            "status": response.status.value,
            "data": response.data,
            "metadata": response.metadata,
            "error": response.error
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Skill execution failed: {str(e)}")


@app.get("/api/skills/list")
async def list_skills():
    """List all available skills for current user (Sprint 12).

    Response:
        {
            "skills": [
                {
                    "name": str,
                    "skill_id": str,
                    "capability": str,
                    "description": str,
                    "available": bool,
                    "providers": [str],
                    "cost_tier": str
                }
            ]
        }
    """
    try:
        # Get all skills from orchestrator
        all_skills = skill_orchestrator.list_available_skills()

        return {"skills": all_skills}

    except Exception as e:
        raise HTTPException(500, f"Failed to list skills: {str(e)}")


@app.get("/api/skills/{skill_name}/info")
async def get_skill_info(skill_name: str):
    """Get detailed information about a specific skill (Sprint 12).

    Response:
        {
            "name": str,
            "skill_id": str,
            "capability": str,
            "description": str,
            "available": bool,
            "providers": [str],
            "cost_tier": str,
            "input_schema": dict,
            "output_schema": dict,
            "examples": [dict]
        }
    """
    try:
        # Get skill info from orchestrator
        skill_info = skill_orchestrator.get_skill_info(skill_name)

        if not skill_info:
            raise HTTPException(404, f"Skill '{skill_name}' not found")

        return skill_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to get skill info: {str(e)}")


@app.get("/api/skills/health")
async def check_skills_health():
    """Check health status of all skill providers (Sprint 12).

    Response:
        {
            "providers": {
                "claude_skill": {"available": bool, "latency_ms": int},
                "native_python": {"available": bool, "latency_ms": int},
                "openai": {"available": bool, "latency_ms": int},
                "local_llm": {"available": bool, "latency_ms": int}
            },
            "overall_status": "healthy" | "degraded" | "unhealthy"
        }
    """
    try:
        # Check provider health
        health_status = await skill_orchestrator.check_provider_health()

        return health_status

    except Exception as e:
        raise HTTPException(500, f"Health check failed: {str(e)}")


# Sprint 10: File Operations Endpoints
@app.get("/api/manuscript/files")
async def list_scene_files():
    """List all scene files in the manuscript (Sprint 10).

    Returns both the manuscript structure and actual .md files on disk.
    """
    try:
        manuscript_path = project_path / ".manuscript" / "explants-v1"

        if not manuscript_path.exists():
            return {"files": [], "scenes_dir": None}

        storage = ManuscriptStorage(manuscript_path)
        manuscript = storage.load()

        if not manuscript:
            return {"files": [], "scenes_dir": None}

        # Scan for .md files
        scenes_dir = manuscript_path / "scenes"
        file_list = []

        if scenes_dir.exists():
            for md_file in scenes_dir.rglob("*.md"):
                rel_path = md_file.relative_to(manuscript_path)
                file_list.append({
                    "path": str(rel_path),
                    "name": md_file.name,
                    "size": md_file.stat().st_size,
                    "modified": md_file.stat().st_mtime
                })

        return {
            "files": file_list,
            "scenes_dir": str(scenes_dir) if scenes_dir.exists() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scene/create")
async def create_scene(request: dict):
    """Create a new scene in the manuscript (Sprint 10).

    Args:
        request: {
            "chapter_id": str,
            "title": str,
            "content": str (optional),
            "position": int (optional)
        }
    """
    try:
        chapter_id = request.get("chapter_id")
        title = request.get("title", "New Scene")
        content = request.get("content", "")
        position = request.get("position")  # None = append to end

        if not chapter_id:
            raise HTTPException(status_code=400, detail="chapter_id required")

        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find the chapter
        target_chapter = None
        for act in manuscript.acts:
            for chapter in act.chapters:
                if chapter.id == chapter_id:
                    target_chapter = chapter
                    break
            if target_chapter:
                break

        if not target_chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        # Create new scene
        from factory.core.manuscript.structure import Scene
        import uuid

        scene_id = f"scene-{uuid.uuid4().hex[:8]}"
        new_scene = Scene(
            id=scene_id,
            title=title,
            content=content
        )

        # Add to chapter
        if position is not None and 0 <= position <= len(target_chapter.scenes):
            target_chapter.scenes.insert(position, new_scene)
        else:
            target_chapter.scenes.append(new_scene)

        # Save manuscript
        manuscript_path = project_path / ".manuscript" / "explants-v1"
        storage = ManuscriptStorage(manuscript_path)
        success = storage.save(manuscript)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save manuscript")

        return {
            "success": True,
            "scene": {
                "id": new_scene.id,
                "title": new_scene.title,
                "file_path": new_scene.file_path
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/scene/{scene_id}/rename")
async def rename_scene(scene_id: str, request: dict):
    """Rename a scene (Sprint 10).

    Updates both the manifest and renames the .md file.
    """
    try:
        new_title = request.get("title")
        if not new_title:
            raise HTTPException(status_code=400, detail="title required")

        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find and update scene
        scene = manuscript.get_scene(scene_id)
        if not scene:
            raise HTTPException(status_code=404, detail="Scene not found")

        scene.title = new_title

        # Save manuscript (will update the .md file)
        manuscript_path = project_path / ".manuscript" / "explants-v1"
        storage = ManuscriptStorage(manuscript_path)
        success = storage.save(manuscript)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save manuscript")

        return {
            "success": True,
            "title": new_title,
            "file_path": scene.file_path
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/scene/{scene_id}")
async def delete_scene(scene_id: str):
    """Delete a scene (Sprint 10).

    Removes from manifest and deletes the .md file.
    """
    try:
        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        if not manuscript:
            raise HTTPException(status_code=404, detail="No manuscript loaded")

        # Find and remove scene
        scene_file_path = None
        scene_found = False

        for act in manuscript.acts:
            for chapter in act.chapters:
                for i, scene in enumerate(chapter.scenes):
                    if scene.id == scene_id:
                        scene_file_path = scene.file_path
                        chapter.scenes.pop(i)
                        scene_found = True
                        break
                if scene_found:
                    break
            if scene_found:
                break

        if not scene_found:
            raise HTTPException(status_code=404, detail="Scene not found")

        # Delete the .md file
        if scene_file_path:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            file_to_delete = manuscript_path / scene_file_path
            if file_to_delete.exists():
                file_to_delete.unlink()

        # Save updated manuscript
        storage = ManuscriptStorage(manuscript_path)
        success = storage.save(manuscript)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save manuscript")

        return {"success": True, "deleted": scene_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("🚀 Starting Writers Factory Web Server (Phase 3 - Real AI)")
    print("=" * 70)
    print()
    print("Backend API:  http://127.0.0.1:8000")
    print("Health check: http://127.0.0.1:8000/api/health")
    print()
    print("Connected to real AI agents:")
    print("  - Model comparison with real LLM outputs")
    print("  - Scene generation with selected models")
    print("  - Scene enhancement workflows")
    print("  - Knowledge base queries")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Health Check Endpoint (for launcher script)
@app.get("/health")
async def health_check():
    """Health check endpoint for startup verification."""
    return {
        "status": "healthy",
        "service": "Writers Factory Backend",
        "version": "2.0.0"
    }
