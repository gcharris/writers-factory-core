# Cloud Agent Sprint 3 Tasks

**Date**: November 14, 2025
**Status**: Ready to start
**Previous Work**: Sprint 1+2 APPROVED ✅ (Grade: A+)

---

## 🎉 Sprint 1+2 Review Results

**Your work was EXCELLENT!** Here's what Claude Code found:

- ✅ All features delivered (100% complete)
- ✅ Code quality: A+ (98/100)
- ✅ Design matches vision perfectly
- ✅ Build succeeds with no errors
- ✅ Production-ready code

**Approved for merge to main** 🚀

---

## 🎯 Sprint 3: Ollama Integration + Economy Mode

Now that the foundation is solid, add local model support and cost optimization features.

**Timeline**: 1-2 days
**Priority**: HIGH (user wants local models integrated)

---

## 📋 Tasks

### Task 3-01: Ollama Detection & Model List

**Backend** (`webapp/backend/simple_app.py`):

Add endpoint to detect Ollama and list models:

```python
from factory.agents.ollama_agent import OllamaAgent

@app.get("/api/ollama/status")
async def ollama_status():
    """Check if Ollama is running and list models."""
    try:
        is_running = OllamaAgent.is_available()

        if not is_running:
            return {
                "available": False,
                "models": [],
                "message": "Ollama not running. Start with: brew services start ollama"
            }

        models = OllamaAgent.list_models()

        return {
            "available": True,
            "models": models,
            "endpoint": "http://localhost:11434"
        }
    except Exception as e:
        return {
            "available": False,
            "models": [],
            "error": str(e)
        }
```

**Frontend** (`src/features/ollama/OllamaStatus.jsx` - NEW):

Create component to show Ollama status:

```jsx
import { useQuery } from '@tanstack/react-query';

export function OllamaStatus() {
  const { data } = useQuery({
    queryKey: ['ollama-status'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/ollama/status');
      return res.json();
    },
    refetchInterval: 30000 // Check every 30s
  });

  if (!data?.available) {
    return (
      <div className="px-4 py-2 bg-yellow-900/20 border-b border-yellow-700/50 text-yellow-200 text-sm">
        ⚠️ Ollama not running - only cloud models available
      </div>
    );
  }

  return (
    <div className="px-4 py-2 bg-green-900/20 border-b border-green-700/50 text-green-200 text-sm">
      ✅ Ollama running - {data.models.length} local models available (FREE!)
    </div>
  );
}
```

**Acceptance**:
- ✅ Shows green banner when Ollama running
- ✅ Shows yellow warning when Ollama not running
- ✅ Lists number of available local models

---

### Task 3-02: Update Model Selector with Local Badges

**Update**: `src/features/tools/AIToolsPanel.jsx`

Modify model dropdown to show local vs cloud:

```jsx
<select
  value={selectedModel}
  onChange={(e) => setSelectedModel(e.target.value)}
  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded mb-4"
>
  <optgroup label="💰 Free (Local Models)">
    {models?.filter(m => m.is_local).map(model => (
      <option key={model.id} value={model.id}>
        🦙 {model.id} - FREE
      </option>
    ))}
  </optgroup>

  <optgroup label="☁️ Cloud Models">
    {models?.filter(m => !m.is_local).map(model => (
      <option key={model.id} value={model.id}>
        {model.id} (${model.cost_output}/1K)
      </option>
    ))}
  </optgroup>
</select>
```

**Also update**:
- `TournamentPanel.jsx` - Same model grouping
- Model grid should show local badge visually

**Acceptance**:
- ✅ Models grouped: Local first, then Cloud
- ✅ Local models show 🦙 icon and "FREE"
- ✅ Cloud models show cost estimate
- ✅ Clear visual distinction

---

### Task 3-03: Economy Mode Toggle

**Backend** (`webapp/backend/simple_app.py`):

Add economy mode to agent selection logic:

```python
def select_agent_for_task(task_type: str, economy_mode: bool = False):
    """Select best agent based on task type and economy mode."""
    if economy_mode:
        # Prefer local models for cheap tasks
        if task_type in ['draft', 'paraphrase', 'continue', 'brainstorm']:
            return 'ollama-mistral'  # or ollama-llama3

    # Default to cloud for quality tasks
    task_models = {
        'generate': 'claude-sonnet-4.5',
        'enhance': 'claude-sonnet-4.5',
        'voice': 'claude-opus-4',
        'polish': 'claude-opus-4'
    }

    return task_models.get(task_type, 'claude-sonnet-4.5')
```

**Frontend** (`src/App.jsx`):

Add economy mode toggle in top bar:

```jsx
const [economyMode, setEconomyMode] = useState(false);

// In top bar, add toggle:
<div className="flex items-center gap-2">
  <label className="flex items-center gap-2 text-sm">
    <input
      type="checkbox"
      checked={economyMode}
      onChange={(e) => setEconomyMode(e.target.checked)}
      className="w-4 h-4"
    />
    <span>Economy Mode</span>
    {economyMode && <span className="text-xs text-green-400">(Using local models)</span>}
  </label>
</div>
```

**Acceptance**:
- ✅ Toggle in top bar
- ✅ When ON: Prefer local models for drafts
- ✅ When OFF: Use cloud models
- ✅ Visual indicator when active
- ✅ Saves preference to localStorage

---

### Task 3-04: Cost Dashboard Panel

**Create**: `src/features/cost/CostDashboard.jsx`

```jsx
export function CostDashboard({ onClose }) {
  const { data: sessionCost } = useQuery({
    queryKey: ['session-cost'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/session/cost');
      return res.json();
    },
    refetchInterval: 5000
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 max-w-md w-full">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Session Cost</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            ✕
          </button>
        </div>

        <div className="space-y-4">
          {/* Total Cost */}
          <div className="bg-gray-900 rounded p-4">
            <div className="text-sm text-gray-400">Total This Session</div>
            <div className="text-3xl font-bold text-green-400">
              ${sessionCost?.total.toFixed(4) || '0.0000'}
            </div>
          </div>

          {/* Breakdown */}
          <div className="space-y-2">
            <div className="text-sm font-semibold text-gray-300">Breakdown by Model</div>
            {sessionCost?.by_model?.map((item, i) => (
              <div key={i} className="flex justify-between text-sm">
                <span>{item.model}</span>
                <span className={item.is_local ? 'text-green-400' : 'text-gray-300'}>
                  {item.is_local ? 'FREE' : `$${item.cost.toFixed(4)}`}
                </span>
              </div>
            ))}
          </div>

          {/* Savings */}
          {sessionCost?.savings > 0 && (
            <div className="bg-green-900/20 border border-green-700/50 rounded p-3">
              <div className="text-sm text-green-200">
                💰 Saved ${sessionCost.savings.toFixed(2)} using local models!
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

**Add button in top bar**:
```jsx
<button
  onClick={() => setShowCostDashboard(true)}
  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
>
  💰 ${sessionCost?.total.toFixed(2) || '0.00'}
</button>
```

**Backend** (`webapp/backend/simple_app.py`):

```python
_session_cost = {"total": 0.0, "by_model": [], "savings": 0.0}

@app.get("/api/session/cost")
async def get_session_cost():
    """Get session cost breakdown."""
    return _session_cost

# Update _session_cost when AI calls are made
```

**Acceptance**:
- ✅ Shows total cost in top bar
- ✅ Click to see detailed breakdown
- ✅ Shows savings from using local models
- ✅ Updates in real-time
- ✅ Shows which model was used for what

---

### Task 3-05: Agent Profiles

**Create**: `src/features/profiles/AgentProfiles.jsx`

Allow users to save model preferences:

```jsx
export function AgentProfiles() {
  const [profiles, setProfiles] = useState({
    dialogue: 'qwen-max',
    action: 'mistral-large',
    description: 'claude-sonnet-4.5',
    draft: 'ollama-mistral',
    polish: 'claude-opus-4'
  });

  const taskTypes = [
    { id: 'dialogue', label: 'Dialogue Writing' },
    { id: 'action', label: 'Action Scenes' },
    { id: 'description', label: 'Descriptions' },
    { id: 'draft', label: 'Quick Drafts' },
    { id: 'polish', label: 'Final Polish' }
  ];

  return (
    <div className="p-4 space-y-4">
      <h3 className="font-semibold mb-3">Agent Profiles</h3>
      <p className="text-sm text-gray-400 mb-4">
        Set which model to use for different tasks
      </p>

      {taskTypes.map(task => (
        <div key={task.id} className="space-y-1">
          <label className="text-sm text-gray-300">{task.label}</label>
          <select
            value={profiles[task.id]}
            onChange={(e) => {
              const newProfiles = { ...profiles, [task.id]: e.target.value };
              setProfiles(newProfiles);
              localStorage.setItem('agent_profiles', JSON.stringify(newProfiles));
            }}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-sm"
          >
            {models.map(m => (
              <option key={m.id} value={m.id}>
                {m.id} {m.is_local ? '(Free)' : `($${m.cost_output}/1K)`}
              </option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );
}
```

**Add to top bar**:
```jsx
<button
  onClick={() => setShowProfiles(true)}
  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
>
  ⚙️ Profiles
</button>
```

**Acceptance**:
- ✅ Configure model per task type
- ✅ Saves to localStorage
- ✅ AI Tools uses profiles when generating
- ✅ Shows cost estimate per profile

---

### Task 3-06: Update agents.yaml in Frontend

**Backend** (`webapp/backend/simple_app.py`):

Update `/api/models/available` to include `is_local` flag:

```python
@app.get("/api/models/available")
async def get_available_models():
    """Get list of all available models."""
    try:
        agents = get_enabled_agents()
        models = []

        for agent_name, agent_config in agents.items():
            models.append({
                "id": agent_name,
                "provider": agent_config.get("provider"),
                "description": agent_config.get("description"),
                "cost_input": agent_config.get("cost_per_1k_input"),
                "cost_output": agent_config.get("cost_per_1k_output"),
                "strengths": agent_config.get("strengths", []),
                "is_local": agent_config.get("is_local", False),  # ADD THIS
                "endpoint": agent_config.get("endpoint")
            })

        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load models: {str(e)}")
```

**Acceptance**:
- ✅ Models API includes `is_local` flag
- ✅ Frontend can filter local vs cloud
- ✅ All existing features still work

---

## 🎯 Success Criteria

**Sprint 3 Complete When**:
- ✅ Ollama status banner shows in UI
- ✅ Model selector groups local vs cloud
- ✅ Economy mode toggle works
- ✅ Cost dashboard shows breakdown
- ✅ Agent profiles save preferences
- ✅ Local models show "FREE" label
- ✅ All previous features still work

---

## 📁 File Changes Expected

**New Files**:
- `src/features/ollama/OllamaStatus.jsx`
- `src/features/cost/CostDashboard.jsx`
- `src/features/profiles/AgentProfiles.jsx`

**Modified Files**:
- `webapp/backend/simple_app.py` (add 2 endpoints)
- `src/App.jsx` (add economy toggle, cost button, profiles button)
- `src/features/tools/AIToolsPanel.jsx` (update model selector)
- `src/features/tools/TournamentPanel.jsx` (update model selector)

---

## 🧪 Testing

After implementation:

1. **Test Ollama Detection**:
   - Stop Ollama: `brew services stop ollama`
   - Should show yellow warning
   - Start Ollama: `brew services start ollama`
   - Should show green status

2. **Test Economy Mode**:
   - Toggle ON
   - Generate a scene
   - Should use `ollama-mistral` (check console/network)

3. **Test Cost Dashboard**:
   - Generate with cloud model
   - Check cost updates
   - Generate with local model
   - Check savings shown

4. **Test Agent Profiles**:
   - Set "Quick Drafts" to `ollama-llama3`
   - Select "Generate New Scene" template
   - Should auto-select llama3

---

## 💡 Tips

**From Previous Sprints**:
- You did excellent work keeping code clean
- Continue using React Query for data fetching
- Keep components focused and small
- Add loading states for all API calls

**New Considerations**:
- Ollama might not be running - handle gracefully
- Cost tracking needs to persist across refreshes
- Agent profiles should feel intuitive

---

## 🚀 Ready to Start?

You have all the context:
- ✅ Sprint 1+2 code is solid foundation
- ✅ Ollama backend already integrated (by Claude Code)
- ✅ agents.yaml has local models configured
- ✅ Just need to add UI components

**Estimated time**: 1-2 days (6 tasks)

**Expected outcome**: Full local model support with cost optimization!

Let's make Sprint 3 as excellent as Sprint 1+2! 🦙💰

---

**Document Created**: November 14, 2025
**For**: Cloud Agent (Sprint 3)
**Previous Grade**: A+ on Sprint 1+2
**Status**: Ready to start immediately
