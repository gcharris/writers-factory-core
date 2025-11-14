# Sprint 10: Ready for Cloud Agent Implementation

**Date**: November 14, 2025
**Status**: ✅ Specification Complete - Ready to Hand Off
**Branch**: `claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs`

---

## What's Ready

### 📋 Complete Specifications Created:

1. **[SPRINT_10_THREE_PANEL_LAYOUT.md](SPRINT_10_THREE_PANEL_LAYOUT.md)** (506 lines)
   - Technical specification for three-panel layout
   - Component architecture and implementation details
   - Testing checklist and success criteria

2. **[PROMPT_FOR_CLOUD_AGENT_SPRINT_10.md](PROMPT_FOR_CLOUD_AGENT_SPRINT_10.md)** (handoff instructions)
   - Complete implementation guide for Cloud Agent
   - Code examples for all components
   - Backend API endpoint specification

### ✅ Prerequisites Complete:

- ✅ Sprint 9: File-based storage (commit c717258)
- ✅ Sprint 7R: TipTap editor (React 19 compatible)
- ✅ Sprint 8: Student polish (welcome modal, help panel)
- ✅ All dependencies installed
- ✅ Build working correctly

---

## What Cloud Agent Will Build

### 🎯 Goal: Three-Panel Layout ("Scrivener × VS Code × AI")

**Layout**:
```
┌──────────────┬─────────────────────┬──────────────┐
│              │                     │              │
│  File Tree   │   Scene Editor      │  AI Tools    │
│  (Left)      │   (Center)          │  (Right)     │
│              │                     │              │
│  📁 ACT_1    │   [TipTap Editor]   │  🤖 Model    │
│    📁 CH_1   │                     │  ⚙️ Options  │
│      📄 1.1  │   [Writing here]    │  ✨ Generate │
│      📄 1.2  │                     │  🪄 Enhance  │
│  📁 ACT_2    │                     │  📊 Analyze  │
│              │                     │  💰 $0.12    │
└──────────────┴─────────────────────┴──────────────┘
     320px           flexible            320px
  (resizable)                         (resizable)
```

### 📦 Components to Create:

**1. PanelLayout.jsx** (~150 lines)
- Location: `webapp/frontend-v2/src/components/layout/PanelLayout.jsx`
- Resizable three-panel container
- Keyboard shortcuts (Cmd+B, Cmd+J, Cmd+\)
- Persistent panel widths (localStorage)

**2. FileTree.jsx** (~200 lines)
- Location: `webapp/frontend-v2/src/features/explorer/FileTree.jsx`
- Recursive file tree display
- Expand/collapse folders
- Click to open files
- Highlight current file
- Icons: 📁 folders, 📄 markdown files

**3. AIToolsPanel.jsx** (~150 lines)
- Location: `webapp/frontend-v2/src/features/ai-tools/AIToolsPanel.jsx`
- Model selection dropdown (Claude, GPT-4, Ollama)
- Economy mode toggle
- Generate/Enhance/Analyze buttons
- Cost tracking display

**4. Backend API** (~50 lines)
- File: `webapp/backend/simple_app.py`
- New endpoint: `/api/list_files?project_id=<id>`
- Returns recursive file tree structure
- Excludes hidden files and `__pycache__`

**5. Integration** (~100 lines)
- File: `webapp/frontend-v2/src/App.jsx`
- Replace current layout with PanelLayout
- Wire up FileTree, SceneEditor, AIToolsPanel
- Connect file selection to editor loading

### 📚 Dependencies to Install:

```bash
npm install react-resizable lucide-react
```

---

## Instructions for Cloud Agent

### 🚀 To Start Implementation:

1. **Read the specification**:
   ```
   /Users/gch2024/writers-factory-core/PROMPT_FOR_CLOUD_AGENT_SPRINT_10.md
   ```

2. **Install dependencies**:
   ```bash
   cd /Users/gch2024/writers-factory-core/webapp/frontend-v2
   npm install react-resizable lucide-react
   ```

3. **Create components** in this order:
   - PanelLayout.jsx (foundation)
   - FileTree.jsx (left panel)
   - AIToolsPanel.jsx (right panel)
   - Backend `/api/list_files` endpoint
   - Integration in App.jsx

4. **Test**:
   - Verify panels resize correctly
   - Verify keyboard shortcuts work
   - Verify file tree displays project structure
   - Verify clicking file loads in editor
   - Verify AI tools connect to existing agents

5. **Commit with format**:
   ```
   Sprint 10: Three-Panel Layout (Complete "Scrivener × VS Code × AI" vision)

   [Details of implementation]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

---

## Budget & Timeline

**Estimated Effort**: 6-8 hours
**Estimated Cost**: ~$15-20 (of $20 remaining budget)
**Timeline**: Complete within 2 days
**Deadline**: 4 days total before budget runs out

---

## Success Criteria

When Sprint 10 is complete, Writers Factory will have:

✅ **Complete "Scrivener × VS Code × AI" Vision**:
- ✅ File-based storage (Sprint 9)
- ✅ Three-panel layout (Sprint 10)
- ✅ Professional writing environment
- ✅ AI-assisted scene generation
- ✅ Ready for user's novel workflow

**User will be able to**:
- See all project files in left panel
- Click file to open in center editor
- Edit with professional TipTap editor
- Use AI tools in right panel
- Resize panels to focus on writing
- Toggle panels with keyboard shortcuts
- Edit files externally (Typora, Cursor AI, VS Code)

---

## What Comes After Sprint 10

**If budget allows** (~$10-15 remaining):
1. Documentation updates (help content, README)
2. Bug fixes and polish
3. Additional testing

**User's Next Steps**:
- Use Writers Factory for novel writing (The Explants Volume 2)
- Test complete workflow
- Provide feedback for improvements

---

## Repository Status

**Branch**: `claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs`
**Latest Commit**: `089ef6a` - Sprint 10 specification
**Previous Commit**: `c717258` - Sprint 9 implementation (file-based storage)

**To access**:
```bash
git clone https://github.com/gcharris/writers-factory-core.git
git checkout claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs
```

---

**Ready to go!** 🚀

Cloud Agent has everything needed to implement Sprint 10. The specification is complete, dependencies are documented, and the path forward is clear.

This is the final core feature before Writers Factory matches the user's vision perfectly.
