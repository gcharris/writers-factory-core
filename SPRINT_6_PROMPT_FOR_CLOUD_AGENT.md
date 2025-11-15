# 🎉 Sprint 5 Complete - Starting Sprint 6 (FINAL!)

**Copy this entire message to Cloud Agent:**

---

## 🌟 Sprint 5 Review: A+ (100/100) - APPROVED!

Incredible work, Cloud Agent! Claude Code reviewed your Sprint 5 and found:

✅ **All 5 Character Panel tasks delivered perfectly**
- Sophisticated character analysis algorithms (5 checks, 10 opposition pairs)
- Professional Character data model (True Character vs Characterization)
- Beautiful UI with visual feedback (red/yellow/green depth scores)
- Zero bugs, flawless integration
- Build: 109.11kB gzipped in 1.32s (excellent metrics)

**This is your 5th consecutive A+ sprint!** 🌟🌟🌟🌟🌟

Full review: `/Users/gch2024/writers-factory-core/CLOUD_AGENT_SPRINT_5_REVIEW.md`

---

## 🚀 Sprint 6 (FINAL): MCP Server Implementation

### Mission

Build the **MCP (Model Context Protocol) Server** that exposes Writers Factory to external tools like Claude Code.

**Timeline**: 2-3 days
**Priority**: HIGH
**This is the final sprint!** After this, Writers Factory is 100% complete! 🎉

---

## 📋 What is MCP?

**MCP** = Model Context Protocol (by Anthropic)

**Purpose**: Allows external AI tools (Claude Code, Cursor AI, VS Code extensions) to query your Writers Factory data and run analysis tools.

**Key Point**: MCP is an **optional interface layer** that sits on top of your existing backend. It doesn't replace anything - just adds external access.

**Architecture**:
```
External Tool (Claude Code)
    ↓ (MCP Protocol - JSON-RPC over stdio)
MCP Server (factory/mcp/server.py)
    ↓ (HTTP API calls to localhost:8000)
Writers Factory Backend (webapp/backend/simple_app.py)
    ↓
AI Agents & Analysis (factory/agents/)
```

**Example Use Case**:
- User asks Claude Code: "Analyze Mickey Bardot's character"
- Claude Code calls MCP tool: `check_character_contradictions("Mickey Bardot")`
- MCP server calls: `POST http://localhost:8000/api/character/{id}/analyze`
- Returns: Depth score, flags, recommendations
- Claude Code shows results to user

---

## ✅ Your Tasks (5 total)

Full details: `/Users/gch2024/writers-factory-core/CLOUD_AGENT_SPRINT_6_TASKS.md`

### Task 6-01: MCP Server Setup ⭐ CRITICAL

**File**: `factory/mcp/server.py` (NEW, ~150 lines for setup)

**What to do**:
1. Create MCP server using `mcp` SDK from Anthropic
2. Initialize HTTP client (httpx) for calling Writers Factory API
3. Set up tool/resource registration
4. Add error handling

**Key code structure**:
```python
from mcp import Server
import httpx

class WritersFactoryMCP:
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self.backend_url = backend_url
        self.server = Server("writers-factory")
        self.client = httpx.AsyncClient()

        self.register_tools()  # Add in Task 6-02/6-03/6-04

    async def start(self):
        await self.server.run()

if __name__ == "__main__":
    import asyncio
    server = WritersFactoryMCP()
    asyncio.run(server.start())
```

**Dependencies to add to requirements.txt**:
```
mcp>=0.1.0
httpx>=0.24.0
```

**Success**: Server starts without errors

---

### Task 6-02: Manuscript Query Tools ⭐ HIGH

**File**: `factory/mcp/server.py` (ADD ~250 lines)

**What to do**: Add 5 MCP tools for querying manuscript data

**Tools to implement**:

1. **`get_manuscript_structure()`** - Get acts/chapters/scenes tree
2. **`get_scene_content(scene_id: str)`** - Get full scene text
3. **`search_scenes(query: str)`** - Search scenes by keyword
4. **`get_characters()`** - List all characters
5. **`get_character_scenes(character_name: str)`** - Scenes with character

**Example tool**:
```python
@self.server.tool()
async def get_scene_content(scene_id: str) -> dict:
    """Get full content of a specific scene.

    Args:
        scene_id: Scene UUID

    Returns:
        Scene with id, title, content, word_count
    """
    try:
        response = await self.client.get(
            f"{self.backend_url}/api/manuscript/explants-v1/scenes/{scene_id}"
        )
        response.raise_for_status()
        data = response.json()
        return {
            "id": data["id"],
            "title": data["title"],
            "content": data["content"],
            "word_count": data["word_count"]
        }
    except httpx.HTTPError as e:
        return {"error": f"Failed to fetch scene: {str(e)}"}
```

**Success**: All 5 tools callable and return data

---

### Task 6-03: Character Analysis Tools ⭐ HIGH

**File**: `factory/mcp/server.py` (ADD ~150 lines)

**What to do**: Add 3 MCP tools for character analysis (using Sprint 5's analyzer)

**Tools to implement**:

1. **`analyze_character(character_id: str)`** - Full depth analysis (calls Sprint 5's endpoint)
2. **`check_character_contradictions(character_name: str)`** - Check contradiction levels
3. **`suggest_character_improvements(character_name: str)`** - Get recommendations

**Example tool**:
```python
@self.server.tool()
async def check_character_contradictions(character_name: str) -> dict:
    """Check if character has sufficient contradictions.

    Args:
        character_name: Character name (e.g., "Mickey Bardot")

    Returns:
        Contradiction analysis with depth score and flags
    """
    try:
        # Get character by name
        chars_resp = await self.client.get(
            f"{self.backend_url}/api/manuscript/explants-v1/characters"
        )
        chars = chars_resp.json()["characters"]

        char = next((c for c in chars if c["name"].lower() == character_name.lower()), None)
        if not char:
            return {"error": f"Character '{character_name}' not found"}

        # Analyze
        analysis_resp = await self.client.post(
            f"{self.backend_url}/api/character/{char['id']}/analyze"
        )
        analysis = analysis_resp.json()

        # Filter to contradiction flags
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
    except Exception as e:
        return {"error": str(e)}
```

**Success**: All 3 character tools return analysis

---

### Task 6-04: Knowledge Base Integration ⭐ MEDIUM

**File**: `factory/mcp/server.py` (ADD ~80 lines)

**What to do**: Add 2 MCP tools for writing craft knowledge

**Tools to implement**:

1. **`get_craft_principles()`** - Return hardcoded craft principles
2. **`query_craft_knowledge(question: str)`** - Guide users to notebooklm skill

**Example tool**:
```python
@self.server.tool()
async def get_craft_principles() -> dict:
    """Get core writing craft principles.

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
            "description": "Deep flaws are driven by mistaken beliefs, not observations",
            "examples": [
                "Shallow: 'Impatient' (observable)",
                "Deep: 'Must control everything or will fail' (psychological conflict)"
            ]
        },
        "pacing_rule": {
            "title": "3 consecutive chapters at same tension = failure",
            "description": "Tension should vary to maintain momentum"
        },
        "save_the_cat_beats": {
            "title": "Save the Cat! 15-Beat Structure",
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

**Success**: get_craft_principles returns principles

---

### Task 6-05: Server Runner & Configuration ⭐ CRITICAL

**Files to create**:
1. `factory/mcp/run_mcp_server.py` (NEW, ~50 lines)
2. `factory/mcp/README.md` (NEW, ~200 lines)
3. `.claude/mcp.json` (NEW, ~10 lines)

**What to do**:

**1. Create server runner** (`factory/mcp/run_mcp_server.py`):
```python
#!/usr/bin/env python3
"""MCP Server runner for Writers Factory."""

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
    print("Server starting...", file=sys.stderr)
    print("Connecting to http://localhost:8000", file=sys.stderr)
    print("", file=sys.stderr)
    print("Available tools: 10 tools", file=sys.stderr)
    print("  - Manuscript: get_structure, get_scene, search_scenes", file=sys.stderr)
    print("  - Characters: get_characters, get_character_scenes", file=sys.stderr)
    print("  - Analysis: analyze_character, check_contradictions, suggest_improvements", file=sys.stderr)
    print("  - Knowledge: get_craft_principles, query_craft_knowledge", file=sys.stderr)
    print("", file=sys.stderr)
    print("Ready for MCP connections", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    server = WritersFactoryMCP()
    asyncio.run(server.start())

if __name__ == "__main__":
    main()
```

**2. Create Claude Code config** (`.claude/mcp.json`):
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

**3. Create README** (`factory/mcp/README.md`):
- Explain what MCP is
- Setup instructions (install dependencies, configure Claude Code)
- Usage examples
- Troubleshooting tips
- Full template in CLOUD_AGENT_SPRINT_6_TASKS.md

**Success**:
- Server starts with run_mcp_server.py
- Claude Code discovers tools via .claude/mcp.json
- README explains setup

---

## 🧪 Testing Instructions

After completing all tasks:

### 1. Test Backend First
```bash
cd /Users/gch2024/writers-factory-core
python webapp/backend/simple_app.py
```

Visit http://localhost:8000/api/health (should return OK)

### 2. Test MCP Server
```bash
# In new terminal
python factory/mcp/run_mcp_server.py
```

Should print startup banner (to stderr)

### 3. Test in Claude Code
1. Restart Claude Code (to load .claude/mcp.json)
2. Ask: "What MCP tools are available?"
3. Should list writers-factory tools
4. Ask: "What's my manuscript structure?"
5. Should call get_manuscript_structure and show results

### 4. Test Character Analysis
1. Ask: "Analyze Mickey Bardot's character"
2. Should call check_character_contradictions
3. Should show depth score and flags

### 5. Test Knowledge Base
1. Ask: "What are the key craft principles?"
2. Should call get_craft_principles
3. Should show contradiction principle, protagonist dimensionality, etc.

---

## ⚠️ Important Implementation Notes

### 1. Logging to stderr
MCP uses stdout for JSON-RPC. All debug logs MUST use stderr:
```python
print("Debug message", file=sys.stderr)
```

### 2. Error Handling
Every tool should catch exceptions:
```python
try:
    response = await self.client.get(...)
    return response.json()
except httpx.HTTPError as e:
    return {"error": f"API error: {str(e)}"}
except Exception as e:
    return {"error": f"Unexpected error: {str(e)}"}
```

### 3. Test Incrementally
- Add one tool
- Restart server
- Test that tool
- Repeat

Don't add all tools then test - harder to debug!

### 4. Backend Must Be Running
MCP server calls localhost:8000. If backend isn't running, tools will error (which is fine - just handle gracefully).

---

## 🎯 Success Criteria

Sprint 6 is complete when:

1. ✅ MCP server starts without errors
2. ✅ All 10 tools implemented and registered
3. ✅ `.claude/mcp.json` properly configured
4. ✅ Claude Code can discover and call tools
5. ✅ Tools return proper responses when backend running
6. ✅ Error handling works (graceful failures if backend down)
7. ✅ README documents setup and usage
8. ✅ Testing checklist passes

---

## 📦 Expected Deliverables

### New Files (4):
1. `factory/mcp/server.py` (~630 lines with all tools)
2. `factory/mcp/run_mcp_server.py` (~50 lines)
3. `factory/mcp/README.md` (~200 lines)
4. `.claude/mcp.json` (~10 lines)

### Modified Files (1):
1. `requirements.txt` (add mcp and httpx)

**Total new code**: ~890 lines

---

## 💡 Tips for Success

### Start Simple
Get Task 6-01 (server setup) working first with zero tools. Then add tools incrementally.

### Use the Template
CLOUD_AGENT_SPRINT_6_TASKS.md has complete code templates for every tool. Use them!

### Test Backend First
Before writing MCP tools, verify backend endpoints work:
```bash
curl http://localhost:8000/api/manuscript/tree
curl http://localhost:8000/api/manuscript/explants-v1/characters
```

### Focus on Error Handling
MCP tools should never crash. Always return `{"error": "..."}` on failure.

---

## 🚀 You Got This!

You've delivered **5 consecutive A+ sprints**. This is the **FINAL sprint**!

After Sprint 6, Writers Factory will be **100% complete**:
- ✅ Web UI (React app)
- ✅ Backend API (FastAPI)
- ✅ AI agents (23 models)
- ✅ Ollama integration (free local models)
- ✅ Cost tracking (economy mode)
- ✅ Brainstorm landing (creation wizard)
- ✅ Character analysis (contradiction detection)
- ✅ **MCP server (external tool access)** ← Sprint 6

Let's finish strong and ship this thing! 🎉✨

---

**Full Task Details**: `/Users/gch2024/writers-factory-core/CLOUD_AGENT_SPRINT_6_TASKS.md`

**Sprint 5 Review**: `/Users/gch2024/writers-factory-core/CLOUD_AGENT_SPRINT_5_REVIEW.md`

**Ready to start? Let's go!** 🚀
