"""Simplified FastAPI backend for Writers Factory web interface.

Minimal working version with essential endpoints.
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

# Initialize FastAPI app
app = FastAPI(
    title="Writers Factory",
    description="Multi-model AI novel writing system",
    version="0.2.0"
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
        "version": "0.2.0",
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


# Model Comparison Endpoints
@app.post("/api/compare")
async def compare_models(request: ModelComparisonRequest):
    """Compare multiple models on the same prompt."""
    try:
        # Simplified - returns mock results
        results = {}
        for model in request.models:
            results[model] = f"[{model} output would appear here]\n\n{request.prompt}"

        return {
            "success": True,
            "results": results,
            "costs": {},
            "metadata": {}
        }
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
                "strengths": agent_config.get("strengths", [])
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


# Scene Operations Endpoints (Simplified)
@app.post("/api/scene/generate")
async def generate_scene(request: dict):
    """Generate a new scene."""
    return {
        "success": True,
        "scene": f"[Generated scene would appear here]\n\nPrompt: {request.get('prompt')}",
        "metadata": {}
    }


@app.post("/api/scene/enhance")
async def enhance_scene(request: dict):
    """Enhance an existing scene."""
    return {
        "success": True,
        "enhanced_scene": f"[Enhanced scene would appear here]\n\nOriginal: {request.get('scene_text')[:100]}...",
        "changes": [],
        "metadata": {}
    }


# Knowledge Router Endpoints (Simplified)
@app.post("/api/knowledge/query")
async def knowledge_query(request: dict):
    """Ask a question to the knowledge base."""
    return {
        "success": True,
        "answer": f"[Knowledge base answer would appear here]\n\nQuestion: {request.get('question')}",
        "source": "cognee",
        "confidence": 0.85,
        "references": []
    }


# Session Management Endpoints
@app.get("/api/session/status")
async def session_status():
    """Get current session status."""
    return {
        "active": True,
        "session_id": "demo-session",
        "total_cost": 0.0,
        "stage": "creation",
        "last_save": None
    }


@app.post("/api/session/save")
async def session_save():
    """Manually save session."""
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("🚀 Starting Writers Factory Web Server (Simplified)")
    print("=" * 70)
    print()
    print("Backend API:  http://127.0.0.1:8000")
    print("Health check: http://127.0.0.1:8000/api/health")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    uvicorn.run(app, host="127.0.0.1", port=8000)
