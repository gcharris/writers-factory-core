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
    """Update scene content (for autosave)."""
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

        # Find and update scene
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    if scene.id == scene_id:
                        scene.update_content(content)

                        # Save manuscript
                        manuscript_path = project_path / ".manuscript" / "explants-v1"
                        storage = ManuscriptStorage(manuscript_path)
                        success = storage.save(manuscript)

                        if success:
                            return {
                                "success": True,
                                "word_count": scene.word_count,
                                "saved_at": "now"
                            }
                        else:
                            raise HTTPException(status_code=500, detail="Failed to save")

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
