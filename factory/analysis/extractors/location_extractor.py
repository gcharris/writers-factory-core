"""Location Extractor - Extract settings and locations from manuscript.

Identifies:
- Settings and locations
- World details
- Spatial relationships
- Descriptive consistency
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field, asdict
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class Location:
    """Extracted location entity.

    Attributes:
        name: Location name
        type: Type of location (city, planet, building, room, etc.)
        description: Physical description
        first_appearance: Chunk ID where location first appears
        appearances: List of chunk IDs where location appears
        sub_locations: Child locations (e.g., rooms within a building)
        parent_location: Parent location
    """
    name: str
    type: str = "unknown"
    description: str = ""
    first_appearance: str = ""
    appearances: List[str] = field(default_factory=list)
    sub_locations: List[str] = field(default_factory=list)
    parent_location: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class LocationExtractor:
    """Extract locations from manuscript."""

    def __init__(self, llm_provider=None):
        """Initialize location extractor.

        Args:
            llm_provider: Optional LLM for intelligent extraction
        """
        self.llm = llm_provider
        self.locations: Dict[str, Location] = {}

    async def extract(self, chunks: List[Any]) -> List[Location]:
        """Extract all locations from manuscript.

        Args:
            chunks: List of ManuscriptChunk objects

        Returns:
            List of extracted Location objects
        """
        logger.info("Extracting locations from manuscript")

        # Pass 1: Identify location names
        location_names = await self._identify_locations(chunks)
        logger.info(f"Found {len(location_names)} potential locations")

        # Pass 2: Extract details for each location
        for name in location_names:
            location = await self._extract_location_details(name, chunks)
            self.locations[name] = location

        return list(self.locations.values())

    async def _identify_locations(self, chunks: List[Any]) -> Set[str]:
        """Identify location names from text.

        Args:
            chunks: Manuscript chunks

        Returns:
            Set of location names
        """
        locations = set()

        # Sample first few chunks
        sample_chunks = chunks[:min(10, len(chunks))]

        for chunk in sample_chunks:
            if self.llm:
                chunk_locations = await self._extract_locations_llm(chunk.content)
                locations.update(chunk_locations)
            else:
                chunk_locations = self._extract_locations_heuristic(chunk.content)
                locations.update(chunk_locations)

        return locations

    async def _extract_locations_llm(self, text: str) -> Set[str]:
        """Extract locations using LLM.

        Args:
            text: Text to analyze

        Returns:
            Set of location names
        """
        text_sample = text[:2000]

        prompt = f"""Extract all location names from this text (cities, buildings, planets, rooms, etc.).
Return ONLY the location names, one per line.

Text:
{text_sample}

Locations:"""

        try:
            result = await self.llm.generate(prompt)
            locations = [l.strip() for l in result.split('\n') if l.strip()]
            return set(locations)
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}")
            return self._extract_locations_heuristic(text)

    def _extract_locations_heuristic(self, text: str) -> Set[str]:
        """Extract locations using heuristics.

        Args:
            text: Text to analyze

        Returns:
            Set of location names
        """
        locations = set()

        # Pattern 1: "in [location]", "at [location]", "to [location]"
        preposition_locations = re.findall(
            r'\b(?:in|at|to|from)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            text
        )
        locations.update(preposition_locations)

        # Pattern 2: "[Location] was/is..."
        descriptive_locations = re.findall(
            r'\b([A-Z][a-z]+)\s+(?:was|is)\s+(?:a|an)\s+(?:city|planet|building|room|place)',
            text
        )
        locations.update(descriptive_locations)

        return locations

    async def _extract_location_details(
        self,
        name: str,
        chunks: List[Any]
    ) -> Location:
        """Extract detailed information about a location.

        Args:
            name: Location name
            chunks: Manuscript chunks

        Returns:
            Location object with details
        """
        location = Location(name=name)

        # Find all appearances
        for chunk in chunks:
            if name in chunk.content:
                location.appearances.append(chunk.chunk_id)
                if not location.first_appearance:
                    location.first_appearance = chunk.chunk_id

        # Extract description from first appearance
        if location.first_appearance:
            first_chunk = next(c for c in chunks if c.chunk_id == location.first_appearance)

            if self.llm:
                location.description = await self._extract_description_llm(name, first_chunk.content)
            else:
                location.description = self._extract_description_heuristic(name, first_chunk.content)

        return location

    async def _extract_description_llm(self, name: str, text: str) -> str:
        """Extract location description using LLM.

        Args:
            name: Location name
            text: Text containing location

        Returns:
            Description string
        """
        prompt = f"""Describe the location "{name}" based on this text.
Keep it to 1-2 sentences maximum.

Text:
{text[:1000]}

Description:"""

        try:
            result = await self.llm.generate(prompt)
            return result.strip()[:300]
        except Exception as e:
            logger.warning(f"Description extraction failed: {e}")
            return ""

    def _extract_description_heuristic(self, name: str, text: str) -> str:
        """Extract location description using heuristics.

        Args:
            name: Location name
            text: Text containing location

        Returns:
            Description string (may be empty)
        """
        # Find sentence containing location name
        sentences = text.split('.')
        for sentence in sentences:
            if name in sentence:
                return sentence.strip()[:300]

        return ""
