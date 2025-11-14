# Sprint 11: NotebookLM Integration (Production Implementation)

**Priority**: HIGH
**Type**: Core Feature
**Estimated Effort**: 8-12 hours
**Dependencies**: Sprint 9 (File-based storage), Sprint 10 (Three-panel layout)

---

## 🎯 Goal

**Integrate NotebookLM into Writers Factory as a first-class research tool**, not a bolt-on MCP server.

**Why**:
- Research is core to long-form creative writing
- NotebookLM provides source-grounded answers (zero hallucinations)
- Students need research tools built-in, not external dependencies
- Should be as integrated as the TipTap editor or file tree

**Result**: Users can query their research notebooks directly from Writers Factory UI, with answers appearing in a dedicated Research Panel.

---

## 📋 Requirements

### Functional Requirements

**FR-01**: User can add NotebookLM notebooks to their project
- Store notebook URL, name, description, tags
- Multiple notebooks per project
- Persistent storage (in project manifest or separate config)

**FR-02**: User can query notebooks from UI
- Ask natural language questions
- Select specific notebook or auto-select based on tags
- View answers with source citations
- History of recent queries

**FR-03**: AI agents can query notebooks
- Via backend API endpoints
- Via MCP server tools
- Automatic notebook selection based on query context

**FR-04**: Authentication handled transparently
- One-time Google OAuth login
- Credentials stored securely
- Re-authentication flow if expired

**FR-05**: Works offline gracefully
- Clear error messages if NotebookLM unavailable
- Cached responses (optional)
- Doesn't break other features

### Non-Functional Requirements

**NFR-01**: Performance
- Queries return within 10 seconds (NotebookLM dependent)
- UI remains responsive during queries
- Progress indicator for long queries

**NFR-02**: Reliability
- Handles NotebookLM API changes gracefully
- Proper error handling (network, auth, rate limits)
- Logs errors for debugging

**NFR-03**: Security
- OAuth credentials stored securely (not in git)
- No exposure of Google credentials
- Notebook URLs validated before use

**NFR-04**: Maintainability
- Clean separation: backend API ↔ browser automation ↔ NotebookLM
- Well-documented code
- Easy to update if NotebookLM changes

---

## 🏗️ Architecture

### System Architecture

```
┌──────────────────────────────────────────────────────────┐
│ Frontend (React)                                          │
│                                                           │
│  ┌────────────────┐  ┌──────────────────────────────┐   │
│  │ File Tree      │  │ Research Panel (NEW)         │   │
│  │ (Left)         │  │ - Notebook library           │   │
│  │                │  │ - Query input                │   │
│  │                │  │ - Answer display             │   │
│  │                │  │ - Citation list              │   │
│  └────────────────┘  └──────────────────────────────┘   │
│                                                           │
│  ┌────────────────┐  ┌──────────────────────────────┐   │
│  │ Scene Editor   │  │ AI Tools Panel               │   │
│  │ (Center)       │  │ - Can insert research        │   │
│  └────────────────┘  └──────────────────────────────┘   │
└────────────────┬──────────────────────────────────────────┘
                 │ HTTP API
┌────────────────▼──────────────────────────────────────────┐
│ Backend (FastAPI)                                          │
│                                                            │
│  New Endpoints:                                            │
│  - POST /api/research/query                                │
│  - GET  /api/research/notebooks                            │
│  - POST /api/research/notebooks                            │
│  - PUT  /api/research/notebooks/{id}                       │
│  - DELETE /api/research/notebooks/{id}                     │
│  - GET  /api/research/auth/status                          │
│  - POST /api/research/auth/login                           │
└────────────────┬──────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────┐
│ NotebookLM Client (Python)                                 │
│                                                            │
│  factory/research/notebooklm_client.py                     │
│  - Browser automation (Playwright)                         │
│  - Query execution                                         │
│  - Citation extraction                                     │
│  - Authentication management                               │
└────────────────┬──────────────────────────────────────────┘
                 │ Browser automation
┌────────────────▼──────────────────────────────────────────┐
│ NotebookLM (Google)                                        │
│  - Gemini 2.5 processes documents                          │
│  - Returns grounded answers                                │
│  - Provides source citations                               │
└───────────────────────────────────────────────────────────┘
```

### Data Flow

**Query Flow**:
1. User types question in Research Panel
2. Frontend sends `POST /api/research/query` with `{question, notebook_id}`
3. Backend calls `NotebookLMClient.query(question, notebook_url)`
4. Client uses Playwright to automate browser:
   - Opens NotebookLM notebook
   - Types question in chat interface
   - Waits for Gemini response
   - Extracts answer + citations
5. Backend returns `{answer, sources, notebook_name}`
6. Frontend displays answer with citation links

**Authentication Flow**:
1. User clicks "Connect NotebookLM"
2. Backend initiates OAuth flow
3. Browser opens Google login
4. User authorizes Writers Factory
5. Backend saves OAuth tokens securely
6. Future queries use saved tokens

---

## 📦 Implementation Tasks

### Task 11-01: NotebookLM Python Client

**Create**: `factory/research/notebooklm_client.py`

**Responsibilities**:
- Browser automation via Playwright
- Query execution
- Citation extraction
- Error handling

**Key Methods**:

```python
class NotebookLMClient:
    """Client for querying Google NotebookLM."""

    def __init__(self, auth_tokens_path: Path = None):
        """Initialize with optional stored auth tokens."""
        self.auth_tokens_path = auth_tokens_path or Path.home() / ".writers-factory" / "notebooklm_auth.json"
        self.browser = None
        self.context = None
        self.page = None

    async def authenticate(self) -> bool:
        """Authenticate with Google (one-time setup).

        Returns:
            True if authentication successful
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # User needs to see login
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to NotebookLM
            await page.goto("https://notebooklm.google.com")

            # Wait for user to complete Google login
            # Save auth cookies/tokens

            await browser.close()
            return True

    async def query(self, question: str, notebook_url: str, timeout: int = 30) -> dict:
        """Query a NotebookLM notebook.

        Args:
            question: Question to ask
            notebook_url: URL of notebook to query
            timeout: Maximum wait time in seconds

        Returns:
            {
                "answer": str,
                "sources": [{"title": str, "excerpt": str, "page": int}],
                "notebook_name": str,
                "timestamp": str
            }

        Raises:
            AuthenticationError: If not authenticated
            NotebookNotFoundError: If notebook doesn't exist
            QueryTimeoutError: If query takes too long
        """
        if not await self._is_authenticated():
            raise AuthenticationError("Not authenticated with Google")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await self._create_authenticated_context(browser)
            page = await context.new_page()

            try:
                # Navigate to notebook
                await page.goto(notebook_url, wait_until="networkidle")

                # Find chat input
                chat_input = await page.wait_for_selector('textarea[placeholder*="Ask"]', timeout=5000)

                # Type question
                await chat_input.fill(question)
                await chat_input.press("Enter")

                # Wait for response
                response_selector = ".response-container"  # Adjust based on actual HTML
                await page.wait_for_selector(response_selector, timeout=timeout * 1000)

                # Extract answer
                answer_element = await page.query_selector(response_selector)
                answer = await answer_element.inner_text()

                # Extract citations
                sources = await self._extract_citations(page)

                # Extract notebook name
                notebook_name = await self._get_notebook_name(page)

                return {
                    "answer": answer,
                    "sources": sources,
                    "notebook_name": notebook_name,
                    "timestamp": datetime.now().isoformat()
                }

            finally:
                await browser.close()

    async def _extract_citations(self, page) -> list:
        """Extract source citations from response."""
        citations = []
        citation_elements = await page.query_selector_all(".citation")  # Adjust selector

        for elem in citation_elements:
            citation = {
                "title": await elem.get_attribute("data-title"),
                "excerpt": await elem.inner_text(),
                "page": await elem.get_attribute("data-page")
            }
            citations.append(citation)

        return citations

    async def _is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.auth_tokens_path.exists()

    async def _create_authenticated_context(self, browser):
        """Create browser context with saved auth."""
        # Load saved cookies/tokens
        # Create context with authentication
        pass

    async def test_connection(self) -> bool:
        """Test if NotebookLM is accessible."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto("https://notebooklm.google.com", timeout=10000)
                await browser.close()
                return True
        except Exception:
            return False
```

**Dependencies**:
```python
# requirements.txt additions
playwright>=1.40.0
```

**Installation**:
```bash
pip install playwright
playwright install chromium  # Install Chromium browser
```

---

### Task 11-02: Backend API Endpoints

**File**: `webapp/backend/simple_app.py`

**New imports**:
```python
from factory.research.notebooklm_client import NotebookLMClient, AuthenticationError, NotebookNotFoundError
from pathlib import Path
import json
```

**Initialize client**:
```python
# Global NotebookLM client
notebooklm_client = NotebookLMClient()
```

**Endpoints**:

```python
# ============================================================================
# Research / NotebookLM Endpoints
# ============================================================================

@app.post("/api/research/query")
async def query_research(request: dict):
    """Query a NotebookLM notebook.

    Request:
        {
            "question": str,
            "notebook_id": str (optional - auto-selects if omitted),
            "project_id": str
        }

    Response:
        {
            "answer": str,
            "sources": list,
            "notebook_name": str,
            "timestamp": str
        }
    """
    try:
        question = request.get("question")
        notebook_id = request.get("notebook_id")
        project_id = request.get("project_id")

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
    except NotebookNotFoundError:
        raise HTTPException(404, "Notebook not accessible. Check URL and permissions.")
    except Exception as e:
        raise HTTPException(500, f"Query failed: {str(e)}")


@app.get("/api/research/notebooks")
async def list_notebooks(project_id: str):
    """List all notebooks for a project.

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
    """Add a notebook to a project.

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
        project_id = request.get("project_id")
        name = request.get("name")
        url = request.get("url")
        description = request.get("description", "")
        tags = request.get("tags", [])

        if not all([project_id, name, url]):
            raise HTTPException(400, "project_id, name, and url required")

        # Validate URL
        if not url.startswith("https://notebooklm.google.com/notebook/"):
            raise HTTPException(400, "Invalid NotebookLM URL")

        # Load existing notebooks
        notebooks = _load_project_notebooks(project_id)

        # Create new notebook entry
        import uuid
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

    except Exception as e:
        raise HTTPException(500, str(e))


@app.put("/api/research/notebooks/{notebook_id}")
async def update_notebook(notebook_id: str, request: dict):
    """Update a notebook's metadata."""
    try:
        project_id = request.get("project_id")
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

    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/api/research/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str, project_id: str):
    """Delete a notebook from a project."""
    try:
        notebooks = _load_project_notebooks(project_id)
        notebooks = [nb for nb in notebooks if nb["id"] != notebook_id]
        _save_project_notebooks(project_id, notebooks)

        return {"success": True}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/research/auth/status")
async def get_auth_status():
    """Check if NotebookLM is authenticated."""
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
    """Initiate NotebookLM authentication flow."""
    try:
        success = await notebooklm_client.authenticate()
        return {
            "success": success,
            "message": "Authentication complete" if success else "Authentication failed"
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ============================================================================
# Helper Functions
# ============================================================================

def _load_project_notebooks(project_id: str) -> list:
    """Load notebooks for a project."""
    notebooks_file = project_path / project_id / "notebooks.json"

    if not notebooks_file.exists():
        return []

    with open(notebooks_file, "r") as f:
        return json.load(f)


def _save_project_notebooks(project_id: str, notebooks: list):
    """Save notebooks for a project."""
    project_dir = project_path / project_id
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
```

---

### Task 11-03: Frontend Research Panel

**Create**: `webapp/frontend-v2/src/features/research/ResearchPanel.jsx`

```jsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Book, Plus, Send, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export function ResearchPanel({ projectId }) {
  const [question, setQuestion] = useState('');
  const [selectedNotebook, setSelectedNotebook] = useState(null);
  const [showAddNotebook, setShowAddNotebook] = useState(false);
  const queryClient = useQueryClient();

  // Fetch notebooks
  const { data: notebooksData, isLoading: loadingNotebooks } = useQuery({
    queryKey: ['notebooks', projectId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/research/notebooks?project_id=${projectId}`);
      return res.json();
    }
  });

  // Query mutation
  const queryMutation = useMutation({
    mutationFn: async ({ question, notebookId }) => {
      const res = await fetch('http://localhost:8000/api/research/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          notebook_id: notebookId,
          project_id: projectId
        })
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail);
      }
      return res.json();
    },
    onSuccess: (data) => {
      toast.success('Answer received');
    },
    onError: (error) => {
      toast.error(`Query failed: ${error.message}`);
    }
  });

  const handleQuery = () => {
    if (!question.trim()) return;

    queryMutation.mutate({
      question: question.trim(),
      notebookId: selectedNotebook
    });
  };

  const notebooks = notebooksData?.notebooks || [];

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold text-gray-900 flex items-center">
            <Book size={18} className="mr-2" />
            Research
          </h2>
          <button
            onClick={() => setShowAddNotebook(true)}
            className="text-sm px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            <Plus size={14} className="inline mr-1" />
            Add Notebook
          </button>
        </div>

        {/* Notebook selector */}
        <select
          value={selectedNotebook || ''}
          onChange={(e) => setSelectedNotebook(e.target.value || null)}
          className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
        >
          <option value="">Auto-select notebook</option>
          {notebooks.map(nb => (
            <option key={nb.id} value={nb.id}>
              {nb.name}
            </option>
          ))}
        </select>
      </div>

      {/* Query input */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex gap-2">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your research..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded resize-none"
            rows={3}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.metaKey) {
                handleQuery();
              }
            }}
          />
          <button
            onClick={handleQuery}
            disabled={queryMutation.isPending || !question.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {queryMutation.isPending ? (
              <Loader2 size={18} className="animate-spin" />
            ) : (
              <Send size={18} />
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-1">Cmd+Enter to send</p>
      </div>

      {/* Answer display */}
      <div className="flex-1 overflow-y-auto p-4">
        {queryMutation.data && (
          <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            <div className="text-sm text-gray-600 mb-2">
              From: <span className="font-medium">{queryMutation.data.notebook_name}</span>
            </div>

            <div className="prose prose-sm max-w-none mb-4">
              {queryMutation.data.answer}
            </div>

            {queryMutation.data.sources && queryMutation.data.sources.length > 0 && (
              <div className="border-t pt-3">
                <div className="text-xs font-semibold text-gray-700 mb-2">Sources:</div>
                {queryMutation.data.sources.map((source, idx) => (
                  <div key={idx} className="text-xs text-gray-600 mb-1">
                    {idx + 1}. {source.title} {source.page && `(p. ${source.page})`}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {queryMutation.isPending && (
          <div className="text-center text-gray-500 py-8">
            <Loader2 size={24} className="animate-spin mx-auto mb-2" />
            Querying NotebookLM...
          </div>
        )}

        {!queryMutation.data && !queryMutation.isPending && (
          <div className="text-center text-gray-400 py-8">
            Ask a question about your research
          </div>
        )}
      </div>

      {/* Add notebook modal */}
      {showAddNotebook && (
        <AddNotebookModal
          projectId={projectId}
          onClose={() => setShowAddNotebook(false)}
          onSuccess={() => {
            queryClient.invalidateQueries(['notebooks', projectId]);
            setShowAddNotebook(false);
          }}
        />
      )}
    </div>
  );
}

// Add Notebook Modal component
function AddNotebookModal({ projectId, onClose, onSuccess }) {
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState('');

  const addMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/research/notebooks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Failed to add notebook');
      return res.json();
    },
    onSuccess: () => {
      toast.success('Notebook added');
      onSuccess();
    },
    onError: () => {
      toast.error('Failed to add notebook');
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    addMutation.mutate({
      project_id: projectId,
      name,
      url,
      description,
      tags: tags.split(',').map(t => t.trim()).filter(Boolean)
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 className="text-lg font-semibold mb-4">Add NotebookLM Notebook</h3>

        <form onSubmit={handleSubmit}>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 border rounded"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">NotebookLM URL</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://notebooklm.google.com/notebook/..."
                className="w-full px-3 py-2 border rounded"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Description (optional)</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 border rounded"
                rows={2}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Tags (comma-separated)</label>
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="characters, worldbuilding, research"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>

          <div className="flex gap-2 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border rounded hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={addMutation.isPending}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {addMutation.isPending ? 'Adding...' : 'Add Notebook'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

---

### Task 11-04: Integrate Research Panel into App

**File**: `webapp/frontend-v2/src/App.jsx`

**Add Research Panel** as a fourth panel (optional) or replace AI Tools panel with tabs:

**Option A: Four-panel layout** (File Tree | Editor | AI Tools | Research)

**Option B: Tabbed right panel** (AI Tools tab | Research tab)

**Recommended**: **Option B** (tabbed right panel)

```jsx
// In App.jsx
import { ResearchPanel } from './features/research/ResearchPanel';
import { useState } from 'react';

function App() {
  const [rightPanelTab, setRightPanelTab] = useState('ai-tools'); // 'ai-tools' or 'research'

  return (
    <PanelLayout
      left={<FileTree ... />}
      center={<SceneEditor ... />}
      right={
        <div className="h-full flex flex-col">
          {/* Tabs */}
          <div className="flex border-b border-gray-300">
            <button
              onClick={() => setRightPanelTab('ai-tools')}
              className={`flex-1 px-4 py-2 ${
                rightPanelTab === 'ai-tools' ? 'bg-white border-b-2 border-blue-600' : 'bg-gray-100'
              }`}
            >
              AI Tools
            </button>
            <button
              onClick={() => setRightPanelTab('research')}
              className={`flex-1 px-4 py-2 ${
                rightPanelTab === 'research' ? 'bg-white border-b-2 border-blue-600' : 'bg-gray-100'
              }`}
            >
              Research
            </button>
          </div>

          {/* Panel content */}
          <div className="flex-1">
            {rightPanelTab === 'ai-tools' && <AIToolsPanel ... />}
            {rightPanelTab === 'research' && <ResearchPanel projectId={currentProjectId} />}
          </div>
        </div>
      }
    />
  );
}
```

---

### Task 11-05: Update MCP Server

**File**: `factory/mcp/server.py`

**Add NotebookLM tools**:

```python
@self.server.tool()
async def query_notebooklm(question: str, notebook_name: str = None) -> dict:
    """Query NotebookLM for research answers with citations.

    Args:
        question: The question to ask
        notebook_name: Optional notebook name (auto-selects if omitted)

    Returns:
        {
            "answer": str,
            "sources": list,
            "notebook_name": str
        }
    """
    try:
        # Get current project ID (from context or default)
        project_id = "explants-v2"  # TODO: Get from context

        response = await self.client.post(
            f"{self.backend_url}/api/research/query",
            json={
                "question": question,
                "notebook_id": None,  # Auto-select
                "project_id": project_id
            }
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"[MCP] Error querying NotebookLM: {e}", file=sys.stderr)
        return {"error": str(e)}


@self.server.tool()
async def list_research_notebooks(project_id: str = "explants-v2") -> dict:
    """List available NotebookLM notebooks."""
    try:
        response = await self.client.get(
            f"{self.backend_url}/api/research/notebooks",
            params={"project_id": project_id}
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"[MCP] Error listing notebooks: {e}", file=sys.stderr)
        return {"error": str(e)}
```

---

### Task 11-06: Testing

**Create**: `tests/test_notebooklm_integration.py`

```python
import pytest
from factory.research.notebooklm_client import NotebookLMClient

@pytest.mark.asyncio
async def test_authentication():
    """Test NotebookLM authentication flow."""
    client = NotebookLMClient()
    # Manual test: requires user interaction
    # assert await client.authenticate()

@pytest.mark.asyncio
async def test_query():
    """Test querying a notebook."""
    client = NotebookLMClient()

    # Requires authenticated client
    if not await client._is_authenticated():
        pytest.skip("Not authenticated")

    result = await client.query(
        question="What are the main themes?",
        notebook_url="https://notebooklm.google.com/notebook/test-id"
    )

    assert "answer" in result
    assert "sources" in result
    assert isinstance(result["sources"], list)

@pytest.mark.asyncio
async def test_connection():
    """Test NotebookLM connection."""
    client = NotebookLMClient()
    is_reachable = await client.test_connection()
    assert isinstance(is_reachable, bool)
```

**Manual testing checklist**:
- [ ] Add notebook via UI
- [ ] Query notebook via UI
- [ ] View answer with citations
- [ ] Query via MCP server (Claude Code)
- [ ] Auto-select notebook based on question
- [ ] Handle authentication errors gracefully
- [ ] Handle network errors gracefully

---

## 📁 File Structure

```
writers-factory-core/
├── factory/
│   ├── research/                      # NEW
│   │   ├── __init__.py
│   │   └── notebooklm_client.py      # Browser automation client
│   └── mcp/
│       └── server.py                  # Updated with NotebookLM tools
│
├── webapp/
│   ├── backend/
│   │   └── simple_app.py              # Updated with research endpoints
│   └── frontend-v2/
│       └── src/
│           └── features/
│               └── research/          # NEW
│                   ├── ResearchPanel.jsx
│                   └── AddNotebookModal.jsx
│
├── project/
│   └── .manuscript/
│       └── [project-name]/
│           ├── manifest.json
│           ├── scenes/
│           └── notebooks.json         # NEW - Notebook library
│
└── tests/
    └── test_notebooklm_integration.py # NEW
```

---

## 🎓 For Students (Course Setup)

**In QUICK_START.md**, add:

### NotebookLM Research (Optional but Recommended)

**What it is**: Query your research notebooks directly from Writers Factory

**Setup** (5 minutes):

1. **Create notebook** on https://notebooklm.google.com
2. **Upload research** (character profiles, worldbuilding, outlines, etc.)
3. **In Writers Factory**:
   - Open Research panel (right side, "Research" tab)
   - Click "Add Notebook"
   - Paste NotebookLM URL
   - Add name and tags
4. **First-time auth**:
   - Click "Connect NotebookLM"
   - Complete Google login
   - One-time setup

**Usage**:
- Ask questions: "What are my protagonist's motivations?"
- Get grounded answers from your documents
- See source citations
- AI tools can also query your research

---

## ✅ Definition of Done

### Backend
- [ ] `NotebookLMClient` implemented with Playwright
- [ ] Authentication flow working (Google OAuth)
- [ ] Query execution returning answers + citations
- [ ] All 7 API endpoints implemented
- [ ] Notebook storage (notebooks.json) working
- [ ] Error handling for auth, network, timeout

### Frontend
- [ ] ResearchPanel component created
- [ ] Add notebook UI working
- [ ] Query UI working
- [ ] Answer display with citations
- [ ] Integrated into App.jsx (tabbed right panel)
- [ ] Toast notifications for all operations

### MCP Server
- [ ] `query_notebooklm` tool added
- [ ] `list_research_notebooks` tool added
- [ ] Claude Code can query via MCP

### Testing
- [ ] Manual test: Add notebook
- [ ] Manual test: Query notebook
- [ ] Manual test: View citations
- [ ] Manual test: MCP tools work
- [ ] Unit tests for NotebookLMClient
- [ ] Error scenarios tested

### Documentation
- [ ] QUICK_START.md updated with setup
- [ ] Research panel documented
- [ ] Troubleshooting guide for auth issues

---

## 🚀 Estimated Timeline

- **Task 11-01** (NotebookLM Client): 4-5 hours
- **Task 11-02** (Backend API): 2-3 hours
- **Task 11-03** (Frontend Panel): 2-3 hours
- **Task 11-04** (Integration): 1 hour
- **Task 11-05** (MCP Server): 1 hour
- **Task 11-06** (Testing): 1-2 hours

**Total**: 11-15 hours (spread over 2-3 days)

---

## 💡 Future Enhancements

**Phase 2** (After Sprint 11):
- [ ] Query history (save past queries)
- [ ] Smart notebook selection (embedding similarity)
- [ ] Multi-notebook queries (ask multiple notebooks)
- [ ] Insert answer into scene (from research → editor)
- [ ] Cached responses (offline mode)
- [ ] Export citations (for bibliography)

---

## 📋 Hand to New Claude Code Agent

**Message**:
```
I need you to implement Sprint 11: NotebookLM Integration.

This is a PRODUCTION implementation - not a quick hack. NotebookLM is critical for research workflow in long-form creative writing.

Read the complete specification:
/Users/gch2024/writers-factory-core/SPRINT_11_NOTEBOOKLM_INTEGRATION.md

Key requirements:
- Integrate NotebookLM as first-class feature (not bolt-on)
- Users can add notebooks to projects
- Query notebooks from UI with citations
- AI tools can query research
- Works for all users (not just Claude Code users)

Start with Task 11-01 (NotebookLM Client) and work through systematically.

This is the right way to build it - robust, maintainable, integrated.
```

---

**This is the production-quality integration you need.** 🎯

No temporary solutions, no retrofitting - built properly from the start.