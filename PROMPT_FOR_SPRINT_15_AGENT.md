# Prompt for Sprint 15 Implementation Agent

## Mission: Build NotebookLM-Based Beginner Mode 🎯

**Sprint:** 15 - NotebookLM Beginner Mode
**Priority:** CRITICAL - Required for January course
**Timeline:** 3 weeks
**Dependencies:** Sprint 14 ✅ Complete

---

## What You're Building

**The Problem:**
Writers Factory requires 2,500+ words of existing fiction to generate custom skills. Beginners arrive with concept only (0 words). System is currently unusable for them.

**Your Solution:**
Build a "beginner path" that extracts voice from personal writing (emails, social media, diary) uploaded to NotebookLM, generates "starter skills," then upgrades to "novel skills" at 2,500 words.

---

## Read These Files First

1. **SPRINT_15_NOTEBOOKLM_BEGINNER_MODE.md** - Complete specification
2. **docs/ARCHITECTURAL_DECISION_BEGINNER_MODE.md** - Why we're doing this
3. **SPRINT_14_PROJECT_SETUP_WIZARD.md** - What already exists

---

## Your 3-Week Plan

### **Week 1: NotebookLM Voice Extraction**

**Goal:** Extract voice from personal writing in NotebookLM

**Build:**
1. `factory/integrations/notebooklm_voice_extractor.py`
   - `extract_personal_voice()` - Get writing from notebook
   - `categorize_sources()` - Detect email vs social vs diary
   - `extract_text_by_category()` - Get text by type

2. `factory/core/dual_voice_profiles.py`
   - `StarterVoiceProfile` dataclass (lower confidence)
   - `NovelVoiceProfile` dataclass (higher confidence)

3. Tests: `tests/test_notebooklm_voice_extraction.py`

**Success:** Can extract 5,000+ words from NotebookLM and generate StarterVoiceProfile

---

### **Week 2: Starter Skills & Progress Tracking**

**Goal:** Generate skills from personal voice, track progress

**Build:**
1. `factory/core/starter_skill_generator.py`
   - `generate_starter_skills()` - Create 6 skills with caveats
   - `_add_starter_caveats()` - Add "starter mode" warnings

2. `factory/core/progress_upgrade_system.py`
   - `track_word_count()` - Monitor cumulative words
   - `perform_upgrade()` - Switch from starter to novel

3. Backend API endpoints:
   - `POST /api/setup/analyze-from-notebooklm`
   - `POST /api/setup/upgrade-to-novel-skills`

4. Tests: `tests/test_starter_skills.py`, `tests/test_progress_upgrade.py`

**Success:** Can generate starter skills and trigger upgrade at 2,500 words

---

### **Week 3: Upgrade Wizard & Polish**

**Goal:** Build UI for upgrade flow, polish UX

**Build:**
1. `webapp/frontend-v2/src/features/upgrade/UpgradeWizard.jsx`
   - Auto-open at 2,500 words
   - Show upgrade button
   - Celebrate with confetti

2. `webapp/frontend-v2/src/features/upgrade/VoiceComparisonDisplay.jsx`
   - Show starter vs novel voice
   - Highlight evolution/improvements

3. Update `webapp/frontend-v2/src/features/setup/ProjectSetupWizard.jsx`
   - Add "Do you have fiction?" fork
   - Beginner path → NotebookLM input

4. E2E tests: `tests/test_beginner_e2e.py`

**Success:** Complete beginner flow works end-to-end

---

## Key Technical Decisions

### **1. How to Extract from NotebookLM**

**Use existing NotebookLMClient:**
```python
from factory.research.notebooklm_client import NotebookLMClient

client = NotebookLMClient()
await client.query_notebook(
    notebook_url=url,
    query="Extract all writing samples by the user (emails, social posts, diary)"
)
```

**Categorization strategy:**
- Email: Look for "From:", "Subject:", formal language
- Social media: Look for hashtags, @mentions, casual tone
- Diary: Look for dates, "I felt...", personal reflection

---

### **2. Starter vs Novel Voice Profiles**

**Key difference:**
- **Starter:** confidence_level = "medium" (never "high")
- **Novel:** confidence_level can be "high"

**Both use same VoiceProfile structure:**
```python
@dataclass
class StarterVoiceProfile(VoiceProfile):
    is_starter: bool = True
    source_types: List[str]  # ["email", "social_media"]
    upgrade_threshold: int = 2500
    warnings: List[str] = [
        "Based on casual writing, not fiction",
        "Upgrade at 2,500 words for better accuracy"
    ]
```

---

### **3. Upgrade Detection**

**Trigger conditions:**
```python
if (project.is_starter_mode and
    project.total_words >= 2500 and
    not project.upgrade_prompted):
    show_upgrade_wizard()
```

**Auto-prompt on:**
- Scene save (if word count crosses threshold)
- Page load (if already past threshold)
- Manual check (user clicks progress bar)

---

### **4. Progress Tracking UI**

**Show in sidebar:**
```jsx
<ProgressCard>
  <Typography variant="h6">
    Progress to Novel Skills
  </Typography>
  <LinearProgress
    value={(words / 2500) * 100}
    variant="determinate"
  />
  <Typography variant="caption">
    {words} / 2,500 words ({2500 - words} to go)
  </Typography>
</ProgressCard>
```

---

## Common Pitfalls to Avoid

### **Pitfall 1: Expecting High-Quality Starter Skills**

**Wrong:** Make starter skills as good as novel skills
**Right:** Starter skills should be "good enough," not perfect

**Why:** Email voice ≠ fiction voice. Lower bar is intentional.

---

### **Pitfall 2: Complex Upgrade Logic**

**Wrong:** Try to intelligently merge starter + novel voice
**Right:** Replace starter entirely at 2,500 words

**Why:** Simpler = less bugs. Full replacement works fine.

---

### **Pitfall 3: Forgetting the Celebration**

**Wrong:** Upgrade happens silently in background
**Right:** Big celebration with confetti, comparison display

**Why:** Upgrade should feel like achievement, not chore.

---

## Testing Strategy

### **Unit Tests (Week 1-2)**

```bash
pytest tests/test_notebooklm_voice_extraction.py -v
pytest tests/test_starter_skills.py -v
pytest tests/test_progress_upgrade.py -v
```

**Coverage targets:**
- Voice extraction: 90%+
- Skill generation: 85%+
- Upgrade logic: 95%+

---

### **Integration Tests (Week 3)**

```bash
pytest tests/test_beginner_e2e.py -v
```

**Test flow:**
1. Mock NotebookLM with 5,000 words of "emails"
2. Extract starter voice
3. Generate starter skills
4. Simulate writing 2,500 words
5. Trigger upgrade
6. Verify novel skills generated
7. Check voice comparison accurate

---

### **User Acceptance Testing (Week 3)**

**Recruit 5 beta testers:**
- 2 complete beginners
- 2 intermediate writers
- 1 experienced writer

**Give them:**
- Access to dev environment
- Instructions: "Upload personal writing, generate skills, write 2,500 words"
- Survey after completion

**Success criteria:**
- 5/5 complete without blocking bugs
- 4/5 successfully upgrade
- 4/5 report positive experience

---

## Success Criteria

**Sprint 15 is DONE when:**

- [ ] Can extract voice from NotebookLM (5,000+ words)
- [ ] StarterVoiceProfile generates correctly
- [ ] 6 starter skills created with caveats
- [ ] Word count tracking works accurately
- [ ] Upgrade prompt triggers at 2,500 words
- [ ] Novel skills replace starter skills on upgrade
- [ ] Voice comparison shows meaningful insights
- [ ] Upgrade wizard UX is polished (confetti!)
- [ ] All tests pass (unit + integration + e2e)
- [ ] 5 beta testers complete flow successfully

---

## Integration with Existing Code

### **Sprint 14 Already Has:**

✅ `VoiceProfileExtractor` - Use this for novel voice
✅ `SkillGenerator` - Use this for novel skills
✅ `ProjectCreator` - Use this for project structure
✅ `/api/setup/analyze-voice` endpoint

**You're adding:**
- Beginner onboarding fork
- NotebookLM voice extraction
- Starter skills variant
- Progress tracking
- Upgrade wizard

**Don't break:**
- Experienced writer path (Sprint 14)
- Existing projects
- Novel skill generation

---

## Architecture Diagram

```
┌────────────────────────────────────────┐
│  USER ARRIVES (0 words)                │
└────────────┬───────────────────────────┘
             │
             ▼
┌────────────────────────────────────────┐
│  ONBOARDING FORK                       │
│  "Do you have 3-5 fiction passages?"   │
└────┬────────────────────────┬──────────┘
     │ YES                    │ NO
     │                        │
     ▼                        ▼
┌─────────────┐      ┌────────────────────┐
│ SPRINT 14   │      │ SPRINT 15          │
│ (Existing)  │      │ (You're building)  │
│             │      │                    │
│ Analyze     │      │ 1. NotebookLM      │
│ Fiction     │      │    Voice Extract   │
│ Voice       │      │                    │
│             │      │ 2. Generate        │
│ Generate    │      │    Starter Skills  │
│ Novel       │      │                    │
│ Skills      │      │ 3. Write with      │
│             │      │    Starter Skills  │
└─────────────┘      │                    │
                     │ 4. At 2,500 words: │
                     │    UPGRADE         │
                     │                    │
                     │ 5. Generate Novel  │
                     │    Skills          │
                     └────────┬───────────┘
                              │
                              ▼
                     ┌────────────────────┐
                     │  NOVEL MODE        │
                     │  (Both paths merge)│
                     └────────────────────┘
```

---

## Dependencies

**Python packages (already installed):**
- anthropic (LLM calls)
- fastapi (backend)
- playwright (NotebookLM automation)

**Frontend packages (already installed):**
- react
- @mui/material
- canvas-confetti (for celebration)

**New dependencies:** None! Everything needed is already there.

---

## Resources

**Code references:**
- Existing NotebookLM: `factory/research/notebooklm_client.py`
- Existing voice extraction: `factory/core/voice_extractor.py`
- Existing skill generation: `factory/core/skill_generator.py`
- Existing setup wizard: `webapp/frontend-v2/src/features/setup/ProjectSetupWizard.jsx`

**Documentation:**
- Sprint 15 spec: `SPRINT_15_NOTEBOOKLM_BEGINNER_MODE.md`
- Architecture decision: `docs/ARCHITECTURAL_DECISION_BEGINNER_MODE.md`
- Field guide: `docs/WRITERS_FACTORY_FIELD_GUIDE.md`

**Budget:** Unlimited - use APIs freely for testing

---

## Communication

**Daily standups (async):**
Post to GitHub Discussions:
- What you completed yesterday
- What you're working on today
- Any blockers

**End of week demos:**
- Week 1: Show voice extraction working
- Week 2: Show starter skills + progress tracking
- Week 3: Show full upgrade flow

**Final deliverable:**
- Pull request with all code
- E2E test passing
- Documentation updated
- 5 beta testers completed flow

---

## Let's Build This! 🚀

You're creating the missing piece that makes Writers Factory accessible to beginners while keeping full power for experienced writers.

**Start with Week 1: NotebookLM Voice Extraction**

First file to create: `factory/integrations/notebooklm_voice_extractor.py`

Good luck! 🎯
