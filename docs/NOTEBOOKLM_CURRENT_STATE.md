# NotebookLM Integration - Current State & Capabilities

**Date:** November 15, 2025
**Status:** ALREADY IMPLEMENTED (Sprint 11)
**Clarification:** We DO have NotebookLM MCP integration!

---

## You Were Correct!

We already built NotebookLM integration in **Sprint 11**. I apologize for the confusion - I was comparing to an external project when we already have our own implementation.

---

## What We Currently Have (Sprint 11)

### 1. NotebookLM Client (`factory/research/notebooklm_client.py`)

**Capabilities:**
- ✅ Browser automation via Playwright
- ✅ Google authentication (one-time setup)
- ✅ Query notebooks with questions
- ✅ Extract citations from responses
- ✅ Session management

**Methods:**
```python
class NotebookLMClient:
    async def authenticate() -> bool
    async def query(question: str, notebook_url: str, timeout: int = 30) -> Dict
    async def test_connection() -> bool
```

---

### 2. NotebookLM Setup Integration (`factory/integrations/notebooklm_setup.py`)

**Capabilities:**
- ✅ Extract project knowledge during setup
- ✅ Extract voice context
- ✅ Extract character context
- ✅ Extract world context

**Methods:**
```python
class NotebookLMSetupIntegration:
    async def extract_project_knowledge(notebooklm_urls: List[str]) -> str
    async def extract_voice_context(notebooklm_urls: List[str]) -> str
    async def extract_character_context(notebooklm_urls: List[str]) -> str
    async def extract_world_context(notebooklm_urls: List[str]) -> str
```

**Predefined Queries:**
- Character summaries, traits, relationships, arcs
- Story world, settings, locations
- Plot threads and themes
- Voice and writing style
- Metaphors, symbols, motifs

---

### 3. MCP Server Tools (`factory/mcp/server.py`)

**Already Implemented (Sprint 11):**

#### `query_notebooklm`
```python
@server.tool()
async def query_notebooklm(question: str, notebook_name: str = None) -> dict:
    """
    Query NotebookLM for research answers with citations.

    Args:
        question: The question to ask
        notebook_name: Optional notebook name (auto-selects if omitted)

    Returns:
        {
            "success": bool,
            "answer": str,
            "sources": list,
            "notebook_name": str
        }
    """
```

#### `list_research_notebooks`
```python
@server.tool()
async def list_research_notebooks(project_id: str = "explants-v1") -> dict:
    """
    List available NotebookLM notebooks for research.

    Returns:
        {
            "notebooks": [
                {
                    "id": str,
                    "name": str,
                    "url": str,
                    "description": str,
                    "tags": list
                }
            ]
        }
    """
```

---

### 4. Backend API Endpoints (`webapp/backend/simple_app.py`)

**Already Implemented (Sprint 11):**

#### `POST /api/research/query`
```python
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
```

#### `GET /api/research/notebooks`
```python
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
```

---

### 5. Project Notebook Storage

**Storage Location:**
```
/path/to/.manuscript/{project_id}/notebooks.json
```

**Format:**
```json
[
    {
        "id": "notebook-1",
        "name": "Character Profiles",
        "url": "https://notebooklm.google.com/notebook/abc123",
        "description": "Character backstories and development",
        "tags": ["characters", "backstories"],
        "created_at": "2025-11-15T10:00:00Z"
    },
    {
        "id": "notebook-2",
        "name": "World Building",
        "url": "https://notebooklm.google.com/notebook/def456",
        "description": "Story world and settings",
        "tags": ["world", "settings"],
        "created_at": "2025-11-15T10:05:00Z"
    }
]
```

---

### 6. Auto-Selection Logic

**Helper Function:**
```python
def _auto_select_notebook(question: str, notebooks: list) -> dict:
    """
    Auto-select notebook based on question and tags.

    Logic:
    - Checks tags in question keywords
    - Returns most relevant notebook
    - Falls back to first notebook if no match
    """
```

---

## What We Can Already Do

### ✅ Multi-Notebook Support (ALREADY EXISTS!)

**Storage structure already supports multiple notebooks:**

```python
# notebooks.json can contain multiple notebooks
notebooks = [
    {"id": "nb-1", "name": "Ideas", "url": "...", "tags": ["ideas", "plot"]},
    {"id": "nb-2", "name": "Characters", "url": "...", "tags": ["characters"]},
    {"id": "nb-3", "name": "Structure", "url": "...", "tags": ["structure"]}
]
```

### ✅ Tag-Based Organization (ALREADY EXISTS!)

```python
# Each notebook has tags
{
    "id": "notebook-1",
    "name": "Character Profiles",
    "tags": ["characters", "backstories", "relationships"]
}
```

### ✅ Auto-Selection (ALREADY EXISTS!)

```python
# Query without specifying notebook - auto-selects
POST /api/research/query
{
    "question": "What is Mickey's character arc?",
    "project_id": "explants-v1"
    // No notebook_id - system auto-selects based on tags/content
}
```

### ✅ Manual Selection (ALREADY EXISTS!)

```python
# Query specific notebook
POST /api/research/query
{
    "question": "What is Mickey's character arc?",
    "notebook_id": "notebook-1",  # Explicitly select Character notebook
    "project_id": "explants-v1"
}
```

---

## What's Missing (Gaps for Your Multi-Notebook Architecture)

### ❌ API Endpoints to Add/Update/Remove Notebooks

**Current:** Notebooks managed manually in `notebooks.json`

**Needed:**
```python
POST /api/research/notebooks/add
{
    "project_id": str,
    "url": str,
    "name": str,
    "description": str,
    "tags": list
}

PUT /api/research/notebooks/{notebook_id}
{
    "name": str,
    "description": str,
    "tags": list
}

DELETE /api/research/notebooks/{notebook_id}
```

### ❌ Usage Statistics Tracking

**Current:** No tracking of query frequency per notebook

**Needed:**
```python
{
    "id": "notebook-1",
    "use_count": 47,
    "last_used": "2025-11-15T14:30:00Z"
}
```

### ❌ Session-Based Context Preservation

**Current:** Each query is independent

**Needed:** Multi-turn conversations
```python
# First query
POST /api/research/query
{
    "question": "Tell me about Mickey",
    "session_id": "session-123"
}

# Follow-up (maintains context)
POST /api/research/query
{
    "question": "What's his relationship with The Chronicler?",
    "session_id": "session-123"  # Same session
}
```

---

## Answering Your Original Questions (Revisited)

### 1. "Are we assuming one NotebookLM or multiple?"

**Answer:** We ALREADY support multiple notebooks!

**Current Implementation:**
- `notebooks.json` stores array of notebooks
- Each has id, name, URL, tags
- Auto-selection based on tags
- Manual selection by notebook_id

**What you described (multiple specialized notebooks) is ALREADY SUPPORTED:**
```json
[
    {"name": "Ideas & World-Building", "tags": ["ideas", "creative"]},
    {"name": "Character Profiles", "tags": ["characters"]},
    {"name": "Story Structure", "tags": ["structure", "planning"]}
]
```

### 2. "Can we push to NotebookLM or create notebooks?"

**Answer:** No (same limitation as external project)

**Our Implementation:**
- User manually creates notebooks in NotebookLM
- User provides URLs to Writers Factory
- System stores URLs in `notebooks.json`
- Queries via browser automation

**We CANNOT:**
- Create notebooks programmatically
- Add sources to notebooks
- Write content to notebooks

**We CAN:**
- Register multiple notebook URLs
- Tag and describe notebooks
- Query notebooks
- Auto-select relevant notebook

### 3. "What about ongoing knowledge graph?"

**Answer:** Knowledge graph is separate system (Sprint 13)

**Two Knowledge Systems:**

| NotebookLM (Sprint 11) | Knowledge Graph (Sprint 13) |
|------------------------|------------------------------|
| External user-curated knowledge | Internal AI-extracted entities |
| Queries via browser automation | Queries via graph traversal |
| Storage: Google's NotebookLM | Storage: Local JSON/graph DB |
| Updated: Manually by user | Updated: Auto from manuscript |

**They coexist but serve different purposes.**

---

## What You Can Do RIGHT NOW

### 1. Create Multiple Notebooks in NotebookLM

Manually create your specialized notebooks:
- Ideas & World-Building notebook
- Character Profiles notebook
- Story Structure notebook

### 2. Register Them in Writers Factory

Edit `.manuscript/explants-v1/notebooks.json`:
```json
[
    {
        "id": "ideas-nb",
        "name": "Ideas & World-Building",
        "url": "https://notebooklm.google.com/notebook/YOUR_IDEAS_URL",
        "description": "Creative flashes, plot development, world-building notes",
        "tags": ["ideas", "creative", "plot", "world-building"],
        "created_at": "2025-11-15T00:00:00Z"
    },
    {
        "id": "characters-nb",
        "name": "Character Profiles",
        "url": "https://notebooklm.google.com/notebook/YOUR_CHARACTERS_URL",
        "description": "Character backstories, relationships, development arcs",
        "tags": ["characters", "backstories", "relationships"],
        "created_at": "2025-11-15T00:00:00Z"
    },
    {
        "id": "structure-nb",
        "name": "Story Structure",
        "url": "https://notebooklm.google.com/notebook/YOUR_STRUCTURE_URL",
        "description": "Chapter outlines, acts, structure notes",
        "tags": ["structure", "planning", "chapters", "acts"],
        "created_at": "2025-11-15T00:00:00Z"
    }
]
```

### 3. Query via MCP Server

**In Claude Code:**
```
User: "Query NotebookLM: What is Mickey's character arc?"

Claude Code: *calls query_notebooklm tool*
- Auto-selects Character Profiles notebook (based on "character" tag)
- Returns answer with citations
```

### 4. Query via API

**Direct API call:**
```bash
# Auto-select (system picks best notebook)
curl -X POST http://localhost:8000/api/research/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Mickey character arc?",
    "project_id": "explants-v1"
  }'

# Manual select (pick specific notebook)
curl -X POST http://localhost:8000/api/research/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Mickey character arc?",
    "notebook_id": "characters-nb",
    "project_id": "explants-v1"
  }'
```

---

## What We Should Add (Sprint 16 Enhancements)

### 1. Notebook Management API

**Add CRUD endpoints:**
```python
# factory/mcp/server.py additions

@server.tool()
async def add_notebook(
    project_id: str,
    url: str,
    name: str,
    description: str = None,
    tags: List[str] = None
) -> dict:
    """Add notebook to project library."""
    # POST to /api/research/notebooks/add

@server.tool()
async def update_notebook(
    project_id: str,
    notebook_id: str,
    name: str = None,
    description: str = None,
    tags: List[str] = None
) -> dict:
    """Update notebook metadata."""
    # PUT to /api/research/notebooks/{id}

@server.tool()
async def remove_notebook(
    project_id: str,
    notebook_id: str
) -> dict:
    """Remove notebook from library."""
    # DELETE to /api/research/notebooks/{id}
```

### 2. Usage Statistics

**Track query frequency:**
```python
{
    "id": "characters-nb",
    "name": "Character Profiles",
    "use_count": 47,
    "last_used": "2025-11-15T14:30:00Z"
}
```

### 3. Session Management

**Multi-turn conversations:**
```python
@server.tool()
async def start_research_session(project_id: str, notebook_id: str = None) -> dict:
    """Start new research session with context preservation."""

@server.tool()
async def continue_research_session(session_id: str, question: str) -> dict:
    """Continue research session (maintains context)."""
```

### 4. Smart Notebook Selection UI

**Add to frontend:**
- "Select Research Notebook" dropdown
- Tag-based filtering
- Usage statistics display
- Quick-switch between notebooks

---

## Summary

### What We Have ✅
- Multi-notebook storage (`notebooks.json`)
- Tag-based organization
- Auto-selection logic
- MCP tools (`query_notebooklm`, `list_research_notebooks`)
- Backend API endpoints (`/api/research/*`)
- Multiple notebook URLs per project

### What's Missing ❌
- CRUD API for notebook management
- Usage statistics tracking
- Session-based context
- UI for notebook management

### What You Can Do NOW ✅
1. Create specialized notebooks in NotebookLM
2. Edit `notebooks.json` to register them
3. Query via MCP tools (auto-selection works!)
4. Query via API (manual selection works!)

### What Needs Building (Sprint 16) 🔨
1. Notebook management API endpoints
2. Usage statistics
3. Session management
4. UI enhancements

---

**Your multi-notebook architecture is ALREADY supported in the backend!**

The missing piece is just a UI to manage notebooks instead of editing JSON manually.
