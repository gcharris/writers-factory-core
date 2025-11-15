"""Character Extractor - Extract characters and their attributes from manuscript.

Uses NLP + heuristics to identify:
- Character names (proper nouns, pronouns)
- Traits (adjectives, descriptions)
- Psychology (motivations, fears, goals)
- Relationships (interactions, dynamics)
- Character arcs (changes over time)
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class Character:
    """Extracted character entity.

    Attributes:
        name: Primary character name
        aliases: Alternative names/nicknames
        traits: Physical and personality traits
        psychology: Motivations, fears, goals
        first_appearance: Chunk ID where character first appears
        appearances: List of chunk IDs where character appears
        relationships: Relationships with other characters
        arc_notes: Character development notes across manuscript
    """
    name: str
    aliases: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    psychology: str = ""
    first_appearance: str = ""
    appearances: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    arc_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class CharacterExtractor:
    """Extract characters from manuscript.

    Uses:
    1. LLM for intelligent extraction (if available)
    2. Heuristics fallback (proper nouns, patterns)
    """

    def __init__(self, llm_provider=None):
        """Initialize character extractor.

        Args:
            llm_provider: Optional LLM for intelligent extraction
        """
        self.llm = llm_provider
        self.characters: Dict[str, Character] = {}
        self.name_patterns = self._compile_name_patterns()

    async def extract(self, chunks: List[Any]) -> List[Character]:
        """Extract all characters from manuscript.

        Args:
            chunks: List of ManuscriptChunk objects

        Returns:
            List of extracted Character objects
        """
        # Pass 1: Identify character names
        logger.info("Pass 1: Identifying character names")
        character_names = await self._identify_names(chunks)
        logger.info(f"Found {len(character_names)} potential characters")

        # Pass 2: Extract details for each character
        logger.info("Pass 2: Extracting character details")
        for name in character_names:
            character = await self._extract_character_details(name, chunks)
            self.characters[name] = character

        # Pass 3: Extract relationships
        logger.info("Pass 3: Extracting relationships")
        await self._extract_relationships(chunks)

        # Pass 4: Analyze character arcs
        logger.info("Pass 4: Analyzing character arcs")
        await self._analyze_arcs(chunks)

        return list(self.characters.values())

    async def _identify_names(self, chunks: List[Any]) -> Set[str]:
        """Identify character names using NLP or heuristics.

        Args:
            chunks: Manuscript chunks

        Returns:
            Set of character names
        """
        names = set()

        # Sample first few chunks for character discovery
        sample_chunks = chunks[:min(10, len(chunks))]

        for chunk in sample_chunks:
            if self.llm:
                # Use LLM for intelligent extraction
                chunk_names = await self._extract_names_llm(chunk.content)
                names.update(chunk_names)
            else:
                # Fallback: Regex for capitalized words
                chunk_names = self._extract_names_heuristic(chunk.content)
                names.update(chunk_names)

        # Filter out common non-names
        names = self._filter_non_names(names)

        return names

    async def _extract_names_llm(self, text: str) -> Set[str]:
        """Extract character names using LLM.

        Args:
            text: Text to analyze

        Returns:
            Set of character names
        """
        # Truncate text for LLM
        text_sample = text[:2000]

        prompt = f"""Extract all character names from this text.
Return ONLY the names, one per line, nothing else.
Include both full names and common nicknames/aliases.

Text:
{text_sample}

Names:"""

        try:
            result = await self.llm.generate(prompt)
            names = [n.strip() for n in result.split('\n') if n.strip()]
            # Filter out obvious non-names
            names = [n for n in names if self._looks_like_name(n)]
            return set(names)
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}, falling back to heuristics")
            return self._extract_names_heuristic(text)

    def _extract_names_heuristic(self, text: str) -> Set[str]:
        """Extract character names using heuristics.

        Args:
            text: Text to analyze

        Returns:
            Set of potential character names
        """
        names = set()

        # Pattern 1: Capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        names.update(capitalized)

        # Pattern 2: Names in dialogue attribution
        # e.g., "she said", "John replied"
        dialogue_names = re.findall(r'([A-Z][a-z]+)\s+(?:said|asked|replied|shouted|whispered)', text)
        names.update(dialogue_names)

        # Pattern 3: Possessive forms
        # e.g., "Mickey's weapon", "Sarah's house"
        possessive_names = re.findall(r"([A-Z][a-z]+)'s\b", text)
        names.update(possessive_names)

        return names

    def _filter_non_names(self, names: Set[str]) -> Set[str]:
        """Filter out common words that aren't character names.

        Args:
            names: Set of potential names

        Returns:
            Filtered set of names
        """
        # Common words to exclude
        common_words = {
            # Time words
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
            "January", "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December",
            # Places (may be characters, but filter obvious ones)
            "Earth", "City", "Street", "Road", "Avenue",
            # Other common capitalizations
            "The", "A", "An", "I", "He", "She", "They",
            "Chapter", "Scene", "Act"
        }

        filtered = {
            name for name in names
            if name not in common_words and len(name) > 1
        }

        return filtered

    def _looks_like_name(self, text: str) -> bool:
        """Check if text looks like a character name.

        Args:
            text: Potential name

        Returns:
            True if looks like a name
        """
        # Must start with capital letter
        if not text or not text[0].isupper():
            return False

        # Must be reasonable length (1-4 words)
        words = text.split()
        if len(words) > 4:
            return False

        # Each word should start with capital
        if not all(w[0].isupper() for w in words if w):
            return False

        return True

    async def _extract_character_details(
        self,
        name: str,
        chunks: List[Any]
    ) -> Character:
        """Extract detailed information about a character.

        Args:
            name: Character name
            chunks: Manuscript chunks

        Returns:
            Character object with details
        """
        character = Character(name=name)

        # Find all appearances
        for chunk in chunks:
            if name in chunk.content:
                character.appearances.append(chunk.chunk_id)
                if not character.first_appearance:
                    character.first_appearance = chunk.chunk_id

        # Extract traits from first few appearances
        if character.appearances:
            first_chunks = [
                chunk for chunk in chunks
                if chunk.chunk_id in character.appearances[:3]
            ]

            if self.llm:
                character.traits = await self._extract_traits_llm(name, first_chunks)
                character.psychology = await self._extract_psychology_llm(name, first_chunks)
            else:
                character.traits = self._extract_traits_heuristic(name, first_chunks)

        return character

    async def _extract_traits_llm(self, name: str, chunks: List[Any]) -> List[str]:
        """Extract character traits using LLM.

        Args:
            name: Character name
            chunks: Chunks where character appears

        Returns:
            List of traits
        """
        # Combine relevant text
        text = "\n\n".join(chunk.content[:1000] for chunk in chunks)[:3000]

        prompt = f"""Analyze the character "{name}" in this text.
List their key traits (physical, personality, abilities).
Return ONLY the traits, one per line, maximum 10 traits.

Text:
{text}

Traits:"""

        try:
            result = await self.llm.generate(prompt)
            traits = [t.strip() for t in result.split('\n') if t.strip()]
            return traits[:10]
        except Exception as e:
            logger.warning(f"Trait extraction failed: {e}")
            return []

    def _extract_traits_heuristic(self, name: str, chunks: List[Any]) -> List[str]:
        """Extract character traits using heuristics.

        Args:
            name: Character name
            chunks: Chunks where character appears

        Returns:
            List of traits
        """
        traits = []

        # Look for descriptive patterns near character name
        for chunk in chunks:
            # Pattern: "Name was/is/seemed [adjective]"
            pattern = f"{name}\\s+(?:was|is|seemed|appeared)\\s+(\\w+)"
            matches = re.findall(pattern, chunk.content, re.IGNORECASE)
            traits.extend(matches)

        # Deduplicate and limit
        return list(set(traits))[:10]

    async def _extract_psychology_llm(self, name: str, chunks: List[Any]) -> str:
        """Extract character psychology using LLM.

        Args:
            name: Character name
            chunks: Chunks where character appears

        Returns:
            Psychology description
        """
        text = "\n\n".join(chunk.content[:1000] for chunk in chunks)[:3000]

        prompt = f"""Analyze the character "{name}" and describe their core psychology:
- Main motivations
- Fears
- Goals
- Internal conflicts

Keep it to 2-3 sentences maximum.

Text:
{text}

Psychology:"""

        try:
            result = await self.llm.generate(prompt)
            return result.strip()[:500]  # Limit length
        except Exception as e:
            logger.warning(f"Psychology extraction failed: {e}")
            return ""

    async def _extract_relationships(self, chunks: List[Any]):
        """Extract relationships between characters.

        Args:
            chunks: Manuscript chunks
        """
        # Look for characters appearing together in scenes
        for chunk in chunks:
            appearing_chars = [
                name for name in self.characters.keys()
                if name in chunk.content
            ]

            # If multiple characters in same scene, they have a relationship
            if len(appearing_chars) >= 2:
                for i, char1 in enumerate(appearing_chars):
                    for char2 in appearing_chars[i+1:]:
                        # Record bidirectional relationship
                        if char2 not in self.characters[char1].relationships:
                            self.characters[char1].relationships[char2] = "appears_with"
                        if char1 not in self.characters[char2].relationships:
                            self.characters[char2].relationships[char1] = "appears_with"

    async def _analyze_arcs(self, chunks: List[Any]):
        """Analyze character arcs across manuscript.

        Args:
            chunks: Manuscript chunks
        """
        for name, character in self.characters.items():
            if len(character.appearances) < 2:
                continue

            # Analyze changes between first and last appearance
            first_chunk = next(c for c in chunks if c.chunk_id == character.first_appearance)
            last_chunk = next(c for c in chunks if c.chunk_id == character.appearances[-1])

            # Simple arc note
            arc_note = f"Appears in {len(character.appearances)} scenes from {first_chunk.metadata.get('chapter', 'start')} to {last_chunk.metadata.get('chapter', 'end')}"
            character.arc_notes.append(arc_note)

    def _compile_name_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for name detection.

        Returns:
            List of compiled regex patterns
        """
        return [
            re.compile(r'\b[A-Z][a-z]+\b'),  # Single capitalized word
            re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'),  # Two word name
        ]
