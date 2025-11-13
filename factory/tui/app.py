"""Main TUI application for Writers Factory."""

import asyncio
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from factory.core.storage import Session, CostTracker, PreferencesManager
from factory.knowledge.router import KnowledgeRouter
from factory.tools import ModelComparisonTool
from .status_bar import StatusBar
from .stage_navigator import StageNavigator
from .query_dialog import QueryDialog

logger = logging.getLogger(__name__)


class WritersFactoryApp:
    """Main TUI application.
    
    Features:
    - Full-screen interface with Rich
    - 5-stage workflow navigation
    - Live status updates
    - Auto-save integration
    - Keyboard shortcuts
    """
    
    def __init__(self, project_path: Path):
        """Initialize application.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.console = Console()

        # Core components (from Task 1)
        self.session = Session(self.project_path)
        self.cost_tracker = CostTracker(self.project_path / ".session")
        self.preferences = PreferencesManager(self.project_path / ".session")

        # Knowledge router (Task 3)
        notebooklm_enabled = self.preferences.data.notebooklm_enabled if hasattr(self.preferences.data, 'notebooklm_enabled') else False
        notebooklm_id = self.preferences.data.notebooklm_notebook_id if hasattr(self.preferences.data, 'notebooklm_notebook_id') else None
        self.knowledge_router = KnowledgeRouter(
            project_path=self.project_path,
            notebooklm_enabled=notebooklm_enabled,
            notebooklm_notebook_id=notebooklm_id
        )

        # UI components
        self.status_bar = StatusBar()
        self.navigator = StageNavigator(self.session.data.current_state.stage)
        self.query_dialog = QueryDialog(self.knowledge_router, self.console)
        self.model_comparison = ModelComparisonTool(
            preferences_manager=self.preferences,
            console=self.console
        )

        # State
        self.running = False
        self._last_key: Optional[str] = None
        
    def make_layout(self) -> Layout:
        """Create main layout."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=1),
        )
        
        return layout
        
    def update_layout(self, layout: Layout):
        """Update layout with current content."""
        # Header: Status bar
        self.status_bar.update(
            stage=self.navigator.current_stage,
            session_cost=self.cost_tracker.get_session_cost(),
            last_save_time=self.session.data.last_save_time,
            is_saving=self.session._saving,
            has_unsaved_changes=self.session.data.dirty,
        )
        layout["header"].update(Panel(self.status_bar.render(), style="on #1a1a1a"))
        
        # Body: Current stage view
        layout["body"].update(self.navigator.render_stage_panel())
        
        # Footer: Help text
        help_text = Text(
            "TAB/SHIFT+TAB: Navigate stages | C: Model Comparison | K: Ask Question | Q: Quit",
            style="dim",
            justify="center"
        )
        layout["footer"].update(Panel(help_text, style="dim"))
        
    async def start(self):
        """Start the application."""
        self.running = True
        
        # Check for crash recovery
        if self.session.was_interrupted():
            self.console.print(
                "[yellow]⚠ Previous session was interrupted. Resuming...[/]"
            )
            await asyncio.sleep(1)
        
        # Start auto-save
        self.session.start_auto_save()
        
        # Create layout
        layout = self.make_layout()
        
        # Main loop with Live display
        try:
            with Live(
                layout,
                console=self.console,
                screen=True,
                refresh_per_second=4,
            ) as live:
                while self.running:
                    # Update display
                    self.update_layout(layout)
                    live.refresh()
                    
                    # Check for keyboard input (simplified - real impl would use blessed/prompt_toolkit)
                    await asyncio.sleep(0.25)
                    
        except KeyboardInterrupt:
            pass
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the application."""
        self.running = False
        self.session.stop_auto_save()
        
        # Final save
        await self.session.close()
        
        self.console.print("\n[green]Session saved. Goodbye![/]")
        
    async def handle_key(self, key: str):
        """Handle keyboard input.
        
        Args:
            key: Key pressed
        """
        self._last_key = key
        
        if key == "tab":
            # Next stage
            new_stage = self.navigator.next_stage()
            self.session.set_stage(new_stage)
            
        elif key == "shift+tab":
            # Previous stage
            new_stage = self.navigator.prev_stage()
            self.session.set_stage(new_stage)
            
        elif key == "c":
            # Open model comparison (Task 5)
            await self._handle_model_comparison()

        elif key == "k":
            # Ask question (Task 3)
            await self._handle_query_dialog()
            
        elif key == "q":
            # Quit
            self.running = False

    async def _handle_query_dialog(self):
        """Handle knowledge query dialog.

        Triggered by 'K' keyboard shortcut.
        """
        # Run interactive query
        result = await self.query_dialog.interactive_query()

        if result:
            # Track query in session
            self.session.add_recent_query(
                query=result.metadata.get("query", ""),
                source=result.source.value
            )

    async def _handle_model_comparison(self):
        """Handle model comparison dialog.

        Triggered by 'C' keyboard shortcut.
        """
        self.console.print("\n[bold cyan]Model Comparison Tool[/]\n")
        self.console.print("Enter prompt to test across models:")

        try:
            prompt = self.console.input("[cyan]❯[/] ")
        except (KeyboardInterrupt, EOFError):
            return

        if not prompt.strip():
            return

        self.console.print("\nSelect models to compare (2-4):")
        self.console.print("1. claude-sonnet-4.5")
        self.console.print("2. claude-opus-4")
        self.console.print("3. gpt-4o")
        self.console.print("4. gemini-2-flash")

        try:
            selection = self.console.input("\n[cyan]Enter numbers (e.g., 1,3):[/] ")
        except (KeyboardInterrupt, EOFError):
            return

        # Parse model selection
        model_map = {
            "1": "claude-sonnet-4.5",
            "2": "claude-opus-4",
            "3": "gpt-4o",
            "4": "gemini-2-flash"
        }

        selected_models = [
            model_map[num.strip()]
            for num in selection.split(",")
            if num.strip() in model_map
        ]

        if len(selected_models) < 2:
            self.console.print("[red]Need at least 2 models[/]")
            return

        # Run comparison
        self.console.print(f"\n[yellow]Comparing {len(selected_models)} models...[/]")

        result = await self.model_comparison.compare_models(
            prompt=prompt,
            models=selected_models
        )

        # Display comparison
        self.console.print(self.model_comparison.render_comparison(result))

        # Ask for winner
        self.console.print("\n[cyan]Select winner (or press Enter to skip):[/]")
        for i, model in enumerate(selected_models, 1):
            self.console.print(f"{i}. {model}")

        try:
            winner_input = self.console.input("\n[cyan]Winner number:[/] ")
            if winner_input.strip() and winner_input.strip().isdigit():
                winner_idx = int(winner_input.strip()) - 1
                if 0 <= winner_idx < len(selected_models):
                    winner = selected_models[winner_idx]
                    await self.model_comparison.save_preference(result, winner)
                    self.console.print(f"[green]✓ Saved preference: {winner}[/]")
        except (KeyboardInterrupt, EOFError, ValueError):
            pass


# Simple CLI entry point for testing
async def main():
    """CLI entry point."""
    import sys
    
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1])
    else:
        project_path = Path.cwd()
    
    app = WritersFactoryApp(project_path)
    await app.start()


if __name__ == "__main__":
    asyncio.run(main())
