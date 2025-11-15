# Data Architecture Analysis - Current State

**Date:** November 15, 2025
**Purpose:** Understand storage structure before designing Sprint 17

---

## Current Directory Structure

### 1. `project/` (Singular - Original Explants Project)

**Location:** `/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/project/`

```
project/
├── manuscript/          # Actual manuscript scenes
├── planning/            # Planning documents
├── admin/              # Administrative files
├── archive/            # Archived content
├── output/             # Production outputs
└── reference/          # Reference materials
    └── Reference_Library/  # Current reference files
```

**What this is:**
- Original project structure (pre-Sprint 14)
- Single project: The Explants
- Your actual working manuscript location
- Reference materials stored in `Reference_Library/`

---

### 2. `projects/` (Plural - Sprint 14 Test Projects)

**Location:** `/Users/gch2024/writers-factory-core/projects/`

```
projects/
├── test-thriller/       # Test project #1 (Sprint 14 testing)
├── witty-hearts/        # Test project #2 (Sprint 14 testing)
└── quiet-depths/        # Test project #3 (Sprint 14 testing)
```

**What these are:**
- Created during Sprint 14 bug squashing (November 15, 2025)
- Test projects to validate the Project Setup Wizard
- Each has complete structure with 6 custom skills

**Structure of each test project:**
```
test-thriller/
├── config.json                 # Project configuration
├── README.md                   # Project documentation
├── scenes/                     # Scene storage (empty - test projects)
├── knowledge/                  # Knowledge storage
│   └── craft/
│       ├── story-context.md
│       └── voice-gold-standard.md
└── .claude/
    └── skills/                 # 6 custom skills
        ├── scene-analyzer-test-thriller/
        │   ├── SKILL.md
        │   └── references/
        │       ├── voice-profile.md
        │       ├── quality-criteria.md
        │       ├── anti-patterns.md
        │       └── metaphor-domains.md
        ├── scene-enhancer-test-thriller/
        ├── character-validator-test-thriller/
        ├── scene-writer-test-thriller/
        ├── scene-multiplier-test-thriller/
        └── scaffold-generator-test-thriller/
```

---

## The Confusion Explained

**You saw two project structures:**
1. `project/` - YOUR actual Explants project (original structure in Documents folder)
2. `projects/` - Test projects created for Sprint 14 validation (in writers-factory-core repo)

**The reference directory you mentioned:**
- Location: `project/reference/Reference_Library/`
- Currently contains your actual reference files
- Purpose: Organizing reference materials for The Explants

---

## Where Knowledge is Actually Stored (Current State)

### Sprint 13: Knowledge Graph

**Storage location:** NOT IMPLEMENTED YET for persistent storage

**Intended location:**
```
projects/{project-id}/knowledge_graph.json
```

**Current state:**
- Knowledge graph can be built from manuscript (Sprint 13 code exists)
- But only exported to JSON on-demand
- NOT automatically saved/updated
- NOT persisted between sessions

**What should be in knowledge_graph.json:**
```json
{
  "manuscript_id": "test-thriller",
  "nodes": [
    {
      "node_id": "character-0",
      "node_type": "character",
      "name": "Mickey Bardot",
      "attributes": {
        "traits": ["tactical", "observer"],
        "psychology": "analytical thinker",
        "arc_notes": "passive to active"
      },
      "metadata": {
        "first_appearance": "scene-1",
        "appearances": ["scene-1", "scene-12", "scene-23"],
        "appearance_count": 3
      }
    },
    {
      "node_id": "location-0",
      "node_type": "location",
      "name": "The Hotel",
      "attributes": {
        "type": "building",
        "description": "Mysterious hotel"
      },
      "metadata": {
        "first_appearance": "scene-12",
        "appearances": ["scene-12", "scene-23", "scene-31"]
      }
    }
  ],
  "edges": [
    {
      "edge_id": "relationship-0",
      "edge_type": "appears_at",
      "source_id": "character-0",
      "target_id": "location-0",
      "attributes": {
        "scenes": ["scene-12", "scene-23", "scene-31"]
      },
      "weight": 3.0
    }
  ]
}
```

---

### Sprint 14: Project Knowledge (Skills References)

**Storage location:**
```
projects/{project-id}/.claude/skills/{skill-name}/references/
```

**Files created per skill:**
- `voice-profile.md` - Voice characteristics
- `story-context.md` - Story background
- `quality-criteria.md` - Quality scoring criteria
- `anti-patterns.md` - What to avoid
- `fix-patterns.md` - How to enhance
- `metaphor-domains.md` - Metaphor usage

**Example:** `projects/test-thriller/.claude/skills/scene-analyzer-test-thriller/references/voice-profile.md`

**What this contains:**
```markdown
# Voice Profile: test-thriller

## Core Characteristics
- Compressed prose
- Direct action verbs
- Minimal adjectives

## Sentence Structure
- Short, declarative sentences
- Active voice predominant
- Minimal subordinate clauses

## POV and Perspective
- Close third-person
- Character-focused
```

---

### Sprint 14: Project Craft Knowledge

**Storage location:**
```
projects/{project-id}/knowledge/craft/
```

**Files:**
- `story-context.md` - Overall story background
- `voice-gold-standard.md` - Voice exemplars

**Purpose:** Shared knowledge across all skills

---

### Sprint 11: NotebookLM Notebooks (External)

**Storage location:**
```
projects/{project-id}/notebooks.json
```

**OR:**
```
.manuscript/{project-id}/notebooks.json
```

**What this contains:**
```json
[
  {
    "id": "nb-abc123",
    "name": "Ideas & World-Building",
    "url": "https://notebooklm.google.com/notebook/abc",
    "description": "Creative flashes, plot development",
    "notebook_type": "ideas",
    "tags": ["ideas", "creative", "plot"],
    "use_count": 47,
    "last_used": "2025-11-15T14:30:00Z",
    "created_at": "2025-11-01T10:00:00Z"
  },
  {
    "id": "nb-def456",
    "name": "Character Profiles",
    "url": "https://notebooklm.google.com/notebook/def",
    "tags": ["characters", "backstories"]
  }
]
```

**Note:** Actual content lives in NotebookLM (Google's servers), not locally

---

## Your Question: Where Should Knowledge Be Stored?

### Current Problems

1. **Knowledge Graph** (Sprint 13):
   - Can be built but NOT persisted
   - No automatic updates
   - No storage location defined

2. **Reference Directories** (Original structure):
   - `project/reference/Reference_Library/` - Has your files
   - Not structured for AI-extracted knowledge
   - Separate from writers-factory-core repo

3. **Fragmented Storage:**
   - Skills have `references/` folders (per-skill knowledge)
   - Project has `knowledge/craft/` (shared knowledge)
   - No central "extracted knowledge" location

---

## Proposed Data Architecture (For Discussion)

### Option 1: Use Existing `knowledge/` Directory

```
projects/{project-id}/
├── knowledge/
│   ├── craft/                      # Existing (Sprint 14)
│   │   ├── story-context.md
│   │   └── voice-gold-standard.md
│   ├── graph/                      # NEW (Sprint 17)
│   │   └── knowledge_graph.json    # Knowledge graph
│   ├── extracted/                  # NEW (Sprint 17)
│   │   ├── characters.md           # Extracted character info
│   │   ├── locations.md            # Extracted locations
│   │   ├── plot_threads.md         # Extracted plot threads
│   │   └── motifs.md               # Extracted motifs/themes
│   └── exports/                    # NEW (Sprint 17)
│       └── for_notebooklm/         # Ready for NotebookLM upload
│           ├── characters_export.md
│           ├── plot_export.md
│           └── world_export.md
```

**Pros:**
- Builds on existing structure
- Everything in one `knowledge/` location
- Clear categorization

**Cons:**
- Mixes AI-extracted (graph, extracted) with human-curated (craft)

---

### Option 2: Separate Extracted Knowledge

```
projects/{project-id}/
├── knowledge/                      # Human-curated
│   └── craft/
│       ├── story-context.md
│       └── voice-gold-standard.md
├── graph/                          # AI-extracted (NEW)
│   ├── knowledge_graph.json        # Graph structure
│   ├── entities/                   # Extracted entities
│   │   ├── characters.json
│   │   ├── locations.json
│   │   ├── plot_threads.json
│   │   └── motifs.json
│   └── exports/                    # For NotebookLM
│       ├── characters_summary.md
│       └── plot_summary.md
└── reference/                      # User's manual notes (NEW)
    ├── research/
    ├── characters/
    └── worldbuilding/
```

**Pros:**
- Clear separation: Human-curated vs. AI-extracted
- `reference/` used for manual notes
- `graph/` dedicated to knowledge graph

**Cons:**
- More top-level directories
- Less centralized

---

### Option 3: Mirror Your Explants Structure

**For your actual Explants project:**
```
/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/project/
├── manuscript/                     # Scenes
├── reference/                      # All reference materials
│   ├── Reference_Library/          # Your existing files (manual)
│   ├── extracted/                  # AI-extracted knowledge (NEW)
│   │   ├── knowledge_graph.json
│   │   ├── characters_extracted.md
│   │   ├── locations_extracted.md
│   │   └── plot_threads_extracted.md
│   └── exports/                    # For NotebookLM upload (NEW)
│       ├── characters_for_notebooklm.md
│       └── plot_for_notebooklm.md
└── .claude/skills/                 # Skills with references
```

**For new projects in writers-factory-core:**
```
writers-factory-core/projects/{project-id}/
├── scenes/
├── knowledge/
│   ├── craft/
│   ├── graph/
│   ├── extracted/
│   └── exports/
```

**Pros:**
- Respects your existing Explants structure
- Future projects use clean new structure
- Everything reference-related in one place

**Cons:**
- Two different structures to maintain
- Migration complexity

---

## Your Workflow (Stated Back Logically)

### Step 1: User Writes Scenes
- User writes Scene 1, Scene 2, ... Scene N
- Scenes stored in `projects/{id}/scenes/`

### Step 2: Knowledge Graph Auto-Updates (Sprint 17)
- On every scene save:
  - Extract entities (characters, locations, plot threads, motifs)
  - Update `knowledge_graph.json`
  - Add new nodes (new characters/locations)
  - Update existing nodes (character development)
  - Add/strengthen edges (relationships)

### Step 3: Export Consolidated Summaries
- User clicks "Export Knowledge for NotebookLM"
- System queries knowledge graph
- Generates consolidated markdown files by category:
  - `characters_export.md` - All characters with traits, arcs, appearances
  - `locations_export.md` - All locations with descriptions, significance
  - `plot_export.md` - Plot threads, status, resolution
  - `themes_export.md` - Motifs, metaphors, thematic elements

### Step 4: Manual Upload to NotebookLM
- User downloads exported markdown files
- User uploads to corresponding NotebookLM notebooks:
  - `characters_export.md` → Character Profiles notebook
  - `plot_export.md` → Story Structure notebook
  - `locations_export.md` → World-Building notebook

### Step 5: Bidirectional Knowledge Flow
- **Writers Factory → Knowledge Graph:** Auto-extracted from scenes (real-time)
- **Knowledge Graph → Export Files:** Generated summaries (on-demand)
- **Export Files → NotebookLM:** Manual upload (user-controlled)
- **NotebookLM → Writers Factory:** Query for ideas/plans (Sprint 11 already works)

**Result:** Two knowledge systems synchronized:
- **Knowledge Graph:** What you actually wrote (ground truth)
- **NotebookLM:** Original plans + actual results (vision + execution)

---

## Questions for Discussion

### 1. Storage Location

**Where should knowledge graph live?**
- A. `projects/{id}/knowledge/graph/knowledge_graph.json`
- B. `projects/{id}/graph/knowledge_graph.json`
- C. Mirror Explants structure for each project type

**Where should extracted summaries live?**
- A. `projects/{id}/knowledge/extracted/`
- B. `projects/{id}/graph/entities/`
- C. `projects/{id}/reference/extracted/`

**Where should NotebookLM export files live?**
- A. `projects/{id}/knowledge/exports/for_notebooklm/`
- B. `projects/{id}/exports/notebooklm/`
- C. `projects/{id}/reference/exports/`

### 2. Export Categories

**What categories should we export?**
- Characters (definitely)
- Locations/World-building (definitely)
- Plot threads (definitely)
- Themes/Motifs (probably)
- Timeline/Events (maybe)
- Dialogue patterns (maybe)
- Metaphor usage (maybe)

**Should exports match NotebookLM notebook types?**
- Yes - mirror the structure (Ideas, Characters, Structure, Research)
- No - organize by entity type regardless of notebooks

### 3. Update Frequency

**When should knowledge graph update?**
- A. Every scene save (real-time, Sprint 17 plan)
- B. User clicks "Update Knowledge Graph" (manual)
- C. Nightly batch (once per day)
- D. Combination: Real-time + nightly verification

**When should exports be generated?**
- A. Automatically after knowledge graph updates
- B. User clicks "Export for NotebookLM" (on-demand)
- C. Scheduled (weekly)

### 4. Integration with Your Explants Project

**How should we handle your existing Explants project?**
- A. Migrate it to new `projects/explants/` structure
- B. Keep it separate, add knowledge graph to existing location
- C. Hybrid: Keep manuscript where it is, store graph in writers-factory-core

---

## My Recommendation (For Discussion)

### Proposed Structure

```
projects/{project-id}/
├── scenes/                         # User writes here
│   ├── scene-001.md
│   └── scene-002.md
├── knowledge/                      # ALL knowledge (centralized)
│   ├── craft/                      # Human-curated (Sprint 14)
│   │   ├── story-context.md
│   │   └── voice-gold-standard.md
│   ├── graph/                      # AI-extracted (NEW)
│   │   ├── knowledge_graph.json    # Raw graph data
│   │   └── stats.json              # Graph statistics
│   ├── entities/                   # Extracted & summarized (NEW)
│   │   ├── characters.md
│   │   ├── locations.md
│   │   ├── plot_threads.md
│   │   ├── motifs.md
│   │   └── timeline.md
│   └── exports/                    # For NotebookLM (NEW)
│       ├── characters_for_notebooklm.md
│       ├── world_for_notebooklm.md
│       ├── plot_for_notebooklm.md
│       └── last_export.json        # Metadata
├── .claude/skills/                 # Skills (Sprint 14)
└── config.json                     # Project config
```

### Workflow

1. **User writes** → Scene saved to `scenes/`
2. **Auto-extract** → Update `knowledge/graph/knowledge_graph.json`
3. **Auto-summarize** → Update `knowledge/entities/*.md` (human-readable)
4. **User exports** → Generate `knowledge/exports/*_for_notebooklm.md`
5. **User uploads** → Manual upload to NotebookLM notebooks

### Why This Structure

- ✅ Everything in `knowledge/` (centralized)
- ✅ Clear hierarchy: craft → graph → entities → exports
- ✅ Builds on existing Sprint 14 structure
- ✅ Human-readable summaries (`entities/*.md`) separate from raw data (`graph/*.json`)
- ✅ Export files clearly marked `for_notebooklm`

---

## Next Steps (After Discussion)

1. **Agree on storage location** for knowledge graph
2. **Agree on export categories** (what to generate)
3. **Agree on update triggers** (when to extract/export)
4. **Design Sprint 17** based on agreed architecture

**Let's discuss before I create Sprint 17 spec!**
