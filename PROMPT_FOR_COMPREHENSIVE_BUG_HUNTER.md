# Comprehensive Bug Hunter - System-Wide Testing

## Mission: Test Every Component, Find Every Bug 🔨

Sprint 14 testing found **13 bugs in 400 lines**. We have **23,088 lines total**.

Your job: Systematically test EVERY subsystem. Find and fix HUNDREDS of bugs.

---

## Read These Files First

1. **COMPREHENSIVE_BUG_HUNT.md** - Your testing roadmap
2. **BUG_SQUASHING_SESSION.md** - Sprint 14 results (what we learned)
3. **docs/WRITERS_FACTORY_FIELD_GUIDE.md** - What each component does

---

## Your Systematic Approach

**DON'T:** Randomly test things
**DO:** Work through components in order (dependencies first)

### Week 1: Foundation & Analysis
- Test core storage, manuscript structure
- Test voice analysis, knowledge graph
- Test extractors (character, plot, motif, location)

### Week 2: Skills & Generation
- Test skill generation and orchestration
- Test MCP server integration
- Test project creation (already ✅ working)

### Week 3: Workflows & Integrations
- Test scene generation/enhancement workflows
- Test model comparison
- Test NotebookLM integration

### Week 4: UI & End-to-End
- Test TUI, CLI, Wizard
- Test frontend components
- Full user scenario testing

---

## Testing Process (For Each Component)

```bash
# 1. Import test
python3 -c "from factory.core.agent_pool import AgentPool; print('✅')"

# 2. Initialization test
python3 -c "
from factory.core.agent_pool import AgentPool
pool = AgentPool(max_agents=3)
print(f'✅ Created: {pool}')
"

# 3. Basic operation test
# Write test_agent_pool.py with real usage scenarios

# 4. Integration test
# Test AgentPool + WorkflowEngine together

# 5. End-to-end test
# Test full user workflow using this component
```

---

## Bug Patterns to Watch For

From Sprint 14's 13 bugs:

1. **Parameter mismatches** (40%) - Wrong param names
2. **Missing dependencies** (15%) - Module not installed
3. **Method name errors** (15%) - Wrong method name
4. **Async/sync confusion** (10%) - await mistakes
5. **Attribute errors** (15%) - Wrong attribute names
6. **Type mismatches** (5%) - Object vs list confusion

**Every component will have similar bugs!**

---

## Priority Order (Test These First)

### 🔥 Critical (Users Need These)
1. Scene generation workflow
2. Scene enhancement workflow
3. Model comparison/tournament
4. Manuscript importer
5. Knowledge graph analysis

### ⚠️ Important (Infrastructure)
6. Agent pool
7. Workflow engine
8. Skill orchestrator routing
9. MCP server
10. NotebookLM client

### 📋 Nice to Have (Experimental)
11. TUI interface
12. Chinese LLM agents
13. CLI commands

---

## For Each Bug You Find

1. Add to BUG_SQUASHING_SESSION.md (continue from Bug #13)
2. Document: File, line, error, fix
3. Make minimal fix (match actual interface)
4. Test the fix
5. Commit with clear message
6. Move to next component

---

## Success Criteria

**After Week 1:**
- ✅ All core modules import and initialize
- ✅ Storage layer works
- ✅ Manuscript structure functional
- ✅ Basic analysis working

**After Week 2:**
- ✅ Skill generation end-to-end
- ✅ MCP server functional
- ✅ Project creation complete

**After Week 3:**
- ✅ Scene workflows working
- ✅ Model comparison functional
- ✅ Integrations tested

**After Week 4:**
- ✅ UI layers working
- ✅ Full user scenarios
- ✅ 100+ bugs documented and fixed
- ✅ System production-ready

---

## Resources

**Budget:** ~$900 credits (expires in 3 days - use them!)
**Approach:** Systematic, component-by-component
**Philosophy:** "If untested, assume broken"

**Repository:** `/Users/gch2024/writers-factory-core`
**Branch:** `claude/task-14-continued-01UMjgFnnqVSwjZjwerw3nGw`

---

## First Steps

```bash
# 1. Read the roadmap
cat COMPREHENSIVE_BUG_HUNT.md

# 2. Start with AgentPool (Phase 1, Component #3)
python3 -c "from factory.core.agent_pool import AgentPool; print('Testing AgentPool...')"

# 3. Document what you find
# 4. Fix bugs
# 5. Move to next component
```

---

**Expected Results:**

Sprint 14: 400 lines, 13 bugs = **3.25% bug rate**

Whole system: 23,088 lines × 3.25% = **~750 potential bugs**

Your mission: Find and fix as many as possible before January students arrive.

**Let's make Writers Factory bulletproof!** 🚀
