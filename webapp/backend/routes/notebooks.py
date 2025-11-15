"""
Notebook Management API Routes - Sprint 16

CRUD endpoints for managing NotebookLM notebooks:
- POST   /api/research/notebooks/add       - Add notebook to project
- PUT    /api/research/notebooks/{id}      - Update notebook metadata
- DELETE /api/research/notebooks/{id}      - Remove notebook
- POST   /api/research/notebooks/test      - Test URL connectivity
- GET    /api/research/notebooks/{id}/stats - Get usage statistics

Integrates with Sprint 11 (NotebookLM backend) and Sprint 15 (Beginner mode).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
import logging
import json
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add factory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from factory.research.notebooklm_client import NotebookLMClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/research/notebooks", tags=["notebooks"])


# Request/Response Models

class AddNotebookRequest(BaseModel):
    """Request model for adding a notebook."""
    projectId: str
    name: str
    url: str
    description: str = ""
    tags: List[str] = []
    category: Optional[str] = None  # "ideas", "characters", "structure", "research", "custom"


class UpdateNotebookRequest(BaseModel):
    """Request model for updating a notebook."""
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class TestNotebookRequest(BaseModel):
    """Request model for testing notebook connectivity."""
    url: str


class NotebookResponse(BaseModel):
    """Response model for a notebook."""
    id: str
    name: str
    url: str
    description: str
    tags: List[str]
    category: Optional[str]
    createdAt: str
    updatedAt: str


class NotebookStatsResponse(BaseModel):
    """Response model for notebook statistics."""
    id: str
    name: str
    queryCount: int
    lastQueried: Optional[str]
    totalWords: Optional[int]
    averageResponseTime: Optional[float]


class TestNotebookResponse(BaseModel):
    """Response model for notebook connectivity test."""
    success: bool
    accessible: bool
    message: str
    notebookName: Optional[str] = None


# Helper Functions

def get_notebooks_file_path(project_id: str) -> Path:
    """Get path to notebooks.json for a project.

    Args:
        project_id: Project identifier

    Returns:
        Path to notebooks.json
    """
    # Assuming projects are stored in projects/[project-id]/notebooks.json
    return Path(f"./projects/{project_id}/notebooks.json")


def load_notebooks(project_id: str) -> Dict[str, Any]:
    """Load notebooks.json for a project.

    Args:
        project_id: Project identifier

    Returns:
        Dict with notebooks data
    """
    notebooks_file = get_notebooks_file_path(project_id)

    if not notebooks_file.exists():
        # Create empty notebooks file
        notebooks_file.parent.mkdir(parents=True, exist_ok=True)
        default_data = {"notebooks": []}
        notebooks_file.write_text(json.dumps(default_data, indent=2))
        return default_data

    try:
        with open(notebooks_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {notebooks_file}")
        return {"notebooks": []}


def save_notebooks(project_id: str, data: Dict[str, Any]):
    """Save notebooks.json for a project.

    Args:
        project_id: Project identifier
        data: Notebooks data to save
    """
    notebooks_file = get_notebooks_file_path(project_id)
    notebooks_file.parent.mkdir(parents=True, exist_ok=True)

    with open(notebooks_file, 'w') as f:
        json.dump(data, f, indent=2)


def generate_notebook_id() -> str:
    """Generate unique notebook ID.

    Returns:
        Unique ID string
    """
    return str(uuid.uuid4())[:8]


# API Endpoints

@router.post("/add", response_model=NotebookResponse)
async def add_notebook(request: AddNotebookRequest):
    """Add a new notebook to the project.

    Creates a new notebook entry in notebooks.json with metadata,
    tags, and timestamps.

    Args:
        request: Notebook details (name, URL, description, tags, category)

    Returns:
        Created notebook with generated ID
    """
    try:
        logger.info(f"Adding notebook '{request.name}' to project {request.projectId}")

        # Load existing notebooks
        notebooks_data = load_notebooks(request.projectId)

        # Check for duplicate URL
        for notebook in notebooks_data["notebooks"]:
            if notebook["url"] == request.url:
                raise HTTPException(
                    status_code=400,
                    detail=f"Notebook with URL {request.url} already exists"
                )

        # Generate notebook ID
        notebook_id = generate_notebook_id()

        # Create notebook entry
        now = datetime.now().isoformat()
        new_notebook = {
            "id": notebook_id,
            "name": request.name,
            "url": request.url,
            "description": request.description,
            "tags": request.tags,
            "category": request.category,
            "createdAt": now,
            "updatedAt": now,
            "queryCount": 0,
            "lastQueried": None
        }

        # Add to notebooks list
        notebooks_data["notebooks"].append(new_notebook)

        # Save updated notebooks
        save_notebooks(request.projectId, notebooks_data)

        logger.info(f"Notebook '{request.name}' added with ID: {notebook_id}")

        return NotebookResponse(
            id=new_notebook["id"],
            name=new_notebook["name"],
            url=new_notebook["url"],
            description=new_notebook["description"],
            tags=new_notebook["tags"],
            category=new_notebook.get("category"),
            createdAt=new_notebook["createdAt"],
            updatedAt=new_notebook["updatedAt"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add notebook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add notebook: {str(e)}"
        )


@router.put("/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(notebook_id: str, request: UpdateNotebookRequest, project_id: str):
    """Update an existing notebook's metadata.

    Args:
        notebook_id: ID of notebook to update
        request: Updated fields (name, description, tags, category)
        project_id: Project identifier (query parameter)

    Returns:
        Updated notebook
    """
    try:
        logger.info(f"Updating notebook {notebook_id} in project {project_id}")

        # Load notebooks
        notebooks_data = load_notebooks(project_id)

        # Find notebook
        notebook = None
        for nb in notebooks_data["notebooks"]:
            if nb["id"] == notebook_id:
                notebook = nb
                break

        if not notebook:
            raise HTTPException(
                status_code=404,
                detail=f"Notebook {notebook_id} not found"
            )

        # Update fields
        if request.name is not None:
            notebook["name"] = request.name
        if request.description is not None:
            notebook["description"] = request.description
        if request.tags is not None:
            notebook["tags"] = request.tags
        if request.category is not None:
            notebook["category"] = request.category

        # Update timestamp
        notebook["updatedAt"] = datetime.now().isoformat()

        # Save updated notebooks
        save_notebooks(project_id, notebooks_data)

        logger.info(f"Notebook {notebook_id} updated successfully")

        return NotebookResponse(
            id=notebook["id"],
            name=notebook["name"],
            url=notebook["url"],
            description=notebook["description"],
            tags=notebook["tags"],
            category=notebook.get("category"),
            createdAt=notebook["createdAt"],
            updatedAt=notebook["updatedAt"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update notebook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update notebook: {str(e)}"
        )


@router.delete("/{notebook_id}")
async def delete_notebook(notebook_id: str, project_id: str):
    """Remove a notebook from the project.

    Args:
        notebook_id: ID of notebook to remove
        project_id: Project identifier (query parameter)

    Returns:
        Success message
    """
    try:
        logger.info(f"Deleting notebook {notebook_id} from project {project_id}")

        # Load notebooks
        notebooks_data = load_notebooks(project_id)

        # Find and remove notebook
        original_count = len(notebooks_data["notebooks"])
        notebooks_data["notebooks"] = [
            nb for nb in notebooks_data["notebooks"]
            if nb["id"] != notebook_id
        ]

        if len(notebooks_data["notebooks"]) == original_count:
            raise HTTPException(
                status_code=404,
                detail=f"Notebook {notebook_id} not found"
            )

        # Save updated notebooks
        save_notebooks(project_id, notebooks_data)

        logger.info(f"Notebook {notebook_id} deleted successfully")

        return {"success": True, "message": f"Notebook {notebook_id} removed"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete notebook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete notebook: {str(e)}"
        )


@router.post("/test", response_model=TestNotebookResponse)
async def test_notebook(request: TestNotebookRequest):
    """Test connectivity to a NotebookLM URL.

    Attempts to connect to the notebook and retrieve its name.
    Does not save any data.

    Args:
        request: Notebook URL to test

    Returns:
        Test result with success status and notebook name
    """
    try:
        logger.info(f"Testing notebook connectivity: {request.url}")

        # Initialize NotebookLM client
        client = NotebookLMClient()

        # Test query (simple question to verify connectivity)
        test_question = "What is this notebook about? Provide a brief summary."

        try:
            result = await client.query(
                question=test_question,
                notebook_url=request.url,
                timeout=30
            )

            notebook_name = result.get("notebook_name", "Unknown Notebook")

            logger.info(f"Notebook accessible: {notebook_name}")

            return TestNotebookResponse(
                success=True,
                accessible=True,
                message=f"Successfully connected to notebook: {notebook_name}",
                notebookName=notebook_name
            )

        except Exception as query_error:
            logger.warning(f"Notebook query failed: {str(query_error)}")
            return TestNotebookResponse(
                success=False,
                accessible=False,
                message=f"Could not access notebook: {str(query_error)}"
            )

    except Exception as e:
        logger.error(f"Notebook test failed: {str(e)}", exc_info=True)
        return TestNotebookResponse(
            success=False,
            accessible=False,
            message=f"Test failed: {str(e)}"
        )


@router.get("/{notebook_id}/stats", response_model=NotebookStatsResponse)
async def get_notebook_stats(notebook_id: str, project_id: str):
    """Get usage statistics for a notebook.

    Args:
        notebook_id: ID of notebook
        project_id: Project identifier (query parameter)

    Returns:
        Usage statistics (query count, last queried, etc.)
    """
    try:
        logger.info(f"Getting stats for notebook {notebook_id} in project {project_id}")

        # Load notebooks
        notebooks_data = load_notebooks(project_id)

        # Find notebook
        notebook = None
        for nb in notebooks_data["notebooks"]:
            if nb["id"] == notebook_id:
                notebook = nb
                break

        if not notebook:
            raise HTTPException(
                status_code=404,
                detail=f"Notebook {notebook_id} not found"
            )

        return NotebookStatsResponse(
            id=notebook["id"],
            name=notebook["name"],
            queryCount=notebook.get("queryCount", 0),
            lastQueried=notebook.get("lastQueried"),
            totalWords=notebook.get("totalWords"),
            averageResponseTime=notebook.get("averageResponseTime")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notebook stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}"
        )


# Helper endpoint to increment query count (called by query endpoint)
@router.post("/{notebook_id}/track-query")
async def track_query(notebook_id: str, project_id: str):
    """Track that a query was made to this notebook.

    Internal endpoint called by the query endpoint to update stats.

    Args:
        notebook_id: ID of notebook
        project_id: Project identifier (query parameter)

    Returns:
        Success message
    """
    try:
        # Load notebooks
        notebooks_data = load_notebooks(project_id)

        # Find notebook
        for notebook in notebooks_data["notebooks"]:
            if notebook["id"] == notebook_id:
                notebook["queryCount"] = notebook.get("queryCount", 0) + 1
                notebook["lastQueried"] = datetime.now().isoformat()
                save_notebooks(project_id, notebooks_data)
                return {"success": True}

        return {"success": False, "message": "Notebook not found"}

    except Exception as e:
        logger.error(f"Failed to track query: {str(e)}")
        return {"success": False, "message": str(e)}
