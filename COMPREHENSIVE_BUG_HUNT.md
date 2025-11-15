# Comprehensive Bug Hunt - Test Everything

**Mission:** Systematically test EVERY component of Writers Factory, not just Sprint 14

**Philosophy:** "If we haven't run it, it's broken until proven otherwise"

---

## Why This Matters

Sprint 14 had **13 bugs** in just 4 API endpoints. We have:
- **23,088 lines of code** total
- **10 major subsystems**
- **35+ features** (per Field Guide)
- Most of it **NEVER TESTED**

If Sprint 14 had 13 bugs in ~400 lines, the whole system probably has **hundreds of bugs** waiting to be found.

---

## The Systematic Approach

Test each subsystem in order, from bottom to top (dependencies first):

### Phase 1: Core Foundation (Week 1)
1. ✅ Storage layer (Session, CostTracker, HistoryManager, PreferencesManager)
2. ✅ Manuscript structure (Scene, Chapter, Part, Manuscript)
3. Agent pool (multi-agent management)
4. Workflow engine (workflow execution)
5. Configuration system

### Phase 2: Analysis & Intelligence (Week 1-2)
6. ✅ Voice extractor (analyze writing voice)
7. Knowledge graph (manuscript relationships)
8. Manuscript ingester (import documents)
9. Character extractor
10. Plot tracker
11. Motif analyzer
12. Location extractor
13. Strategic planner

### Phase 3: Skills & Generation (Week 2)
14. ✅ Skill generator (create custom skills)
15. ✅ Skill orchestrator (route skill requests)
16. ✅ Project creator (initialize projects)
17. MCP server (Claude Code integration)
18. MCP skill bridge
19. Knowledge router (project-specific routing)

### Phase 4: Integrations (Week 2-3)
20. NotebookLM client (browser automation)
21. NotebookLM setup integration
22. Ollama agent (local LLM)
23. Chinese LLM agents (5 providers)

### Phase 5: Workflows (Week 3)
24. Scene generation workflow
25. Scene enhancement workflow
26. Voice testing workflow
27. Multi-model comparison workflow
28. Project genesis workflow

### Phase 6: Tools (Week 3)
29. Model comparison tool
30. Manuscript importer (Scrivener/Word)
31. File migration script

### Phase 7: UI Layers (Week 4)
32. CLI interface
33. TUI (Textual terminal UI)
34. Wizard (interactive setup)
35. ✅ Backend API (4 setup endpoints working)
36. Frontend React app (12+ components)

---

## How to Test Each Component

### 1. Import Test
**Goal:** Verify module loads without errors

```python
python3 -c "
from factory.core.agent_pool import AgentPool
print('✅ AgentPool imports successfully')
"
```

**Common issues:**
- Missing dependencies
- Import path errors
- Circular imports

### 2. Initialization Test
**Goal:** Create an instance with valid parameters

```python
python3 -c "
from factory.core.agent_pool import AgentPool
pool = AgentPool(max_agents=5)
print(f'✅ AgentPool initialized: {pool}')
"
```

**Common issues:**
- Wrong parameter names
- Missing required parameters
- Type mismatches

### 3. Basic Functionality Test
**Goal:** Call the main methods with sample data

```python
python3 -c "
from factory.core.agent_pool import AgentPool
from anthropic import Anthropic
import os

pool = AgentPool(max_agents=3)
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
# Test basic operations
print('✅ AgentPool basic operations work')
"
```

**Common issues:**
- Method name mismatches
- Parameter order errors
- Async/sync confusion

### 4. Integration Test
**Goal:** Test component working with other components

```python
# Test AgentPool + WorkflowEngine together
```

**Common issues:**
- Interface mismatches
- Data format incompatibilities
- Missing error handling

### 5. End-to-End Test
**Goal:** Test realistic user scenario

```bash
# Example: Create project, generate scene, enhance it
curl -X POST http://127.0.0.1:8000/api/setup/create-project ...
# Then use the created skills
```

---

## Testing Priority (Start Here)

### 🔥 Critical (Test First)
Components users will actually use:

1. **Setup Wizard** (✅ Done - 13 bugs found)
2. **Scene generation workflow** - Generate scenes with custom skills
3. **Scene enhancement workflow** - Improve existing scenes
4. **Model comparison** - Tournament between AI models
5. **Manuscript importer** - Import from Scrivener/Word

### ⚠️ Important (Test Next)
Core infrastructure:

6. **Knowledge graph** - Understand manuscript structure
7. **Manuscript ingester** - Parse novels
8. **Character/plot extractors** - Analysis intelligence
9. **Skill orchestrator routing** - Direct skills to right projects
10. **MCP server** - Claude Code integration

### 📋 Nice to Have (Test Later)
Experimental/alternative interfaces:

11. **TUI interface** - Terminal UI (may be abandoned)
12. **Chinese LLM agents** - International providers (experimental)
13. **CLI commands** - Command-line interface
14. **Frontend components** - React UI (mostly working)

---

## Test Script Template

For each component, create a test file:

```python
# tests/test_component_name.py

import pytest
from factory.core.component_name import ComponentClass

def test_import():
    """Test 1: Module imports without errors"""
    assert ComponentClass is not None

def test_initialization():
    """Test 2: Can create instance with valid params"""
    instance = ComponentClass(required_param="value")
    assert instance is not None

def test_basic_operation():
    """Test 3: Main method works with sample data"""
    instance = ComponentClass(required_param="value")
    result = instance.main_method(test_data)
    assert result is not None

def test_error_handling():
    """Test 4: Handles invalid input gracefully"""
    instance = ComponentClass(required_param="value")
    with pytest.raises(ValueError):
        instance.main_method(invalid_data)

def test_integration():
    """Test 5: Works with dependent components"""
    # Test with real dependencies
    pass
```

---

## Common Bug Patterns (From Sprint 14)

Based on 13 bugs found in Sprint 14:

### Pattern #1: Parameter Mismatches (40% of bugs)
**Symptom:** `__init__() got unexpected keyword argument`
**Cause:** Endpoint uses different param names than actual class
**Fix:** Read the actual class signature, fix the caller

### Pattern #2: Missing Dependencies (15% of bugs)
**Symptom:** `ModuleNotFoundError`
**Cause:** Library not installed
**Fix:** Add to requirements.txt and `pip install`

### Pattern #3: Method Name Errors (15% of bugs)
**Symptom:** `object has no attribute 'method_name'`
**Cause:** Caller uses wrong method name
**Fix:** Check actual class, update caller

### Pattern #4: Async/Sync Confusion (10% of bugs)
**Symptom:** `object is not awaitable` or vice versa
**Cause:** Mixing async/sync incorrectly
**Fix:** Add/remove `await` and `async`

### Pattern #5: Attribute Access Errors (15% of bugs)
**Symptom:** `object has no attribute 'attr'`
**Cause:** Wrong attribute name or wrong type
**Fix:** Check actual dataclass/object definition

### Pattern #6: Type Mismatches (5% of bugs)
**Symptom:** `object is not iterable`
**Cause:** Expected list but got single object
**Fix:** Check actual return type

---

## Bug Tracking

For each bug found:

1. **Document it** - Add to BUG_SQUASHING_SESSION.md
2. **Number it** - Continue from Bug #13
3. **Describe it** - File, line, error message
4. **Fix it** - Make minimal fix to match actual interface
5. **Test it** - Verify fix works
6. **Commit it** - Clear commit message

---

## Success Criteria

**Phase 1 Complete:**
- ✅ All core modules import without errors
- ✅ All core modules initialize with valid params
- ✅ Basic operations work for each module

**Phase 2 Complete:**
- ✅ All analysis modules tested
- ✅ Knowledge graph can ingest a manuscript
- ✅ Extractors produce valid output

**Phase 3 Complete:**
- ✅ Can generate skills for new project
- ✅ Skills route to correct project
- ✅ MCP server accepts skill requests

**Phase 4 Complete:**
- ✅ NotebookLM integration works
- ✅ At least one alternative LLM agent works
- ✅ Ollama local LLM functional

**Phase 5 Complete:**
- ✅ Scene generation end-to-end
- ✅ Scene enhancement end-to-end
- ✅ Model comparison tournament
- ✅ Voice testing workflow

**Final Success:**
- ✅ Every module tested
- ✅ All critical paths working
- ✅ 100+ bugs found and fixed
- ✅ System ready for real users

---

## Resources

**Time:** 4 weeks recommended (1 week per phase)
**Budget:** $900 in Claude credits + subscription
**Approach:** Test systematically, not randomly

**Current Progress:**
- ✅ Sprint 14 complete (13 bugs fixed)
- ⚠️ ~95% of codebase untested
- 🎯 Next: Scene generation workflow

---

## Quick Start Commands

**Test a specific module:**
```bash
python3 -c "from factory.workflows.scene_operations.generation import SceneGenerationWorkflow; print('✅')"
```

**Run existing tests:**
```bash
pytest tests/test_manuscript_structure.py -v
```

**Test with real API:**
```bash
# Start backend
python3 webapp/backend/simple_app.py > /tmp/backend.log 2>&1 &

# Test endpoint
curl -X POST http://127.0.0.1:8000/api/scene/generate ...
```

---

## Philosophy

**"Test it before you ship it. Test it even if you're not shipping it."**

Every line of untested code is a ticking time bomb.
Every bug you find now is a disaster you prevent later.

Sprint 14 proved this: **4 endpoints, 13 bugs, 100% success after fixing.**

Now let's do that for the other **23,000 lines**. 🔨

---

**Ready to start? Begin with Phase 1, Component #3: Agent Pool**
