# Prompt for Cloud Agent: Sprint 9 - File-Based Editing

**Date**: November 14, 2025
**Priority**: 🔴 CRITICAL
**Budget**: $65 remaining, 4 days
**Repo**: https://github.com/gcharris/writers-factory-core

---

## Context

You've successfully completed Sprints 1-8, including:
- ✅ Sprint 7 Revision: TipTap editor (React 19 compatible)
- ✅ Sprint 8: Student polish (welcome modal, help panel, examples)

**However**, there's a CRITICAL architectural issue that must be fixed:

**User's Vision**: "Scrivener meets VS Code"
- File-based storage (like Scrivener + VS Code)
- Scenes as individual `.md` files (not embedded in JSON)
- Left panel file tree (see your project structure)
- Portable (works with Cursor AI, VS Code, any editor)

**Current Implementation**:
- Scenes embedded in `manuscript.json` (monolithic JSON file)
- No file tree UI
- Not portable (tied to Writers Factory)

**This is blocking** the user's novel workflow. They want to use Writers Factory to write their novel (The Explants, Volume 2) which is organized like this:

```
Explants/
├── manuscript/
│   ├── ACT_4/
│   │   ├── CHAPTER_1/
│   │   │   ├── 2.1.1 The Comfortable Cage.md
│   │   │   ├── 2.1.2 The Signal Probe.md
│   └── ACT_5/
├── reference/
│   └── Characters/
└── planning/
```

**Writers Factory needs to support this file structure.**

---

## Your Task

**Implement Sprint 9: File-Based Editing**

**Read the complete specification**:
👉 **[SPRINT_9_FILE_BASED_EDITING.md](SPRINT_9_FILE_BASED_EDITING.md)**

### Summary of Changes

**Transform storage from**:
```
project/
└── manuscript.json  ← All scenes embedded here (BAD)
```

**To**:
```
project/
├── manuscript.json          ← Index only (structure + metadata)
└── manuscript/
    ├── ACT_1/
    │   ├── CHAPTER_1/
    │   │   ├── scene-1-1-1 Opening.md  ← Scene content here
    │   │   └── scene-1-1-2 Inciting.md
    └── ACT_2/
```

### Key Changes

**1. Update `factory/core/manuscript/structure.py`**:
- Add `file_path: Optional[str]` to `Scene` dataclass

**2. Update `factory/core/manuscript/storage.py`**:
- `save()`: Write each scene to individual `.md` file
- `load()`: Read scene content from `.md` files
- `manifest.json`: Store only structure (no content)
- Add `_generate_scene_path()` helper

**3. Update `webapp/backend/simple_app.py`**:
- `/save_scene`: Write directly to `.md` file
- Add `/list_scene_files`: List all scene files (for future file tree)

**4. Create `factory/scripts/migrate_to_file_based.py`**:
- Migration script to convert existing projects

**5. Create `tests/test_file_based_storage.py`**:
- Test that saving creates `.md` files
- Test that loading reads from `.md` files
- Test that `manifest.json` excludes content

---

## Implementation Notes

### Path Format

Generate scene paths like this:
```
manuscript/ACT_{act_num}/CHAPTER_{chapter_num}/{scene_id} {title}.md
```

Example:
```
manuscript/ACT_1/CHAPTER_1/scene-1-1-1 Opening Scene.md
```

### Manifest Format (New)

**`manuscript.json`** should look like:
```json
{
  "title": "My Novel",
  "author": "Writer",
  "acts": [
    {
      "id": "act-1",
      "title": "Act 1",
      "chapters": [
        {
          "id": "chapter-1",
          "title": "Chapter 1",
          "scenes": [
            {
              "id": "scene-1-1-1",
              "title": "Opening Scene",
              "file_path": "manuscript/ACT_1/CHAPTER_1/scene-1-1-1 Opening Scene.md",
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

**Note**: No `"content"` field in scenes - content lives in `.md` files.

### Scene File Format

**`scene-1-1-1 Opening Scene.md`**:
```markdown
# 1.1.1 Opening Scene

[Scene content goes here - the actual prose]
```

Keep it simple - just a heading and content. Metadata is in `manifest.json`.

---

## Testing Checklist

Before marking complete, verify:

### Backend Storage
- [ ] Create new project → Creates `manuscript.json` + `manuscript/` folder
- [ ] Add scene → Creates `.md` file in correct location
- [ ] Edit scene → Updates `.md` file content
- [ ] Load project → Reads content from `.md` files
- [ ] `manifest.json` doesn't contain scene content

### API Endpoints
- [ ] `/save_scene` writes to `.md` file
- [ ] `/list_scene_files` returns file list
- [ ] No errors in console

### Migration
- [ ] Run migration script on test project
- [ ] Verify all scenes migrated to `.md` files
- [ ] Verify manifest updated to v2.0

### Tests
- [ ] All unit tests pass
- [ ] No regressions in existing functionality

---

## Success Criteria

**When complete**:

✅ **Projects are folders** (not just JSON files)
✅ **Scenes are individual `.md` files** (portable, editable outside Writers Factory)
✅ **Manifest is lightweight** (structure + metadata only)
✅ **Existing projects can migrate** (no data loss)
✅ **Tests pass** (no regressions)

**This enables**:
- User can open project folder in Cursor AI / VS Code
- User can edit `.md` files directly
- User can organize files into folders (Acts, Chapters)
- User can use git for version control
- User can backup by copying folder

---

## Estimated Effort

**Time**: 8-12 hours
**Cost**: ~$40-50 (of $65 remaining budget)
**Timeline**: Complete within 4 days

---

## Deliverables

When complete, create a commit message like:

```
Sprint 9: File-Based Editing (CRITICAL architecture change)

Transformed Writers Factory to file-based storage:
- Scenes stored as individual .md files
- manifest.json as index (structure only)
- Direct editing of Markdown files
- Portable (works with Cursor AI, VS Code)

Changes:
- Modified: factory/core/manuscript/structure.py (add file_path)
- Modified: factory/core/manuscript/storage.py (save/load .md files)
- Modified: webapp/backend/simple_app.py (write to files directly)
- Added: factory/scripts/migrate_to_file_based.py (migration)
- Added: tests/test_file_based_storage.py (tests)

Result: Projects now match "Scrivener × VS Code" vision

Files modified: 5
Lines added: ~800
Lines removed: ~200

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Questions?

If anything is unclear, check:
1. **[SPRINT_9_FILE_BASED_EDITING.md](SPRINT_9_FILE_BASED_EDITING.md)** - Complete specification
2. **User's Explants project structure** at: `/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/project/`
3. **Existing storage code**: `factory/core/manuscript/storage.py`

---

## Priority

🔴 **CRITICAL** - This is the most important change for Writers Factory.

Without this:
- ❌ User can't use Writers Factory for their novel
- ❌ Projects not portable
- ❌ Can't organize files properly
- ❌ Doesn't match "Scrivener × VS Code" vision

With this:
- ✅ User can write novel in Writers Factory
- ✅ Projects are portable (work with any editor)
- ✅ Files can be organized (Acts, Chapters, etc.)
- ✅ Matches vision perfectly

---

**Go build!** 🚀

This is the most important sprint yet. Take your time, test thoroughly, don't lose any data.

Budget: $65 remaining / 4 days
Target: Complete Sprint 9 within 2-3 days, leaving $15-20 for polish/fixes
