# Master Instructions: Complete Writers Factory Implementation

**Repository**: `writers-factory-core`
**Your Access**: Full read/write/push permissions
**Work Mode**: Autonomous - Complete all tasks sequentially without waiting for approval

---

## Mission

You are implementing the complete Writers Factory system - a multi-model AI novel writing tool. All task specifications have been uploaded to this repository in the `docs/tasks/` directory.

**Your job**: Implement each task in order, commit your work, push to the repository, and continue to the next task. When all 7 tasks are complete, report back with a summary.

---

## Work Protocol

### For Each Task:

1. **Read** the task document thoroughly from `docs/tasks/TASK_*.md`
2. **Implement** the functionality as specified
3. **Test** your implementation (unit tests + integration tests)
4. **Commit** your work with descriptive commit messages
5. **Push** to the `writers-factory-core` repository
6. **Continue** to the next task immediately

### Commit Message Format:

```
[Task N] Brief description

- Bullet point of what was implemented
- Another key feature added
- Tests added/updated

Closes: TASK_<name>
```

Example:
```
[Task 1] Implement Storage & Session Management

- File-based JSON storage for sessions
- Auto-save system with 30s interval
- Cost tracking with budget warnings
- Crash recovery on startup
- Session history (last 20 sessions)

Closes: TASK_Storage_Session_Management
```

### Testing Requirements:

For each task:
- ✅ Write unit tests in `factory/tests/`
- ✅ Write integration tests where applicable
- ✅ Manually test the feature works end-to-end
- ✅ Document any assumptions or deviations from spec

---

## Implementation Order

Complete these tasks in sequence:

### **Task 1: Storage & Session Management** (3-4 hours)
**File**: `docs/tasks/TASK_Storage_Session_Management.md`
**Priority**: CRITICAL - Foundation for everything else

**What to Build**:
- File-based JSON storage (`project/.session/`)
- Auto-save system (30s intervals, non-blocking)
- Cost tracking per operation
- Session history (last 20 sessions)
- Crash recovery

**Deliverables**:
```
factory/core/storage/
├── __init__.py
├── session.py              # Session class
├── cost_tracker.py         # CostTracker class
├── preferences.py          # Preferences management
├── history.py              # Session history
├── file_watcher.py         # File change detection
└── json_store.py           # Thread-safe JSON storage

factory/core/storage/models/
├── __init__.py
├── session_data.py         # Pydantic models
├── cost_data.py            # Pydantic models
└── history_data.py         # Pydantic models

factory/tests/storage/
├── test_session.py
├── test_cost_tracker.py
└── test_crash_recovery.py
```

**Success Check**:
- [ ] Auto-save runs every 30s without blocking
- [ ] Cost tracking logs all operations accurately
- [ ] Session recovers after simulated crash
- [ ] History shows last 20 sessions

---

### **Task 2: Master CLI (Rich TUI)** (4-5 hours)
**File**: `docs/tasks/TASK_Master_CLI.md`
**Priority**: HIGH - User-facing interface

**What to Build**:
- Rich TUI implementation (NOT basic CLI)
- 5-stage navigation (Creation → Writing → Enhancing → Analyzing → Scoring)
- Status bar with pipeline progress
- Cost dashboard
- Keyboard-first navigation
- Implements the UX design from `docs/UX_DESIGN_SPECIFICATION.md`

**Deliverables**:
```
factory/ui/
├── __init__.py
├── tui.py                  # Main TUI class
├── components/
│   ├── status_bar.py       # Status bar component
│   ├── stage_view.py       # Base stage view
│   ├── dashboard.py        # Main dashboard
│   └── cost_dashboard.py   # Cost tracking view
├── stages/
│   ├── creation_stage.py   # Creation wizard UI
│   ├── writing_stage.py    # Writing UI
│   ├── enhancing_stage.py  # Enhancing UI
│   ├── analyzing_stage.py  # Analyzing UI
│   └── scoring_stage.py    # Scoring UI
└── keyboard.py             # Keyboard handler

factory/tests/ui/
├── test_tui_navigation.py
└── test_keyboard_shortcuts.py
```

**Status Bar Format** (from UX spec):
```
Creation ✓ | Writing ⚡ (45/120) | Enhancing | Analyzing | Scoring   Session: $2.47   ● 12s ago
```

**Success Check**:
- [ ] `factory start` launches Rich TUI
- [ ] Status bar shows stage progress and costs
- [ ] TAB/SHIFT+TAB navigates between stages
- [ ] Keyboard shortcuts work (C, H, E, Q, etc.)
- [ ] UI matches ASCII mockups in UX spec

---

### **Task 3: Knowledge Router** (3-4 hours)
**File**: `docs/tasks/TASK_Knowledge_Router.md`
**Priority**: HIGH - Powers intelligent query routing

**What to Build**:
- Cognee integration (local, 17MB, hidden from users)
- NotebookLM integration (external, optional, user-configured)
- Intelligent query routing based on query type
- **NOT** exposing Gemini File Search to users

**Deliverables**:
```
factory/knowledge/
├── __init__.py
├── router.py               # KnowledgeRouter class
├── cognee_client.py        # Cognee integration
├── notebooklm_client.py    # NotebookLM integration
└── query_analyzer.py       # Query classification

factory/tests/knowledge/
├── test_router.py
├── test_cognee.py
└── test_notebooklm.py
```

**Query Routing Logic**:
```python
Factual/character questions → Cognee (instant, local)
Creative/thematic questions → NotebookLM (if configured)
Fallback → Cognee
```

**Success Check**:
- [ ] Cognee is invisible to users (they just "ask questions")
- [ ] NotebookLM is opt-in during Creation Wizard
- [ ] Query routing works automatically
- [ ] Users never see "Gemini File Search" option

---

### **Task 4: Workflows Module** (4-5 hours)
**File**: `docs/tasks/TASK_Workflows_Module.md`
**Priority**: HIGH - Core writing operations

**What to Build**:
- Scene generation workflow
- Scene enhancement workflow (voice, pacing, dialogue)
- Voice testing workflow
- Integration with Knowledge Router
- Integration with Cost Tracker

**Deliverables**:
```
factory/workflows/
├── __init__.py
├── scene_generation.py     # SceneGenerationWorkflow
├── scene_enhancement.py    # SceneEnhancementWorkflow
├── voice_testing.py        # VoiceTestingWorkflow
└── workflow_base.py        # Base workflow class

factory/tests/workflows/
├── test_scene_generation.py
├── test_scene_enhancement.py
└── test_voice_testing.py
```

**Key Workflows**:
```python
class SceneGenerationWorkflow:
    async def generate(
        prompt: str,
        model: str,
        knowledge_context: Optional[str] = None
    ) -> GeneratedScene

class SceneEnhancementWorkflow:
    async def enhance(
        scene_text: str,
        enhancement_type: str,  # "voice", "pacing", "dialogue"
        model: str
    ) -> EnhancedScene

class VoiceTestingWorkflow:
    async def test_voice(
        scene_text: str,
        character_name: str
    ) -> VoiceTestReport
```

**Success Check**:
- [ ] Scene generation works with knowledge context
- [ ] Enhancement works (voice, pacing, dialogue)
- [ ] Voice testing produces detailed reports
- [ ] Cost warnings appear before expensive operations

---

### **Task 5: Model Comparison Tool** (3-4 hours)
**File**: `docs/tasks/TASK_Model_Comparison_Tool.md`
**Priority**: MEDIUM - Repurposed tournament system

**What to Build**:
- Side-by-side model comparison (2-4 models)
- Visual diff highlighting
- Cost comparison
- User voting/preference tracking
- **Repurpose existing tournament orchestrator** as this tool

**Deliverables**:
```
factory/tools/
├── __init__.py
├── model_comparison.py     # ModelComparisonTool class
└── diff_viewer.py          # Visual diff component

factory/tests/tools/
└── test_model_comparison.py
```

**Integration Point**:
```python
# In Writing stage:
# User presses 'C' → Model Comparison Tool opens

class ModelComparisonTool:
    def __init__(self, tournament_orchestrator: TournamentOrchestrator):
        self.orchestrator = tournament_orchestrator

    async def compare_models(
        prompt: str,
        models: List[str],  # ["claude-sonnet-3.5", "gemini-flash", "gpt-4"]
        context: Optional[str] = None
    ) -> ComparisonResult
```

**Success Check**:
- [ ] Press 'C' in Writing stage → Comparison tool opens
- [ ] Side-by-side comparison shows 2-4 models
- [ ] Visual diff highlights differences
- [ ] User can select winner → Preference saved
- [ ] Tournament orchestrator successfully repurposed

---

### **Task 6: Creation Wizard** (6-8 hours)
**File**: `docs/tasks/TASK_Creation_Wizard.md`
**Priority**: MEDIUM - Most complex, depends on all other systems

**What to Build**:
- Conversational questionnaire (NOT form-like)
- 5 phases: Foundation → Character → Plot → World → Symbolism
- Save the Cat! 15-beat structure
- Integrated "Find Your Voice" tool
- NotebookLM linking (optional)
- Marathon runner progress indicator

**Deliverables**:
```
factory/wizard/
├── __init__.py
├── wizard.py               # Main wizard orchestrator
├── phases/
│   ├── foundation.py       # Phase 1: Foundation
│   ├── character.py        # Phase 2: Character construction
│   ├── plot.py             # Phase 3: Save the Cat! 15 beats
│   ├── world.py            # Phase 4: World & context
│   └── symbolism.py        # Phase 5: Symbolic layering
├── tools/
│   └── find_your_voice.py  # Voice discovery tool
└── output/
    └── story_bible.py      # 4,000-6,000 word output generator

factory/tests/wizard/
├── test_wizard_flow.py
├── test_phases.py
└── test_voice_tool.py
```

**Phase Structure**:
- **Phase 1**: Foundation (15-25 questions, ~25 minutes)
- **Phase 2**: Character Construction (30-40 questions, ~40 minutes)
- **Phase 3**: Plot Architecture (25-35 questions, ~35 minutes)
- **Phase 4**: World & Context (15-20 questions, ~15 minutes)
- **Phase 5**: Symbolic Layering (10-15 questions, optional)

**Success Check**:
- [ ] `factory init` launches conversational wizard
- [ ] Wizard feels conversational, not form-like
- [ ] Marathon runner progress indicator works
- [ ] "Find Your Voice" tool generates style samples
- [ ] Output: 4,000-6,000 word story bible
- [ ] NotebookLM linking (optional) works

---

### **Task 7: Integration & Polish** (2-3 hours)
**Priority**: FINAL - Tie everything together

**What to Do**:
1. **End-to-end testing**:
   - Run full user journey: `factory init` → `factory start` → navigate stages
   - Test crash recovery (kill process, restart)
   - Test cost warnings and tracking
   - Test knowledge queries during writing
   - Test model comparison tool

2. **Documentation**:
   - Update main README.md with usage instructions
   - Create ARCHITECTURE.md explaining the hybrid system
   - Document API reference for each module
   - Add troubleshooting guide

3. **Performance optimization**:
   - Ensure auto-save doesn't block UI
   - Optimize knowledge query response times
   - Check for memory leaks in long sessions

4. **Polish**:
   - Clean up any TODOs in code
   - Ensure consistent error messages
   - Add helpful user feedback throughout UI
   - Test all keyboard shortcuts

**Deliverables**:
```
docs/
├── README.md               # Updated with usage guide
├── ARCHITECTURE.md         # Hybrid architecture explained
├── API_REFERENCE.md        # API docs for each module
└── TROUBLESHOOTING.md      # Common issues & fixes

factory/tests/integration/
├── test_full_workflow.py   # End-to-end user journey
├── test_crash_recovery.py  # Crash scenarios
└── test_performance.py     # Performance benchmarks
```

**Success Check**:
- [ ] Full user journey works end-to-end
- [ ] All 23 success criteria from rebuild prompt met
- [ ] Documentation is complete and clear
- [ ] No blocking bugs or performance issues

---

## Architecture Context

### What Exists (Keep & Build On)

From the previous agent's work:

✅ **Agent Pool System** (`factory/core/agent_pool.py`)
- Multi-LLM registry
- Chinese LLM integrations (DeepSeek, Qwen, etc.)
- **Keep this** - it's solid

✅ **Tournament Orchestrator** (`factory/core/tournament_orchestrator.py`)
- Parallel model execution
- **Repurpose as Model Comparison Tool** in Task 5

✅ **SQLite Analytics** (`factory/storage/`)
- Keep for metrics/analytics only
- Add file-based session storage (Task 1)

✅ **UX Design Specification** (`docs/UX_DESIGN_SPECIFICATION.md`)
- Your excellent 67KB design spec
- **Implement this** in Task 2 (Master CLI)

### Hybrid Architecture Vision

```
┌─────────────────────────────────────────────────────────────┐
│                    RICH TUI INTERFACE                        │
│  Status Bar: Creation ✓ | Writing ⚡ | Enhancing | Analyzing│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              5-STAGE WORKFLOW (Primary System)               │
│  Creation → Writing → Enhancing → Analyzing → Scoring       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     CORE SYSTEMS                             │
│  • Agent Pool ✅                                              │
│  • Knowledge Router 🏗️                                       │
│  • Storage & Sessions 🏗️                                     │
│  • Cost Tracker 🏗️                                           │
│  • Model Comparison Tool 🏗️ (tournament repurposed)         │
└─────────────────────────────────────────────────────────────┘
```

**Key Principle**: Tournament system is **one tool** within the Writing stage, not the core architecture.

---

## Key Architecture Decisions

### 1. Storage Strategy

**Session/Manuscript Data** → File-based JSON
```
project/
├── .session/
│   ├── current.json      # Active session
│   ├── history.json      # Last 20 sessions
│   └── costs.json        # Cost tracking
├── manuscript/
├── reference/
└── planning/
```

**Analytics/Metrics** → SQLite (existing)
```
factory/storage/
└── analytics.db
```

### 2. Knowledge System

**Cognee (Local)**:
- 17MB footprint, instant responses
- **Hidden from users** - they just "ask questions"
- Handles factual/character queries

**NotebookLM (External)**:
- User-configured during Creation Wizard
- **Optional** - not everyone has Google account
- Creative/thematic queries

**Gemini File Search**:
- **Not exposed to users** as selectable option

### 3. Cost Tracking

**Before every expensive operation** (> $0.10):
```
⚠️  This operation will cost approximately $0.15
    (claude-sonnet-3.5, ~12,000 tokens)
    Continue? [Y/n]
```

**Budget warnings**:
```
⚠️  You've used 80% of your daily budget ($40/$50)
```

---

## Testing Strategy

### Unit Tests (Each Task)
```python
# Write tests alongside implementation
factory/tests/<module>/
├── test_<component1>.py
├── test_<component2>.py
└── test_<component3>.py
```

### Integration Tests (Task 7)
```python
# Test full workflows
factory/tests/integration/
├── test_full_workflow.py
├── test_crash_recovery.py
└── test_cost_tracking.py
```

### Manual Testing (Each Task)
- Test the feature works end-to-end
- Test error handling
- Test edge cases
- Document any issues

---

## Success Criteria (All 23 from Rebuild Prompt)

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

## Common Pitfalls to Avoid

### 1. Don't Over-Engineer Storage
❌ Complex SQLite schema for everything
✅ Simple JSON files for sessions, SQLite only for analytics

### 2. Don't Expose Too Many Knowledge Options
❌ "Choose: Cognee, NotebookLM, Gemini File Search, or RAG?"
✅ User just asks questions. System routes intelligently.

### 3. Don't Make Tournament the Core
❌ Every operation goes through tournament system
✅ Tournament is **one tool** in Writing stage (Model Comparison)

### 4. Don't Block UI During Operations
❌ Synchronous LLM calls that freeze the interface
✅ Async operations with progress indicators

### 5. Don't Forget Cost Warnings
❌ User accidentally spends $50 on one operation
✅ Warn before operations > $0.10, show estimates

---

## Final Report Template

When all tasks are complete, create a report:

```markdown
# Writers Factory Implementation Complete

## Summary

All 7 tasks have been completed and pushed to `writers-factory-core` repository.

## Commits Summary

- [Task 1] Storage & Session Management - <commit hash>
- [Task 2] Master CLI (Rich TUI) - <commit hash>
- [Task 3] Knowledge Router - <commit hash>
- [Task 4] Workflows Module - <commit hash>
- [Task 5] Model Comparison Tool - <commit hash>
- [Task 6] Creation Wizard - <commit hash>
- [Task 7] Integration & Polish - <commit hash>

## Success Criteria

All 23 success criteria met:
- ✅ Core Functionality (5/5)
- ✅ Knowledge System (4/4)
- ✅ Writing Workflows (3/3)
- ✅ Model Comparison Tool (4/4)
- ✅ Creation Wizard (4/4)
- ✅ Session Management (3/3)

## Tests Written

- Unit tests: <count> tests across <count> modules
- Integration tests: <count> end-to-end workflows
- All tests passing

## Known Issues / Assumptions

[Document any deviations from specs or assumptions made]

## Next Steps

The system is ready for user testing. Recommended:
1. Manual walkthrough: `factory init` → `factory start`
2. Test crash recovery
3. Test long session (2+ hours) for memory leaks
4. Get user feedback on UX
```

---

## Questions?

If you encounter ambiguities:
1. **Read the task documents** in `docs/tasks/`
2. **Review the UX spec** in `docs/UX_DESIGN_SPECIFICATION.md`
3. **Review the rebuild prompt** in `docs/PROMPT_Cloud_Agent_Rebuild.md`
4. **Document your assumptions** and proceed
5. **Ask clarifying questions** only if truly blocked

---

## Your Mission

✅ Complete all 7 tasks sequentially
✅ Commit and push after each task
✅ Write tests for everything
✅ When done, create final report
✅ Report back with summary

**You have full autonomy. Don't wait for approval between tasks. Keep moving forward.**

Good luck! 🚀
