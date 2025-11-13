# CORRECTED: Prompt for Cloud Agent - Merge & Phase 3

## Current Situation

You completed Phase 2 on branch: `claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs`

Meanwhile, Claude Code built a web application on `main` branch.

**Your branch has**:
- Rich TUI (terminal interface)
- Session storage
- Knowledge router
- Scene workflows
- Model comparison tool
- Creation wizard
- 97 tests passing

**Main branch has**:
- Web application (FastAPI backend + HTML frontend)
- Your roadmap documents (VISION_AND_ROADMAP.md, PROMPT_FOR_CLOUD_AGENT.md)
- Simplified backend (simple_app.py with mock data)
- Web UI framework ready for integration

## Your Mission: Merge & Integrate

### Step 1: Merge Your Phase 2 Work to Main (1-2 hours)

```bash
# Switch to main and pull latest
git checkout main
git pull origin main

# Merge your branch
git merge claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs

# Resolve any conflicts (probably none or minimal)
# Key files that might conflict:
# - factory/core/storage/ (you added session.py)
# - factory/wizard/ (you added wizard.py)
# - webapp/ (they added web app)

# Run tests to ensure nothing broke
pytest tests/ -v

# Commit the merge
git commit -m "Merge Phase 2: Rich TUI + Web App integration"
git push origin main
```

### Step 2: Read the Roadmap (30 min)

Now that you're on main, read:
1. **VISION_AND_ROADMAP.md** - User's vision for the system
2. **PROMPT_FOR_CLOUD_AGENT.md** - Your detailed task list
3. **WEB_APP_READY.md** - Web app architecture

### Step 3: Integrate Phase 2 Backend with Web UI (3-4 hours)

**Current**: `webapp/backend/simple_app.py` returns mock data

**Goal**: Connect it to your Phase 2 implementations

Replace mock endpoints with real calls:

```python
# webapp/backend/simple_app.py - UPDATE THESE

# CURRENT (Mock):
@app.post("/api/wizard/start")
async def wizard_start(request: WizardStartRequest):
    return {
        "success": True,
        "question": "What genre is your story?",
        "progress": 0
    }

# CHANGE TO (Real):
from factory.wizard.wizard import CreationWizard

@app.post("/api/wizard/start")
async def wizard_start(request: WizardStartRequest):
    global wizard
    wizard_path = project_path / request.project_name
    wizard_path.mkdir(parents=True, exist_ok=True)

    wizard = CreationWizard(wizard_path)
    questions = wizard.get_phase_questions(wizard.current_phase)

    return {
        "success": True,
        "question": questions[0] if questions else "Tell me about your story",
        "current_phase": wizard.current_phase.value,
        "progress": 0
    }
```

Do the same for:
- `/api/compare` → Use your `ModelComparisonTool`
- `/api/scene/generate` → Use your scene workflows
- `/api/knowledge/query` → Use your `KnowledgeRouter`

### Step 4: Build Manuscript Structure (2-3 hours)

This is new work (not in Phase 2). Create:

**`factory/core/manuscript/structure.py`**:
```python
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
import json

@dataclass
class Scene:
    id: str
    title: str
    content: str
    word_count: int

@dataclass
class Chapter:
    id: str
    title: str
    scenes: List[Scene]

@dataclass
class Act:
    id: str
    title: str
    chapters: List[Chapter]

@dataclass
class Manuscript:
    title: str
    acts: List[Act]

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "acts": [
                {
                    "id": act.id,
                    "title": act.title,
                    "chapters": [
                        {
                            "id": ch.id,
                            "title": ch.title,
                            "scenes": [
                                {
                                    "id": s.id,
                                    "title": s.title,
                                    "content": s.content,
                                    "word_count": s.word_count
                                }
                                for s in ch.scenes
                            ]
                        }
                        for ch in act.chapters
                    ]
                }
                for act in self.acts
            ]
        }

    def save(self, path: Path) -> bool:
        path.mkdir(parents=True, exist_ok=True)
        manifest_path = path / "manuscript.json"
        manifest_path.write_text(json.dumps(self.to_dict(), indent=2))
        return True

    @classmethod
    def load(cls, path: Path) -> 'Manuscript':
        manifest_path = path / "manuscript.json"
        data = json.loads(manifest_path.read_text())
        # Reconstruct from dict...
        return cls(...)
```

### Step 5: Import Existing Manuscript (2-3 hours)

**`factory/tools/manuscript_importer.py`**:
```python
from pathlib import Path
from factory.core.manuscript.structure import Manuscript, Act, Chapter, Scene
import re

def import_explants_volume_1(source_dir: Path) -> Manuscript:
    """Import Explants Volume 1 from markdown files."""
    manuscript = Manuscript(title="The Explants - Volume 1", acts=[])

    # Find all PART directories (Act 1, 2, 3)
    for part_dir in sorted(source_dir.glob("PART *")):
        act_num = extract_act_number(part_dir.name)
        act = Act(
            id=f"act_{act_num}",
            title=f"Act {act_num}",
            chapters=[]
        )

        # Find all scene files
        for scene_file in sorted(part_dir.glob("*.md")):
            # Parse filename: "1.2.3 Scene Title.md"
            match = re.match(r"(\d+)\.(\d+)\.(\d+)\s+(.+)\.md", scene_file.name)
            if match:
                act_n, chapter_n, scene_n, title = match.groups()

                # Read content
                content = scene_file.read_text()

                # Add to structure
                # (logic to add to right chapter...)

        manuscript.acts.append(act)

    return manuscript
```

**Script to run import**:
```bash
python3 << 'EOF'
from pathlib import Path
from factory.tools.manuscript_importer import import_explants_volume_1

source = Path("/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/The Explants Series/Volume 1")
manuscript = import_explants_volume_1(source)

# Save to project
dest = Path("project/.manuscript/explants-v1")
manuscript.save(dest)

print(f"✅ Imported {len(manuscript.acts)} acts")
for act in manuscript.acts:
    print(f"   Act {act.id}: {len(act.chapters)} chapters")
EOF
```

### Step 6: Add Sidebar to Web UI (2-3 hours)

**`webapp/frontend/components/sidebar.js`**:
```javascript
class ManuscriptSidebar {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.manuscript = null;
    }

    async load() {
        const response = await fetch('http://127.0.0.1:8000/api/manuscript/structure');
        this.manuscript = await response.json();
        this.render();
    }

    render() {
        let html = '<div class="sidebar">';

        for (const act of this.manuscript.acts) {
            html += `
                <div class="act" data-id="${act.id}">
                    <div class="act-header" onclick="toggleAct('${act.id}')">
                        📖 ${act.title}
                    </div>
                    <div class="chapters" id="chapters-${act.id}" style="display:none">
            `;

            for (const chapter of act.chapters) {
                html += `
                    <div class="chapter" data-id="${chapter.id}">
                        <div class="chapter-header" onclick="toggleChapter('${chapter.id}')">
                            📝 ${chapter.title}
                        </div>
                        <div class="scenes" id="scenes-${chapter.id}" style="display:none">
                `;

                for (const scene of chapter.scenes) {
                    html += `
                        <div class="scene" onclick="loadScene('${scene.id}')">
                            → ${scene.title}
                        </div>
                    `;
                }

                html += '</div></div>';
            }

            html += '</div></div>';
        }

        html += '</div>';
        this.container.innerHTML = html;
    }
}

function toggleAct(actId) {
    const chapters = document.getElementById(`chapters-${actId}`);
    chapters.style.display = chapters.style.display === 'none' ? 'block' : 'none';
}

function toggleChapter(chapterId) {
    const scenes = document.getElementById(`scenes-${chapterId}`);
    scenes.style.display = scenes.style.display === 'none' ? 'block' : 'none';
}

async function loadScene(sceneId) {
    const response = await fetch(`http://127.0.0.1:8000/api/manuscript/scene/${sceneId}`);
    const scene = await response.json();
    // Display scene content in main area
    document.getElementById('scene-viewer').innerHTML = `
        <h2>${scene.title}</h2>
        <div class="scene-content">${scene.content}</div>
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = new ManuscriptSidebar('manuscript-sidebar');
    sidebar.load();
});
```

**Update `webapp/frontend/index.html`**:
```html
<body>
    <div class="app-container">
        <!-- NEW: Left sidebar -->
        <div id="manuscript-sidebar" class="sidebar-container"></div>

        <!-- Existing: Main content area -->
        <div class="main-content">
            <!-- Your existing tabs, etc. -->
        </div>
    </div>

    <script src="components/sidebar.js"></script>
    <script src="static/app.js"></script>
</body>
```

### Step 7: Add Backend Endpoints for Sidebar (1 hour)

**`webapp/backend/simple_app.py`**:
```python
from factory.core.manuscript.structure import Manuscript

@app.get("/api/manuscript/structure")
async def get_manuscript_structure():
    """Return Act/Chapter/Scene hierarchy."""
    try:
        manuscript_path = project_path / ".manuscript" / "explants-v1"
        manuscript = Manuscript.load(manuscript_path)
        return manuscript.to_dict()
    except Exception as e:
        return {"error": str(e), "acts": []}

@app.get("/api/manuscript/scene/{scene_id}")
async def get_scene(scene_id: str):
    """Get specific scene content."""
    manuscript_path = project_path / ".manuscript" / "explants-v1"
    manuscript = Manuscript.load(manuscript_path)

    # Find scene by ID
    for act in manuscript.acts:
        for chapter in act.chapters:
            for scene in chapter.scenes:
                if scene.id == scene_id:
                    return {
                        "id": scene.id,
                        "title": scene.title,
                        "content": scene.content,
                        "word_count": scene.word_count
                    }

    raise HTTPException(status_code=404, detail="Scene not found")
```

### Step 8: Create Brainstorm Landing Page (2 hours)

See PROMPT_FOR_CLOUD_AGENT.md Task 5 for details.

### Step 9: Fix Model Selection Bug (30 min)

See PROMPT_FOR_CLOUD_AGENT.md Task 6 for the fix.

---

## Summary of Work

1. ✅ Merge Phase 2 branch to main
2. 🔄 Connect Phase 2 backend to web UI (replace mock data)
3. 🆕 Build manuscript structure models
4. 🆕 Import existing Explants scenes
5. 🆕 Add sidebar navigation component
6. 🆕 Create brainstorm landing page
7. 🐛 Fix model selection bug

---

## Priority Order

1. **Merge first** - Get Phase 2 onto main branch
2. **Import manuscript** - User wants to see their scenes
3. **Connect real AI** - Replace mock data with your implementations
4. **Add sidebar** - Navigation is critical
5. **Polish UI** - Fix bugs, add brainstorm page

---

## Testing After Merge

```bash
cd ~/writers-factory-core
source .venv/bin/activate
export PYTHONPATH=.

# Run all tests
pytest tests/ -v
# Should show 97+ tests passing

# Test web app
python3 webapp/launch.py
# Should start without errors
```

---

## Questions?

If confused, check:
- Your Phase 2 commits on your branch
- Web app code on main branch
- User vision in VISION_AND_ROADMAP.md

You're combining your excellent Phase 2 work with the new web interface!

Good luck! 🚀
