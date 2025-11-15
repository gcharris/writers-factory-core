# Sprint 13: Novel Intelligence System - Automated Analysis & Knowledge Graph

**Date**: November 14, 2025
**Priority**: GAME-CHANGER - This is THE killer feature
**Estimated Time**: 25-32 hours (with agent efficiency, much faster)
**Budget**: Well within $920 remaining
**Market Impact**: Revolutionary for authors stuck in revision

---

## 🎯 The Vision

**Transform Writers Factory from writing tool → AI Story Bible / Novel Intelligence System**

Upload your manuscript → Get professional-level analysis → Receive strategic rewrite plan → Explore interactive knowledge graph → Query your novel like an expert editor

### The Problem We're Solving

**Every author faces this:**
- "I know something's wrong with my novel, but I can't pinpoint it"
- "Did I contradict my character's backstory in Chapter 15?"
- "Is this subplot resolved or did I forget about it?"
- "Am I overusing this metaphor/motif?"
- "My beta readers say pacing drags in the middle - where exactly?"
- "How do I maintain consistency across 100,000 words?"

**Current solutions:**
- Hire expensive editor ($2,000-5,000) ❌
- Read entire manuscript multiple times ❌
- Manual tracking in spreadsheets ❌
- Hope beta readers catch everything ❌

**Writers Factory solution:**
- Upload manuscript (5 minutes) ✅
- AI analyzes everything (automatic) ✅
- Get strategic rewrite plan (prioritized) ✅
- Interactive knowledge graph (visual exploration) ✅
- Natural language queries ("Show me all plot threads") ✅
- **Cost: $0-50 per manuscript** ✅

---

## 🌟 Market Opportunity

### Target Audiences

**Primary: Revision-Stage Authors**
- 500,000+ manuscripts in revision on Wattpad alone
- NaNoWriMo: 400,000+ participants annually (all need revision help)
- Self-publishing: 2.3M books/year on Amazon (most need revision)
- **Pain point**: "I have a draft but don't know how to fix it"
- **Willingness to pay**: $50-200 for professional analysis

**Secondary: Series Writers**
- Need continuity tracking across multiple books
- Complex character arcs spanning 3-10 books
- World-building consistency is critical
- **Use case**: The Explants (perfect example!)

**Tertiary: Writing Teachers/Coaches**
- Critique partners, beta readers, writing groups
- MFA programs, writing courses
- Need tools to give better feedback faster

### Competitive Landscape

**Current tools:**
- **Scrivener**: Manual organization, no AI analysis
- **Plottr**: Manual plotting, no automated feedback
- **AutoCrit**: Surface-level grammar/style only
- **ProWritingAid**: Sentence-level only, no story analysis
- **Manuscript Academy**: Human editors (expensive, slow)

**Writers Factory Novel Intelligence:**
- ✅ Deep story analysis (plot, character, theme)
- ✅ Automated feedback (not just grammar)
- ✅ Visual knowledge graph (explore your universe)
- ✅ Strategic rewrite plans (prioritized action items)
- ✅ Natural language queries (ask anything about your novel)
- ✅ Continuity tracking (perfect for series)
- ✅ Fast (minutes, not weeks)
- ✅ Affordable ($0-50 vs $2,000-5,000)

### Revenue Potential

**Freemium Model:**
- Free: 1 analysis per month (up to 50k words)
- Standard: $19/month (unlimited analyses up to 100k words each)
- Pro: $49/month (unlimited analyses, unlimited words, priority processing)
- Enterprise: $199/month (team collaboration, API access, white-label)

**Conservative Projections:**
- Year 1: 10,000 users × 30% paid = 3,000 × $19/mo = $684,000/year
- Year 2: 50,000 users × 30% paid = 15,000 × $19/mo = $3.4M/year
- Year 3: 200,000 users × 35% paid = 70,000 × $25/mo (avg) = $21M/year

**Upside:**
- Platform for ALL writers (not just novelists)
- Screenplays, memoirs, non-fiction books
- International market (translate to 20+ languages)
- B2B sales (publishers, agencies, MFA programs)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Novel Intelligence Pipeline                    │
└─────────────────────────────────────────────────────────────┘

INPUT STAGE
├─ Upload: DOCX, PDF, Markdown, ePub
├─ Or: Use existing Writers Factory project
└─ Parser: Split into chapters, scenes, paragraphs, dialogue

                         ↓

EXTRACTION STAGE (Parallel Processing)
├─ Character Extractor Agent
│   • Names, aliases, traits, psychology
│   • Character arcs and development
│   • Relationships and dynamics
│
├─ Location Extractor Agent
│   • Settings, world details
│   • Spatial relationships
│   • Descriptive consistency
│
├─ Plot Thread Tracker Agent
│   • Main plot and subplots
│   • Setup, development, resolution
│   • Plot holes and loose threads
│
├─ Motif & Theme Analyzer Agent
│   • Recurring images, symbols
│   • Metaphor domain distribution
│   • Theme development and reinforcement
│
├─ Timeline Builder Agent
│   • Sequence of events
│   • Causality chains
│   • Time markers and consistency
│
└─ Dialogue Analyzer Agent
    • Character voice distinctness
    • Exposition vs subtext balance
    • Dialogue tags and action beats

                         ↓

KNOWLEDGE GRAPH CONSTRUCTION
├─ Nodes: Characters, Locations, Motifs, Themes, Events
├─ Edges: Relationships, Causality, Timeline, References
├─ Attributes: Traits, descriptions, metadata, scores
└─ Storage: Graph database (Neo4j or JSON-based)

                         ↓

ANALYSIS STAGE (Your Existing Skills!)
├─ Scene Analyzer: Score all scenes (100-point system)
├─ Character Validator: Consistency across manuscript
├─ Voice Authenticator: Style consistency check
├─ Plot Hole Detector: Unresolved threads
├─ Pacing Analyzer: Narrative momentum tracking
└─ Metaphor Analyzer: Domain distribution and saturation

                         ↓

INSIGHT GENERATION
├─ Priority Matrix: P0 (critical) → P3 (minor)
├─ Strategic Rewrite Plan: Specific actionable fixes
├─ Character Arc Reports: Development analysis
├─ Plot Thread Status: Resolved vs unresolved
├─ Theme Reinforcement: Where to strengthen themes
└─ Pacing Heatmap: Scene-by-scene momentum

                         ↓

INTERACTIVE EXPLORATION
├─ Visual Knowledge Graph: Explore entities and relationships
├─ Natural Language Queries: Ask anything about your novel
├─ Analysis Dashboard: Scores, charts, priorities
├─ Scene Navigation: Click to jump to specific scenes
└─ Export & Share: Reports, graphs, insights
```

---

## 📋 Implementation Tasks

### Phase A: Core Pipeline (15-20h)

#### Task 13-01: Manuscript Ingestion & Parsing (3h)

**Goal:** Accept manuscripts in multiple formats and parse into analyzable chunks

**File:** `factory/analysis/manuscript_ingester.py`

**Key Components:**

```python
from pathlib import Path
from typing import Dict, List, Any, Optional
import docx
import PyPDF2
import markdown
from dataclasses import dataclass

@dataclass
class ManuscriptChunk:
    """A chunk of manuscript for analysis."""
    chunk_id: str
    chunk_type: str  # "chapter", "scene", "paragraph", "dialogue"
    content: str
    metadata: Dict[str, Any]
    parent_id: Optional[str] = None
    order: int = 0

class ManuscriptIngester:
    """
    Ingest manuscripts from various formats.

    Supports:
    - DOCX (Microsoft Word)
    - PDF
    - Markdown
    - Plain text
    - Existing Writers Factory projects (scenes/ directory)
    """

    def __init__(self):
        self.parsers = {
            '.docx': self._parse_docx,
            '.pdf': self._parse_pdf,
            '.md': self._parse_markdown,
            '.txt': self._parse_text
        }

    async def ingest(
        self,
        source: str | Path,
        source_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Ingest manuscript from file or project.

        Args:
            source: File path or project ID
            source_type: "file", "project", or "auto"

        Returns:
            {
                "manuscript_id": str,
                "title": str,
                "word_count": int,
                "chunks": List[ManuscriptChunk],
                "metadata": {...}
            }
        """
        if source_type == "project" or self._is_project(source):
            return await self._ingest_project(source)
        else:
            return await self._ingest_file(source)

    async def _ingest_project(self, project_path: Path) -> Dict:
        """Ingest existing Writers Factory project."""
        # Read manifest.json
        manifest_path = project_path / "manifest.json"
        manifest = json.loads(manifest_path.read_text())

        chunks = []
        chunk_order = 0

        # Walk through acts and chapters
        for act in manifest["acts"]:
            for chapter in act["chapters"]:
                for scene in chapter["scenes"]:
                    # Load scene file
                    scene_path = project_path / scene["file_path"]
                    content = scene_path.read_text()

                    # Parse scene metadata from frontmatter
                    metadata = self._parse_frontmatter(content)

                    # Create chunk
                    chunk = ManuscriptChunk(
                        chunk_id=scene["id"],
                        chunk_type="scene",
                        content=content,
                        metadata={
                            **metadata,
                            "act": act["title"],
                            "chapter": chapter["title"],
                            "word_count": scene["word_count"]
                        },
                        parent_id=chapter["id"],
                        order=chunk_order
                    )
                    chunks.append(chunk)
                    chunk_order += 1

        return {
            "manuscript_id": manifest["id"],
            "title": manifest["title"],
            "word_count": sum(c.metadata.get("word_count", 0) for c in chunks),
            "chunks": chunks,
            "metadata": {
                "source_type": "project",
                "acts": len(manifest["acts"]),
                "chapters": sum(len(a["chapters"]) for a in manifest["acts"]),
                "scenes": len(chunks)
            }
        }

    async def _ingest_file(self, file_path: Path) -> Dict:
        """Ingest manuscript from file."""
        file_path = Path(file_path)

        # Select parser based on extension
        parser = self.parsers.get(file_path.suffix, self._parse_text)

        # Parse file
        raw_content = parser(file_path)

        # Split into chunks
        chunks = self._split_into_chunks(raw_content)

        # Generate manuscript ID
        manuscript_id = self._generate_id(file_path.stem)

        return {
            "manuscript_id": manuscript_id,
            "title": file_path.stem,
            "word_count": sum(len(c.content.split()) for c in chunks),
            "chunks": chunks,
            "metadata": {
                "source_type": "file",
                "source_path": str(file_path),
                "file_format": file_path.suffix
            }
        }

    def _parse_docx(self, file_path: Path) -> str:
        """Parse DOCX file."""
        doc = docx.Document(file_path)
        return "\n\n".join(p.text for p in doc.paragraphs)

    def _parse_pdf(self, file_path: Path) -> str:
        """Parse PDF file."""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n\n".join(
                page.extract_text() for page in reader.pages
            )

    def _parse_markdown(self, file_path: Path) -> str:
        """Parse Markdown file."""
        return file_path.read_text()

    def _parse_text(self, file_path: Path) -> str:
        """Parse plain text file."""
        return file_path.read_text()

    def _split_into_chunks(self, content: str) -> List[ManuscriptChunk]:
        """
        Split content into analyzable chunks.

        Strategy:
        1. Detect chapter boundaries (# Chapter, "Chapter N", etc.)
        2. Split chapters into scenes (*** scene breaks, blank lines)
        3. Preserve paragraph structure
        """
        chunks = []

        # Split by chapter markers
        chapters = self._detect_chapters(content)

        for i, chapter in enumerate(chapters):
            # Split chapter into scenes
            scenes = self._detect_scenes(chapter["content"])

            for j, scene in enumerate(scenes):
                chunk = ManuscriptChunk(
                    chunk_id=f"chunk-{i}-{j}",
                    chunk_type="scene",
                    content=scene,
                    metadata={
                        "chapter": chapter.get("title", f"Chapter {i+1}"),
                        "scene_number": j+1,
                        "word_count": len(scene.split())
                    },
                    parent_id=f"chapter-{i}",
                    order=len(chunks)
                )
                chunks.append(chunk)

        return chunks

    def _detect_chapters(self, content: str) -> List[Dict]:
        """Detect chapter boundaries."""
        # Look for patterns like:
        # "# Chapter 1"
        # "Chapter One"
        # "CHAPTER 1"
        # etc.

        chapter_patterns = [
            r'^#\s+Chapter\s+\d+',
            r'^Chapter\s+(?:\d+|One|Two|Three|Four|Five)',
            r'^CHAPTER\s+\d+',
        ]

        # Implementation: Regex split
        # For now, return simple split

        return [{"title": "Chapter", "content": content}]

    def _detect_scenes(self, chapter_content: str) -> List[str]:
        """Detect scene boundaries within chapter."""
        # Look for:
        # "***" or "* * *" (scene breaks)
        # Multiple blank lines
        # POV changes

        # Simple implementation: Split on triple asterisk
        if "***" in chapter_content:
            return [s.strip() for s in chapter_content.split("***") if s.strip()]

        # Or split on double newlines
        return [s.strip() for s in chapter_content.split("\n\n\n") if s.strip()]

    def _parse_frontmatter(self, content: str) -> Dict:
        """Parse YAML frontmatter from scene file."""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2:
                import yaml
                return yaml.safe_load(parts[1])
        return {}
```

**Testing:**
- Test with DOCX, PDF, Markdown, plain text
- Test with existing Writers Factory project
- Verify chunk splitting accuracy
- Test metadata extraction

---

#### Task 13-02: Entity Extraction Agents (6-8h)

**Goal:** Extract all entities from manuscript using specialized agents

**Files:**
- `factory/analysis/extractors/character_extractor.py`
- `factory/analysis/extractors/location_extractor.py`
- `factory/analysis/extractors/plot_tracker.py`
- `factory/analysis/extractors/motif_analyzer.py`
- `factory/analysis/extractors/timeline_builder.py`

**Character Extractor:**

```python
from typing import Dict, List, Set
from dataclasses import dataclass
import re

@dataclass
class Character:
    """Extracted character entity."""
    name: str
    aliases: List[str]
    traits: List[str]
    psychology: str
    first_appearance: str  # chunk_id
    appearances: List[str]  # List of chunk_ids
    relationships: Dict[str, str]  # {other_character: relationship_type}
    arc_notes: List[str]

class CharacterExtractor:
    """
    Extract characters from manuscript.

    Uses NLP + heuristics to identify:
    - Character names (proper nouns, pronouns)
    - Traits (adjectives, descriptions)
    - Psychology (motivations, fears, goals)
    - Relationships (interactions, dynamics)
    - Character arcs (changes over time)
    """

    def __init__(self, llm_provider=None):
        self.llm = llm_provider
        self.characters = {}
        self.name_patterns = self._compile_name_patterns()

    async def extract(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[Character]:
        """Extract all characters from manuscript."""

        # Pass 1: Identify character names
        character_names = await self._identify_names(chunks)

        # Pass 2: Extract details for each character
        for name in character_names:
            character = await self._extract_character_details(
                name, chunks
            )
            self.characters[name] = character

        # Pass 3: Extract relationships
        await self._extract_relationships(chunks)

        # Pass 4: Analyze character arcs
        await self._analyze_arcs(chunks)

        return list(self.characters.values())

    async def _identify_names(
        self,
        chunks: List[ManuscriptChunk]
    ) -> Set[str]:
        """Identify character names using NLP."""
        names = set()

        for chunk in chunks:
            # Use LLM to extract names
            if self.llm:
                prompt = f"""
                Extract all character names from this text.
                Return only the names, one per line.

                Text:
                {chunk.content[:2000]}
                """

                result = await self.llm.generate(prompt)
                chunk_names = [n.strip() for n in result.split('\n') if n.strip()]
                names.update(chunk_names)
            else:
                # Fallback: Regex for capitalized words
                chunk_names = re.findall(r'\b[A-Z][a-z]+\b', chunk.content)
                names.update(chunk_names)

        # Filter out common non-names
        names = self._filter_non_names(names)

        return names

    async def _extract_character_details(
        self,
        name: str,
        chunks: List[ManuscriptChunk]
    ) -> Character:
        """Extract detailed information about a character."""

        # Find all chunks where character appears
        appearances = [
            chunk.chunk_id for chunk in chunks
            if name in chunk.content
        ]

        # Extract traits
        traits = await self._extract_traits(name, chunks)

        # Extract psychology
        psychology = await self._extract_psychology(name, chunks)

        # Find aliases
        aliases = await self._find_aliases(name, chunks)

        return Character(
            name=name,
            aliases=aliases,
            traits=traits,
            psychology=psychology,
            first_appearance=appearances[0] if appearances else None,
            appearances=appearances,
            relationships={},
            arc_notes=[]
        )

    async def _extract_traits(
        self,
        name: str,
        chunks: List[ManuscriptChunk]
    ) -> List[str]:
        """Extract character traits."""

        if not self.llm:
            return []

        # Get chunks where character appears
        relevant_chunks = [
            c for c in chunks if name in c.content
        ][:5]  # First 5 appearances

        # Ask LLM to extract traits
        prompt = f"""
        Extract character traits for {name} from these excerpts.
        Return specific traits as a list.

        Examples: cynical, protective, analytical, traumatized

        Excerpts:
        {self._format_chunks_for_prompt(relevant_chunks, name)}
        """

        result = await self.llm.generate(prompt)
        traits = [t.strip() for t in result.split('\n') if t.strip()]

        return traits[:10]  # Top 10 traits

    async def _extract_psychology(
        self,
        name: str,
        chunks: List[ManuscriptChunk]
    ) -> str:
        """Extract character psychology summary."""

        if not self.llm:
            return ""

        relevant_chunks = [
            c for c in chunks if name in c.content
        ][:10]

        prompt = f"""
        Analyze the psychology of {name} based on these excerpts.
        Write a 2-3 sentence summary covering:
        - Core motivations
        - Fears or conflicts
        - Personality patterns

        Excerpts:
        {self._format_chunks_for_prompt(relevant_chunks, name)}
        """

        psychology = await self.llm.generate(prompt)

        return psychology.strip()

    async def _extract_relationships(
        self,
        chunks: List[ManuscriptChunk]
    ) -> None:
        """Extract relationships between characters."""

        if not self.llm:
            return

        character_names = list(self.characters.keys())

        # Find chunks with multiple characters
        for chunk in chunks:
            characters_in_chunk = [
                name for name in character_names
                if name in chunk.content
            ]

            if len(characters_in_chunk) < 2:
                continue

            # Ask LLM about relationships
            prompt = f"""
            Describe the relationships between these characters in this scene:
            {', '.join(characters_in_chunk)}

            Return in format: "Character1 -> Character2: relationship_type"
            Examples:
            - "Mickey -> Noni: partnership, trust"
            - "Mickey -> CIA: distrust, forced cooperation"

            Scene:
            {chunk.content[:1500]}
            """

            result = await self.llm.generate(prompt)

            # Parse relationships
            for line in result.split('\n'):
                if '->' in line:
                    parts = line.split('->')
                    if len(parts) == 2:
                        from_char = parts[0].strip()
                        rest = parts[1].split(':')
                        if len(rest) == 2:
                            to_char = rest[0].strip()
                            relationship = rest[1].strip()

                            if from_char in self.characters:
                                self.characters[from_char].relationships[to_char] = relationship

    async def _analyze_arcs(
        self,
        chunks: List[ManuscriptChunk]
    ) -> None:
        """Analyze character arcs across manuscript."""

        if not self.llm:
            return

        for name, character in self.characters.items():
            # Get first, middle, last appearances
            appearances = character.appearances
            if len(appearances) < 3:
                continue

            sample_chunks = [
                chunks[0],  # First appearance
                chunks[len(chunks) // 2],  # Middle
                chunks[-1]  # End
            ]

            # Filter to chunks with this character
            sample_chunks = [c for c in sample_chunks if name in c.content]

            if not sample_chunks:
                continue

            prompt = f"""
            Analyze the character arc for {name} across these key moments.
            Describe how they change or develop.

            Beginning:
            {sample_chunks[0].content[:500] if len(sample_chunks) > 0 else "N/A"}

            Middle:
            {sample_chunks[1].content[:500] if len(sample_chunks) > 1 else "N/A"}

            End:
            {sample_chunks[2].content[:500] if len(sample_chunks) > 2 else "N/A"}
            """

            arc_analysis = await self.llm.generate(prompt)
            character.arc_notes.append(arc_analysis)
```

**Plot Thread Tracker:**

```python
@dataclass
class PlotThread:
    """A plot thread or subplot."""
    thread_id: str
    title: str
    introduction: str  # chunk_id where introduced
    developments: List[str]  # chunk_ids where developed
    resolution: Optional[str]  # chunk_id where resolved
    status: str  # "resolved", "unresolved", "abandoned"
    priority: str  # "main", "major_subplot", "minor_subplot"
    related_characters: List[str]
    related_locations: List[str]
    description: str

class PlotThreadTracker:
    """
    Track plot threads and subplots.

    Identifies:
    - Main plot and subplots
    - Setup, development, resolution
    - Plot holes (unresolved threads)
    - Abandoned subplots
    """

    def __init__(self, llm_provider):
        self.llm = llm_provider
        self.threads = {}

    async def track(
        self,
        chunks: List[ManuscriptChunk],
        characters: List[Character]
    ) -> List[PlotThread]:
        """Track all plot threads."""

        # Identify plot threads
        threads = await self._identify_threads(chunks)

        # Track development
        for thread in threads:
            await self._track_development(thread, chunks)

        # Check resolution status
        for thread in threads:
            await self._check_resolution(thread, chunks)

        return threads

    async def _identify_threads(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[PlotThread]:
        """Identify main plot threads."""

        # Analyze entire manuscript for threads
        prompt = f"""
        Identify all major plot threads in this manuscript.

        For each thread, provide:
        - Title (brief, descriptive)
        - Priority (main, major_subplot, minor_subplot)
        - Characters involved

        Format:
        Thread: [Title]
        Priority: [main/major/minor]
        Characters: [list]

        Manuscript summary:
        {self._create_manuscript_summary(chunks)}
        """

        result = await self.llm.generate(prompt, max_tokens=2000)

        # Parse result into PlotThread objects
        threads = self._parse_threads(result)

        return threads

    async def _track_development(
        self,
        thread: PlotThread,
        chunks: List[ManuscriptChunk]
    ) -> None:
        """Track where thread is developed."""

        # Search for mentions of thread
        for chunk in chunks:
            prompt = f"""
            Does this scene develop the plot thread "{thread.title}"?
            Answer with just "yes" or "no", then brief explanation.

            Scene:
            {chunk.content[:1000]}
            """

            result = await self.llm.generate(prompt, max_tokens=100)

            if result.lower().startswith("yes"):
                thread.developments.append(chunk.chunk_id)

    async def _check_resolution(
        self,
        thread: PlotThread,
        chunks: List[ManuscriptChunk]
    ) -> None:
        """Check if thread is resolved."""

        # Check last 20% of manuscript
        final_chunks = chunks[-len(chunks)//5:]

        prompt = f"""
        Is the plot thread "{thread.title}" resolved in these final scenes?

        Answer "resolved" if the thread reaches a conclusion.
        Answer "unresolved" if it's left hanging.
        Answer "abandoned" if it's dropped without resolution.

        Then explain briefly.

        Final scenes:
        {self._format_chunks_for_prompt(final_chunks)}
        """

        result = await self.llm.generate(prompt, max_tokens=200)

        if "resolved" in result.lower():
            thread.status = "resolved"
            # Find resolution scene
            for chunk in final_chunks:
                if thread.title.lower() in chunk.content.lower():
                    thread.resolution = chunk.chunk_id
                    break
        elif "abandoned" in result.lower():
            thread.status = "abandoned"
        else:
            thread.status = "unresolved"
```

**Motif & Theme Analyzer:**

```python
@dataclass
class Motif:
    """A recurring motif or theme."""
    name: str
    category: str  # "metaphor_domain", "symbol", "theme"
    occurrences: List[str]  # chunk_ids where it appears
    frequency: int
    distribution: Dict[str, int]  # Distribution across acts/chapters
    analysis: str

class MotifAnalyzer:
    """
    Analyze motifs, metaphors, and themes.

    Tracks:
    - Metaphor domain distribution (casino, addiction, martial arts, etc.)
    - Recurring symbols and images
    - Theme development and reinforcement
    """

    def __init__(self, llm_provider, metaphor_domains: Dict = None):
        self.llm = llm_provider
        self.metaphor_domains = metaphor_domains or self._default_domains()
        self.motifs = []

    def _default_domains(self) -> Dict[str, List[str]]:
        """Default metaphor domains."""
        return {
            "gambling": ["casino", "poker", "blackjack", "chips", "dealer", "house edge", "odds", "bet"],
            "addiction": ["craving", "withdrawal", "detox", "relapse", "recovery", "sobriety", "fix"],
            "martial_arts": ["stance", "balance", "center", "kata", "sparring", "dojo", "discipline"],
            "music": ["rhythm", "tempo", "harmony", "cadence", "note", "chord", "symphony"],
            "medical": ["surgical", "diagnosis", "symptom", "treatment", "therapy", "prescription"]
        }

    async def analyze(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[Motif]:
        """Analyze all motifs in manuscript."""

        # Analyze metaphor domains
        domain_motifs = await self._analyze_metaphor_domains(chunks)
        self.motifs.extend(domain_motifs)

        # Identify recurring symbols
        symbol_motifs = await self._identify_symbols(chunks)
        self.motifs.extend(symbol_motifs)

        # Track themes
        theme_motifs = await self._track_themes(chunks)
        self.motifs.extend(theme_motifs)

        return self.motifs

    async def _analyze_metaphor_domains(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[Motif]:
        """Analyze metaphor domain distribution."""

        domain_motifs = []

        for domain_name, keywords in self.metaphor_domains.items():
            occurrences = []
            total_count = 0
            distribution = {}

            for chunk in chunks:
                # Count keyword occurrences
                count = sum(
                    chunk.content.lower().count(keyword)
                    for keyword in keywords
                )

                if count > 0:
                    occurrences.append(chunk.chunk_id)
                    total_count += count

                    # Track distribution by chapter
                    chapter = chunk.metadata.get("chapter", "Unknown")
                    distribution[chapter] = distribution.get(chapter, 0) + count

            if total_count > 0:
                motif = Motif(
                    name=f"{domain_name}_metaphors",
                    category="metaphor_domain",
                    occurrences=occurrences,
                    frequency=total_count,
                    distribution=distribution,
                    analysis=f"Used {total_count} times across {len(occurrences)} scenes"
                )
                domain_motifs.append(motif)

        return domain_motifs

    async def _identify_symbols(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[Motif]:
        """Identify recurring symbols."""

        if not self.llm:
            return []

        # Ask LLM to identify symbols
        prompt = f"""
        Identify recurring symbols or images in this manuscript.

        Look for:
        - Objects that appear multiple times with significance
        - Recurring visual images
        - Symbolic elements

        Return as list: "Symbol name: Brief description"

        Manuscript excerpts:
        {self._sample_manuscript(chunks, sample_size=10)}
        """

        result = await self.llm.generate(prompt, max_tokens=500)

        # Parse symbols
        symbols = []
        for line in result.split('\n'):
            if ':' in line:
                symbol_name = line.split(':')[0].strip()
                description = line.split(':')[1].strip()

                # Find occurrences
                occurrences = [
                    c.chunk_id for c in chunks
                    if symbol_name.lower() in c.content.lower()
                ]

                if occurrences:
                    motif = Motif(
                        name=symbol_name,
                        category="symbol",
                        occurrences=occurrences,
                        frequency=len(occurrences),
                        distribution={},
                        analysis=description
                    )
                    symbols.append(motif)

        return symbols

    async def _track_themes(
        self,
        chunks: List[ManuscriptChunk]
    ) -> List[Motif]:
        """Track major themes."""

        if not self.llm:
            return []

        # Identify themes
        prompt = f"""
        Identify the major themes in this manuscript.

        For each theme, provide:
        - Theme name (concise)
        - Brief description

        Format: "Theme: Description"

        Manuscript summary:
        {self._sample_manuscript(chunks, sample_size=15)}
        """

        result = await self.llm.generate(prompt, max_tokens=500)

        # Parse themes
        themes = []
        for line in result.split('\n'):
            if ':' in line:
                theme_name = line.split(':')[0].strip()
                description = line.split(':')[1].strip()

                # Track where theme appears
                occurrences = []
                for chunk in chunks:
                    # Ask if theme appears in chunk
                    check_prompt = f"""
                    Does the theme "{theme_name}" appear in this scene?
                    Answer yes or no.

                    Scene: {chunk.content[:500]}
                    """

                    check_result = await self.llm.generate(check_prompt, max_tokens=10)

                    if "yes" in check_result.lower():
                        occurrences.append(chunk.chunk_id)

                if occurrences:
                    motif = Motif(
                        name=theme_name,
                        category="theme",
                        occurrences=occurrences,
                        frequency=len(occurrences),
                        distribution={},
                        analysis=description
                    )
                    themes.append(motif)

        return themes
```

**Testing:**
- Test character extraction on real manuscripts
- Validate plot thread tracking accuracy
- Check motif analysis results
- Test with The Explants Volume 1

---

#### Task 13-03: Knowledge Graph Construction (4-5h)

**Goal:** Build interactive knowledge graph from extracted entities

**File:** `factory/analysis/knowledge_graph.py`

**Key Components:**

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass
class GraphNode:
    """Node in knowledge graph."""
    node_id: str
    node_type: str  # "character", "location", "motif", "theme", "event"
    name: str
    attributes: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class GraphEdge:
    """Edge in knowledge graph."""
    edge_id: str
    edge_type: str  # "relationship", "timeline", "causality", "reference"
    source_id: str
    target_id: str
    attributes: Dict[str, Any]
    weight: float = 1.0

class NovelKnowledgeGraph:
    """
    Knowledge graph for novel universe.

    Provides:
    - Visual exploration of entities and relationships
    - Query interface for finding connections
    - Export formats (JSON, GraphML, etc.)
    """

    def __init__(self, manuscript_id: str):
        self.manuscript_id = manuscript_id
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.node_counter = 0
        self.edge_counter = 0

    def add_node(
        self,
        node_type: str,
        name: str,
        attributes: Dict = None,
        metadata: Dict = None
    ) -> str:
        """Add node to graph."""
        node_id = f"{node_type}-{self.node_counter}"
        self.node_counter += 1

        node = GraphNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            attributes=attributes or {},
            metadata=metadata or {}
        )

        self.nodes[node_id] = node
        return node_id

    def add_edge(
        self,
        edge_type: str,
        source_id: str,
        target_id: str,
        attributes: Dict = None,
        weight: float = 1.0
    ) -> str:
        """Add edge to graph."""
        edge_id = f"{edge_type}-{self.edge_counter}"
        self.edge_counter += 1

        edge = GraphEdge(
            edge_id=edge_id,
            edge_type=edge_type,
            source_id=source_id,
            target_id=target_id,
            attributes=attributes or {},
            weight=weight
        )

        self.edges[edge_id] = edge
        return edge_id

    def populate_from_entities(
        self,
        characters: List[Character],
        locations: List[Location],
        plot_threads: List[PlotThread],
        motifs: List[Motif]
    ) -> None:
        """Populate graph from extracted entities."""

        # Add character nodes
        character_ids = {}
        for char in characters:
            node_id = self.add_node(
                node_type="character",
                name=char.name,
                attributes={
                    "aliases": char.aliases,
                    "traits": char.traits,
                    "psychology": char.psychology,
                    "arc_notes": char.arc_notes
                },
                metadata={
                    "first_appearance": char.first_appearance,
                    "appearances": char.appearances
                }
            )
            character_ids[char.name] = node_id

        # Add location nodes
        location_ids = {}
        for loc in locations:
            node_id = self.add_node(
                node_type="location",
                name=loc.name,
                attributes={
                    "description": loc.description,
                    "type": loc.location_type
                },
                metadata={
                    "first_appearance": loc.first_appearance,
                    "appearances": loc.appearances
                }
            )
            location_ids[loc.name] = node_id

        # Add plot thread nodes
        thread_ids = {}
        for thread in plot_threads:
            node_id = self.add_node(
                node_type="plot_thread",
                name=thread.title,
                attributes={
                    "description": thread.description,
                    "status": thread.status,
                    "priority": thread.priority
                },
                metadata={
                    "introduction": thread.introduction,
                    "developments": thread.developments,
                    "resolution": thread.resolution
                }
            )
            thread_ids[thread.title] = node_id

        # Add motif nodes
        for motif in motifs:
            node_id = self.add_node(
                node_type="motif",
                name=motif.name,
                attributes={
                    "category": motif.category,
                    "analysis": motif.analysis,
                    "frequency": motif.frequency
                },
                metadata={
                    "occurrences": motif.occurrences,
                    "distribution": motif.distribution
                }
            )

        # Add relationship edges
        for char in characters:
            char_id = character_ids[char.name]
            for other_char, relationship in char.relationships.items():
                if other_char in character_ids:
                    self.add_edge(
                        edge_type="relationship",
                        source_id=char_id,
                        target_id=character_ids[other_char],
                        attributes={"type": relationship},
                        weight=1.0
                    )

        # Add plot-character edges
        for thread in plot_threads:
            thread_id = thread_ids[thread.title]
            for char_name in thread.related_characters:
                if char_name in character_ids:
                    self.add_edge(
                        edge_type="involves",
                        source_id=thread_id,
                        target_id=character_ids[char_name],
                        attributes={"role": "participant"}
                    )

    def query(
        self,
        query_type: str,
        **params
    ) -> List[Dict]:
        """
        Query graph for specific patterns.

        Query types:
        - "neighbors": Find all nodes connected to a node
        - "path": Find path between two nodes
        - "filter": Filter nodes by attributes
        - "subgraph": Extract subgraph matching criteria
        """

        if query_type == "neighbors":
            return self._query_neighbors(params["node_id"])
        elif query_type == "path":
            return self._query_path(params["source_id"], params["target_id"])
        elif query_type == "filter":
            return self._query_filter(params)
        elif query_type == "subgraph":
            return self._query_subgraph(params)
        else:
            raise ValueError(f"Unknown query type: {query_type}")

    def _query_neighbors(self, node_id: str) -> List[Dict]:
        """Find all neighbors of a node."""
        neighbors = []

        for edge in self.edges.values():
            if edge.source_id == node_id:
                neighbor = self.nodes[edge.target_id]
                neighbors.append({
                    "node": asdict(neighbor),
                    "edge": asdict(edge),
                    "direction": "outgoing"
                })
            elif edge.target_id == node_id:
                neighbor = self.nodes[edge.source_id]
                neighbors.append({
                    "node": asdict(neighbor),
                    "edge": asdict(edge),
                    "direction": "incoming"
                })

        return neighbors

    def _query_filter(self, params: Dict) -> List[GraphNode]:
        """Filter nodes by attributes."""
        results = []

        for node in self.nodes.values():
            match = True

            for key, value in params.items():
                if key == "node_type":
                    if node.node_type != value:
                        match = False
                        break
                elif key in node.attributes:
                    if node.attributes[key] != value:
                        match = False
                        break

            if match:
                results.append(node)

        return results

    def export_json(self, output_path: Path) -> None:
        """Export graph as JSON."""
        data = {
            "manuscript_id": self.manuscript_id,
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges.values()]
        }

        output_path.write_text(json.dumps(data, indent=2))

    def export_for_visualization(self) -> Dict:
        """Export in format for D3.js visualization."""
        return {
            "nodes": [
                {
                    "id": node.node_id,
                    "label": node.name,
                    "type": node.node_type,
                    "attributes": node.attributes
                }
                for node in self.nodes.values()
            ],
            "links": [
                {
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "type": edge.edge_type,
                    "weight": edge.weight,
                    "attributes": edge.attributes
                }
                for edge in self.edges.values()
            ]
        }
```

**Storage:**
- JSON-based (simple, portable)
- Optional: Neo4j integration for complex queries
- Cache in memory for performance

**Testing:**
- Test graph construction from entities
- Test query functionality
- Test export formats
- Validate graph integrity

---

#### Task 13-04: Automated Analysis Pipeline (4-5h)

**Goal:** Run analysis skills on manuscript and aggregate results

**File:** `factory/analysis/analysis_pipeline.py`

**Key Components:**

```python
from typing import Dict, List, Any
from factory.core.skill_orchestrator import SkillOrchestrator, SkillRequest
from factory.analysis.manuscript_ingester import ManuscriptChunk

class AnalysisPipeline:
    """
    Run comprehensive analysis on manuscript.

    Coordinates:
    - Scene scoring (all scenes)
    - Character consistency checking
    - Plot hole detection
    - Pacing analysis
    - Voice authentication
    - Metaphor analysis
    """

    def __init__(self):
        self.orchestrator = SkillOrchestrator()
        self.results = {}

    async def analyze_manuscript(
        self,
        manuscript_id: str,
        chunks: List[ManuscriptChunk],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run full analysis pipeline.

        Returns:
            {
                "scene_scores": {...},
                "character_consistency": {...},
                "plot_holes": {...},
                "pacing_analysis": {...},
                "metaphor_analysis": {...},
                "priority_matrix": {...}
            }
        """

        # Scene scoring (parallel)
        scene_scores = await self._score_all_scenes(chunks, user_id)

        # Character consistency
        character_report = await self._check_character_consistency(chunks, user_id)

        # Plot hole detection
        plot_holes = await self._detect_plot_holes(chunks, user_id)

        # Pacing analysis
        pacing = await self._analyze_pacing(chunks, scene_scores)

        # Metaphor analysis
        metaphor_report = await self._analyze_metaphors(chunks, user_id)

        # Generate priority matrix
        priority_matrix = self._generate_priority_matrix(
            scene_scores,
            character_report,
            plot_holes,
            pacing,
            metaphor_report
        )

        return {
            "manuscript_id": manuscript_id,
            "scene_scores": scene_scores,
            "character_consistency": character_report,
            "plot_holes": plot_holes,
            "pacing_analysis": pacing,
            "metaphor_analysis": metaphor_report,
            "priority_matrix": priority_matrix
        }

    async def _score_all_scenes(
        self,
        chunks: List[ManuscriptChunk],
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Score all scenes in parallel."""

        # Execute scene analyzer on all chunks in parallel
        tasks = []
        for chunk in chunks:
            request = SkillRequest(
                skill_name="scene-analyzer",
                capability="analyze",
                input_data={
                    "scene_content": chunk.content,
                    "mode": "quick"  # Use quick mode for batch processing
                },
                user_id=user_id
            )
            tasks.append(self.orchestrator.execute_skill(request))

        # Wait for all results
        results = await asyncio.gather(*tasks)

        # Aggregate scores
        scores = {}
        for chunk, result in zip(chunks, results):
            if result.status == "success":
                scores[chunk.chunk_id] = {
                    "total_score": result.data["total_score"],
                    "quality_tier": result.data["quality_tier"],
                    "category_scores": result.data["category_scores"],
                    "fixes": result.data.get("fixes", [])
                }

        # Calculate statistics
        all_scores = [s["total_score"] for s in scores.values()]

        return {
            "scores": scores,
            "statistics": {
                "average": sum(all_scores) / len(all_scores) if all_scores else 0,
                "min": min(all_scores) if all_scores else 0,
                "max": max(all_scores) if all_scores else 0,
                "gold_standard": len([s for s in all_scores if s >= 95]),
                "needs_work": len([s for s in all_scores if s < 70])
            }
        }

    async def _check_character_consistency(
        self,
        chunks: List[ManuscriptChunk],
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Check character consistency across manuscript."""

        # For now, use scene analyzer results
        # Future: Dedicated character validator skill

        return {
            "status": "Not yet implemented",
            "issues": []
        }

    async def _detect_plot_holes(
        self,
        chunks: List[ManuscriptChunk],
        user_id: Optional[str]
    ) -> List[Dict]:
        """Detect plot holes and unresolved threads."""

        # This would use PlotThreadTracker results
        # Identify threads with status == "unresolved"

        return []

    async def _analyze_pacing(
        self,
        chunks: List[ManuscriptChunk],
        scene_scores: Dict
    ) -> Dict[str, Any]:
        """Analyze narrative pacing."""

        # Calculate momentum based on:
        # - Word count per scene
        # - Scene scores (quality as proxy for intensity)
        # - Scene transitions

        pacing_data = []

        for chunk in chunks:
            word_count = chunk.metadata.get("word_count", 0)
            score = scene_scores["scores"].get(chunk.chunk_id, {}).get("total_score", 0)

            # Momentum = word count × (score / 100)
            momentum = word_count * (score / 100)

            pacing_data.append({
                "chunk_id": chunk.chunk_id,
                "chapter": chunk.metadata.get("chapter", "Unknown"),
                "word_count": word_count,
                "score": score,
                "momentum": momentum
            })

        # Detect pacing issues
        issues = []

        # Check for plateaus (3+ consecutive scenes with low momentum)
        for i in range(len(pacing_data) - 2):
            if all(
                pacing_data[j]["momentum"] < 500
                for j in range(i, i + 3)
            ):
                issues.append({
                    "type": "plateau",
                    "location": f"Scenes {i+1}-{i+3}",
                    "description": "Pacing may feel slow - consider adding intensity"
                })

        return {
            "pacing_data": pacing_data,
            "issues": issues
        }

    async def _analyze_metaphors(
        self,
        chunks: List[ManuscriptChunk],
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Analyze metaphor domain distribution."""

        # This would use MotifAnalyzer results
        # Already have domain distribution from extraction

        return {
            "status": "Use MotifAnalyzer results",
            "domains": {}
        }

    def _generate_priority_matrix(
        self,
        scene_scores: Dict,
        character_report: Dict,
        plot_holes: List,
        pacing: Dict,
        metaphor_report: Dict
    ) -> Dict[str, List]:
        """
        Generate priority matrix for fixes.

        Priority levels:
        P0: Critical (plot holes, major character inconsistencies)
        P1: Important (low-scoring scenes, pacing issues)
        P2: Recommended (voice polish, metaphor balance)
        P3: Optional (minor tweaks)
        """

        priorities = {
            "P0": [],
            "P1": [],
            "P2": [],
            "P3": []
        }

        # P0: Plot holes
        for hole in plot_holes:
            priorities["P0"].append({
                "type": "plot_hole",
                "description": hole.get("description"),
                "location": hole.get("location"),
                "priority": "P0"
            })

        # P1: Low-scoring scenes
        for chunk_id, score_data in scene_scores["scores"].items():
            if score_data["total_score"] < 70:
                priorities["P1"].append({
                    "type": "low_score",
                    "description": f"Scene needs enhancement (score: {score_data['total_score']})",
                    "location": chunk_id,
                    "fixes": score_data.get("fixes", []),
                    "priority": "P1"
                })

        # P1: Pacing issues
        for issue in pacing.get("issues", []):
            priorities["P1"].append({
                "type": "pacing",
                "description": issue["description"],
                "location": issue["location"],
                "priority": "P1"
            })

        # P2: Scenes 70-84 (good but could be better)
        for chunk_id, score_data in scene_scores["scores"].items():
            if 70 <= score_data["total_score"] < 85:
                priorities["P2"].append({
                    "type": "enhancement_recommended",
                    "description": f"Scene is good but could be stronger (score: {score_data['total_score']})",
                    "location": chunk_id,
                    "fixes": score_data.get("fixes", []),
                    "priority": "P2"
                })

        return priorities
```

**Testing:**
- Test with full manuscript
- Verify parallel processing
- Check aggregation accuracy
- Test priority matrix generation

---

#### Task 13-05: Strategic Plan Generator (2-3h)

**Goal:** Generate actionable rewrite plan from analysis results

**File:** `factory/analysis/strategic_planner.py`

**Key Components:**

```python
class StrategicPlanner:
    """
    Generate strategic rewrite plan.

    Creates:
    - Prioritized action items
    - Estimated effort per fix
    - Dependencies between fixes
    - Suggested implementation order
    """

    def generate_plan(
        self,
        analysis_results: Dict[str, Any],
        manuscript_chunks: List[ManuscriptChunk]
    ) -> Dict[str, Any]:
        """Generate comprehensive rewrite plan."""

        plan = {
            "manuscript_id": analysis_results["manuscript_id"],
            "overview": self._generate_overview(analysis_results),
            "action_items": self._generate_action_items(analysis_results),
            "implementation_order": self._determine_order(analysis_results),
            "effort_estimate": self._estimate_effort(analysis_results),
            "expected_improvement": self._estimate_improvement(analysis_results)
        }

        return plan

    def _generate_overview(self, results: Dict) -> str:
        """Generate plan overview."""

        scene_stats = results["scene_scores"]["statistics"]
        priority_counts = {
            "P0": len(results["priority_matrix"]["P0"]),
            "P1": len(results["priority_matrix"]["P1"]),
            "P2": len(results["priority_matrix"]["P2"]),
            "P3": len(results["priority_matrix"]["P3"])
        }

        overview = f"""
        Manuscript Analysis Overview:

        Average Scene Score: {scene_stats['average']:.1f}/100
        Gold Standard Scenes: {scene_stats['gold_standard']}
        Needs Work: {scene_stats['needs_work']}

        Priority Issues:
        • P0 (Critical): {priority_counts['P0']} issues
        • P1 (Important): {priority_counts['P1']} issues
        • P2 (Recommended): {priority_counts['P2']} issues
        • P3 (Optional): {priority_counts['P3']} issues

        Estimated rewrite time: {self._estimate_effort(results)['total_hours']} hours
        Expected score improvement: +{self._estimate_improvement(results)} points average
        """

        return overview.strip()

    def _generate_action_items(self, results: Dict) -> List[Dict]:
        """Generate specific action items."""

        items = []

        # Add all priority items with detailed instructions
        for priority_level in ["P0", "P1", "P2", "P3"]:
            for item in results["priority_matrix"][priority_level]:
                action_item = {
                    "id": f"action-{len(items)}",
                    "priority": priority_level,
                    "type": item["type"],
                    "description": item["description"],
                    "location": item["location"],
                    "specific_fixes": item.get("fixes", []),
                    "effort_estimate": self._estimate_item_effort(item),
                    "status": "pending"
                }
                items.append(action_item)

        return items

    def _determine_order(self, results: Dict) -> List[str]:
        """Determine implementation order for fixes."""

        # Order by priority, then by dependencies
        # P0 first (plot holes must be fixed before everything)
        # Then P1 (major issues)
        # Then P2 and P3

        order = []

        for priority in ["P0", "P1", "P2", "P3"]:
            items = results["priority_matrix"][priority]
            order.extend([item.get("location") for item in items])

        return order

    def _estimate_effort(self, results: Dict) -> Dict[str, Any]:
        """Estimate total effort required."""

        total_hours = 0
        breakdown = {}

        for priority in ["P0", "P1", "P2", "P3"]:
            items = results["priority_matrix"][priority]
            hours = sum(self._estimate_item_effort(item) for item in items)
            total_hours += hours
            breakdown[priority] = hours

        return {
            "total_hours": total_hours,
            "breakdown": breakdown,
            "estimated_sessions": (total_hours // 4) + 1  # Assuming 4-hour sessions
        }

    def _estimate_item_effort(self, item: Dict) -> float:
        """Estimate hours for single item."""

        # Base estimates by type
        effort_map = {
            "plot_hole": 4.0,  # Requires new scene or major revision
            "low_score": 2.0,  # Scene enhancement
            "pacing": 3.0,  # May require structural changes
            "enhancement_recommended": 1.0,  # Polish pass
            "character_inconsistency": 2.5,
            "voice_issue": 1.5
        }

        return effort_map.get(item["type"], 1.0)

    def _estimate_improvement(self, results: Dict) -> float:
        """Estimate expected score improvement."""

        # Based on number and priority of issues
        current_avg = results["scene_scores"]["statistics"]["average"]

        # Each P0 fix: +2 points average
        # Each P1 fix: +1 point average
        # Each P2 fix: +0.5 points average

        p0_improvement = len(results["priority_matrix"]["P0"]) * 2
        p1_improvement = len(results["priority_matrix"]["P1"]) * 1
        p2_improvement = len(results["priority_matrix"]["P2"]) * 0.5

        total_improvement = p0_improvement + p1_improvement + p2_improvement

        # Cap at realistic maximum (95 - current)
        max_improvement = 95 - current_avg

        return min(total_improvement, max_improvement)
```

**Testing:**
- Test plan generation with various scenarios
- Validate effort estimates
- Check ordering logic
- Test improvement predictions

---

### Phase B: Interactive Exploration UI (10-12h)

#### Task 13-06: Knowledge Graph Visualization (5-6h)

**Goal:** Interactive graph viewer in UI

**File:** `webapp/frontend-v2/src/features/analysis/GraphVisualization.jsx`

**Uses:** D3.js or React Flow for graph rendering

**Key Features:**
- Node rendering (different colors for types)
- Edge rendering (arrows, labels)
- Zoom and pan
- Click to select node
- Hover for details
- Filter by node type
- Search nodes
- Export as image

**Component:**

```jsx
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export function GraphVisualization({ graphData, onNodeClick }) {
  const svgRef = useRef();
  const [selectedNode, setSelectedNode] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    if (!graphData) return;

    // D3.js force-directed graph
    const svg = d3.select(svgRef.current);
    const width = 1200;
    const height = 800;

    // Clear existing
    svg.selectAll("*").remove();

    // Create simulation
    const simulation = d3.forceSimulation(graphData.nodes)
      .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Add links
    const link = svg.append("g")
      .selectAll("line")
      .data(graphData.links)
      .enter().append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", d => Math.sqrt(d.weight));

    // Add nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(graphData.nodes)
      .enter().append("circle")
      .attr("r", 8)
      .attr("fill", d => getNodeColor(d.type))
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
      .on("click", (event, d) => {
        setSelectedNode(d);
        onNodeClick?.(d);
      });

    // Add labels
    const label = svg.append("g")
      .selectAll("text")
      .data(graphData.nodes)
      .enter().append("text")
      .text(d => d.label)
      .attr("font-size", 10)
      .attr("dx", 12)
      .attr("dy", 4);

    // Update positions on tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    function getNodeColor(type) {
      const colors = {
        character: '#4A90E2',
        location: '#7ED321',
        plot_thread: '#F5A623',
        motif: '#BD10E0',
        theme: '#50E3C2'
      };
      return colors[type] || '#999';
    }

  }, [graphData, filter]);

  return (
    <div className="graph-visualization">
      <div className="controls">
        <select value={filter} onChange={e => setFilter(e.target.value)}>
          <option value="all">All Nodes</option>
          <option value="character">Characters Only</option>
          <option value="location">Locations Only</option>
          <option value="plot_thread">Plot Threads Only</option>
        </select>
      </div>

      <svg ref={svgRef} width={1200} height={800} />

      {selectedNode && (
        <div className="node-details">
          <h3>{selectedNode.label}</h3>
          <p>Type: {selectedNode.type}</p>
          <pre>{JSON.stringify(selectedNode.attributes, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

**Testing:**
- Test with various graph sizes
- Test interactions (drag, zoom, click)
- Test performance with 100+ nodes
- Test filtering

---

#### Task 13-07: Natural Language Query Interface (3-4h)

**Goal:** Allow users to query their novel using natural language

**File:** `webapp/frontend-v2/src/features/analysis/QueryInterface.jsx`

**Example Queries:**
- "Show me all scenes with Mickey and Noni"
- "Track casino metaphor usage across chapters"
- "Find unresolved plot threads"
- "Which characters appear in quantum space?"
- "Show me the character arc for Trevor"

**Component:**

```jsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

export function QueryInterface({ manuscriptId, onResults }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);

  const queryMutation = useMutation({
    mutationFn: async (query) => {
      const res = await fetch('/api/analysis/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          manuscript_id: manuscriptId,
          query: query
        })
      });
      return res.json();
    },
    onSuccess: (data) => {
      setResults(data);
      onResults?.(data);
    }
  });

  const exampleQueries = [
    "Show me all scenes with [character name]",
    "Track [motif/theme] across chapters",
    "Find unresolved plot threads",
    "Which characters appear in [location]?",
    "Show character arc for [character name]",
    "What's the pacing in Act II?",
    "List all casino metaphors"
  ];

  return (
    <div className="query-interface">
      <h3>Ask About Your Novel</h3>

      <div className="query-input">
        <textarea
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask anything about your novel..."
          rows={3}
        />
        <button
          onClick={() => queryMutation.mutate(query)}
          disabled={!query || queryMutation.isLoading}
        >
          {queryMutation.isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="example-queries">
        <strong>Try these:</strong>
        {exampleQueries.map((ex, i) => (
          <button
            key={i}
            onClick={() => setQuery(ex)}
            className="example-query"
          >
            {ex}
          </button>
        ))}
      </div>

      {results && (
        <div className="query-results">
          <h4>Results ({results.count})</h4>

          {results.type === 'scenes' && (
            <div className="scene-results">
              {results.items.map(scene => (
                <div key={scene.id} className="scene-card">
                  <h5>{scene.title}</h5>
                  <p>{scene.excerpt}</p>
                  <button onClick={() => onResults?.(scene)}>
                    View Scene
                  </button>
                </div>
              ))}
            </div>
          )}

          {results.type === 'graph_nodes' && (
            <div className="node-results">
              {results.items.map(node => (
                <div key={node.id} className="node-card">
                  <h5>{node.name}</h5>
                  <p>Type: {node.type}</p>
                  <pre>{JSON.stringify(node.attributes, null, 2)}</pre>
                </div>
              ))}
            </div>
          )}

          {results.type === 'analysis' && (
            <div className="analysis-results">
              <p>{results.summary}</p>
              <div className="data-visualization">
                {/* Chart or graph based on analysis */}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

**Backend Endpoint:**

```python
@app.post("/api/analysis/query")
async def query_manuscript(request: dict):
    """
    Natural language query interface.

    Uses LLM to parse query → translate to graph query → return results
    """
    manuscript_id = request["manuscript_id"]
    query = request["query"]

    # Load knowledge graph
    graph = load_graph(manuscript_id)

    # Parse query with LLM
    llm = get_llm_provider()

    parse_prompt = f"""
    Parse this natural language query about a novel into a structured query.

    Query: {query}

    Return JSON format:
    {{
        "query_type": "find_scenes" | "track_motif" | "character_arc" | "plot_threads" | "filter_nodes",
        "parameters": {{...}}
    }}
    """

    parsed = await llm.generate(parse_prompt)
    query_struct = json.loads(parsed)

    # Execute structured query on graph
    results = graph.query(
        query_type=query_struct["query_type"],
        **query_struct["parameters"]
    )

    # Format results
    if query_struct["query_type"] == "find_scenes":
        return {
            "type": "scenes",
            "count": len(results),
            "items": results
        }
    elif query_struct["query_type"] == "filter_nodes":
        return {
            "type": "graph_nodes",
            "count": len(results),
            "items": [node_to_dict(n) for n in results]
        }
    # ... other types
```

**Testing:**
- Test various query types
- Test query parsing accuracy
- Test results formatting
- Test performance

---

#### Task 13-08: Analysis Dashboard (2-3h)

**Goal:** Overview dashboard showing all analysis results

**File:** `webapp/frontend-v2/src/features/analysis/AnalysisDashboard.jsx`

**Displays:**
- Scene scores overview (chart)
- Character consistency matrix
- Pacing heatmap
- Metaphor domain distribution (pie chart)
- Priority issues list
- Strategic plan summary

**Component:**

```jsx
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, PieChart, Pie, Heatmap } from 'recharts';

export function AnalysisDashboard({ manuscriptId }) {
  const { data: analysis } = useQuery(['manuscript-analysis', manuscriptId],
    () => fetch(`/api/analysis/${manuscriptId}`).then(r => r.json())
  );

  if (!analysis) return <div>Loading analysis...</div>;

  return (
    <div className="analysis-dashboard">
      <h2>Novel Analysis Dashboard</h2>

      {/* Scene Scores Overview */}
      <div className="widget scene-scores">
        <h3>Scene Quality</h3>
        <div className="stats">
          <div className="stat">
            <strong>Average Score:</strong>
            <span className="value">{analysis.scene_scores.statistics.average}/100</span>
          </div>
          <div className="stat">
            <strong>Gold Standard:</strong>
            <span className="value">{analysis.scene_scores.statistics.gold_standard} scenes</span>
          </div>
          <div className="stat">
            <strong>Needs Work:</strong>
            <span className="value">{analysis.scene_scores.statistics.needs_work} scenes</span>
          </div>
        </div>

        <BarChart width={600} height={300} data={formatScoreDistribution(analysis)}>
          <Bar dataKey="count" fill="#4A90E2" />
        </BarChart>
      </div>

      {/* Priority Issues */}
      <div className="widget priority-issues">
        <h3>Priority Issues</h3>
        <div className="priority-grid">
          <div className="priority-cell p0">
            <strong>P0 Critical:</strong> {analysis.priority_matrix.P0.length}
          </div>
          <div className="priority-cell p1">
            <strong>P1 Important:</strong> {analysis.priority_matrix.P1.length}
          </div>
          <div className="priority-cell p2">
            <strong>P2 Recommended:</strong> {analysis.priority_matrix.P2.length}
          </div>
          <div className="priority-cell p3">
            <strong>P3 Optional:</strong> {analysis.priority_matrix.P3.length}
          </div>
        </div>

        <div className="issue-list">
          {analysis.priority_matrix.P0.slice(0, 5).map((issue, i) => (
            <div key={i} className="issue">
              <span className="badge p0">P0</span>
              <span className="description">{issue.description}</span>
              <button onClick={() => viewIssue(issue)}>View</button>
            </div>
          ))}
        </div>
      </div>

      {/* Pacing Heatmap */}
      <div className="widget pacing">
        <h3>Narrative Pacing</h3>
        <PacingHeatmap data={analysis.pacing_analysis} />
      </div>

      {/* Metaphor Distribution */}
      <div className="widget metaphors">
        <h3>Metaphor Domains</h3>
        <PieChart width={400} height={300}>
          <Pie
            data={formatMetaphorData(analysis)}
            dataKey="value"
            nameKey="name"
            fill="#8884d8"
          />
        </PieChart>
      </div>

      {/* Strategic Plan Summary */}
      <div className="widget strategic-plan">
        <h3>Strategic Rewrite Plan</h3>
        <pre>{analysis.strategic_plan?.overview}</pre>
        <button onClick={() => viewFullPlan(analysis.strategic_plan)}>
          View Full Plan
        </button>
      </div>
    </div>
  );
}
```

**Testing:**
- Test with real analysis data
- Test all visualizations
- Test interactions
- Test responsive design

---

## 🧪 Testing Strategy

### Unit Tests

**Entity Extractors:**
```python
async def test_character_extraction():
    text = """
    Mickey Bardot stood in the lobby.
    Noni approached with practiced ease.
    "The CIA wants you," she said.
    """

    extractor = CharacterExtractor()
    names = await extractor._identify_names([
        ManuscriptChunk(chunk_id="test", chunk_type="scene", content=text, metadata={})
    ])

    assert "Mickey" in names or "Mickey Bardot" in names
    assert "Noni" in names
```

**Knowledge Graph:**
```python
def test_graph_construction():
    graph = NovelKnowledgeGraph("test-manuscript")

    char_id = graph.add_node("character", "Mickey", {"traits": ["cynical"]})
    loc_id = graph.add_node("location", "Vegas", {})

    graph.add_edge("appears_in", char_id, loc_id)

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
```

### Integration Tests

**Full Pipeline:**
```python
async def test_full_analysis_pipeline():
    # Load test manuscript
    ingester = ManuscriptIngester()
    manuscript = await ingester.ingest("test_novel.docx")

    # Run extraction
    extractor = CharacterExtractor()
    characters = await extractor.extract(manuscript["chunks"])

    assert len(characters) > 0

    # Build graph
    graph = NovelKnowledgeGraph(manuscript["manuscript_id"])
    graph.populate_from_entities(characters, [], [], [])

    assert len(graph.nodes) == len(characters)

    # Run analysis pipeline
    pipeline = AnalysisPipeline()
    results = await pipeline.analyze_manuscript(
        manuscript["manuscript_id"],
        manuscript["chunks"]
    )

    assert "scene_scores" in results
    assert "priority_matrix" in results
```

### Validation Tests

**Test with The Explants Volume 1:**
```python
async def test_explants_volume_1():
    # Load actual manuscript
    project_path = Path("/path/to/explants/volume1")

    ingester = ManuscriptIngester()
    manuscript = await ingester.ingest(project_path)

    # Should have 136 scenes
    assert len(manuscript["chunks"]) == 136

    # Run character extraction
    extractor = CharacterExtractor()
    characters = await extractor.extract(manuscript["chunks"])

    # Should find main characters
    char_names = [c.name for c in characters]
    assert "Mickey" in char_names
    assert "Noni" in char_names
    assert "Trevor" in char_names

    # Run full analysis
    pipeline = AnalysisPipeline()
    results = await pipeline.analyze_manuscript(
        manuscript["manuscript_id"],
        manuscript["chunks"]
    )

    # Verify scene scores
    assert results["scene_scores"]["statistics"]["average"] > 0

    # Check for known issues
    # (We know Act II has casino saturation)
    metaphor_report = results["metaphor_analysis"]
    # Assert casino domain is flagged
```

---

## 📚 Documentation

### User Guide: NOVEL_ANALYSIS_GUIDE.md

**Contents:**
- How to upload your manuscript
- Understanding the analysis results
- Reading the knowledge graph
- Using natural language queries
- Interpreting the strategic plan
- Best practices for revisions

### Developer Guide: ANALYSIS_SYSTEM_ARCHITECTURE.md

**Contents:**
- System overview
- Entity extraction pipelines
- Knowledge graph design
- Analysis algorithms
- Adding new extractors
- Extending the system

### API Reference: ANALYSIS_API.md

**Contents:**
- All analysis endpoints
- Request/response formats
- Query language syntax
- Rate limits and quotas
- Error codes

---

## 🎯 Success Criteria

### Sprint 13 Complete When:

**Phase A:**
- [ ] Can upload manuscript (DOCX, PDF, Markdown)
- [ ] Extracts characters, locations, plot threads, motifs
- [ ] Builds knowledge graph from entities
- [ ] Runs automated analysis (scene scores, plot holes, pacing)
- [ ] Generates strategic rewrite plan
- [ ] All analysis results stored and accessible

**Phase B:**
- [ ] Knowledge graph visualization works
- [ ] Can query novel with natural language
- [ ] Analysis dashboard displays all metrics
- [ ] Can export results and graphs
- [ ] Performance acceptable (< 5 minutes for 100k word novel)

**Overall:**
- [ ] Can analyze The Explants Volume 1 successfully
- [ ] Identifies known issues (Act II casino saturation, etc.)
- [ ] Generates useful strategic plan
- [ ] Students can use system for their novels
- [ ] UI is intuitive and beautiful

---

## 💰 Monetization Strategy

### Pricing Tiers

**Free Tier:**
- 1 manuscript analysis per month
- Up to 50,000 words
- Basic analysis (scene scores, character list)
- Limited queries (10 per month)

**Standard: $19/month**
- Unlimited analyses
- Up to 100,000 words per manuscript
- Full analysis (everything)
- Unlimited queries
- Export reports (PDF, JSON)
- Priority processing

**Pro: $49/month**
- Unlimited analyses
- Unlimited words
- Series tracking (multiple books)
- Advanced features (custom skills)
- API access
- Priority support

**Enterprise: $199/month**
- Everything in Pro
- Team collaboration (5 users)
- White-label option
- Custom integrations
- Dedicated support

### Add-ons

- **Deep Dive Analysis: $29 one-time**
  - Human editor review of AI analysis
  - Personalized recommendations
  - 30-minute consultation call

- **Series Continuity Check: $49 one-time**
  - Analyze 3+ books for continuity
  - Cross-book character tracking
  - Theme progression analysis

### B2B Sales

**Publishers: $999/month**
- Analyze submissions
- Quick quality assessment
- Standardized feedback

**Writing Programs: $499/month**
- Unlimited student analyses
- Instructor dashboard
- Cohort tracking

**Writing Coaches: $199/month**
- Analyze client manuscripts
- Generate feedback reports
- Track progress over time

---

## 🚀 Launch Plan

### Phase 1: Alpha (G.C. Harris + 2-3 Users)

**Week 1:**
- Analyze The Explants Volume 1
- Validate results against known issues
- Fix critical bugs

**Week 2:**
- Invite 2-3 beta users (writer friends)
- Collect detailed feedback
- Iterate on UX

### Phase 2: Beta (50-100 Users)

**Month 1:**
- Soft launch to writing community
- Free tier for all beta users
- Monitor performance and costs
- Fix bugs and improve UX

**Month 2:**
- Add paid tiers
- Marketing push (writing forums, Twitter)
- Collect testimonials
- Refine features based on feedback

### Phase 3: Public Launch

**Month 3:**
- Full public launch
- PR push (writing blogs, podcasts)
- Partnerships with writing programs
- Affiliate program for writing coaches

**Month 4-6:**
- Scale infrastructure
- Add advanced features
- Build B2B sales pipeline
- International expansion

---

## 🔮 Future Enhancements

**Sprint 14: Advanced Analysis**
- Comp title analysis (compare to bestsellers)
- Genre convention checking
- Market fit scoring
- Audience targeting recommendations

**Sprint 15: Collaborative Features**
- Multi-user projects
- Critique partner tools
- Annotation and commenting
- Version comparison

**Sprint 16: AI-Assisted Rewriting**
- Apply strategic plan automatically
- Generate scene alternatives
- Suggest dialogue improvements
- Intelligent scene stitching

**Sprint 17: Series Intelligence**
- Track continuity across 3-10 books
- Character progression over series
- World-building consistency
- Plot thread management

**Sprint 18: Market Intelligence**
- Comp title database
- Genre trend analysis
- Success predictors
- Publisher matching

---

## 🎉 The Revolutionary Impact

After Sprint 13, Writers Factory becomes:

✅ **Scrivener** - File management ✓
✅ **VS Code** - Clean editing ✓
✅ **NotebookLM** - Research queries ✓
✅ **Your 6 Explants Skills** - Craft mastery ✓
✅ **Novel Intelligence System** - AI Story Bible ← **NEW**

**For Authors:**
- Upload draft → Get professional analysis
- Strategic plan → Know exactly what to fix
- Knowledge graph → Explore your universe
- Natural language queries → Find anything instantly

**For The Explants Volume 2:**
- Analyze Volume 1 → Perfect continuity
- Track all entities → No forgotten subplots
- Query system → "What's unresolved from V1?"
- Strategic plan → Focus on what matters

**For Students:**
- Learn by seeing AI dissect story
- Get professional feedback (free/$19)
- Track improvement over revisions
- Build portfolio of analyzed work

**For The Business:**
- $3-21M revenue potential (Year 1-3)
- Sticky product (authors return for each book)
- Viral growth (writers share results)
- B2B opportunities (publishers, schools, coaches)

---

## 💬 Prompt for Cloud Agent

```
Sprint 13: Novel Intelligence System

Please implement the complete specification in SPRINT_13_NOVEL_INTELLIGENCE_SYSTEM.md

This sprint builds on Sprint 12's skill orchestration system to create an
AI-powered novel analysis and knowledge graph system.

PHASE A - Core Pipeline (15-20h):
1. Manuscript Ingestion - Parse DOCX/PDF/Markdown/existing projects
2. Entity Extraction - Characters, locations, plots, motifs, themes
3. Knowledge Graph Construction - Build interactive graph
4. Automated Analysis - Scene scoring, plot holes, pacing
5. Strategic Plan Generation - Prioritized rewrite plan

PHASE B - Interactive UI (10-12h):
6. Graph Visualization - D3.js interactive graph
7. Natural Language Queries - Ask anything about your novel
8. Analysis Dashboard - Charts, metrics, insights

CRITICAL REQUIREMENTS:
- Test with The Explants Volume 1 (136 scenes)
- Validate accuracy of entity extraction
- Knowledge graph must be queryable
- Analysis must produce actionable insights
- UI must be beautiful and intuitive

TESTING:
- Unit tests for all extractors
- Integration tests for full pipeline
- Validation with real manuscript
- Performance testing (< 5 min for 100k words)

This is THE killer feature that makes Writers Factory revolutionary.

Begin with Task 13-01 (Manuscript Ingestion).
```

---

**Ready to build the future of novel writing? Let's revolutionize revision! 🚀📚✨**
