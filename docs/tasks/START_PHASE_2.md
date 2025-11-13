# START HERE: Phase 2 Implementation

**Repository**: `writers-factory-core`
**Your Access**: Full read/write/push permissions
**Work Mode**: Autonomous (no approval needed between tasks)

---

## Quick Context

You successfully completed **Phase 1** and built an excellent tournament-based multi-model comparison system (100% of tasks completed, 19/19 tests passing).

Now we're building **Phase 2**: A stage-based workflow interface on top of your existing foundation.

---

## What You Built (Phase 1) - KEEP THIS

✅ Core engine (workflow_engine.py, agent_pool.py) - Excellent, reusable
✅ 16 LLM agent integrations - All configured and ready
✅ Tournament system (multi_model_generation/) - We'll repurpose this
✅ SQLite analytics database - Keep for metrics
✅ Knowledge router - We'll enhance this
✅ Documentation - Comprehensive

**Result**: Solid foundation with 10,122 lines of production code

---

## What We're Building (Phase 2) - NEW FEATURES

**Vision**: Transform the tournament system into a daily writing interface where users work through stages:

```
Creation → Writing → Enhancing → Analyzing → Scoring
```

**Key Changes**:
1. **Full-screen Rich TUI** (not basic CLI) - Status bar, keyboard navigation
2. **File-based sessions** with auto-save every 30s (+ SQLite for analytics)
3. **Creation Wizard** - 5 phases, Save the Cat! 15 beats, 4,000-6,000 word output
4. **Scene workflows** - Generation, enhancement, voice testing
5. **Model Comparison Tool** - Repurpose your tournament as one tool within Writing stage

---

## Your Instructions

**Read**: `docs/tasks/PHASE_2_INSTRUCTIONS.md` (17,000+ words, complete specification)

This document contains:
- 7 sequential tasks with exact code examples
- Success criteria (23 checkpoints)
- Timeline (44-60 hours, ~2 weeks)
- Commit message templates
- Zero ambiguity

---

## Work Protocol

1. **Read** `PHASE_2_INSTRUCTIONS.md` completely
2. **Work through Tasks 1-7 sequentially**:
   - Task 1: Session Storage (6-8h) ← START HERE
   - Task 2: Rich TUI (8-10h)
   - Task 3: Knowledge Router (4-6h)
   - Task 4: Scene Workflows (6-8h)
   - Task 5: Model Comparison Tool (4-6h)
   - Task 6: Creation Wizard (12-16h)
   - Task 7: Integration & Polish (4-6h)
3. **For each task**:
   - Implement functionality
   - Write tests
   - Commit with template message
   - Push to repository
   - **Continue immediately to next task** (no approval needed)
4. **When complete**: Create final report summarizing all changes

---

## Success Criteria (23 Checkpoints)

All must be met before Phase 2 is complete:

### Core Functionality (5)
1. Rich TUI launches with 5-stage pipeline
2. Status bar shows progress/costs/auto-save
3. TAB/SHIFT+TAB navigates stages
4. Auto-save every 30s (non-blocking)
5. Cost warnings before expensive operations

### Knowledge System (4)
6. Ask questions from any stage
7. Routes to Cognee/NotebookLM intelligently
8. Gemini File Search not exposed to users
9. Cognee invisible to users

### Writing Workflows (3)
10. Generate scenes with knowledge context
11. Enhance scenes (voice/pacing/dialogue)
12. Voice testing reports

### Model Comparison Tool (4)
13. Press 'C' → Comparison opens
14. Side-by-side 2-4 models
15. Visual diff highlighting
16. User selects winner → Preference saved

### Creation Wizard (4)
17. `factory init` → Wizard starts
18. Conversational (not form-like)
19. 5 phases with marathon runner progress
20. Output: 4,000-6,000 word story bible

### Session Management (3)
21. Crash recovery on restart
22. Lose < 30s of work
23. History shows last 20 sessions

---

## Important Reminders

✅ **Keep existing code**: Don't delete Phase 1 work (tournament, agents, workflow engine)
✅ **Repurpose, don't rebuild**: Tournament becomes Model Comparison Tool
✅ **Build on foundation**: Use your excellent workflow engine and agent pool
✅ **Autonomous work**: Don't wait for approval between tasks

---

## Ready?

Start by reading `docs/tasks/PHASE_2_INSTRUCTIONS.md` completely, then begin with **Task 1: Session Storage**.

When all 7 tasks are complete and all 23 checkpoints verified, create your final report.

**Good luck!** 🚀
