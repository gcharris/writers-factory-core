"""
Wizard Routes - WebSocket endpoints for AI Wizard conversation

Handles real-time bi-directional communication between frontend and
SetupWizardAgent for intelligent project setup.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse

from factory.ai.setup_wizard_agent import SetupWizardAgent
from factory.ai.model_router import ModelRouter
from factory.templates.category_templates import get_all_categories


router = APIRouter()


class WizardSession:
    """
    Manage an active wizard session via WebSocket.
    """

    def __init__(
        self,
        websocket: WebSocket,
        project_id: str,
        notebook_url: str,
        model: str = "llama3.3"
    ):
        self.websocket = websocket
        self.project_id = project_id
        self.notebook_url = notebook_url
        self.model = model

        # User response queue
        self.user_response_queue: asyncio.Queue = asyncio.Queue()

        # Create wizard agent
        self.agent = SetupWizardAgent(
            project_id=project_id,
            notebook_url=notebook_url,
            model=model,
            user_response_callback=self._get_user_response
        )

    async def send_message(
        self,
        message_type: str,
        content: Any,
        requires_input: bool = False,
        input_type: str = "text",
        options: Optional[list] = None
    ):
        """Send message to frontend."""
        await self.websocket.send_json({
            "type": message_type,
            "content": content,
            "requires_input": requires_input,
            "input_type": input_type,
            "options": options
        })

    async def _get_user_response(self, prompt_data: Dict[str, Any]) -> str:
        """
        Request input from user and wait for response.

        This is called by the wizard agent when it needs user input.
        """
        # Send prompt to frontend
        await self.send_message(
            message_type="ai_message",
            content=prompt_data.get("message", ""),
            requires_input=True,
            input_type=prompt_data.get("input_type", "text"),
            options=prompt_data.get("options")
        )

        # Wait for user response
        response = await self.user_response_queue.get()
        return response

    async def handle_user_message(self, message: Dict[str, Any]):
        """Handle incoming message from user."""
        if message.get("type") == "user_response":
            # Put response in queue for wizard agent
            await self.user_response_queue.put(message.get("content", ""))

    async def run_wizard(self):
        """Run the complete wizard process."""
        try:
            # Welcome message
            await self.send_message(
                message_type="ai_message",
                content=f"""Welcome to the AI Wizard! 🧙‍♂️

I'll help you organize your story knowledge from NotebookLM into 8 structured categories:

1. Characters
2. Story Structure
3. World Building
4. Themes & Philosophy
5. Voice & Craft
6. Antagonism & Conflict
7. Key Beats & Pacing
8. Research & Setting Specifics

Let's begin by extracting information from your NotebookLM notebook.
""",
                requires_input=False
            )

            # Process all categories
            results = await self.agent.run_full_wizard()

            # Completion message
            await self.send_message(
                message_type="complete",
                content={
                    "message": "Setup complete! Initializing knowledge graph...",
                    "results": results
                }
            )

            # TODO: Initialize knowledge graph from created category files
            # await initialize_knowledge_graph(self.project_id)

            # Redirect to editor
            await self.send_message(
                message_type="redirect",
                content="/editor"
            )

        except Exception as e:
            await self.send_message(
                message_type="error",
                content=f"An error occurred: {str(e)}"
            )


@router.websocket("/ws/wizard/{project_id}")
async def wizard_websocket(websocket: WebSocket, project_id: str):
    """
    WebSocket endpoint for AI wizard conversation.

    Args:
        websocket: WebSocket connection
        project_id: Project identifier
    """
    await websocket.accept()

    try:
        # Get initial configuration from client
        init_message = await websocket.receive_json()

        if init_message.get("type") != "init":
            await websocket.send_json({
                "type": "error",
                "content": "Expected 'init' message"
            })
            await websocket.close()
            return

        notebook_url = init_message.get("notebook_url")
        if not notebook_url:
            await websocket.send_json({
                "type": "error",
                "content": "notebook_url is required"
            })
            await websocket.close()
            return

        # Get model preference
        router_inst = ModelRouter(project_id)
        model = router_inst.get_model_for_task("setup_wizard")

        # Create session
        session = WizardSession(
            websocket=websocket,
            project_id=project_id,
            notebook_url=notebook_url,
            model=model
        )

        # Run wizard in background task
        wizard_task = asyncio.create_task(session.run_wizard())

        # Handle incoming messages
        while True:
            try:
                message = await websocket.receive_json()
                await session.handle_user_message(message)

                # Check if wizard is done
                if wizard_task.done():
                    break

            except WebSocketDisconnect:
                print(f"Client disconnected from wizard session: {project_id}")
                wizard_task.cancel()
                break

        # Wait for wizard to complete
        if not wizard_task.done():
            await wizard_task

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {project_id}")
    except Exception as e:
        print(f"Error in wizard WebSocket: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass


@router.get("/api/wizard/status/{project_id}")
async def get_wizard_status(project_id: str):
    """
    Get status of wizard for a project.

    Args:
        project_id: Project identifier

    Returns:
        Wizard status
    """
    # Check if project has completed wizard setup
    # by checking for reference folder structure

    from pathlib import Path

    project_path = Path(f"projects/{project_id}")
    reference_path = project_path / "reference"

    if not reference_path.exists():
        return JSONResponse({
            "status": "not_started",
            "message": "Wizard has not been run for this project"
        })

    # Check which categories exist
    categories = get_all_categories()
    completed_categories = []

    for category in categories:
        category_path = reference_path / category
        if category_path.exists() and list(category_path.glob("*.md")):
            completed_categories.append(category)

    if len(completed_categories) == len(categories):
        return JSONResponse({
            "status": "completed",
            "completed_categories": completed_categories,
            "total_categories": len(categories)
        })
    elif len(completed_categories) > 0:
        return JSONResponse({
            "status": "in_progress",
            "completed_categories": completed_categories,
            "remaining_categories": [c for c in categories if c not in completed_categories],
            "progress_percent": int((len(completed_categories) / len(categories)) * 100)
        })
    else:
        return JSONResponse({
            "status": "not_started",
            "message": "No categories have been processed yet"
        })


@router.post("/api/wizard/reset/{project_id}")
async def reset_wizard(project_id: str):
    """
    Reset wizard progress for a project.

    Args:
        project_id: Project identifier

    Returns:
        Reset confirmation
    """
    from pathlib import Path
    import shutil

    project_path = Path(f"projects/{project_id}")
    reference_path = project_path / "reference"

    if reference_path.exists():
        # Backup before deleting
        backup_path = project_path / f"reference_backup_{int(asyncio.get_event_loop().time())}"
        shutil.move(str(reference_path), str(backup_path))

        return JSONResponse({
            "success": True,
            "message": "Wizard progress reset",
            "backup_location": str(backup_path)
        })

    return JSONResponse({
        "success": True,
        "message": "No wizard progress to reset"
    })
