# 📋 Cloud Agent Sprint 6: MCP Server Implementation

**Sprint**: 6 of 6 (Final Sprint!)
**Timeline**: 2-3 days
**Priority**: HIGH (Enables external tool integration)
**Status**: Ready to start

---

## 🎯 Sprint Goal

Implement an **MCP (Model Context Protocol) Server** that exposes Writers Factory's capabilities to external tools like Claude Code, Cursor AI, and VS Code extensions.

**What is MCP?**
- Protocol by Anthropic for AI-to-tool communication
- Allows external tools to query your Writers Factory data
- Runs as background process (invisible to end users)
- Uses JSON-RPC for communication

**Key Point**: MCP is an **optional interface layer** on top of Writers Factory's existing backend. It doesn't replace anything - just adds external access.

---

## 📚 Background Reading

**MCP Specification**: https://modelcontextprotocol.io/
**Python SDK**: https://github.com/anthropics/python-mcp-sdk

**Core Concepts**:
1. **Server**: Your Writers Factory MCP server (runs in background)
2. **Client**: Claude Code, Cursor AI, etc. (connects to your server)
3. **Tools**: Functions exposed via MCP (e.g., "get_scene", "analyze_character")
4. **Resources**: Data exposed via MCP (e.g., manuscript structure)

---

## ✅ Tasks (5 total)

### Task 6-01: MCP Server Setup ⭐ CRITICAL

**File**: `factory/mcp/server.py` (NEW)

**Requirements**:
1. Create MCP server using `python-mcp-sdk`
2. Initialize connection to Writers Factory backend
3. Set up JSON-RPC handler
4. Add error handling and logging

**Example Structure**:
```python
from mcp import Server, Tool, Resource
from mcp.types import TextContent, ImageContent
import httpx  # For calling Writers Factory API

class WritersFactoryMCP:
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self.backend_url = backend_url
        self.server = Server("writers-factory")
        self.client = httpx.AsyncClient()

        # Register tools and resources
        self.register_tools()
        self.register_resources()

    def register_tools(self):
        # We'll add tools in Task 6-02
        pass

    def register_resources(self):
        # We'll add resources in Task 6-03
        pass

    async def start(self):
        """Start MCP server (listens on stdio by default)."""
        await self.server.run()

if __name__ == "__main__":
    import asyncio
    server = WritersFactoryMCP()
    asyncio.run(server.start())
```

**Dependencies**:
```bash
# Add to requirements.txt:
mcp>=0.1.0  # Anthropic's MCP SDK
httpx>=0.24.0  # For async HTTP requests
```

**Success Criteria**:
- ✅ Server starts without errors
- ✅ Listens on stdio for MCP protocol messages
- ✅ Can connect to Writers Factory backend at localhost:8000

---

### Task 6-02: Manuscript Query Tools ⭐ HIGH

**File**: `factory/mcp/server.py` (MODIFY)

**Requirements**:
Add MCP tools for querying manuscript data:

**Tools to implement**:

**1. `get_manuscript_structure`**
```python
@self.server.tool()
async def get_manuscript_structure() -> dict:
    """Get complete manuscript structure (acts, chapters, scenes)."""
    response = await self.client.get(f"{self.backend_url}/api/manuscript/tree")
    return response.json()
```

**2. `get_scene_content`**
```python
@self.server.tool()
async def get_scene_content(scene_id: str) -> dict:
    """Get full content of a specific scene."""
    response = await self.client.get(
        f"{self.backend_url}/api/manuscript/explants-v1/scenes/{scene_id}"
    )
    data = response.json()
    return {
        "id": data["id"],
        "title": data["title"],
        "content": data["content"],
        "word_count": data["word_count"]
    }
```

**3. `search_scenes`**
```python
@self.server.tool()
async def search_scenes(query: str) -> list:
    """Search scenes by keyword or phrase.

    Args:
        query: Search term (e.g., "Mickey", "quantum", "confrontation")

    Returns:
        List of matching scenes with titles and excerpts
    """
    response = await self.client.get(
        f"{self.backend_url}/api/manuscript/search",
        params={"q": query}
    )
    return response.json()["results"]
```

**4. `get_characters`**
```python
@self.server.tool()
async def get_characters() -> list:
    """Get all characters in the manuscript."""
    response = await self.client.get(
        f"{self.backend_url}/api/manuscript/explants-v1/characters"
    )
    return response.json()["characters"]
```

**5. `get_character_scenes`**
```python
@self.server.tool()
async def get_character_scenes(character_name: str) -> list:
    """Get all scenes featuring a specific character.

    Args:
        character_name: Character name (e.g., "Mickey Bardot")

    Returns:
        List of scenes with this character
    """
    # First get all characters to find ID
    chars = await self.get_characters()
    char = next((c for c in chars if c["name"].lower() == character_name.lower()), None)

    if not char:
        return {"error": f"Character '{character_name}' not found"}

    # Return scenes from character's scene_appearances field
    return char.get("scene_appearances", [])
```

**Tool Registration**:
```python
def register_tools(self):
    # Tools are registered via @self.server.tool() decorator
    # MCP SDK automatically exposes them to clients
    pass
```

**Success Criteria**:
- ✅ All 5 tools registered and callable
- ✅ Tools return proper JSON responses
- ✅ Error handling for missing scenes/characters
- ✅ Tools show up in Claude Code's MCP tool list

---

### Task 6-03: Character Analysis Tools ⭐ HIGH

**File**: `factory/mcp/server.py` (MODIFY)

**Requirements**:
Add MCP tools for character analysis (using Sprint 5's analyzer):

**Tools to implement**:

**1. `analyze_character`**
```python
@self.server.tool()
async def analyze_character(character_id: str) -> dict:
    """Analyze character dimensional depth (from Sprint 5).

    Args:
        character_id: Character UUID

    Returns:
        Analysis with depth_score, flags, recommendations
    """
    response = await self.client.post(
        f"{self.backend_url}/api/character/{character_id}/analyze"
    )
    return response.json()
```

**2. `check_character_contradictions`**
```python
@self.server.tool()
async def check_character_contradictions(character_name: str) -> dict:
    """Check if character has sufficient internal/external contradictions.

    Args:
        character_name: Character name

    Returns:
        Contradiction analysis with specific flags
    """
    # Get character by name
    chars = await self.get_characters()
    char = next((c for c in chars if c["name"].lower() == character_name.lower()), None)

    if not char:
        return {"error": f"Character '{character_name}' not found"}

    # Analyze
    analysis = await self.analyze_character(char["id"])

    # Filter to just contradiction-related flags
    contradiction_flags = [
        f for f in analysis.get("flags", [])
        if "CONTRADICTION" in f["type"]
    ]

    return {
        "character": char["name"],
        "depth_score": analysis["depth_score"],
        "contradiction_flags": contradiction_flags,
        "has_contradictions": len(contradiction_flags) == 0
    }
```

**3. `suggest_character_improvements`**
```python
@self.server.tool()
async def suggest_character_improvements(character_name: str) -> list:
    """Get actionable recommendations for improving character depth.

    Args:
        character_name: Character name

    Returns:
        List of recommendations with examples
    """
    # Get character
    chars = await self.get_characters()
    char = next((c for c in chars if c["name"].lower() == character_name.lower()), None)

    if not char:
        return [{"error": f"Character '{character_name}' not found"}]

    # Analyze
    analysis = await self.analyze_character(char["id"])

    # Extract recommendations from flags
    recommendations = []
    for flag in analysis.get("flags", []):
        recommendations.append({
            "severity": flag["severity"],
            "issue": flag["message"],
            "suggestion": flag.get("recommendation", ""),
            "example": flag.get("example", "")
        })

    return recommendations
```

**Success Criteria**:
- ✅ All 3 character tools working
- ✅ Returns analysis from Sprint 5's character_analyzer.py
- ✅ Tools callable from Claude Code via MCP

---

### Task 6-04: Knowledge Base Integration ⭐ MEDIUM

**File**: `factory/mcp/server.py` (MODIFY)

**Requirements**:
Add MCP tools for querying NotebookLM knowledge base:

**Note**: This assumes you have the `notebooklm` skill already set up (which you do).

**Tools to implement**:

**1. `query_craft_knowledge`**
```python
@self.server.tool()
async def query_craft_knowledge(question: str) -> str:
    """Query NotebookLM for writing craft advice.

    Args:
        question: Question about writing craft (e.g., "How do I create tension?")

    Returns:
        Answer from NotebookLM with source citations
    """
    # This would call your NotebookLM skill
    # For now, return a placeholder that guides users to use the skill directly
    return (
        f"To query craft knowledge, use the 'notebooklm' skill directly in Claude Code:\n"
        f"  1. Invoke skill: notebooklm\n"
        f"  2. Ask: '{question}'\n\n"
        f"NotebookLM integration via MCP requires browser automation, "
        f"which is better handled by the skill system."
    )
```

**2. `get_craft_principles`**
```python
@self.server.tool()
async def get_craft_principles() -> dict:
    """Get core writing craft principles from NotebookLM analysis.

    Returns:
        Key principles with explanations
    """
    return {
        "contradiction_principle": {
            "title": "Complexity is created by CONTRADICTION",
            "description": "Dimensional characters have internal contradictions (guilt-ridden ambition) and external contradictions (charming thief)",
            "examples": [
                "True Character vs Characterization (inner core vs observable)",
                "Ambitious yet guilty (internal contradiction)",
                "Loyal but appears untrustworthy (external contradiction)"
            ]
        },
        "protagonist_dimensionality": {
            "title": "Protagonist must be most dimensional",
            "description": "Supporting cast should delineate protagonist's complexity, not overshadow it",
            "check": "Protagonist depth score >= all supporting characters"
        },
        "fatal_flaw_depth": {
            "title": "Flaw = Mistaken Belief",
            "description": "Deep flaws are driven by mistaken beliefs (must control everything or will fail) not observations (impatient)",
            "examples": [
                "Shallow: 'Impatient' (observable behavior)",
                "Deep: 'Must control everything or will fail' (psychological conflict)"
            ]
        },
        "pacing_rule": {
            "title": "3 consecutive chapters at same tension = pacing failure",
            "description": "Tension should vary across chapters to maintain momentum",
            "check": "No 3+ chapter flatlines"
        },
        "save_the_cat_beats": {
            "title": "Save the Cat! 15-Beat Structure",
            "description": "Specific percentage targets for story beats",
            "beats": {
                "Catalyst": "10%",
                "Break Into 2": "20%",
                "Midpoint": "50%",
                "All Is Lost": "75%",
                "Break Into 3": "80%"
            }
        }
    }
```

**Success Criteria**:
- ✅ get_craft_principles returns hardcoded principles
- ✅ query_craft_knowledge guides users to skill system
- ✅ (Optional) Full NotebookLM integration if time permits

---

### Task 6-05: MCP Server Runner & Configuration ⭐ CRITICAL

**Files**:
- `factory/mcp/run_mcp_server.py` (NEW)
- `factory/mcp/README.md` (NEW)
- `.claude/mcp.json` (NEW - for Claude Code integration)

**Requirements**:

**1. Server Runner Script**

Create `factory/mcp/run_mcp_server.py`:
```python
#!/usr/bin/env python3
"""
MCP Server runner for Writers Factory.

Starts the MCP server that exposes Writers Factory capabilities
to external tools (Claude Code, Cursor AI, VS Code extensions).

Usage:
    python factory/mcp/run_mcp_server.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from factory.mcp.server import WritersFactoryMCP

def main():
    print("=" * 70, file=sys.stderr)
    print("🚀 Writers Factory MCP Server", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print("", file=sys.stderr)
    print("MCP server starting...", file=sys.stderr)
    print("Connecting to Writers Factory at http://localhost:8000", file=sys.stderr)
    print("", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    print("  - get_manuscript_structure", file=sys.stderr)
    print("  - get_scene_content", file=sys.stderr)
    print("  - search_scenes", file=sys.stderr)
    print("  - get_characters", file=sys.stderr)
    print("  - analyze_character", file=sys.stderr)
    print("  - check_character_contradictions", file=sys.stderr)
    print("  - get_craft_principles", file=sys.stderr)
    print("", file=sys.stderr)
    print("Server ready for MCP connections", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # Start server
    server = WritersFactoryMCP()
    asyncio.run(server.start())

if __name__ == "__main__":
    main()
```

**2. Claude Code MCP Configuration**

Create `.claude/mcp.json`:
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
    }
  }
}
```

**3. README Documentation**

Create `factory/mcp/README.md`:
```markdown
# Writers Factory MCP Server

MCP (Model Context Protocol) server that exposes Writers Factory capabilities to external tools.

## What is MCP?

MCP is Anthropic's protocol for AI-to-tool communication. It allows external tools (Claude Code, Cursor AI, VS Code extensions) to query your Writers Factory data and run analysis tools.

## Setup

### 1. Install dependencies

```bash
pip install mcp httpx
```

### 2. Start Writers Factory backend

```bash
cd webapp/backend
python simple_app.py
```

Backend should be running at http://localhost:8000

### 3. Configure Claude Code

Add to `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "writers-factory": {
      "command": "python",
      "args": ["factory/mcp/run_mcp_server.py"],
      "cwd": "/Users/gch2024/writers-factory-core"
    }
  }
}
```

### 4. Start MCP server

```bash
python factory/mcp/run_mcp_server.py
```

Or let Claude Code start it automatically (recommended).

## Available Tools

### Manuscript Queries
- `get_manuscript_structure` - Get acts, chapters, scenes
- `get_scene_content(scene_id)` - Get full scene text
- `search_scenes(query)` - Search scenes by keyword
- `get_characters()` - List all characters
- `get_character_scenes(character_name)` - Scenes with character

### Character Analysis
- `analyze_character(character_id)` - Full depth analysis
- `check_character_contradictions(name)` - Check contradiction levels
- `suggest_character_improvements(name)` - Get recommendations

### Knowledge Base
- `get_craft_principles()` - Core writing principles
- `query_craft_knowledge(question)` - Ask craft questions (via skill)

## Usage in Claude Code

Once configured, Claude Code can call these tools automatically:

```
User: "Analyze Mickey Bardot's character depth"
Claude Code: *calls check_character_contradictions("Mickey Bardot")*
Claude Code: "Mickey has a depth score of 85/100..."
```

## Architecture

```
┌─────────────────────────────────────┐
│ External Tools                       │
│ - Claude Code                        │
│ - Cursor AI                          │
│ - VS Code Extensions                 │
└────────────┬────────────────────────┘
             │ MCP Protocol (JSON-RPC)
┌────────────▼────────────────────────┐
│ Writers Factory MCP Server           │
│ (factory/mcp/server.py)              │
└────────────┬────────────────────────┘
             │ HTTP API
┌────────────▼────────────────────────┐
│ Writers Factory Backend              │
│ (webapp/backend/simple_app.py)       │
└─────────────────────────────────────┘
             │
┌────────────▼────────────────────────┐
│ AI Agents & Analysis                 │
│ (factory/agents/)                    │
└─────────────────────────────────────┘
```

## Troubleshooting

**MCP server not starting**:
- Check backend is running at localhost:8000
- Check Python dependencies installed (`pip install mcp httpx`)
- Check PYTHONPATH includes project root

**Tools not showing in Claude Code**:
- Restart Claude Code after changing `.claude/mcp.json`
- Check MCP server output for errors
- Verify `.claude/mcp.json` syntax

**Backend connection errors**:
- Ensure Writers Factory backend is running first
- Check http://localhost:8000/api/health
- Check firewall settings

## Development

To add new tools:

1. Add function to `factory/mcp/server.py`
2. Decorate with `@self.server.tool()`
3. Restart MCP server
4. Test in Claude Code

Example:
```python
@self.server.tool()
async def my_new_tool(arg: str) -> dict:
    """Tool description."""
    response = await self.client.get(f"{self.backend_url}/api/...")
    return response.json()
```
```

**Success Criteria**:
- ✅ `run_mcp_server.py` starts without errors
- ✅ `.claude/mcp.json` properly configured
- ✅ README explains setup and usage
- ✅ Claude Code can discover and call MCP tools
- ✅ Tools work when backend is running

---

## 🧪 Testing Checklist

After completing all tasks, test:

### Basic MCP Functionality
1. ✅ Start Writers Factory backend (`python webapp/backend/simple_app.py`)
2. ✅ Start MCP server (`python factory/mcp/run_mcp_server.py`)
3. ✅ Restart Claude Code
4. ✅ In Claude Code, ask: "What tools are available via MCP?"
5. ✅ Should see: writers-factory tools listed

### Manuscript Query Tools
6. ✅ Ask: "What's the structure of my manuscript?"
7. ✅ Should call `get_manuscript_structure` and show acts/chapters
8. ✅ Ask: "Show me scene X"
9. ✅ Should call `get_scene_content` with scene ID
10. ✅ Ask: "Search for scenes with 'quantum'"
11. ✅ Should call `search_scenes` and show results

### Character Analysis Tools
12. ✅ Ask: "Analyze Mickey Bardot's character"
13. ✅ Should call `check_character_contradictions`
14. ✅ Should show depth score and flags
15. ✅ Ask: "How can I improve Mickey's character?"
16. ✅ Should call `suggest_character_improvements`
17. ✅ Should show recommendations with examples

### Knowledge Base Tools
18. ✅ Ask: "What are the key writing craft principles?"
19. ✅ Should call `get_craft_principles`
20. ✅ Should show contradiction principle, protagonist dimensionality, etc.

---

## 📦 Deliverables

### New Files (4):
1. `factory/mcp/server.py` - MCP server implementation
2. `factory/mcp/run_mcp_server.py` - Server runner script
3. `factory/mcp/README.md` - Documentation
4. `.claude/mcp.json` - Claude Code configuration

### Modified Files (1):
1. `requirements.txt` - Add `mcp` and `httpx` dependencies

### Expected Line Count:
- `server.py`: ~400-500 lines (tools + error handling)
- `run_mcp_server.py`: ~50 lines
- `README.md`: ~200 lines
- `.claude/mcp.json`: ~10 lines

**Total new code**: ~660-760 lines

---

## 💡 Implementation Tips

### Tip 1: Start with Task 6-01 (Server Setup)
Get the basic server running first, even with no tools. This ensures your dependencies and setup are correct.

### Tip 2: Test incrementally
After adding each tool in Task 6-02, restart the server and test that specific tool. Don't wait until all tools are done.

### Tip 3: Use stderr for logging
MCP uses stdout for JSON-RPC communication. All debug prints must go to stderr:
```python
print("Debug message", file=sys.stderr)
```

### Tip 4: Error handling is critical
Every tool should handle errors gracefully:
```python
@self.server.tool()
async def my_tool(arg: str) -> dict:
    try:
        response = await self.client.get(...)
        return response.json()
    except httpx.HTTPError as e:
        return {"error": f"API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

### Tip 5: Test backend endpoints first
Before implementing MCP tools, verify all backend endpoints work via curl:
```bash
curl http://localhost:8000/api/manuscript/tree
curl http://localhost:8000/api/manuscript/explants-v1/characters
curl -X POST http://localhost:8000/api/character/<id>/analyze
```

---

## 🎯 Success Criteria

Sprint 6 is complete when:

1. ✅ MCP server starts without errors
2. ✅ All 10 tools registered and callable
3. ✅ Claude Code can discover tools via `.claude/mcp.json`
4. ✅ Tools return proper responses when backend is running
5. ✅ Error handling works (graceful failures if backend down)
6. ✅ README documents setup and usage
7. ✅ Testing checklist passes

---

## 📝 Handoff Notes

**For Cloud Agent**:

This is the **final sprint**! 🎉

You've delivered 5 consecutive A+ sprints. Sprint 6 adds MCP as an optional interface layer - it doesn't replace anything, just adds external tool access.

**Key Points**:
1. MCP server is a **separate process** from the web app
2. It **calls Writers Factory's existing API** (localhost:8000)
3. It **runs in the background** when Claude Code needs it
4. Users don't see it - it's infrastructure

**Architecture**:
```
Claude Code → MCP Protocol → MCP Server → Writers Factory API → Backend
```

**Don't overthink it**:
- MCP server is just a wrapper around your existing API
- Tools are simple: call backend endpoint, return JSON
- Focus on error handling (backend might not be running)

**Testing**:
- Start backend first: `python webapp/backend/simple_app.py`
- Then start MCP: `python factory/mcp/run_mcp_server.py`
- Then test in Claude Code

You got this! Let's finish strong! 🚀

---

**Document Created**: November 14, 2025
**Sprint**: 6 of 6
**Estimated Effort**: 2-3 days
**Status**: Ready to start
