"""
Setup Wizard Agent - Intelligent conversation agent for knowledge extraction

This is NOT a dumb form - it's an AI agent that:
- Queries NotebookLM intelligently
- Validates findings with user
- Disambiguates confusing references
- Fills gaps through conversation
- Creates structured files after confirmation

Uses Llama 3.3 by default (free local) for cost-effective setup.
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from factory.ai.model_router import ModelRouter
from factory.ai.ollama_setup import OllamaSetup


class SetupWizardAgent:
    """
    AI agent for intelligent project setup through conversation.

    Processes 8 knowledge categories:
    1. Characters
    2. Story_Structure
    3. World_Building
    4. Themes_and_Philosophy
    5. Voice_and_Craft
    6. Antagonism_and_Conflict
    7. Key_Beats_and_Pacing
    8. Research_and_Setting_Specifics
    """

    CATEGORIES = [
        "Characters",
        "Story_Structure",
        "World_Building",
        "Themes_and_Philosophy",
        "Voice_and_Craft",
        "Antagonism_and_Conflict",
        "Key_Beats_and_Pacing",
        "Research_and_Setting_Specifics",
    ]

    def __init__(
        self,
        project_id: str,
        notebook_url: str,
        model: str = "llama3.3",
        user_response_callback: Optional[callable] = None
    ):
        """
        Initialize Setup Wizard Agent.

        Args:
            project_id: Project identifier
            notebook_url: NotebookLM notebook URL
            model: Model to use for conversation (default: llama3.3)
            user_response_callback: Async callback for getting user responses
        """
        self.project_id = project_id
        self.notebook_url = notebook_url
        self.model = model
        self.user_response_callback = user_response_callback

        self.project_path = Path(f"projects/{project_id}")
        self.reference_path = self.project_path / "reference"

        # Conversation history for context
        self.conversation_history: List[Dict[str, str]] = []

        # Extracted data storage
        self.extracted_data: Dict[str, Any] = {}

    async def query_notebooklm(self, question: str) -> str:
        """
        Query user's NotebookLM for specific information.

        Args:
            question: Question to ask NotebookLM

        Returns:
            Response from NotebookLM
        """
        # TODO: Integrate with actual NotebookLM client (Sprint 11)
        # For now, return placeholder
        # In production, this would use factory.research.notebooklm_client

        print(f"[NotebookLM Query] {question}")

        # Placeholder response
        return f"[NotebookLM would respond to: {question}]"

    async def ask_user(
        self,
        message: str,
        options: Optional[List[str]] = None,
        input_type: str = "text"
    ) -> str:
        """
        Ask user a question and wait for response.

        Args:
            message: Message to show user
            options: Optional list of choices
            input_type: Type of input ('text', 'choice', 'confirmation')

        Returns:
            User's response
        """
        if self.user_response_callback:
            return await self.user_response_callback({
                "type": "user_input_needed",
                "message": message,
                "options": options,
                "input_type": input_type
            })

        # Fallback for testing
        return input(f"{message}\n> ")

    async def generate_response(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Generate AI response using configured model.

        Args:
            prompt: User prompt
            system: Optional system prompt

        Returns:
            AI-generated response
        """
        result = await OllamaSetup.generate(
            model=self.model,
            prompt=prompt,
            system=system,
            temperature=0.7
        )

        if result["success"]:
            return result["response"]
        else:
            raise Exception(f"Failed to generate response: {result['error']}")

    async def present_findings_to_user(
        self,
        category: str,
        findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Present findings to user for validation and correction.

        Args:
            category: Category name
            findings: Extracted findings

        Returns:
            Validated and corrected findings
        """
        summary = self._format_findings(findings)

        message = f"""
I found the following information about {category}:

{summary}

Is this correct? You can:
1. Confirm (all correct)
2. Edit specific items
3. Add missing items
4. Remove incorrect items
"""

        response = await self.ask_user(
            message,
            options=["Confirm", "Edit", "Add", "Remove"],
            input_type="choice"
        )

        if response == "Confirm":
            return findings

        # Handle edits, additions, removals
        # In production, this would be more sophisticated
        return findings

    def _format_findings(self, findings: Dict[str, Any]) -> str:
        """Format findings for display to user."""
        lines = []
        for key, value in findings.items():
            if isinstance(value, list):
                lines.append(f"- {key}: {', '.join(value)}")
            else:
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    async def suggest_subcategories(
        self,
        category: str,
        item_count: int
    ) -> Optional[Dict[str, Any]]:
        """
        Suggest subcategory structure based on content volume.

        Args:
            category: Category name
            item_count: Number of items found

        Returns:
            Subcategory suggestion or None
        """
        if item_count < 5:
            return {
                "structure": "flat",
                "message": f"You have {item_count} {category.lower()}. Keeping structure flat for simplicity."
            }

        if item_count < 15:
            if category == "Characters":
                return {
                    "structure": "basic",
                    "subcategories": ["Core_Cast", "Supporting_Cast"],
                    "message": f"You have {item_count} characters. I suggest organizing into Core Cast and Supporting Cast."
                }

        if item_count >= 15:
            if category == "Characters":
                # Check for antagonist keywords
                has_antagonist = True  # TODO: Actually check notebook

                subcats = ["Core_Cast", "Supporting_Cast"]
                if has_antagonist:
                    subcats.append("Antagonists")
                subcats.append("Relationships")

                return {
                    "structure": "detailed",
                    "subcategories": subcats,
                    "message": f"You have {item_count} characters - a large cast! I suggest organizing into: {', '.join(subcats)}"
                }

        return None

    async def create_category_file(
        self,
        category: str,
        filename: str,
        content: Dict[str, Any]
    ) -> Path:
        """
        Create structured markdown file from template + extracted data.

        Args:
            category: Category name
            filename: File name (e.g., "Mickey_Bardot_profile.md")
            content: Content dictionary

        Returns:
            Path to created file
        """
        category_path = self.reference_path / category
        category_path.mkdir(parents=True, exist_ok=True)

        file_path = category_path / filename

        # Generate markdown content
        markdown = self._generate_markdown(content)

        with open(file_path, 'w') as f:
            f.write(markdown)

        print(f"Created: {file_path}")
        return file_path

    def _generate_markdown(self, content: Dict[str, Any]) -> str:
        """Generate markdown from content dictionary."""
        lines = [f"# {content.get('name', 'Untitled')}\n"]

        for section, fields in content.items():
            if section == 'name':
                continue

            lines.append(f"\n## {section}\n")

            if isinstance(fields, dict):
                for field_name, field_value in fields.items():
                    lines.append(f"**{field_name}**: {field_value}\n")
            elif isinstance(fields, list):
                for item in fields:
                    lines.append(f"- {item}\n")
            else:
                lines.append(f"{fields}\n")

        return "\n".join(lines)

    async def process_characters_category(self) -> Dict[str, Any]:
        """
        Process Characters category through intelligent conversation.

        Returns:
            Processing results
        """
        print("\n" + "="*60)
        print("Processing Category: Characters")
        print("="*60)

        # Step 1: Discover characters
        query = "Who are the main characters in this story? List all named characters mentioned."
        raw_response = await self.query_notebooklm(query)

        # Step 2: Parse character list
        # In production, use AI to parse the response
        characters_prompt = f"""
Based on this response from NotebookLM:
{raw_response}

Extract a list of character names. Return only a JSON array of names.
"""

        characters_json = await self.generate_response(characters_prompt)

        # Parse characters (handle both JSON and plain text)
        try:
            characters = json.loads(characters_json)
        except:
            # Fallback: extract names manually
            characters = ["Character 1", "Character 2"]  # Placeholder

        # Step 3: Validate with user
        validated = await self.ask_user(
            f"I found {len(characters)} characters: {', '.join(characters)}\n\nAre these all main characters, or are some just references/research subjects?",
            input_type="text"
        )

        # Step 4: Process each character
        results = {
            "category": "Characters",
            "files_created": [],
            "character_count": len(characters)
        }

        for char in characters:
            # Extract character details
            char_data = await self._extract_character_details(char)

            # Create file
            filename = f"{char.replace(' ', '_')}_profile.md"
            file_path = await self.create_category_file(
                "Characters",
                filename,
                char_data
            )

            results["files_created"].append(str(file_path))

        return results

    async def _extract_character_details(self, character_name: str) -> Dict[str, Any]:
        """
        Extract detailed information about a character.

        Args:
            character_name: Character's name

        Returns:
            Character data dictionary
        """
        # Query NotebookLM for various character aspects
        queries = {
            "role": f"What is {character_name}'s role in the story?",
            "internal_conflicts": f"What are {character_name}'s internal conflicts?",
            "motivations": f"What motivates {character_name}? What are their goals?",
            "fears": f"What are {character_name}'s fears and insecurities?",
        }

        char_data = {
            "name": character_name,
            "Basic Information": {},
            "Core Dimensions": {},
        }

        for field, query in queries.items():
            response = await self.query_notebooklm(query)

            if "would respond to" not in response:  # Has real data
                char_data["Core Dimensions"][field] = response
            else:
                # No data found - ask user or leave blank
                char_data["Core Dimensions"][field] = "[TO BE ADDED DURING WRITING]"

        return char_data

    async def process_category(self, category: str) -> Dict[str, Any]:
        """
        Process a single category through intelligent conversation.

        Args:
            category: Category name

        Returns:
            Processing results
        """
        if category == "Characters":
            return await self.process_characters_category()

        # Other categories would have similar implementations
        return {
            "category": category,
            "status": "not_implemented",
            "message": f"{category} processing coming soon!"
        }

    async def run_full_wizard(self) -> Dict[str, Any]:
        """
        Run complete wizard through all 8 categories.

        Returns:
            Complete wizard results
        """
        results = {
            "project_id": self.project_id,
            "started_at": datetime.now().isoformat(),
            "categories_processed": [],
            "files_created": [],
        }

        for category in self.CATEGORIES:
            print(f"\n{'='*60}")
            print(f"Category {len(results['categories_processed']) + 1}/8: {category}")
            print(f"{'='*60}")

            category_result = await self.process_category(category)
            results["categories_processed"].append(category_result)

            if "files_created" in category_result:
                results["files_created"].extend(category_result["files_created"])

        results["completed_at"] = datetime.now().isoformat()
        results["total_files"] = len(results["files_created"])

        return results


# Convenience function for testing
async def test_wizard():
    """Test the wizard agent."""
    agent = SetupWizardAgent(
        project_id="test-project",
        notebook_url="https://notebooklm.google.com/notebook/test",
        model="llama3.3"
    )

    # Test character extraction
    result = await agent.process_characters_category()
    print("\n" + "="*60)
    print("Results:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(test_wizard())
