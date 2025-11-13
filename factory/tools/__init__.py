"""Tools for Writers Factory.

This module provides user-facing tools that wrap workflows and provide
enhanced functionality:
- Model comparison with visual diffs
- Preference tracking
- Side-by-side output display
"""

from .model_comparison import ModelComparisonTool, ComparisonResult

__all__ = [
    "ModelComparisonTool",
    "ComparisonResult",
]
