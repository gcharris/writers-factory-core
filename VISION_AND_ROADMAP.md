# Writers Factory - Vision and Roadmap

## Current Status (Nov 14, 2025)

✅ **Phase 1**: Tournament system with 23 AI models (COMPLETE)
✅ **Phase 2**: Rich TUI with 5-stage workflow (COMPLETE)
✅ **Web App MVP**: Basic UI with mock data (FUNCTIONAL)

---

## User Vision - Key Insights

### 1. Structure-First Approach

**NOT**: Generic "creation wizard"
**YES**: Hierarchical manuscript structure

```
📚 Novel Project
├── 📖 Act 1: The Discovery
│   ├── 📝 Chapter 1: Awakening
│   │   ├── Scene 1.1: Mickey's First Vision
│   │   ├── Scene 1.2: Lab Confrontation
│   │   └── Scene 1.3: The Quantum Leap
│   └── 📝 Chapter 2: The Facility
│       ├── Scene 2.1: Arrival
│       └── Scene 2.2: Meeting Noni
├── 📖 Act 2: The New Reality
│   └── ...
└── 📖 Act 3: The Consciousness War
    └── ...
```

**Key Feature**: Click to expand Acts → Chapters → Scenes

### 2. Brainstorming BEFORE Writing

**Landing Page Should Be**:
- "Before You Begin Writing" workspace
- NotebookLM integration instructions
- Upload/organize research materials
- Query your knowledge base

**Workflow**:
1. **Gather Materials** → PDFs, videos, articles, notes, MP3s
2. **Build NotebookLM** → Upload to Google's NotebookLM
3. **Brainstorm & Query** → "Who is Mickey?", "What's the Beehive?"
4. **Structure Story** → Define Acts/Chapters/Scenes
5. **Write Scenes** → Generate with AI + context from NotebookLM

### 3. Real Features Needed

- [x] Mock UI works
- [ ] Scene hierarchy (Acts → Chapters → Scenes)
- [ ] NotebookLM setup guide
- [ ] Real model comparison (not mock)
- [ ] Scene generation with context
- [ ] Model selection/deselection
- [ ] Knowledge base connection

---

## Proposed New Structure

### Left Sidebar: Project Structure
```
📚 The Explants (Volume 1)
  ↓
  📖 ACT 1: THE AWAKENING
    ↓
    📝 Chapter 1: Quantum Dreams
      → Scene 1.1: First Vision
      → Scene 1.2: Lab Morning
      → Scene 1.3: The Leap
    📝 Chapter 2: The Facility
      → Scene 2.1: Arrival
      ...
  📖 ACT 2: THE EXPERIMENT
    ...
  📖 ACT 3: THE WAR
    ...
```

**Interactions**:
- Click Act → expand/collapse chapters
- Click Chapter → expand/collapse scenes
- Click Scene → open in editor/viewer
- Right-click → Generate new scene, Delete, Rename

### Main Area: Current View

**Tabbed Interface**:
1. **Brainstorm** - NotebookLM setup, research materials, knowledge queries
2. **Write** - Scene editor with AI generation
3. **Compare** - Model comparison for current scene
4. **Enhance** - Scene enhancement tools
5. **Analyze** - Voice consistency, pacing, character analysis

---

## Priority Tasks for Cloud Agent (Overnight)

### Task 1: Scene Hierarchy Data Model (HIGH PRIORITY)
**File**: `factory/core/manuscript/structure.py`

Create data models for:
```python
class Scene:
    id: str
    title: str
    content: str
    word_count: int
    version: int
    created_at: datetime
    modified_at: datetime
    metadata: Dict

class Chapter:
    id: str
    title: str
    scenes: List[Scene]
    chapter_number: int

class Act:
    id: str
    title: str
    chapters: List[Chapter]
    act_number: int

class Manuscript:
    title: str
    acts: List[Act]
    project_path: Path

    # Methods
    def add_act(self, title: str) -> Act
    def add_chapter(self, act_id: str, title: str) -> Chapter
    def add_scene(self, chapter_id: str, title: str) -> Scene
    def get_scene(self, scene_id: str) -> Scene
    def save(self) -> bool
    def load(cls, project_path: Path) -> Manuscript
```

**Storage**: JSON files in `project/.manuscript/`
```
project/
  .manuscript/
    manifest.json          # Project metadata
    act_1/
      chapter_1/
        scene_1_1.json
        scene_1_2.json
      chapter_2/
        ...
    act_2/
      ...
```

---

### Task 2: Import Existing Explants Manuscript (HIGH PRIORITY)
**File**: `factory/tools/manuscript_importer.py`

Scan `/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/The Explants Series/Volume 1/` and create Manuscript structure from existing files.

**Logic**:
- Find all markdown files in PART folders
- Parse filenames to extract act/chapter/scene numbers
- Extract titles from filenames
- Read content from each file
- Create Manuscript object with all scenes
- Save to `project/.manuscript/`

**Success Criteria**:
- All existing scenes imported
- Hierarchy preserved (Acts → Chapters → Scenes)
- Scene content readable
- No data loss

---

### Task 3: Web UI - Left Sidebar Component (MEDIUM PRIORITY)
**File**: `webapp/frontend/components/sidebar.js`

Create collapsible tree view:
```javascript
class ManuscriptSidebar {
  constructor(manuscript) {
    this.manuscript = manuscript;
    this.selectedScene = null;
  }

  render() {
    // Generate HTML for acts/chapters/scenes
    // Make clickable and collapsible
  }

  onActClick(actId) { /* expand/collapse */ }
  onChapterClick(chapterId) { /* expand/collapse */ }
  onSceneClick(sceneId) { /* load scene in editor */ }
}
```

**Update**: `webapp/frontend/index.html` to include sidebar

---

### Task 4: Brainstorm Tab with NotebookLM Guide (MEDIUM PRIORITY)
**File**: `webapp/frontend/brainstorm.html`

Create landing page with:

**Section 1: Welcome**
- "Before you begin writing, gather your research materials"
- "NotebookLM helps you query your story universe"

**Section 2: Setup NotebookLM**
```
1. Go to https://notebooklm.google.com
2. Create new notebook: "[Your Story Title] Research"
3. Upload materials:
   - Character notes (PDF/MD)
   - Plot outlines
   - World-building docs
   - YouTube videos about themes
   - MP3 recordings of ideas
   - Relevant articles
4. Get NotebookLM notebook ID
5. Paste it in Writers Factory settings
```

**Section 3: Knowledge Base Query**
- Text input: "Ask a question about your story..."
- Button: "Query NotebookLM"
- Results display with sources

**Section 4: Existing Materials**
- Upload area for new files
- List of uploaded materials
- Quick actions: View, Delete, Re-upload to NotebookLM

---

### Task 5: Connect Real AI Agents (HIGH PRIORITY)
**File**: `webapp/backend/agents_integration.py`

Replace mock data with real agent calls:

```python
async def generate_scene_with_agent(
    prompt: str,
    model: str,
    context: Optional[str] = None
) -> str:
    """Generate scene using real AI agent."""
    agent = get_agent(model)

    # Build prompt with context
    full_prompt = build_scene_prompt(prompt, context)

    # Call agent
    response = await agent.generate(full_prompt)

    return response.text
```

**Connect to**:
- Scene generation endpoint
- Model comparison endpoint
- Scene enhancement endpoint

**Use existing**:
- `factory/agents/` implementations
- `config/credentials.json` API keys
- Agent pool from Phase 1

---

### Task 6: Model Comparison - Real Tournament (HIGH PRIORITY)
**File**: `webapp/backend/comparison_integration.py`

Connect web UI to Phase 1 tournament system:

```python
async def run_comparison_tournament(
    prompt: str,
    models: List[str]
) -> Dict[str, str]:
    """Run real model comparison using Phase 1 tournament."""
    from factory.tools.model_comparison import ModelComparisonTool

    tool = ModelComparisonTool(...)
    result = await tool.compare_models(prompt, models)

    return result
```

**Fix in Frontend**: Allow deselecting models
```javascript
function toggleModelSelection(modelId, cardElement) {
    const index = selectedModels.indexOf(modelId);

    if (index > -1) {
        // Deselect
        selectedModels.splice(index, 1);
        cardElement.classList.remove('selected');
    } else {
        // Select
        if (selectedModels.length >= 4) {
            alert('Maximum 4 models');
            return;
        }
        selectedModels.push(modelId);
        cardElement.classList.add('selected');
    }
}
```

---

### Task 7: Knowledge Router Integration (MEDIUM PRIORITY)
**File**: `webapp/backend/knowledge_integration.py`

Connect NotebookLM and Cognee:

```python
async def query_knowledge_base(
    question: str,
    notebook_id: Optional[str] = None
) -> Dict:
    """Query NotebookLM or Cognee."""
    from factory.knowledge.router import KnowledgeRouter

    router = KnowledgeRouter(...)

    if notebook_id:
        # Use NotebookLM
        result = await router.query_notebooklm(question, notebook_id)
    else:
        # Use Cognee (local)
        result = await router.query_cognee(question)

    return result
```

---

## Success Criteria for Overnight Work

After Cloud Agent completes tasks:

✅ **Data Model**: Can create/save/load Act/Chapter/Scene hierarchy
✅ **Import**: Existing Explants manuscript imported successfully
✅ **Sidebar**: Collapsible tree view shows Acts → Chapters → Scenes
✅ **Brainstorm Tab**: NotebookLM setup guide is clear and helpful
✅ **Real AI**: Model comparison generates actual text (not mock)
✅ **Model Selection**: Can select AND deselect models
✅ **Knowledge**: Can query NotebookLM or Cognee from UI

---

## Architecture After Overnight Work

```
writers-factory-core/
├── factory/
│   ├── core/
│   │   └── manuscript/          # 🆕 Scene hierarchy models
│   │       ├── structure.py
│   │       └── storage.py
│   ├── tools/
│   │   └── manuscript_importer.py  # 🆕 Import existing work
│   └── agents/                  # ✅ Already exists
│
├── webapp/
│   ├── backend/
│   │   ├── simple_app.py       # 🔄 Connect to real agents
│   │   ├── agents_integration.py     # 🆕
│   │   ├── comparison_integration.py # 🆕
│   │   └── knowledge_integration.py  # 🆕
│   └── frontend/
│       ├── index.html          # 🔄 Add sidebar
│       ├── brainstorm.html     # 🆕 Landing page
│       ├── components/
│       │   └── sidebar.js      # 🆕 Tree view
│       └── static/
│           └── app.js          # 🔄 Fix model deselection
│
└── project/
    └── .manuscript/            # 🆕 Imported scenes
        ├── manifest.json
        ├── act_1/
        ├── act_2/
        └── act_3/
```

---

## Future Enhancements (Not Overnight)

- Scene editor with live AI suggestions
- Voice consistency checker (compare to Mickey Voice Gold Standard)
- Auto-save as you type
- Version history for each scene
- Export to Word/PDF
- Collaboration features
- Mobile app

---

## Notes for Cloud Agent

**What You Have**:
- Phase 1 & 2 complete and tested (97 tests passing)
- 23 AI agents configured with API keys
- Existing Explants manuscript in markdown files
- Web UI framework already built

**What to Build**:
1. Data models for manuscript structure
2. Importer for existing scenes
3. Real agent integration (replace mock data)
4. Sidebar UI component
5. Brainstorm/landing page
6. Model selection fixes

**Don't Break**:
- Existing Phase 1 & 2 code
- Test suite (keep 97 tests passing)
- API key configuration
- Agent pool

**Test Everything**:
- Unit tests for new models
- Integration tests for importer
- API endpoint tests
- UI component tests

---

**Prioritize Tasks 1, 2, 5, 6** - These give immediate value:
- Import existing manuscript ✍️
- Real AI generation 🤖
- Working model comparison 🏆
- Proper data structure 📚

Good luck Cloud Agent! 🚀
