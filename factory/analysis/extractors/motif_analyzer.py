"""Motif Analyzer - Extract recurring motifs and themes.

Identifies:
- Recurring images and symbols
- Metaphor domain distribution
- Theme development and reinforcement
- Motif patterns
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import Counter
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class Motif:
    """Extracted motif/theme.

    Attributes:
        motif_id: Unique identifier
        name: Motif name
        type: symbol, image, metaphor, theme
        pattern: Recurring pattern or concept
        frequency: Number of occurrences
        appearances: List of chunk IDs where motif appears
        examples: Example quotes
        significance: Thematic significance
    """
    motif_id: str
    name: str
    type: str = "motif"
    pattern: str = ""
    frequency: int = 0
    appearances: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    significance: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class MotifAnalyzer:
    """Analyze motifs and themes in manuscript."""

    def __init__(self, llm_provider=None):
        """Initialize motif analyzer.

        Args:
            llm_provider: Optional LLM for intelligent extraction
        """
        self.llm = llm_provider
        self.motifs: Dict[str, Motif] = {}
        self.motif_counter = 0

    async def extract(self, chunks: List[Any]) -> List[Motif]:
        """Extract motifs and themes from manuscript.

        Args:
            chunks: List of ManuscriptChunk objects

        Returns:
            List of Motif objects
        """
        logger.info("Analyzing motifs and themes")

        # Pass 1: Identify recurring patterns
        await self._identify_patterns(chunks)

        # Pass 2: Analyze metaphor domains
        await self._analyze_metaphor_domains(chunks)

        # Pass 3: Extract thematic elements
        await self._extract_themes(chunks)

        return list(self.motifs.values())

    async def _identify_patterns(self, chunks: List[Any]):
        """Identify recurring patterns in text.

        Args:
            chunks: Manuscript chunks
        """
        # Collect all text
        all_text = " ".join(chunk.content for chunk in chunks)

        # Find recurring words and phrases (heuristic approach)
        # Extract significant words (not common words)
        words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())

        # Count frequencies
        word_freq = Counter(words)

        # Common words to exclude
        common_words = {
            'that', 'this', 'with', 'from', 'have', 'been', 'were', 'said',
            'would', 'there', 'their', 'about', 'which', 'when', 'make',
            'could', 'them', 'into', 'time', 'more', 'some', 'what', 'only'
        }

        # Find significantly recurring words (appear > 10 times and not common)
        for word, count in word_freq.most_common(20):
            if word in common_words:
                continue

            if count > 10:
                motif = Motif(
                    motif_id=f"motif-{self.motif_counter}",
                    name=word.capitalize(),
                    type="recurring_word",
                    pattern=word,
                    frequency=count
                )

                # Find examples
                for chunk in chunks:
                    if word in chunk.content.lower():
                        motif.appearances.append(chunk.chunk_id)

                        # Extract example sentence
                        sentences = chunk.content.split('.')
                        for sentence in sentences:
                            if word in sentence.lower():
                                motif.examples.append(sentence.strip()[:200])
                                break

                        if len(motif.examples) >= 3:
                            break

                self.motifs[motif.motif_id] = motif
                self.motif_counter += 1

                if self.motif_counter >= 10:
                    break

    async def _analyze_metaphor_domains(self, chunks: List[Any]):
        """Analyze metaphor domain usage.

        Args:
            chunks: Manuscript chunks
        """
        # Define common metaphor domains
        metaphor_domains = {
            'military': ['weapon', 'battle', 'war', 'soldier', 'combat', 'tactical', 'deploy'],
            'nature': ['flower', 'tree', 'bloom', 'grow', 'seed', 'root', 'storm'],
            'mechanical': ['machine', 'gear', 'clockwork', 'mechanism', 'click', 'grind'],
            'water': ['wave', 'tide', 'flow', 'drown', 'current', 'depth'],
            'light': ['glow', 'shine', 'bright', 'dark', 'shadow', 'illuminate']
        }

        domain_counts = {domain: 0 for domain in metaphor_domains}

        # Count domain usage
        all_text = " ".join(chunk.content for chunk in chunks).lower()

        for domain, keywords in metaphor_domains.items():
            for keyword in keywords:
                domain_counts[domain] += all_text.count(keyword)

        # Create motifs for dominant domains
        total_metaphors = sum(domain_counts.values())
        if total_metaphors > 0:
            for domain, count in domain_counts.items():
                if count > total_metaphors * 0.15:  # Domain is > 15% of metaphors
                    motif = Motif(
                        motif_id=f"motif-{self.motif_counter}",
                        name=f"{domain.capitalize()} Metaphors",
                        type="metaphor_domain",
                        pattern=f"{domain} metaphors",
                        frequency=count,
                        significance=f"Primary metaphor domain ({count/total_metaphors*100:.1f}% of metaphors)"
                    )
                    self.motifs[motif.motif_id] = motif
                    self.motif_counter += 1

    async def _extract_themes(self, chunks: List[Any]):
        """Extract thematic elements using LLM if available.

        Args:
            chunks: Manuscript chunks
        """
        if not self.llm:
            logger.info("No LLM available, skipping theme extraction")
            return

        # Sample text from beginning, middle, end
        sample_chunks = []
        if chunks:
            sample_chunks.append(chunks[0])
        if len(chunks) > 1:
            sample_chunks.append(chunks[len(chunks) // 2])
        if len(chunks) > 2:
            sample_chunks.append(chunks[-1])

        text = "\n\n".join(chunk.content[:1000] for chunk in sample_chunks)[:3000]

        prompt = f"""Identify the main themes in this text.
List 3-5 major themes.
For each theme, provide:
- Name: Theme name
- Description: One sentence

Format:
Name: [theme name]
Description: [description]

(separate each theme with a blank line)

Text:
{text}

Themes:"""

        try:
            result = await self.llm.generate(prompt)

            # Parse themes
            current_theme = {}
            for line in result.split('\n'):
                line = line.strip()
                if not line:
                    if current_theme:
                        motif = Motif(
                            motif_id=f"motif-{self.motif_counter}",
                            name=current_theme.get('name', 'Theme'),
                            type="theme",
                            pattern="thematic element",
                            significance=current_theme.get('description', '')
                        )
                        self.motifs[motif.motif_id] = motif
                        self.motif_counter += 1
                        current_theme = {}
                    continue

                if line.startswith('Name:'):
                    current_theme['name'] = line.replace('Name:', '').strip()
                elif line.startswith('Description:'):
                    current_theme['description'] = line.replace('Description:', '').strip()

            if current_theme:
                motif = Motif(
                    motif_id=f"motif-{self.motif_counter}",
                    name=current_theme.get('name', 'Theme'),
                    type="theme",
                    pattern="thematic element",
                    significance=current_theme.get('description', '')
                )
                self.motifs[motif.motif_id] = motif
                self.motif_counter += 1

        except Exception as e:
            logger.warning(f"Theme extraction failed: {e}")
