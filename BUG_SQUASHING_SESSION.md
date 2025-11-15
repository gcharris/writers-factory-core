# Bug Squashing Session - Sprint 14 Testing

**Date Started:** November 15, 2025  
**Mission:** Test Sprint 14 Project Setup Wizard and fix ALL bugs found

---

## Context: What We Just Built

**Sprint 14** implemented the **Project Setup Wizard** - the system that lets ANY writer create custom skills for THEIR novel (not just The Explants).

**Code Complete:**
- ✅ **Phase A (Backend):** 2,893 lines - Voice analysis, skill generation, project creation
- ✅ **Phase B (Frontend + API):** 1,750 lines - 6-step wizard UI, 4 API endpoints

**Total:** ~4,643 lines of new code across 13 files

**Branch:** `claude/task-14-continued-01UMjgFnnqVSwjZjwerw3nGw`

---

## Bugs Found & Fixed (11 total)

### ✅ Bug #1: Missing Phase A Code
**Fix:** Merged Phase A commit (3e66414) - brought in 2,893 lines

### ✅ Bug #2: Missing Playwright
**Fix:** `pip3 install playwright && python3 -m playwright install chromium`

### ✅ Bug #3: Missing Anthropic Client
**Fix:** Added `get_anthropic_client()` helper, fixed all Phase A class initializations

### ✅ Bug #4: Wrong Parameter Names
**Fix:** Changed to match Phase A interface - `example_passages`, `uploaded_docs`, etc.

### ✅ Bug #5: ProjectCreator Parameter
**Fix:** Changed `base_projects_dir` to `projects_root`

### ✅ Bug #6: VoiceProfile Invalid Parameter `dialogue_patterns`
**File:** `webapp/backend/routes/setup.py:395-406`
**Error:** `VoiceProfile.__init__() got an unexpected keyword argument 'dialogue_patterns'`
**Fix:** Removed `dialogue_patterns` parameter, added missing `genre` and `voice_consistency_notes` parameters to match actual VoiceProfile signature

### ✅ Bug #7: Wrong Method Name `generate_all_skills`
**File:** `webapp/backend/routes/setup.py:189`
**Error:** `'SkillGenerator' object has no attribute 'generate_all_skills'`
**Fix:** Changed `generate_all_skills()` to `generate_project_skills()` and fixed parameter name from `knowledge_context` to `notebooklm_context`

### ✅ Bug #8: GeneratedSkill Wrong Attribute `skill_md`
**File:** `webapp/backend/routes/setup.py:201,307`
**Error:** `'GeneratedSkill' object has no attribute 'skill_md'`
**Fix:** Changed `skill.skill_md` to `skill.skill_prompt` and fixed GeneratedSkill reconstruction to include required `voice_profile` parameter

### ✅ Bug #9: SkillRequest Missing `capability` Parameter
**File:** `webapp/backend/routes/setup.py:243`
**Error:** `SkillRequest.__init__() missing 1 required positional argument: 'capability'`
**Fix:** Added capability mapping (scene-analyzer→analyze, scene-enhancer→enhance, etc.) and included capability in SkillRequest

### ✅ Bug #10: SkillResponse Wrong Attribute `success`
**File:** `webapp/backend/routes/setup.py:262`
**Error:** `'SkillResponse' object has no attribute 'success'`
**Fix:** Changed `result.success` to `result.status != SkillStatus.SUCCESS`

### ✅ Bug #11: ProjectCreator Wrong Parameters
**File:** `webapp/backend/routes/setup.py:343-349`
**Error:** `ProjectCreator.create_project() got an unexpected keyword argument 'genre'`
**Fix:** Removed `genre` parameter, changed `knowledge_context` to `notebooklm_context`, removed `await` (method is sync not async)

---

## What Works Now (ALL 4 ENDPOINTS!)

✅ `/api/setup/analyze-voice` - Tested, works perfectly, returns VoiceProfile JSON
✅ `/api/setup/generate-skills` - Tested, generates all 6 skills with reference files
✅ `/api/setup/test-skill` - Tested, properly validates skill existence
✅ `/api/setup/create-project` - Tested, creates complete project structure

---

## Test Projects Created

✅ **test-thriller** - Thriller project with compressed prose
✅ **witty-hearts** - Romance project with bright dialogue
✅ **quiet-depths** - Literary fiction with contemplative voice

All 3 projects have:
- Complete directory structure (.claude/skills/, knowledge/, scenes/)
- 6 custom skills (scene-analyzer, scene-enhancer, character-validator, scene-writer, scene-multiplier, scaffold-generator)
- config.json and README.md
- Voice profile and reference materials

---

## Test Commands

**Test generate-skills:**
```bash
curl -X POST http://127.0.0.1:8000/api/setup/generate-skills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-thriller",
    "genre": "thriller",
    "examplePassages": ["She needed to leave. Quick. No looking back."],
    "uploadedDocs": [],
    "notebooklmUrls": []
  }'
```

**Test test-skill:**
```bash
curl -X POST http://127.0.0.1:8000/api/setup/test-skill \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "test-thriller",
    "skillType": "scene-analyzer",
    "testScene": "She left. No looking back."
  }'
```

**Test create-project:**
```bash
curl -X POST http://127.0.0.1:8000/api/setup/create-project \
  -H "Content-Type: application/json" \
  -d '{
    "name": "witty-hearts",
    "genre": "romance",
    "examplePassages": ["Emma laughed. Bright and unexpected."],
    "uploadedDocs": [],
    "notebooklmUrls": []
  }'
```

---

## How to Fix Bugs

1. Run test command
2. Check error: `tail -50 /tmp/backend_final.log`
3. Find bug in `webapp/backend/routes/setup.py`
4. Check Phase A truth in `factory/core/`
5. Fix the mismatch
6. Restart: `pkill -f simple_app.py && python3 webapp/backend/simple_app.py > /tmp/backend_final.log 2>&1 &`
7. Test again

---

## Common Bug Patterns

- Missing Anthropic client
- Parameter name mismatches  
- Type mismatches (object vs list)
- Missing imports
- Async vs sync issues

---

## Success Criteria

- ✅ All 4 endpoints work
- ✅ Can create complete projects
- ✅ Generated skills properly formatted
- ✅ Create 3 test projects (thriller, romance, literary)

---

## Resources

**Server:** http://127.0.0.1:8000  
**Logs:** `/tmp/backend_final.log`  
**Budget:** ~$900 (spend it!)

**Philosophy:** "Stop planning. Start using. Fix what breaks."
