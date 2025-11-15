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
    """Main entry point for MCP server."""
    print("=" * 70, file=sys.stderr)
    print("🚀 Writers Factory MCP Server", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print("", file=sys.stderr)
    print("MCP server starting...", file=sys.stderr)
    print("Connecting to Writers Factory at http://localhost:8000", file=sys.stderr)
    print("", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    print("", file=sys.stderr)
    print("  Manuscript Queries:", file=sys.stderr)
    print("    - get_manuscript_structure", file=sys.stderr)
    print("    - get_scene_content", file=sys.stderr)
    print("    - search_scenes", file=sys.stderr)
    print("    - get_characters", file=sys.stderr)
    print("    - get_character_scenes", file=sys.stderr)
    print("", file=sys.stderr)
    print("  Character Analysis:", file=sys.stderr)
    print("    - analyze_character", file=sys.stderr)
    print("    - check_character_contradictions", file=sys.stderr)
    print("    - suggest_character_improvements", file=sys.stderr)
    print("", file=sys.stderr)
    print("  Knowledge Base:", file=sys.stderr)
    print("    - query_craft_knowledge", file=sys.stderr)
    print("    - get_craft_principles", file=sys.stderr)
    print("", file=sys.stderr)
    print("Server ready for MCP connections", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print("", file=sys.stderr)

    # Start server
    server = WritersFactoryMCP()
    asyncio.run(server.start())


if __name__ == "__main__":
    main()
