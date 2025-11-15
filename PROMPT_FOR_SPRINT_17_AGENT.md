# Prompt for Sprint 17 Implementation Agent

## Mission: Enhanced Welcome Flow + Live Knowledge Graph 🎯

**Sprint:** 17 - Intelligent Setup Wizard + Auto-Updating Knowledge Graph
**Priority:** HIGH - Foundation for January Course
**Timeline:** 3 weeks
**Dependencies:** Sprint 15 ✅ Complete, Sprint 16 ✅ Complete

---

## What You're Building

**The Complete Workflow:**

1. **Enhanced Welcome** → User chooses path (Experienced/Prepared/New)
2. **AI Wizard** → Extracts knowledge from NotebookLM intelligently
3. **Category Folders** → Structured reference library created
4. **Knowledge Graph** → Initialized from categories
5. **Live Updates** → Graph auto-updates as user writes
6. **Development Docs** → All queries saved for NotebookLM upload
7. **Export Summaries** → Consolidated exports (characters, locations, plot, themes)

**Result:** Bidirectional knowledge flow between NotebookLM and Writers Factory!

---

## Read These Files First

1. **SPRINT_17_LIVE_KNOWLEDGE_GRAPH_AND_WELCOME_FLOW.md** - Complete specification (18,000+ words)
2. **docs/DATA_ARCHITECTURE_ANALYSIS.md** - Architecture decisions
3. **docs/KNOWLEDGE_SYSTEMS_ARCHITECTURE.md** - NotebookLM vs Knowledge Graph
4. **docs/NOTEBOOKLM_CURRENT_STATE.md** - What Sprint 11 already built

---

## Your 3-Week Plan

### **Week 1: Enhanced Welcome Flow (Frontend)**

**Goal:** Replace current welcome flow with intelligent path selection

**Build:**

1. **Modify Existing Component**
   - File: `webapp/frontend-v2/src/components/WelcomeModal.jsx`
   - Change: Replace Step 3 with `<PathSelectionStep />`

2. **New Components (4 files)**
   - `PathSelectionStep.jsx` - Three-path chooser (Experienced/Prepared/New)
   - `PathOption.jsx` - Reusable path card with hover effects
   - `NotebookLMRecommendation.jsx` - Modal for new writers
   - `NotebookLMGuide.jsx` - Full page guide (5 steps)

3. **Routing Updates**
   - File: `webapp/frontend-v2/src/App.jsx`
   - Add routes: `/onboarding/notebooklm-guide`, `/onboarding/ai-wizard`, `/onboarding/interactive-qa`

**Design System:**
- ✅ Reuse existing Tailwind theme (dark mode, gradients)
- ✅ Use Lucide React icons (Notebook, FileText, Sparkles, etc.)
- ✅ Match existing card/button patterns
- ✅ Responsive layout

**Success Criteria:**
- [ ] PathSelectionStep shows 3 clear options
- [ ] "Prepared Writer" marked RECOMMENDED ⭐
- [ ] Routing works for all paths
- [ ] NotebookLM guide is comprehensive and helpful
- [ ] User can bookmark guide and return later

---

### **Week 2: AI Wizard Backend**

**Goal:** Build intelligent conversation agent for knowledge extraction

**Build:**

1. **Model Router** (`factory/ai/model_router.py`)
   - Default: Llama 3.3 (local via Ollama) - FREE
   - Optional: Claude, GPT, Gemini (user-configured)
   - Task-specific routing (extraction vs writing)

2. **Ollama Integration** (`factory/ai/ollama_setup.py`)
   - Check if Ollama installed
   - Auto-download Llama 3.3 if missing
   - Fallback to API models if Ollama unavailable

3. **Setup Wizard Agent** (`factory/ai/setup_wizard_agent.py`)
   - **NOT a dumb form** - This is an AI agent having a conversation
   - Tools: query_notebooklm, create_category_file, suggest_subcategories
   - Process 8 categories: Characters, Story_Structure, World_Building, etc.
   - Adaptive subcategories (based on content volume)

4. **Category Templates** (`factory/templates/category_templates.py`)
   - 8 templates with field definitions
   - Each field has: query, required flag, prompt_if_empty flag
   - Example: Character template with 15+ fields

5. **WebSocket Endpoint** (`webapp/backend/routes/wizard.py`)
   - Real-time conversation via WebSocket
   - Stream AI messages to frontend
   - Wait for user responses
   - Progress through all categories

**Key Principle:** AI agent validates findings with user at every step

**Example Conversation:**
```
AI: "I found 5 characters in your notebook: Tom, Harry, Dick,
     President Trump, Elon Musk. Are these all main characters,
     or are some just references?"

User: "Just Tom and Harry. Dick is historical research."

AI: "Got it. Creating profiles for Tom and Harry..."
```

**Success Criteria:**
- [ ] Model Router works (Llama default, API optional)
- [ ] Ollama setup check works
- [ ] AI wizard processes all 8 categories
- [ ] Intelligent disambiguation (not blindly extracting)
- [ ] Subcategories adapt to content (flat vs hierarchical)
- [ ] Category files created correctly
- [ ] WebSocket communication stable

---

### **Week 3: AI Wizard Frontend + Live Knowledge Graph**

**Goal:** Complete wizard UI + auto-updating knowledge graph

**Build:**

#### Part A: Wizard Frontend

1. **AI Wizard Page** (`webapp/frontend-v2/src/pages/AIWizard.jsx`)
   - Two-panel layout: Progress sidebar + Chat area
   - Progress shows 8 categories with status (pending/in_progress/complete)
   - Chat-like interface (AI messages vs User messages)

2. **Chat Components** (`webapp/frontend-v2/src/components/wizard/ChatMessage.jsx`)
   - AI message: Blue/purple gradient avatar + Sparkles icon
   - User message: Gray avatar + User icon
   - Option selection buttons
   - Markdown rendering for AI responses

3. **WebSocket Frontend**
   - Connect to `/ws/wizard/{project_id}`
   - Stream AI messages in real-time
   - Send user responses
   - Handle completion → redirect to editor

#### Part B: Knowledge Graph Lifecycle

1. **Initial Ingest** (`factory/analysis/knowledge_graph_manager.py`)
   - After wizard completes → Read all category files
   - Extract nodes: characters, locations, plot threads, motifs
   - Extract edges: relationships, appears_at, etc.
   - Save: `projects/{id}/knowledge/graph/knowledge_graph.json`

2. **Scene Completion Hook** (`webapp/backend/routes/scenes.py`)
   - POST `/api/scenes/{id}/complete`
   - Extract entities from completed scene
   - Update knowledge graph nodes/edges
   - Check for modified category files → sync if changed
   - Return notification data

3. **Development Docs** (`factory/analysis/development_docs.py`)
   - Every knowledge graph query → Save answer
   - Meaningful filename: `scene_03_mickey_emotional_state.md`
   - Location: `exports_for_notebooklm/development_docs/`

4. **User Notification** (`webapp/frontend-v2/src/components/SceneCompleteNotification.jsx`)
   - Modal after scene complete
   - Shows: X new entities, Y category files synced, Z development docs created
   - Buttons: [Open Folder] [Remind Later] [Done]

5. **Export Summaries** (`factory/analysis/knowledge_graph_exporter.py`)
   - Generate consolidated markdown files
   - Categories: all_characters.md, all_locations.md, plot_threads.md, themes_motifs.md, timeline.md
   - Location: `exports_for_notebooklm/summaries/`

6. **Export UI** (`webapp/frontend-v2/src/components/settings/ExportPanel.jsx`)
   - In Project Settings or Tools panel
   - Buttons for each export category
   - "Export All" button

**Success Criteria:**
- [ ] Wizard UI chat works smoothly
- [ ] Progress sidebar updates correctly
- [ ] Knowledge graph initialized after wizard
- [ ] Scene completion extracts entities
- [ ] Modified category files synced automatically
- [ ] Development docs saved with meaningful names
- [ ] Notification appears after scene complete
- [ ] "Open Folder" button works
- [ ] Export summaries generate correctly
- [ ] Complete bidirectional knowledge flow works

---

## Key Technical Decisions

### 1. Model Strategy (Cost-Conscious)

**Default (FREE):**
```json
{
  "setup_wizard": "llama3.3",           // Local, free
  "knowledge_extraction": "llama3.3",    // Local, free
  "knowledge_query": "llama3.3",         // Local, free
  "scene_writing": "claude-sonnet-4.5",  // Via MCP (course credits)
  "voice_analysis": "claude-sonnet-4.5"  // Via MCP (course credits)
}
```

**Premium (User Configurable):**
```json
{
  "setup_wizard": "claude-sonnet-4.5",   // $2-5 one-time
  "knowledge_extraction": "claude-sonnet-4.5",  // $5-10/month
  // ... etc
}
```

**For January Course:** Default = $0 additional cost!

---

### 2. Category Folder Structure

**8 Core Categories (Created by Wizard):**

1. **Characters/** - Profiles, arcs, relationships
2. **Story_Structure/** - Acts, chapters, beats
3. **World_Building/** - Locations, technology, world rules
4. **Themes_and_Philosophy/** - Core ideas, symbolism
5. **Voice_and_Craft/** - Style guides, writing patterns
6. **Antagonism_and_Conflict/** - Opposition forces, tension
7. **Key_Beats_and_Pacing/** - Scene-level execution
8. **Research_and_Setting_Specifics/** - Concrete facts, historical data

**Adaptive Subcategories:**
- <5 items → Flat structure
- 5-15 items → Basic subcategories (Core/Supporting)
- 15+ items → Detailed subcategories (Core/Supporting/Antagonists/Relationships)

---

### 3. Knowledge Graph Update Triggers

**When to update:**
1. **Initial ingest:** After wizard completes (one-time)
2. **Scene complete:** Extract from scene + sync modified category files
3. **Manual sync:** User clicks "Sync Knowledge Graph" (optional)

**What updates:**
- New nodes (characters, locations discovered in scene)
- Updated nodes (character development, location changes)
- New/strengthened edges (relationships, interactions)
- Category file changes (user manually edited reference files)

---

### 4. Development Docs Naming

**Pattern:** `{scene_id}_{keyword1}_{keyword2}_{keyword3}.md`

**Examples:**
- Query: "What's Mickey's emotional state?"
  - File: `scene_03_mickey_emotional_state.md`

- Query: "Describe the Hotel's architecture"
  - File: `scene_12_hotel_architecture.md`

- Query: "What are the themes of consciousness war?"
  - File: `scene_05_consciousness_war_themes.md`

**Implementation:**
```python
def generate_meaningful_filename(scene_id: str, question: str) -> str:
    keywords = extract_keywords(question)  # NLP keyword extraction
    key_terms = "_".join(keywords[:3])     # Limit to 3 keywords
    return f"{scene_id}_{key_terms}.md"
```

---

### 5. Export Summary Format

**Example: `all_characters.md`**

```markdown
# Characters

*Exported: 2025-11-15 16:30*

## Mickey Bardot

**Role:** Protagonist, Enhanced human observer

**Internal Conflicts:** Passive observation vs. active intervention

**Motivations:** Understand consciousness war, protect Noni

**Appearances:** 23 scenes
- First: scene_001
- Latest: scene_023

**Relationships:**
- The Chronicler: mentor
- Noni: emerging_connection

---

## Noni

...
```

---

## Common Pitfalls to Avoid

### Pitfall 1: Treating Wizard as Dumb Form

**Wrong:** Extract all data blindly, create files, done.

**Right:** Validate findings with user at every step.

**Example:**
```python
# WRONG
characters = extract_all_names_from_notebook()
for char in characters:
    create_character_file(char)

# RIGHT
raw_names = extract_all_names_from_notebook()
validated = ask_user(f"Found: {raw_names}. Which are actual characters?")
for char in validated:
    extracted_data = extract_character_details(char)
    confirmed = ask_user(f"Is this correct? {extracted_data}")
    create_character_file(confirmed)
```

---

### Pitfall 2: Not Handling Empty NotebookLM Fields

**Wrong:** Leave field blank if NotebookLM has no data.

**Right:** Prompt user during wizard for critical fields.

**Template Field Definition:**
```python
{
    "name": "internal_conflicts",
    "query": "What are {character_name}'s internal conflicts?",
    "required": True,
    "prompt_if_empty": True  # ← ASK USER if NotebookLM empty
}
```

---

### Pitfall 3: Forgetting to Sync Modified Category Files

**Wrong:** Only extract from scenes, never check category folders.

**Right:** On scene complete, check for modified reference files.

```python
# Get all category files
category_files = glob("projects/{id}/reference/**/*.md")

# Check modification times
modified_since_last_sync = [
    f for f in category_files
    if os.path.getmtime(f) > last_sync_time
]

# Re-ingest modified files
for file_path in modified_since_last_sync:
    graph.ingest_category_file(file_path)
```

---

### Pitfall 4: Meaningless Development Doc Names

**Wrong:** `query_001.md`, `query_002.md`, `answer_12345.md`

**Right:** `scene_03_mickey_emotional_state.md`

**Why:** User needs to quickly find relevant docs when uploading to NotebookLM.

---

### Pitfall 5: Not Using WebSocket for Wizard

**Wrong:** Traditional request/response with loading spinners.

**Right:** WebSocket for real-time streaming conversation.

**Why:** Better UX - user sees AI "thinking" and responding naturally.

---

## Testing Strategy

### Unit Tests (Week 2)

**Model Router:**
```bash
pytest tests/test_model_router.py -v
```

**Coverage:**
- Default model selection (Llama)
- User-configured model selection
- Fallback when model unavailable
- Task-specific routing

**Wizard Agent:**
```bash
pytest tests/test_setup_wizard_agent.py -v
```

**Coverage:**
- NotebookLM queries
- Character extraction and validation
- Subcategory logic (adaptive structure)
- File creation with templates

---

### Integration Tests (Week 3)

**End-to-End Wizard Flow:**
```bash
pytest tests/test_wizard_integration.py -v
```

**Test Scenario:**
1. User selects "Prepared Writer" path
2. Connects NotebookLM URL
3. Wizard analyzes notebook
4. Processes all 8 categories
5. User validates findings
6. Category files created
7. Knowledge graph initialized
8. User redirected to editor

**Knowledge Graph Lifecycle:**
```bash
pytest tests/test_knowledge_graph_lifecycle.py -v
```

**Test Scenario:**
1. Wizard completes → Knowledge graph initialized
2. User writes Scene 1
3. User queries graph → Development doc saved
4. User completes Scene 1 → Graph updates
5. User edits category file
6. User completes Scene 2 → Category file synced
7. User exports summaries → Files generated

---

### User Acceptance Testing (Week 3)

**5 Beta Testers:**
- 2 with NotebookLM notebooks already prepared
- 2 new writers (will follow guide)
- 1 experienced writer (import flow)

**Task:**
"Set up a new novel project and write 3 scenes. Upload development docs to NotebookLM."

**Success Metrics:**
- 5/5 complete setup without blocking bugs
- 4/5 successfully create project via AI wizard
- 5/5 knowledge graph updates correctly
- 4/5 find development docs easily
- 4/5 successfully upload to NotebookLM

---

## File Checklist (35 New/Modified Files)

### Frontend (React) - 11 Files

**New:**
1. `webapp/frontend-v2/src/components/onboarding/PathSelectionStep.jsx`
2. `webapp/frontend-v2/src/components/onboarding/PathOption.jsx`
3. `webapp/frontend-v2/src/components/onboarding/NotebookLMRecommendation.jsx`
4. `webapp/frontend-v2/src/pages/NotebookLMGuide.jsx`
5. `webapp/frontend-v2/src/pages/AIWizard.jsx`
6. `webapp/frontend-v2/src/components/wizard/ChatMessage.jsx`
7. `webapp/frontend-v2/src/components/wizard/ProgressSteps.jsx`
8. `webapp/frontend-v2/src/components/SceneCompleteNotification.jsx`
9. `webapp/frontend-v2/src/components/settings/ExportPanel.jsx`

**Modified:**
10. `webapp/frontend-v2/src/components/WelcomeModal.jsx` - Replace Step 3
11. `webapp/frontend-v2/src/App.jsx` - Add routes

---

### Backend (Python) - 9 Files

**New:**
1. `factory/ai/model_router.py`
2. `factory/ai/ollama_setup.py`
3. `factory/ai/setup_wizard_agent.py`
4. `factory/templates/category_templates.py`
5. `factory/analysis/knowledge_graph_manager.py`
6. `factory/analysis/entity_extractor.py`
7. `factory/analysis/knowledge_graph_exporter.py`
8. `webapp/backend/routes/wizard.py`
9. `webapp/backend/routes/knowledge.py`

**Modified:**
10. `webapp/backend/simple_app.py` - Register routers
11. `webapp/backend/routes/scenes.py` - Scene completion

---

### Tests - 5 Files

**New:**
1. `tests/test_model_router.py`
2. `tests/test_setup_wizard_agent.py`
3. `tests/test_wizard_integration.py`
4. `tests/test_knowledge_graph_lifecycle.py`
5. `tests/test_export_summaries.py`

---

### Templates/Config - 9 Files

**Character Template:**
1. `factory/templates/character_template.json`

**Other Templates:**
2. `story_structure_template.json`
3. `world_building_template.json`
4. `themes_philosophy_template.json`
5. `voice_craft_template.json`
6. `antagonism_conflict_template.json`
7. `beats_pacing_template.json`
8. `research_template.json`

**Ollama Config:**
9. `factory/ai/ollama_config.yaml`

---

## Success Criteria (Final Checklist)

### Week 1: Welcome Flow ✓
- [ ] PathSelectionStep shows 3 options clearly
- [ ] "Prepared Writer" marked RECOMMENDED
- [ ] NotebookLM guide comprehensive and helpful
- [ ] Routing works for all paths
- [ ] User can save/bookmark guide

### Week 2: AI Wizard Backend ✓
- [ ] Model Router works (Llama + API)
- [ ] Ollama setup check/download works
- [ ] Wizard processes all 8 categories
- [ ] Intelligent validation (not blind extraction)
- [ ] Subcategories adapt to content volume
- [ ] Category files created correctly
- [ ] WebSocket stable

### Week 3: Frontend + Knowledge Graph ✓
- [ ] Chat UI works smoothly
- [ ] Progress sidebar updates
- [ ] Knowledge graph initialized
- [ ] Scene completion extracts entities
- [ ] Category files synced automatically
- [ ] Development docs saved meaningfully
- [ ] Notification after scene complete
- [ ] "Open Folder" works
- [ ] Export summaries generate correctly
- [ ] **Bidirectional knowledge flow complete**

---

## Integration with Existing Sprints

**Sprint 11 (NotebookLM):** ✅
- Uses existing NotebookLMClient for queries
- No changes needed to Sprint 11 code

**Sprint 14 (Project Setup):** 🔄
- Keeps import flow intact
- Adds new wizard path alongside existing flow

**Sprint 15 (Beginner Mode):** ✅
- Voice extraction still works
- AI wizard can extract voice from NotebookLM

**Sprint 16 (Multi-Notebook):** ✅
- Wizard can use multiple specialized notebooks
- Export summaries go to corresponding notebooks

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  USER: New Project                                       │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  Welcome Modal - Choose Your Path                       │
│  ○ Experienced Writer (import)                          │
│  ● Prepared Writer (AI wizard) ⭐ SELECTED              │
│  ○ New Writer (guide or interactive)                    │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  AI Wizard (WebSocket Conversation)                     │
│                                                          │
│  [Progress]        [Chat Interface]                     │
│  ✓ Characters      AI: "I found 5 characters..."        │
│  → Structure       User: "Just Tom and Harry"           │
│  ○ World           AI: "Got it. Extracting..."          │
│  ○ Themes          ...                                  │
│  ○ Voice                                                │
│  ○ Conflict                                             │
│  ○ Beats                                                │
│  ○ Research                                             │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  Category Folders Created                               │
│  ✓ Characters/                                          │
│    ├─ Tom_profile.md                                    │
│    └─ Harry_profile.md                                  │
│  ✓ Story_Structure/                                     │
│  ✓ World_Building/                                      │
│  ... (all 8 categories)                                 │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  Knowledge Graph Initialized                            │
│  {                                                       │
│    nodes: [                                             │
│      {type: "character", name: "Tom", ...},             │
│      {type: "character", name: "Harry", ...},           │
│      {type: "location", name: "Hotel", ...}             │
│    ],                                                   │
│    edges: [...]                                         │
│  }                                                      │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  USER: Writing Scene 1                                   │
│  Query: "What's Tom's personality?"                     │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  Knowledge Graph Query                                   │
│  Answer: "Tom is analytical, cautious..."               │
│  Saved: scene_01_tom_personality.md                     │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  USER: Scene 1 Complete                                  │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  Knowledge Graph Update                                  │
│  • Extract entities from Scene 1                        │
│  • Update Tom node (new trait discovered)               │
│  • Check category files (none modified)                 │
│  • Notify user (1 development doc created)              │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│  USER: Upload development docs to NotebookLM            │
│  [Open Folder] → exports_for_notebooklm/development_docs│
│  Copy scene_01_tom_personality.md to NotebookLM         │
└─────────────────────────────────────────────────────────┘
```

---

## Budget: $0 with Default Config! 💰

**Llama 3.3 Local:**
- Setup wizard: FREE
- Knowledge extraction: FREE
- Knowledge queries: FREE
- Development docs: FREE

**Claude via MCP (Course Credits):**
- Scene writing: Included in course
- Voice analysis: Included in course

**Total Additional Cost:** $0 for January course students!

---

## Dependencies (Already Installed)

**Python:**
- fastapi ✅
- websockets ✅
- anthropic ✅
- ollama (will auto-install if missing)

**Frontend:**
- react ✅
- @mui/material ✅
- lucide-react ✅
- react-markdown ✅

**No new dependencies required!**

---

## Let's Build This! 🚀

You're implementing the complete knowledge flow:

**NotebookLM (Plans)** ↔ **Writers Factory (Reality)** ↔ **Knowledge Graph (Truth)**

**Start with Week 1: Welcome Flow UI**

First files to create:
1. `PathSelectionStep.jsx`
2. `NotebookLMRecommendation.jsx`
3. `NotebookLMGuide.jsx`

Good luck! 🎯
