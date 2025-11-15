# Architectural Decision: Beginner Mode for Writers Factory

**Date:** November 15, 2025
**Status:** Proposed
**Decision Maker:** G.C. Harris

---

## Problem Statement

**Writers Factory has a critical onboarding gap:**

### Current System (Sprint 14):
- Requires 3-5 example passages (2,500-5,000 words minimum)
- Analyzes existing voice to generate custom skills
- Designed for experienced writers with established style

### Reality for New Writers:
- January course students arrive with **concept only**, not existing text
- Beginners don't have voice profile yet
- Need AI assistance from **Day 1**, but can't provide examples until **Day 3-4**

**Result:** Writers Factory is **unusable** for beginners in its current form.

---

## Comparison Analysis

### Notion Writers Desktop (Simple System)
**Strengths for beginners:**
- ✅ No prerequisites - start immediately
- ✅ Clear checklist guides process
- ✅ Brainstorming → Planning → Writing → Publishing
- ✅ Accountability through tracking

**What it lacks:**
- ❌ No AI assistance
- ❌ No voice analysis
- ❌ No quality scoring
- ❌ No automated consistency checking

### Writers Factory (Our System)
**Strengths for experienced writers:**
- ✅ Custom skills tuned to YOUR voice
- ✅ AI-powered quality analysis
- ✅ Multi-model comparison
- ✅ Automated plot/character tracking

**What it requires:**
- ❌ Existing writing samples (2,500+ words)
- ❌ Established voice to analyze
- ❌ Technical comfort

---

## Proposed Solution: Hybrid "Training Wheels" Mode

### Two-Path Onboarding

```
NEW USER ARRIVES
       │
       ▼
┌──────────────────┐
│ Do you have      │
│ 3-5 example      │◄─── CRITICAL FORK
│ passages?        │
└──────┬───────────┘
       │
   ┌───┴────┐
   │        │
   ▼        ▼
 YES       NO
   │        │
   │        ▼
   │  ┌────────────────────┐
   │  │ BEGINNER PATH      │
   │  │                    │
   │  │ - Notion-style     │
   │  │   checklists       │
   │  │ - Generic AI       │
   │  │   prompts          │
   │  │ - Progressive      │
   │  │   voice analysis   │
   │  │                    │
   │  │ Upgrade when:      │
   │  │ ✓ 2,500+ words     │
   │  └────────────────────┘
   │
   ▼
┌────────────────────┐
│ EXPERIENCED PATH   │
│                    │
│ - Sprint 14 Wizard │
│ - Voice analysis   │
│ - Custom skills    │
│ - Full power       │
└────────────────────┘
```

---

## Beginner Mode Features

### Phase I: Brainstorming (Days 1-2)

**Notion-inspired checklist:**
- [ ] Define genre and target audience
- [ ] Create high concept (1 sentence)
- [ ] Outline protagonist and antagonist
- [ ] List 5 key plot events
- [ ] Identify 3 core themes

**AI assistance (generic, not voice-specific):**
- Brainstorming template generator
- Character questionnaire
- Plot structure suggestions (3-act, hero's journey, etc.)

**What's different from full mode:**
- Uses **generic prompts** (not custom skills)
- No voice analysis yet
- Simpler, guided workflow

---

### Phase II: Planning (Days 2-3)

**Checklist:**
- [ ] Create chapter outline (12-20 chapters)
- [ ] Character arc for protagonist
- [ ] Subplot identification
- [ ] World building (if fantasy/sci-fi)

**AI assistance:**
- Generic scaffold generator (not tuned to voice)
- Plot consistency checker (basic)
- Character arc template

**Progress tracking:**
- Word count: 0 → 2,500 target
- **Upgrade prompt appears at 2,500 words:**
  > "🎉 You've written 2,500 words! Ready to unlock custom skills?
  > Generate your voice profile now to get AI tools tuned to YOUR style."

---

### Phase III: Writing (Days 3-7)

**Checklist:**
- [ ] Write first draft (one chapter/day)
- [ ] Daily word count: 500-2000 words
- [ ] Run basic scene analysis
- [ ] Track consistency issues

**AI assistance:**
- Generic scene generator
- Basic enhancement (not voice-preserving yet)
- Simple pacing analysis

**Upgrade path:**
Once 2,500+ words written:
1. Run voice analysis on accumulated text
2. Generate 6 custom skills
3. **SWITCH TO FULL MODE**
4. Re-analyze existing scenes with custom analyzer
5. Continue with personalized tools

---

## Technical Implementation

### New Components Needed

1. **Onboarding Router** (`factory/core/onboarding_router.py`)
   ```python
   class OnboardingRouter:
       def determine_path(self, user_input):
           if has_example_passages():
               return "experienced_path"
           else:
               return "beginner_path"
   ```

2. **Beginner Checklist System** (`factory/beginner/checklist_manager.py`)
   - Implement Notion-style phase tracking
   - Store checklist state in session
   - Show progress dashboard

3. **Generic Skills** (`factory/knowledge/generic/`)
   - Pre-built skills not tuned to any voice
   - Broad templates (thriller, romance, literary)
   - Used until custom skills available

4. **Progressive Analysis** (`factory/core/progressive_analyzer.py`)
   - Monitor word count
   - Trigger upgrade prompt at 2,500 words
   - Extract voice from accumulated text
   - Generate custom skills mid-project

5. **Upgrade Wizard** (`webapp/frontend-v2/src/features/upgrade/UpgradeWizard.jsx`)
   - Shows when user hits 2,500 words
   - "Analyze my writing" button
   - Runs Sprint 14 voice analysis on existing draft
   - Switches user to full mode

---

## Benefits

### For Beginners:
✅ Start immediately (no prerequisites)
✅ Guided process (like Notion Desktop)
✅ AI assistance from Day 1 (generic prompts)
✅ Natural progression (upgrade when ready)
✅ Lower barrier to entry

### For Experienced Writers:
✅ Skip beginner mode entirely
✅ Go straight to Sprint 14 Wizard
✅ Full power immediately
✅ No changes to existing workflow

### For January Course:
✅ Students can start Day 1
✅ Use generic tools Days 1-3
✅ Upgrade to custom skills Days 3-4
✅ Finish with personalized AI tools

---

## Risks & Mitigation

### Risk #1: Generic Skills Feel Generic
**Mitigation:** Set expectations clearly
- "These are starter tools. Upgrade for personalized skills!"
- Show preview of what custom skills do
- Make upgrade feel like unlock/achievement

### Risk #2: Two Code Paths to Maintain
**Mitigation:** Share as much code as possible
- Beginner uses same backend (FastAPI)
- Same manuscript structure
- Different UI flow, same core engine

### Risk #3: Users Never Upgrade
**Mitigation:** Make upgrade compelling
- Show score comparison (generic vs custom)
- Gamify: "Unlock advanced features"
- Auto-prompt at 2,500 words (not optional to ignore)

---

## Implementation Priority

### Sprint 15: Beginner Mode Foundation (2 weeks)
**Phase A: Backend Infrastructure**
- Onboarding router
- Generic skill templates
- Progressive analyzer
- Word count monitoring

**Phase B: Frontend Flow**
- Beginner onboarding UI
- Checklist dashboard (Notion-style)
- Upgrade wizard
- Progress tracking

### Sprint 16: Polish & Integration (1 week)
- Test with non-technical users
- Refine checklist content
- Improve upgrade UX
- Document beginner workflow

---

## Success Criteria

**Beginner can:**
- [ ] Start using Writers Factory with NO existing text
- [ ] Follow checklist from concept → draft
- [ ] Use generic AI tools from Day 1
- [ ] Upgrade to custom skills at 2,500 words
- [ ] Complete 10,000-word novella in 1 week

**Experienced writer can:**
- [ ] Skip beginner mode entirely
- [ ] Use Sprint 14 Wizard immediately
- [ ] Never see beginner UI

---

## Decision

**Recommendation:** **IMPLEMENT BEGINNER MODE**

**Rationale:**
1. **Writers Factory is currently unusable for 50%+ of potential users** (beginners)
2. **January course needs this** - students won't have examples on Day 1
3. **Notion Desktop proves the model works** - checklists + structure = results
4. **Best of both worlds** - Combine Notion's accessibility with our AI power
5. **Low risk** - Beginner path doesn't break existing experienced path

**Timeline:**
- Sprint 15-16 (3 weeks)
- Ready before January course
- Tested with 5-10 beta users

---

## Open Questions

1. **Should beginner mode be separate app or integrated?**
   - Proposal: Integrated (same codebase, different UI flow)

2. **What triggers automatic upgrade?**
   - Proposal: 2,500 words + user clicks "Analyze my voice"

3. **Can users downgrade back to beginner?**
   - Proposal: No - once custom skills generated, that's the path

4. **Should we charge differently for beginner vs full?**
   - Proposal: Same price, beginner just uses fewer API calls

---

## Next Steps

1. **Validate with user research** - Interview 5 beginner writers
2. **Prototype beginner checklist** - Build Phase I in React
3. **Create generic skill templates** - Start with 3 genres
4. **Design upgrade wizard** - Make it feel like achievement
5. **Update onboarding** - Add "Do you have examples?" fork

---

**Status:** Awaiting approval from G.C. Harris
