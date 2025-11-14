# Writers Factory MCP Server

MCP (Model Context Protocol) server that exposes Writers Factory capabilities to external tools.

## What is MCP?

MCP is Anthropic's protocol for AI-to-tool communication. It allows external tools (Claude Code, Cursor AI, VS Code extensions) to query your Writers Factory data and run analysis tools.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

This will install the required dependencies:
- `mcp>=0.1.0` - Anthropic's MCP SDK
- `httpx>=0.26.0` - For async HTTP requests

### 2. Start Writers Factory backend

```bash
cd webapp/backend
python simple_app.py
```

Backend should be running at http://localhost:8000

### 3. Configure Claude Code

The `.claude/mcp.json` file is already configured in the project root. If you need to update it:

```json
{
  "mcpServers": {
    "writers-factory": {
      "command": "python",
      "args": ["factory/mcp/run_mcp_server.py"],
      "cwd": "/home/user/writers-factory-core",
      "env": {
        "PYTHONPATH": "/home/user/writers-factory-core"
      }
    }
  }
}
```

**Note**: Update the `cwd` path to match your project location.

### 4. Start MCP server

```bash
python factory/mcp/run_mcp_server.py
```

Or let Claude Code start it automatically (recommended).

## Available Tools

### Manuscript Queries

- **`get_manuscript_structure`** - Get acts, chapters, scenes structure
- **`get_scene_content(scene_id)`** - Get full scene text with metadata
- **`search_scenes(query)`** - Search scenes by keyword
- **`get_characters()`** - List all characters with full data
- **`get_character_scenes(character_name)`** - Get scenes featuring a specific character

### Character Analysis

- **`analyze_character(character_id)`** - Full dimensional depth analysis (Sprint 5)
- **`check_character_contradictions(name)`** - Check contradiction levels
- **`suggest_character_improvements(name)`** - Get actionable recommendations

### Knowledge Base

- **`get_craft_principles()`** - Core writing principles from NotebookLM analysis
- **`query_craft_knowledge(question)`** - Ask craft questions (via skill system)

## Usage in Claude Code

Once configured, Claude Code can call these tools automatically:

```
User: "Analyze Mickey Bardot's character depth"
Claude Code: *calls check_character_contradictions("Mickey Bardot")*
Claude Code: "Mickey has a depth score of 85/100..."
```

Example queries:
- "What's the structure of my manuscript?"
- "Show me all scenes with quantum physics"
- "Analyze the protagonist's character depth"
- "What are the key writing craft principles?"
- "How can I improve character X?"

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

### MCP server not starting

**Issue**: Server fails to start or shows import errors

**Solutions**:
- Check backend is running at localhost:8000
- Check Python dependencies installed: `pip install -r requirements.txt`
- Check PYTHONPATH includes project root
- Verify Python version (3.9+ required)

### Tools not showing in Claude Code

**Issue**: Claude Code doesn't discover MCP tools

**Solutions**:
- Restart Claude Code after changing `.claude/mcp.json`
- Check MCP server output for errors (logged to stderr)
- Verify `.claude/mcp.json` syntax is valid JSON
- Check that `cwd` path in `mcp.json` matches your project location

### Backend connection errors

**Issue**: Tools return "API error" or connection refused

**Solutions**:
- Ensure Writers Factory backend is running first: `python webapp/backend/simple_app.py`
- Check http://localhost:8000/api/health in your browser
- Verify no firewall blocking localhost:8000
- Check backend logs for errors

### Character not found errors

**Issue**: Character analysis tools return "Character not found"

**Solutions**:
- Verify character exists in manuscript
- Check character name spelling (case-insensitive matching is supported)
- Use `get_characters()` tool to see all available characters

## Development

### Adding New Tools

To add new tools to the MCP server:

1. Add function to `factory/mcp/server.py` in the `register_tools()` method
2. Decorate with `@self.server.tool()`
3. Add proper error handling (HTTP errors and exceptions)
4. Restart MCP server
5. Test in Claude Code

Example:
```python
@self.server.tool()
async def my_new_tool(arg: str) -> dict:
    """Tool description shown to Claude Code."""
    try:
        response = await self.client.get(f"{self.backend_url}/api/...")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"[MCP] Error in my_new_tool: {e}", file=sys.stderr)
        return {"error": f"API error: {str(e)}"}
    except Exception as e:
        print(f"[MCP] Unexpected error in my_new_tool: {e}", file=sys.stderr)
        return {"error": f"Unexpected error: {str(e)}"}
```

### Important Development Notes

- **Logging**: Use `print(..., file=sys.stderr)` for all logging. stdout is reserved for MCP JSON-RPC communication.
- **Error Handling**: Every tool must handle `httpx.HTTPError` and generic exceptions gracefully.
- **Type Hints**: Include type hints for parameters and return values - they help Claude Code understand the tool.
- **Docstrings**: Write clear docstrings - Claude Code uses them to understand when to use each tool.

### Testing Tools Manually

You can test backend endpoints with curl before implementing MCP tools:

```bash
# Test manuscript structure
curl http://localhost:8000/api/manuscript/tree

# Test characters
curl http://localhost:8000/api/manuscript/explants-v1/characters

# Test character analysis (replace <id> with actual UUID)
curl -X POST http://localhost:8000/api/character/<id>/analyze

# Test scene search
curl "http://localhost:8000/api/manuscript/search?q=quantum"
```

## Sprint 6 Overview

This MCP server was built in **Sprint 6**, the final sprint of Writers Factory development.

**Key Features**:
- 10 MCP tools across 3 categories
- Full integration with Sprint 5's character analyzer
- Hardcoded craft principles from NotebookLM analysis
- Comprehensive error handling
- Clean architecture (MCP server → Backend API → AI Agents)

**Sprint Timeline**:
- Task 6-01: MCP Server Setup
- Task 6-02: Manuscript Query Tools (5 tools)
- Task 6-03: Character Analysis Tools (3 tools)
- Task 6-04: Knowledge Base Integration (2 tools)
- Task 6-05: Server Runner & Configuration

## Additional Resources

- **MCP Specification**: https://modelcontextprotocol.io/
- **Python MCP SDK**: https://github.com/anthropics/python-mcp-sdk
- **Writers Factory Documentation**: See project README
- **Character Analyzer**: See `factory/agents/character_analyzer.py` for analysis logic

## License

Part of Writers Factory - Multi-model AI writing system.
