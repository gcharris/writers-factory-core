# Cloud Agent Sprint 1 + 2: Writers Factory UI

**Date**: November 14, 2025
**Assigned to**: Cloud Agent
**Managed by**: Claude Code
**Timeline**: 2-3 days
**Budget**: ~$500-700 of remaining credits

---

## 🎯 Mission

Build a **Cursor AI-style web interface** for Writers Factory that connects to the existing production backend.

**Design Philosophy**: Clean, simple, text-focused. NO fancy graphics. Professional writer's tool, not flashy webapp.

---

## 📊 Current State

### ✅ What Already Works (Phase 2 + 3)

**Backend** (`/Users/gch2024/writers-factory-core`):
- ✅ FastAPI server: `webapp/backend/simple_app.py`
- ✅ Real AI integration: `webapp/backend/agent_integration.py`
- ✅ 23 AI models configured in `config/agents.yaml`
- ✅ API keys in `config/credentials.json`
- ✅ Manuscript structure models: `factory/core/manuscript/`
- ✅ Import script: `scripts/import_explants.py`
- ✅ Knowledge router: Cognee + NotebookLM
- ✅ 156 tests passing

**Existing API Endpoints**:
```
GET  /api/health                  ✅ Working
GET  /api/models/available        ✅ Working
POST /api/compare                 ✅ Working (real AI comparison)
POST /api/scene/generate          ✅ Working (real AI generation)
POST /api/scene/enhance           ✅ Working (real AI enhancement)
POST /api/knowledge/query         ✅ Working (Cognee + NotebookLM)
GET  /api/session/status          ✅ Working
```

### ❌ What's Missing

- ❌ VS Code-style 3-pane UI
- ❌ Manuscript Explorer (Acts → Chapters → Scenes)
- ❌ Monaco editor for markdown
- ❌ Tournament Compare grid UI
- ❌ AI Tools panel
- ❌ Knowledge tab
- ❌ Setup wizard

---

## 🎨 User's Design Vision

### Three Core Features (Priority Order)

**1. Simple File Navigation + Good Editor**
- File tree on left (Acts → Chapters → Scenes)
- Click scene → opens in professional markdown editor
- Clean, text-focused (like Cursor AI)

**2. Pre-Programmed Task Templates**
- Center/right panel with simple task titles
- "Character Background Development" → interactive AI dialogue
- "Scene Enhancement" → guided workflow
- "Voice Testing" → step-by-step process

**3. Smart Agent Selection**
- Dropdown to select from 23 models
- System suggests best model for each task
- Track which models work best for which purposes
- Examples: "Qwen for dialogue", "Mistral for outlines"

### Aesthetic: **Cursor AI Style**
- ❌ NO fancy graphics, colors, animations
- ❌ NO cluttered buttons and options
- ✅ CLEAN text-focused interface
- ✅ SIMPLE file tree on left
- ✅ PROFESSIONAL editor in center
- ✅ FOCUSED tools panel on right

**Reference**: Think Cursor AI / VS Code, NOT colorful webapp dashboard

---

## 📋 Sprint 1: Foundation (Week 1)

### S1-01: React + Vite Project Scaffold

**Location**: `webapp/frontend-v2/` (NEW - don't touch old frontend)

**Tech Stack**:
```json
{
  "framework": "React 18 + Vite",
  "styling": "Tailwind CSS",
  "state": "Zustand",
  "data": "React Query (@tanstack/react-query)",
  "editor": "@monaco-editor/react",
  "layout": "react-resizable-panels",
  "toasts": "sonner",
  "icons": "lucide-react"
}
```

**Initial Setup**:
```bash
cd webapp
npm create vite@latest frontend-v2 -- --template react
cd frontend-v2
npm install
npm install -D tailwindcss postcss autoprefixer
npm install zustand @tanstack/react-query
npm install @monaco-editor/react react-resizable-panels sonner lucide-react
```

**Layout Structure**:
```
┌─────────────────────────────────────────────────────────┐
│ Top Bar: [Project] [Agent ▼] [Knowledge ▼] [Run] [Save]│
├─────────┬─────────────────────────┬─────────────────────┤
│         │                         │                     │
│ Files   │   Editor                │  AI Tools           │
│ Tree    │   (Monaco)              │                     │
│         │                         │  - Generate         │
│ Acts    │   Markdown content      │  - Enhance          │
│ ├─ Ch1  │   editing here...       │  - Continue         │
│ │  ├─S1 │                         │  - Voice Test       │
│ │  └─S2 │                         │                     │
│ └─ Ch2  │                         │  Knowledge          │
│         │                         │  - Cognee / NLM     │
│         │                         │  - Query snippets   │
│         │                         │                     │
│ 200px   │   flex-1                │  300px              │
└─────────┴─────────────────────────┴─────────────────────┘
```

**Acceptance Criteria**:
- ✅ App boots at `localhost:5173`
- ✅ 3 resizable panes render
- ✅ Top bar with dropdowns (not functional yet, just UI)
- ✅ Health check call to backend shows status in footer
- ✅ Clean, minimal styling (gray backgrounds, simple borders)

---

### S1-02: Manuscript Explorer (Left Sidebar)

**First: Add Backend Endpoints**

**File**: `webapp/backend/simple_app.py`

Add these endpoints:

```python
from factory.core.manuscript import Manuscript, ManuscriptStorage

# Global manuscript cache
_manuscript_cache = {}

@app.get("/api/manuscript/tree")
async def get_manuscript_tree():
    """Get hierarchical manuscript structure."""
    try:
        manuscript_path = project_path / ".manuscript" / "explants-v1"

        # Check if manuscript exists
        if not manuscript_path.exists():
            return {"acts": []}

        # Load manuscript
        storage = ManuscriptStorage(manuscript_path)
        manuscript = storage.load()

        if not manuscript:
            return {"acts": []}

        # Cache it
        _manuscript_cache['current'] = manuscript

        # Return tree structure
        return {
            "title": manuscript.title,
            "acts": [
                {
                    "id": act.id,
                    "title": act.title,
                    "chapters": [
                        {
                            "id": chapter.id,
                            "title": chapter.title,
                            "scenes": [
                                {
                                    "id": scene.id,
                                    "title": scene.title,
                                    "word_count": scene.word_count
                                }
                                for scene in chapter.scenes
                            ]
                        }
                        for chapter in act.chapters
                    ]
                }
                for act in manuscript.acts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load manuscript: {str(e)}")


@app.get("/api/scene/{scene_id}")
async def get_scene(scene_id: str):
    """Get specific scene content."""
    try:
        manuscript = _manuscript_cache.get('current')

        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        # Find scene by ID
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    if scene.id == scene_id:
                        return {
                            "id": scene.id,
                            "title": scene.title,
                            "content": scene.content,
                            "word_count": scene.word_count,
                            "notes": scene.notes,
                            "metadata": scene.metadata
                        }

        raise HTTPException(status_code=404, detail="Scene not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/scene/{scene_id}")
async def update_scene(scene_id: str, request: dict):
    """Update scene content (for autosave)."""
    try:
        content = request.get("content", "")

        manuscript = _manuscript_cache.get('current')
        if not manuscript:
            manuscript_path = project_path / ".manuscript" / "explants-v1"
            storage = ManuscriptStorage(manuscript_path)
            manuscript = storage.load()
            _manuscript_cache['current'] = manuscript

        # Find and update scene
        for act in manuscript.acts:
            for chapter in act.chapters:
                for scene in chapter.scenes:
                    if scene.id == scene_id:
                        scene.content = content
                        scene.word_count = len(content.split())

                        # Save manuscript
                        manuscript_path = project_path / ".manuscript" / "explants-v1"
                        storage = ManuscriptStorage(manuscript_path)
                        success = storage.save(manuscript)

                        if success:
                            return {
                                "success": True,
                                "word_count": scene.word_count,
                                "saved_at": "now"  # TODO: Add timestamp
                            }
                        else:
                            raise HTTPException(status_code=500, detail="Failed to save")

        raise HTTPException(status_code=404, detail="Scene not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/manuscript/node")
async def create_node(request: dict):
    """Create new scene/chapter/act."""
    # TODO: Implement in future sprint
    return {"success": False, "message": "Not implemented yet"}


@app.patch("/api/manuscript/node/{node_id}")
async def update_node(node_id: str, request: dict):
    """Rename/move node."""
    # TODO: Implement in future sprint
    return {"success": False, "message": "Not implemented yet"}


@app.delete("/api/manuscript/node/{node_id}")
async def delete_node(node_id: str):
    """Delete node."""
    # TODO: Implement in future sprint
    return {"success": False, "message": "Not implemented yet"}
```

**Frontend: File Tree Component**

**File**: `webapp/frontend-v2/src/features/explorer/FileTree.jsx`

```jsx
import { useQuery } from '@tanstack/react-query';
import { ChevronRight, ChevronDown, FileText } from 'lucide-react';
import { useState } from 'react';

export function FileTree({ onSceneSelect }) {
  const [expandedActs, setExpandedActs] = useState(new Set());
  const [expandedChapters, setExpandedChapters] = useState(new Set());

  const { data, isLoading } = useQuery({
    queryKey: ['manuscript-tree'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/manuscript/tree');
      return res.json();
    }
  });

  const toggleAct = (actId) => {
    const newSet = new Set(expandedActs);
    if (newSet.has(actId)) {
      newSet.delete(actId);
    } else {
      newSet.add(actId);
    }
    setExpandedActs(newSet);
  };

  const toggleChapter = (chapterId) => {
    const newSet = new Set(expandedChapters);
    if (newSet.has(chapterId)) {
      newSet.delete(chapterId);
    } else {
      newSet.add(chapterId);
    }
    setExpandedChapters(newSet);
  };

  if (isLoading) return <div className="p-4 text-gray-500">Loading...</div>;
  if (!data?.acts?.length) return <div className="p-4 text-gray-500">No manuscript loaded</div>;

  return (
    <div className="h-full overflow-y-auto text-sm">
      <div className="p-2 border-b border-gray-700 font-semibold text-gray-300">
        {data.title}
      </div>

      {data.acts.map(act => (
        <div key={act.id}>
          <div
            className="flex items-center gap-1 px-2 py-1 hover:bg-gray-700 cursor-pointer"
            onClick={() => toggleAct(act.id)}
          >
            {expandedActs.has(act.id) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            <span className="font-medium">{act.title}</span>
          </div>

          {expandedActs.has(act.id) && (
            <div className="ml-4">
              {act.chapters.map(chapter => (
                <div key={chapter.id}>
                  <div
                    className="flex items-center gap-1 px-2 py-1 hover:bg-gray-700 cursor-pointer"
                    onClick={() => toggleChapter(chapter.id)}
                  >
                    {expandedChapters.has(chapter.id) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    <span>{chapter.title}</span>
                  </div>

                  {expandedChapters.has(chapter.id) && (
                    <div className="ml-4">
                      {chapter.scenes.map(scene => (
                        <div
                          key={scene.id}
                          className="flex items-center gap-2 px-2 py-1 hover:bg-gray-700 cursor-pointer text-gray-300"
                          onClick={() => onSceneSelect(scene)}
                        >
                          <FileText size={14} />
                          <span>{scene.title}</span>
                          <span className="ml-auto text-xs text-gray-500">{scene.word_count}w</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

**Acceptance Criteria**:
- ✅ Tree loads manuscript from `/api/manuscript/tree`
- ✅ Acts collapse/expand on click
- ✅ Chapters collapse/expand on click
- ✅ Scenes show word count
- ✅ Click scene calls `onSceneSelect(scene)`
- ✅ Loading state shown while fetching
- ✅ Error handling with toast

---

### S1-03: Monaco Markdown Editor (Center Panel)

**File**: `webapp/frontend-v2/src/features/editor/SceneEditor.jsx`

```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Editor from '@monaco-editor/react';
import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { useDebounce } from '../hooks/useDebounce';

export function SceneEditor({ sceneId }) {
  const [content, setContent] = useState('');
  const [lastSaved, setLastSaved] = useState(null);
  const debouncedContent = useDebounce(content, 2000); // 2s autosave delay
  const queryClient = useQueryClient();

  // Load scene
  const { data: scene, isLoading } = useQuery({
    queryKey: ['scene', sceneId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`);
      if (!res.ok) throw new Error('Failed to load scene');
      return res.json();
    },
    enabled: !!sceneId
  });

  // Update content when scene loads
  useEffect(() => {
    if (scene?.content) {
      setContent(scene.content);
    }
  }, [scene]);

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async (newContent) => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
      if (!res.ok) throw new Error('Save failed');
      return res.json();
    },
    onSuccess: () => {
      setLastSaved(new Date());
      queryClient.invalidateQueries(['manuscript-tree']); // Update word counts
    },
    onError: () => {
      toast.error('Failed to save');
    }
  });

  // Autosave when content changes
  useEffect(() => {
    if (debouncedContent && debouncedContent !== scene?.content) {
      saveMutation.mutate(debouncedContent);
    }
  }, [debouncedContent]);

  // Manual save on Cmd+S
  useEffect(() => {
    const handleSave = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        saveMutation.mutate(content);
        toast.success('Saved');
      }
    };
    window.addEventListener('keydown', handleSave);
    return () => window.removeEventListener('keydown', handleSave);
  }, [content]);

  if (!sceneId) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        Select a scene to edit
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        Loading scene...
      </div>
    );
  }

  const wordCount = content.split(/\s+/).filter(Boolean).length;

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-700 px-4 py-2 flex items-center justify-between bg-gray-800">
        <h2 className="font-semibold">{scene?.title}</h2>
        <div className="flex items-center gap-4 text-sm text-gray-400">
          <span>{wordCount} words</span>
          {lastSaved && (
            <span>Saved {new Date(lastSaved).toLocaleTimeString()}</span>
          )}
          {saveMutation.isPending && <span className="text-yellow-500">Saving...</span>}
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1">
        <Editor
          height="100%"
          defaultLanguage="markdown"
          theme="vs-dark"
          value={content}
          onChange={(value) => setContent(value || '')}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            wordWrap: 'on',
            padding: { top: 16, bottom: 16 }
          }}
        />
      </div>
    </div>
  );
}
```

**Hook**: `webapp/frontend-v2/src/hooks/useDebounce.js`

```javascript
import { useEffect, useState } from 'react';

export function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

**Acceptance Criteria**:
- ✅ Loads scene content from `/api/scene/{id}`
- ✅ Monaco editor renders with markdown syntax
- ✅ Autosaves after 2s of inactivity
- ✅ Cmd/Ctrl+S forces immediate save
- ✅ Shows word count in header
- ✅ Shows "Saved at" timestamp
- ✅ Shows "Saving..." indicator during save
- ✅ Dark theme matching overall UI

---

### S1-04: Setup Wizard (First Run)

**File**: `webapp/frontend-v2/src/features/setup/SetupWizard.jsx`

```jsx
import { useState } from 'react';
import { toast } from 'sonner';

const PROVIDERS = [
  { id: 'anthropic', name: 'Anthropic', envKey: 'ANTHROPIC_API_KEY' },
  { id: 'openai', name: 'OpenAI', envKey: 'OPENAI_API_KEY' },
  { id: 'google', name: 'Google', envKey: 'GOOGLE_API_KEY' },
  { id: 'xai', name: 'xAI', envKey: 'XAI_API_KEY' },
  { id: 'mistral', name: 'Mistral', envKey: 'MISTRAL_API_KEY' },
  { id: 'qwen', name: 'Qwen', envKey: 'QWEN_API_KEY' },
  { id: 'deepseek', name: 'DeepSeek', envKey: 'DEEPSEEK_API_KEY' },
  { id: 'kimi', name: 'Moonshot Kimi', envKey: 'KIMI_API_KEY' },
  { id: 'chatglm', name: 'ChatGLM', envKey: 'CHATGLM_API_KEY' },
  { id: 'hunyuan', name: 'Tencent Hunyuan', envKey: 'HUNYUAN_API_KEY' },
];

export function SetupWizard({ onComplete }) {
  const [keys, setKeys] = useState({});
  const [testing, setTesting] = useState({});

  const handleTest = async (provider) => {
    setTesting({ ...testing, [provider.id]: true });

    // TODO: Add actual test endpoint
    setTimeout(() => {
      setTesting({ ...testing, [provider.id]: false });
      toast.success(`${provider.name} connection OK`);
    }, 1000);
  };

  const handleSave = () => {
    // Note: In production, this should save to .env.local or keychain
    localStorage.setItem('api_keys', JSON.stringify(keys));
    toast.success('API keys saved');
    onComplete();
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-2">Welcome to Writers Factory</h1>
      <p className="text-gray-400 mb-8">Configure your API keys to get started</p>

      <div className="space-y-4">
        {PROVIDERS.map(provider => (
          <div key={provider.id} className="border border-gray-700 rounded p-4">
            <div className="flex items-center justify-between mb-2">
              <label className="font-medium">{provider.name}</label>
              <button
                onClick={() => handleTest(provider)}
                disabled={!keys[provider.id] || testing[provider.id]}
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded text-sm"
              >
                {testing[provider.id] ? 'Testing...' : 'Test'}
              </button>
            </div>
            <input
              type="password"
              placeholder={`Enter ${provider.name} API key`}
              value={keys[provider.id] || ''}
              onChange={(e) => setKeys({ ...keys, [provider.id]: e.target.value })}
              className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded focus:outline-none focus:border-blue-500"
            />
            <div className="text-xs text-gray-500 mt-1">{provider.envKey}</div>
          </div>
        ))}
      </div>

      <div className="mt-8 flex justify-end gap-3">
        <button
          onClick={() => onComplete()}
          className="px-4 py-2 text-gray-400 hover:text-white"
        >
          Skip for now
        </button>
        <button
          onClick={handleSave}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium"
        >
          Save & Continue
        </button>
      </div>
    </div>
  );
}
```

**Acceptance Criteria**:
- ✅ Shows list of all providers
- ✅ Input fields for each API key (type=password)
- ✅ Test button per provider (stub for now)
- ✅ Save to localStorage (TODO: upgrade to .env.local)
- ✅ Skip button for testing
- ✅ Clean, simple form layout

---

## 📋 Sprint 2: AI Tools (Week 2)

### S2-01: AI Tools Tab (Right Panel)

**File**: `webapp/frontend-v2/src/features/tools/AIToolsPanel.jsx`

```jsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

const TEMPLATES = [
  { id: 'generate', label: 'Generate New Scene', endpoint: '/api/scene/generate' },
  { id: 'enhance', label: 'Enhance Scene', endpoint: '/api/scene/enhance' },
  { id: 'continue', label: 'Continue Scene', endpoint: '/api/scene/generate' },
  { id: 'voice', label: 'Voice Test', endpoint: '/api/scene/enhance' },
];

export function AIToolsPanel({ currentScene, models }) {
  const [selectedTemplate, setSelectedTemplate] = useState('generate');
  const [selectedModel, setSelectedModel] = useState('claude-sonnet-4.5');
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);

  const generateMutation = useMutation({
    mutationFn: async () => {
      const template = TEMPLATES.find(t => t.id === selectedTemplate);
      const res = await fetch(`http://localhost:8000${template.endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          model: selectedModel,
          scene_text: currentScene?.content,
          context: currentScene?.notes
        })
      });
      if (!res.ok) throw new Error('Generation failed');
      return res.json();
    },
    onSuccess: (data) => {
      setResult(data);
      toast.success('Generated successfully');
    },
    onError: () => {
      toast.error('Generation failed');
    }
  });

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3">AI Tools</h3>

        {/* Template Selector */}
        <div className="space-y-2 mb-4">
          {TEMPLATES.map(template => (
            <button
              key={template.id}
              onClick={() => setSelectedTemplate(template.id)}
              className={`w-full text-left px-3 py-2 rounded ${
                selectedTemplate === template.id
                  ? 'bg-blue-600'
                  : 'bg-gray-800 hover:bg-gray-700'
              }`}
            >
              {template.label}
            </button>
          ))}
        </div>

        {/* Model Selector */}
        <label className="block mb-2 text-sm text-gray-400">Model</label>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded mb-4"
        >
          {models?.map(model => (
            <option key={model.id} value={model.id}>
              {model.id}
            </option>
          ))}
        </select>

        {/* Prompt */}
        <label className="block mb-2 text-sm text-gray-400">Prompt</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt..."
          rows={4}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded mb-4 resize-none"
        />

        {/* Run Button */}
        <button
          onClick={() => generateMutation.mutate()}
          disabled={generateMutation.isPending || !prompt}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium"
        >
          {generateMutation.isPending ? 'Generating...' : 'Run'}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="flex-1 overflow-y-auto p-4">
          <div className="border border-gray-700 rounded p-4 bg-gray-800">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-gray-400">Result</span>
              <button
                onClick={() => navigator.clipboard.writeText(result.scene || result.enhanced_scene || '')}
                className="text-sm text-blue-400 hover:text-blue-300"
              >
                Copy
              </button>
            </div>
            <pre className="whitespace-pre-wrap text-sm">
              {result.scene || result.enhanced_scene || JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
```

**Acceptance Criteria**:
- ✅ Shows template buttons (Generate, Enhance, Continue, Voice Test)
- ✅ Model dropdown populated from `/api/models/available`
- ✅ Prompt textarea
- ✅ Run button calls appropriate endpoint
- ✅ Results display in panel below
- ✅ Copy button for result
- ✅ Loading state during generation

---

### S2-02: Knowledge Tab

**File**: `webapp/frontend-v2/src/features/tools/KnowledgePanel.jsx`

```jsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

export function KnowledgePanel() {
  const [source, setSource] = useState('cognee');
  const [query, setQuery] = useState('');
  const [snippets, setSnippets] = useState([]);
  const [selected, setSelected] = useState(new Set());

  const queryMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('http://localhost:8000/api/knowledge/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          source,
          limit: 5
        })
      });
      if (!res.ok) throw new Error('Query failed');
      return res.json();
    },
    onSuccess: (data) => {
      setSnippets(data.snippets || []);
      toast.success('Knowledge retrieved');
    },
    onError: () => {
      toast.error('Query failed');
    }
  });

  const toggleSnippet = (index) => {
    const newSelected = new Set(selected);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelected(newSelected);
  };

  return (
    <div className="h-full flex flex-col p-4">
      <h3 className="font-semibold mb-3">Knowledge Base</h3>

      {/* Source Selector */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setSource('cognee')}
          className={`flex-1 px-3 py-2 rounded ${
            source === 'cognee' ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'
          }`}
        >
          Cognee
        </button>
        <button
          onClick={() => setSource('notebooklm')}
          className={`flex-1 px-3 py-2 rounded ${
            source === 'notebooklm' ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'
          }`}
        >
          NotebookLM
        </button>
      </div>

      {/* Query Input */}
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question about your story..."
        rows={3}
        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded mb-4 resize-none"
      />

      <button
        onClick={() => queryMutation.mutate()}
        disabled={queryMutation.isPending || !query}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium mb-4"
      >
        {queryMutation.isPending ? 'Searching...' : 'Search'}
      </button>

      {/* Snippets */}
      {snippets.length > 0 && (
        <div className="flex-1 overflow-y-auto space-y-2">
          <div className="text-sm text-gray-400 mb-2">
            {selected.size} selected • ~{selected.size * 200} tokens
          </div>
          {snippets.map((snippet, i) => (
            <label
              key={i}
              className="flex items-start gap-2 p-3 bg-gray-800 border border-gray-700 rounded hover:bg-gray-750 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selected.has(i)}
                onChange={() => toggleSnippet(i)}
                className="mt-1"
              />
              <div className="flex-1 text-sm">
                <div className="text-gray-300">{snippet.text || snippet.content}</div>
                {snippet.source && (
                  <div className="text-xs text-gray-500 mt-1">{snippet.source}</div>
                )}
              </div>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
```

**Acceptance Criteria**:
- ✅ Source toggle: Cognee vs NotebookLM
- ✅ Query input and search button
- ✅ Calls `/api/knowledge/query` with source parameter
- ✅ Displays snippets with checkboxes
- ✅ Shows token budget estimate
- ✅ Selected snippets tracked in state (for future context inclusion)

---

### S2-03: Tournament Compare View

**File**: `webapp/frontend-v2/src/features/tools/TournamentPanel.jsx`

```jsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Star } from 'lucide-react';

export function TournamentPanel({ currentScene, models }) {
  const [selectedModels, setSelectedModels] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [results, setResults] = useState([]);
  const [votes, setVotes] = useState({});

  const toggleModel = (modelId) => {
    if (selectedModels.includes(modelId)) {
      setSelectedModels(selectedModels.filter(id => id !== modelId));
    } else if (selectedModels.length < 4) {
      setSelectedModels([...selectedModels, modelId]);
    } else {
      toast.error('Maximum 4 models');
    }
  };

  const compareMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('http://localhost:8000/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          models: selectedModels
        })
      });
      if (!res.ok) throw new Error('Comparison failed');
      return res.json();
    },
    onSuccess: (data) => {
      setResults(data.results || []);
      toast.success('Tournament complete');
    },
    onError: () => {
      toast.error('Tournament failed');
    }
  });

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3">Tournament Compare</h3>

        {/* Model Selection Grid */}
        <div className="grid grid-cols-2 gap-2 mb-4">
          {models?.slice(0, 8).map(model => (
            <button
              key={model.id}
              onClick={() => toggleModel(model.id)}
              className={`px-3 py-2 rounded text-sm ${
                selectedModels.includes(model.id)
                  ? 'bg-blue-600'
                  : 'bg-gray-800 hover:bg-gray-700'
              }`}
            >
              {model.id.split('-')[0]}
            </button>
          ))}
        </div>

        <div className="text-xs text-gray-400 mb-4">
          {selectedModels.length}/4 selected
        </div>

        {/* Prompt */}
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt for comparison..."
          rows={3}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded mb-4 resize-none"
        />

        <button
          onClick={() => compareMutation.mutate()}
          disabled={compareMutation.isPending || selectedModels.length < 2 || !prompt}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium"
        >
          {compareMutation.isPending ? 'Comparing...' : 'Run Tournament'}
        </button>
      </div>

      {/* Results Grid */}
      {results.length > 0 && (
        <div className="flex-1 overflow-y-auto p-4">
          <div className={`grid gap-4 ${results.length === 2 ? 'grid-cols-2' : 'grid-cols-1'}`}>
            {results.map((result, i) => (
              <div key={i} className="border border-gray-700 rounded p-4 bg-gray-800">
                <div className="flex items-center justify-between mb-3">
                  <span className="font-medium">{result.model}</span>
                  <button
                    onClick={() => setVotes({ ...votes, [i]: !votes[i] })}
                    className={votes[i] ? 'text-yellow-500' : 'text-gray-500'}
                  >
                    <Star size={18} fill={votes[i] ? 'currentColor' : 'none'} />
                  </button>
                </div>
                <pre className="whitespace-pre-wrap text-sm text-gray-300">
                  {result.output || result.scene}
                </pre>
                {result.cost && (
                  <div className="text-xs text-gray-500 mt-2">${result.cost.toFixed(4)}</div>
                )}
              </div>
            ))}
          </div>

          <button
            className="w-full mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 rounded font-medium"
            onClick={() => toast.info('Hybridize feature coming in Sprint 4')}
          >
            Hybridize Selected
          </button>
        </div>
      )}
    </div>
  );
}
```

**Acceptance Criteria**:
- ✅ Grid to select 2-4 models
- ✅ Prompt input
- ✅ Run button calls `/api/compare`
- ✅ Results display in grid (2 columns if 2 models, else 1)
- ✅ Star/vote buttons per result
- ✅ Cost shown per result
- ✅ Hybridize button (stub for now)

---

## 🎯 Main App Integration

**File**: `webapp/frontend-v2/src/App.jsx`

```jsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { useState, useEffect } from 'react';
import { FileTree } from './features/explorer/FileTree';
import { SceneEditor } from './features/editor/SceneEditor';
import { AIToolsPanel } from './features/tools/AIToolsPanel';
import { KnowledgePanel } from './features/tools/KnowledgePanel';
import { TournamentPanel } from './features/tools/TournamentPanel';
import { SetupWizard } from './features/setup/SetupWizard';

const queryClient = new QueryClient();

function App() {
  const [showSetup, setShowSetup] = useState(false);
  const [selectedScene, setSelectedScene] = useState(null);
  const [rightPanel, setRightPanel] = useState('tools'); // 'tools' | 'knowledge' | 'tournament'
  const [models, setModels] = useState([]);

  useEffect(() => {
    // Check if setup needed
    const hasKeys = localStorage.getItem('api_keys');
    if (!hasKeys) {
      setShowSetup(true);
    }

    // Load models
    fetch('http://localhost:8000/api/models/available')
      .then(res => res.json())
      .then(data => setModels(data.models || []));
  }, []);

  if (showSetup) {
    return (
      <QueryClientProvider client={queryClient}>
        <SetupWizard onComplete={() => setShowSetup(false)} />
        <Toaster />
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="h-screen flex flex-col bg-gray-900 text-gray-100">
        {/* Top Bar */}
        <div className="h-12 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
          <div className="flex items-center gap-4">
            <h1 className="font-bold">Writers Factory</h1>
            <select className="px-3 py-1 bg-gray-700 rounded text-sm">
              <option>Explants V1</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setRightPanel('tools')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'tools' ? 'bg-blue-600' : 'bg-gray-700'}`}
            >
              Tools
            </button>
            <button
              onClick={() => setRightPanel('knowledge')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'knowledge' ? 'bg-blue-600' : 'bg-gray-700'}`}
            >
              Knowledge
            </button>
            <button
              onClick={() => setRightPanel('tournament')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'tournament' ? 'bg-blue-600' : 'bg-gray-700'}`}
            >
              Tournament
            </button>
          </div>
        </div>

        {/* Main Layout */}
        <div className="flex-1">
          <PanelGroup direction="horizontal">
            {/* Left: File Tree */}
            <Panel defaultSize={20} minSize={15} className="border-r border-gray-700 bg-gray-800">
              <FileTree onSceneSelect={setSelectedScene} />
            </Panel>

            <PanelResizeHandle className="w-1 hover:bg-blue-500" />

            {/* Center: Editor */}
            <Panel defaultSize={50} minSize={30}>
              <SceneEditor sceneId={selectedScene?.id} />
            </Panel>

            <PanelResizeHandle className="w-1 hover:bg-blue-500" />

            {/* Right: Tools Panel */}
            <Panel defaultSize={30} minSize={20} className="border-l border-gray-700 bg-gray-800">
              {rightPanel === 'tools' && <AIToolsPanel currentScene={selectedScene} models={models} />}
              {rightPanel === 'knowledge' && <KnowledgePanel />}
              {rightPanel === 'tournament' && <TournamentPanel currentScene={selectedScene} models={models} />}
            </Panel>
          </PanelGroup>
        </div>
      </div>

      <Toaster position="bottom-right" />
    </QueryClientProvider>
  );
}

export default App;
```

---

## 🧪 Testing Requirements

### Backend Tests
```bash
# Ensure all existing tests still pass
cd /Users/gch2024/writers-factory-core
source .venv/bin/activate
export PYTHONPATH=.
pytest tests/ -v

# Should show: 156 tests passing
```

### Frontend Tests
```bash
cd webapp/frontend-v2
npm run build  # Should complete without errors
npm run dev    # Should start on localhost:5173
```

### Integration Tests (Manual)

**Sprint 1 Checklist**:
- [ ] File tree loads manuscript from backend
- [ ] Acts/Chapters/Scenes expand/collapse
- [ ] Click scene loads content in Monaco editor
- [ ] Edit scene and wait 2s → autosave triggers
- [ ] Cmd+S forces save
- [ ] Word count updates
- [ ] Setup wizard shows on first run
- [ ] API keys save to localStorage

**Sprint 2 Checklist**:
- [ ] AI Tools tab shows templates
- [ ] Generate button calls real backend
- [ ] Result displays in panel
- [ ] Knowledge tab queries Cognee/NotebookLM
- [ ] Snippets load and can be selected
- [ ] Tournament compare runs with 2-4 models
- [ ] Results display in grid
- [ ] Vote/star buttons work

---

## 📁 File Structure

```
writers-factory-core/
├── webapp/
│   ├── backend/
│   │   ├── simple_app.py          (UPDATE - add new endpoints)
│   │   └── agent_integration.py   (EXISTING - keep as is)
│   └── frontend-v2/               (NEW - create this)
│       ├── src/
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   ├── features/
│       │   │   ├── explorer/
│       │   │   │   └── FileTree.jsx
│       │   │   ├── editor/
│       │   │   │   └── SceneEditor.jsx
│       │   │   ├── tools/
│       │   │   │   ├── AIToolsPanel.jsx
│       │   │   │   ├── KnowledgePanel.jsx
│       │   │   │   └── TournamentPanel.jsx
│       │   │   └── setup/
│       │   │       └── SetupWizard.jsx
│       │   ├── hooks/
│       │   │   └── useDebounce.js
│       │   └── index.css
│       ├── index.html
│       ├── vite.config.js
│       ├── tailwind.config.js
│       └── package.json
└── factory/                       (EXISTING - don't touch)
    ├── core/
    ├── tools/
    └── wizard/
```

---

## 🚀 Getting Started

### Step 1: Review Existing Code
```bash
cd /Users/gch2024/writers-factory-core
git status
git log --oneline -10

# Read these files:
cat webapp/backend/simple_app.py
cat webapp/backend/agent_integration.py
cat factory/core/manuscript/structure.py
```

### Step 2: Update Backend
Add the new endpoints to `webapp/backend/simple_app.py`:
- GET /api/manuscript/tree
- GET /api/scene/{scene_id}
- PUT /api/scene/{scene_id}

### Step 3: Create Frontend
```bash
cd webapp
npm create vite@latest frontend-v2 -- --template react
cd frontend-v2
npm install
# ... install dependencies
```

### Step 4: Build Components
Follow the order:
1. S1-01: App shell + layout
2. S1-02: FileTree component + backend endpoints
3. S1-03: SceneEditor component
4. S1-04: SetupWizard
5. S2-01: AIToolsPanel
6. S2-02: KnowledgePanel
7. S2-03: TournamentPanel

### Step 5: Test
```bash
# Terminal 1: Backend
cd /Users/gch2024/writers-factory-core
python3 webapp/launch.py

# Terminal 2: Frontend
cd webapp/frontend-v2
npm run dev

# Open browser: http://localhost:5173
```

---

## ✅ Definition of Done

### Sprint 1 Complete When:
- ✅ React app boots on localhost:5173
- ✅ 3-pane layout with resizing works
- ✅ File tree loads Acts → Chapters → Scenes
- ✅ Click scene loads in Monaco editor
- ✅ Autosave after 2s idle
- ✅ Cmd+S manual save works
- ✅ Setup wizard shows on first run
- ✅ Clean, Cursor AI-style aesthetic

### Sprint 2 Complete When:
- ✅ AI Tools panel has 4 templates
- ✅ Generate/Enhance calls real backend
- ✅ Results display correctly
- ✅ Knowledge panel queries both sources
- ✅ Tournament compare runs 2-4 models
- ✅ Results grid displays with voting
- ✅ All panels switch via top bar tabs

---

## 💡 Key Principles

1. **Keep It Simple**: Cursor AI style, not fancy webapp
2. **Text-Focused**: Writers want words, not graphics
3. **Use Existing Backend**: Don't rebuild what works
4. **Dark Theme**: Easy on eyes for long writing sessions
5. **Keyboard Shortcuts**: Power users will love them
6. **Clean Code**: Others will maintain this

---

## 🔗 Resources

- **Backend API**: http://localhost:8000/docs (FastAPI auto-docs)
- **Existing Tests**: `/tests/` directory (156 tests)
- **Manuscript Models**: `factory/core/manuscript/structure.py`
- **Agent Config**: `config/agents.yaml`
- **Phase 3 Review**: `PHASE_3_REVIEW.md`

---

## 📞 Questions?

If stuck, check:
1. PHASE_3_REVIEW.md - What's already built
2. COMPLETE_INVENTORY.md - Full system overview
3. Simple_app.py - Existing API endpoints
4. Ask Claude Code for clarification

---

## 🎯 Success Metrics

**Sprint 1 Success**:
- User can navigate their manuscript
- User can edit scenes in Monaco
- Autosave works reliably
- No errors in console

**Sprint 2 Success**:
- User can generate scenes with AI
- User can compare 2-4 models side-by-side
- User can query knowledge base
- All tools feel smooth and responsive

---

## 🚦 Ready to Start?

1. Read this entire document
2. Review existing backend code
3. Create feature branch: `git checkout -b sprint-1-2-ui`
4. Start with S1-01: React scaffold
5. Build incrementally, test often
6. Commit frequently with clear messages
7. When done, create PR for Claude Code to review

**Let's build something writers will love!** 🚀

---

**Document Version**: 1.0
**Last Updated**: November 14, 2025
**Maintained By**: Claude Code
