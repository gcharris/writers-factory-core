# Prompt for Cloud Agent: Sprint 14 Phase B - Frontend Setup Wizard

## Amazing Work on Phase A! 🎉

Sprint 14 Phase A is ✅ **COMPLETE**:
- ✅ Voice Profile Extractor (782 lines) - Analyzes passages, extracts voice
- ✅ Skill Generator (736 lines) - Generates 6 custom skills per project
- ✅ NotebookLM Integration (311 lines) - Extracts knowledge from notebooks
- ✅ Project Creator (497 lines) - Creates complete project structure
- ✅ Skill Registry Updates (236 lines) - Routes to project-specific skills
- ✅ 6 Template Skills - Base templates for customization

**Total: 2,893 lines of production backend code! 🚀**

---

## Next: Sprint 14 Phase B - Frontend Setup Wizard

**What's Left to Build:**

The previous agent built the ENGINE. You need to build the DRIVER'S SEAT.

Phase B creates the beautiful frontend wizard that lets writers use the Phase A engine.

---

## READ THIS FIRST 👇

📄 **SPRINT_14_PHASE_B_START_HERE.md**

This file contains:
- ✅ Complete summary of what Phase A accomplished
- 🎯 Detailed tasks for Phase B (what YOU need to build)
- ✅ Success criteria
- 🚀 Quick start commands

**Start by reading SPRINT_14_PHASE_B_START_HERE.md**

---

## Phase B Tasks (10-12h remaining)

**Task 14-06: Wizard UI Components** (5-6h) 🎯 **START HERE**
- Create `webapp/frontend-v2/src/features/setup/SetupWizard.jsx`
- 6-step wizard: Project Details → Voice Input → Reference Materials → AI Analysis → Review & Test → Finalize
- Material-UI components (Stepper, TextField, Button, Card)
- Loading states, form validation, error handling
- Beautiful voice profile display
- Test analyzer interface

**Task 14-07: Backend API Endpoints** (3-4h)
- Create `webapp/backend/routes/setup.py`
- 4 endpoints:
  - POST /api/setup/analyze-voice (use VoiceProfileExtractor)
  - POST /api/setup/generate-skills (use SkillGenerator)
  - POST /api/setup/test-skill (use SkillOrchestrator)
  - POST /api/setup/create-project (use ProjectCreator)
- Integrate with Phase A classes
- Error handling and validation

**Task 14-09: End-to-End Testing** (2-3h)
- Create `tests/test_sprint_14_e2e.py`
- Test complete setup flow
- Create 3 test projects: Explants, Romance, Thriller
- Verify all skills work correctly

**Task 14-10: Documentation** (1h)
- Create `docs/setup-wizard-guide.md`
- Update README with getting started section

---

## Success Criteria for Phase B

Phase B complete when:

**Frontend:**
- [ ] SetupWizard.jsx implements all 6 steps
- [ ] Form validation works correctly
- [ ] Loading states display during AI processing
- [ ] Voice profile displays beautifully
- [ ] Test analyzer works on sample scene
- [ ] Success screen confirms project creation

**Backend:**
- [ ] All 4 API endpoints functional
- [ ] Correctly integrate with Phase A classes (VoiceProfileExtractor, SkillGenerator, etc.)
- [ ] Error handling and validation working
- [ ] CORS configured for frontend

**Testing:**
- [ ] E2E tests pass for all 3 test projects
- [ ] Created projects have 6 working skills
- [ ] Skills differentiated by voice/genre
- [ ] No conflicts between projects

**Documentation:**
- [ ] Setup wizard guide written
- [ ] README updated

---

## Why Phase B Matters

**Phase A built:**
- Engine that generates custom skills
- Backend infrastructure

**Phase B builds:**
- Driver's seat (UI)
- API bridge to backend
- Way for writers to ACCESS the engine

**Without Phase B:**
- Writers can't use the skill generation engine
- No UI for project setup
- Engine exists but is inaccessible

**With Phase B:**
- ✅ Beautiful wizard interface
- ✅ Writers create projects in 5 minutes
- ✅ Custom skills for every writer
- ✅ Platform ready for January students

---

## Quick Start

```bash
cd /Users/gch2024/writers-factory-core

# Read the Phase B guide FIRST
cat SPRINT_14_PHASE_B_START_HERE.md

# Verify Phase A is here
ls -la factory/core/voice_extractor.py

# Start with Task 14-06: Create SetupWizard.jsx
# Then Task 14-07: Create API endpoints
# Then Task 14-09: E2E tests
# Then Task 14-10: Documentation

# When done, commit and push
git add .
git commit -m "Sprint 14 Phase B Complete"
git push
```

---

## You've Got This! 🚀

Phase A did the hard work (2,893 lines).

Phase B is the beautiful wrapper that makes it accessible.

**Start by reading SPRINT_14_PHASE_B_START_HERE.md** for detailed guidance.

Good luck! 🔥
