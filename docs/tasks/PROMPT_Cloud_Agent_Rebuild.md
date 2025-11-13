# Task: Rebuild Writers Factory Core with Hybrid Architecture

**Priority**: Critical
**Estimated Time**: 2-3 days
**Repository**: `writers-factory-core` (you have full read/write/push access)

---

## Context: What You're Building

You are rebuilding the **Writers Factory** - a multi-model AI novel writing system that helps authors write, enhance, analyze, and score their fiction using multiple LLM providers in parallel.

**Previous Work**: A previous agent created an excellent UX design specification and partially implemented a tournament-based architecture. You'll be building on this foundation but pivoting to a **hybrid architecture** that merges two approaches:

1. **Tournament System** (keep as a specialized tool)
2. **Stage-Based Workflow** (build as the primary interface)

---

## The Hybrid Architecture Vision

### What We're Merging

**From Tournament Architecture** (already partially built):
- ✅ **Agent Pool System** (`factory/core/agent_pool.py`) - Keep this! It's solid.
- ✅ **Tournament Orchestrator** - Repurpose as "Model Comparison Tool" (one tool among many)
- ✅ **SQLite Analytics** (`factory/storage/`) - Keep for metrics/analytics only
- ✅ **Chinese LLM Integrations** (DeepSeek, Qwen, etc.) - Keep the agent registry

**From Stage-Based UX Design** (you created the spec, now implement it):
- 🏗️ **Rich TUI Interface** - Implement your excellent UX design spec
- 🏗️ **5-Stage Workflow Pipeline**: Creation → Writing → Enhancing → Analyzing → Scoring
- 🏗️ **File-Based Session Management** (JSON for sessions, not SQLite)
- 🏗️ **Multiple Specialized Tools** (tournament is just one of them)

### Architecture Principle

```
┌─────────────────────────────────────────────────────────────┐
│                    RICH TUI INTERFACE                        │
│  Status Bar: Creation ✓ | Writing ⚡ | Enhancing | Analyzing│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              5-STAGE WORKFLOW (Primary System)               │
│                                                              │
│  Stage 1: CREATION WIZARD                                    │
│    └─ Conversational questionnaire (15-beat structure)      │
│                                                              │
│  Stage 2: WRITING                                            │
│    └─ Scene generation, enhancement, voice testing          │
│    └─ Tools: Knowledge Router, Model Comparison             │
│                                                              │
│  Stage 3: ENHANCING                                          │
│    └─ Surgical fixes, voice consistency                     │
│                                                              │
│  Stage 4: ANALYZING                                          │
│    └─ Scene evaluation, scoring                             │
│                                                              │
│  Stage 5: SCORING                                            │
│    └─ Comparative analysis, multiplier variants             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     CORE SYSTEMS                             │
│                                                              │
│  • Agent Pool (multi-LLM registry) ✅ Already built          │
│  • Knowledge Router (Cognee + NotebookLM)                   │
│  • Storage & Sessions (file-based JSON)                     │
│  • Cost Tracker                                              │
│  • Model Comparison Tool (tournament repurposed) ✅          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## What Exists Now (Review First)

### Files to Review in `writers-factory-core`

1. **`docs/UX_DESIGN_SPECIFICATION.md`** (67KB)
   - Your excellent work! This is the visual design to implement.
   - 15+ ASCII mockups showing all screens
   - Status bar design, keyboard shortcuts, cost dashboard

2. **`factory/core/agent_pool.py`**
   - Agent registry system
   - **Keep this** - it's solid foundation

3. **`factory/core/workflow_engine.py`**
   - Basic workflow orchestration
   - Needs expansion for 5-stage pipeline

4. **`factory/agents/`**
   - Base agent class + 5 Chinese LLMs
   - **Keep this** - integrate into Agent Pool

5. **`factory/storage/`**
   - SQLite analytics database
   - **Keep for analytics only** - add file-based session storage

---

## Task Documents You'll Implement

In the parent repository (`The-Explants`), there are 6 detailed task documents in `factory/docs/`:

### 1. **TASK_Storage_Session_Management.md** (16KB)
**Why First**: Foundation for everything else
- File-based JSON storage for sessions (not SQLite)
- Auto-save system (30s interval)
- Cost tracking per session
- Crash recovery
- Session history

**Directory Structure to Create**:
```
project/
├── .session/              # Session state (gitignored)
│   ├── current.json      # Active session data
│   ├── history.json      # Session history
│   ├── costs.json        # Cost tracking
│   └── preferences.json  # User preferences
```

**Key API**:
```python
class Session:
    async def save()
    async def load(session_id: str = "current")
    def set_stage(stage: str)
    def set_model_preference(stage: str, model: str)
    def add_recent_query(query: str, source: str)
    def has_changes() -> bool

class CostTracker:
    async def log_operation(operation, model, input_tokens, output_tokens)
    def get_estimated_cost(model: str, estimated_tokens: int) -> float
    def should_warn_budget() -> Optional[str]
```

---

### 2. **TASK_Master_CLI.md** (23KB)
**Why Second**: The user interface layer
- Rich TUI implementation (NOT basic CLI)
- Implements your UX design specification
- 5-stage navigation
- Status bar with pipeline progress
- Cost dashboard
- Keyboard-first navigation

**Core Implementation**:
```python
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

class WritersFactoryTUI:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.session = Session()

    def render_status_bar(self):
        """Creation ✓ | Writing ⚡ (45/120) | Enhancing | Analyzing"""

    def render_stage(self, stage: str):
        """Render current stage view"""
```

**Status Bar Format** (from your UX spec):
```
Creation ✓ | Writing ⚡ (45/120) | Enhancing | Analyzing | Scoring   Session: $2.47   ● 12s ago
```

---

### 3. **TASK_Knowledge_Router.md** (20KB)
**Why Third**: Powers intelligent query routing
- Integrates **Cognee** (local, 17MB, hidden from users)
- Integrates **NotebookLM** (external, user-configured, optional)
- Intelligent query routing based on query type
- NOT exposing Gemini File Search to users

**Query Routing Logic**:
```python
class KnowledgeRouter:
    async def route_query(self, query: str) -> KnowledgeSource:
        """
        Factual/character questions → Cognee (instant, local)
        Creative/thematic questions → NotebookLM (if configured)
        Fallback → Cognee
        """
```

**User Experience**:
- Cognee is **invisible** to users (they just "ask questions")
- NotebookLM is **opt-in** during Creation Wizard
- Users never see "Gemini File Search" option

---

### 4. **TASK_Workflows_Module.md** (23KB)
**Why Fourth**: Core writing operations
- Scene generation workflow
- Scene enhancement workflow
- Voice testing workflow
- Integration with Knowledge Router
- Integration with Cost Tracker

**Key Workflows**:
```python
class SceneGenerationWorkflow:
    async def generate(
        self,
        prompt: str,
        model: str,
        knowledge_context: Optional[str] = None
    ) -> GeneratedScene

class SceneEnhancementWorkflow:
    async def enhance(
        self,
        scene_text: str,
        enhancement_type: str,  # "voice", "pacing", "dialogue"
        model: str
    ) -> EnhancedScene

class VoiceTestingWorkflow:
    async def test_voice(
        self,
        scene_text: str,
        character_name: str
    ) -> VoiceTestReport
```

---

### 5. **TASK_Model_Comparison_Tool.md** (24KB)
**Why Fifth**: Repurposed tournament system
- **This is where the tournament code gets repurposed**
- Side-by-side model comparison (2-4 models)
- Visual diff highlighting
- Cost comparison
- User voting/preference tracking

**Integration Point**:
```python
# In Writing stage:
# User presses 'C' → Model Comparison Tool

class ModelComparisonTool:
    async def compare_models(
        self,
        prompt: str,
        models: List[str],  # ["claude-sonnet-3.5", "gemini-flash", "gpt-4"]
        context: Optional[str] = None
    ) -> ComparisonResult
```

**This uses the tournament orchestrator** you already have, but exposed as a **tool within the Writing stage**, not the primary interface.

---

### 6. **TASK_Creation_Wizard.md** (35KB)
**Why Last**: Most complex, depends on all other systems
- Conversational questionnaire (not form-like)
- 5 phases: Foundation → Character → Plot → World → Symbolism
- Save the Cat! 15-beat structure
- Integrated "Find Your Voice" tool
- NotebookLM linking (optional)
- Marathon runner progress indicator

**Phase Structure**:
```
Phase 1: Foundation (15-25 questions, ~25 minutes)
  ├─ Mindset & commitment assessment
  ├─ High concept development
  └─ Theme/message identification

Phase 2: Character Construction (30-40 questions, ~40 minutes)
  ├─ True character vs characterization
  ├─ Character flaw & growth
  └─ Supporting cast

Phase 3: Plot Architecture (25-35 questions, ~35 minutes)
  └─ Save the Cat! 15 beats with midpoint clarification

Phase 4: World & Context (15-20 questions, ~15 minutes)
  └─ Setting, info-dumping avoidance, opening clichés

Phase 5: Symbolic Layering (10-15 questions, optional)
```

---

## Implementation Priority & Strategy

### Suggested Order

**Week 1: Foundation**
1. ✅ Review existing code (`agent_pool.py`, `workflow_engine.py`, `agents/`)
2. 🏗️ **TASK_Storage_Session_Management** - File-based JSON storage
3. 🏗️ **TASK_Master_CLI** - Rich TUI shell (stage navigation, status bar)

**Week 2: Integration**
4. 🏗️ **TASK_Knowledge_Router** - Cognee + NotebookLM integration
5. 🏗️ **TASK_Workflows_Module** - Scene generation, enhancement, voice testing
6. 🏗️ **TASK_Model_Comparison_Tool** - Repurpose tournament as comparison tool

**Week 3: Creation Wizard**
7. 🏗️ **TASK_Creation_Wizard** - Conversational questionnaire (most complex)

---

## Key Architecture Decisions

### 1. Storage Strategy

**Session/Manuscript Data** → File-based (JSON/Markdown)
```
project/
├── .session/
│   ├── current.json
│   ├── history.json
│   └── costs.json
├── manuscript/
├── reference/
└── planning/
```

**Analytics/Metrics** → SQLite (keep existing)
```
factory/storage/
└── analytics.db
```

**Why Both?**
- File-based: Easy to backup, version control, human-readable, no schema migrations
- SQLite: Efficient for analytics queries, historical metrics, cost aggregations

### 2. Knowledge System Architecture

**Cognee (Local)**:
- 17MB footprint
- Instant responses
- **Hidden from users** - they just "ask questions"
- Handles factual/character queries

**NotebookLM (External)**:
- User-configured during Creation Wizard
- **Optional** - not everyone has Google account
- Creative/thematic queries
- Audio summaries (unique feature)

**Gemini File Search**:
- **Not exposed to users** as a selectable option
- May be used internally by Cognee/NotebookLM
- Users never see "Gemini File Search" in UI

### 3. Tournament → Model Comparison Tool

**Current Tournament Code** (`factory/core/tournament_orchestrator.py`):
```python
class TournamentOrchestrator:
    async def run_tournament(
        self,
        prompt: str,
        agents: List[Agent]
    ) -> TournamentResult
```

**Repurpose as**:
```python
class ModelComparisonTool:
    def __init__(self, tournament_orchestrator: TournamentOrchestrator):
        self.orchestrator = tournament_orchestrator

    async def compare_models(
        self,
        prompt: str,
        models: List[str]
    ) -> ComparisonResult:
        """User-facing wrapper around tournament system"""
        agents = [self.agent_pool.get(model) for model in models]
        tournament_result = await self.orchestrator.run_tournament(prompt, agents)
        return self._format_for_ui(tournament_result)
```

**Invocation**: User presses `C` in Writing stage → Model Comparison Tool opens → Side-by-side comparison → User selects winner → Preference saved

### 4. Rich TUI Implementation

**Your UX Design** (`UX_DESIGN_SPECIFICATION.md`) already specifies:
- Layout structure (header, main, status bar)
- Keyboard shortcuts (TAB, SHIFT+TAB, C, H, E, Q, etc.)
- ASCII mockups for each screen

**Implementation Pattern**:
```python
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

class WritersFactoryTUI:
    def __init__(self):
        self.console = Console()
        self.layout = self._create_layout()
        self.session = Session(Path.cwd() / "project")
        self.current_stage = self.session.data.current_state.stage

    def _create_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="status_bar", size=1),
            Layout(name="main"),
            Layout(name="footer", size=1)
        )
        return layout

    def render_status_bar(self):
        stage_indicators = self._get_stage_indicators()
        cost_info = self.session.cost_tracker.session_total
        save_info = self._get_save_time_elapsed()

        return Panel(
            f"{stage_indicators}   Session: ${cost_info:.2f}   ● {save_info}",
            style="bold white on blue"
        )

    async def main_loop(self):
        with Live(self.layout, console=self.console, refresh_per_second=4):
            while True:
                key = await self._get_key()
                await self._handle_key(key)
```

---

## Integration with Parent Repository

The parent repository (`The-Explants`) contains:
- Manuscript files (`project/manuscript/`)
- Reference materials (`project/reference/`)
- Task documents (`factory/docs/TASK_*.md`)
- This is the **USER'S PROJECT**

Your `writers-factory-core` repository is the **REUSABLE TOOL** that operates on projects like `The-Explants`.

**Usage Model**:
```bash
cd ~/The-Explants
factory init   # Creates project/ structure if needed
factory start  # Launches Rich TUI
```

**File Structure**:
```
~/The-Explants/                    # User's project
├── project/
│   ├── .session/                  # Auto-generated
│   ├── manuscript/
│   ├── reference/
│   └── planning/
└── factory/                       # Your tool
    └── docs/                      # Task specs you're implementing
        ├── TASK_Storage_Session_Management.md
        ├── TASK_Master_CLI.md
        ├── TASK_Knowledge_Router.md
        ├── TASK_Workflows_Module.md
        ├── TASK_Model_Comparison_Tool.md
        └── TASK_Creation_Wizard.md

~/writers-factory-core/            # Your repository
├── factory/
│   ├── core/
│   │   ├── agent_pool.py         ✅ Keep
│   │   ├── tournament_orchestrator.py  ✅ Repurpose
│   │   └── workflow_engine.py    ✅ Expand
│   ├── agents/                    ✅ Keep
│   ├── storage/                   ✅ Keep + Expand
│   ├── knowledge/                 🏗️ Build (Cognee + NotebookLM)
│   ├── workflows/                 🏗️ Build
│   └── ui/                        🏗️ Build (Rich TUI)
└── docs/
    └── UX_DESIGN_SPECIFICATION.md ✅ Your excellent work
```

---

## Success Criteria

Your rebuild is complete when:

### Core Functionality
1. ✅ User can launch `factory start` and see Rich TUI with 5-stage pipeline
2. ✅ Status bar shows stage progress, costs, and auto-save status
3. ✅ User can navigate between stages with TAB/SHIFT+TAB
4. ✅ Auto-save runs every 30 seconds without blocking UI
5. ✅ Cost tracking logs all operations and warns before expensive operations

### Knowledge System
6. ✅ User can ask questions from any stage
7. ✅ Questions route to Cognee (local) or NotebookLM (if configured)
8. ✅ Users never see "Gemini File Search" option
9. ✅ Cognee is invisible (users just "ask questions")

### Writing Workflows
10. ✅ User can generate scenes with knowledge context
11. ✅ User can enhance existing scenes (voice, pacing, dialogue)
12. ✅ User can run voice tests on scenes

### Model Comparison Tool
13. ✅ User can press 'C' in Writing stage → Model Comparison opens
14. ✅ Side-by-side comparison shows 2-4 model outputs
15. ✅ Visual diff highlights differences
16. ✅ User can select winner → Preference saved

### Creation Wizard
17. ✅ User can run `factory init` → Conversational wizard starts
18. ✅ Wizard feels conversational, not form-like
19. ✅ 5 phases with progress indicator (marathon runner)
20. ✅ Output: 4,000-6,000 word story bible

### Session Management
21. ✅ If system crashes, session recovers on restart
22. ✅ User loses < 30 seconds of work
23. ✅ History shows last 20 sessions

---

## Testing Strategy

### Phase 1: Unit Tests
```python
# test_session.py
async def test_session_save_load()
async def test_cost_tracking()
async def test_crash_recovery()

# test_knowledge_router.py
async def test_query_routing()
async def test_cognee_integration()
async def test_notebooklm_integration()

# test_workflows.py
async def test_scene_generation()
async def test_scene_enhancement()
async def test_voice_testing()

# test_model_comparison.py
async def test_tournament_repurposed()
async def test_side_by_side_comparison()
```

### Phase 2: Integration Tests
```python
# test_full_workflow.py
async def test_creation_to_writing_pipeline()
async def test_knowledge_query_during_writing()
async def test_model_comparison_preference_tracking()
async def test_cost_warnings_before_expensive_ops()
```

### Phase 3: Manual Testing
```bash
# Test full user journey:
cd ~/The-Explants
factory init    # Run Creation Wizard
factory start   # Launch TUI
# Navigate through stages
# Generate scenes
# Run model comparison
# Test crash recovery (kill process, restart)
```

---

## Common Pitfalls to Avoid

### 1. Don't Over-Engineer Storage
❌ **Bad**: Complex SQLite schema for everything
✅ **Good**: Simple JSON files for sessions, SQLite only for analytics

### 2. Don't Expose Too Many Knowledge Options
❌ **Bad**: "Choose: Cognee, NotebookLM, Gemini File Search, or RAG?"
✅ **Good**: User just asks questions. System routes intelligently.

### 3. Don't Make Tournament the Core
❌ **Bad**: Every operation goes through tournament system
✅ **Good**: Tournament is **one tool** in the Writing stage (Model Comparison)

### 4. Don't Block UI During Operations
❌ **Bad**: Synchronous LLM calls that freeze the interface
✅ **Good**: Async operations with progress indicators

### 5. Don't Forget Cost Warnings
❌ **Bad**: User accidentally spends $50 on one operation
✅ **Good**: Warn before operations > $0.10, show estimates

---

## Questions? Assumptions?

If anything is unclear:
1. **Read the task documents** in `The-Explants/factory/docs/`
2. **Review your UX spec** in `docs/UX_DESIGN_SPECIFICATION.md`
3. **Document your assumptions** and proceed
4. **Ask clarifying questions** if truly blocked

---

## Expected Timeline

**Week 1**: Storage + Master CLI (foundation)
**Week 2**: Knowledge Router + Workflows + Model Comparison (integration)
**Week 3**: Creation Wizard (polish)

**Total**: 2-3 weeks for full implementation

---

## Final Notes

You've already proven your abilities with the excellent UX design specification. This rebuild is about **implementing that vision** while merging it with the solid agent pool foundation that already exists.

**Key Philosophy**:
- Tournament system was a good idea → Repurpose as Model Comparison Tool
- Stage-based workflow is the primary interface → Your UX design is perfect
- Keep what works (agent pool, analytics) → Build what's missing (Rich TUI, knowledge router)

**You have full access** to `writers-factory-core` repository (read, write, commit, push). The task documents are in the parent repository (`The-Explants/factory/docs/`) - read them carefully before implementing each component.

**Good luck!** Your UX design was exceptional. Now bring it to life. 🚀
