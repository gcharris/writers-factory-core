"""Status bar for TUI showing session info, costs, and auto-save status."""

from datetime import datetime, timedelta
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
from rich.text import Text
from typing import Optional


class StatusBar:
    """Renders status bar at top of TUI.
    
    Shows:
    - Current stage with progress indicator
    - Session cost and budget status
    - Auto-save indicator
    - Keyboard shortcuts hint
    """
    
    def __init__(self):
        """Initialize status bar."""
        self.stage = "creation"
        self.session_cost = 0.0
        self.budget_daily = 5.0
        self.last_save_time: Optional[datetime] = None
        self.is_saving = False
        self.has_unsaved_changes = False
        
    def update(
        self,
        stage: Optional[str] = None,
        session_cost: Optional[float] = None,
        last_save_time: Optional[datetime] = None,
        is_saving: Optional[bool] = None,
        has_unsaved_changes: Optional[bool] = None,
    ):
        """Update status bar values."""
        if stage is not None:
            self.stage = stage
        if session_cost is not None:
            self.session_cost = session_cost
        if last_save_time is not None:
            self.last_save_time = last_save_time
        if is_saving is not None:
            self.is_saving = is_saving
        if has_unsaved_changes is not None:
            self.has_unsaved_changes = has_unsaved_changes
            
    def render(self) -> Table:
        """Render status bar as Rich table."""
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left", ratio=2)
        table.add_column(justify="center", ratio=1)
        table.add_column(justify="right", ratio=2)
        
        # Left: Stage indicators
        stages = ["Creation", "Writing", "Enhancing", "Analyzing", "Scoring"]
        stage_text = Text()
        for s in stages:
            s_lower = s.lower()
            if s_lower == self.stage:
                stage_text.append(f"{s} ⚡", style="bold cyan")
            elif stages.index(s) < stages.index(self.stage.title()):
                stage_text.append(f"{s} ✓", style="dim green")
            else:
                stage_text.append(s, style="dim")
            if s != stages[-1]:
                stage_text.append(" | ", style="dim")
        
        # Center: Cost info
        cost_pct = (self.session_cost / self.budget_daily) * 100 if self.budget_daily > 0 else 0
        cost_style = "red" if cost_pct >= 80 else "yellow" if cost_pct >= 50 else "green"
        cost_text = Text(f"Session: ${self.session_cost:.2f}", style=cost_style)
        
        # Right: Save status
        if self.is_saving:
            save_text = Text("● Saving...", style="yellow")
        elif self.has_unsaved_changes:
            save_text = Text("● Unsaved changes", style="yellow")
        elif self.last_save_time:
            seconds_ago = int((datetime.now() - self.last_save_time).total_seconds())
            if seconds_ago < 60:
                save_text = Text(f"● Auto-saved {seconds_ago}s ago", style="dim green")
            else:
                minutes_ago = seconds_ago // 60
                save_text = Text(f"● Auto-saved {minutes_ago}m ago", style="dim green")
        else:
            save_text = Text("● Not saved", style="dim")
        
        table.add_row(stage_text, cost_text, save_text)
        return table
