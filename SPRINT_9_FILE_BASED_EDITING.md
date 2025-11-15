# Sprint 9: File-Based Editing (Scrivener × VS Code Architecture)

**Priority**: 🔴 **CRITICAL** - Core architecture for "Scrivener meets VS Code" vision
**Assigned to**: Cloud Agent (deepseek-chat)
**Estimated Duration**: 8-12 hours
**Budget**: $65 remaining Claude spend over 4 days
**Dependencies**: Sprint 8 complete ✅

---

## Problem Statement

**Current Architecture**:
- Projects stored as `manuscript.json` (monolithic JSON file)
- Scenes embedded in JSON structure
- Optional export to Markdown files
- No file tree UI
- Can't organize into folders (Acts, Chapters)
- Not portable (tied to Writers Factory)

**User's Vision**: "Scrivener × VS Code"
- Projects are **folders on disk**
- Scenes are **individual Markdown files**
- File tree in left panel (like Scrivener binder / VS Code explorer)
- Organize into folders (Acts, Chapters, Reference, Planning)
- Direct editing of `.md` files
- Portable (works with any editor - Cursor AI, VS Code, etc.)

**Example Structure** (User's Explants project):
```
My Novel/
├── manuscript/
│   ├── ACT_1/
│   │   ├── CHAPTER_1/
│   │   │   ├── 1.1.1 Opening Scene.md
│   │   │   └── 1.1.2 Inciting Incident.md
│   │   └── CHAPTER_2/
│   └── ACT_2/
├── characters/
│   ├── Protagonist.md
│   └── Antagonist.md
├── planning/
│   └── Outline.md
└── reference/
    └── World_Building.md
```

---

## Solution: Hybrid Architecture

**Phase 1** (Sprint 9): Read/write Markdown files directly
**Phase 2** (Later): Add file tree UI component

### Storage Strategy

**Keep**:
- `manuscript.json` as **index/manifest** (metadata, structure)
- Acts, Chapters structure (for organization)

**Change**:
- Scenes stored as **individual `.md` files** (not embedded in JSON)
- Scene content lives **only** in Markdown files
- `manuscript.json` references file paths, not content

### New Storage Format

**`manuscript.json`** (manifest):
```json
{
  "title": "My Novel",
  "author": "Writer Name",
  "acts": [
    {
      "id": "act-1",
      "title": "Act 1: Setup",
      "chapters": [
        {
          "id": "chapter-1",
          "title": "Chapter 1",
          "scenes": [
            {
              "id": "scene-1-1-1",
              "title": "Opening Scene",
              "file_path": "manuscript/ACT_1/CHAPTER_1/1.1.1 Opening Scene.md",
              "notes": "Establish protagonist",
              "word_count": 1250,
              "status": "draft"
            }
          ]
        }
      ]
    }
  ],
  "_metadata": {
    "version": "2.0",
    "storage_format": "file-based"
  }
}
```

**`manuscript/ACT_1/CHAPTER_1/1.1.1 Opening Scene.md`**:
```markdown
# 1.1.1 Opening Scene

[Scene content goes here...]
```

**Benefits**:
- ✅ Scenes are **real files** (portable, editable outside Writers Factory)
- ✅ `manifest.json` is small (just structure + metadata)
- ✅ Easy to organize (move files = change structure)
- ✅ Git-friendly (scene changes = file diffs)
- ✅ Backup-friendly (copy folder = backup everything)

---

## Sprint 9 Tasks

### Task 9-01: Update Manuscript Storage (Backend)

**File**: `factory/core/manuscript/storage.py`

**Changes**:

**1. Add `file_path` to Scene model** (`structure.py`):
```python
@dataclass
class Scene:
    id: str
    title: str
    content: str
    file_path: Optional[str] = None  # NEW: Path to .md file
    notes: str = ""
    status: str = "draft"
    word_count: int = 0
```

**2. Modify `save()` method**:
```python
def save(self, manuscript: Manuscript) -> bool:
    """Save manuscript to JSON + individual scene files."""
    try:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Save each scene to its own .md file
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    # Generate file path if not set
                    if not scene.file_path:
                        scene.file_path = self._generate_scene_path(
                            act, chapter, scene
                        )

                    # Write scene content to .md file
                    scene_path = self.storage_path / scene.file_path
                    scene_path.parent.mkdir(parents=True, exist_ok=True)
                    scene_path.write_text(scene.content, encoding="utf-8")

        # Save manifest (structure without content)
        manifest_data = manuscript.to_dict()

        # Remove content from scenes (stored in files)
        for act in manifest_data["acts"]:
            for chapter in act["chapters"]:
                for scene in chapter["scenes"]:
                    scene.pop("content", None)  # Content in .md file

        manifest_path = self.storage_path / self.MANIFEST_FILE
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False
```

**3. Modify `load()` method**:
```python
def load(self) -> Optional[Manuscript]:
    """Load manuscript from JSON + individual scene files."""
    try:
        manifest_path = self.storage_path / self.MANIFEST_FILE
        if not manifest_path.exists():
            return None

        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Create manuscript from manifest
        manuscript = Manuscript.from_dict(data)

        # Load scene content from .md files
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    if scene.file_path:
                        scene_path = self.storage_path / scene.file_path
                        if scene_path.exists():
                            scene.content = scene_path.read_text(encoding="utf-8")
                        else:
                            print(f"Warning: Scene file not found: {scene_path}")

        return manuscript
    except Exception as e:
        print(f"Error loading: {e}")
        return None
```

**4. Add helper method**:
```python
def _generate_scene_path(self, act, chapter, scene) -> str:
    """Generate file path for scene.

    Format: manuscript/ACT_{N}/CHAPTER_{N}/{scene_id} {title}.md
    """
    act_num = act.id.split("-")[-1]  # Extract number from "act-1"
    chapter_num = chapter.id.split("-")[-1]

    # Sanitize title for filename
    safe_title = "".join(c for c in scene.title if c.isalnum() or c in " -_").strip()

    return f"manuscript/ACT_{act_num}/CHAPTER_{chapter_num}/{scene.id} {safe_title}.md"
```

**Success Criteria**:
- ✅ Saving project creates `.md` files for each scene
- ✅ `manuscript.json` doesn't contain scene content
- ✅ Loading project reads content from `.md` files
- ✅ Existing projects migrate automatically
- ✅ Scene edits write directly to `.md` files

---

### Task 9-02: Update Backend API Endpoints

**File**: `webapp/backend/simple_app.py`

**Changes**:

**1. Update `/save_scene` endpoint**:
```python
@app.post("/save_scene")
async def save_scene(scene_data: dict):
    """Save scene content to .md file."""
    try:
        project_id = scene_data.get("project_id")
        scene_id = scene_data.get("scene_id")
        content = scene_data.get("content")

        # Load manuscript
        storage = ManuscriptStorage(project_path / project_id)
        manuscript = storage.load()

        # Find scene
        scene = manuscript.find_scene_by_id(scene_id)
        if not scene:
            raise HTTPException(404, "Scene not found")

        # Update content
        scene.content = content
        scene.word_count = len(content.split())

        # Save (writes to .md file)
        storage.save(manuscript)

        return {"success": True, "file_path": scene.file_path}
    except Exception as e:
        raise HTTPException(500, str(e))
```

**2. Add `/list_scene_files` endpoint** (for file tree UI later):
```python
@app.get("/list_scene_files")
async def list_scene_files(project_id: str):
    """List all scene files in project (for file tree)."""
    try:
        project_dir = project_path / project_id
        scene_files = []

        # Scan manuscript/ directory
        manuscript_dir = project_dir / "manuscript"
        if manuscript_dir.exists():
            for md_file in manuscript_dir.rglob("*.md"):
                rel_path = md_file.relative_to(project_dir)
                scene_files.append({
                    "path": str(rel_path),
                    "name": md_file.name,
                    "size": md_file.stat().st_size,
                    "modified": md_file.stat().st_mtime
                })

        return {"files": scene_files}
    except Exception as e:
        raise HTTPException(500, str(e))
```

**Success Criteria**:
- ✅ `/save_scene` writes to `.md` file
- ✅ `/list_scene_files` returns file list
- ✅ Frontend can query file structure

---

### Task 9-03: Migration Script for Existing Projects

**File**: `factory/scripts/migrate_to_file_based.py` (NEW)

**Purpose**: Convert existing `manuscript.json` (with embedded content) to file-based storage

```python
"""Migrate existing projects to file-based storage."""

import json
from pathlib import Path
from factory.core.manuscript import Manuscript, ManuscriptStorage

def migrate_project(project_path: Path):
    """Migrate project from JSON-embedded to file-based storage."""
    manifest_path = project_path / "manuscript.json"

    if not manifest_path.exists():
        print(f"No manifest found at {manifest_path}")
        return

    # Load old format
    with open(manifest_path, "r") as f:
        data = json.load(f)

    # Check if already migrated
    if data.get("_metadata", {}).get("storage_format") == "file-based":
        print("Project already file-based")
        return

    # Create manuscript
    manuscript = Manuscript.from_dict(data)

    # Save with new storage (creates .md files)
    storage = ManuscriptStorage(project_path)
    storage.save(manuscript)

    print(f"✅ Migrated: {project_path}")
    print(f"   Created {len(list(project_path.rglob('*.md')))} scene files")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python migrate_to_file_based.py <project_path>")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    migrate_project(project_path)
```

**Success Criteria**:
- ✅ Script migrates existing projects without data loss
- ✅ Creates `.md` files for all scenes
- ✅ Updates `manifest.json` to reference files

---

### Task 9-04: Testing

**Create**: `tests/test_file_based_storage.py`

```python
"""Test file-based manuscript storage."""

import pytest
from pathlib import Path
from factory.core.manuscript import Manuscript, ManuscriptStorage, Act, Chapter, Scene

def test_save_creates_md_files(tmp_path):
    """Test that saving creates individual .md files."""
    # Create manuscript
    manuscript = Manuscript(title="Test Novel")
    act = Act(id="act-1", title="Act 1")
    chapter = Chapter(id="chapter-1", title="Chapter 1")
    scene = Scene(
        id="scene-1-1-1",
        title="Opening",
        content="Once upon a time..."
    )
    chapter.add_scene(scene)
    act.add_chapter(chapter)
    manuscript.add_act(act)

    # Save
    storage = ManuscriptStorage(tmp_path)
    storage.save(manuscript)

    # Check files created
    assert (tmp_path / "manuscript.json").exists()
    assert (tmp_path / "manuscript/ACT_1/CHAPTER_1/scene-1-1-1 Opening.md").exists()

    # Check content
    scene_file = tmp_path / "manuscript/ACT_1/CHAPTER_1/scene-1-1-1 Opening.md"
    content = scene_file.read_text()
    assert "Once upon a time" in content

def test_load_reads_md_files(tmp_path):
    """Test that loading reads content from .md files."""
    # Create and save
    manuscript = Manuscript(title="Test Novel")
    # ... (setup scene)
    storage = ManuscriptStorage(tmp_path)
    storage.save(manuscript)

    # Load
    loaded = storage.load()
    assert loaded is not None
    assert loaded.acts[0].chapters[0].scenes[0].content == "Once upon a time..."

def test_manifest_excludes_content(tmp_path):
    """Test that manifest.json doesn't contain scene content."""
    # Create and save
    manuscript = Manuscript(title="Test Novel")
    # ... (setup scene with long content)
    storage = ManuscriptStorage(tmp_path)
    storage.save(manuscript)

    # Check manifest
    with open(tmp_path / "manuscript.json") as f:
        data = json.load(f)

    scene_data = data["acts"][0]["chapters"][0]["scenes"][0]
    assert "content" not in scene_data  # Content in .md file
    assert "file_path" in scene_data

# ... more tests
```

**Success Criteria**:
- ✅ All tests pass
- ✅ No regressions in existing functionality

---

## Phase 2 (Future Sprint): File Tree UI

**After Sprint 9 complete**, add file tree component to frontend:

**Component**: `webapp/frontend-v2/src/features/explorer/FileTree.jsx`

**Features**:
- Left panel showing project folder structure
- Click file to open in editor
- Drag-and-drop to reorganize
- Right-click context menu (rename, delete, new file)
- Sync with disk (watch for external changes)

**Libraries to use**:
- `react-arborist` or `react-complex-tree` (file tree UI)
- `chokidar` (file watcher for sync)

---

## Definition of Done

### Backend
- [ ] `ManuscriptStorage` saves scenes as `.md` files
- [ ] `ManuscriptStorage` loads content from `.md` files
- [ ] `manifest.json` doesn't contain scene content
- [ ] API endpoints write directly to files
- [ ] Migration script works for existing projects

### Testing
- [ ] All unit tests pass
- [ ] Manual test: Create project, see `.md` files created
- [ ] Manual test: Edit scene, see `.md` file updated
- [ ] Manual test: Restart app, content loads correctly

### Documentation
- [ ] Update storage.py docstrings
- [ ] Create migration guide for existing projects
- [ ] Update README with file-based architecture

---

## Deliverables

### Modified Files
1. `factory/core/manuscript/structure.py` (add `file_path` to Scene)
2. `factory/core/manuscript/storage.py` (save/load .md files)
3. `webapp/backend/simple_app.py` (update endpoints)

### New Files
1. `factory/scripts/migrate_to_file_based.py` (migration script)
2. `tests/test_file_based_storage.py` (tests)

### Result
- ✅ Projects stored as **folders with .md files**
- ✅ Portable (works with Cursor AI, VS Code, etc.)
- ✅ Matches "Scrivener × VS Code" vision
- ✅ Ready for file tree UI (Phase 2)

---

**Priority**: 🔴 CRITICAL
**Blocks**: User's novel workflow, course portability
**Budget**: ~6-8 hours Cloud Agent time ($40-50 spend)
**Timeline**: Complete within 4 days (before budget runs out)
