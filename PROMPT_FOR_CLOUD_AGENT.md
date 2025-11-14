# Prompt for Cloud Agent: Sprint 14 CRITICAL Implementation

## Sprint 12 Complete BUT Missing Critical Piece! 🚨

Sprint 12 Phase A works perfectly:
- ✅ All 6 Explants Claude Skills accessible via MCP Bridge
- ✅ Skill Orchestrator routing intelligently
- ✅ Native Scene Analyzer working
- ✅ API endpoints functional
- ✅ Craft Panel UI ready
- ✅ 3,000+ lines of code, all tests passing!

**HOWEVER:** Skills are hardcoded for The Explants project only. New writers cannot use the system.

---

## CRITICAL: Sprint 14 - Project Setup Wizard (DO THIS FIRST!)

**BLOCKING ISSUE:**
User feedback: "This is not a nice to have add-on. This is a crucial component of setting up the project."

Sprint 12 only works for G.C. Harris + The Explants. January students cannot use it.

**THE FIX: Project Setup Wizard**

Every writer needs custom skills for THEIR voice, not Explants voice.

---

## Sprint 14 Before Sprint 13

Originally planned Sprint 13 (Novel Intelligence), but Sprint 14 is BLOCKING:

**Sprint 14:** Project Setup Wizard - CRITICAL, DO NOW
**Sprint 13:** Novel Intelligence - Do after Sprint 14

---

## Sprint 14: What to Build

**THE CRITICAL FOUNDATION**

Please read and implement:
📄 **SPRINT_14_PROJECT_SETUP_WIZARD.md** (2,580 lines)

This builds the Project Setup Wizard that lets EVERY writer create custom skills.

### Phase A: Backend - Skill Generation Engine (15-18h)

**Task 14-01: Voice Profile Extractor (4-5h)**
- Analyze 3-5 example passages using LLM
- Extract: sentence structure, vocabulary, POV style, metaphor domains
- Identify anti-patterns from style guide
- Derive quality criteria from genre + voice

**Task 14-02: Skill Generator (6-7h)**
- Generate 6 custom skills per project
- Each skill gets custom SKILL.md with project-specific prompts
- Create references/ directory: voice-profile.md, anti-patterns.md, quality-criteria.md
- Skills: scene-analyzer-[project], scene-enhancer-[project], etc.

**Task 14-03: NotebookLM Integration (3-4h)**
- Extract knowledge from user's NotebookLM notebooks
- Query for: characters, world, plot, voice, themes
- Use in voice analysis and skill generation

**Task 14-04: Project Structure Creator (2-3h)**
- Create projects/[project-name]/ directory structure
- Save all 6 skills to .claude/skills/
- Create knowledge/ base with project-specific content
- Generate config.json and README.md

**Task 14-05: Skill Registry Updates (2-3h)**
- Update Skill Orchestrator to support project_id routing
- Route skill calls to correct project-specific skill
- Fallback to global skills if no project_id

### Phase B: Frontend - Setup Wizard UI (10-12h)

**Task 14-06: Wizard UI Components (5-6h)**
- 6-step wizard with progress indicator
- Step 1: Project details (name, genre, goals)
- Step 2: Voice input (paste passages, NotebookLM links, upload docs)
- Step 3: Reference materials (style guide, character sheets)
- Step 4: AI Analysis (show extracted voice profile)
- Step 5: Review & Test (show generated skills, test analyzer)
- Step 6: Finalize (create project)

**Task 14-07: Backend API Endpoints (3-4h)**
- POST /api/setup/analyze-voice
- POST /api/setup/generate-skills
- POST /api/setup/test-skill
- POST /api/setup/create-project

**Task 14-08: Template Skills (2h)**
- Create 6 base template SKILL.md files
- LLM customizes templates for each project

### Testing & Docs (3-5h)

**Task 14-09: End-to-End Testing (2-3h)**
- Create The Explants project via wizard (migration test)
- Create Romance project via wizard (different voice)
- Create Thriller project via wizard (minimal inputs)
- Verify all skills work correctly

**Task 14-10: User Documentation (1-2h)**
- Setup wizard guide
- Project structure documentation

---

## Success Criteria

Sprint 14 complete when:

**Phase A:**
- [ ] Voice Profile Extractor analyzes passages and extracts characteristics
- [ ] Skill Generator creates 6 custom skills with project-specific SKILL.md
- [ ] NotebookLM integration extracts knowledge
- [ ] Project Creator builds correct directory structure
- [ ] Skill Orchestrator routes to project-specific skills

**Phase B:**
- [ ] 6-step wizard UI complete and intuitive
- [ ] API endpoints functional
- [ ] Template skills created

**Testing:**
- [ ] Created 3+ test projects (Explants, Romance, Thriller)
- [ ] All projects have 6 working skills
- [ ] Skills correctly differentiated by voice/genre
- [ ] No conflicts between project skills

**Final Validation:**
- [ ] January students can use wizard to set up their novels
- [ ] Platform supports unlimited concurrent projects
- [ ] Every writer gets skills tailored to THEIR voice

---

## Why This Is CRITICAL

**Without Sprint 14:**
- ❌ System only works for The Explants
- ❌ Students cannot use platform in January
- ❌ No multi-project support
- ❌ Platform cannot scale

**With Sprint 14:**
- ✅ EVERY writer can set up novel with custom skills
- ✅ Students ready for January course
- ✅ Unlimited concurrent projects
- ✅ Foundation for platform scale
- ✅ Skills match each writer's unique voice

**This transforms Writers Factory from single-user tool to PLATFORM.**

---

## After Sprint 14: Then Sprint 13

Once Sprint 14 complete, Sprint 13 (Novel Intelligence) can use project-specific skills:
- Analyze ANY novel with that novel's custom skills
- Generate strategic plans using project-specific criteria
- Works for romance, thriller, literary fiction, etc.

---

## Start Here

Begin with Task 14-01 (Voice Profile Extractor).

Everything you need is in SPRINT_14_PROJECT_SETUP_WIZARD.md

**This is THE critical foundation. Build it NOW!** 🚀

Good luck! 🔥🔥🔥
