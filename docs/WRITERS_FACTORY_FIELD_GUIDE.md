# Writers Factory Field Guide
## Your Practical Guide to Understanding What Should Happen

**Created:** November 15, 2025
**Purpose:** Help you understand expected behavior, trace bugs, and add features
**Audience:** Vibe coders and practical developers (not computer engineering theory)

---

## Table of Contents

1. [Quick Start: What Is This Thing?](#quick-start)
2. [The Big Picture](#big-picture)
3. [Feature Catalog](#feature-catalog) - All 35 features explained
4. [Major Workflows](#major-workflows) - What should happen step-by-step
5. [Component Cheat Sheet](#component-cheat-sheet) - What each piece does
6. [Bug Detective Guide](#bug-detective-guide) - How to trace issues
7. [Common Problems & Solutions](#common-problems)

---

## Quick Start: What Is This Thing? {#quick-start}

**Writers Factory** is a writing assistant that:
- Analyzes YOUR unique writing style
- Creates custom AI tools tuned to YOUR voice
- Lets you compare different AI models side-by-side
- Helps you write, edit, and plan novels

### The Magic Trick

Instead of using generic AI prompts that work for everyone (poorly), Writers Factory:
1. Reads 3-5 examples of YOUR writing
2. Figures out YOUR patterns (sentence length, metaphors, POV style)
3. Generates 6 custom AI "skills" that understand YOUR voice
4. Uses those skills to help you write consistently

### Three Ways to Use It

1. **Web Interface** - Visual, browser-based, easiest
   - Start: `npm run dev` → visit http://localhost:5173

2. **Terminal UI (TUI)** - Full-screen terminal app, keyboard-driven
   - Start: `python -m factory.tui.app`

3. **Command Line (CLI)** - Scriptable commands
   - Example: `python -m factory.ui.cli workflow run scene-generation`

---

## The Big Picture {#big-picture}

### How Writers Factory Is Organized

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Setup Wizard │  │ Scene Editor │  │ AI Tools     │      │
│  │ (Create      │  │ (Write/Edit) │  │ (Compare     │      │
│  │  Project)    │  │              │  │  Models)     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
└─────────┼─────────────────┼──────────────────┼───────────────┘
          │                 │                  │
          ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  REST API Routes:                                       │ │
│  │  /api/setup/*      /api/scene/*      /api/compare      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────┬──────────────────┬──────────────────┬─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      CORE ENGINE                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Voice Extractor │  │ Skill Generator │  │ Skill       │ │
│  │ (Analyze your   │  │ (Create custom  │  │ Orchestrator│ │
│  │  writing)       │  │  AI prompts)    │  │ (Run skills)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Agent Pool      │  │ Knowledge       │  │ Storage     │ │
│  │ (Manage 15+     │  │ Router          │  │ (Save       │ │
│  │  AI models)     │  │ (Query NotebookLM)│ │  sessions)  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────┬──────────────────┬──────────────────┬─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Anthropic    │  │ OpenAI       │  │ Google       │      │
│  │ (Claude)     │  │ (GPT-4)      │  │ (Gemini)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Ollama       │  │ DeepSeek     │  │ NotebookLM   │      │
│  │ (Local Free) │  │ (Chinese LLM)│  │ (Knowledge)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: What Happens When You Write

```
1. You write/edit scene
       ↓
2. Frontend saves to backend
       ↓
3. Backend stores in manuscript structure
       ↓
4. If you click "Analyze Scene":
       ↓
5. Skill Orchestrator loads your custom analyzer
       ↓
6. Sends scene + your voice profile to Claude/GPT
       ↓
7. AI scores scene using YOUR quality criteria
       ↓
8. Results shown in UI with breakdown
```

---

## Feature Catalog {#feature-catalog}

All 35 features, organized by what you're trying to do.

### PROJECT SETUP & MANAGEMENT

#### 1. Project Setup Wizard ⭐ **NEW - Sprint 14**

**What it does:** Creates a custom writing project tuned to YOUR voice in 10 minutes.

**How to use:**
1. Click "Create New Project" in web UI
2. Follow 6 steps:
   - Enter project name and genre
   - Paste 3-5 example passages (500-1000 words each)
   - Upload style guides (optional)
   - Wait for AI analysis (2-3 minutes)
   - Review generated skills
   - Click "Create Project"

**Expected result:**
- New folder: `projects/your-project-name/`
- 6 custom skills in `.claude/skills/`
- Voice profile saved in `knowledge/craft/`
- Project config in `config.json`

**How to verify it worked:**
```bash
ls projects/your-project-name/.claude/skills/
# Should show 6 folders:
# scene-analyzer-your-project/
# scene-enhancer-your-project/
# character-validator-your-project/
# scene-writer-your-project/
# scene-multiplier-your-project/
# scaffold-generator-your-project/
```

**Common issues:**
- **Skills not generated**: Check backend logs, may need API key
- **Voice profile empty**: Passages too short (need 500+ words each)
- **Analysis failed**: Check Claude API connection

**Where to look:**
- Frontend: `webapp/frontend-v2/src/features/setup/ProjectSetupWizard.jsx`
- Backend: `webapp/backend/routes/setup.py`
- Core: `factory/core/voice_extractor.py`, `factory/core/skill_generator.py`

---

#### 2. Manuscript Import

**What it does:** Brings existing manuscript into Writers Factory structure.

**How to use:**
```bash
python factory/tools/manuscript_importer.py \
  --source /path/to/your/manuscript \
  --output projects/my-novel/scenes
```

**Expected result:**
- Scenes organized: `Act 1/Chapter 1/1.1.1 Scene Title.md`
- Metadata extracted from filenames
- Word counts calculated

**File naming convention it expects:**
```
1.2.3 Scene Title.md
│ │ │
│ │ └─ Scene number within chapter
│ └─── Chapter number
└───── Act number
```

**Common issues:**
- **Files not imported**: Check filename format matches pattern
- **Wrong structure**: Verify directory organization (PART 1/, PART 2/)

---

#### 3. Session Management

**What it does:** Auto-saves your work, tracks session history.

**How to use:** Automatic - just work normally.

**Expected behavior:**
- Auto-saves every 30 seconds (shown in status bar)
- "Last saved: 15s ago" updates in real-time
- Session history shows last 20 sessions

**How to verify it worked:**
```bash
ls .sessions/
# Should show files like: session_2025-11-15_10-30-45.json
```

**Common issues:**
- **Not auto-saving**: Check status bar shows "Auto-save: ON"
- **Lost work**: Sessions stored in `.sessions/` directory

---

### WRITING & EDITING

#### 4. Scene Generation

**What it does:** Creates new scenes from outlines or prompts.

**How to use:**
1. Go to "Writing" tab
2. Enter scene outline: "Mickey Bardot confronts her handler about the missing shipment"
3. Select model (or use default)
4. Click "Generate Scene"

**Expected result:**
- 500-1500 word scene
- Matches your voice profile
- Takes 30-60 seconds
- Cost shown after generation

**How to verify quality:**
- Run scene through your custom analyzer
- Should score 70+ if outline was clear

**Common issues:**
- **Generic output**: Voice profile not loaded - check project config
- **Wrong style**: Selected wrong model - try Claude Sonnet for creative work

---

#### 5. Scene Enhancement

**What it does:** Improves existing scenes while keeping your voice.

**How to use:**
1. Paste scene into editor
2. Choose focus: "Voice consistency", "Pacing", or "Overall"
3. Click "Enhance Scene"

**Expected result:**
- Scene rewritten with improvements
- Preserves plot/structure
- Tightens prose or fixes voice drift
- Shows diff of changes

**Before/After example:**
```
Before: "She felt really angry about the situation and seemed upset."
After:  "Rage simmered beneath her calm exterior."
```

**Common issues:**
- **Changes too much**: Use "Voice only" focus, not "Overall"
- **Doesn't improve**: Scene may already be strong - check analyzer score first

---

#### 6. Custom Scene Analyzer ⭐ **GENERATED SKILL**

**What it does:** Scores scenes 0-100 using YOUR quality criteria.

**How to use:**
1. Select your project
2. Paste scene
3. Click "Analyze Scene"

**Expected output:**
```
Overall Score: 87/100 (Excellent)

Breakdown:
- Voice Authenticity: 27/30 ✓ Strong compressed style, good metaphor discipline
- Character: 18/20 ✓ Consistent with Mickey's cynicism
- Scene Craft: 26/30 ⚠ Pacing drags in middle paragraph
- Emotional Impact: 16/20 ✓ Effective tension building

Recommendations:
- Consider tightening lines 34-38
- Strong opening hook
```

**Score ranges:**
- 90-100: Excellent (publish-ready)
- 80-89: Good (minor tweaks)
- 70-79: Needs work (revision required)
- Below 70: Weak (major rewrite)

**Common issues:**
- **All scenes score low**: Criteria may be too strict - check `quality-criteria.md`
- **Contradictory feedback**: May need to refine voice profile

---

### AI TOOLS & ANALYSIS

#### 7. Model Comparison Tool

**What it does:** Runs same prompt on 2-4 models, shows side-by-side results.

**How to use:**
1. Click "Compare Models"
2. Select 2-4 models (e.g., Claude Sonnet, GPT-4, Gemini)
3. Enter prompt
4. Click "Compare"

**Expected result:**
```
┌─────────────────┬─────────────────┬─────────────────┐
│ Claude Sonnet   │ GPT-4o          │ Gemini 2 Flash  │
├─────────────────┼─────────────────┼─────────────────┤
│ [Output]        │ [Output]        │ [Output]        │
│ Cost: $0.05     │ Cost: $0.03     │ Cost: $0.01     │
│ Time: 15s       │ Time: 12s       │ Time: 8s        │
│ Words: 847      │ Words: 923      │ Words: 756      │
└─────────────────┴─────────────────┴─────────────────┘

Visual Diff: [Highlights where outputs differ]
```

**How to use results:**
- Pick the best output → System learns your preferences
- Future suggestions prioritize your preferred models

**Common issues:**
- **Models timeout**: Try smaller prompts or fewer models
- **Identical outputs**: Models may collapse to similar style - try more creative prompts

---

#### 8. Voice Profile Extraction

**What it does:** Analyzes your writing to extract patterns.

**How to use:** Automatic in Setup Wizard step 4.

**What it extracts:**
1. **Voice Name**: "Compressed Noir" or "Warm Literary"
2. **Sentence Structure**:
   - Average length: 12-15 words (you) vs 18-22 (typical)
   - Compression: 65% (tight) vs 90% (normal)
   - Variety: High/Medium/Low
3. **POV Style**:
   - Depth: Deep/Psychic
   - Consciousness mode: 75% (very immersive)
4. **Metaphor Domains**:
   - Gambling: 25% ("stacked deck", "betting on", "all in")
   - Technology: 15% ("interface", "circuit", "system")
5. **Anti-Patterns**: "Avoid: filter words (felt, seemed), adverbs"

**Expected display:**
```
Voice Profile: Mickey Bardot Enhanced Noir

Primary Characteristics:
✓ Compressed sentence structure (65% of literary average)
✓ Economical dialogue (subtext > exposition)
✓ Gambling metaphors (20-25% usage)
✓ Deep POV with minimal filter words
✓ Present-tense immediacy

Metaphor Domains:
🎰 Gambling (25%) - Cards, bets, odds, stakes
💻 Technology (15%) - Systems, interfaces, networks
⚔️ Combat (10%) - Tactical, strategic, engagement
```

---

### KNOWLEDGE & RESEARCH

#### 9. Knowledge Router

**What it does:** Answers questions about your story using AI knowledge systems.

**How to use:**
1. Press 'K' in TUI or click "Ask Question"
2. Type: "What are Mickey's primary motivations?"
3. System routes to Cognee (local) or NotebookLM (if configured)

**Expected response time:**
- Cognee: 2-5 seconds
- NotebookLM: 10-15 seconds (calls external API)

**Question types it handles:**
- **Factual**: "What color are Mickey's eyes?"
- **Analytical**: "How does Mickey's relationship with Trace evolve?"
- **Thematic**: "What does gambling represent in this story?"

**Common issues:**
- **Empty responses**: Knowledge base not populated - import manuscript first
- **Wrong answers**: Update knowledge base after major edits

---

#### 10. NotebookLM Integration

**What it does:** Extracts knowledge from your Google NotebookLM notebooks.

**How to use:**
1. Setup Wizard step 2: Paste NotebookLM URLs
2. System queries notebooks for characters, world, themes
3. Knowledge saved to `knowledge/craft/story-context.md`

**Expected extraction:**
```
Characters:
- Mickey Bardot: Protagonist, ex-military, augmented vision...
- Trace: Handler, conflicted loyalties...

World:
- Detroit 2089: Post-collapse megacity...
- Quantum tunnels: Unstable transit network...

Themes:
- Trust vs self-preservation
- Human augmentation ethics
```

**Common issues:**
- **Can't access notebook**: Make sure notebook is shared/public
- **No data extracted**: Notebook may be empty - add source documents

---

### MODEL COMPARISON

#### 11. Available Models

**What models are supported:**

**Premium (Best Quality):**
- Claude Sonnet 4.5 ($0.003 in / $0.015 out per 1K tokens)
- Claude Opus 4 ($0.015 in / $0.075 out)
- GPT-4o ($0.0025 in / $0.01 out)

**Fast & Cheap:**
- Gemini 2.0 Flash ($0.0001 in / $0.0004 out)
- GPT-3.5 Turbo ($0.0005 in / $0.0015 out)

**Local (FREE):**
- Ollama Llama 3.2 ($0.00)
- Ollama Mistral ($0.00)

**Chinese Models:**
- DeepSeek V3
- Qwen Max
- Kimi
- Doubao

**How to see all models:**
```bash
python -m factory.ui.cli agent list
```

**Expected output:**
```
Available Models:
┌────────────────────┬──────────┬─────────┬──────────────┐
│ Model              │ Provider │ Enabled │ Cost/1K Out  │
├────────────────────┼──────────┼─────────┼──────────────┤
│ claude-sonnet-4.5  │ Anthropic│ ✓       │ $0.015       │
│ gpt-4o             │ OpenAI   │ ✓       │ $0.010       │
│ ollama-mistral     │ Ollama   │ ✓       │ FREE         │
└────────────────────┴──────────┴─────────┴──────────────┘
```

---

### CHARACTER & STORY TOOLS

#### 12. Creation Wizard (Story Bible Generator)

**What it does:** Builds complete story bible through 5-phase questionnaire.

**How to use:**
1. Run: `python -m factory.wizard.wizard`
2. Answer questions across 5 phases
3. Get 4,000-6,000 word story bible

**Phases:**
1. **Foundation** (10 min):
   - Genre, themes, core concept
   - Target audience, tone
2. **Character** (15 min):
   - Protagonist wants, needs, flaws
   - Supporting cast
3. **Plot** (20 min):
   - 15-beat structure
   - Major turning points
4. **World** (15 min):
   - Setting, rules, cultural context
5. **Symbolism** (10 min):
   - Recurring motifs, deeper meanings

**Expected output file:** `story-bible.md`

**Sample output:**
```markdown
# Story Bible: The Explants

## Foundation
Genre: Sci-fi Noir Thriller
Logline: A woman with augmented vision navigates corporate...

## Protagonist
Name: Mickey Bardot
Want: Escape her handler's control
Need: Learn to trust others
Fatal Flaw: Self-reliance to the point of isolation
...
```

---

### OTHER TOOLS

#### 13. Cost Tracking

**What it tracks:**
- Cost per API call
- Session total
- Lifetime total
- Cost by model

**Where to see it:**
- Status bar (TUI): "Session: $2.47"
- Stats command: `python -m factory.ui.cli stats`

**Expected output:**
```
Session Statistics:
Total Cost: $2.47
Total Generations: 12
Average Cost/Generation: $0.21

By Model:
- Claude Sonnet 4.5: $1.85 (8 calls)
- GPT-4o: $0.42 (3 calls)
- Ollama Mistral: $0.00 (1 call, FREE)
```

**How to reduce costs:**
- Use Ollama for drafts (FREE)
- Use Gemini Flash for quick tasks ($0.0004/1K)
- Reserve Claude Opus for final polish only

---

#### 14. Auto-save System

**What it does:** Saves work automatically every 30 seconds.

**How to verify it's working:**
- Check status bar: "Last saved: 12s ago"
- Files appear in `.sessions/` directory

**Manual save:** Press Ctrl+S (or Cmd+S)

**What gets saved:**
- Scene content
- Session state
- Cost data
- Operation history

**Recovery after crash:**
- Restart app → "Resume session from 2 minutes ago?" → Yes

---

## Major Workflows {#major-workflows}

### Workflow 1: Create New Project (Setup Wizard)

**Time:** 10-15 minutes
**Complexity:** Easy

```
Step 1: Project Details (1 min)
├─ User enters: name, genre, goals
└─ Validation: Name must be lowercase-with-dashes

Step 2: Voice Input (5 min)
├─ User pastes 3-5 passages (500-1000 words each)
├─ Optional: Add NotebookLM URLs
├─ Validation: Each passage must be 500+ words
└─ Expected: "Passage 3/5 added"

Step 3: Reference Materials (2 min - optional)
├─ User uploads: style guides, character sheets
├─ User pastes: anti-patterns to avoid
└─ Expected: Files listed with delete buttons

Step 4: AI Analysis (2-3 min - automated)
├─ Loading: "Analyzing your voice... (1-2 minutes)"
├─ Backend: Calls voice_extractor.py
├─ AI: Claude Sonnet 4.5 analyzes passages
├─ Extraction: Voice name, characteristics, metaphors, criteria
└─ Display: Voice profile with cards and metrics

Step 5: Review & Test (2-3 min - automated + optional)
├─ Loading: "Generating 6 custom skills... (2-3 minutes)"
├─ Backend: Calls skill_generator.py
├─ AI: Generates 6 SKILL.md files with custom prompts
├─ Display: Checklist of 6 skills
├─ Optional Test:
│  ├─ User pastes test scene
│  ├─ Click "Test Analyzer"
│  └─ See score (0-100) with breakdown
└─ Expected: All 6 skills showing "Ready" status

Step 6: Finalize (30 sec)
├─ Display: Project summary
├─ User clicks: "Create Project"
├─ Backend: Calls project_creator.py
├─ File operations:
│  ├─ Create directory: projects/project-name/
│  ├─ Save skills: .claude/skills/*/SKILL.md
│  ├─ Save voice profile: knowledge/craft/voice-gold-standard.md
│  └─ Save config: config.json
└─ Success: "Project created successfully!"

Result:
└─ New project ready to use with 6 custom AI skills
```

**What should exist after:**
```
projects/my-novel/
├── .claude/
│   └── skills/
│       ├── scene-analyzer-my-novel/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── voice-profile.md
│       │       ├── anti-patterns.md
│       │       ├── quality-criteria.md
│       │       └── metaphor-domains.md
│       ├── scene-enhancer-my-novel/
│       ├── character-validator-my-novel/
│       ├── scene-writer-my-novel/
│       ├── scene-multiplier-my-novel/
│       └── scaffold-generator-my-novel/
├── knowledge/
│   └── craft/
│       ├── voice-gold-standard.md
│       └── story-context.md (if NotebookLM used)
├── scenes/ (empty, ready for manuscript)
├── config.json
└── README.md
```

---

### Workflow 2: Analyze a Scene

**Time:** 30-60 seconds
**Complexity:** Easy

```
Step 1: Select Project
├─ User: Opens project dropdown
├─ System: Lists all projects in projects/ directory
└─ User: Selects "my-novel"

Step 2: Open Scene Analyzer
├─ User: Clicks "AI Tools" → "Scene Analyzer"
└─ UI: Shows analyzer interface

Step 3: Input Scene
├─ User: Pastes scene content (200+ words recommended)
└─ UI: Shows word count

Step 4: Run Analysis
├─ User: Clicks "Analyze Scene"
├─ UI: Shows loading: "Analyzing..."
├─ Backend: POST /api/setup/test-skill
├─ Skill Orchestrator: Loads scene-analyzer-my-novel
├─ Loads references:
│  ├── voice-profile.md
│  ├── quality-criteria.md
│  └── anti-patterns.md
├─ Builds prompt: Scene + Voice Profile + Criteria
├─ Calls: Claude Sonnet 4.5
├─ Claude: Scores scene across 4 categories
└─ Returns: JSON with scores and feedback

Step 5: Display Results
├─ Overall Score: 87/100
├─ Quality Tier: "Excellent"
├─ Category Breakdown:
│  ├── Voice Authenticity: 27/30
│  ├── Character Consistency: 18/20
│  ├── Scene Craft: 26/30
│  └── Emotional Impact: 16/20
└─ Recommendations: "Strong opening hook. Consider..."

Step 6: User Action
├─ Option A: Accept → Move on
├─ Option B: Enhance → Send to scene enhancer
└─ Option C: Rewrite → Edit manually
```

**Expected timing:**
- API call: 10-15 seconds
- Display: Instant
- Total: 15-20 seconds

**Expected cost:**
- Input: ~500 tokens (scene) + ~1000 tokens (voice profile)
- Output: ~500 tokens (analysis)
- Total: ~$0.03 per analysis

---

### Workflow 3: Generate New Scene

**Time:** 45-90 seconds
**Complexity:** Medium

```
Step 1: Prepare Outline
├─ User: Writes scene outline
└─ Example: "Mickey confronts Trace about missing shipment. She's angry but controlled. Location: Safe house basement. Goal: Get truth without revealing her suspicions."

Step 2: Optional: Query Knowledge
├─ User: Presses 'K' or clicks "Ask Question"
├─ Question: "What's Mickey and Trace's relationship history?"
├─ Knowledge Router: Checks Cognee → NotebookLM
└─ Returns: Context about their backstory

Step 3: Select Generation Settings
├─ Model: Claude Sonnet 4.5 (recommended for creative)
├─ Length: 800 words
└─ Knowledge: Include story context ✓

Step 4: Generate
├─ User: Clicks "Generate Scene"
├─ Backend: POST /api/scene/generate
├─ Workflow Engine: scene_operations/generation.py
├─ Build prompt:
│  ├── Outline
│  ├── Voice profile
│  ├── Story context (from knowledge query)
│  └── "Write in Mickey Bardot Enhanced Noir voice..."
├─ Call: Selected model (Claude Sonnet)
├─ Stream: Results appear progressively
└─ Complete: Full scene returned

Step 5: Review Generated Scene
├─ Display: Scene in editor
├─ Show: Word count, generation time, cost
└─ Auto-run: Quick quality check

Step 6: User Decision
├─ Option A: Accept → Save to manuscript
├─ Option B: Enhance → Run through enhancer
├─ Option C: Regenerate → Try different model
└─ Option D: Edit → Manual revision
```

**Expected quality markers:**
- Uses project-specific metaphors ✓
- Matches sentence compression ✓
- Appropriate POV depth ✓
- Consistent character voice ✓

---

### Workflow 4: Compare Models on Same Prompt

**Time:** 30-60 seconds
**Complexity:** Easy

```
Step 1: Open Model Comparison
├─ User: Clicks "Compare Models" or presses 'C' (TUI)
└─ UI: Shows model selection grid

Step 2: Select Models
├─ User: Clicks 2-4 models
├─ Examples:
│  ├── Claude Sonnet 4.5 (quality benchmark)
│  ├── GPT-4o (comparison)
│  ├── Gemini 2.0 Flash (speed test)
│  └── Ollama Mistral (free option)
└─ Validation: Must select 2-4 models

Step 3: Enter Prompt
├─ User: Types prompt
└─ Example: "Describe Mickey's augmented vision activating"

Step 4: Run Comparison
├─ User: Clicks "Compare"
├─ Backend: POST /api/compare
├─ Model Comparison Tool: parallel execution
├─ For each model:
│  ├── Start timer
│  ├── Call API
│  ├── Collect response
│  ├── Calculate cost
│  └── Count words
└─ Wait: All models complete (or timeout at 60s)

Step 5: Display Side-by-Side
├─ Layout: 2-4 columns (one per model)
├─ Each column shows:
│  ├── Model name
│  ├── Generated output
│  ├── Word count
│  ├── Generation time
│  └── Cost
└─ Visual diff: Highlights where outputs differ

Step 6: Pick Winner
├─ User: Clicks "This one's best" on preferred output
├─ System: Records preference
└─ Future: Prioritizes this model for similar tasks
```

**Expected output example:**
```
┌────────────────────┬────────────────────┬────────────────────┐
│ Claude Sonnet 4.5  │ GPT-4o             │ Gemini 2.0 Flash   │
├────────────────────┼────────────────────┼────────────────────┤
│ The world shifted  │ Her vision flared  │ Augmented vision   │
│ to overlays—       │ with data streams  │ came online with   │
│ threat markers in  │ as the implant     │ a soft chime...    │
│ crimson, safe      │ activated...       │                    │
│ zones in azure...  │                    │                    │
│                    │                    │                    │
│ 147 words          │ 152 words          │ 98 words           │
│ 18.2s              │ 14.7s              │ 6.3s               │
│ $0.043             │ $0.028             │ $0.002             │
│                    │                    │                    │
│ [Select] ✓         │ [Select]           │ [Select]           │
└────────────────────┴────────────────────┴────────────────────┘

Differences highlighted:
- Claude: More metaphorical ("shifted to overlays")
- GPT: More technical ("data streams")
- Gemini: Simpler, faster
```

---

### Workflow 5: Import Existing Manuscript

**Time:** 2-5 minutes
**Complexity:** Medium

```
Step 1: Prepare Files
├─ Organize manuscript with naming convention:
│  └─ Format: "A.C.S Scene Title.md"
│     └─ Example: "1.2.3 Mickey Meets Trace.md"
└─ Directory structure (optional):
   └─ PART 1/, PART 2/, etc.

Step 2: Run Import
├─ Command:
│  └─ python factory/tools/manuscript_importer.py \
│       --source /path/to/manuscript \
│       --output projects/my-novel/scenes
└─ Process starts

Step 3: File Processing
├─ Scanner: Walks directory tree
├─ For each .md file:
│  ├── Parse filename: Extract act, chapter, scene numbers
│  ├── Read content
│  ├── Count words
│  ├── Extract metadata
│  └── Create scene object
└─ Build hierarchy: Acts → Chapters → Scenes

Step 4: Storage
├─ Create manuscript structure:
│  └─ projects/my-novel/scenes/
│     ├─ Act 1/
│     │  ├─ Chapter 1/
│     │  │  ├─ 1.1.1 Opening Scene.md
│     │  │  └─ 1.1.2 Mickey's Apartment.md
│     │  └─ Chapter 2/
│     └─ Act 2/
└─ Save metadata: manuscript.json

Step 5: Build Knowledge Base
├─ Analyze imported scenes
├─ Extract:
│  ├── Character appearances
│  ├── Location references
│  ├── Plot threads
│  └── Recurring themes
└─ Populate: Cognee knowledge graph

Step 6: Verification
├─ Show summary:
│  ├── Total scenes: 89
│  ├── Total words: 124,567
│  ├── Acts: 3
│  └── Chapters: 12
└─ Import complete
```

**Expected result:**
```
Import Summary:
✓ 89 scenes imported
✓ 124,567 total words
✓ Structure: 3 acts, 12 chapters
✓ Metadata extracted
✓ Knowledge base populated

Breakdown by Act:
- Act 1: 28 scenes, 41,234 words
- Act 2: 35 scenes, 52,891 words
- Act 3: 26 scenes, 30,442 words
```

---

### Workflow 6: Query Story Knowledge

**Time:** 5-15 seconds
**Complexity:** Easy

```
Step 1: Open Knowledge Panel
├─ TUI: Press 'K'
├─ Web: Click "Ask Question"
└─ UI: Shows query input

Step 2: Type Question
└─ Examples:
   ├─ "What are Mickey's augmentations?"
   ├─ "Where is the safe house located?"
   ├─ "What's the timeline of Chapter 3?"
   └─ "How does the quantum tunnel work?"

Step 3: Route Query
├─ Knowledge Router analyzes question type
├─ Decision tree:
│  ├─ Factual → Cognee (local, fast)
│  ├─ Analytical → NotebookLM (external, deeper)
│  └─ Complex → Both, merge results
└─ Selected: Cognee

Step 4: Query Execution
├─ Cognee:
│  ├── Search knowledge graph
│  ├── Find relevant nodes
│  ├── Extract context
│  └── Build answer
├─ Or NotebookLM:
│  ├── Call external API
│  ├── Wait for response
│  └── Parse result
└─ Return: Structured answer

Step 5: Display Answer
└─ Format:
   ├─ Direct answer
   ├─ Supporting evidence
   ├─ Source references
   └─ Related topics

Example Response:
"Mickey's Augmentations:

Primary: Augmented vision system
- Overlay HUD with threat detection
- Infrared/UV spectrum vision
- Time dilation perception (slow-mo mode)

Secondary: Neural link
- Direct interface with systems
- Enhanced reaction time

Source: Act 1, Chapter 2 (1.2.1, 1.2.3)
Related: Technology systems, Combat capabilities"
```

**Speed expectations:**
- Cognee: 2-5 seconds (local)
- NotebookLM: 10-15 seconds (API call)

---

## Component Cheat Sheet {#component-cheat-sheet}

### Core Engine Components

**What each piece does (plain English):**

| Component | What It Does | When It Runs |
|-----------|-------------|--------------|
| **Voice Extractor** | Reads your example passages and figures out your writing patterns (sentence length, metaphors, POV style) | Setup wizard step 4 |
| **Skill Generator** | Takes your voice profile and creates 6 custom AI prompt files (SKILL.md) | Setup wizard step 5 |
| **Skill Orchestrator** | Routes skill requests to the right custom skill and executes them | Every time you analyze/enhance |
| **Project Creator** | Creates the folder structure for new projects (skills, knowledge, scenes) | Setup wizard step 6 |
| **Agent Pool** | Manages connections to 15+ AI models (Claude, GPT, Gemini, etc.) | Every API call |
| **Knowledge Router** | Decides whether to use Cognee (local) or NotebookLM (external) for questions | When you ask questions |
| **Workflow Engine** | Runs multi-step processes (like "generate then enhance then validate") | Workflow commands |
| **Storage Manager** | Auto-saves sessions, tracks history, handles crash recovery | Continuously (every 30s) |
| **Cost Tracker** | Counts tokens and calculates $ cost for every API call | Every API response |

---

### Frontend Components

**What each UI piece does:**

| Component | What You See | What It Does |
|-----------|-------------|--------------|
| **ProjectSetupWizard.jsx** | 6-step form with progress bar | Collects voice samples, generates skills |
| **SceneEditor.jsx** | Monaco code editor | Edit scenes with syntax highlighting |
| **CraftPanel.jsx** | AI tools dropdown + result display | Run skills (analyze, enhance, etc.) |
| **AIToolsPanel.jsx** | Model selector + prompt input | Quick AI generation |
| **TournamentPanel.jsx** | Model grid with checkboxes | Compare 2-4 models side-by-side |
| **KnowledgePanel.jsx** | Question input + answer display | Query story knowledge |
| **ResearchPanel.jsx** | NotebookLM interface | Deep research queries |
| **FileTree.jsx** | Acts → Chapters → Scenes tree | Navigate manuscript structure |
| **CharacterPanel.jsx** | Character list + details | View/edit character info |
| **BrainstormPage.jsx** | Creation wizard UI | Generate story bible |

---

### Backend Routes

**What each API endpoint does:**

| Endpoint | Method | What It Does | Returns |
|----------|--------|-------------|---------|
| `/api/setup/analyze-voice` | POST | Analyzes voice from passages | Voice profile JSON |
| `/api/setup/generate-skills` | POST | Creates 6 custom skills | Skills objects |
| `/api/setup/test-skill` | POST | Tests analyzer on sample | Score + feedback |
| `/api/setup/create-project` | POST | Creates project structure | Project path |
| `/api/scene/generate` | POST | Generates new scene | Scene text |
| `/api/scene/enhance` | POST | Improves scene | Enhanced scene |
| `/api/compare` | POST | Runs model comparison | Side-by-side results |
| `/api/knowledge/query` | POST | Answers question | Knowledge response |
| `/api/models/available` | GET | Lists models | Model list with costs |
| `/api/session/status` | GET | Current session info | Session data |

---

### File Locations

**Where stuff lives:**

```
writers-factory-core/
├── factory/                    # Core engine (Python)
│   ├── core/                   # Main engine components
│   │   ├── voice_extractor.py       # Analyzes your writing
│   │   ├── skill_generator.py       # Creates custom skills
│   │   ├── skill_orchestrator.py    # Routes skill execution
│   │   ├── project_creator.py       # Makes project folders
│   │   ├── agent_pool.py            # Manages AI models
│   │   └── storage/                 # Session/cost tracking
│   ├── agents/                 # AI model integrations
│   ├── workflows/              # Multi-step processes
│   ├── knowledge/              # Knowledge routing
│   └── integrations/           # External services (NotebookLM)
│
├── webapp/
│   ├── backend/                # FastAPI server
│   │   ├── simple_app.py            # Main API routes
│   │   └── routes/setup.py          # Setup wizard endpoints
│   └── frontend-v2/src/        # React UI
│       └── features/                # UI components by feature
│
├── projects/                   # Your writing projects
│   └── [project-name]/
│       ├── .claude/skills/          # Generated skills
│       ├── knowledge/craft/         # Voice profile
│       ├── scenes/                  # Your manuscript
│       └── config.json              # Project settings
│
└── .sessions/                  # Auto-save data
```

---

## Bug Detective Guide {#bug-detective-guide}

### How to Trace What Went Wrong

#### Problem: Setup wizard fails at voice analysis

**Where to look:**
1. Browser console (F12) - Check for frontend errors
2. Backend logs - Look for API errors
3. Check Claude API connection

**How to debug:**
```bash
# Check backend logs
tail -f webapp/backend/logs/app.log

# Test Claude API directly
curl -X POST http://localhost:8000/api/setup/analyze-voice \
  -H "Content-Type: application/json" \
  -d '{"examplePassages": ["test"], "genre": "literary"}'
```

**Common causes:**
- ❌ API key not set: Check `.env` or credentials
- ❌ Passages too short: Need 500+ words each
- ❌ Network timeout: Claude API slow/unavailable

**Fix:**
```bash
# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Test API connection
python -c "from anthropic import Anthropic; print(Anthropic().models.list())"
```

---

#### Problem: Generated skills don't work

**Where to look:**
1. Check skill files exist:
```bash
ls -la projects/my-novel/.claude/skills/
# Should show 6 folders
```

2. Check SKILL.md content:
```bash
cat projects/my-novel/.claude/skills/scene-analyzer-my-novel/SKILL.md
# Should have full prompt, not empty
```

3. Check references exist:
```bash
ls projects/my-novel/.claude/skills/scene-analyzer-my-novel/references/
# Should show: voice-profile.md, quality-criteria.md, etc.
```

**Common causes:**
- ❌ Skill generation timed out
- ❌ Files written but empty (disk full?)
- ❌ Wrong project selected

**Fix:**
- Re-run setup wizard
- Check disk space: `df -h`
- Verify project config: `cat projects/my-novel/config.json`

---

#### Problem: Scene analyzer gives weird scores

**Debug process:**

**Step 1: Check what criteria are being used**
```bash
cat projects/my-novel/.claude/skills/scene-analyzer-my-novel/references/quality-criteria.md
```

**Step 2: Verify voice profile matches your style**
```bash
cat projects/my-novel/knowledge/craft/voice-gold-standard.md
```

**Step 3: Test analyzer manually**
```python
# Test analyzer with debug output
from factory.core.skill_orchestrator import SkillOrchestrator, SkillRequest

orchestrator = SkillOrchestrator()
request = SkillRequest(
    skill_name="scene-analyzer-my-novel",
    input_data={"scene_content": "YOUR SCENE HERE"},
    context={"project_id": "my-novel"}
)

result = await orchestrator.execute_skill(request, project_id="my-novel")
print(result.debug_info)  # Shows what prompt was sent to AI
```

**Common issues:**
- Voice profile extracted wrong patterns → Re-run wizard with better examples
- Quality criteria too strict → Edit `quality-criteria.md` manually
- Using wrong project → Check project selector

---

#### Problem: Model comparison shows identical outputs

**This might be normal!**

Models sometimes converge on similar solutions. Try:
- More creative/ambiguous prompts
- Longer prompts (500+ words)
- Different model combinations

**If ALWAYS identical:**
Check if models are actually different:
```bash
python -m factory.ui.cli agent list
# Verify each model has different provider/config
```

---

#### Problem: NotebookLM integration not working

**Checklist:**
```bash
# 1. Is NotebookLM client configured?
python -c "from factory.research.notebooklm_client import NotebookLMClient; client = NotebookLMClient(); print('OK')"

# 2. Can you reach NotebookLM API?
curl https://notebooklm.google.com/api/v1/health

# 3. Are notebook URLs valid?
# Should be: https://notebooklm.google.com/notebook/abc123...
```

**Common issues:**
- Notebook not shared/public
- API credentials missing
- Network firewall blocking Google APIs

**Workaround:**
Skip NotebookLM during setup, manually add knowledge to:
```
projects/my-novel/knowledge/craft/story-context.md
```

---

### Logging & Debugging Tools

**Enable debug mode:**
```bash
export WRITERS_FACTORY_DEBUG=1
python -m factory.tui.app
```

**Check session logs:**
```bash
# Find recent session
ls -lt .sessions/ | head -5

# View session details
cat .sessions/session_2025-11-15_10-30-45.json | jq .
```

**API request logging:**
```bash
# Watch backend requests in real-time
tail -f webapp/backend/logs/requests.log

# Filter for errors only
grep ERROR webapp/backend/logs/app.log
```

**Cost tracking audit:**
```bash
# See all API calls with costs
python -m factory.ui.cli stats --detailed

# Expected output:
# Session 2025-11-15 10:30
# - analyze-voice: Claude Sonnet, $0.15
# - generate-skills: Claude Sonnet, $0.87 (6 skills)
# - test-analyzer: Claude Sonnet, $0.03
# Total: $1.05
```

---

## Common Problems & Solutions {#common-problems}

### Installation Issues

**Problem:** `pip install -r requirements.txt` fails

**Solution:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

**Problem:** React app won't start (`npm run dev` fails)

**Solution:**
```bash
cd webapp/frontend-v2
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

### API Connection Issues

**Problem:** "API key not found" errors

**Solution:**
```bash
# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
EOF

# Verify keys loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

---

**Problem:** Claude API timeouts

**Possible causes:**
- Prompt too long (>100K tokens)
- API rate limits hit
- Network issues

**Solutions:**
- Reduce passage length
- Wait 1 minute, retry
- Check Anthropic status: https://status.anthropic.com

---

### Generation Quality Issues

**Problem:** AI outputs don't match my voice

**Diagnosis:**
```bash
# Check voice profile
cat projects/my-novel/knowledge/craft/voice-gold-standard.md

# Look for:
# - Sentence structure metrics match your style?
# - Metaphor domains correct?
# - POV depth accurate?
```

**Solution:**
Re-run setup wizard with better example passages:
- Use 5 passages (not just 3)
- Pick your absolute best writing
- Ensure variety: dialogue, action, description

---

**Problem:** Scene analyzer scores everything low (below 70)

**Possible causes:**
- Quality criteria too strict
- Voice profile unrealistic
- Scenes genuinely need work

**How to check:**
```bash
# Review criteria
cat projects/my-novel/.claude/skills/scene-analyzer-my-novel/references/quality-criteria.md

# Try a known-good scene
# If your BEST scene scores 65, criteria are too strict
```

**Fix:**
Edit `quality-criteria.md` - adjust point thresholds:
```markdown
Before: "Voice Authenticity (30 points) - Must be flawless"
After:  "Voice Authenticity (30 points) - Should match voice profile closely"
```

---

### Performance Issues

**Problem:** Generation takes forever (>2 minutes)

**Check:**
- Which model? (Opus is slowest)
- How long is prompt? (10K+ tokens = slow)
- Network speed?

**Solutions:**
- Use faster model: Gemini Flash, GPT-4o
- Reduce prompt size
- Check internet connection

---

**Problem:** UI freezes during analysis

**This is normal!**
- AI calls take 10-60 seconds
- UI should show "Loading..." spinner
- If spinner missing, that's the bug (not the freeze)

**Fix UI freeze (if spinner missing):**
```jsx
// In React component, ensure loading state shown:
{isLoading && <Loader2 className="animate-spin" />}
```

---

### Data Loss Issues

**Problem:** Lost work after crash

**Recovery:**
```bash
# Find last session
ls -lt .sessions/ | head -1

# Check if recoverable
cat .sessions/[latest-session].json | jq .last_saved

# Manual recovery:
# Open session file, copy scene content from JSON
```

**Prevention:**
- Auto-save runs every 30s automatically
- Manual save: Ctrl+S
- Session files in `.sessions/` are backups

---

## Quick Reference

### File Naming Conventions

**Scenes:**
```
Format: A.C.S Scene Title.md
Example: 1.2.3 Mickey Confronts Trace.md

A = Act number (1, 2, 3...)
C = Chapter number (1, 2, 3...)
S = Scene number (1, 2, 3...)
```

**Projects:**
```
Format: lowercase-with-dashes
Examples:
✓ the-explants
✓ my-romance-novel
✗ The Explants (no caps)
✗ my_novel (no underscores)
```

---

### Keyboard Shortcuts (TUI)

```
TAB         - Next stage
SHIFT+TAB   - Previous stage
C           - Compare models
K           - Ask knowledge question
E           - Enhance current scene
Q           - Quit (with save prompt)
Ctrl+S      - Manual save
```

---

### Cost Estimates

**Typical operations:**

| Operation | Model | Typical Cost |
|-----------|-------|-------------|
| Voice analysis | Claude Sonnet | $0.15-0.25 |
| Generate 6 skills | Claude Sonnet | $0.80-1.20 |
| Analyze scene | Claude Sonnet | $0.03-0.05 |
| Generate scene (800w) | Claude Sonnet | $0.08-0.12 |
| Enhance scene | Claude Sonnet | $0.10-0.15 |
| Model comparison (4 models) | Mixed | $0.15-0.30 |

**Budget options:**
- Use Ollama (local) for drafts: **$0.00**
- Use Gemini Flash: **~90% cheaper** than Claude
- Use GPT-3.5: **~70% cheaper** than Claude

---

### Where to Get Help

**Documentation:**
- Setup Guide: `docs/setup-wizard-guide.md`
- Architecture: `docs/ARCHITECTURE.md`
- This Guide: `docs/WRITERS_FACTORY_FIELD_GUIDE.md`

**Debugging:**
- Check logs: `webapp/backend/logs/app.log`
- Session history: `.sessions/`
- Enable debug: `export WRITERS_FACTORY_DEBUG=1`

**Community:**
- GitHub Issues: https://github.com/gcharris/writers-factory-core/issues
- Discussions: (TBD)

---

## Bug Report Template

Use this when you find issues:

```markdown
## Bug Report

**Feature:** [e.g., Setup Wizard - Voice Analysis]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happened]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Result]

**Environment:**
- OS: [Mac/Windows/Linux]
- Python: [version]
- Node: [version]
- Branch: [git branch name]

**Logs:**
```
[Paste relevant logs here]
```

**Files Involved:**
[Which files are related to this bug]

**Workaround:**
[If you found a way to work around it]
```

---

## Conclusion

This guide should help you:
- ✅ Understand what each feature does
- ✅ Know what SHOULD happen (expected behavior)
- ✅ Trace bugs when things go wrong
- ✅ Add new features with confidence

**Remember:** Writers Factory is complex, but each piece has a clear job. When debugging:
1. Identify which component should handle this
2. Check if that component is running
3. Verify its inputs are correct
4. Check its outputs
5. Follow the data flow

**Happy writing!** 🚀✍️
