"""Query dialog for asking questions about the story."""

from typing import Optional
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Console

from factory.knowledge.router import KnowledgeRouter, QueryResult


class QueryDialog:
    """Interactive dialog for querying knowledge base.

    Features:
    - Ask questions about story, characters, plot
    - Automatic routing to best knowledge source
    - Displays results with references
    - Hides implementation details (Cognee/Gemini)
    """

    def __init__(self, router: KnowledgeRouter, console: Optional[Console] = None):
        """Initialize query dialog.

        Args:
            router: Knowledge router instance
            console: Rich console for output
        """
        self.router = router
        self.console = console or Console()
        self.last_result: Optional[QueryResult] = None

    async def ask_question(self, question: str) -> QueryResult:
        """Ask a question and get answer.

        Args:
            question: User's question

        Returns:
            QueryResult with answer and references
        """
        # Route and execute query
        result = await self.router.query(question, max_results=5)
        self.last_result = result

        return result

    def render_result(self, result: QueryResult) -> Panel:
        """Render query result as Rich panel.

        Args:
            result: Query result to display

        Returns:
            Rich Panel with formatted result
        """
        content = Text()

        # Answer
        content.append("Answer:\n", style="bold cyan")
        content.append(f"{result.answer}\n\n", style="white")

        # Confidence
        confidence_pct = int(result.confidence * 100)
        confidence_style = "green" if confidence_pct >= 80 else "yellow" if confidence_pct >= 60 else "red"
        content.append(f"Confidence: {confidence_pct}%\n\n", style=confidence_style)

        # References
        if result.references:
            content.append("References:\n", style="bold cyan")
            for ref in result.references:
                content.append(f"  • {ref}\n", style="dim")

        # Source info (subtle, not prominent)
        source_name = self._get_source_display_name(result.source.value)
        content.append(f"\nSource: {source_name}", style="dim italic")

        return Panel(
            content,
            title="[bold cyan]Knowledge Query Result[/]",
            border_style="cyan",
        )

    def _get_source_display_name(self, source: str) -> str:
        """Get user-friendly source name.

        Args:
            source: Internal source name

        Returns:
            User-friendly display name
        """
        # Hide implementation details
        display_names = {
            "cognee": "Local Knowledge Base",
            "gemini_file_search": "Local Knowledge Base",  # Hide Gemini
            "notebooklm": "NotebookLM Analysis"
        }
        return display_names.get(source, "Knowledge Base")

    def render_input_prompt(self) -> Panel:
        """Render input prompt for question.

        Returns:
            Rich Panel with prompt
        """
        prompt_text = Text()
        prompt_text.append("Ask a question about your story:\n\n", style="bold")
        prompt_text.append("Examples:\n", style="dim")
        prompt_text.append("  • What is Sarah's motivation in Chapter 3?\n", style="dim cyan")
        prompt_text.append("  • How does the magic system work?\n", style="dim cyan")
        prompt_text.append("  • What are the main themes?\n", style="dim cyan")
        prompt_text.append("\n")
        prompt_text.append("Type your question below:", style="italic")

        return Panel(
            prompt_text,
            title="[bold cyan]Ask a Question[/]",
            border_style="cyan",
        )

    def render_thinking(self) -> Panel:
        """Render 'thinking' indicator while processing.

        Returns:
            Rich Panel with thinking indicator
        """
        text = Text("Searching knowledge base...", style="yellow italic")
        return Panel(
            text,
            title="[yellow]Processing[/]",
            border_style="yellow",
        )

    async def interactive_query(self) -> Optional[QueryResult]:
        """Run interactive query session.

        Returns:
            QueryResult if successful, None if cancelled
        """
        # Show prompt
        self.console.print(self.render_input_prompt())

        # Get question
        try:
            question = self.console.input("\n[cyan]❯[/] ")
        except (KeyboardInterrupt, EOFError):
            return None

        if not question.strip():
            return None

        # Show thinking
        self.console.print(self.render_thinking())

        # Execute query
        result = await self.ask_question(question)

        # Show result
        self.console.print(self.render_result(result))

        return result
