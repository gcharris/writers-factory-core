# Handoff Prompt for New Claude Code Agent

**Date**: November 14, 2025
**Context**: User is switching to Writers Factory codebase for testing and bug finding
**Your Role**: Help user test, debug, and improve Writers Factory for personal use

---

## 📋 Quick Context

I'm G.C. Harris, a novelist writing *The Explants* trilogy. I've just completed **Sprint 10** of Writers Factory - an AI-augmented writing environment that combines Scrivener's organization + VS Code's interface + AI assistance.

**My immediate goals**:
1. **Test Writers Factory** by using it for real work (writing The Explants Volume 2)
2. **Find and fix bugs** over the next few days
3. **Eventually test with 2-3 students** to gather feedback
4. **Decide if we package as desktop app** for January 2025 course

**You're helping me** with Phase 1: Personal testing and bug fixing.

---

## 🏗️ What Writers Factory Is

**Vision**: "Scrivener meets VS Code meets AI"

**Core Architecture**:
- **Backend**: Python FastAPI (port 8000)
- **Frontend**: React 19 + Vite (port 5173)
- **Storage**: File-based (scenes as individual `.md` files)
- **AI**: Multi-model support (Claude, GPT-4, Gemini, Ollama)

**Key Features**:
- Three-panel layout (File Tree | Editor | AI Tools)
- File-based manuscript storage (portable, editable in any editor)
- TipTap WYSIWYM markdown editor
- Scene creation/editing/deletion via UI
- AI scene generation and enhancement
- Tournament mode (compare multiple AI models)
- Character depth analysis
- Cost tracking for AI usage

---

## 🎯 Sprint History (What's Been Built)

### Completed Sprints

**Sprint 1-2**: Foundation
- Project initialization
- Basic agent system

**Sprint 3**: Ollama Integration (A+)
- Local model support
- Cost-free AI generation

**Sprint 4**: Brainstorm Landing Page (A+)
- Idea capture and organization

**Sprint 5**: Character Development Panel (A+)
- Deep character analysis
- Contradiction detection

**Sprint 6**: MCP Server (A+)
- Model Context Protocol integration
- 763 lines, 10 tools

**Sprint 7R**: TipTap Editor (A+)
- Replaced Toast UI Editor (React 17 incompatible)
- Writer-first WYSIWYM editor
- React 19 compatible
- 30% smaller bundle

**Sprint 8**: Student Polish (A+)
- Welcome modal
- Help panel with searchable topics
- Quick tips

**Sprint 9**: File-Based Storage (A+) - **CRITICAL**
- Transformed from JSON-embedded to file-based
- Scenes stored as individual `.md` files
- `manifest.json` as index (structure + metadata only)
- Portable (edit in VS Code, Typora, Cursor AI)
- 895 lines added/modified

**Sprint 10**: Three-Panel Layout + File Operations (A+) - **JUST COMPLETED**
- Three-panel layout (File Tree | Editor | AI Tools)
- Right-click context menus
- Inline scene rename
- Scene creation/deletion
- Toast notifications
- 438 lines added/modified

### Recent Additions (Today)

**Licensing & Governance**:
- Apache 2.0 LICENSE (commercial use allowed)
- CODE_OF_CONDUCT.md
- CONTRIBUTORS.md
- Contributor License Agreement (CLA)
- LICENSING_SUMMARY.md

**Easy Launch System**:
- `setup.sh` - One-time dependency installation
- `start.sh` - One-command launch (backend + frontend)
- Health check endpoint (`/health`)
- Automatic browser opening
- Clean shutdown on Ctrl+C

**Documentation**:
- QUICK_START.md - Complete setup guide
- TESTING_PLAN.md - 3-phase rollout plan
- All sprint review documents (CLOUD_AGENT_SPRINT_*_REVIEW.md)

---

## 📂 Repository Structure

```
writers-factory-core/
├── factory/                    # Core Python backend
│   ├── core/
│   │   ├── manuscript/         # Manuscript storage system
│   │   │   ├── structure.py    # Manuscript, Act, Chapter, Scene dataclasses
│   │   │   └── storage.py      # File-based storage (Sprint 9)
│   │   ├── agents/             # AI model integrations
│   │   │   ├── base_agent.py
│   │   │   ├── ollama_agent.py
│   │   │   └── character_analyzer.py
│   │   └── config/             # Agent configuration
│   ├── workflows/              # Multi-agent workflows
│   ├── knowledge/              # Knowledge base systems
│   └── venv/                   # Python virtual environment
│
├── webapp/
│   ├── backend/
│   │   ├── simple_app.py       # FastAPI server (main backend)
│   │   └── agent_integration.py
│   └── frontend-v2/            # React frontend
│       ├── src/
│       │   ├── features/
│       │   │   ├── explorer/
│       │   │   │   └── FileTree.jsx       # File tree navigation (Sprint 10)
│       │   │   ├── editor/
│       │   │   │   └── SceneEditor.jsx    # TipTap editor (Sprint 7R)
│       │   │   ├── ai-tools/
│       │   │   │   └── AIToolsPanel.jsx   # AI tools sidebar
│       │   │   ├── character/
│       │   │   │   └── CharacterPanel.jsx # Character analysis
│       │   │   └── help/
│       │   │       └── HelpPanel.jsx      # Help system
│       │   ├── components/
│       │   │   └── layout/
│       │   │       └── PanelLayout.jsx    # Three-panel layout
│       │   └── App.jsx                    # Main application
│       └── node_modules/
│
├── project/                    # User's manuscripts stored here
│   └── .manuscript/
│       └── [project-name]/
│           ├── manifest.json   # Structure + metadata (NO content)
│           └── scenes/         # Individual .md files
│               ├── act-1/
│               │   └── chapter-1/
│               │       └── scene-abc123.md
│               └── act-2/
│
├── .tmp/                       # Runtime logs
│   ├── backend.log
│   ├── frontend.log
│   ├── backend.pid
│   └── frontend.pid
│
├── setup.sh                    # First-time setup script
├── start.sh                    # Launch script (run every time)
├── QUICK_START.md             # User guide
├── TESTING_PLAN.md            # Testing strategy
└── LICENSE                     # Apache 2.0
```

---

## 🔧 Technical Architecture

### File-Based Storage (Sprint 9)

**Key Concept**: Scenes are NOT stored in JSON - they're individual `.md` files

**Storage Format**:

`manifest.json` (structure only):
```json
{
  "title": "My Novel",
  "acts": [
    {
      "id": "act-1",
      "chapters": [
        {
          "id": "chapter-1",
          "scenes": [
            {
              "id": "scene-abc123",
              "title": "Opening Scene",
              "file_path": "scenes/act-1/chapter-1/scene-abc123.md",
              "word_count": 1250,
              "status": "draft",
              "notes": "Establish protagonist"
              // NO "content" field - content is in .md file
            }
          ]
        }
      ]
    }
  ],
  "_metadata": {
    "version": "2.0",
    "storage_type": "file_based"
  }
}
```

`scenes/act-1/chapter-1/scene-abc123.md`:
```markdown
---
id: scene-abc123
title: Opening Scene
act: Act 1
chapter: Chapter 1
word_count: 1250
---

## Notes

Establish protagonist

---

[Actual scene content goes here - the prose]
```

**Key Methods** (in `factory/core/manuscript/storage.py`):
- `save(manuscript)` - Writes each scene to individual `.md` file, saves manifest WITHOUT content
- `load()` - Reads manifest, loads scene content from `.md` files
- `save_scene(scene_id, content)` - Updates individual scene file
- `_save_scene_file()` - Writes scene with metadata header
- `_extract_content_from_md()` - Extracts content from .md file (skips metadata)

### Backend API (webapp/backend/simple_app.py)

**Key Endpoints**:

**Manuscript Management**:
- `GET /api/manuscript/tree` - Get manuscript structure for file tree
- `GET /api/manuscript/files` - List all scene `.md` files (Sprint 10)

**Scene Operations**:
- `GET /api/scene/{scene_id}` - Get specific scene
- `PUT /api/scene/{scene_id}` - Update scene (writes to `.md` file)
- `POST /api/scene/create` - Create new scene (Sprint 10)
- `PUT /api/scene/{scene_id}/rename` - Rename scene (Sprint 10)
- `DELETE /api/scene/{scene_id}` - Delete scene (Sprint 10)

**AI Generation**:
- `POST /api/scene/generate` - Generate scene from outline
- `POST /api/scene/enhance` - Enhance existing prose
- `POST /api/compare` - Tournament mode (compare multiple models)

**Character Analysis**:
- `POST /api/character/analyze` - Analyze character depth

**Health**:
- `GET /health` - Health check (for launcher script)

### Frontend Components

**Main Components**:
- `App.jsx` - Application entry point, integrates three-panel layout
- `PanelLayout.jsx` - Resizable three-panel container
- `FileTree.jsx` - File explorer (create/rename/delete scenes)
- `SceneEditor.jsx` - TipTap markdown editor
- `AIToolsPanel.jsx` - AI tools sidebar
- `CharacterPanel.jsx` - Character analysis
- `HelpPanel.jsx` - Searchable help system

**State Management**:
- React Query for server state
- React hooks for local state
- Toast notifications (sonner library)

---

## 🚀 How to Launch (For Testing)

**First time only**:
```bash
cd /Users/gch2024/writers-factory-core
./setup.sh
```

**Every time**:
```bash
./start.sh
```

**What happens**:
1. Backend starts (Python FastAPI on port 8000)
2. Frontend starts (React + Vite on port 5173)
3. Browser opens to http://localhost:5173
4. Ready to write!

**Stop**:
- Press `Ctrl+C` in terminal

**Logs**:
- Backend: `.tmp/backend.log`
- Frontend: `.tmp/frontend.log`

---

## 🎯 Your Immediate Tasks

### Task 1: Inventory and Understand (First Session)

**Your mission**: Do a complete code review and create an inventory

**Steps**:
1. **Read the sprint reviews** to understand what was built:
   - `CLOUD_AGENT_SPRINT_9_REVIEW.md` - File-based storage
   - `CLOUD_AGENT_SPRINT_10_REVIEW.md` - Three-panel layout

2. **Explore the codebase** using the Task tool:
   - "Explore the file-based storage implementation in factory/core/manuscript/"
   - "Explore the React frontend components in webapp/frontend-v2/"
   - "Find all API endpoints in the backend"
   - "Understand how scenes are created/saved/loaded"

3. **Create an inventory document** (`CODEBASE_INVENTORY.md`):
   - List all major components
   - Describe data flow (user action → API → storage → response)
   - Identify potential bug areas
   - Document dependencies and their versions

4. **Verify the build works**:
   ```bash
   # Backend
   cd factory
   source venv/bin/activate
   cd ../webapp/backend
   python simple_app.py  # Should start without errors

   # Frontend (in another terminal)
   cd webapp/frontend-v2
   npm run dev  # Should build and start
   ```

### Task 2: Testing Support (Ongoing)

**Your role**: Help user find and fix bugs as they test

**When user reports a bug**:
1. **Reproduce it** - Ask for exact steps
2. **Check logs** - Look at `.tmp/backend.log` and `.tmp/frontend.log`
3. **Find the code** - Locate the relevant component/endpoint
4. **Diagnose** - Identify the root cause
5. **Suggest fix** - Provide code fix or workaround
6. **Verify fix** - Ensure fix works and doesn't break other features

**Common areas to watch**:
- File creation/deletion (ensure `.md` files are properly created/removed)
- Scene rename (ensure both manifest and file are updated)
- External editing (ensure changes sync when user edits `.md` in VS Code)
- Auto-save (ensure content isn't lost)
- AI generation errors (API key issues, model availability)
- CORS errors (frontend can't reach backend)

### Task 3: Bug Documentation

**Create `BUGS.md`** to track issues:

```markdown
# Writers Factory Bugs

## Critical (P0) - Fix Immediately
- [ ] BUG-001: [Description]
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Error logs
  - Proposed fix

## High Priority (P1) - Fix This Week
...

## Medium Priority (P2) - Fix Before Course
...

## Low Priority (P3) - Nice to Have
...
```

### Task 4: Feature Understanding

**User will ask questions like**:
- "How does scene deletion work?"
- "Why isn't my scene saving?"
- "Can I import my existing Explants scenes?"

**Your responses should**:
- Explain the relevant code/architecture
- Show exact file paths and line numbers
- Suggest solutions or workarounds
- Consider edge cases

---

## 🐛 Known Potential Issues to Watch For

Based on Sprint 10 implementation:

### File Operations
- ❓ Does scene deletion properly delete both manifest entry AND `.md` file?
- ❓ Does rename update both scene title in manifest AND `.md` file metadata?
- ❓ Do concurrent edits (user edits in Writers Factory + external editor) conflict?
- ❓ Are file paths properly sanitized (special characters, long names)?

### Storage
- ❓ Does manifest correctly exclude scene content?
- ❓ Do scenes load properly when app restarts?
- ❓ Is word count calculation accurate?
- ❓ Does auto-save work reliably?

### UI/UX
- ❓ Do toast notifications appear and dismiss correctly?
- ❓ Does file tree refresh after operations?
- ❓ Is context menu properly positioned?
- ❓ Do keyboard shortcuts work?

### Performance
- ❓ Is startup time acceptable (<5 seconds)?
- ❓ Does file tree lag with many scenes (100+)?
- ❓ Does editor handle large scenes (10,000+ words)?

### Integration
- ❓ Do local models (Ollama) work correctly?
- ❓ Do cloud models (Claude, GPT) work with API keys?
- ❓ Does tournament mode compare models properly?
- ❓ Does character analysis work?

---

## 📖 Key Files to Understand

**Backend Storage** (Critical):
- `factory/core/manuscript/structure.py` - Data models (Manuscript, Scene, etc.)
- `factory/core/manuscript/storage.py` - File-based storage implementation

**Backend API** (Critical):
- `webapp/backend/simple_app.py` - All API endpoints

**Frontend File Management** (Critical):
- `webapp/frontend-v2/src/features/explorer/FileTree.jsx` - File tree + CRUD operations

**Frontend Editor** (Critical):
- `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` - TipTap editor

**Frontend Layout**:
- `webapp/frontend-v2/src/App.jsx` - Main application
- `webapp/frontend-v2/src/components/layout/PanelLayout.jsx` - Three-panel layout

---

## 🎓 User's Background

**G.C. Harris**:
- Novelist writing *The Explants* trilogy
- Volume 1: Complete (499 scenes, ~120,000 words)
- Volume 2: In progress (~30% complete, using Writers Factory)
- Teaching "AI and the One-Week Novel" course (January 2025)

**Technical Level**:
- Comfortable with Git, terminal, Python, Node.js
- Uses Cursor AI, VS Code, Typora
- Understands code structure but not a professional developer
- Prefers clear explanations with examples

**Writing Workflow**:
- Organizes by Acts → Chapters → Scenes
- Writes in "Enhanced Mickey" voice (compressed, direct)
- Uses AI for scene generation and enhancement
- Values portability (wants to edit in multiple editors)
- Uses NotebookLM for research and context

---

## 💡 Important Principles

1. **User owns their creative work** - The Explants novel is 100% user's copyright, Apache 2.0 only covers software

2. **File-based storage is critical** - Scenes MUST be individual `.md` files, NOT embedded in JSON

3. **No data loss tolerated** - User is writing a novel, losing content is catastrophic

4. **External editing must work** - User should be able to edit `.md` files in VS Code, Typora, etc.

5. **Professional UX expected** - Should feel like Scrivener + VS Code, not a prototype

6. **Multi-model AI** - Support both local (Ollama) and cloud (Claude, GPT, Gemini)

7. **Phased rollout** - Personal testing → Student testing → Course distribution

---

## 🚨 Critical Don'ts

**DO NOT**:
- ❌ Suggest embedding scene content in JSON (must be in `.md` files)
- ❌ Break file-based storage (this is core architecture)
- ❌ Cause data loss (prioritize data safety above all)
- ❌ Assume user wants quick hacks (prefer proper fixes)
- ❌ Forget to check logs (`.tmp/*.log` has critical debugging info)

**DO**:
- ✅ Prioritize data integrity
- ✅ Explain architecture clearly
- ✅ Provide code examples with line numbers
- ✅ Consider edge cases
- ✅ Suggest proper fixes, not workarounds
- ✅ Document bugs systematically

---

## 📝 Your First Response

When user starts, say something like:

> "I've reviewed the Writers Factory codebase. This is an impressive AI-augmented writing environment with a clean three-panel layout and file-based storage architecture.
>
> **Key components I understand**:
> - Sprint 10 three-panel layout (FileTree | SceneEditor | AIToolsPanel)
> - File-based storage (scenes as `.md` files, not JSON)
> - TipTap editor for writing
> - Multi-model AI integration (Ollama + cloud models)
>
> **I'm ready to help you**:
> 1. Test the system
> 2. Debug any issues
> 3. Fix bugs as we find them
> 4. Improve the user experience
>
> **To start, I recommend**:
> - Run `./setup.sh` if you haven't already
> - Run `./start.sh` to launch
> - Create a test project or import your Explants scenes
> - Start writing and let me know what breaks!
>
> What would you like to focus on first?"

---

## 🎯 Success Metrics (For You)

By the end of user's testing phase, you should have helped achieve:

**Week 1**:
- [ ] User successfully launches Writers Factory
- [ ] User creates/edits scenes without data loss
- [ ] All critical bugs documented
- [ ] 5+ scenes written in Writers Factory

**Week 2**:
- [ ] Critical bugs fixed
- [ ] External editing workflow tested
- [ ] AI features tested (local + cloud)
- [ ] User comfortable using for real work

**Week 3** (if student testing happens):
- [ ] Student onboarding materials ready
- [ ] Student bugs documented
- [ ] Priority bugs fixed
- [ ] Decision made: web app vs desktop app

---

## 📚 Resources

**Documentation**:
- [QUICK_START.md](QUICK_START.md) - Setup guide
- [TESTING_PLAN.md](TESTING_PLAN.md) - Testing strategy
- [LICENSING_SUMMARY.md](LICENSING_SUMMARY.md) - Legal framework
- Sprint reviews in root directory

**Logs**:
- `.tmp/backend.log` - Backend errors
- `.tmp/frontend.log` - Frontend errors

**Code**:
- Backend: `webapp/backend/simple_app.py`
- Storage: `factory/core/manuscript/storage.py`
- Frontend: `webapp/frontend-v2/src/`

---

## ✅ Ready to Begin!

You're helping G.C. Harris test and debug Writers Factory so they can:
1. Use it for real work (The Explants Volume 2)
2. Test with students
3. Eventually distribute to course students

**Your focus**: Testing support, bug fixing, code understanding, clear explanations.

**Start by**: Reading sprint reviews, understanding architecture, being ready to debug.

**Good luck!** 🚀

---

*This handoff was created by Claude Code on November 14, 2025 after completing Sprint 10 and setting up easy-launch system.*
