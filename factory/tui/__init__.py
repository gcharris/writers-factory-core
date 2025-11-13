"""Rich TUI components for Writers Factory.

This module provides the full-screen terminal user interface with:
- 5-stage workflow pipeline (Creation → Writing → Enhancing → Analyzing → Scoring)
- Live status bar with costs, auto-save, session info
- Keyboard navigation (TAB/SHIFT+TAB between stages)
- Real-time updates
- Knowledge query interface (K shortcut)
"""

from .app import WritersFactoryApp
from .status_bar import StatusBar
from .stage_navigator import StageNavigator
from .query_dialog import QueryDialog

__all__ = [
    "WritersFactoryApp",
    "StatusBar",
    "StageNavigator",
    "QueryDialog",
]
