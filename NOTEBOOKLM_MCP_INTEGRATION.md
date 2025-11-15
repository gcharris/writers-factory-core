# NotebookLM MCP Server Integration

**Date**: November 14, 2025
**Priority**: HIGH (Critical for research workflow)
**Goal**: Add NotebookLM integration so all users can query research notebooks

---

## 🎯 Why This Is Needed

**Your Current Workflow**:
- You use the `notebooklm` Claude Code skill to query your Explants research
- Character profiles, worldbuilding, story structure all live in NotebookLM
- This is **critical** for maintaining consistency in The Explants trilogy

**The Problem**:
- Claude Code skills are only available to Claude Code users
- Other users of Writers Factory won't have access
- Students in your course won't be able to query NotebookLM
- The web interface has no way to access NotebookLM

**The Solution**:
- Add the NotebookLM MCP server (same developer as your skill)
- Integrate into Writers Factory backend
- Expose via UI so anyone can query their notebooks
- Works for all users, not just Claude Code users

---

## 📦 What Is NotebookLM MCP Server?

**Repository**: https://github.com/PleasePrompto/notebooklm-mcp

**What It Does**:
- Queries Google NotebookLM via browser automation
- Returns answers grounded in your uploaded documents
- Provides citations (source tracking)
- Zero hallucinations (only answers from your docs)

**Key Features**:
- **Library Management**: Save notebook links with tags
- **Intelligent Selection**: Claude auto-selects relevant notebooks
- **Cross-Tool Support**: Works in Claude Code, Cursor, etc.
- **Source Citations**: Every answer includes document references

**How It Works**:
1. You create notebooks on notebooklm.google.com
2. Upload documents (PDFs, Word docs, links, etc.)
3. MCP server uses browser automation to query
4. Gemini 2.5 processes your documents
5. Returns grounded answers with citations

---

## 🏗️ Current State vs Desired State

### Current State (Sprint 6 MCP Server)

**What you have**:
- MCP server with 10 tools
- Manuscript queries (structure, scenes, search)
- Character analysis (depth, contradictions)
- **Hardcoded craft principles** (static, from NotebookLM analysis)

**File**: `factory/mcp/server.py`

**Craft knowledge tools**:
```python
@self.server.tool()
async def get_craft_principles() -> dict:
    """Get core writing craft principles."""
    # Returns hardcoded principles from NotebookLM analysis
    return {
        "principles": [
            {
                "principle": "Complexity is created by CONTRADICTION",
                "explanation": "Characters must embody opposing forces..."
            },
            # ... more hardcoded principles
        ]
    }
```

**Limitation**: Static data, can't query live NotebookLM

---

### Desired State (With NotebookLM Integration)

**What you'll have**:
- All current MCP tools (manuscript, character analysis)
- **+ Live NotebookLM queries** (dynamic, always up-to-date)
- **+ Notebook library management** (multiple notebooks with tags)
- **+ Citation tracking** (source references)

**New tools**:
```python
@self.server.tool()
async def query_notebooklm(question: str, notebook_id: str = None) -> dict:
    """Query NotebookLM for research answers with citations."""
    # Queries live NotebookLM
    # Returns answer + sources

@self.server.tool()
async def list_notebooks() -> dict:
    """List available NotebookLM notebooks with tags."""
    # Returns user's notebook library

@self.server.tool()
async def add_notebook(url: str, name: str, tags: list) -> dict:
    """Add a notebook to the library."""
    # Saves notebook for future queries
```

---

## 🔧 Implementation Plan

### Option 1: Standalone MCP Server (Recommended)

**Approach**: Run NotebookLM MCP server alongside Writers Factory MCP server

**Architecture**:
```
Claude Code / Cursor AI
    ↓
┌─────────────────────────────────┐
│ MCP Servers (both running)      │
│                                  │
│  writers-factory                 │
│  - Manuscript queries            │
│  - Character analysis            │
│  - Scene search                  │
│                                  │
│  notebooklm                      │
│  - Query notebooks               │
│  - Manage library                │
│  - Get citations                 │
└─────────────────────────────────┘
```

**Setup** (in `.claude/mcp.json` or `claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "writers-factory": {
      "command": "python",
      "args": ["factory/mcp/run_mcp_server.py"],
      "cwd": "/Users/gch2024/writers-factory-core"
    },
    "notebooklm": {
      "command": "npx",
      "args": ["notebooklm-mcp@latest"]
    }
  }
}
```

**Pros**:
- ✅ No code changes to Writers Factory
- ✅ Maintained by original developer
- ✅ Auto-updates (npx pulls latest)
- ✅ Works in Claude Code immediately

**Cons**:
- ⚠️ Requires Node.js (npx)
- ⚠️ Two separate servers to manage

---

### Option 2: Integrate Into Writers Factory Backend

**Approach**: Add NotebookLM querying directly to Writers Factory

**Architecture**:
```
Writers Factory Backend (simple_app.py)
    ↓
┌─────────────────────────────────┐
│ New Endpoints                    │
│                                  │
│  POST /api/notebooklm/query      │
│  GET  /api/notebooklm/notebooks  │
│  POST /api/notebooklm/add        │
└─────────────────────────────────┘
    ↓
Python NotebookLM client
(browser automation)
```

**Implementation**:
1. Install `notebooklm-python` package (if exists)
2. Add endpoints to `simple_app.py`
3. Add UI in frontend (NotebookLM panel)
4. Add to MCP server tools

**Pros**:
- ✅ Fully integrated (one system)
- ✅ UI available for web users
- ✅ Single server to manage

**Cons**:
- ⚠️ More complex implementation
- ⚠️ Need to maintain browser automation
- ⚠️ Requires Google auth management

---

## 🎯 Recommended Approach

**For You (Immediate Use)**: **Option 1** - Standalone MCP server

**For Students (Course)**: **Option 2** - Integrated into Writers Factory

---

## 📝 Implementation: Option 1 (Quick Setup)

### Step 1: Install NotebookLM MCP Server

```bash
# Option A: Claude Code auto-install
claude mcp add notebooklm npx notebooklm-mcp@latest

# Option B: Manual install (if Claude Code command doesn't work)
npm install -g notebooklm-mcp
```

### Step 2: Configure MCP Servers

**File**: `.claude/mcp.json` (or `~/Library/Application Support/Claude/claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "writers-factory": {
      "command": "python",
      "args": ["factory/mcp/run_mcp_server.py"],
      "cwd": "/Users/gch2024/writers-factory-core",
      "env": {
        "PYTHONPATH": "/Users/gch2024/writers-factory-core"
      }
    },
    "notebooklm": {
      "command": "npx",
      "args": ["notebooklm-mcp@latest"],
      "env": {}
    }
  }
}
```

### Step 3: Authenticate with Google

**First time only**:
```bash
# Run NotebookLM MCP server manually to authenticate
npx notebooklm-mcp@latest

# It will open browser for Google login
# Complete authentication
# Server will save credentials
```

### Step 4: Share Notebook Links

**In your NotebookLM** (https://notebooklm.google.com):
1. Open your Explants notebook
2. Click "Share" → Copy link
3. Tell Claude Code the link

**Example**:
```
Claude Code, add this NotebookLM notebook to your library:
URL: https://notebooklm.google.com/notebook/8b1f262a-fe2a-45f3-8c3b-39689c9d3123
Name: "Explants Story Bible"
Tags: ["explants", "characters", "worldbuilding", "story-structure"]
```

### Step 5: Use in Claude Code

**Query NotebookLM**:
```
User: "What are Mickey Bardot's key character contradictions according to my research?"
Claude Code: *calls notebooklm tool*
Claude Code: "According to your Explants Story Bible, Mickey's core contradictions are..."
```

**Automatic library selection**:
```
User: "What's the morphic resonance framework in The Explants?"
Claude Code: *automatically selects "Explants Story Bible" notebook*
Claude Code: *queries for morphic resonance info*
Claude Code: "Based on your worldbuilding notes..."
```

---

## 📝 Implementation: Option 2 (Integrated - For Later)

**Tasks**:

### Task NB-01: Backend Integration

**Add NotebookLM querying to Writers Factory backend**

**File**: `webapp/backend/simple_app.py`

**New endpoints**:
```python
from playwright.async_api import async_playwright
# or from selenium import webdriver (whichever browser automation library)

@app.post("/api/notebooklm/query")
async def query_notebooklm(request: dict):
    """Query a NotebookLM notebook."""
    question = request.get("question")
    notebook_url = request.get("notebook_url")

    # Use browser automation to query NotebookLM
    # Return answer + citations
    pass

@app.get("/api/notebooklm/notebooks")
async def list_notebooks():
    """List saved NotebookLM notebooks."""
    # Load from storage (JSON file or DB)
    pass

@app.post("/api/notebooklm/add")
async def add_notebook(request: dict):
    """Add a notebook to the library."""
    # Save to storage
    pass
```

### Task NB-02: Frontend UI

**Create NotebookLM panel in Writers Factory UI**

**Component**: `webapp/frontend-v2/src/features/research/NotebookLMPanel.jsx`

**UI**:
```jsx
export function NotebookLMPanel() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);

  return (
    <div className="notebooklm-panel">
      <h2>Research Assistant</h2>

      {/* Notebook library */}
      <NotebookList />

      {/* Query input */}
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about your research..."
      />

      <button onClick={handleQuery}>Ask NotebookLM</button>

      {/* Answer with citations */}
      {answer && (
        <div className="answer">
          <p>{answer.text}</p>
          <div className="citations">
            {answer.sources.map(source => (
              <cite key={source.id}>{source.title}</cite>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

### Task NB-03: MCP Server Tools

**Add NotebookLM tools to Writers Factory MCP server**

**File**: `factory/mcp/server.py`

```python
@self.server.tool()
async def query_notebooklm(question: str, notebook_name: str = None) -> dict:
    """Query NotebookLM for research answers with citations.

    Args:
        question: The question to ask
        notebook_name: Optional notebook to query (auto-selects if omitted)

    Returns:
        {"answer": str, "sources": list, "notebook": str}
    """
    try:
        response = await self.client.post(
            f"{self.backend_url}/api/notebooklm/query",
            json={"question": question, "notebook": notebook_name}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@self.server.tool()
async def list_notebooklm_notebooks() -> dict:
    """List available NotebookLM notebooks."""
    # Implementation
    pass
```

---

## 🎓 For Your Course Students

**Setup Instructions** (in QUICK_START.md):

### NotebookLM Integration (Optional)

**What it is**: Query your research notebooks directly from Writers Factory

**Setup** (5 minutes):

1. **Create notebook** on https://notebooklm.google.com
2. **Upload research docs** (character profiles, worldbuilding, etc.)
3. **Install MCP server**: `claude mcp add notebooklm npx notebooklm-mcp@latest`
4. **Authenticate** with Google (one-time)
5. **Share notebook link** with Claude Code

**Usage**:
- Ask questions in Claude Code: "What are my protagonist's goals?"
- Writers Factory AI tools can query your research
- Get answers grounded in your documents
- See source citations

---

## 🚀 Immediate Next Steps (For You)

**To get NotebookLM working NOW** (5-10 minutes):

1. **Check if you have npx**:
   ```bash
   npx --version
   # If not found: brew install node
   ```

2. **Install NotebookLM MCP**:
   ```bash
   claude mcp add notebooklm npx notebooklm-mcp@latest
   # OR manually: npm install -g notebooklm-mcp
   ```

3. **Configure both MCP servers** in `.claude/mcp.json`

4. **Authenticate**:
   ```bash
   npx notebooklm-mcp@latest
   # Complete Google auth in browser
   ```

5. **Share notebook link** with Claude Code:
   ```
   Add this notebook to your library:
   URL: https://notebooklm.google.com/notebook/[your-id]
   Name: "Explants Research"
   Tags: ["explants", "characters", "worldbuilding"]
   ```

6. **Test it**:
   ```
   Query the Explants notebook: "What are Mickey's core contradictions?"
   ```

---

## 📊 Comparison

| Feature | Current (Hardcoded) | With NotebookLM MCP |
|---------|---------------------|---------------------|
| **Craft principles** | Static | Dynamic, queryable |
| **Character info** | In code | In notebooks |
| **Worldbuilding** | In code | In notebooks |
| **Updates** | Require code change | Update notebook |
| **Student access** | Same for everyone | Their own notebooks |
| **Citations** | None | Full source tracking |
| **Fresh info** | Stale | Always current |

---

## ✅ Decision

**Recommendation**:

**Phase 1 (Now)**: **Option 1** - Standalone MCP server
- Quick setup (5-10 minutes)
- Works immediately for you
- No code changes needed
- Maintained by original developer

**Phase 2 (Later)**: **Option 2** - Integrated backend
- Add to Writers Factory for students
- Build UI panel
- Full integration
- Better user experience

**You can use Option 1 starting today!**

---

## 📝 Add to Handoff Document

**For your new Claude Code agent**, add this to HANDOFF_TO_NEW_CLAUDE_CODE.md:

```markdown
## NotebookLM Integration

User has NotebookLM notebooks with research for The Explants:
- Character profiles
- Worldbuilding (morphic resonance, quantum implants)
- Story structure
- Themes and philosophy

**Current setup**:
- User has `notebooklm` Claude Code skill (for personal use)
- NotebookLM MCP server can be added for broader access

**If user asks to query NotebookLM**:
- Use the notebooklm MCP server if configured
- Otherwise, mention they can add it with: `claude mcp add notebooklm npx notebooklm-mcp@latest`

**Key notebook**: https://notebooklm.google.com/notebook/8b1f262a-fe2a-45f3-8c3b-39689c9d3123
```

---

**Want me to help you set this up right now?** It only takes 5-10 minutes and then you'll have live NotebookLM queries in Writers Factory!