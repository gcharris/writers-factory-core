# NotebookLM MCP Server Comparison & Integration Strategy

**Date:** November 15, 2025
**Reference:** https://github.com/PleasePrompto/notebooklm-mcp
**Status:** Analysis for Writers Factory Integration

---

## Executive Summary

The PleasePrompto NotebookLM MCP server provides **significantly more capabilities** than our current implementation, including:

✅ **Multi-notebook library management**
✅ **Notebook switching** (select active notebook)
✅ **Add/update/remove notebooks** programmatically
✅ **Session management** (concurrent sessions, auto-recovery)
✅ **Tag-based organization**
✅ **Usage statistics tracking**

**Key Insight:** They DO have "write" capabilities - but it's **metadata management** (add notebook to library, update tags/descriptions), NOT content creation in NotebookLM itself.

**Recommendation:** Integrate their MCP server OR adopt their architecture patterns for Writers Factory.

---

## Detailed Capability Comparison

### Our Current Implementation (`factory/research/notebooklm_client.py`)

**Capabilities:**
- ✅ Authenticate with Google (one-time browser login)
- ✅ Query single notebook with question
- ✅ Extract citations from responses
- ❌ No multi-notebook management
- ❌ No notebook library system
- ❌ No session management
- ❌ No metadata/tagging
- ❌ No notebook switching

**Architecture:**
- Playwright browser automation
- Headless Chrome
- One-off queries (no session persistence)
- Direct URL access per query

**Limitations:**
- Must provide notebook URL every query
- No way to organize/categorize notebooks
- No usage tracking
- No concurrent sessions

---

### PleasePrompto NotebookLM MCP Server

**Full Tool List (15 tools):**

#### 1. Query & Interaction Tools

**`ask_question`**
```typescript
{
  url?: string,           // Optional if notebook already selected
  question: string,
  sessionId?: string,     // For multi-turn conversations
  showBrowser?: boolean   // Debug mode
}
```

**`search_notebooks`**
```typescript
{
  query: string  // Search by name, description, tags
}
```

#### 2. Library Management Tools

**`add_notebook`** ⭐ NEW CAPABILITY
```typescript
{
  url: string,               // NotebookLM URL
  name: string,              // Human-readable name
  description?: string,      // What's in this notebook
  topics?: string[],         // ["world-building", "characters"]
  content_types?: string[],  // ["research", "notes", "examples"]
  use_cases?: string[],      // ["scene-generation", "continuity"]
  tags?: string[]            // Flexible categorization
}
```

**`list_notebooks`** ⭐ NEW CAPABILITY
```typescript
// Returns array of all registered notebooks with metadata
```

**`get_notebook`** ⭐ NEW CAPABILITY
```typescript
{
  id: string  // Get specific notebook details
}
```

**`select_notebook`** ⭐ NEW CAPABILITY
```typescript
{
  id: string  // Set as active notebook
}
// Future queries use this notebook by default!
```

**`update_notebook`** ⭐ NEW CAPABILITY
```typescript
{
  id: string,
  name?: string,
  description?: string,
  topics?: string[],
  // ... update any metadata
}
```

**`remove_notebook`** ⭐ NEW CAPABILITY
```typescript
{
  id: string  // Remove from library
}
```

#### 3. Session Management Tools

**`list_sessions`**
```typescript
// View all active browser sessions
```

**`close_session`**
```typescript
{
  sessionId: string
}
```

**`reset_session`**
```typescript
{
  sessionId: string  // Clear session state
}
```

#### 4. System Tools

**`get_health`**
```typescript
// Check authentication status, browser health
```

**`setup_auth`**
```typescript
// Initialize Google authentication
```

**`re_auth`**
```typescript
// Refresh authentication
```

**`cleanup_data`**
```typescript
// Remove all stored data
```

**`get_library_stats`**
```typescript
// Aggregate statistics about notebook usage
```

---

## Key Architectural Differences

### 1. Library System

**Our Implementation:**
```python
# Must provide URL every time
await client.query(
    question="What are the characters?",
    notebook_url="https://notebooklm.google.com/notebook/abc123"
)
```

**Their Implementation:**
```typescript
// One-time registration
add_notebook({
    url: "https://notebooklm.google.com/notebook/abc123",
    name: "Character Profiles",
    topics: ["characters", "backstories"],
    tags: ["mickey-bardot", "the-chronicler"]
})

// Later: Query without URL
select_notebook({ id: "notebook-1" })
ask_question({ question: "What are Mickey's traits?" })
// Automatically uses selected notebook!
```

**Benefit:** No URL repetition, cleaner API, context preservation.

---

### 2. Multi-Notebook Workflow

**Your Desired Workflow (from earlier conversation):**
> "One notebook keeps those ideas for creative flashes, and world building and plot development, but there are other notebooks which save documents on specific things like characters or previous and future chapters acts structure, etc."

**How PleasePrompto Enables This:**

```typescript
// Setup phase (one-time)
add_notebook({
    url: "https://notebooklm.google.com/.../ideas",
    name: "Ideas & World-Building",
    topics: ["creative-flashes", "plot-development"],
    use_cases: ["brainstorming", "world-building"],
    tags: ["ideas", "creative"]
})

add_notebook({
    url: "https://notebooklm.google.com/.../characters",
    name: "Character Profiles",
    topics: ["characters", "backstories", "relationships"],
    use_cases: ["character-validation", "continuity"],
    tags: ["characters"]
})

add_notebook({
    url: "https://notebooklm.google.com/.../structure",
    name: "Story Structure",
    topics: ["chapters", "acts", "outlines"],
    use_cases: ["planning", "structure"],
    tags: ["structure", "planning"]
})

// Usage: Switch between notebooks contextually
select_notebook({ name: "Character Profiles" })
ask_question({ question: "What is Mickey's arc?" })

select_notebook({ name: "Story Structure" })
ask_question({ question: "What chapters are planned?" })

select_notebook({ name: "Ideas & World-Building" })
ask_question({ question: "Any new plot twists added recently?" })
```

**This is EXACTLY your multi-notebook architecture!**

---

### 3. Session Management

**Our Implementation:**
- One-off queries
- Browser opens/closes each query
- No conversation context
- No concurrent queries

**Their Implementation:**
```typescript
// Multi-turn conversation with session persistence
ask_question({
    question: "Tell me about Mickey",
    sessionId: "session-1"
})

ask_question({
    question: "What's his relationship with The Chronicler?",
    sessionId: "session-1"  // Same session - maintains context!
})

ask_question({
    question: "How does his arc develop?",
    sessionId: "session-1"  // Continues conversation
})
```

**Benefits:**
- Follow-up questions work naturally
- NotebookLM sees conversation context
- Better answers from Gemini
- Concurrent sessions (up to 10)

---

### 4. Tag-Based Organization

**Example for Writers Factory:**

```typescript
// Organize by project
add_notebook({
    url: "...",
    name: "The Explants - Characters",
    tags: ["explants", "characters", "trilogy"]
})

add_notebook({
    url: "...",
    name: "One Week Novel Course - Examples",
    tags: ["course", "teaching", "examples"]
})

// Search by tag
search_notebooks({ query: "explants" })
// Returns: All Explants-related notebooks

search_notebooks({ query: "characters" })
// Returns: All character-focused notebooks
```

---

## What They CAN'T Do (Important Clarifications)

### ❌ Cannot Create Notebooks in NotebookLM

```typescript
// This DOES NOT create a new notebook in NotebookLM!
add_notebook({
    url: "https://notebooklm.google.com/.../new-notebook",
    name: "My New Notebook"
})
```

**Reality:** User must:
1. Go to notebooklm.google.com
2. Click "New Notebook"
3. Upload sources manually
4. Copy the URL
5. Register with `add_notebook()`

**What `add_notebook` DOES:** Adds existing NotebookLM URL to local library.

---

### ❌ Cannot Add Sources to Notebooks

```typescript
// This DOES NOT upload files to NotebookLM!
add_notebook({
    url: "...",
    sources: ["character_profile.pdf"]  // ❌ Not supported
})
```

**Reality:** User must upload sources via NotebookLM web interface.

---

### ❌ Cannot Write Content to Notebooks

```typescript
// This DOES NOT add text to the notebook!
update_notebook({
    id: "notebook-1",
    content: "Mickey is an Enhanced human..."  // ❌ Not supported
})
```

**Reality:** `update_notebook()` only updates **metadata** (name, tags, description in local library).

---

## What They CAN Do (Metadata Management)

### ✅ Register Existing Notebooks

```typescript
add_notebook({
    url: "https://notebooklm.google.com/notebook/abc",
    name: "Character Profiles",
    description: "Character backstories and development arcs",
    topics: ["characters", "psychology", "arcs"],
    content_types: ["profiles", "notes", "examples"],
    use_cases: ["character-validation", "continuity-checking"],
    tags: ["characters", "explants", "mickey-bardot"]
})
```

**Stored locally in:** MCP server's database/config

---

### ✅ Update Metadata

```typescript
update_notebook({
    id: "notebook-1",
    description: "Updated: Now includes secondary characters",
    tags: ["characters", "explants", "mickey-bardot", "sarah-chen"]
})
```

**Effect:** Updates local library only. NotebookLM unchanged.

---

### ✅ Track Usage Statistics

```typescript
get_library_stats()
// Returns:
{
    total_notebooks: 5,
    total_queries: 127,
    most_used: "Character Profiles (47 queries)",
    notebooks: [
        {
            id: "notebook-1",
            name: "Character Profiles",
            use_count: 47,
            last_used: "2025-11-15T10:30:00Z"
        },
        // ...
    ]
}
```

---

## Integration Strategy for Writers Factory

### Option 1: Use Their MCP Server Directly (RECOMMENDED)

**Approach:**
1. Install their NotebookLM MCP server
2. Configure as separate MCP server in `.claude/mcp.json`
3. Writers Factory calls their MCP tools via MCP protocol
4. No need to rewrite our NotebookLM client

**Configuration:**
```json
{
  "mcpServers": {
    "writers-factory": {
      "command": "python",
      "args": ["factory/mcp/run_mcp_server.py"],
      "cwd": "/path/to/writers-factory-core"
    },
    "notebooklm": {
      "command": "npx",
      "args": ["-y", "@pleasepromo/notebooklm-mcp"],
      "env": {
        "NOTEBOOKLM_HEADLESS": "true"
      }
    }
  }
}
```

**Benefits:**
- ✅ No code duplication
- ✅ They maintain browser automation
- ✅ We get all 15 tools immediately
- ✅ Future updates automatic (npm package)

**Drawbacks:**
- Two separate MCP servers (complexity)
- JavaScript dependency (we're Python-based)
- Less control over implementation

---

### Option 2: Port Their Architecture to Python

**Approach:**
1. Rewrite `factory/research/notebooklm_client.py` with their patterns
2. Add library management
3. Add session management
4. Add metadata/tagging

**New Architecture:**

```python
# factory/research/notebooklm_library.py

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class NotebookMetadata:
    id: str
    url: str
    name: str
    description: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    content_types: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    use_count: int = 0
    last_used: Optional[datetime] = None

class NotebookLibrary:
    """Manage collection of NotebookLM notebooks."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.notebooks: Dict[str, NotebookMetadata] = {}
        self.active_notebook_id: Optional[str] = None
        self._load_library()

    def add_notebook(
        self,
        url: str,
        name: str,
        description: Optional[str] = None,
        topics: Optional[List[str]] = None,
        content_types: Optional[List[str]] = None,
        use_cases: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """Register notebook in library."""
        notebook_id = self._generate_id()
        notebook = NotebookMetadata(
            id=notebook_id,
            url=url,
            name=name,
            description=description,
            topics=topics or [],
            content_types=content_types or [],
            use_cases=use_cases or [],
            tags=tags or []
        )
        self.notebooks[notebook_id] = notebook
        self._save_library()
        return notebook_id

    def select_notebook(self, notebook_id: str) -> None:
        """Set active notebook."""
        if notebook_id not in self.notebooks:
            raise ValueError(f"Notebook {notebook_id} not found")
        self.active_notebook_id = notebook_id

    def get_active_notebook(self) -> Optional[NotebookMetadata]:
        """Get currently selected notebook."""
        if not self.active_notebook_id:
            return None
        return self.notebooks.get(self.active_notebook_id)

    def list_notebooks(self) -> List[NotebookMetadata]:
        """List all registered notebooks."""
        return list(self.notebooks.values())

    def search_notebooks(self, query: str) -> List[NotebookMetadata]:
        """Search by name, description, or tags."""
        query_lower = query.lower()
        results = []
        for notebook in self.notebooks.values():
            if (query_lower in notebook.name.lower() or
                (notebook.description and query_lower in notebook.description.lower()) or
                any(query_lower in tag.lower() for tag in notebook.tags)):
                results.append(notebook)
        return results

    def update_notebook(
        self,
        notebook_id: str,
        **kwargs
    ) -> None:
        """Update notebook metadata."""
        if notebook_id not in self.notebooks:
            raise ValueError(f"Notebook {notebook_id} not found")

        notebook = self.notebooks[notebook_id]
        for key, value in kwargs.items():
            if hasattr(notebook, key):
                setattr(notebook, key, value)

        self._save_library()

    def remove_notebook(self, notebook_id: str) -> None:
        """Remove notebook from library."""
        if notebook_id in self.notebooks:
            del self.notebooks[notebook_id]
            if self.active_notebook_id == notebook_id:
                self.active_notebook_id = None
            self._save_library()

    def record_usage(self, notebook_id: str) -> None:
        """Track notebook usage."""
        if notebook_id in self.notebooks:
            notebook = self.notebooks[notebook_id]
            notebook.use_count += 1
            notebook.last_used = datetime.now()
            self._save_library()

    def get_library_stats(self) -> Dict:
        """Get aggregate statistics."""
        return {
            "total_notebooks": len(self.notebooks),
            "total_queries": sum(nb.use_count for nb in self.notebooks.values()),
            "most_used": max(
                self.notebooks.values(),
                key=lambda nb: nb.use_count,
                default=None
            ),
            "notebooks": sorted(
                self.notebooks.values(),
                key=lambda nb: nb.use_count,
                reverse=True
            )
        }

    def _generate_id(self) -> str:
        """Generate unique notebook ID."""
        import uuid
        return f"notebook-{uuid.uuid4().hex[:8]}"

    def _load_library(self) -> None:
        """Load library from disk."""
        if self.storage_path.exists():
            import json
            data = json.loads(self.storage_path.read_text())
            self.notebooks = {
                nb_id: NotebookMetadata(**nb_data)
                for nb_id, nb_data in data.get("notebooks", {}).items()
            }
            self.active_notebook_id = data.get("active_notebook_id")

    def _save_library(self) -> None:
        """Save library to disk."""
        import json
        from dataclasses import asdict
        data = {
            "notebooks": {
                nb_id: asdict(nb)
                for nb_id, nb in self.notebooks.items()
            },
            "active_notebook_id": self.active_notebook_id
        }
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(json.dumps(data, indent=2, default=str))
```

**Enhanced NotebookLM Client:**

```python
# factory/research/notebooklm_client.py (enhanced)

class NotebookLMClient:
    """Enhanced client with library and session management."""

    def __init__(
        self,
        auth_tokens_path: Optional[Path] = None,
        library_path: Optional[Path] = None
    ):
        self.auth_tokens_path = auth_tokens_path or (
            Path.home() / ".writers-factory" / "notebooklm_auth.json"
        )
        self.library = NotebookLibrary(
            library_path or Path.home() / ".writers-factory" / "notebooklm_library.json"
        )
        self.sessions: Dict[str, BrowserSession] = {}

    async def query(
        self,
        question: str,
        notebook_url: Optional[str] = None,
        notebook_id: Optional[str] = None,
        session_id: Optional[str] = None,
        timeout: int = 30
    ) -> Dict:
        """
        Query notebook with optional session context.

        Args:
            question: Question to ask
            notebook_url: Direct URL (optional if notebook_id or active notebook set)
            notebook_id: Library notebook ID (optional if notebook_url provided)
            session_id: Session ID for multi-turn conversation (optional)
            timeout: Query timeout

        Returns:
            Query response with answer and citations
        """
        # Determine notebook URL
        if not notebook_url:
            if notebook_id:
                notebook = self.library.notebooks.get(notebook_id)
                if not notebook:
                    raise ValueError(f"Notebook {notebook_id} not found in library")
                notebook_url = notebook.url
            else:
                # Use active notebook
                active = self.library.get_active_notebook()
                if not active:
                    raise ValueError("No notebook specified and no active notebook set")
                notebook_url = active.url
                notebook_id = active.id

        # Get or create session
        if session_id:
            session = self.sessions.get(session_id)
            if not session:
                session = await self._create_session()
                self.sessions[session_id] = session
        else:
            session = await self._create_session()

        # Execute query (existing implementation)
        response = await self._execute_query(
            session=session,
            notebook_url=notebook_url,
            question=question,
            timeout=timeout
        )

        # Track usage
        if notebook_id:
            self.library.record_usage(notebook_id)

        return response

    async def _create_session(self) -> BrowserSession:
        """Create new browser session."""
        # Implementation
        pass

    async def _execute_query(
        self,
        session: BrowserSession,
        notebook_url: str,
        question: str,
        timeout: int
    ) -> Dict:
        """Execute query in session."""
        # Existing implementation from current client
        pass
```

**Benefits:**
- ✅ Full control over implementation
- ✅ Python-native (matches our stack)
- ✅ Can customize for Writers Factory needs
- ✅ Integrated with existing codebase

**Drawbacks:**
- Significant development time
- We maintain browser automation
- Need to implement all 15 tools

---

### Option 3: Hybrid Approach (BEST OF BOTH)

**Approach:**
1. Use their MCP server for multi-notebook management
2. Keep our Python client for Sprint 15 beginner mode
3. Gradually migrate to their architecture

**Phase 1 (Sprint 15):**
- Use our existing client for beginner voice extraction
- Single notebook (beginner's initial collection)

**Phase 2 (Sprint 16):**
- Install their MCP server
- Add multi-notebook support using their library tools
- Writers Factory UI → calls their MCP server

**Phase 3 (Sprint 17+):**
- Port their architecture to Python
- Replace MCP dependency with native implementation
- Full control + all features

---

## Recommended Integration Plan

### Immediate (Sprint 15)

**Keep current implementation:**
```python
# For beginner voice extraction
client = NotebookLMClient()
response = await client.query(
    question="Extract user's personal writing samples",
    notebook_url=user_provided_url
)
```

**No changes needed** - current client works for single-notebook beginner flow.

---

### Sprint 16: Add Multi-Notebook Support

**Install their MCP server:**
```bash
npm install -g @pleasepromo/notebooklm-mcp
```

**Add to Writers Factory MCP tools:**
```python
# factory/mcp/notebooklm_bridge.py

class NotebookLMBridge:
    """Bridge to PleasePrompto NotebookLM MCP server."""

    async def add_notebook_to_library(
        self,
        url: str,
        name: str,
        purpose: str,  # "ideas", "characters", "structure"
        tags: List[str]
    ) -> str:
        """Add notebook to library via their MCP server."""
        # Call their add_notebook tool via MCP protocol
        pass

    async def query_notebook(
        self,
        notebook_id: str,
        question: str
    ) -> str:
        """Query notebook from library."""
        # Call their select_notebook + ask_question tools
        pass
```

**User workflow:**
```python
# Setup - user provides URLs for specialized notebooks
bridge = NotebookLMBridge()

ideas_id = await bridge.add_notebook_to_library(
    url="https://notebooklm.google.com/.../ideas",
    name="Ideas & World-Building",
    purpose="ideas",
    tags=["creative", "plot", "world-building"]
)

characters_id = await bridge.add_notebook_to_library(
    url="https://notebooklm.google.com/.../characters",
    name="Character Profiles",
    purpose="characters",
    tags=["characters", "backstories"]
)

# Usage - query specific notebooks
answer = await bridge.query_notebook(
    notebook_id=characters_id,
    question="What is Mickey's character arc?"
)
```

---

### Sprint 17: Port to Python (Optional)

**If we want full control**, port their architecture:
1. Implement `NotebookLibrary` class (shown above)
2. Enhanced `NotebookLMClient` with sessions
3. Remove dependency on their MCP server

---

## Key Takeaways

### What You Asked vs. What's Possible

**Your Question:**
> "can we send information to an existing or to even create a notebook in notebook, LM"

**Answer:**

**Create notebooks:** ❌ No - must be done manually in NotebookLM web interface

**Add to existing:** ⚠️ Partial
- ❌ Cannot add sources/content to NotebookLM
- ✅ CAN add notebook URLs to local library
- ✅ CAN update metadata (tags, descriptions)
- ✅ CAN query across multiple notebooks

**Better framing:** Their system doesn't CREATE notebooks, it MANAGES references to existing notebooks.

---

### What This Enables for Writers Factory

**Your Multi-Notebook Architecture (FULLY SUPPORTED):**

```python
# One-time setup
library.add_notebook(
    url="https://notebooklm.google.com/.../ideas",
    name="Ideas Notebook",
    topics=["creative-flashes", "world-building", "plot"],
    use_cases=["brainstorming", "inspiration"]
)

library.add_notebook(
    url="https://notebooklm.google.com/.../characters",
    name="Character Notebook",
    topics=["characters", "backstories", "relationships"],
    use_cases=["character-validation", "continuity"]
)

library.add_notebook(
    url="https://notebooklm.google.com/.../structure",
    name="Structure Notebook",
    topics=["chapters", "acts", "outlines"],
    use_cases=["planning", "structure"]
)

# Contextual queries
library.select_notebook(name="Character Notebook")
client.query("What's Mickey's relationship with The Chronicler?")
# Uses character notebook automatically

library.select_notebook(name="Ideas Notebook")
client.query("Any new plot twists added recently?")
# Switches to ideas notebook

library.select_notebook(name="Structure Notebook")
client.query("What's the structure of Act 2?")
# Switches to structure notebook
```

**This is EXACTLY what you wanted!**

---

## Final Recommendation

**For Sprint 15 (Beginner Mode):**
- ✅ Keep current implementation (works fine for single notebook)

**For Sprint 16 (Multi-Notebook):**
- ✅ **Option 1:** Install their MCP server (fastest, lowest effort)
- ⚠️ **Option 2:** Port to Python (more control, more work)

**My Recommendation:** **Option 1** (use their MCP server)

**Why:**
1. They already solved multi-notebook management
2. Actively maintained (recent commits)
3. We can focus on Writers Factory features, not browser automation
4. Can always port to Python later if needed

**Integration Effort:** ~8-12 hours to build bridge layer

---

## Next Steps

1. **Evaluate their MCP server:** Install and test with your notebooks
2. **Design bridge layer:** How Writers Factory calls their tools
3. **Update Sprint 16 spec:** Include multi-notebook architecture
4. **Prototype:** Test with your actual NotebookLM notebooks

Would you like me to create a Sprint 16 specification for multi-notebook integration using their MCP server?
