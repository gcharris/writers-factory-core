"""Stage navigator for 5-stage workflow pipeline."""

from typing import List, Optional
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


class StageNavigator:
    """Manages navigation through 5-stage workflow.
    
    Stages:
    1. Creation - Project setup, wizard
    2. Writing - Scene generation, model comparison
    3. Enhancing - Scene refinement, voice testing
    4. Analyzing - Consistency checking
    5. Scoring - Quality evaluation
    
    Navigation:
    - TAB: Next stage
    - SHIFT+TAB: Previous stage
    """
    
    STAGES = [
        "creation",
        "writing",
        "enhancing",
        "analyzing",
        "scoring",
    ]
    
    def __init__(self, initial_stage: str = "creation"):
        """Initialize navigator."""
        self.current_stage = initial_stage
        self.stage_index = self.STAGES.index(initial_stage)
        
    def next_stage(self) -> str:
        """Move to next stage."""
        self.stage_index = (self.stage_index + 1) % len(self.STAGES)
        self.current_stage = self.STAGES[self.stage_index]
        return self.current_stage
        
    def prev_stage(self) -> str:
        """Move to previous stage."""
        self.stage_index = (self.stage_index - 1) % len(self.STAGES)
        self.current_stage = self.STAGES[self.stage_index]
        return self.current_stage
        
    def goto_stage(self, stage: str) -> bool:
        """Go to specific stage."""
        if stage in self.STAGES:
            self.current_stage = stage
            self.stage_index = self.STAGES.index(stage)
            return True
        return False
        
    def get_stage_info(self, stage: str) -> dict:
        """Get information about a stage."""
        info = {
            "creation": {
                "title": "Creation",
                "description": "Set up your project with the Creation Wizard",
                "tools": ["Creation Wizard", "Project Setup"],
                "color": "cyan",
            },
            "writing": {
                "title": "Writing",
                "description": "Generate and compare scenes across models",
                "tools": ["Scene Generator", "Model Comparison", "Knowledge Query"],
                "color": "green",
            },
            "enhancing": {
                "title": "Enhancing",
                "description": "Refine scenes with voice testing and editing",
                "tools": ["Scene Enhancer", "Voice Tester", "Style Editor"],
                "color": "yellow",
            },
            "analyzing": {
                "title": "Analyzing",
                "description": "Check consistency and canon compliance",
                "tools": ["Consistency Checker", "Canon Validator"],
                "color": "blue",
            },
            "scoring": {
                "title": "Scoring",
                "description": "Evaluate quality and compare versions",
                "tools": ["Quality Scorer", "Version Comparator"],
                "color": "magenta",
            },
        }
        return info.get(stage, {})
        
    def render_pipeline(self) -> Table:
        """Render the 5-stage pipeline."""
        table = Table.grid(expand=True)
        table.add_column(justify="center")
        
        pipeline = Text()
        for i, stage in enumerate(self.STAGES):
            info = self.get_stage_info(stage)
            
            # Add stage
            if stage == self.current_stage:
                pipeline.append(f"[{info['title'].upper()}]", style=f"bold {info['color']}")
            else:
                pipeline.append(info['title'], style=f"dim {info['color']}")
            
            # Add arrow
            if i < len(self.STAGES) - 1:
                pipeline.append(" → ", style="dim")
        
        table.add_row(pipeline)
        return table
        
    def render_stage_panel(self) -> Panel:
        """Render detailed panel for current stage."""
        info = self.get_stage_info(self.current_stage)
        
        content = Text()
        content.append(f"{info['description']}\n\n", style="italic")
        content.append("Available Tools:\n", style="bold")
        for tool in info['tools']:
            content.append(f"  • {tool}\n", style=info['color'])
        content.append("\n")
        content.append("Navigation: TAB (next) | SHIFT+TAB (prev) | Q (quit)", style="dim")
        
        return Panel(
            content,
            title=f"[bold {info['color']}]{info['title']}[/]",
            border_style=info['color'],
        )
