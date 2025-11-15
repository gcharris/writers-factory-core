"""NotebookLM Voice Extractor - Extract voice from personal writing in NotebookLM.

Extracts voice profile from personal writing (emails, social media, diary)
uploaded to NotebookLM, enabling beginners to start with 0 words of fiction.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
from anthropic import Anthropic

from factory.research.notebooklm_client import NotebookLMClient
from factory.core.dual_voice_profiles import StarterVoiceProfile
from factory.core.voice_extractor import (
    MetaphorDomain,
    AntiPattern,
    QualityCriteria
)
import json
import re

logger = logging.getLogger(__name__)


@dataclass
class PersonalVoiceData:
    """Data extracted from NotebookLM for voice analysis."""

    notebook_url: str
    total_words: int
    sources_by_type: Dict[str, List[str]]  # {"email": [...], "social_media": [...]}
    all_text: str  # Combined text from all sources
    word_counts_by_type: Dict[str, int]  # Word counts per type


class NotebookLMVoiceExtractor:
    """Extract voice profile from NotebookLM sources.

    Uses NotebookLM to extract personal writing (emails, social media, diary)
    and generate a StarterVoiceProfile for beginners.
    """

    def __init__(self, notebooklm_client: Optional[NotebookLMClient] = None, anthropic_client: Optional[Anthropic] = None):
        """Initialize NotebookLM voice extractor.

        Args:
            notebooklm_client: NotebookLM client for querying notebooks
            anthropic_client: Anthropic client for voice analysis
        """
        self.nlm_client = notebooklm_client or NotebookLMClient()
        self.anthropic_client = anthropic_client

    async def extract_personal_voice(
        self,
        notebook_url: str,
        min_words: int = 3000
    ) -> PersonalVoiceData:
        """Extract personal writing from NotebookLM notebook.

        Queries NotebookLM for:
        - Email excerpts
        - Social media posts
        - Diary/journal entries
        - Blog posts
        - Text messages

        Args:
            notebook_url: URL of the NotebookLM notebook
            min_words: Minimum words required (default 3000)

        Returns:
            PersonalVoiceData with categorized sources

        Raises:
            ValueError: If less than min_words found
        """
        logger.info(f"Extracting personal voice from NotebookLM: {notebook_url}")

        # Query NotebookLM for personal writing
        query = """Extract all writing samples by the user that show their personal voice.

This includes:
- Email excerpts (personal, not business)
- Social media posts (Twitter, LinkedIn, blog posts)
- Text messages or casual writing
- Diary or journal entries
- Personal essays or reflections

For each piece of writing, identify what type it is (email, social media, diary, etc.)
and include the full text.

Format your response as:

TYPE: [email|social_media|diary|blog|other]
TEXT: [full text here]
---

Repeat for each writing sample found."""

        try:
            result = await self.nlm_client.query(
                question=query,
                notebook_url=notebook_url,
                timeout=60
            )
            response_text = result["answer"]
        except Exception as e:
            logger.error(f"Failed to query NotebookLM: {e}")
            raise ValueError(f"Could not extract personal writing from NotebookLM: {e}")

        # Parse response into categorized sources
        sources_by_type = self._parse_personal_writing(response_text)

        # Count words
        total_words = 0
        word_counts_by_type = {}
        all_texts = []

        for source_type, texts in sources_by_type.items():
            type_word_count = sum(len(text.split()) for text in texts)
            word_counts_by_type[source_type] = type_word_count
            total_words += type_word_count
            all_texts.extend(texts)

        # Validate minimum words
        if total_words < min_words:
            raise ValueError(
                f"Insufficient personal writing found. "
                f"Need at least {min_words} words, found {total_words}. "
                f"Please add more emails, social media posts, or diary entries to NotebookLM."
            )

        logger.info(f"Extracted {total_words} words across {len(all_texts)} sources")
        logger.info(f"Breakdown by type: {word_counts_by_type}")

        return PersonalVoiceData(
            notebook_url=notebook_url,
            total_words=total_words,
            sources_by_type=sources_by_type,
            all_text="\n\n".join(all_texts),
            word_counts_by_type=word_counts_by_type
        )

    async def categorize_sources(
        self,
        notebook_url: str
    ) -> Dict[str, List[str]]:
        """Categorize notebook sources by type.

        Identifies:
        - personal_writing (emails, diary, social)
        - fiction_attempts (old drafts)
        - influences (favorite authors)
        - research (craft, genre)

        Args:
            notebook_url: URL of the NotebookLM notebook

        Returns:
            Dict mapping category to list of source titles
        """
        query = """Categorize all sources in this notebook into these categories:

1. Personal Writing: Emails, social media, diary, blog posts, text messages
2. Fiction Attempts: Any fiction drafts, story fragments, or creative writing exercises
3. Influences: Excerpts from favorite authors, books, articles
4. Research: Craft articles, genre research, worldbuilding notes

For each source, indicate which category it belongs to.

Format:
CATEGORY: [personal_writing|fiction_attempts|influences|research]
SOURCE: [source title or description]
---"""

        try:
            result = await self.nlm_client.query(
                question=query,
                notebook_url=notebook_url,
                timeout=30
            )
            response_text = result["answer"]
        except Exception as e:
            logger.warning(f"Could not categorize sources: {e}")
            return {}

        # Parse categorization
        categories = {
            "personal_writing": [],
            "fiction_attempts": [],
            "influences": [],
            "research": []
        }

        current_category = None
        for line in response_text.split("\n"):
            line = line.strip()
            if line.startswith("CATEGORY:"):
                current_category = line.split(":", 1)[1].strip().lower()
            elif line.startswith("SOURCE:") and current_category:
                source = line.split(":", 1)[1].strip()
                if current_category in categories:
                    categories[current_category].append(source)

        return categories

    async def extract_text_by_category(
        self,
        notebook_url: str,
        category: str
    ) -> List[str]:
        """Get all text from a specific category.

        Args:
            notebook_url: URL of the NotebookLM notebook
            category: Category to extract ("personal_writing", "fiction_attempts", etc.)

        Returns:
            List of text excerpts from that category
        """
        category_queries = {
            "personal_writing": "Extract all personal writing (emails, social media, diary)",
            "fiction_attempts": "Extract all fiction drafts and creative writing attempts",
            "influences": "Extract excerpts from favorite authors or influences",
            "research": "Extract craft articles and genre research notes"
        }

        query = category_queries.get(
            category,
            f"Extract all content related to: {category}"
        )

        try:
            result = await self.nlm_client.query(
                question=query,
                notebook_url=notebook_url,
                timeout=45
            )
            response_text = result["answer"]
        except Exception as e:
            logger.warning(f"Could not extract category '{category}': {e}")
            return []

        # Split into chunks (simple split by paragraphs)
        chunks = [chunk.strip() for chunk in response_text.split("\n\n") if chunk.strip()]
        return chunks

    async def generate_starter_voice_profile(
        self,
        personal_voice_data: PersonalVoiceData,
        genre: str
    ) -> StarterVoiceProfile:
        """Generate StarterVoiceProfile from personal writing.

        Uses LLM to analyze personal writing and extract voice characteristics.

        Args:
            personal_voice_data: PersonalVoiceData from extract_personal_voice()
            genre: Target genre for the novel (e.g., "thriller", "romance")

        Returns:
            StarterVoiceProfile with medium confidence

        Raises:
            ValueError: If no Anthropic client available
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic client required for voice analysis")

        logger.info(f"Generating starter voice profile for genre: {genre}")

        # Analyze personal writing voice
        analysis = await self._analyze_personal_writing(
            personal_voice_data.all_text,
            genre,
            list(personal_voice_data.sources_by_type.keys())
        )

        # Extract metaphor domains
        metaphor_domains = await self._extract_metaphor_domains_from_personal(
            personal_voice_data.all_text
        )

        # Identify anti-patterns
        anti_patterns = await self._identify_casual_anti_patterns(
            personal_voice_data.all_text
        )

        # Derive quality criteria (generic for starter)
        quality_criteria = self._create_starter_quality_criteria(genre)

        # Create StarterVoiceProfile
        starter_profile = StarterVoiceProfile(
            voice_name=analysis["voice_name"],
            genre=genre,
            primary_characteristics=analysis["primary_characteristics"],
            sentence_structure=analysis["sentence_structure"],
            vocabulary=analysis["vocabulary"],
            pov_style=analysis["pov_style"],
            metaphor_domains=metaphor_domains,
            anti_patterns=anti_patterns,
            quality_criteria=quality_criteria,
            voice_consistency_notes=analysis.get("consistency_notes", []),
            source_types=list(personal_voice_data.sources_by_type.keys()),
            total_source_words=personal_voice_data.total_words,
            upgrade_threshold=2500,
            confidence_level="medium"
        )

        logger.info(f"Starter voice profile created: {starter_profile.voice_name}")
        return starter_profile

    # Private helper methods

    def _parse_personal_writing(self, response_text: str) -> Dict[str, List[str]]:
        """Parse NotebookLM response into categorized writing samples.

        Expected format:
        TYPE: email
        TEXT: [text here]
        ---
        TYPE: social_media
        TEXT: [text here]
        ---

        Args:
            response_text: Response from NotebookLM

        Returns:
            Dict mapping type to list of texts
        """
        sources_by_type = {
            "email": [],
            "social_media": [],
            "diary": [],
            "blog": [],
            "other": []
        }

        # Split by separator
        sections = response_text.split("---")

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Extract TYPE and TEXT
            type_match = re.search(r"TYPE:\s*(\w+)", section, re.IGNORECASE)
            text_match = re.search(r"TEXT:\s*(.+)", section, re.IGNORECASE | re.DOTALL)

            if type_match and text_match:
                source_type = type_match.group(1).lower()
                text = text_match.group(1).strip()

                # Normalize type names
                if source_type not in sources_by_type:
                    source_type = "other"

                sources_by_type[source_type].append(text)

        return sources_by_type

    async def _analyze_personal_writing(
        self,
        text: str,
        genre: str,
        source_types: List[str]
    ) -> Dict[str, Any]:
        """Analyze personal writing to extract voice characteristics.

        Args:
            text: Combined personal writing text
            genre: Target genre
            source_types: Types of sources (for context)

        Returns:
            Dict with voice analysis
        """
        prompt = f"""Analyze this personal writing (from {', '.join(source_types)}) to extract voice characteristics.

The writer plans to write a {genre} novel. Analyze their casual voice to predict fiction style.

PERSONAL WRITING:
{text[:4000]}

Provide JSON analysis:

{{
  "voice_name": "<descriptive name, e.g., 'Casual Direct', 'Warm Conversational'>",
  "primary_characteristics": [
    "characteristic 1",
    "characteristic 2",
    "characteristic 3"
  ],
  "sentence_structure": {{
    "typical_length": "<avg words>",
    "compression_level": "<1-10 scale>",
    "preferred_patterns": ["pattern1", "pattern2"]
  }},
  "vocabulary": {{
    "formality_level": "casual|neutral|formal",
    "complexity": "simple|moderate|complex",
    "distinctive_domains": ["domain1", "domain2"]
  }},
  "pov_style": {{
    "depth": "shallow|medium|deep",
    "consciousness_mode_percentage": "<estimated %>",
    "filter_word_tolerance": "strict|moderate|lenient"
  }},
  "consistency_notes": [
    "Note about consistent patterns",
    "Note about variations"
  ]
}}

IMPORTANT: This is CASUAL writing, not fiction. Voice may differ when they write fiction.
Focus on transferable patterns (sentence rhythm, vocabulary choices, personality).
"""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = json.loads(response.content[0].text)
        return analysis

    async def _extract_metaphor_domains_from_personal(
        self,
        text: str
    ) -> Dict[str, MetaphorDomain]:
        """Extract metaphor domains from personal writing.

        Args:
            text: Personal writing text

        Returns:
            Dict of metaphor domains
        """
        prompt = f"""Identify metaphor domains in this personal writing.

TEXT:
{text[:3000]}

Return JSON:
{{
  "domains": [
    {{
      "name": "domain_name",
      "frequency_percentage": <number>,
      "max_recommended_percentage": <suggested limit>,
      "keywords": ["word1", "word2"],
      "examples": ["metaphor1", "metaphor2"]
    }}
  ]
}}

Only include domains with 10%+ usage.
"""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        result = json.loads(response.content[0].text)

        metaphor_domains = {}
        for domain in result.get("domains", []):
            metaphor_domains[domain["name"]] = MetaphorDomain(
                max_percentage=domain["max_recommended_percentage"],
                keywords=domain["keywords"],
                examples=domain["examples"]
            )

        return metaphor_domains

    async def _identify_casual_anti_patterns(
        self,
        text: str
    ) -> List[AntiPattern]:
        """Identify anti-patterns specific to transitioning from casual to fiction writing.

        Args:
            text: Personal writing text

        Returns:
            List of AntiPattern objects
        """
        # Common casual → fiction anti-patterns
        casual_anti_patterns = [
            AntiPattern(
                pattern_id="casual_filter_words",
                name="Excessive Filter Words",
                description="Overuse of 'saw', 'heard', 'felt', 'noticed' from casual writing",
                why_avoid="Fiction benefits from deeper POV immersion",
                detection_method="keyword",
                keywords=["saw", "heard", "felt", "noticed", "thought", "wondered"],
                severity="medium",
                examples=[]
            ),
            AntiPattern(
                pattern_id="casual_telling",
                name="Telling vs Showing",
                description="Casual writing often tells directly; fiction should show",
                why_avoid="Fiction readers expect immersive showing, not journalistic telling",
                detection_method="llm",
                severity="high",
                examples=[]
            ),
            AntiPattern(
                pattern_id="informal_dialogue_tags",
                name="Overly Casual Dialogue",
                description="Social media casualness may be too informal for {genre} fiction",
                why_avoid="Fiction dialogue needs balance of authenticity and readability",
                detection_method="llm",
                severity="low",
                examples=[]
            )
        ]

        return casual_anti_patterns

    def _create_starter_quality_criteria(self, genre: str) -> QualityCriteria:
        """Create generic quality criteria for starter mode.

        Criteria are broader and more forgiving than novel-specific criteria.

        Args:
            genre: Target genre

        Returns:
            QualityCriteria object
        """
        # Generic criteria for starters
        categories = [
            {
                "category_id": "voice_consistency",
                "name": "Voice Consistency",
                "points": 25,
                "description": "Does this feel like your personal voice?",
                "sub_criteria": [
                    {
                        "name": "Sentence patterns",
                        "points": 12,
                        "check": "Similar rhythm to your casual writing"
                    },
                    {
                        "name": "Vocabulary level",
                        "points": 13,
                        "check": "Natural word choices for you"
                    }
                ]
            },
            {
                "category_id": "story_clarity",
                "name": "Story Clarity",
                "points": 25,
                "description": "Is the scene clear and understandable?",
                "sub_criteria": [
                    {
                        "name": "Scene purpose",
                        "points": 13,
                        "check": "Clear what's happening and why"
                    },
                    {
                        "name": "Character actions",
                        "points": 12,
                        "check": "Characters behave logically"
                    }
                ]
            },
            {
                "category_id": "engagement",
                "name": "Reader Engagement",
                "points": 25,
                "description": "Would a reader keep reading?",
                "sub_criteria": [
                    {
                        "name": "Interest",
                        "points": 13,
                        "check": "Scene holds attention"
                    },
                    {
                        "name": "Pacing",
                        "points": 12,
                        "check": "Not too slow or rushed"
                    }
                ]
            },
            {
                "category_id": "craft_basics",
                "name": "Craft Basics",
                "points": 25,
                "description": "Basic writing craft elements",
                "sub_criteria": [
                    {
                        "name": "Grammar",
                        "points": 10,
                        "check": "No major errors"
                    },
                    {
                        "name": "POV consistency",
                        "points": 8,
                        "check": "Consistent point of view"
                    },
                    {
                        "name": "Dialogue format",
                        "points": 7,
                        "check": "Proper dialogue punctuation"
                    }
                ]
            }
        ]

        return QualityCriteria(
            total_points=100,
            categories=categories
        )
