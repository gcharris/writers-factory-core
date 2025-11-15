"""Entity Extraction Agents - Sprint 13 Task 13-02.

Specialized agents for extracting different entity types from manuscripts:
- Characters (names, traits, psychology, relationships, arcs)
- Locations (settings, world details, spatial relationships)
- Plot Threads (main plot, subplots, setup, resolution, plot holes)
- Motifs & Themes (recurring images, symbols, metaphors)
"""

from .character_extractor import CharacterExtractor, Character
from .location_extractor import LocationExtractor, Location
from .plot_tracker import PlotTracker, PlotThread
from .motif_analyzer import MotifAnalyzer, Motif

__all__ = [
    "CharacterExtractor", "Character",
    "LocationExtractor", "Location",
    "PlotTracker", "PlotThread",
    "MotifAnalyzer", "Motif"
]
