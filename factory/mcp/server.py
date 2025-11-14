"""Writers Factory MCP Server.

Exposes Writers Factory capabilities via Model Context Protocol (MCP).

This server allows external tools (Claude Code, Cursor AI, VS Code extensions)
to query manuscript data, analyze characters, and access craft knowledge.

Architecture:
    External Tool → MCP Protocol → This Server → Writers Factory API → Backend
"""

from mcp import Server
import httpx
import sys
from typing import Dict, List, Any, Optional


class WritersFactoryMCP:
    """MCP server for Writers Factory."""

    def __init__(self, backend_url: str = "http://localhost:8000"):
        """Initialize Writers Factory MCP server.

        Args:
            backend_url: URL of Writers Factory backend API
        """
        self.backend_url = backend_url
        self.server = Server("writers-factory")
        self.client = httpx.AsyncClient()

        # Log initialization (stderr only - stdout reserved for JSON-RPC)
        print(f"[MCP] Initializing Writers Factory MCP server", file=sys.stderr)
        print(f"[MCP] Backend URL: {backend_url}", file=sys.stderr)

        # Register tools and resources
        self.register_tools()
        self.register_resources()

    def register_tools(self):
        """Register MCP tools.

        Tools will be added incrementally across tasks:
        - Task 6-02: Manuscript query tools (5 tools)
        - Task 6-03: Character analysis tools (3 tools)
        - Task 6-04: Knowledge base tools (2 tools)
        """
        print("[MCP] Registering tools...", file=sys.stderr)

        # Task 6-02: Manuscript Query Tools
        @self.server.tool()
        async def get_manuscript_structure() -> dict:
            """Get complete manuscript structure (acts, chapters, scenes)."""
            try:
                response = await self.client.get(f"{self.backend_url}/api/manuscript/tree")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"[MCP] Error in get_manuscript_structure: {e}", file=sys.stderr)
                return {"error": f"API error: {str(e)}"}
            except Exception as e:
                print(f"[MCP] Unexpected error in get_manuscript_structure: {e}", file=sys.stderr)
                return {"error": f"Unexpected error: {str(e)}"}

        @self.server.tool()
        async def get_scene_content(scene_id: str) -> dict:
            """Get full content of a specific scene.

            Args:
                scene_id: Scene UUID

            Returns:
                Scene data with id, title, content, word_count
            """
            try:
                response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/explants-v1/scenes/{scene_id}"
                )
                response.raise_for_status()
                data = response.json()
                return {
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "content": data.get("content"),
                    "word_count": data.get("word_count")
                }
            except httpx.HTTPError as e:
                print(f"[MCP] Error in get_scene_content: {e}", file=sys.stderr)
                return {"error": f"API error: {str(e)}"}
            except Exception as e:
                print(f"[MCP] Unexpected error in get_scene_content: {e}", file=sys.stderr)
                return {"error": f"Unexpected error: {str(e)}"}

        @self.server.tool()
        async def search_scenes(query: str) -> list:
            """Search scenes by keyword or phrase.

            Args:
                query: Search term (e.g., "Mickey", "quantum", "confrontation")

            Returns:
                List of matching scenes with titles and excerpts
            """
            try:
                response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/search",
                    params={"q": query}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except httpx.HTTPError as e:
                print(f"[MCP] Error in search_scenes: {e}", file=sys.stderr)
                return [{"error": f"API error: {str(e)}"}]
            except Exception as e:
                print(f"[MCP] Unexpected error in search_scenes: {e}", file=sys.stderr)
                return [{"error": f"Unexpected error: {str(e)}"}]

        @self.server.tool()
        async def get_characters() -> list:
            """Get all characters in the manuscript.

            Returns:
                List of characters with full data
            """
            try:
                response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/explants-v1/characters"
                )
                response.raise_for_status()
                data = response.json()
                return data.get("characters", [])
            except httpx.HTTPError as e:
                print(f"[MCP] Error in get_characters: {e}", file=sys.stderr)
                return [{"error": f"API error: {str(e)}"}]
            except Exception as e:
                print(f"[MCP] Unexpected error in get_characters: {e}", file=sys.stderr)
                return [{"error": f"Unexpected error: {str(e)}"}]

        @self.server.tool()
        async def get_character_scenes(character_name: str) -> dict:
            """Get all scenes featuring a specific character.

            Args:
                character_name: Character name (e.g., "Mickey Bardot")

            Returns:
                List of scenes with this character, or error if character not found
            """
            try:
                # First get all characters to find ID
                chars_response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/explants-v1/characters"
                )
                chars_response.raise_for_status()
                chars_data = chars_response.json()
                chars = chars_data.get("characters", [])

                # Find character by name (case-insensitive)
                char = next(
                    (c for c in chars if c.get("name", "").lower() == character_name.lower()),
                    None
                )

                if not char:
                    return {"error": f"Character '{character_name}' not found"}

                # Return scenes from character's scene_appearances field
                return {
                    "character_name": char.get("name"),
                    "character_id": char.get("id"),
                    "scenes": char.get("scene_appearances", [])
                }
            except httpx.HTTPError as e:
                print(f"[MCP] Error in get_character_scenes: {e}", file=sys.stderr)
                return {"error": f"API error: {str(e)}"}
            except Exception as e:
                print(f"[MCP] Unexpected error in get_character_scenes: {e}", file=sys.stderr)
                return {"error": f"Unexpected error: {str(e)}"}

        print("[MCP] Registered 5 manuscript query tools", file=sys.stderr)

        # Task 6-03: Character Analysis Tools
        @self.server.tool()
        async def analyze_character(character_id: str) -> dict:
            """Analyze character dimensional depth (from Sprint 5).

            Args:
                character_id: Character UUID

            Returns:
                Analysis with depth_score, flags, recommendations
            """
            try:
                response = await self.client.post(
                    f"{self.backend_url}/api/character/{character_id}/analyze"
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"[MCP] Error in analyze_character: {e}", file=sys.stderr)
                return {"error": f"API error: {str(e)}"}
            except Exception as e:
                print(f"[MCP] Unexpected error in analyze_character: {e}", file=sys.stderr)
                return {"error": f"Unexpected error: {str(e)}"}

        @self.server.tool()
        async def check_character_contradictions(character_name: str) -> dict:
            """Check if character has sufficient internal/external contradictions.

            Args:
                character_name: Character name

            Returns:
                Contradiction analysis with specific flags
            """
            try:
                # Get character by name
                chars_response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/explants-v1/characters"
                )
                chars_response.raise_for_status()
                chars_data = chars_response.json()
                chars = chars_data.get("characters", [])

                # Find character (case-insensitive)
                char = next(
                    (c for c in chars if c.get("name", "").lower() == character_name.lower()),
                    None
                )

                if not char:
                    return {"error": f"Character '{character_name}' not found"}

                # Analyze character
                analysis_response = await self.client.post(
                    f"{self.backend_url}/api/character/{char['id']}/analyze"
                )
                analysis_response.raise_for_status()
                analysis = analysis_response.json()

                # Filter to just contradiction-related flags
                contradiction_flags = [
                    f for f in analysis.get("flags", [])
                    if "CONTRADICTION" in f.get("type", "")
                ]

                return {
                    "character": char.get("name"),
                    "depth_score": analysis.get("depth_score"),
                    "contradiction_flags": contradiction_flags,
                    "has_contradictions": len(contradiction_flags) == 0
                }
            except httpx.HTTPError as e:
                print(f"[MCP] Error in check_character_contradictions: {e}", file=sys.stderr)
                return {"error": f"API error: {str(e)}"}
            except Exception as e:
                print(f"[MCP] Unexpected error in check_character_contradictions: {e}", file=sys.stderr)
                return {"error": f"Unexpected error: {str(e)}"}

        @self.server.tool()
        async def suggest_character_improvements(character_name: str) -> list:
            """Get actionable recommendations for improving character depth.

            Args:
                character_name: Character name

            Returns:
                List of recommendations with examples
            """
            try:
                # Get character by name
                chars_response = await self.client.get(
                    f"{self.backend_url}/api/manuscript/explants-v1/characters"
                )
                chars_response.raise_for_status()
                chars_data = chars_response.json()
                chars = chars_data.get("characters", [])

                # Find character (case-insensitive)
                char = next(
                    (c for c in chars if c.get("name", "").lower() == character_name.lower()),
                    None
                )

                if not char:
                    return [{"error": f"Character '{character_name}' not found"}]

                # Analyze character
                analysis_response = await self.client.post(
                    f"{self.backend_url}/api/character/{char['id']}/analyze"
                )
                analysis_response.raise_for_status()
                analysis = analysis_response.json()

                # Extract recommendations from flags
                recommendations = []
                for flag in analysis.get("flags", []):
                    recommendations.append({
                        "severity": flag.get("severity"),
                        "issue": flag.get("message"),
                        "suggestion": flag.get("recommendation", ""),
                        "example": flag.get("example", "")
                    })

                # If no flags, character is well-developed
                if not recommendations:
                    recommendations.append({
                        "severity": "INFO",
                        "issue": "Character is well-developed",
                        "suggestion": f"{char.get('name')} has strong dimensional depth (score: {analysis.get('depth_score')}/100)",
                        "example": ""
                    })

                return recommendations
            except httpx.HTTPError as e:
                print(f"[MCP] Error in suggest_character_improvements: {e}", file=sys.stderr)
                return [{"error": f"API error: {str(e)}"}]
            except Exception as e:
                print(f"[MCP] Unexpected error in suggest_character_improvements: {e}", file=sys.stderr)
                return [{"error": f"Unexpected error: {str(e)}"}]

        print("[MCP] Registered 3 character analysis tools", file=sys.stderr)

        # Task 6-04: Knowledge Base Integration
        @self.server.tool()
        async def query_craft_knowledge(question: str) -> str:
            """Query NotebookLM for writing craft advice.

            Args:
                question: Question about writing craft (e.g., "How do I create tension?")

            Returns:
                Guidance on using the NotebookLM skill system
            """
            return (
                f"To query craft knowledge about '{question}', use the 'notebooklm' skill directly in Claude Code:\n\n"
                f"  1. Invoke skill: notebooklm\n"
                f"  2. Ask: '{question}'\n\n"
                f"NotebookLM integration via MCP requires browser automation, "
                f"which is better handled by the skill system.\n\n"
                f"Alternatively, use the 'get_craft_principles' tool to see core principles."
            )

        @self.server.tool()
        async def get_craft_principles() -> dict:
            """Get core writing craft principles from NotebookLM analysis.

            Returns:
                Key principles with explanations and examples
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

        print("[MCP] Registered 2 knowledge base tools", file=sys.stderr)
        print("[MCP] Total tools registered: 10", file=sys.stderr)

    def register_resources(self):
        """Register MCP resources.

        Resources provide access to manuscript data and other static content.
        Will be implemented as needed.
        """
        print("[MCP] Resource registration - pending task implementation", file=sys.stderr)
        pass

    async def start(self):
        """Start MCP server.

        Server listens on stdio for MCP protocol messages (JSON-RPC).
        All logging must go to stderr to avoid interfering with JSON-RPC.
        """
        print("[MCP] Starting server...", file=sys.stderr)
        print("[MCP] Listening on stdio for MCP protocol messages", file=sys.stderr)
        print("[MCP] Ready for connections", file=sys.stderr)

        try:
            await self.server.run()
        except Exception as e:
            print(f"[MCP] Server error: {e}", file=sys.stderr)
            raise

    async def shutdown(self):
        """Shutdown MCP server and cleanup resources."""
        print("[MCP] Shutting down...", file=sys.stderr)
        await self.client.aclose()
        print("[MCP] Shutdown complete", file=sys.stderr)


if __name__ == "__main__":
    import asyncio

    # Start server
    server = WritersFactoryMCP()

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n[MCP] Received interrupt signal", file=sys.stderr)
    except Exception as e:
        print(f"[MCP] Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
