# Sprint 10: Three-Panel Layout (Cursor AI / VS Code Clone)

**Priority**: 🔴 HIGH - Completes "Scrivener × VS Code" vision
**Assigned to**: Cloud Agent (deepseek-chat)
**Estimated Duration**: 6-8 hours
**Dependencies**: Sprint 9 complete ✅
**Budget**: ~$15-20 remaining

---

## Problem Statement

**Current UI**:
- No file tree (can't see project structure)
- Editor takes full screen (no dedicated AI panel)
- Tools scattered (AI, Character Panel, Cost in different modals)
- Not like Cursor AI / VS Code (no panels)

**User's Vision**: "Three-panel layout like Cursor AI"
```
┌──────────────┬────────────────────────────┬──────────────┐
│  FILE TREE   │      EDITOR (TipTap)       │  AI TOOLS    │
│  (Left)      │      (Center/Main)         │  (Right)     │
│              │                            │              │
│  📁 ACT_1    │  # Scene Title             │  🤖 Claude   │
│    📁 CH_1   │                            │              │
│    📄 1.1.1  │  [Scene content...]        │  Generate    │
│    📄 1.1.2  │                            │  Enhance     │
│  📁 ACT_2    │                            │  Analyze     │
│              │  Words: 1,250              │  Cost: $0.45 │
└──────────────┴────────────────────────────┴──────────────┘
```

**Like**: Cursor AI, VS Code with AI panel, Scrivener binder

---

## Solution: Three-Panel Responsive Layout

### Panel Structure

**Layout**: `20% Files | 60% Editor | 20% AI Tools`

**Features**:
- ✅ Resizable panels (drag borders)
- ✅ Collapsible panels (hide/show)
- ✅ Remember layout (localStorage)
- ✅ Responsive (collapse on small screens)

---

## Sprint 10 Tasks

### Task 10-01: Create Panel Layout System

**New Component**: `webapp/frontend-v2/src/components/layout/PanelLayout.jsx`

```jsx
import { useState, useEffect } from 'react';
import { ResizableBox } from 'react-resizable';
import 'react-resizable/css/styles.css';

export function PanelLayout({ left, center, right }) {
  const [leftWidth, setLeftWidth] = useState(
    parseInt(localStorage.getItem('leftPanelWidth') || '320')
  );
  const [rightWidth, setRightWidth] = useState(
    parseInt(localStorage.getItem('rightPanelWidth') || '320')
  );
  const [leftVisible, setLeftVisible] = useState(
    localStorage.getItem('leftPanelVisible') !== 'false'
  );
  const [rightVisible, setRightVisible] = useState(
    localStorage.getItem('rightPanelVisible') !== 'false'
  );

  // Save layout preferences
  useEffect(() => {
    localStorage.setItem('leftPanelWidth', leftWidth);
    localStorage.setItem('rightPanelWidth', rightWidth);
    localStorage.setItem('leftPanelVisible', leftVisible);
    localStorage.setItem('rightPanelVisible', rightVisible);
  }, [leftWidth, rightWidth, leftVisible, rightVisible]);

  return (
    <div className="flex h-screen overflow-hidden bg-gray-900 text-gray-100">
      {/* Left Panel: File Tree */}
      {leftVisible && (
        <ResizableBox
          width={leftWidth}
          height={Infinity}
          minConstraints={[200, Infinity]}
          maxConstraints={[600, Infinity]}
          axis="x"
          resizeHandles={['e']}
          onResizeStop={(e, data) => setLeftWidth(data.size.width)}
          className="border-r border-gray-700"
        >
          <div className="h-full overflow-y-auto">
            {left}
          </div>
        </ResizableBox>
      )}

      {/* Center Panel: Editor */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex-1 overflow-y-auto">
          {center}
        </div>
      </div>

      {/* Right Panel: AI Tools */}
      {rightVisible && (
        <ResizableBox
          width={rightWidth}
          height={Infinity}
          minConstraints={[250, Infinity]}
          maxConstraints={[600, Infinity]}
          axis="x"
          resizeHandles={['w']}
          onResizeStop={(e, data) => setRightWidth(data.size.width)}
          className="border-l border-gray-700"
        >
          <div className="h-full overflow-y-auto">
            {right}
          </div>
        </ResizableBox>
      )}

      {/* Toggle Buttons (Floating) */}
      <div className="fixed bottom-4 left-4 flex gap-2">
        <button
          onClick={() => setLeftVisible(!leftVisible)}
          className="p-2 bg-gray-800 rounded hover:bg-gray-700 border border-gray-600"
          title={leftVisible ? "Hide file tree" : "Show file tree"}
        >
          {leftVisible ? '←' : '→'} Files
        </button>
      </div>
      <div className="fixed bottom-4 right-4 flex gap-2">
        <button
          onClick={() => setRightVisible(!rightVisible)}
          className="p-2 bg-gray-800 rounded hover:bg-gray-700 border border-gray-600"
          title={rightVisible ? "Hide AI panel" : "Show AI panel"}
        >
          AI {rightVisible ? '→' : '←'}
        </button>
      </div>
    </div>
  );
}
```

**Dependencies to add**:
```json
{
  "react-resizable": "^3.0.5"
}
```

**Success Criteria**:
- ✅ Three panels render correctly
- ✅ Panels resizable by dragging borders
- ✅ Toggle buttons hide/show panels
- ✅ Layout persists across sessions

---

### Task 10-02: Create File Tree Component

**New Component**: `webapp/frontend-v2/src/features/explorer/FileTree.jsx`

```jsx
import { useState, useEffect } from 'react';
import { ChevronRight, ChevronDown, File, Folder, FolderOpen } from 'lucide-react';

export function FileTree({ projectPath, onFileSelect, currentFile }) {
  const [tree, setTree] = useState(null);
  const [expanded, setExpanded] = useState(new Set(['root', 'scenes']));

  // Load file tree from backend
  useEffect(() => {
    fetch(`/api/list_files?project_path=${encodeURIComponent(projectPath)}`)
      .then(res => res.json())
      .then(data => setTree(data))
      .catch(err => console.error('Failed to load file tree:', err));
  }, [projectPath]);

  const toggleExpand = (path) => {
    const newExpanded = new Set(expanded);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    setExpanded(newExpanded);
  };

  const renderNode = (node, depth = 0) => {
    const isExpanded = expanded.has(node.path);
    const isSelected = currentFile === node.path;
    const isFolder = node.type === 'directory';

    return (
      <div key={node.path}>
        <div
          className={`
            flex items-center gap-2 px-2 py-1 cursor-pointer
            hover:bg-gray-800 rounded
            ${isSelected ? 'bg-blue-900' : ''}
          `}
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
          onClick={() => isFolder ? toggleExpand(node.path) : onFileSelect(node.path)}
        >
          {/* Expand/Collapse Icon */}
          {isFolder && (
            <span className="text-gray-400">
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </span>
          )}

          {/* File/Folder Icon */}
          {isFolder ? (
            isExpanded ? <FolderOpen size={16} className="text-blue-400" /> : <Folder size={16} className="text-blue-400" />
          ) : (
            <File size={16} className="text-gray-400" />
          )}

          {/* Name */}
          <span className="text-sm truncate">
            {node.name}
          </span>
        </div>

        {/* Children */}
        {isFolder && isExpanded && node.children && (
          <div>
            {node.children.map(child => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  if (!tree) {
    return <div className="p-4 text-gray-400">Loading project...</div>;
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="font-semibold">Project Files</h2>
        <p className="text-xs text-gray-400 truncate">{projectPath}</p>
      </div>

      {/* Tree */}
      <div className="flex-1 overflow-y-auto p-2">
        {renderNode(tree)}
      </div>

      {/* Footer */}
      <div className="p-2 border-t border-gray-700 text-xs text-gray-400">
        {tree.file_count || 0} scenes
      </div>
    </div>
  );
}
```

**Backend API Endpoint** (add to `simple_app.py`):
```python
@app.get("/api/list_files")
async def list_files(project_path: str):
    """List all files in project directory as tree structure."""
    try:
        project_dir = Path(project_path)

        def build_tree(path: Path) -> dict:
            if path.is_file():
                return {
                    "name": path.name,
                    "path": str(path.relative_to(project_dir)),
                    "type": "file",
                    "size": path.stat().st_size,
                }
            else:
                children = sorted(
                    [build_tree(p) for p in path.iterdir()],
                    key=lambda x: (x["type"] != "directory", x["name"])
                )
                return {
                    "name": path.name,
                    "path": str(path.relative_to(project_dir)) if path != project_dir else "root",
                    "type": "directory",
                    "children": children,
                    "file_count": sum(1 for c in children if c["type"] == "file"),
                }

        tree = build_tree(project_dir)
        return tree
    except Exception as e:
        raise HTTPException(500, str(e))
```

**Success Criteria**:
- ✅ File tree loads project structure
- ✅ Folders expand/collapse
- ✅ Clicking file loads in editor
- ✅ Current file highlighted
- ✅ Keyboard navigation (arrow keys)

---

### Task 10-03: Create AI Tools Panel

**New Component**: `webapp/frontend-v2/src/features/ai/AIToolsPanel.jsx`

```jsx
import { useState } from 'react';
import { Sparkles, Wand2, BarChart3, Trophy, DollarSign } from 'lucide-react';

export function AIToolsPanel({ currentScene, onGenerate, onEnhance, onAnalyze }) {
  const [selectedModel, setSelectedModel] = useState('claude-sonnet-4.5');
  const [economyMode, setEconomyMode] = useState(true);
  const [cost, setCost] = useState(0);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="font-semibold flex items-center gap-2">
          <Sparkles size={20} className="text-blue-400" />
          AI Assistant
        </h2>
      </div>

      {/* Model Selection */}
      <div className="p-4 border-b border-gray-700">
        <label className="text-sm text-gray-400">Model</label>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="w-full mt-1 px-2 py-1 bg-gray-800 border border-gray-600 rounded text-sm"
        >
          <option value="claude-sonnet-4.5">Claude Sonnet 4.5</option>
          <option value="gpt-4">GPT-4</option>
          <option value="gemini-pro">Gemini Pro</option>
          <option value="ollama-llama3">Llama 3 (Local)</option>
        </select>

        {/* Economy Mode */}
        <label className="flex items-center gap-2 mt-2 cursor-pointer">
          <input
            type="checkbox"
            checked={economyMode}
            onChange={(e) => setEconomyMode(e.target.checked)}
            className="rounded"
          />
          <span className="text-sm">Economy Mode</span>
        </label>
      </div>

      {/* AI Actions */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        <button
          onClick={() => onGenerate(selectedModel)}
          disabled={!currentScene}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded flex items-center gap-2 disabled:opacity-50"
        >
          <Wand2 size={16} />
          Generate Scene
        </button>

        <button
          onClick={() => onEnhance(selectedModel)}
          disabled={!currentScene}
          className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 rounded flex items-center gap-2 disabled:opacity-50"
        >
          <Sparkles size={16} />
          Enhance Prose
        </button>

        <button
          onClick={() => onAnalyze()}
          disabled={!currentScene}
          className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded flex items-center gap-2 disabled:opacity-50"
        >
          <BarChart3 size={16} />
          Character Analysis
        </button>

        <button
          onClick={() => {/* Open tournament mode */}}
          className="w-full px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded flex items-center gap-2"
        >
          <Trophy size={16} />
          Tournament Mode
        </button>

        <div className="pt-4 border-t border-gray-700">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Session Cost</span>
            <span className="font-mono">${cost.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Footer: Cost Info */}
      <div className="p-4 border-t border-gray-700 bg-gray-800/50">
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <DollarSign size={14} />
          <span>Budget: $65 | Spent: ${cost.toFixed(2)} | Remaining: ${(65 - cost).toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
```

**Success Criteria**:
- ✅ AI tools panel renders
- ✅ Model selection works
- ✅ Economy mode toggle works
- ✅ Action buttons call appropriate functions
- ✅ Cost tracking displays

---

### Task 10-04: Integrate Panels into Main App

**Modify**: `webapp/frontend-v2/src/App.jsx`

```jsx
import { useState } from 'react';
import { PanelLayout } from './components/layout/PanelLayout';
import { FileTree } from './features/explorer/FileTree';
import { SceneEditor } from './features/editor/SceneEditor';
import { AIToolsPanel } from './features/ai/AIToolsPanel';

function App() {
  const [projectPath, setProjectPath] = useState('/Users/user/my-novel');
  const [currentFile, setCurrentFile] = useState(null);
  const [currentScene, setCurrentScene] = useState(null);

  const handleFileSelect = async (filePath) => {
    setCurrentFile(filePath);
    // Load scene content
    const res = await fetch(`/api/load_scene?file_path=${encodeURIComponent(filePath)}`);
    const scene = await res.json();
    setCurrentScene(scene);
  };

  const handleGenerate = (model) => {
    // Call generate API
    console.log('Generating with', model);
  };

  const handleEnhance = (model) => {
    // Call enhance API
    console.log('Enhancing with', model);
  };

  const handleAnalyze = () => {
    // Open character panel
    console.log('Analyzing character');
  };

  return (
    <PanelLayout
      left={
        <FileTree
          projectPath={projectPath}
          onFileSelect={handleFileSelect}
          currentFile={currentFile}
        />
      }
      center={
        <SceneEditor
          scene={currentScene}
          onSave={(content) => {
            // Save scene
            console.log('Saving', content);
          }}
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

export default App;
```

**Success Criteria**:
- ✅ Three panels render correctly
- ✅ File tree loads project
- ✅ Clicking file loads in editor
- ✅ AI tools interact with editor
- ✅ Layout persists across sessions

---

### Task 10-05: Keyboard Shortcuts

**Add global keyboard shortcuts** for panel management:

```jsx
useEffect(() => {
  const handleKeyDown = (e) => {
    // Cmd/Ctrl + B: Toggle left panel (file tree)
    if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
      e.preventDefault();
      setLeftVisible(!leftVisible);
    }

    // Cmd/Ctrl + J: Toggle right panel (AI tools)
    if ((e.metaKey || e.ctrlKey) && e.key === 'j') {
      e.preventDefault();
      setRightVisible(!rightVisible);
    }

    // Cmd/Ctrl + \: Toggle both side panels
    if ((e.metaKey || e.ctrlKey) && e.key === '\\') {
      e.preventDefault();
      const newVisible = !(leftVisible && rightVisible);
      setLeftVisible(newVisible);
      setRightVisible(newVisible);
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, [leftVisible, rightVisible]);
```

**Shortcuts**:
- `Cmd+B` / `Ctrl+B`: Toggle file tree
- `Cmd+J` / `Ctrl+J`: Toggle AI panel
- `Cmd+\` / `Ctrl+\`: Toggle both panels (distraction-free)

---

## Definition of Done

### Layout
- [ ] Three panels render (left, center, right)
- [ ] Panels resizable by dragging
- [ ] Panels collapsible (hide/show)
- [ ] Layout persists in localStorage
- [ ] Responsive (collapse on small screens)

### File Tree
- [ ] Loads project file structure
- [ ] Folders expand/collapse
- [ ] Clicking file loads in editor
- [ ] Current file highlighted
- [ ] Shows file counts

### AI Tools Panel
- [ ] Model selection dropdown
- [ ] Economy mode toggle
- [ ] Generate/Enhance/Analyze buttons
- [ ] Cost tracking display
- [ ] Tournament mode button

### Integration
- [ ] File tree → Editor (click loads scene)
- [ ] Editor → AI tools (current scene passed)
- [ ] Keyboard shortcuts work
- [ ] No layout bugs (overflow, z-index)

### Testing
- [ ] Manual test: Resize panels
- [ ] Manual test: Hide/show panels
- [ ] Manual test: Click file, loads in editor
- [ ] Manual test: Keyboard shortcuts
- [ ] Manual test: Refresh, layout persists

---

## Deliverables

### New Files
1. `webapp/frontend-v2/src/components/layout/PanelLayout.jsx` (~150 lines)
2. `webapp/frontend-v2/src/features/explorer/FileTree.jsx` (~200 lines)
3. `webapp/frontend-v2/src/features/ai/AIToolsPanel.jsx` (~150 lines)

### Modified Files
1. `webapp/frontend-v2/src/App.jsx` (integrate panels)
2. `webapp/frontend-v2/package.json` (add react-resizable)
3. `webapp/backend/simple_app.py` (add /api/list_files endpoint)

### Dependencies
```bash
npm install react-resizable
```

---

## Success Metrics

**Before Sprint 10**:
- ❌ No file tree (can't see project structure)
- ❌ No AI panel (tools scattered)
- ❌ Full-screen editor (no workspace feel)

**After Sprint 10**:
- ✅ Three-panel layout (like Cursor AI)
- ✅ File tree (see all scenes)
- ✅ Dedicated AI panel (tools always accessible)
- ✅ Resizable/collapsible (customize workspace)
- ✅ "Scrivener × VS Code × AI" vision complete

---

**Priority**: 🔴 HIGH
**Impact**: Completes professional writing environment
**Budget**: ~$15-20 (of $65 remaining)
**Timeline**: 1-2 days
