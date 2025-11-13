# Cloud Agent Progress Checklist

Use this to track the Cloud Agent's progress through all 7 tasks.

---

## 📦 Pre-Deploy

- [ ] Package uploaded to `writers-factory-core/docs/tasks/`
- [ ] Verified all 14 files present in repository
- [ ] Cloud Agent conversation started
- [ ] Initial prompt sent to Cloud Agent
- [ ] Cloud Agent confirmed they read START_HERE.md

---

## Task 1: Storage & Session Management (3-4 hours)

### Implementation
- [ ] `factory/core/storage/session.py` - Session class
- [ ] `factory/core/storage/cost_tracker.py` - CostTracker class
- [ ] `factory/core/storage/preferences.py` - Preferences management
- [ ] `factory/core/storage/history.py` - Session history
- [ ] `factory/core/storage/file_watcher.py` - File change detection
- [ ] `factory/core/storage/json_store.py` - Thread-safe JSON storage
- [ ] `factory/core/storage/models/` - Pydantic models (3 files)

### Testing
- [ ] Unit tests for Session class
- [ ] Unit tests for CostTracker
- [ ] Unit tests for crash recovery
- [ ] Integration test for auto-save cycle

### Verification
- [ ] Auto-save runs every 30s without blocking
- [ ] Cost tracking logs operations accurately
- [ ] Session recovers after simulated crash
- [ ] History shows last 20 sessions

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 2: Master CLI (Rich TUI) (4-5 hours)

### Implementation
- [ ] `factory/ui/tui.py` - Main TUI class
- [ ] `factory/ui/components/` - UI components (4 files)
- [ ] `factory/ui/stages/` - Stage views (5 files)
- [ ] `factory/ui/keyboard.py` - Keyboard handler

### Testing
- [ ] UI navigation tests
- [ ] Keyboard shortcut tests

### Verification
- [ ] `factory start` launches Rich TUI
- [ ] Status bar shows stage progress and costs
- [ ] TAB/SHIFT+TAB navigates between stages
- [ ] Keyboard shortcuts work (C, H, E, Q, etc.)
- [ ] UI matches ASCII mockups in UX spec

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 3: Knowledge Router (3-4 hours)

### Implementation
- [ ] `factory/knowledge/router.py` - KnowledgeRouter class
- [ ] `factory/knowledge/cognee_client.py` - Cognee integration
- [ ] `factory/knowledge/notebooklm_client.py` - NotebookLM integration
- [ ] `factory/knowledge/query_analyzer.py` - Query classification

### Testing
- [ ] Query routing tests
- [ ] Cognee integration tests
- [ ] NotebookLM integration tests

### Verification
- [ ] Cognee is invisible to users
- [ ] NotebookLM is opt-in during wizard
- [ ] Query routing works automatically
- [ ] Users never see "Gemini File Search" option

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 4: Workflows Module (4-5 hours)

### Implementation
- [ ] `factory/workflows/scene_generation.py` - SceneGenerationWorkflow
- [ ] `factory/workflows/scene_enhancement.py` - SceneEnhancementWorkflow
- [ ] `factory/workflows/voice_testing.py` - VoiceTestingWorkflow
- [ ] `factory/workflows/workflow_base.py` - Base workflow class

### Testing
- [ ] Scene generation tests
- [ ] Scene enhancement tests
- [ ] Voice testing tests

### Verification
- [ ] Scene generation works with knowledge context
- [ ] Enhancement works (voice, pacing, dialogue)
- [ ] Voice testing produces detailed reports
- [ ] Cost warnings appear before expensive operations

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 5: Model Comparison Tool (3-4 hours)

### Implementation
- [ ] `factory/tools/model_comparison.py` - ModelComparisonTool class
- [ ] `factory/tools/diff_viewer.py` - Visual diff component
- [ ] Tournament orchestrator successfully repurposed

### Testing
- [ ] Model comparison tests
- [ ] Diff viewer tests

### Verification
- [ ] Press 'C' in Writing stage → Comparison opens
- [ ] Side-by-side comparison shows 2-4 models
- [ ] Visual diff highlights differences
- [ ] User can select winner → Preference saved

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 6: Creation Wizard (6-8 hours)

### Implementation
- [ ] `factory/wizard/wizard.py` - Main wizard orchestrator
- [ ] `factory/wizard/phases/foundation.py` - Phase 1
- [ ] `factory/wizard/phases/character.py` - Phase 2
- [ ] `factory/wizard/phases/plot.py` - Phase 3
- [ ] `factory/wizard/phases/world.py` - Phase 4
- [ ] `factory/wizard/phases/symbolism.py` - Phase 5
- [ ] `factory/wizard/tools/find_your_voice.py` - Voice discovery tool
- [ ] `factory/wizard/output/story_bible.py` - Output generator

### Testing
- [ ] Wizard flow tests
- [ ] Phase tests
- [ ] Voice tool tests

### Verification
- [ ] `factory init` launches conversational wizard
- [ ] Wizard feels conversational, not form-like
- [ ] Marathon runner progress indicator works
- [ ] "Find Your Voice" tool generates style samples
- [ ] Output: 4,000-6,000 word story bible
- [ ] NotebookLM linking (optional) works

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## Task 7: Integration & Polish (2-3 hours)

### Documentation
- [ ] `docs/README.md` - Updated with usage guide
- [ ] `docs/ARCHITECTURE.md` - Hybrid architecture explained
- [ ] `docs/API_REFERENCE.md` - API docs for each module
- [ ] `docs/TROUBLESHOOTING.md` - Common issues & fixes

### Testing
- [ ] `factory/tests/integration/test_full_workflow.py` - End-to-end
- [ ] `factory/tests/integration/test_crash_recovery.py` - Crash scenarios
- [ ] `factory/tests/integration/test_performance.py` - Performance benchmarks

### Verification
- [ ] Full user journey works end-to-end
- [ ] All 23 success criteria met (see below)
- [ ] Documentation is complete and clear
- [ ] No blocking bugs or performance issues

### Git
- [ ] Committed with descriptive message
- [ ] Pushed to repository
- [ ] Commit hash: __________________

---

## 23 Success Criteria Checklist

### Core Functionality (5)
- [ ] 1. User can launch `factory start` and see Rich TUI with 5-stage pipeline
- [ ] 2. Status bar shows stage progress, costs, and auto-save status
- [ ] 3. User can navigate between stages with TAB/SHIFT+TAB
- [ ] 4. Auto-save runs every 30 seconds without blocking UI
- [ ] 5. Cost tracking logs all operations and warns before expensive operations

### Knowledge System (4)
- [ ] 6. User can ask questions from any stage
- [ ] 7. Questions route to Cognee (local) or NotebookLM (if configured)
- [ ] 8. Users never see "Gemini File Search" option
- [ ] 9. Cognee is invisible (users just "ask questions")

### Writing Workflows (3)
- [ ] 10. User can generate scenes with knowledge context
- [ ] 11. User can enhance existing scenes (voice, pacing, dialogue)
- [ ] 12. User can run voice tests on scenes

### Model Comparison Tool (4)
- [ ] 13. User can press 'C' in Writing stage → Model Comparison opens
- [ ] 14. Side-by-side comparison shows 2-4 model outputs
- [ ] 15. Visual diff highlights differences
- [ ] 16. User can select winner → Preference saved

### Creation Wizard (4)
- [ ] 17. User can run `factory init` → Conversational wizard starts
- [ ] 18. Wizard feels conversational, not form-like
- [ ] 19. 5 phases with progress indicator (marathon runner)
- [ ] 20. Output: 4,000-6,000 word story bible

### Session Management (3)
- [ ] 21. If system crashes, session recovers on restart
- [ ] 22. User loses < 30 seconds of work
- [ ] 23. History shows last 20 sessions

---

## Final Report

- [ ] Cloud Agent submitted final report
- [ ] All commits summarized with hashes
- [ ] Test coverage documented
- [ ] Known issues/assumptions documented
- [ ] Next steps recommended

---

## Final Verification

### Manual Testing
- [ ] Run `factory init` → Complete wizard → Generates story bible
- [ ] Run `factory start` → Navigate all 5 stages
- [ ] Generate a scene with knowledge context
- [ ] Enhance a scene (voice correction)
- [ ] Run voice test
- [ ] Open Model Comparison Tool (press 'C')
- [ ] Kill process → Restart → Verify session recovered
- [ ] Check session history shows all sessions

### Performance Testing
- [ ] Auto-save doesn't block UI
- [ ] Knowledge queries respond quickly (< 2s)
- [ ] No memory leaks in 2+ hour session
- [ ] Cost tracking accurately reflects usage

### Documentation Review
- [ ] README has clear usage instructions
- [ ] ARCHITECTURE explains hybrid system
- [ ] API_REFERENCE covers all modules
- [ ] TROUBLESHOOTING has common issues

---

## Timeline Tracking

| Task | Estimated | Started | Completed | Actual Time | Commit Hash |
|------|-----------|---------|-----------|-------------|-------------|
| Task 1: Storage | 3-4h | _____ | _____ | _____ | _______ |
| Task 2: Master CLI | 4-5h | _____ | _____ | _____ | _______ |
| Task 3: Knowledge Router | 3-4h | _____ | _____ | _____ | _______ |
| Task 4: Workflows | 4-5h | _____ | _____ | _____ | _______ |
| Task 5: Model Comparison | 3-4h | _____ | _____ | _____ | _______ |
| Task 6: Creation Wizard | 6-8h | _____ | _____ | _____ | _______ |
| Task 7: Polish | 2-3h | _____ | _____ | _____ | _______ |
| **TOTAL** | **25-33h** | _____ | _____ | _____ | - |

---

## Notes / Issues Encountered

```
[Use this space to track any issues, questions, or notable decisions the
Cloud Agent makes during implementation]




```

---

## Completion Status

**Overall Status**: ⏳ Not Started / 🏗️ In Progress / ✅ Complete

**Date Started**: _______________
**Date Completed**: _______________
**Total Time**: _______________

**Final Grade**: _____ / 23 Success Criteria Met

---

## Post-Completion Actions

- [ ] Review final code in repository
- [ ] Pull latest changes locally
- [ ] Run full test suite manually
- [ ] Test Writers Factory with real project
- [ ] Provide feedback to Cloud Agent
- [ ] Document any follow-up improvements needed
- [ ] Celebrate! 🎉

---

**Ready to track progress!** Update this checklist as the Cloud Agent completes each task.
