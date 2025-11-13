"""FastAPI backend for Writers Factory web interface.

Provides REST API and WebSocket endpoints for browser-based access to:
- Creation Wizard (5-phase story bible generator)
- Model Comparison (tournament system)
- Scene Workflows (generation, enhancement, voice testing)
- Knowledge Router (ask questions)
"""

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import asyncio
import json
from typing import Optional, List, Dict
from pydantic import BaseModel
import sys

# Add factory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from factory.wizard.wizard import CreationWizard, WizardPhase
from factory.tools.model_comparison import ModelComparisonTool
from factory.core.storage import Session, PreferencesManager, CostTracker
from factory.knowledge.router import KnowledgeRouter, KnowledgeSource
from factory.workflows.scene_operations import (
    SceneGenerationWorkflow,
    SceneEnhancementWorkflow,
    VoiceTestingWorkflow
)

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
session: Optional[Session] = None
wizard: Optional[CreationWizard] = None
model_comparison: Optional[ModelComparisonTool] = None
knowledge_router: Optional[KnowledgeRouter] = None


# Request/Response Models
class WizardStartRequest(BaseModel):
    project_name: str


class WizardAnswerRequest(BaseModel):
    answer: str


class ModelComparisonRequest(BaseModel):
    prompt: str
    models: List[str]


class KnowledgeQueryRequest(BaseModel):
    question: str
    source: Optional[str] = "cognee"


class SceneGenerationRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    model: str = "claude-sonnet-4.5"


class SceneEnhancementRequest(BaseModel):
    scene_text: str
    focus: str = "voice"
    model: str = "claude-sonnet-4.5"


# Startup/Shutdown
@app.on_event("startup")
async def startup_event():
    """Initialize Writers Factory components."""
    global session, wizard, model_comparison, knowledge_router

    # Create project directory if it doesn't exist
    project_path.mkdir(parents=True, exist_ok=True)

    # Initialize preferences manager (lightweight, doesn't need Session)
    preferences = PreferencesManager(project_path / ".session")

    # Initialize model comparison tool
    model_comparison = ModelComparisonTool(
        preferences_manager=preferences,
        console=None  # Web interface doesn't need Rich console
    )

    # Note: Session, wizard, and knowledge_router are initialized on-demand
    # when endpoints are called, to avoid startup errors

    print("✅ Writers Factory web server started")
    print(f"📁 Project path: {project_path}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown."""
    global session
    if session:
        await session.save()
    print("👋 Writers Factory web server stopped")


# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "project_path": str(project_path)
    }


# Wizard Endpoints
@app.post("/api/wizard/start")
async def wizard_start(request: WizardStartRequest):
    """Start a new creation wizard session."""
    global wizard

    wizard_project_path = project_path / request.project_name
    wizard_project_path.mkdir(parents=True, exist_ok=True)

    wizard = CreationWizard(wizard_project_path)
    current_phase = wizard.get_current_phase()
    question = wizard.get_next_question()

    return {
        "success": True,
        "project_name": request.project_name,
        "current_phase": current_phase.value,
        "question": question,
        "progress": wizard.get_progress()
    }


@app.post("/api/wizard/answer")
async def wizard_answer(request: WizardAnswerRequest):
    """Submit an answer to the wizard."""
    global wizard

    if not wizard:
        raise HTTPException(status_code=400, detail="No wizard session active")

    # Process answer
    wizard.process_answer(request.answer)

    # Get next question or finish
    if wizard.is_complete():
        story_bible = await wizard.generate_story_bible()
        return {
            "success": True,
            "complete": True,
            "story_bible": story_bible
        }
    else:
        next_question = wizard.get_next_question()
        return {
            "success": True,
            "complete": False,
            "question": next_question,
            "current_phase": wizard.get_current_phase().value,
            "progress": wizard.get_progress()
        }


@app.get("/api/wizard/progress")
async def wizard_progress():
    """Get current wizard progress."""
    global wizard

    if not wizard:
        return {"active": False}

    return {
        "active": True,
        "current_phase": wizard.get_current_phase().value,
        "progress": wizard.get_progress(),
        "complete": wizard.is_complete()
    }


# Model Comparison Endpoints
@app.post("/api/compare")
async def compare_models(request: ModelComparisonRequest):
    """Compare multiple models on the same prompt."""
    global model_comparison

    if not model_comparison:
        raise HTTPException(status_code=500, detail="Model comparison not initialized")

    try:
        result = await model_comparison.compare_models(
            prompt=request.prompt,
            models=request.models
        )
        return {
            "success": True,
            "results": result["results"],
            "costs": result.get("costs", {}),
            "metadata": result.get("metadata", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/available")
async def get_available_models():
    """Get list of all available models."""
    from factory.core.config.loader import load_agent_config

    config = load_agent_config()
    models = []

    for agent_name, agent_config in config.get("agents", {}).items():
        if agent_config.get("enabled", True):
            models.append({
                "id": agent_name,
                "provider": agent_config.get("provider"),
                "description": agent_config.get("description"),
                "cost_input": agent_config.get("cost_per_1k_input"),
                "cost_output": agent_config.get("cost_per_1k_output"),
                "strengths": agent_config.get("strengths", [])
            })

    return {"models": models}


@app.get("/api/models/groups")
async def get_model_groups():
    """Get predefined model groups."""
    from factory.core.config.loader import load_agent_config

    config = load_agent_config()
    groups = config.get("agent_groups", {})

    return {"groups": groups}


# Knowledge Router Endpoints
@app.post("/api/knowledge/query")
async def knowledge_query(request: KnowledgeQueryRequest):
    """Ask a question to the knowledge base."""
    global knowledge_router

    if not knowledge_router:
        raise HTTPException(status_code=500, detail="Knowledge router not initialized")

    try:
        source = KnowledgeSource.COGNEE if request.source == "cognee" else KnowledgeSource.NOTEBOOKLM
        result = await knowledge_router.query(request.question, source=source)

        return {
            "success": True,
            "answer": result.get("answer"),
            "source": result.get("source"),
            "confidence": result.get("confidence"),
            "references": result.get("references", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Scene Operations Endpoints
@app.post("/api/scene/generate")
async def generate_scene(request: SceneGenerationRequest):
    """Generate a new scene."""
    try:
        workflow = SceneGenerationWorkflow(
            project_path=project_path,
            preferences=PreferencesManager(project_path / ".session")
        )

        result = await workflow.run(
            prompt=request.prompt,
            context=request.context,
            model=request.model
        )

        return {
            "success": True,
            "scene": result.get("scene"),
            "metadata": result.get("metadata", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scene/enhance")
async def enhance_scene(request: SceneEnhancementRequest):
    """Enhance an existing scene."""
    try:
        workflow = SceneEnhancementWorkflow(
            project_path=project_path,
            preferences=PreferencesManager(project_path / ".session")
        )

        result = await workflow.run(
            scene_text=request.scene_text,
            focus=request.focus,
            model=request.model
        )

        return {
            "success": True,
            "enhanced_scene": result.get("enhanced_scene"),
            "changes": result.get("changes", []),
            "metadata": result.get("metadata", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Session Management Endpoints
@app.get("/api/session/status")
async def session_status():
    """Get current session status."""
    global session

    if not session:
        return {"active": False}

    return {
        "active": True,
        "session_id": str(session.session_id),
        "total_cost": session.get_total_cost(),
        "stage": session.get_current_stage(),
        "last_save": session.last_save_time
    }


@app.post("/api/session/save")
async def session_save():
    """Manually save session."""
    global session

    if not session:
        raise HTTPException(status_code=400, detail="No active session")

    success = await session.save()
    return {"success": success}


# WebSocket for real-time streaming
@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming model responses."""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)

            if request_data.get("type") == "generate":
                # Stream generation results
                prompt = request_data.get("prompt")
                model = request_data.get("model", "claude-sonnet-4.5")

                # TODO: Implement streaming generation
                await websocket.send_json({
                    "type": "chunk",
                    "content": "Streaming not yet implemented"
                })

                await websocket.send_json({
                    "type": "complete"
                })

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
