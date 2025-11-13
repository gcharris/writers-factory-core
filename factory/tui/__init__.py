"""Rich TUI components for Writers Factory.

This module provides the full-screen terminal user interface with:
- 5-stage workflow pipeline (Creation → Writing → Enhancing → Analyzing → Scoring)
- Live status bar with costs, auto-save, session info
- Keyboard navigation (TAB/SHIFT+TAB between stages)
- Real-time updates
"""

from .app import WritersFactoryApp
from .status_bar import StatusBar
from .stage_navigator import StageNavigator

__all__ = [
    "WritersFactoryApp",
    "StatusBar",
    "StageNavigator",
]
