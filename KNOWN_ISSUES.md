# Known Issues & Future Improvements

**Last Updated:** November 14, 2025

---

## 🔴 Priority Issues

### Issue #1: CRITICAL - Missing Project Setup Wizard & Skill Generation System

**Status:** CORE FUNCTIONALITY MISSING from Sprint 12
**Priority:** BLOCKING - Cannot proceed to student testing or platform launch
**Discovered:** Sprint 12 completion review
**User Clarification:** "This is not a nice to have add-on. This is a crucial component of setting up the project."

**Problem:**
Sprint 12 implemented skills as global/hardcoded entities:
- Hardcoded: `explants-scene-analyzer-scorer`
- Knowledge base is Explants-specific
- No project setup wizard
- No mechanism to GENERATE project-specific skills
- Skills lack project-specific SKILL.md files and reference materials

**What's Actually Required (User's Vision):**

At the setup stage of each novel, the system must:

1. **Collect Project Inputs:**
   - NotebookLM links (for knowledge extraction)
   - Uploaded documents (style guides, character sheets, world bible, previous drafts)
   - Example passages (voice samples)
   - Writer's goals and preferences

2. **GENERATE Custom Skills for This Project:**
   - Create `scene-analyzer-[project-name]` with project-specific:
     * Voice profile (built from examples/NotebookLM analysis)
     * Reference materials (SKILL.md + references/ directory)
     * Quality criteria (genre-specific, writer-specific)
     * Anti-patterns (from style guide)
     * Metaphor domains (project-specific)

   - Create `scene-enhancer-[project-name]` with:
     * Same voice profile
     * Fix patterns specific to this voice
     * Project-specific success criteria

   - Create all 6 skill types as project-specific instances

3. **Store Project-Specific Knowledge:**
   - Each project has its own knowledge base
   - References stored in project structure
   - Skills reference project knowledge, not global knowledge

**Why This Is CORE, Not Enhancement:**
- Writers can't use the system without project-specific skills
- January students need this to set up their novels
- Platform requires this to scale beyond The Explants
- This was the intended architecture from the beginning

**Current Gap:**
Sprint 12 has NO mechanism for any of this. The Skill Creation Wizard (Tasks 12-08, 12-09, 12-10) was specified assuming skill configuration, not skill generation.

**Correct Architecture Pattern: Skill Generation from Project Inputs**

```python
# PROJECT SETUP WIZARD WORKFLOW

class ProjectSetupWizard:
    """
    Generates custom skills for new project during setup.
    Uses NotebookLM + LLM analysis to BUILD project-specific skills.
    """

    async def setup_new_project(self, project_inputs: dict) -> Project:
        """
        Step 1: Collect inputs
        - NotebookLM links
        - Uploaded docs (style guides, character sheets, world bible)
        - Example passages (voice samples)
        - Genre, goals, preferences
        """

        # Step 2: Analyze inputs with NotebookLM
        voice_analysis = await self._analyze_voice_from_examples(
            project_inputs["example_passages"],
            project_inputs["notebooklm_links"]
        )

        # Step 3: GENERATE project-specific skills
        skills = await self._generate_project_skills(
            project_name=project_inputs["name"],
            voice_profile=voice_analysis,
            reference_docs=project_inputs["uploaded_docs"],
            genre=project_inputs["genre"]
        )

        # Step 4: Create project structure
        project = Project(
            id=project_inputs["name"],
            skills={
                "scene-analyzer": skills["analyzer"],
                "scene-enhancement": skills["enhancer"],
                "character-validator": skills["validator"],
                "scene-writer": skills["writer"],
                "scene-multiplier": skills["multiplier"],
                "scaffold-generator": skills["scaffold"]
            },
            knowledge_base=f"projects/{project_inputs['name']}/knowledge/"
        )

        return project

    async def _generate_project_skills(
        self,
        project_name: str,
        voice_profile: VoiceProfile,
        reference_docs: List[Document],
        genre: str
    ) -> Dict[str, Skill]:
        """
        Generate all 6 skill types for this specific project.
        Each skill gets:
        - Custom SKILL.md with project-specific prompts
        - references/ directory with project materials
        - Project-specific scoring criteria
        - Voice-specific anti-patterns
        """

        skills = {}

        # Generate Scene Analyzer
        skills["analyzer"] = await self._build_scene_analyzer(
            name=f"scene-analyzer-{project_name}",
            voice_profile=voice_profile,
            quality_criteria=self._derive_quality_criteria(genre, voice_profile),
            anti_patterns=self._extract_anti_patterns(reference_docs, voice_profile),
            metaphor_domains=self._identify_metaphor_domains(voice_profile)
        )

        # Generate Scene Enhancer (same voice, fix patterns)
        skills["enhancer"] = await self._build_scene_enhancer(
            name=f"scene-enhancer-{project_name}",
            voice_profile=voice_profile,
            fix_patterns=skills["analyzer"].anti_patterns
        )

        # Generate remaining 4 skills...

        return skills

# EXAMPLE OUTPUT: The Explants Project

explants_project = {
    "id": "the-explants",
    "skills": {
        "scene-analyzer-the-explants": {
            "skill_file": "projects/the-explants/.claude/skills/scene-analyzer-the-explants/SKILL.md",
            "references": "projects/the-explants/.claude/skills/scene-analyzer-the-explants/references/",
            "voice_profile": {
                "name": "Mickey Bardot (Enhanced)",
                "characteristics": ["cynical", "compressed", "philosophical"],
                "extracted_from": ["NotebookLM analysis", "uploaded voice samples"]
            },
            "quality_criteria": {
                "voice_authenticity": 30,
                "character_consistency": 20,
                "metaphor_discipline": 20,
                # ... derived from genre + voice analysis
            }
        },
        # ... 5 more skills
    }
}

# EXAMPLE OUTPUT: A Romance Novel Project

romance_project = {
    "id": "witty-hearts",
    "skills": {
        "scene-analyzer-witty-hearts": {
            "skill_file": "projects/witty-hearts/.claude/skills/scene-analyzer-witty-hearts/SKILL.md",
            "references": "projects/witty-hearts/.claude/skills/scene-analyzer-witty-hearts/references/",
            "voice_profile": {
                "name": "Witty Romantic Comedy",
                "characteristics": ["witty", "warm", "emotionally open"],
                "extracted_from": ["uploaded romance examples", "style guide"]
            },
            "quality_criteria": {
                "voice_authenticity": 25,
                "romantic_tension": 25,
                "emotional_beats": 20,
                # ... derived from romance genre conventions
            }
        },
        # ... 5 more skills
    }
}
```

**Required Implementation:**

**MUST BE DONE BEFORE STUDENT TESTING (January):**

1. **Project Setup Wizard UI** (Frontend)
   - Multi-step form: Project details → Voice samples → Upload docs → NotebookLM links → Review
   - Progress indicator
   - Preview of generated skills

2. **Skill Generation Engine** (Backend)
   - NotebookLM integration for voice analysis
   - LLM-based voice profile extraction from examples
   - Quality criteria derivation from genre
   - Anti-pattern extraction from style guides
   - SKILL.md file generation
   - Reference materials organization

3. **Project-Specific Storage Structure:**
   ```
   projects/
   ├── the-explants/
   │   ├── .claude/
   │   │   └── skills/
   │   │       ├── scene-analyzer-the-explants/
   │   │       │   ├── SKILL.md
   │   │       │   └── references/
   │   │       │       ├── mickey-voice.md
   │   │       │       ├── anti-patterns.md
   │   │       │       └── metaphor-domains.md
   │   │       ├── scene-enhancer-the-explants/
   │   │       └── ... (4 more skills)
   │   └── knowledge/
   │       └── craft/ (project-specific knowledge)
   └── witty-hearts/
       ├── .claude/
       │   └── skills/
       │       ├── scene-analyzer-witty-hearts/
       │       └── ... (6 skills)
       └── knowledge/
   ```

4. **Skill Registry Updates:**
   - Track skills by project_id
   - Route skill calls to correct project-specific skill
   - Allow skill updates/refinement per project

**Impact if Not Fixed IMMEDIATELY:**
- ❌ BLOCKING: Students cannot set up their novels in January
- ❌ BLOCKING: Platform cannot scale beyond The Explants
- ❌ BLOCKING: No way to test with second project
- ❌ System only works for G.C. Harris

**Impact When Fixed:**
- ✅ Students can set up novels in January course
- ✅ Each writer gets custom skills for their voice/genre
- ✅ Platform ready for multiple concurrent projects
- ✅ Foundation for skill marketplace

---

## 🟡 Medium Priority Issues

### Issue #2: Knowledge Base Structure (RESOLVED by Issue #1 Fix)

**Status:** Will be addressed by Project Setup Wizard
**Priority:** MEDIUM (automatically fixed when Issue #1 resolved)

**Problem:**
Current knowledge base is global with Explants-specific content:
- `factory/knowledge/craft/voice-gold-standard.md` - Has Explants examples
- `factory/knowledge/craft/anti-patterns.md` - Explants-focused
- No project-specific storage

**Solution (Part of Issue #1 Fix):**

When Project Setup Wizard is implemented, knowledge structure becomes:

```
factory/
├── knowledge/
│   └── templates/          ← Generic templates for skill generation
│       ├── voice-guidelines-template.md
│       ├── common-anti-patterns-template.md
│       └── quality-frameworks-template.md
│
projects/
├── the-explants/
│   ├── .claude/skills/     ← Project-specific skills
│   │   ├── scene-analyzer-the-explants/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── mickey-voice.md
│   │   │       ├── anti-patterns.md
│   │   │       └── metaphor-domains.md
│   │   └── ... (5 more skills)
│   └── knowledge/          ← Project-specific knowledge base
│       └── craft/
│
└── witty-hearts/
    ├── .claude/skills/     ← Different project, different skills
    │   └── scene-analyzer-witty-hearts/
    │       ├── SKILL.md
    │       └── references/
    │           └── romance-voice.md
    └── knowledge/
```

**This resolves automatically when Issue #1 (Project Setup Wizard) is implemented.**

---

### Issue #3: MCP Bridge Calls Subprocess

**Status:** Works but fragile
**Priority:** MEDIUM

**Problem:**
Current MCP bridge calls Claude Code via subprocess:
```python
result = subprocess.run(["claude", "skill", skill_name, input])
```

**Issues:**
- Requires Claude Code CLI installed
- Process overhead for each call
- No connection pooling
- Error handling complex

**Better Approach:**
- Direct Anthropic API calls with skill metadata
- Or: Persistent Claude Code process
- Or: Python SDK for Claude Skills (if available)

---

### Issue #4: No Skill Version Management

**Status:** Missing feature
**Priority:** LOW (future)

**Problem:**
Skills have version numbers but no version management:
- Can't roll back to previous version
- Can't test new version without affecting production
- No A/B testing of skill improvements

**Proposed:**
```python
skill_versions = {
    "scene-analyzer": {
        "v1.0": {...},  # Original
        "v1.1": {...},  # Improved scoring
        "v2.0": {...},  # Major rewrite
        "active": "v1.1"
    }
}
```

---

## 🟢 Future Enhancements

### Enhancement #1: Skill Marketplace

**When:** After multi-project support (Issue #1) fixed

**Concept:**
- Writers share skill templates
- Community ratings and reviews
- Featured skills by genre
- Premium skills ($)

**Example:**
- "Literary Fiction Scene Analyzer" by award-winning author
- "Cozy Mystery Consistency Checker" by mystery writing group
- "YA Voice Authenticator" by successful YA author

---

### Enhancement #2: Skill Learning & Improvement

**When:** Post-launch, with usage data

**Concept:**
- Skills learn from user feedback
- "Accept this fix" vs "Reject" trains model
- Personalized skill tuning per writer
- Collaborative filtering (writers with similar style)

**Example:**
```python
# After writer accepts/rejects fixes
skill.learn_from_feedback(
    scene_id="1.3.2",
    suggested_fix="Remove 'with precision'",
    user_action="accepted",
    result_score_improvement=+4
)

# Skill adapts scoring for this writer
skill.weights["anti_patterns"]["with_precision"] *= 1.1
```

---

### Enhancement #3: Cross-Project Insights

**When:** After multiple projects analyzed

**Concept:**
- Compare your project to others in genre
- "Your pacing is 20% slower than typical thriller"
- "Your dialogue/narrative ratio matches bestsellers"
- Market fit scoring

---

## 📋 Technical Debt

### TD-1: Test Coverage

**Current:** Smoke tests only
**Need:** Full unit and integration tests
**Priority:** Before student testing

---

### TD-2: Error Handling

**Current:** Basic error responses
**Need:** Graceful degradation, retry logic, user-friendly errors
**Priority:** Before public launch

---

### TD-3: Performance Optimization

**Current:** No caching, sequential processing
**Need:** Caching, parallel processing, connection pooling
**Priority:** After Sprint 13, before scale

---

### TD-4: Documentation

**Current:** Developer docs only
**Need:** User guides, video tutorials, FAQ
**Priority:** Before student testing

---

## 🔄 Resolution Process

**For each issue:**
1. Document thoroughly (this file)
2. Discuss with user (G.C. Harris)
3. Prioritize in sprint planning
4. Implement and test
5. Mark as resolved
6. Document lessons learned

**Update Frequency:** After each sprint

---

## 📞 Contact

Questions about these issues? Document them here or in sprint planning discussions.

---

**Remember:** These aren't bugs - they're evolution. Sprint 12 built a solid foundation. These issues represent the path from "works for one project" to "platform for all writers."
