# Prompt for Cloud Agent - Phase 3 Development

## Your Mission

Build the core functionality for Writers Factory web application based on user feedback. The UI framework exists but returns mock data. You need to:

1. Create manuscript structure (Acts → Chapters → Scenes)
2. Import existing Explants manuscript
3. Connect real AI agents (replace mock responses)
4. Build sidebar navigation component
5. Create brainstorming/NotebookLM landing page

## What's Already Done ✅

- **Phase 1 & 2**: Tournament system + Rich TUI (97 tests passing)
- **Web UI**: FastAPI backend + HTML/JS frontend (functional with mock data)
- **23 AI Models**: Configured with API keys in `config/credentials.json`
- **Agents**: `factory/agents/` implementations ready to use

## Start Here

Read these files in order:

1. **[VISION_AND_ROADMAP.md](VISION_AND_ROADMAP.md)** - Complete specification with 7 tasks
2. **[READY_FOR_TESTING.md](READY_FOR_TESTING.md)** - Current system capabilities
3. **[WEB_APP_READY.md](WEB_APP_READY.md)** - Web app architecture

## Priority Tasks (Do in This Order)

### Task 1: Scene Hierarchy Data Model (2-3 hours)

**Goal**: Create Python data models for manuscript structure

**Files to Create**:
- `factory/core/manuscript/__init__.py`
- `factory/core/manuscript/structure.py` - Scene, Chapter, Act, Manuscript classes
- `factory/core/manuscript/storage.py` - Save/load to JSON
- `tests/test_manuscript_structure.py` - Unit tests

**Data Model**:
```python
class Scene:
    id: str
    title: str
    content: str
    word_count: int

class Chapter:
    id: str
    title: str
    scenes: List[Scene]

class Act:
    id: str
    title: str
    chapters: List[Chapter]

class Manuscript:
    title: str
    acts: List[Act]

    def add_act(self, title: str) -> Act
    def add_chapter(self, act_id: str, title: str) -> Chapter
    def add_scene(self, chapter_id: str, title: str) -> Scene
    def save(self) -> bool
    @classmethod
    def load(cls, project_path: Path) -> Manuscript
```

**Storage Format**: JSON in `project/.manuscript/`

**Success Criteria**:
- Can create Act/Chapter/Scene hierarchy
- Can save to JSON and load back
- Unit tests pass

---

### Task 2: Import Existing Manuscript (2-3 hours)

**Goal**: Scan existing Explants markdown files and import into structure

**Path to Scan**:
```
/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/The Explants Series/Volume 1/
```

**Files to Create**:
- `factory/tools/manuscript_importer.py`
- `scripts/import_explants.py` - CLI script to run import
- `tests/test_manuscript_importer.py`

**Logic**:
1. Find all `.md` files in `PART */` directories
2. Parse filenames: `1.2.3 Scene Title.md` → Act 1, Chapter 2, Scene 3
3. Extract scene content from file
4. Create Manuscript object with all scenes
5. Save to `project/.manuscript/explants-volume-1/`

**Success Criteria**:
- All existing scenes imported
- Hierarchy preserved (Acts → Chapters → Scenes)
- No data loss
- Can run: `python3 scripts/import_explants.py`

---

### Task 3: Connect Real AI Agents (3-4 hours)

**Goal**: Replace mock data in backend with actual AI model calls

**Files to Modify**:
- `webapp/backend/simple_app.py` - Update endpoints
- Create `webapp/backend/agent_integration.py` - Helper functions

**Endpoints to Fix**:
1. `/api/compare` - Use `ModelComparisonTool` from Phase 1
2. `/api/scene/generate` - Call real agent with prompt
3. `/api/scene/enhance` - Call real agent for enhancement

**Use Existing Code**:
```python
from factory.tools.model_comparison import ModelComparisonTool
from factory.core.config.loader import load_agent_config, get_api_key

# Example: Real model comparison
async def compare_models_real(prompt: str, models: List[str]):
    tool = ModelComparisonTool(...)
    result = await tool.compare_models(prompt, models)
    return result
```

**Success Criteria**:
- Model comparison returns actual AI text (not mock)
- Scene generation produces real content
- Costs are tracked accurately
- All 23 models work

---

### Task 4: Sidebar Component (2-3 hours)

**Goal**: Add collapsible tree navigation to web UI

**Files to Create**:
- `webapp/frontend/components/sidebar.js`
- `webapp/frontend/styles/sidebar.css`

**Files to Modify**:
- `webapp/frontend/index.html` - Add sidebar div
- `webapp/backend/simple_app.py` - Add `/api/manuscript/structure` endpoint

**Features**:
- Click Act → expand/collapse chapters
- Click Chapter → expand/collapse scenes
- Click Scene → load in main area
- Highlight currently selected scene

**API Endpoint**:
```python
@app.get("/api/manuscript/structure")
async def get_manuscript_structure():
    """Return Act/Chapter/Scene hierarchy as JSON."""
    manuscript = Manuscript.load(project_path)
    return manuscript.to_dict()
```

**Success Criteria**:
- Sidebar loads on page load
- Acts/Chapters/Scenes clickable
- Expand/collapse works
- Looks clean and organized

---

### Task 5: Brainstorm Landing Page (2 hours)

**Goal**: Create "Before You Begin" page with NotebookLM guide

**Files to Create**:
- `webapp/frontend/brainstorm.html` - New page
- `webapp/frontend/styles/brainstorm.css`

**Update**: Make this the default landing page (not wizard)

**Sections**:
1. **Welcome** - "Gather your research before writing"
2. **Setup NotebookLM** - Step-by-step guide with links
3. **Upload Materials** - Drag-drop area for PDFs, notes, etc.
4. **Query Knowledge** - Text input to ask questions
5. **Continue to Writing** - Button to enter main workspace

**Success Criteria**:
- Renders beautifully
- NotebookLM instructions are clear
- Can upload files
- Query box connects to knowledge endpoint

---

### Task 6: Fix Model Selection (30 min)

**Goal**: Allow users to deselect models in comparison tab

**File to Fix**: `webapp/frontend/static/app.js`

**Current Bug**: Can select but not deselect model cards

**Fix**:
```javascript
function toggleModelSelection(modelId, cardElement) {
    const index = selectedModels.indexOf(modelId);

    if (index > -1) {
        // Already selected - remove it
        selectedModels.splice(index, 1);
        cardElement.classList.remove('selected');
    } else {
        // Not selected - add it
        if (selectedModels.length >= 4) {
            alert('Maximum 4 models');
            return;
        }
        selectedModels.push(modelId);
        cardElement.classList.add('selected');
    }
}
```

**Success Criteria**:
- Click to select model (adds to list)
- Click again to deselect (removes from list)
- Visual feedback (selected class toggle)

---

### Task 7: Knowledge Router (2 hours)

**Goal**: Connect NotebookLM query to backend

**Files to Modify**:
- `webapp/backend/simple_app.py` - Update `/api/knowledge/query`
- Integrate with `factory/knowledge/router.py`

**Current**: Returns mock data
**Target**: Query Cognee or NotebookLM

**Implementation**:
```python
from factory.knowledge.router import KnowledgeRouter

@app.post("/api/knowledge/query")
async def knowledge_query(request: dict):
    router = KnowledgeRouter(...)

    question = request.get('question')
    notebook_id = request.get('notebook_id')  # Optional

    if notebook_id:
        result = await router.query_notebooklm(question, notebook_id)
    else:
        result = await router.query_cognee(question)

    return {
        "success": True,
        "answer": result.get('answer'),
        "sources": result.get('sources', [])
    }
```

**Success Criteria**:
- Queries return real answers (not mock)
- NotebookLM integration works if ID provided
- Cognee fallback works
- Sources/citations displayed

---

## Testing Requirements

After completing each task:

1. **Write unit tests** - Add to `tests/` directory
2. **Run test suite** - Must maintain 97+ tests passing
3. **Manual test in browser** - Launch web app and verify
4. **Document changes** - Update relevant README if needed

**Run tests**:
```bash
cd ~/writers-factory-core
source .venv/bin/activate
export PYTHONPATH=.
pytest tests/ -v
```

---

## File Locations Reference

```
writers-factory-core/
├── factory/
│   ├── core/
│   │   ├── manuscript/          # Task 1: NEW
│   │   └── config/
│   │       ├── agents.yaml      # 23 models configured
│   │       └── loader.py        # Config utilities
│   ├── tools/
│   │   ├── manuscript_importer.py  # Task 2: NEW
│   │   └── model_comparison.py     # Phase 1: EXISTS
│   ├── knowledge/
│   │   └── router.py            # Phase 2: EXISTS
│   └── agents/                  # Phase 1: EXISTS
│
├── webapp/
│   ├── backend/
│   │   └── simple_app.py        # Tasks 3,4,7: MODIFY
│   └── frontend/
│       ├── index.html           # Task 4: MODIFY
│       ├── brainstorm.html      # Task 5: NEW
│       ├── components/
│       │   └── sidebar.js       # Task 4: NEW
│       └── static/
│           └── app.js           # Task 6: FIX
│
├── scripts/
│   └── import_explants.py       # Task 2: NEW
│
├── tests/                       # Add tests for all tasks
└── config/
    └── credentials.json         # 14 API keys configured
```

---

## Important Notes

### Don't Break Existing Code
- Phase 1 & 2 are complete and working
- Keep all 97 tests passing
- Don't modify agent pool or credentials

### Use Existing Infrastructure
- Agent implementations: `factory/agents/`
- Model comparison: `factory/tools/model_comparison.py`
- Knowledge router: `factory/knowledge/router.py`
- Config loader: `factory/core/config/loader.py`

### User's Manuscript Location
```
/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/The Explants Series/Volume 1/
```

Contains:
- PART 1/ (Act 1 scenes)
- PART 2/ (Act 2 scenes)
- PART 3/ (Act 3 scenes)

Each scene is a markdown file with naming pattern: `1.2.3 Scene Title.md`

### API Keys
All configured in `.env` and `config/credentials.json`:
- Anthropic (Claude models)
- OpenAI (GPT models)
- Google (Gemini models)
- Chinese LLMs (Qwen, DeepSeek, etc.)

---

## Success Criteria for Completion

After finishing all tasks, the system should:

✅ Import existing Explants manuscript into hierarchy
✅ Display Acts → Chapters → Scenes in sidebar
✅ Click scenes to navigate
✅ Model comparison generates real AI text
✅ Scene generation produces actual content
✅ Brainstorm page guides NotebookLM setup
✅ Knowledge queries return real answers
✅ Can select AND deselect models
✅ All tests still passing (97+)
✅ Web app runs without errors

---

## Commit Strategy

Make atomic commits for each task:

```bash
git add -A
git commit -m "Task 1: Add manuscript structure data models

- Created Scene, Chapter, Act, Manuscript classes
- Implemented JSON storage
- Added unit tests (8 tests passing)
- Can create/save/load hierarchy

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Questions? Check These First

- **Architecture**: Read `VISION_AND_ROADMAP.md`
- **Current status**: Check `READY_FOR_TESTING.md`
- **Web app**: See `WEB_APP_READY.md`
- **Phase 2 work**: Review `PHASE_2_IMPLEMENTATION_REPORT.md`
- **Agent config**: Look at `factory/core/config/agents.yaml`

---

## Estimated Time: 12-16 hours

- Task 1: 2-3 hours
- Task 2: 2-3 hours
- Task 3: 3-4 hours
- Task 4: 2-3 hours
- Task 5: 2 hours
- Task 6: 30 min
- Task 7: 2 hours

**Prioritize: Tasks 1, 2, 3, 6** - These give immediate user value.

---

**Good luck! Build something amazing overnight.** 🚀
