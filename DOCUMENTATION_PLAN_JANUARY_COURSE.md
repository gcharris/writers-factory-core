# Writers Factory Documentation Plan

**Date**: November 14, 2025
**Purpose**: Document Writers Factory for public GitHub release
**Secondary Use**: January 2025 course materials (separate, external)

---

## Documentation Categories

### Category A: In-Codebase (Public, General)
- **Location**: `writers-factory-core/` repository (GitHub)
- **Audience**: Anyone using Writers Factory
- **Tone**: Professional, timeless, reusable
- **No mention of**: Course, students, January deadlines

### Category B: Course-Specific (Private, Temporary)
- **Location**: Your course materials folder (NOT in repo)
- **Audience**: January 2025 students only
- **Tone**: Course-focused, deadline-driven
- **Includes**: Course schedule, pass/fail criteria, homework

---

## Documentation Status

### ✅ Already Complete (Sprint 8)

Cloud Agent built a **HelpPanel** with searchable help topics:

**Files**:
- `webapp/frontend-v2/src/features/help/HelpPanel.jsx` (119 lines)
- `webapp/frontend-v2/src/features/help/helpContent.js` (144 lines)

**Content Coverage** (6 topics, 20 Q&A pairs):
1. ✅ Getting Started (3 topics)
2. ✅ AI Models (4 topics including Economy Mode, Tournament Mode, Ollama)
3. ✅ Scene Editor (4 topics)
4. ✅ Character Analysis (4 topics)
5. ✅ Cost Tracking (3 topics)
6. ✅ Troubleshooting (4 topics)

**Plus**:
- ✅ 10 rotating quick tips
- ✅ Searchable by keyword
- ✅ Accessible via Help button (press `?` or click icon)

**Status**: **Good foundation**, but needs expansion for TipTap and course-specific workflows.

---

---

# CATEGORY A: In-Codebase Documentation (Public)

## Priority 1: In-App Help Updates (CRITICAL)

### Update Required: TipTap Editor Section

**File to modify**: `webapp/frontend-v2/src/features/help/helpContent.js`

**Current content is outdated** (references "markdown formatting" and "WYSIWYG mode" which Toast UI had):

```js
sceneEditor: {
  title: "Scene Editor",
  icon: "✍️",
  sections: [
    {
      question: "How do I format text?",
      answer: "The scene editor supports markdown formatting. Use **bold**, *italic*, # headers, and more. You can also switch to WYSIWYG mode for visual editing. The toolbar provides formatting buttons."
    },
    // ... other sections ...
  ]
}
```

**Needs to be updated to**:

```js
sceneEditor: {
  title: "Scene Editor",
  icon: "✍️",
  sections: [
    {
      question: "How do I format text?",
      answer: "Use the formatting toolbar at the top of the editor. Click buttons for Bold, Italic, Headings, Lists, and more. Or use keyboard shortcuts: Ctrl+B (bold), Ctrl+I (italic). Your content saves as Markdown automatically."
    },
    {
      question: "What formatting is available?",
      answer: "Text: Bold, Italic, Strike, Code. Structure: Headings (H1-H4), Bullet Lists, Numbered Lists, Task Lists (checkboxes), Blockquotes, Code Blocks, Horizontal Rules. Advanced: Tables, Images (via URL), Links."
    },
    {
      question: "How do I insert tables?",
      answer: "Click the Table button in the toolbar to insert a 3x3 table. Click inside the table to see table-specific options: add/delete rows, add/delete columns, merge cells, delete table."
    },
    {
      question: "How do I add images?",
      answer: "Click the Image button in the toolbar. Enter the image URL (must be accessible online or a data URL). The image will be embedded in your scene and saved in the Markdown."
    },
    {
      question: "Does my work autosave?",
      answer: "Yes! Writers Factory autosaves your scenes every 2 seconds after you stop typing. Look for the 'Last saved' timestamp at the bottom of the editor."
    },
    {
      question: "How do I export my work?",
      answer: "Click the 'Export' button in the scene editor to download your scene as Markdown (.md), Plain Text (.txt), or HTML (.html). You can also export the entire manuscript from the Manuscript menu."
    },
    {
      question: "What is distraction-free mode?",
      answer: "Press F11 or click the Fullscreen button to enter distraction-free mode. This hides all panels and expands the editor to full screen. Press Escape or F11 to exit."
    }
  ]
}
```

**Action**: Cloud Agent should update this as part of Sprint 7 Revision Task 7R-06 (Documentation).

---

### New Topic Required: Creation Wizard Walkthrough

**Currently missing**: Detailed walkthrough of Creation Wizard phases.

**Add to helpContent.js**:

```js
creationWizard: {
  title: "Creation Wizard",
  icon: "🪄",
  sections: [
    {
      question: "What is the Creation Wizard?",
      answer: "The Creation Wizard is a 4-phase guided process to set up your story foundation. It uses AI to help you develop your premise, characters, world, and structure before you start writing scenes."
    },
    {
      question: "Phase 1: Foundation - What goes here?",
      answer: "Enter your story's Title, Genre (fantasy, sci-fi, thriller, etc.), and Premise (1-3 sentence logline). The wizard will analyze your premise and suggest improvements for clarity, conflict, and stakes."
    },
    {
      question: "Phase 2: Characters - What do I need?",
      answer: "Create your Protagonist (hero) and Antagonist (opposing force). For each, define: Name, Role, True Character (inner traits/values/fears), Characterization (external appearance/mannerisms), and Primary Flaw. The wizard checks for dimensional depth."
    },
    {
      question: "Phase 3: World - What's the setting?",
      answer: "Describe your story's World (physical setting, time period, culture). Add Magic/Tech Rules if applicable (how powers work, limitations, costs). The wizard ensures rules are clear and consistent."
    },
    {
      question: "Phase 4: Structure - How do I plan my story?",
      answer: "Choose an Act Structure (3-act, 4-act, 5-act, Hero's Journey, Save the Cat!). The wizard generates a beat-by-beat outline with key turning points. You can customize beats before generating scenes."
    },
    {
      question: "Can I skip phases?",
      answer: "You can exit the wizard at any time, but incomplete setups may result in weaker AI-generated content. It's recommended to complete all 4 phases for best results."
    },
    {
      question: "Can I edit wizard settings later?",
      answer: "Yes! All wizard inputs are saved to your project metadata. You can edit them anytime from the Project Settings panel (click the gear icon in the top toolbar)."
    }
  ]
}
```

---

### New Topic Required: NotebookLM Integration

**Currently missing**: How to use NotebookLM for research.

**Add to helpContent.js**:

```js
notebooklm: {
  title: "NotebookLM Research",
  icon: "📚",
  sections: [
    {
      question: "What is NotebookLM?",
      answer: "NotebookLM is Google's AI research assistant. You can upload sources (PDFs, web pages, notes) to create a knowledge base, then query it for source-grounded answers. Perfect for research-heavy stories."
    },
    {
      question: "How do I set up NotebookLM?",
      answer: "1) Create a notebook at notebooklm.google.com. 2) Upload your research sources (character notes, world-building docs, historical references). 3) Copy the notebook URL. 4) In Writers Factory, click 'NotebookLM Setup' and paste the URL."
    },
    {
      question: "How do I query my notebook?",
      answer: "Click the 'Ask NotebookLM' button (📚 icon) in the toolbar. Type your question (e.g., 'What are the rules of magic in my world?'). NotebookLM will search your sources and provide citations."
    },
    {
      question: "What sources should I upload?",
      answer: "Upload anything relevant to your story: character profiles, world-building notes, historical research, cultural references, technical documentation, previous drafts, craft books, and inspiration documents."
    },
    {
      question: "Does NotebookLM generate scenes?",
      answer: "No. NotebookLM is for research only (source-grounded Q&A). To generate scenes, use the Scene Generator with Claude/GPT models. NotebookLM helps you answer questions before generation."
    }
  ]
}
```

---

### New Topic Required: MCP Tools

**Currently missing**: Explanation of MCP Server tools for advanced users.

**Add to helpContent.js**:

```js
mcpTools: {
  title: "MCP Tools (Advanced)",
  icon: "🔌",
  sections: [
    {
      question: "What is the MCP Server?",
      answer: "MCP (Model Context Protocol) is a protocol that exposes Writers Factory tools to external AI agents (like Claude Desktop, Cursor AI). It allows AI assistants to query your manuscript, analyze characters, check craft, and more."
    },
    {
      question: "What tools are available?",
      answer: "10 tools: query_manuscript (search scenes), list_characters (get character list), analyze_character_depth (check contradictions), analyze_pacing (check beats), get_story_metadata (project info), search_scenes (keyword search), generate_outline (create beats), validate_world_rules (consistency check), calculate_costs (API spending), list_projects (all stories)."
    },
    {
      question: "How do I enable MCP?",
      answer: "The MCP server is automatically available at localhost:8000/mcp when the backend is running. To connect external tools (Claude Desktop, Cursor), configure their MCP settings to point to this URL. See MCP_SERVER_GUIDE.md for details."
    },
    {
      question: "Do I need MCP for the course?",
      answer: "No! MCP is an advanced feature for power users who want to integrate Writers Factory with other AI tools. The Writers Factory UI provides all features needed for the course."
    }
  ]
}
```

---

## Priority 2: Technical Installation Guide (Public, General)

### Document to Create: `README.md` or `INSTALLATION.md`

**Target Audience**: Anyone installing Writers Factory
**Purpose**: Step-by-step setup for Windows, Mac, Linux
**Tone**: Professional, assumes technical literacy
**Location**: Root of `writers-factory-core/` repo

**Outline**:

```markdown
# Writers Factory Installation Guide

## System Requirements
- OS: Windows 10+, macOS 11+, or Linux (Ubuntu 20.04+)
- RAM: 8GB minimum, 16GB recommended
- Disk Space: 10GB (20GB if using Ollama local models)
- Python: 3.9 or higher
- Node.js: 18 or higher
- Internet: Required for cloud AI models (optional for local models)

## Pre-Installation Checklist
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Git installed (`git --version`)
- [ ] 10GB free disk space
- [ ] API keys ready (Claude, OpenAI, or Gemini)

## Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core
```

### Step 2: Install Backend Dependencies
```bash
cd webapp/backend
pip install -r requirements.txt
```

**Troubleshooting**:
- If `pip` not found, try `pip3`
- On Windows, use `py -m pip install -r requirements.txt`
- On Linux, you may need `sudo apt install python3-pip`

### Step 3: Install Frontend Dependencies
```bash
cd ../frontend-v2
npm install
```

**Troubleshooting**:
- If `npm install` fails with peer dependency errors, try `npm install --legacy-peer-deps`
- If Node.js version too old, upgrade: https://nodejs.org

### Step 4: Configure API Keys
Create a file `webapp/backend/.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-key-here
```

**Getting API Keys**:
- Anthropic (Claude): https://console.anthropic.com/settings/keys
- OpenAI (GPT): https://platform.openai.com/api-keys
- Google (Gemini): https://aistudio.google.com/app/apikey

**Note**: You only need ONE API key to start. Claude recommended for best prose.

### Step 5: Start Backend Server
```bash
cd webapp/backend
python simple_app.py
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Troubleshooting**:
- If port 8000 in use: `lsof -ti:8000 | xargs kill` (Mac/Linux) or use Task Manager (Windows)
- If Python modules missing: `pip install -r requirements.txt`

### Step 6: Start Frontend Dev Server
Open a **new terminal**:
```bash
cd webapp/frontend-v2
npm run dev
```

**Expected Output**:
```
VITE v5.x.x  ready in 523 ms

➜  Local:   http://localhost:5173/
```

### Step 7: Open Writers Factory
Open your browser and navigate to:
```
http://localhost:5173
```

**Expected**: Welcome modal with "Get Started" button.

## Optional: Install Ollama (Free Local Models)

### Why Ollama?
- 100% free AI generation (no API costs)
- Works offline
- Fast on modern hardware
- 90%+ cost savings

### Installation
1. Download from https://ollama.ai
2. Install (Mac/Windows/Linux)
3. Open terminal and run:
   ```bash
   ollama pull llama3
   ```
4. Restart Writers Factory backend
5. Look for green "Ollama Running" banner

### Recommended Models
- `ollama pull llama3` - Best general model (4.7GB)
- `ollama pull qwen2.5:14b` - Strong for fiction (8.7GB)
- `ollama pull deepseek-coder-v2` - Technical writing (8.9GB)

## Verification Checklist

After installation, verify everything works:

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] Welcome modal appears
- [ ] Can create new project
- [ ] Can open Creation Wizard
- [ ] Can select AI model (cloud or local)
- [ ] Can write in scene editor
- [ ] Autosave works (check "Last saved" timestamp)
- [ ] Can export scene (MD/TXT/HTML)
- [ ] Help panel opens (press `?`)

## Troubleshooting Common Issues

### "Backend not responding"
**Symptom**: Frontend loads but no data appears, console shows network errors
**Fix**: Make sure backend is running (`python simple_app.py` in `webapp/backend`)

### "API key invalid"
**Symptom**: AI generation fails with "Invalid API key" error
**Fix**: Check `.env` file has correct keys, restart backend after changing

### "Ollama models not showing"
**Symptom**: Economy Mode available but no local models in dropdown
**Fix**:
1. Check Ollama running: `ollama list` in terminal
2. Make sure you pulled models: `ollama pull llama3`
3. Restart backend

### "Frontend won't build"
**Symptom**: `npm run dev` fails with errors
**Fix**:
1. Delete `node_modules`: `rm -rf node_modules`
2. Reinstall: `npm install --legacy-peer-deps`
3. Try again: `npm run dev`

### "Port already in use"
**Symptom**: Backend won't start, says port 8000 in use
**Fix**:
- Mac/Linux: `lsof -ti:8000 | xargs kill`
- Windows: Open Task Manager, end process using port 8000

## Getting Help

**During Course**:
- Ask instructor or TA for hands-on help
- Check Help panel in Writers Factory (press `?`)
- See `TROUBLESHOOTING.md` for detailed debugging

**After Course**:
- GitHub Issues: https://github.com/gcharris/writers-factory-core/issues
- Documentation: See `factory/docs/` folder
```

---

## Priority 3: Quick Reference Cards (For classroom)

### Document to Create: `QUICK_REFERENCE_CARD.md`

**Format**: Printable 1-page cheat sheet

**Content**:

```markdown
# Writers Factory Quick Reference Card

## Keyboard Shortcuts
- `Ctrl+B` - Bold
- `Ctrl+I` - Italic
- `Ctrl+Z` - Undo
- `Ctrl+Shift+Z` - Redo
- `F11` - Distraction-free mode
- `?` - Open help
- `Ctrl+S` - Save (automatic, but forces immediate save)

## Toolbar Icons
- 🏠 Home - Return to Brainstorm
- 🪄 Creation Wizard - New story setup
- 👥 Characters - Character panel
- 📖 Manuscript - Full manuscript view
- 📚 NotebookLM - Research assistant
- 💰 Costs - API spending tracker
- ⚙️ Settings - API keys, preferences
- ❓ Help - Searchable help topics

## Creation Wizard Phases
1. **Foundation** - Title, Genre, Premise
2. **Characters** - Protagonist, Antagonist (True Character vs Characterization)
3. **World** - Setting, Magic/Tech Rules
4. **Structure** - Act structure, Beat outline

## AI Model Selection
- **Claude Sonnet** - Best prose, natural dialogue ($$)
- **GPT-4** - Strong plot, consistent logic ($$$)
- **Gemini** - Fast, affordable, good for drafts ($)
- **Ollama (local)** - FREE, works offline, good for first drafts

## Economy Mode
- Toggle in toolbar (💰 → green)
- Automatically uses local models when available
- Can save 90%+ on costs

## Scene Editor Features
- **Formatting**: Bold, italic, headings, lists, blockquotes
- **Structure**: Tables, images (URL), links, code blocks, horizontal rules
- **Tasks**: Checkbox lists (for outlines)
- **Autosave**: Every 2 seconds (see "Last saved" timestamp)
- **Export**: MD, TXT, HTML

## Character Depth Scoring
- **0-50**: Flat character (needs contradictions)
- **50-80**: Developing character (add flaw depth)
- **80-100**: Dimensional character (professional quality)

**Checks**:
1. External Contradiction (True Character ≠ Characterization)
2. Internal Contradiction (opposing traits)
3. Flaw Depth (not surface-level)
4. Values vs Fears (clear motivation)
5. Consistency (appearance, speech patterns)

## Export Formats
- **Markdown (.md)** - Preserves formatting, portable
- **Plain Text (.txt)** - Universal compatibility
- **HTML (.html)** - For web viewing, print preview

## Cost Optimization Tips
1. Enable Economy Mode (use local models)
2. Use local models for first drafts
3. Use cloud models for final polish
4. Avoid Tournament Mode (4x cost) unless comparing models
5. Check Cost Dashboard regularly (💰 icon)

## Troubleshooting Quick Fixes
- **Scene won't save** - Check "Last saved" timestamp, refresh page
- **AI generation failed** - Verify API key in Settings
- **Ollama not showing** - Make sure Ollama running (`ollama list` in terminal)
- **Backend not responding** - Restart backend (`python simple_app.py`)

## Getting Help
1. Press `?` for searchable help
2. Check Help Panel topics (6 categories, 20+ Q&As)
3. Ask instructor/TA during course
4. See `TROUBLESHOOTING.md` for detailed debugging
```

---

## Priority 4: Course-Specific Documents

### Document to Create: `COURSE_STUDENT_GUIDE.md`

**Target Audience**: January 2025 students
**Purpose**: Course workflow, day-by-day expectations

**Outline**:

```markdown
# Writers Factory - Course Student Guide
## "AI and the One-Week Novel" - January 2025

### Course Overview
- **Duration**: 5 days (Monday-Friday)
- **Goal**: Complete first draft of a novel (50,000+ words)
- **Method**: AI-assisted writing with Writers Factory
- **Format**: Hands-on intensive with instructor support

### Pre-Course Setup (48 hours before Day 1)
- [ ] Install Writers Factory (see `INSTALLATION_GUIDE.md`)
- [ ] Verify installation (run verification checklist)
- [ ] Get at least ONE API key (Claude recommended)
- [ ] Optional: Install Ollama for free local generation
- [ ] Bring story idea (genre, premise, characters - can be rough!)

### Day-by-Day Workflow

#### Day 1: Foundation & Planning (Monday)
**Morning**:
- [ ] Complete Creation Wizard Phase 1 (Foundation)
- [ ] Complete Creation Wizard Phase 2 (Characters)
- [ ] Run Character Analysis (target: 60+ depth score)

**Afternoon**:
- [ ] Complete Creation Wizard Phase 3 (World)
- [ ] Complete Creation Wizard Phase 4 (Structure)
- [ ] Review generated beat outline
- [ ] Customize beats if needed

**Homework**:
- [ ] Refine character contradictions (target: 80+ depth score)
- [ ] Add 2-3 more characters (supporting cast)

#### Day 2: Act 1 Writing (Tuesday)
**Morning**:
- [ ] Generate opening scene (Beat 1)
- [ ] Edit for voice consistency
- [ ] Generate scenes 2-5 (inciting incident, first turning point)

**Afternoon**:
- [ ] Continue Act 1 scenes (beats 6-10)
- [ ] Run pacing analysis (check beat alignment)
- [ ] Export Act 1 draft

**Homework**:
- [ ] Read Act 1 aloud (mark awkward passages)
- [ ] Polish 2-3 key scenes

#### Day 3: Act 2 Part 1 (Wednesday)
**Morning**:
- [ ] Generate midpoint buildup (beats 11-15)
- [ ] Check character depth (recurring flaws, contradictions)

**Afternoon**:
- [ ] Generate midpoint scene (beat 16 - major reversal)
- [ ] Continue Act 2 (beats 17-20)
- [ ] Run character consistency check

**Homework**:
- [ ] Review midpoint impact (does it change everything?)
- [ ] Identify weak scenes (mark for revision)

#### Day 4: Act 2 Part 2 & Act 3 Start (Thursday)
**Morning**:
- [ ] Complete Act 2 (beats 21-25)
- [ ] Generate dark night / all is lost scene
- [ ] Check pacing (should feel urgent)

**Afternoon**:
- [ ] Start Act 3 (beats 26-30)
- [ ] Generate climax preparation scenes
- [ ] Run full manuscript analysis

**Homework**:
- [ ] Polish climax outline (this is your payoff!)
- [ ] Ensure all character arcs resolve

#### Day 5: Climax & Resolution (Friday)
**Morning**:
- [ ] Generate climax scene (beat 31-32)
- [ ] Edit for maximum impact
- [ ] Generate resolution scenes (beats 33-35)

**Afternoon**:
- [ ] Complete final scenes
- [ ] Run full character arc check
- [ ] Export complete manuscript (MD, TXT, HTML)
- [ ] Celebrate! 🎉

**Final Deliverable**:
- [ ] Export manuscript as Markdown
- [ ] Export character profiles
- [ ] Export beat outline
- [ ] Submit all to instructor

### Daily Targets
- **Word Count**: 10,000 words/day (50,000 total)
- **Scenes**: 6-8 scenes/day (30-40 total)
- **Time**: 6-8 hours/day (breaks included)

### Tools You'll Use Daily
1. **Creation Wizard** - Day 1 only (setup)
2. **Scene Editor** - Every day (writing/editing)
3. **Character Panel** - Day 1, 3, 5 (analysis)
4. **Cost Dashboard** - Every day (track spending)
5. **Export** - Day 2, 5 (backups + final)

### Cost Management
- **Budget**: $20-50 total (with Economy Mode)
- **Strategy**:
  - Use Ollama for first drafts (FREE)
  - Use Claude for final polish ($$)
  - Avoid Tournament Mode (4x cost)
- **Check costs**: Click 💰 icon daily

### Tips for Success
1. **Don't over-edit** - First drafts are supposed to be rough!
2. **Trust the process** - Follow the beat structure
3. **Use Economy Mode** - Save 90% on costs
4. **Take breaks** - 10 min every hour (prevents burnout)
5. **Ask for help** - Instructors and TAs are here for you
6. **Backup daily** - Export manuscript at end of each day
7. **Read aloud** - Best way to catch awkward phrasing
8. **Embrace imperfection** - Done is better than perfect

### Pass/Fail Criteria
**To pass, you must complete 4 of 6**:
1. ✅ Complete first draft (50,000+ words)
2. ✅ Follow beat structure (30+ scenes)
3. ✅ Dimensional protagonist (80+ depth score)
4. ✅ Consistent world rules (if applicable)
5. ✅ Complete character arcs (protagonist changes)
6. ✅ Export final manuscript (MD + character profiles)

### Technical Support
- **During class**: Ask instructor or TA
- **Help Panel**: Press `?` in Writers Factory
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Installation issues**: See `INSTALLATION_GUIDE.md`

### After the Course
- **Continue writing**: You keep Writers Factory forever (open source)
- **Polish draft**: Use revision passes (see `REVISION_GUIDE.md`)
- **Join community**: GitHub discussions for ongoing support
- **Share feedback**: Help improve Writers Factory for future students

### Questions?
Ask during class or check the Help Panel (press `?`). Good luck! 🚀
```

---

## Priority 5: Troubleshooting Guide

### Document to Create: `TROUBLESHOOTING.md`

**Target Audience**: Students + instructors
**Purpose**: Detailed debugging for common issues

**Outline**:

```markdown
# Writers Factory Troubleshooting Guide

## Installation Issues

### Python not found
**Symptom**: `python: command not found` or `python is not recognized`
**Cause**: Python not installed or not in PATH
**Fix**:
1. Install Python 3.9+ from python.org
2. During install, check "Add Python to PATH"
3. Restart terminal
4. Verify: `python --version` (should show 3.9+)

**Alternative**: Try `python3 --version` (Mac/Linux may require `python3`)

### Node.js version too old
**Symptom**: `npm install` fails with "Node.js 18+ required"
**Cause**: Node.js outdated
**Fix**:
1. Check version: `node --version`
2. If < 18, download from nodejs.org
3. Install latest LTS version
4. Restart terminal
5. Verify: `node --version` (should show 18+)

### pip install fails with permissions error
**Symptom**: `ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied`
**Cause**: Trying to install system-wide without permissions
**Fix**:
- **Option 1** (recommended): Use virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate     # Windows
  pip install -r requirements.txt
  ```
- **Option 2**: Install user-local
  ```bash
  pip install --user -r requirements.txt
  ```
- **Option 3**: Use sudo (Linux only, not recommended)
  ```bash
  sudo pip install -r requirements.txt
  ```

### npm install fails with peer dependency errors
**Symptom**: `npm ERR! ERESOLVE unable to resolve dependency tree`
**Cause**: Conflicting package versions
**Fix**:
```bash
npm install --legacy-peer-deps
```

### Git clone fails with authentication error
**Symptom**: `fatal: Authentication failed`
**Cause**: Private repository or SSH key not configured
**Fix**:
1. Make sure repository is public (or you have access)
2. Use HTTPS URL: `https://github.com/gcharris/writers-factory-core.git`
3. If still fails, configure GitHub credentials

---

## Runtime Issues

### Backend won't start - Port 8000 in use
**Symptom**: `Error: [Errno 48] Address already in use` or `OSError: [Errno 98] Address already in use`
**Cause**: Another process using port 8000
**Fix**:

**Mac/Linux**:
```bash
lsof -ti:8000 | xargs kill
```

**Windows**:
1. Open Command Prompt as Admin
2. Find process: `netstat -ano | findstr :8000`
3. Note PID (last column)
4. Kill process: `taskkill /PID <number> /F`

**Alternative**: Change port in `simple_app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```
Then update frontend to use `http://localhost:8001`

### Backend starts but crashes immediately
**Symptom**: Backend terminal shows error and exits
**Cause**: Missing dependencies or Python error
**Fix**:
1. Read error message carefully (usually tells you what's wrong)
2. If "ModuleNotFoundError": `pip install <module_name>`
3. If API key error: Check `.env` file exists and has keys
4. If database error: Delete `webapp/backend/data/` and restart

### Frontend shows "Network Error" or "Failed to fetch"
**Symptom**: Frontend loads but no data, console shows network errors
**Cause**: Backend not running or CORS issue
**Fix**:
1. Verify backend running at http://localhost:8000
2. Open http://localhost:8000/docs in browser (should show API docs)
3. If backend running but still failing, check firewall/antivirus
4. Restart both backend and frontend

### API key invalid error
**Symptom**: "Invalid API key" or "Authentication failed" when generating
**Cause**: API key missing, wrong, or expired
**Fix**:
1. Check `.env` file in `webapp/backend/`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   OPENAI_API_KEY=sk-your-key-here
   GOOGLE_API_KEY=your-key-here
   ```
2. Verify key format (starts with `sk-ant-` for Claude, `sk-` for OpenAI)
3. Test key at provider's website (console.anthropic.com, platform.openai.com)
4. Restart backend after changing `.env`

---

## Feature Issues

### Ollama models not showing in dropdown
**Symptom**: Economy Mode available but no local models listed
**Cause**: Ollama not running or no models pulled
**Fix**:
1. Check Ollama running: `ollama list` (should show installed models)
2. If "command not found": Install Ollama from ollama.ai
3. If no models listed: Pull a model
   ```bash
   ollama pull llama3
   ```
4. Restart Writers Factory backend
5. Look for green "Ollama Running" banner at top

### Scene doesn't save / autosave not working
**Symptom**: "Last saved" timestamp says "Never" or old time
**Cause**: Backend connection lost or error
**Fix**:
1. Check backend still running (terminal should show activity)
2. Check browser console for errors (F12 → Console tab)
3. Try manual save: Ctrl+S
4. Refresh page (changes may be lost if not saved)
5. Restart backend if necessary

### Character depth score always 0 or error
**Symptom**: Character Panel shows score 0 or "Analysis failed"
**Cause**: Character data incomplete or backend error
**Fix**:
1. Make sure character has:
   - Name (required)
   - True Character (at least 2 traits)
   - Characterization (at least 2 observable traits)
   - Primary Flaw (required)
2. Check backend terminal for errors
3. Try refreshing Character Panel

### Export fails or downloads empty file
**Symptom**: Export button clicks but no download, or file is empty
**Cause**: Browser blocked download or scene has no content
**Fix**:
1. Check scene has content (not empty)
2. Check browser download settings (may block automatic downloads)
3. Try different export format (MD → TXT → HTML)
4. Check browser console for errors (F12)

### AI generation fails with timeout error
**Symptom**: "Generation timed out" or "Request took too long"
**Cause**: Model too slow, poor internet, or model overloaded
**Fix**:
1. Try again (temporary issue)
2. Use faster model (Claude Haiku, GPT-3.5, Gemini Flash)
3. Shorten prompt/context
4. If using Ollama: Check system resources (CPU/RAM usage)
5. Check internet connection (for cloud models)

### Creation Wizard stuck or won't advance
**Symptom**: "Next" button disabled or greyed out
**Cause**: Required fields empty
**Fix**:
1. Check all required fields filled:
   - Phase 1: Title, Genre, Premise
   - Phase 2: At least Protagonist name + traits
   - Phase 3: World description
   - Phase 4: Select act structure
2. Look for red validation messages
3. If stuck, click "Save & Exit" and re-enter wizard

---

## Performance Issues

### Editor is slow / laggy when typing
**Symptom**: Noticeable delay between keypress and character appearing
**Cause**: Large scene content or browser resources exhausted
**Fix**:
1. Close unused browser tabs
2. Restart browser
3. Split large scenes into smaller scenes (< 5,000 words/scene)
4. Disable browser extensions (some conflict with editors)
5. Check system resources (Activity Monitor/Task Manager)

### AI generation is very slow (> 2 min)
**Symptom**: Generation starts but takes forever
**Cause**: Model overloaded, poor internet, or large context
**Fix**:
1. Use faster model (Claude Haiku, Gemini Flash)
2. Reduce context (fewer characters, shorter beats)
3. Check internet speed (speedtest.net)
4. Try different time of day (API providers can be busy)
5. If Ollama: Check CPU/RAM usage, may need better hardware

### Frontend build/dev server slow to start
**Symptom**: `npm run dev` takes > 30 seconds
**Cause**: Many dependencies, node_modules bloat
**Fix**:
1. Normal for first run (installs dependencies)
2. Subsequent runs should be faster (< 5 sec)
3. If consistently slow, try:
   ```bash
   rm -rf node_modules .vite
   npm install
   npm run dev
   ```

---

## Data Issues

### Lost my work / scenes disappeared
**Symptom**: Scenes or project missing after restart
**Cause**: Data not saved or database corruption
**Prevention**:
1. Always export backups daily (MD format)
2. Check "Last saved" timestamp before closing
3. Don't force-quit browser/backend during save

**Recovery**:
1. Check `webapp/backend/data/` folder for JSON files
2. If project exists but scenes missing, check backend logs for errors
3. Restore from backup exports if available
4. If data corrupted, delete `data/` folder and start fresh (loses everything)

### Can't delete project / scenes
**Symptom**: Delete button doesn't work or project reappears
**Cause**: Backend permission issue or active references
**Fix**:
1. Close all open scenes
2. Refresh page
3. Try delete again
4. If still fails, manually delete from `webapp/backend/data/`

### Character Panel shows outdated data
**Symptom**: Changed character traits but panel shows old analysis
**Cause**: Cache not refreshed
**Fix**:
1. Click "Refresh Analysis" button
2. If no button, close and reopen Character Panel
3. If still stale, refresh page (F5)

---

## Course-Specific Issues

### Can't complete 10,000 words/day (falling behind)
**Symptom**: Only hitting 5,000-7,000 words/day
**Cause**: Over-editing, slow generation, or complex scenes
**Fix**:
1. Use Economy Mode (local models faster)
2. Stop editing during drafting phase (edit later)
3. Use simpler beats (fewer characters, shorter scenes)
4. Ask instructor for help (may need to adjust scope)
5. Focus on completing draft, not perfection

### Cost exceeding budget ($50+)
**Symptom**: Cost Dashboard shows high spending
**Cause**: Not using Economy Mode, using expensive models, Tournament Mode
**Fix**:
1. Enable Economy Mode (💰 → green)
2. Switch to local Ollama models (FREE)
3. Use cheaper cloud models (Claude Haiku, GPT-3.5, Gemini Flash)
4. Avoid Tournament Mode (4x cost)
5. Generate fewer variations (don't re-generate same scene 10 times)

### Installation failed, course starting tomorrow
**Symptom**: Can't get Writers Factory working
**Cause**: Technical issues, missing dependencies
**Fix**:
1. Ask instructor ASAP for help
2. Use backup classroom machine (pre-configured)
3. Pair with classmate temporarily
4. Instructor may provide cloud instance (backup plan)

---

## Getting More Help

### During Course
- Ask instructor or TA (hands-on help available)
- Check Help Panel in Writers Factory (press `?`)
- Pair with classmate (two heads better than one)

### After Course
- GitHub Issues: https://github.com/gcharris/writers-factory-core/issues
- Documentation: `factory/docs/` folder
- Community: GitHub Discussions

### Debugging Steps (General)
1. Read error message carefully (usually tells you what's wrong)
2. Check backend terminal for errors
3. Check browser console (F12 → Console tab)
4. Try refreshing page (F5)
5. Try restarting backend
6. Try restarting browser
7. Check system resources (CPU/RAM/disk)
8. Search error message online (Stack Overflow, GitHub)
9. Ask for help (provide full error message + steps to reproduce)

---

**Last Updated**: November 14, 2025
**For**: "AI and the One-Week Novel" January 2025 Course
```

---

## Implementation Timeline

### Immediate (After Sprint 7 Revision Complete)
1. **Cloud Agent**: Update `helpContent.js` with TipTap editor section (Task 7R-06)
2. **Cloud Agent**: Add Creation Wizard, NotebookLM, MCP topics to `helpContent.js`

### Week of November 18-22
3. **Me** (Claude Code): Create `INSTALLATION_GUIDE.md`
4. **Me** (Claude Code): Create `TROUBLESHOOTING.md`
5. **Me** (Claude Code): Create `QUICK_REFERENCE_CARD.md`
6. **Me** (Claude Code): Create `COURSE_STUDENT_GUIDE.md`

### Week of November 25-29
7. **Test documentation**: Have someone outside project follow installation guide
8. **Revise based on feedback**: Fix unclear steps
9. **Print reference cards**: PDF for classroom handouts

### Week of December 2-6
10. **Create video walkthrough**: Screen recording of installation (optional but helpful)
11. **Prepare backup materials**: USB drives with installers, pre-configured VMs

---

## Summary

### What We Have ✅
- HelpPanel with 6 topics (20 Q&As)
- Quick tips (10 rotating tips)
- Searchable help interface

### What We Need 📝
1. **Update existing help** (TipTap editor section) - Cloud Agent, Sprint 7R-06
2. **Add new help topics** (Creation Wizard, NotebookLM, MCP) - Cloud Agent or me
3. **Installation guide** - Me (Claude Code), 1-2 hours
4. **Troubleshooting guide** - Me (Claude Code), 2-3 hours
5. **Quick reference card** - Me (Claude Code), 1 hour
6. **Course student guide** - Me (Claude Code), 2 hours

**Total Effort**: ~8-10 hours of documentation writing (me + Cloud Agent)
**Timeline**: Complete by end of November (1 month before course)

---

**Priority Order**:
1. 🔴 Sprint 7 Revision (TipTap) - **CRITICAL, blocks everything**
2. 🔴 Update help content for TipTap - **Part of Sprint 7R-06**
3. 🟡 Installation guide - **Important for pre-course setup**
4. 🟡 Troubleshooting guide - **Important for course support**
5. 🟢 Quick reference card - **Nice to have, printable**
6. 🟢 Course student guide - **Nice to have, sets expectations**

---

**Next Step**: After Cloud Agent completes Sprint 7 Revision, I'll create the installation and troubleshooting guides.
