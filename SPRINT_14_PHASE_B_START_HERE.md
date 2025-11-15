# Sprint 14 Phase B: Frontend Setup Wizard - START HERE

**Date:** November 15, 2025
**Status:** Phase A ✅ COMPLETE | Phase B ⏳ READY TO START
**Branch:** `claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs`
**Last Commit:** `3e66414` - Sprint 14 Phase A Complete

---

## ✅ Phase A Complete (Backend)

The previous agent successfully built the entire backend skill generation engine:

### What's Already Built (2,893 lines):

**Task 14-01: Voice Profile Extractor** ✅
- File: `factory/core/voice_extractor.py` (782 lines)
- Analyzes 3-5 example passages using Claude Sonnet 4.5
- Extracts voice characteristics, sentence structure, vocabulary, POV style
- Identifies metaphor domains and anti-patterns
- Derives quality criteria from genre + voice

**Task 14-02: Skill Generator** ✅
- File: `factory/core/skill_generator.py` (736 lines)
- Generates 6 custom skills per project:
  - `scene-analyzer-[project]`
  - `scene-enhancer-[project]`
  - `character-validator-[project]`
  - `scene-writer-[project]`
  - `scene-multiplier-[project]`
  - `scaffold-generator-[project]`
- Each skill gets custom SKILL.md with project-specific prompts
- Creates references/ directory with voice-profile.md, anti-patterns.md, etc.

**Task 14-03: NotebookLM Integration** ✅
- File: `factory/integrations/notebooklm_setup.py` (311 lines)
- Extracts knowledge from NotebookLM notebooks
- 5 predefined queries: characters, world, plot, voice, themes
- Consolidates into knowledge context string

**Task 14-04: Project Structure Creator** ✅
- File: `factory/core/project_creator.py` (497 lines)
- Creates complete project directory:
  ```
  projects/[project-name]/
  ├─ .claude/skills/ (6 custom skills)
  ├─ knowledge/craft/ (project-specific knowledge)
  ├─ scenes/
  ├─ config.json
  └─ README.md
  ```

**Task 14-05: Skill Registry Updates** ✅
- File: `factory/core/skill_orchestrator.py` (+236 lines)
- Added `project_id` parameter to `execute_skill()`
- Routes skill calls to correct project-specific skill
- Falls back to global skills if no project_id

**Task 14-08: Template Skills** ✅
- 6 template SKILL.md files in `factory/knowledge/templates/`:
  - scene-analyzer-template.md
  - scene-enhancer-template.md
  - character-validator-template.md
  - scene-writer-template.md
  - scene-multiplier-template.md
  - scaffold-generator-template.md

---

## ⏳ Phase B: What You Need to Build NOW

### Your Mission:

Build the **Frontend Setup Wizard** that lets writers create custom skills through a beautiful 6-step UI.

---

### Task 14-06: Wizard UI Components (5-6h) 🎯 START HERE

**File to Create:** `webapp/frontend-v2/src/features/setup/SetupWizard.jsx`

**What to Build:**

A multi-step wizard interface with 6 steps:

**Step 1: Project Details**
- Project name input
- Genre dropdown (literary, thriller, romance, sci-fi, fantasy, mystery, other)
- Project goals textarea

**Step 2: Voice Input**
- Paste 3-5 example passages (500-1000 words each)
- Add passage button (tracks count: "Add Passage (3/5)")
- NotebookLM URL input field (optional)
- Upload documents button (optional)

**Step 3: Reference Materials**
- File upload for style guides, character sheets, world bible
- List of uploaded files with delete option
- Style guide / Anti-patterns textarea

**Step 4: AI Analysis**
- Auto-triggers when step loads
- Shows loading spinner: "Analyzing your voice... (1-2 minutes)"
- Displays extracted voice profile:
  - Voice name (e.g., "Mickey Bardot Enhanced")
  - Primary characteristics (bullet list)
  - Sentence structure (length, compression level)
  - POV style (depth, consciousness mode %)
  - Metaphor domains (cards showing domain name, %, keywords)

**Step 5: Review & Test**
- Auto-generates 6 skills when step loads
- Shows loading: "Generating your 6 custom skills... (2-3 minutes)"
- Displays checklist of generated skills
- Test section:
  - Paste test scene textarea
  - "Test Analyzer" button
  - Results card showing score, quality tier, category scores

**Step 6: Finalize**
- Summary of project
- "Create Project" button
- Success message with project path
- Link to project dashboard

**UI Components Needed:**
- Material-UI Stepper for progress
- TextField, Select, Button components
- File upload with drag-and-drop
- Loading spinners (CircularProgress)
- Cards for displaying voice profile
- Responsive layout

**Key Features:**
- Back/Next navigation
- Form validation (can't proceed without required fields)
- Error handling and display
- Responsive design
- Professional styling

**Reference Existing UI:**
Look at `webapp/frontend-v2/src/features/craft/CraftPanel.jsx` for styling patterns.

---

### Task 14-07: Backend API Endpoints (3-4h)

**File to Create:** `webapp/backend/routes/setup.py`

**Endpoints to Build:**

```python
@router.post("/api/setup/analyze-voice")
async def analyze_voice(request: AnalyzeVoiceRequest):
    """
    Analyzes voice from example passages.

    Request:
    {
      "examplePassages": ["passage1", "passage2", ...],
      "uploadedDocs": [{"filename": "...", "content": "..."}],
      "notebooklmUrls": ["url1", "url2"],
      "styleGuide": "...",
      "genre": "literary"
    }

    Returns:
    {
      "voiceProfile": {
        "voiceName": "...",
        "primaryCharacteristics": [...],
        "sentenceStructure": {...},
        "povStyle": {...},
        "metaphorDomains": {...}
      }
    }
    """
    # Use factory/core/voice_extractor.py
    pass


@router.post("/api/setup/generate-skills")
async def generate_skills(request: GenerateSkillsRequest):
    """
    Generates 6 custom skills for project.

    Request:
    {
      "name": "project-name",
      "genre": "literary",
      "examplePassages": [...],
      "uploadedDocs": [...],
      "notebooklmUrls": [...],
      "voiceProfile": {...}  # From analyze-voice
    }

    Returns:
    {
      "skills": {
        "scene-analyzer": {...},
        "scene-enhancer": {...},
        ...
      }
    }
    """
    # Use factory/core/skill_generator.py
    pass


@router.post("/api/setup/test-skill")
async def test_skill(request: TestSkillRequest):
    """
    Tests generated skill on sample scene.

    Request:
    {
      "projectId": "my-novel",
      "skillType": "scene-analyzer",
      "testScene": "scene content..."
    }

    Returns: Scene analysis results
    """
    # Use factory/core/skill_orchestrator.py
    pass


@router.post("/api/setup/create-project")
async def create_project(request: CreateProjectRequest):
    """
    Finalizes and creates project structure.

    Request:
    {
      "name": "my-novel",
      "genre": "literary",
      "examplePassages": [...],
      "uploadedDocs": [...],
      "notebooklmUrls": [...],
      "voiceProfile": {...},
      "generatedSkills": {...}
    }

    Returns:
    {
      "projectId": "my-novel",
      "projectPath": "/path/to/projects/my-novel",
      "skills": [...]
    }
    """
    # Use factory/core/project_creator.py
    pass
```

**Integration Points:**
- Import and use Phase A classes:
  ```python
  from factory.core.voice_extractor import VoiceProfileExtractor
  from factory.core.skill_generator import SkillGenerator
  from factory.core.project_creator import ProjectCreator
  from factory.integrations.notebooklm_setup import NotebookLMSetupIntegration
  from factory.core.skill_orchestrator import SkillOrchestrator
  ```

**Register Routes:**
Add to `webapp/backend/simple_app.py`:
```python
from routes import setup
app.include_router(setup.router)
```

---

### Task 14-09: End-to-End Testing (2-3h)

**Create Test File:** `tests/test_sprint_14_e2e.py`

**Test Cases:**

```python
def test_complete_setup_flow():
    """
    Test complete wizard flow from start to finish.

    Steps:
    1. POST /api/setup/analyze-voice with example passages
    2. Verify voice profile returned
    3. POST /api/setup/generate-skills with voice profile
    4. Verify 6 skills generated
    5. POST /api/setup/test-skill with sample scene
    6. Verify analysis results
    7. POST /api/setup/create-project
    8. Verify project directory created with all files
    """
    pass


def test_explants_migration():
    """
    Create The Explants project via wizard.

    Use actual Explants scenes as example passages.
    Verify generated skills match original hardcoded skills.
    """
    pass


def test_romance_project():
    """
    Create romance novel project.

    Different voice, different genre.
    Verify skills customized for romance conventions.
    """
    pass


def test_thriller_project():
    """
    Create thriller project with minimal inputs.

    No NotebookLM, no uploads.
    Verify wizard handles sparse data gracefully.
    """
    pass
```

**Run Tests:**
```bash
cd /Users/gch2024/writers-factory-core
pytest tests/test_sprint_14_e2e.py -v
```

---

### Task 14-10: Documentation (1h)

**File to Create:** `docs/setup-wizard-guide.md`

**Content:**
- Step-by-step walkthrough of setup wizard
- Screenshots (if possible)
- Best practices for voice input
- Tips for NotebookLM integration
- Troubleshooting common issues

**File to Update:** `README.md`

Add section:
```markdown
## Getting Started: Project Setup Wizard

New to Writers Factory? Start by creating your project:

1. Launch Writers Factory
2. Click "Create New Project"
3. Follow the 6-step wizard:
   - Enter project details
   - Paste 3-5 example scenes (your voice samples)
   - Upload reference materials (optional)
   - Review AI-extracted voice profile
   - Test your custom analyzer
   - Create project!

You'll get 6 AI skills custom-built for YOUR voice!

[Read the complete Setup Wizard Guide](docs/setup-wizard-guide.md)
```

---

## Success Criteria

Phase B complete when:

**Frontend:**
- [ ] 6-step wizard UI works smoothly
- [ ] All form inputs validate correctly
- [ ] Loading states display during AI processing
- [ ] Voice profile displays beautifully
- [ ] Test analyzer works on sample scene
- [ ] Success screen shows project creation

**Backend:**
- [ ] All 4 API endpoints functional
- [ ] Correctly integrate with Phase A classes
- [ ] Error handling and validation
- [ ] CORS configured for frontend

**Testing:**
- [ ] Created 3 test projects successfully:
  - [ ] The Explants (migration test)
  - [ ] Romance novel (different voice)
  - [ ] Thriller (minimal inputs)
- [ ] All projects have 6 working skills
- [ ] Skills correctly differentiated by voice/genre
- [ ] No conflicts between project skills

**Documentation:**
- [ ] Setup wizard guide complete
- [ ] README updated with getting started section

---

## Quick Start Commands

```bash
# Navigate to repo
cd /Users/gch2024/writers-factory-core

# Verify Phase A is here
ls -la factory/core/voice_extractor.py
ls -la factory/core/skill_generator.py
ls -la factory/core/project_creator.py

# Start building Phase B
# 1. Create SetupWizard.jsx
# 2. Create setup.py routes
# 3. Test end-to-end

# Run tests
pytest tests/test_sprint_14_e2e.py -v

# Commit when done
git add .
git commit -m "Sprint 14 Phase B: Frontend Setup Wizard Complete"
git push origin claude/test-writers-factory-access-011CV5neQMuESAczEChXJbfs
```

---

## Why This Matters

**Phase A** built the engine.
**Phase B** builds the driver's seat.

Without Phase B:
- Writers can't access the skill generation engine
- No UI for project setup
- January students can't use the platform

With Phase B:
- ✅ Beautiful wizard interface
- ✅ Writers create projects in 5 minutes
- ✅ Custom skills for every writer
- ✅ Platform ready for students

---

## Start Here: Task 14-06

Begin with the wizard UI. Everything else builds on it.

**First File to Create:**
`webapp/frontend-v2/src/features/setup/SetupWizard.jsx`

Reference the spec in `SPRINT_14_PROJECT_SETUP_WIZARD.md` for detailed component examples.

You've got this! Phase A did the hard work. Phase B is the beautiful wrapper that makes it accessible to writers. 🚀

Good luck! 🔥
