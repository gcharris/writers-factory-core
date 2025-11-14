# Prompt for Cloud Agent: Sprint 10 - Three-Panel Layout

**Date**: November 14, 2025
**Priority**: 🔴 CRITICAL
**Budget**: $15-20 remaining, 2-3 days
**Repo**: https://github.com/gcharris/writers-factory-core

---

## Context

You've successfully completed Sprint 9 (File-Based Editing) ✅

**Result**: Scenes now stored as individual `.md` files, editable in any text editor.

**User's Vision**: "Scrivener meets VS Code"

Now we need to complete the vision with a **three-panel layout**:
- **Left Panel**: File tree (like Scrivener binder / VS Code explorer)
- **Center Panel**: Scene editor (TipTap)
- **Right Panel**: AI tools (model selection, generate, enhance)

This is the FINAL core feature before Writers Factory is ready for the user's novel workflow.

---

## Your Task

**Implement Sprint 10: Three-Panel Layout**

**Read the complete specification**:
👉 **[SPRINT_10_THREE_PANEL_LAYOUT.md](SPRINT_10_THREE_PANEL_LAYOUT.md)**

### Summary of Changes

**Create three new components**:
1. **PanelLayout.jsx** - Resizable three-panel container
2. **FileTree.jsx** - File explorer with expand/collapse
3. **AIToolsPanel.jsx** - AI tools sidebar

**Update existing**:
4. **App.jsx** - Integrate three-panel layout
5. **simple_app.py** - Add `/api/list_files` endpoint

---

## Implementation Overview

### Component 1: PanelLayout.jsx

**Location**: `webapp/frontend-v2/src/components/layout/PanelLayout.jsx`

**Purpose**: Resizable three-panel container

**Key Features**:
- Left and right panels are resizable (320px default, 200-600px range)
- Toggle visibility for left/right panels
- Keyboard shortcuts:
  - `Cmd+B` (Mac) / `Ctrl+B` (Windows): Toggle left panel
  - `Cmd+J` (Mac) / `Ctrl+J` (Windows): Toggle right panel
  - `Cmd+\` (Mac) / `Ctrl+\` (Windows): Toggle both panels
- Save panel state to localStorage

**Dependencies**:
```bash
npm install react-resizable
```

**Code Structure**:
```jsx
import { Resizable } from 'react-resizable';
import { useState, useEffect } from 'react';

export function PanelLayout({ left, center, right }) {
  const [leftWidth, setLeftWidth] = useState(() => {
    return parseInt(localStorage.getItem('leftPanelWidth')) || 320;
  });
  const [rightWidth, setRightWidth] = useState(() => {
    return parseInt(localStorage.getItem('rightPanelWidth')) || 320;
  });
  const [leftVisible, setLeftVisible] = useState(true);
  const [rightVisible, setRightVisible] = useState(true);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
        e.preventDefault();
        setLeftVisible(v => !v);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'j') {
        e.preventDefault();
        setRightVisible(v => !v);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === '\\') {
        e.preventDefault();
        setLeftVisible(v => !v);
        setRightVisible(v => !v);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left Panel */}
      {leftVisible && (
        <Resizable
          width={leftWidth}
          height={Infinity}
          onResize={(e, { size }) => {
            setLeftWidth(size.width);
            localStorage.setItem('leftPanelWidth', size.width);
          }}
          minConstraints={[200, Infinity]}
          maxConstraints={[600, Infinity]}
          axis="x"
        >
          <div
            className="border-r border-gray-300 overflow-hidden"
            style={{ width: leftWidth }}
          >
            {left}
          </div>
        </Resizable>
      )}

      {/* Center Panel */}
      <div className="flex-1 overflow-hidden">
        {center}
      </div>

      {/* Right Panel */}
      {rightVisible && (
        <Resizable
          width={rightWidth}
          height={Infinity}
          onResize={(e, { size }) => {
            setRightWidth(size.width);
            localStorage.setItem('rightPanelWidth', size.width);
          }}
          minConstraints={[200, Infinity]}
          maxConstraints={[600, Infinity]}
          axis="x"
        >
          <div
            className="border-l border-gray-300 overflow-hidden"
            style={{ width: rightWidth }}
          >
            {right}
          </div>
        </Resizable>
      )}
    </div>
  );
}
```

---

### Component 2: FileTree.jsx

**Location**: `webapp/frontend-v2/src/features/explorer/FileTree.jsx`

**Purpose**: File explorer showing project structure

**Key Features**:
- Display project folder structure (manuscript/, reference/, planning/)
- Expand/collapse folders
- Click file to open in editor
- Highlight currently open file
- Icons for folders/files (📁 folder, 📄 file)

**API Endpoint**: `/api/list_files?project_id=<id>`

**Code Structure**:
```jsx
import { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, File, Folder } from 'lucide-react';

export function FileTree({ projectId, onFileSelect, currentFile }) {
  const [tree, setTree] = useState(null);
  const [expanded, setExpanded] = useState(new Set(['root', 'manuscript']));

  useEffect(() => {
    // Fetch file tree from backend
    fetch(`/api/list_files?project_id=${projectId}`)
      .then(res => res.json())
      .then(data => setTree(data.tree))
      .catch(err => console.error('Failed to load file tree:', err));
  }, [projectId]);

  const toggleExpand = (path) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };

  const renderNode = (node, depth = 0) => {
    const isFolder = node.type === 'folder';
    const isExpanded = expanded.has(node.path);
    const isCurrent = currentFile === node.path;

    return (
      <div key={node.path}>
        <div
          className={`flex items-center px-2 py-1 cursor-pointer hover:bg-gray-100 ${
            isCurrent ? 'bg-blue-100' : ''
          }`}
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
          onClick={() => {
            if (isFolder) {
              toggleExpand(node.path);
            } else {
              onFileSelect(node.path);
            }
          }}
        >
          {isFolder && (
            <span className="mr-1">
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </span>
          )}
          {isFolder ? <Folder size={16} className="mr-2" /> : <File size={16} className="mr-2" />}
          <span className="text-sm">{node.name}</span>
        </div>
        {isFolder && isExpanded && node.children && (
          <div>
            {node.children.map(child => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  if (!tree) {
    return <div className="p-4 text-gray-500">Loading files...</div>;
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-2 border-b border-gray-300 font-semibold text-sm">
        FILES
      </div>
      {renderNode(tree)}
    </div>
  );
}
```

---

### Component 3: AIToolsPanel.jsx

**Location**: `webapp/frontend-v2/src/features/ai-tools/AIToolsPanel.jsx`

**Purpose**: AI tools sidebar

**Key Features**:
- Model selection dropdown (Claude, GPT-4, Ollama)
- Economy mode toggle
- Generate/Enhance/Analyze buttons
- Cost tracking display
- Connect to existing AI agents

**Code Structure**:
```jsx
import { useState } from 'react';
import { Sparkles, Wand2, BarChart3 } from 'lucide-react';

export function AIToolsPanel({ currentScene, onGenerate, onEnhance, onAnalyze }) {
  const [selectedModel, setSelectedModel] = useState('claude-sonnet-4.5');
  const [economyMode, setEconomyMode] = useState(false);
  const [totalCost, setTotalCost] = useState(0);

  const models = [
    { id: 'claude-sonnet-4.5', name: 'Claude Sonnet 4.5', cost: 0.003 },
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', cost: 0.01 },
    { id: 'ollama-llama3', name: 'Ollama Llama3', cost: 0 },
  ];

  const handleGenerate = async () => {
    const result = await onGenerate(selectedModel, economyMode);
    if (result.cost) {
      setTotalCost(prev => prev + result.cost);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-300">
        <h2 className="font-semibold text-sm mb-3">AI TOOLS</h2>

        {/* Model Selection */}
        <div className="mb-3">
          <label className="block text-xs text-gray-600 mb-1">Model</label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
          >
            {models.map(model => (
              <option key={model.id} value={model.id}>
                {model.name} {model.cost > 0 ? `($${model.cost}/1K)` : '(Free)'}
              </option>
            ))}
          </select>
        </div>

        {/* Economy Mode */}
        <div className="flex items-center mb-3">
          <input
            type="checkbox"
            id="economy-mode"
            checked={economyMode}
            onChange={(e) => setEconomyMode(e.target.checked)}
            className="mr-2"
          />
          <label htmlFor="economy-mode" className="text-xs text-gray-700">
            Economy Mode
          </label>
        </div>
      </div>

      {/* Actions */}
      <div className="p-4 space-y-2">
        <button
          onClick={handleGenerate}
          className="w-full flex items-center justify-center px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
        >
          <Sparkles size={16} className="mr-2" />
          Generate Scene
        </button>

        <button
          onClick={() => onEnhance(selectedModel, economyMode)}
          className="w-full flex items-center justify-center px-3 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 text-sm"
        >
          <Wand2 size={16} className="mr-2" />
          Enhance Prose
        </button>

        <button
          onClick={() => onAnalyze(selectedModel)}
          className="w-full flex items-center justify-center px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
        >
          <BarChart3 size={16} className="mr-2" />
          Analyze Voice
        </button>
      </div>

      {/* Cost Tracking */}
      <div className="mt-auto p-4 border-t border-gray-300">
        <div className="text-xs text-gray-600">Session Cost</div>
        <div className="text-lg font-semibold">${totalCost.toFixed(4)}</div>
      </div>
    </div>
  );
}
```

---

### Backend: Add `/api/list_files` Endpoint

**File**: `webapp/backend/simple_app.py`

**Add this endpoint**:
```python
@app.get("/api/list_files")
async def list_files(project_id: str):
    """List all files in project as a tree structure."""
    try:
        project_dir = Path(f"projects/{project_id}")

        if not project_dir.exists():
            raise HTTPException(404, "Project not found")

        def build_tree(path: Path, name: str = None) -> dict:
            """Recursively build file tree."""
            if path.is_file():
                return {
                    "name": path.name,
                    "path": str(path.relative_to(project_dir)),
                    "type": "file",
                    "size": path.stat().st_size,
                }
            else:
                children = []
                for child in sorted(path.iterdir()):
                    # Skip hidden files and __pycache__
                    if child.name.startswith('.') or child.name == '__pycache__':
                        continue
                    children.append(build_tree(child))

                return {
                    "name": name or path.name,
                    "path": str(path.relative_to(project_dir)) if path != project_dir else "root",
                    "type": "folder",
                    "children": children,
                }

        tree = build_tree(project_dir, name=project_id)

        return {"tree": tree}

    except Exception as e:
        raise HTTPException(500, str(e))
```

---

### Integration: Update App.jsx

**File**: `webapp/frontend-v2/src/App.jsx`

**Changes**:
1. Import new components
2. Replace current layout with PanelLayout
3. Pass FileTree, SceneEditor, AIToolsPanel as children

**Example**:
```jsx
import { PanelLayout } from './components/layout/PanelLayout';
import { FileTree } from './features/explorer/FileTree';
import { SceneEditor } from './features/editor/SceneEditor';
import { AIToolsPanel } from './features/ai-tools/AIToolsPanel';

function App() {
  const [currentFile, setCurrentFile] = useState(null);
  const [currentScene, setCurrentScene] = useState(null);

  const handleFileSelect = async (filePath) => {
    setCurrentFile(filePath);
    // Load scene content from file
    const response = await fetch(`/api/load_scene?path=${filePath}`);
    const data = await response.json();
    setCurrentScene(data.scene);
  };

  return (
    <PanelLayout
      left={
        <FileTree
          projectId={currentProjectId}
          onFileSelect={handleFileSelect}
          currentFile={currentFile}
        />
      }
      center={
        <SceneEditor
          scene={currentScene}
          onSave={(content) => saveScene(currentFile, content)}
        />
      }
      right={
        <AIToolsPanel
          currentScene={currentScene}
          onGenerate={handleGenerate}
          onEnhance={handleEnhance}
          onAnalyze={handleAnalyze}
        />
      }
    />
  );
}
```

---

## Testing Checklist

Before marking complete, verify:

### Frontend Layout
- [ ] Three panels render correctly
- [ ] Left and right panels are resizable
- [ ] Toggle buttons hide/show panels
- [ ] Keyboard shortcuts work (Cmd+B, Cmd+J, Cmd+\)
- [ ] Panel widths persist after refresh

### File Tree
- [ ] Files and folders display correctly
- [ ] Expand/collapse works
- [ ] Clicking file loads in editor
- [ ] Current file is highlighted
- [ ] Folder icons show correct state

### AI Tools Panel
- [ ] Model selection dropdown works
- [ ] Generate/Enhance/Analyze buttons trigger actions
- [ ] Cost tracking updates
- [ ] Economy mode toggle works

### Backend API
- [ ] `/api/list_files` returns correct tree structure
- [ ] Tree includes all project folders (manuscript/, reference/, etc.)
- [ ] Hidden files excluded

### Integration
- [ ] Selecting file in tree loads scene in editor
- [ ] Editing scene saves to correct file
- [ ] AI tools connect to existing agents
- [ ] No console errors

---

## Success Criteria

**When complete**:

✅ **Three-panel layout** like Cursor AI / VS Code
✅ **File tree** shows project structure
✅ **Resizable panels** with keyboard shortcuts
✅ **AI tools panel** with model selection
✅ **Complete "Scrivener × VS Code × AI" vision**

**This enables**:
- User can see all project files at a glance
- User can quickly navigate between scenes
- User can resize panels to focus on writing
- User can access AI tools without leaving editor
- User has professional writing environment

---

## Estimated Effort

**Time**: 6-8 hours
**Cost**: ~$15-20 (of $20 remaining budget)
**Timeline**: Complete within 2 days

---

## Deliverables

When complete, create a commit message like:

```
Sprint 10: Three-Panel Layout (Complete "Scrivener × VS Code × AI" vision)

Implemented professional three-panel writing environment:
- File tree (left) for project navigation
- Scene editor (center) for writing
- AI tools (right) for generation/enhancement
- Resizable panels with keyboard shortcuts
- Full integration with file-based storage

Components added:
- Added: webapp/frontend-v2/src/components/layout/PanelLayout.jsx
- Added: webapp/frontend-v2/src/features/explorer/FileTree.jsx
- Added: webapp/frontend-v2/src/features/ai-tools/AIToolsPanel.jsx
- Modified: webapp/frontend-v2/src/App.jsx (integrate layout)
- Modified: webapp/backend/simple_app.py (add /api/list_files)

Dependencies: react-resizable, lucide-react

Result: Writers Factory now matches user's vision perfectly:
"Scrivener meets VS Code with AI assistant"

Files modified: 5
Lines added: ~650
Lines removed: ~50

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Priority

🔴 **CRITICAL** - This completes the core Writers Factory vision.

**After Sprint 10**:
- ✅ File-based storage (Sprint 9)
- ✅ Three-panel layout (Sprint 10)
- ✅ Professional writing environment
- ✅ Ready for user's novel workflow

**Remaining polish** (if budget allows):
- Documentation updates
- Help content improvements
- Bug fixes

---

**Go build!** 🚀

This is the final core feature. Make it beautiful, make it fast, make it feel like Cursor AI.

Budget: $15-20 remaining / 2 days
Target: Complete within 2 days, leaving writers factory ready for production use.
