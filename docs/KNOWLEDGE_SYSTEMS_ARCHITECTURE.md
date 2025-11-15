# Knowledge Systems Architecture: NotebookLM vs Knowledge Graph

**Date:** November 15, 2025
**Author:** Architectural Analysis
**Status:** Current State + Sprint 15 Vision

---

## Executive Summary

Writers Factory has **TWO knowledge systems** serving different purposes:

1. **NotebookLM** - External, user-curated knowledge base (research, ideas, reference)
2. **Knowledge Graph** - Internal, AI-extracted story intelligence (automated continuity tracking)

**Current Reality:** Only partial integration exists
**Sprint 15 Vision:** Add bidirectional flow between both systems
**Your Practice:** Multiple notebooks with specialized purposes (EXCELLENT architectural intuition!)

---

## Question 1: NotebookLM Pipeline - Current vs. Desired

### Current Implementation (Sprint 14)

**Single Notebook Model:**
```
User Setup Flow:
1. User provides NotebookLM URL(s) during project creation
2. System queries notebook with 5 predefined questions:
   - Character summaries
   - Story world/settings
   - Plot threads/themes
   - Voice characteristics
   - Metaphors/motifs
3. Results become "NotebookLM Context" (read-only string)
4. Used for skill generation only
```

**Code Location:** `factory/integrations/notebooklm_setup.py`

**Methods:**
- `extract_project_knowledge()` - General extraction (5 queries)
- `extract_voice_context()` - Voice-specific (3 queries)
- `extract_character_context()` - Character-specific (3 queries)
- `extract_world_context()` - World-building (3 queries)

**Limitation:** One-time extraction at setup. No ongoing updates.

### Your Multi-Notebook Practice (SMART!)

You described:
> "One notebook keeps those ideas for creative flashes, and world building and plot development, but there are other notebooks which save documents on specific things like characters or previous and future chapters acts structure, etc."

**Your Architecture:**
1. **Ideas Notebook** - Creative flashes, world-building brainstorms, plot concepts
2. **Character Notebook** - Character profiles, backstories, voice samples
3. **Structure Notebook** - Chapter outlines, acts, structure notes
4. **[Other specialized notebooks]** - Various domains

**Why This is Better:**
- ✅ Separation of concerns (cleaner queries)
- ✅ Domain-specific optimization
- ✅ Easier to update specific knowledge areas
- ✅ Prevents query overload (NotebookLM performs better with focused queries)

### Proposed Sprint 15+ Architecture

**Multi-Notebook System with Ongoing Sync:**

```python
# New data structure in project config
project_notebooks = {
    "ideas": {
        "url": "https://notebooklm.google.com/notebook/abc123",
        "purpose": "creative_flashes_worldbuilding",
        "sync_frequency": "weekly",
        "queries": [
            "What new world-building ideas have been added?",
            "Any plot developments or twists?"
        ]
    },
    "characters": {
        "url": "https://notebooklm.google.com/notebook/def456",
        "purpose": "character_profiles",
        "sync_frequency": "on_demand",
        "queries": [
            "List all character profiles with updates.",
            "Any new character relationships or arcs?"
        ]
    },
    "structure": {
        "url": "https://notebooklm.google.com/notebook/ghi789",
        "purpose": "plot_structure",
        "sync_frequency": "on_demand",
        "queries": [
            "What is the current chapter outline?",
            "Any structural changes to acts or sequences?"
        ]
    }
}
```

**Benefits:**
- Each notebook queried with domain-specific questions
- Sync on-demand (manual trigger) or scheduled (weekly)
- Modular updates (update character knowledge without re-querying world-building)
- Matches your existing workflow!

---

## Question 2: Can NotebookLM MCP Server Push/Create Notebooks?

### Current Capabilities (Read-Only)

**NotebookLM Client** (`factory/research/notebooklm_client.py`):
- ✅ `authenticate()` - One-time Google login via browser automation
- ✅ `query(question, notebook_url)` - Query existing notebook
- ✅ `_extract_citations()` - Get source references
- ❌ **NO write/create capabilities**

**Technical Constraint:**
NotebookLM has **NO official API**. Our client uses **Playwright browser automation** to:
1. Open notebook URL in headless browser
2. Type question into chat interface
3. Wait for response
4. Scrape answer text and citations

**Why No Write Access (Currently):**
Browser automation is fragile for read operations, **extremely fragile** for write operations:
- Creating notebooks requires UI navigation (unreliable selectors)
- Adding sources requires file upload (complex automation)
- No way to verify write success
- High failure rate (UI changes break automation)

### Theoretical Write Capabilities (Risky)

**Technically possible but NOT recommended for production:**

```python
# FRAGILE - Not recommended
async def create_notebook(self, notebook_name: str) -> str:
    """Create new NotebookLM notebook via browser automation."""
    # Navigate to NotebookLM home
    # Click "New Notebook" button
    # Enter notebook name
    # Wait for creation
    # Return notebook URL
    # BUT: Any UI change breaks this!
```

**Why This is Problematic:**
1. NotebookLM UI changes frequently (Google product)
2. No way to verify creation succeeded
3. Race conditions (async operations)
4. Error recovery is nearly impossible
5. Rate limiting / detection as bot

### Better Alternative: Hybrid Approach

**Recommendation:**

**Phase 1 (Sprint 15): Read-Only Multi-Notebook**
- User manually creates notebooks in NotebookLM
- User provides URLs to Writers Factory
- System queries each notebook with domain-specific questions
- Perfect reliability, matches your current practice

**Phase 2 (Future): NotebookLM Export/Import**
- Writers Factory exports knowledge TO markdown/JSON
- User manually uploads to NotebookLM (drag & drop)
- No automation brittleness
- User maintains control

**Phase 3 (If Official API Released):**
- Use official NotebookLM API for bidirectional sync
- Safe, reliable, supported

### What You CAN Push (Immediately)

**Writers Factory → Local Files → User Uploads:**

```python
# Export knowledge graph to markdown for NotebookLM upload
async def export_knowledge_for_notebooklm(
    project_id: str,
    knowledge_type: str  # "characters", "plot", "world"
) -> Path:
    """
    Export knowledge graph data as markdown files
    that user can upload to NotebookLM.

    Returns:
        Path to generated markdown file
    """
    # Example for characters:
    # ## Character: Mickey Bardot
    # - Traits: Enhanced consciousness, tactical mind
    # - Arc: From observer to active participant
    # - Relationships: ...

    return output_path
```

**User Workflow:**
1. Click "Export Characters to NotebookLM" in UI
2. Download `characters_export.md`
3. Open NotebookLM Characters notebook
4. Upload `characters_export.md`
5. Knowledge now queryable in NotebookLM!

**Benefits:**
- ✅ No fragile automation
- ✅ User control
- ✅ Reliable
- ✅ Bidirectional flow (just not automatic)

---

## Question 3: Knowledge Graph - Current State & Vision

### Current Implementation (Sprint 13)

**Knowledge Graph** (`factory/analysis/knowledge_graph.py`):

**Purpose:** Internal story intelligence extracted from manuscript

**Data Model:**
```python
class GraphNode:
    node_id: str         # "character-0", "location-5"
    node_type: str       # "character", "location", "plot_thread", "motif"
    name: str            # "Mickey Bardot", "The Hotel"
    attributes: Dict     # Traits, descriptions, arc notes
    metadata: Dict       # First appearance, frequency

class GraphEdge:
    edge_id: str         # "relationship-12"
    edge_type: str       # "relationship", "appears_at", "participates_in"
    source_id: str       # "character-0"
    target_id: str       # "location-5"
    attributes: Dict     # Relationship type, shared scenes
    weight: float        # Connection strength (0.0-1.0)
```

**Population Methods:**
```python
graph = NovelKnowledgeGraph(manuscript_id="explants-v1")

# Populated from extracted entities (Sprint 13 extraction agents)
graph.populate_from_entities(
    characters=[...],     # From CharacterExtractor
    locations=[...],      # From LocationExtractor
    plot_threads=[...],   # From PlotThreadTracker
    motifs=[...]          # From MotifAnalyzer
)

# Query connections
graph.query_connections(node_id="character-0", max_depth=2)

# Export to JSON
graph.export_json(output_path="knowledge_graph.json")
```

**When It Gets Built:**
According to Sprint 13 spec, knowledge graph is populated by:
1. **Manuscript Ingestion** - Parse DOCX/PDF into scenes
2. **Entity Extraction** - 6 parallel agents extract entities
3. **Graph Construction** - Entities → nodes, relationships → edges
4. **Storage** - JSON export (no live database yet)

**Current Usage:**
- Character depth analysis (Sprint 5)
- Continuity checking
- Plot hole detection
- Export to JSON for visualization

**Limitation:** Built once at manuscript analysis time. Not continuously updated as you write.

### Vision: Ongoing Knowledge Graph Updates

**What SHOULD Happen:**

```python
# Every time user writes/edits a scene
async def update_knowledge_graph_from_scene(
    project_id: str,
    scene_id: str,
    scene_text: str
):
    """
    Update knowledge graph with new information from scene.

    Process:
    1. Extract entities from new scene (mini extraction)
    2. Add new nodes (new characters, locations)
    3. Update existing nodes (character development)
    4. Add new edges (new relationships)
    5. Update edge weights (relationship strengthening)
    """

    # Extract from scene
    new_entities = await extract_entities_from_scene(scene_text)

    # Load existing graph
    graph = load_knowledge_graph(project_id)

    # Merge new knowledge
    for char in new_entities.characters:
        if char.name not in graph.get_character_names():
            graph.add_character_node(char)
        else:
            graph.update_character_node(char)

    # Save updated graph
    save_knowledge_graph(project_id, graph)
```

**Triggers:**
- ✅ Scene save
- ✅ Scene edit
- ✅ Manual "Refresh Knowledge" button
- ✅ Nightly batch update

### What You Want (Querying While Writing)

> "The original idea was that ongoing information being created would be thrown into this knowledge graph and could be queried for things as one was writing."

**Perfect Use Case:**

```python
# While writing Scene 47
User: "Has Mickey ever been to The Chronicler's hotel before this scene?"

# System queries knowledge graph
graph.query_connections(
    node_id="character-mickey",
    filter_edge_type="appears_at",
    target_filter="location-hotel"
)

# Returns:
{
    "answer": "Yes, Mickey appeared at The Hotel in 3 previous scenes:",
    "scenes": [
        {"scene_id": "scene-12", "chapter": "Chapter 2", "summary": "..."},
        {"scene_id": "scene-23", "chapter": "Chapter 5", "summary": "..."},
        {"scene_id": "scene-31", "chapter": "Chapter 7", "summary": "..."}
    ]
}
```

**Current Gap:** Knowledge graph exists but:
- ❌ Not updated incrementally (only built at analysis time)
- ❌ No query interface exposed to user during writing
- ❌ Not integrated with scene writing workflow

**Sprint 15+ Fix:**
Add incremental update + query interface.

---

## Bidirectional Flow: NotebookLM ↔ Knowledge Graph

### Current Reality (One-Way Flow)

```
NotebookLM (Ideas, Research)
         ↓
   [One-time extraction]
         ↓
Project Setup (Skill Generation)
         ↓
   [User writes scenes]
         ↓
Knowledge Graph (Extracted Entities)
         ↓
   [Analysis & Reports]
         ↓
   [DEAD END - No feedback loop]
```

### Desired Architecture (Two-Way Flow)

```
┌─────────────────────────────────────────────────────┐
│  NotebookLM (External, User-Curated)                │
│  - Ideas notebook (world-building, plot ideas)      │
│  - Character notebook (profiles, backstories)       │
│  - Structure notebook (chapter outlines)            │
└───────────┬─────────────────────────────────────────┘
            │
            │ ┌───── Initial Setup (Sprint 14) ──────┐
            ├─┤ Extract domain-specific knowledge     │
            │ └──────────────────────────────────────┘
            │
            │ ┌───── Ongoing Sync (Sprint 15+) ──────┐
            ├─┤ Query "What's new since last sync?"  │
            │ │ Update project context               │
            │ └──────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────────┐
│  Writers Factory Project                            │
│  - Voice Profile                                    │
│  - Custom Skills (6 skills)                         │
│  - NotebookLM Context (read-only knowledge)         │
└───────────┬─────────────────────────────────────────┘
            │
            │ ┌───── Writing Process ────────────────┐
            ├─┤ User writes scenes                   │
            │ │ Scenes analyzed/enhanced by skills   │
            │ └──────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────────┐
│  Knowledge Graph (Internal, AI-Extracted)           │
│  - Nodes: Characters, locations, plot threads       │
│  - Edges: Relationships, timeline, causality        │
│  - Continuously updated from written scenes         │
└───────────┬─────────────────────────────────────────┘
            │
            │ ┌───── Real-Time Queries (Sprint 15+) ─┐
            ├─┤ "Has Mickey been here before?"       │
            │ │ "What plot threads are unresolved?"  │
            │ │ "Show me all scenes with quantum"    │
            │ └──────────────────────────────────────┘
            │
            │ ┌───── Export Back to NotebookLM ──────┐
            ├─┤ Generate markdown summaries          │
            │ │ User uploads to NotebookLM           │
            │ │ Knowledge loop closes!               │
            │ └──────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────────┐
│  NotebookLM (Updated with actual manuscript data)   │
│  - Character notebook now has extracted traits      │
│  - Structure notebook has actual scene breakdown    │
│  - Plot notebook has identified threads             │
└─────────────────────────────────────────────────────┘
```

### Information Flow Details

**NotebookLM → Writers Factory:**

1. **Initial Setup (Sprint 14):**
   - User provides notebook URLs
   - System queries: characters, world, voice, plot, themes
   - Generates custom skills from knowledge
   - Creates initial project context

2. **Ongoing Sync (Sprint 15+):**
   - User adds new ideas to Ideas notebook
   - User clicks "Sync NotebookLM Knowledge"
   - System queries "What's new since [last_sync_date]?"
   - Updates project context with new information
   - Optionally: Re-generates skills if voice/style changed

**Writers Factory → Knowledge Graph:**

1. **Manuscript Analysis (Sprint 13):**
   - User uploads complete manuscript
   - 6 extraction agents run in parallel
   - Populates knowledge graph with entities
   - One-time comprehensive build

2. **Incremental Updates (Sprint 15+):**
   - User saves new scene
   - Mini extraction on just that scene
   - Add new nodes (new characters/locations)
   - Update existing nodes (character development)
   - Add/update edges (new relationships)

**Knowledge Graph → NotebookLM:**

1. **Export Summaries (Sprint 15+):**
   - User clicks "Export to NotebookLM"
   - Choose domain: Characters / Plot / World / Scenes
   - System generates markdown summary:
     ```markdown
     # Characters Extracted from Manuscript

     ## Mickey Bardot
     - **Type:** Enhanced human, protagonist
     - **Traits:** Tactical thinker, observer-becoming-participant
     - **Arc:** From passive observer to active player in consciousness war
     - **Appears in:** 47 scenes
     - **Key Relationships:**
       - The Chronicler (mentor/guide, appears together in 12 scenes)
       - Sarah Chen (ally, appears together in 8 scenes)

     ## The Chronicler
     ...
     ```
   - User downloads markdown
   - User uploads to Character notebook in NotebookLM
   - Now NotebookLM knows ACTUAL character data, not just plans!

2. **Continuous Feedback Loop:**
   - NotebookLM starts with IDEAS
   - Writers Factory creates REALITY
   - Knowledge Graph extracts TRUTH
   - Export back to NotebookLM
   - NotebookLM now has IDEAS + REALITY
   - User can query discrepancies: "How did Mickey's arc differ from plan?"

---

## Practical Implementation Roadmap

### Sprint 15 (Beginner Mode)

**Focus:** NotebookLM voice extraction for beginners

**New Components:**
1. `factory/integrations/notebooklm_voice_extractor.py` - Extract from personal writing
2. Support single notebook (beginner's initial collection)
3. Extract voice → generate starter skills

**No knowledge graph changes yet.**

### Sprint 16 (Multi-Notebook Support)

**Focus:** Support your multi-notebook architecture

**New Features:**
1. **Multiple Notebook URLs:**
   ```python
   project_config = {
       "notebooks": {
           "ideas": "https://notebooklm.google.com/notebook/abc",
           "characters": "https://notebooklm.google.com/notebook/def",
           "structure": "https://notebooklm.google.com/notebook/ghi"
       }
   }
   ```

2. **Domain-Specific Queries:**
   - Ideas notebook → creative queries
   - Characters notebook → character queries
   - Structure notebook → plot/structure queries

3. **Selective Sync:**
   - "Sync Characters Only" button
   - "Sync All Notebooks" button
   - Last sync timestamp per notebook

### Sprint 17 (Incremental Knowledge Graph)

**Focus:** Make knowledge graph update continuously

**New Features:**
1. **Scene Save Hook:**
   ```python
   async def on_scene_save(scene_id, scene_text):
       await update_knowledge_graph(scene_id, scene_text)
   ```

2. **Query Interface:**
   ```python
   # In scene editor sidebar
   "Ask about your novel" input box

   User: "Has Mickey been to this location?"
   System: Queries knowledge graph → Returns scenes
   ```

3. **Live Updates:**
   - Every scene save → mini extraction
   - Nightly batch → full re-extraction (verify consistency)

### Sprint 18 (Export to NotebookLM)

**Focus:** Close the loop - knowledge graph → NotebookLM

**New Features:**
1. **Export Functions:**
   - Export Characters
   - Export Plot Threads
   - Export Scene Breakdown
   - Export Continuity Report

2. **Markdown Generators:**
   ```python
   generate_character_summary_markdown(graph)
   generate_plot_summary_markdown(graph)
   generate_world_summary_markdown(graph)
   ```

3. **User Workflow:**
   - Click "Export to NotebookLM"
   - Download markdown
   - Upload to relevant notebook
   - Query in NotebookLM: "How does the actual Mickey differ from my original concept?"

---

## Answering Your Specific Questions

### 1. "Are we assuming one NotebookLM or multiple?"

**Current (Sprint 14):** System accepts multiple URLs but treats them uniformly (queries all with same questions)

**Your Practice (Correct!):** Multiple specialized notebooks

**Sprint 15+:** Support multiple notebooks with domain-specific queries for each

**Recommendation:** Implement multi-notebook architecture in Sprint 16 (after beginner mode)

### 2. "Can NotebookLM MCP server push information or create notebooks?"

**Current:** No. NotebookLM client is read-only (browser automation limitations)

**Write Capabilities:** Technically possible but EXTREMELY fragile and unreliable

**Recommendation:**
- Phase 1: Read-only multi-notebook (reliable)
- Phase 2: Export markdown for manual upload (user control)
- Phase 3: Wait for official NotebookLM API (if/when released)

**You CAN:** Export knowledge graph data to markdown files that users upload to NotebookLM manually

### 3. "What about the ongoing knowledge graph?"

**Current State:**
- ✅ Knowledge graph exists (`factory/analysis/knowledge_graph.py`)
- ✅ Populated from manuscript analysis (Sprint 13)
- ❌ **Not** updated incrementally as you write
- ❌ **No** query interface exposed during writing
- ✅ Used for analysis/reports (character depth, plot holes)

**Your Vision (Correct!):**
> "ongoing information being created would be thrown into this knowledge graph and could be queried for things as one was writing"

**Missing Pieces:**
1. Incremental update on scene save
2. Query interface in writing UI
3. Real-time "Ask your novel" feature

**Sprint 17 Fix:** Add these missing pieces

### 4. "How do they coexist?"

**Perfect Separation of Concerns:**

| System | Purpose | Content | Update Model |
|--------|---------|---------|--------------|
| **NotebookLM** | External research, ideas, plans | User-curated knowledge, references, research | Manual (user adds) |
| **Knowledge Graph** | Internal story intelligence | AI-extracted entities, relationships | Automatic (from scenes) |

**NotebookLM = PLANS**
Knowledge Graph = REALITY

**Example:**
- NotebookLM Character notebook says: "Mickey is a passive observer"
- User writes 30 scenes
- Knowledge Graph extracts: "Mickey takes direct action in 15 scenes"
- Export graph → Upload to NotebookLM
- Query NotebookLM: "How did Mickey's actual arc differ from my plan?"
- Get answer: "Plan said passive, reality shows active in second half"

**Power of Both:**
- NotebookLM preserves your creative process (ideas, iteration)
- Knowledge Graph tracks your actual manuscript (ground truth)
- Together: See vision vs. execution

---

## Recommended Architecture Decisions

### Decision 1: Multi-Notebook Support (Sprint 16)

**Implement your practice as the system design:**

```python
# Project config
{
    "notebooklm_notebooks": {
        "ideas": {
            "url": "...",
            "queries": ["creative_prompts", "world_building"],
            "sync": "weekly"
        },
        "characters": {
            "url": "...",
            "queries": ["character_profiles", "relationships"],
            "sync": "on_demand"
        },
        "structure": {
            "url": "...",
            "queries": ["chapter_outline", "act_structure"],
            "sync": "on_demand"
        }
    }
}
```

### Decision 2: Read-Only NotebookLM Integration (Permanent)

**Do NOT attempt write automation:**
- Too fragile
- No official API
- High failure rate
- User loses control

**Instead: Export Workflow:**
1. System generates markdown summaries
2. User downloads
3. User uploads to NotebookLM
4. Reliable, user-controlled, no automation brittleness

### Decision 3: Incremental Knowledge Graph (Sprint 17)

**Make it continuous:**
- Update on every scene save (mini extraction)
- Nightly batch verification (full re-extraction)
- Query interface in UI ("Ask your novel")
- Real-time continuity checking

### Decision 4: Bidirectional Documentation (Sprint 18)

**Close the loop:**
- NotebookLM → Project Setup (Sprint 14 ✅)
- Project → Knowledge Graph (Sprint 13 ✅)
- Knowledge Graph → Export (Sprint 18)
- Export → NotebookLM (Manual upload)
- Full cycle: Ideas → Reality → Verification

---

## Technical Specifications

### Multi-Notebook Data Model

```python
@dataclass
class NotebookConfig:
    url: str
    purpose: str  # "ideas", "characters", "structure", "world"
    query_templates: List[str]
    last_sync: datetime
    sync_frequency: str  # "manual", "daily", "weekly"

@dataclass
class ProjectNotebooks:
    notebooks: Dict[str, NotebookConfig]

    def sync_notebook(self, notebook_type: str):
        """Sync specific notebook."""

    def sync_all(self):
        """Sync all notebooks."""

    def export_to_notebook(self, notebook_type: str, content_type: str):
        """Export knowledge graph to markdown for upload."""
```

### Incremental Graph Update

```python
class IncrementalGraphUpdater:
    """Update knowledge graph as scenes are written."""

    async def update_from_scene(
        self,
        project_id: str,
        scene_id: str,
        scene_text: str
    ):
        """
        Extract entities from new scene and merge into graph.

        Process:
        1. Mini extraction (characters, locations in this scene)
        2. Load existing graph
        3. Merge nodes (add new, update existing)
        4. Merge edges (add new relationships)
        5. Update graph statistics
        6. Save updated graph
        """

    async def verify_consistency(self, project_id: str):
        """
        Nightly batch: Re-extract entire manuscript,
        compare with incremental graph, fix discrepancies.
        """
```

### Query Interface

```python
class KnowledgeGraphQueryEngine:
    """Natural language queries against knowledge graph."""

    async def query(self, project_id: str, question: str) -> Dict:
        """
        Examples:
        - "Has Mickey been to The Hotel before?"
        - "What plot threads are unresolved?"
        - "Show me all scenes with quantum physics"
        - "Which characters have met each other?"
        """
```

---

## Summary & Next Steps

### What Exists Today

1. ✅ NotebookLM Client (read-only, single/multiple URLs)
2. ✅ Knowledge Graph (built from manuscript analysis)
3. ✅ Entity Extraction (6 agent types)
4. ✅ One-way flow: NotebookLM → Project Setup

### What's Missing

1. ❌ Multi-notebook domain-specific queries
2. ❌ Incremental knowledge graph updates
3. ❌ Query interface during writing
4. ❌ Export knowledge graph to NotebookLM

### Sprint 15 (Current)

**Focus:** Beginner mode with NotebookLM voice extraction
- Extract from personal writing (emails, social media)
- Generate starter skills
- Single notebook support

### Post-Sprint 15 Priorities

**Sprint 16: Multi-Notebook Architecture**
- Implement your multi-notebook practice
- Domain-specific queries per notebook
- Selective sync

**Sprint 17: Live Knowledge Graph**
- Incremental updates on scene save
- Query interface in UI
- Real-time continuity checking

**Sprint 18: Export Loop**
- Generate markdown summaries
- Export to NotebookLM workflow
- Close bidirectional knowledge flow

---

## Your Questions Answered

**Q1:** "Are we assuming one NotebookLM or multiple?"
**A:** Currently treats multiple URLs uniformly. Sprint 16 will add your multi-notebook architecture with domain-specific queries.

**Q2:** "Can we push to NotebookLM or create notebooks?"
**A:** No write automation (too fragile). Instead: Export markdown for manual upload. Reliable and user-controlled.

**Q3:** "What about the ongoing knowledge graph?"
**A:** Exists but not incremental. Sprint 17 will add continuous updates + query interface for "Ask your novel while writing."

**Q4:** "How do they coexist?"
**A:** Perfect separation: NotebookLM = External/Curated/Plans, Knowledge Graph = Internal/Extracted/Reality. Together they show vision vs. execution.

---

**Your multi-notebook practice is architecturally superior. We should implement it as the system design.**
