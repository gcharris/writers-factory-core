# Writers Factory Documentation Plan

**Date**: November 14, 2025
**Purpose**: Document Writers Factory for public GitHub release
**Timeline**: Complete by mid-December 2025

---

## Documentation Philosophy

**Two Separate Tracks**:

### Track A: Repository Documentation (Public, Permanent)
- **Location**: `writers-factory-core/` GitHub repository
- **Audience**: Anyone using Writers Factory
- **Tone**: Professional, technical, timeless
- **Format**: Markdown files, in-app help
- **No mention of**: Specific courses, deadlines, pass/fail criteria

### Track B: Course Materials (Private, Temporary)
- **Location**: Separate course materials folder (NOT in repo)
- **Audience**: Specific course students
- **Tone**: Educational, deadline-driven
- **Format**: PDFs, slides, handouts
- **Includes**: Course schedule, homework, grading rubrics

**This document covers Track A only** (repository documentation).

---

## Current Status

### ✅ Already Complete (Sprint 8)

**In-App Help System**:
- `webapp/frontend-v2/src/features/help/HelpPanel.jsx` (119 lines)
- `webapp/frontend-v2/src/features/help/helpContent.js` (144 lines)

**Content Coverage** (6 topics, 20 Q&A pairs):
1. Getting Started (3 Q&As)
2. AI Models (4 Q&As - Economy Mode, Tournament Mode, Ollama)
3. Scene Editor (4 Q&As)
4. Character Analysis (4 Q&As)
5. Cost Tracking (3 Q&As)
6. Troubleshooting (4 Q&As)

**Plus**: 10 rotating quick tips, keyword search

**Status**: Good foundation, needs TipTap updates + new topics

---

## Priority 1: Update In-App Help for TipTap (CRITICAL)

### Task: Update Scene Editor Help Content

**File**: `webapp/frontend-v2/src/features/help/helpContent.js`

**Current problem**: Help references Toast UI features (markdown syntax, WYSIWYG mode toggle)

**Solution**: Update to reflect TipTap toolbar-based editing

**Updated content**:

```javascript
sceneEditor: {
  title: "Scene Editor",
  icon: "✍️",
  sections: [
    {
      question: "How do I format text?",
      answer: "Use the formatting toolbar at the top of the editor. Click buttons for Bold, Italic, Headings, Lists, and more. Keyboard shortcuts work too: Ctrl+B (bold), Ctrl+I (italic), Ctrl+Z (undo)."
    },
    {
      question: "What formatting options are available?",
      answer: "Text: Bold, Italic, Strike, Code. Structure: Headings (H1-H4), Bullet Lists, Numbered Lists, Task Lists, Blockquotes, Code Blocks, Horizontal Rules. Advanced: Tables, Images (URL), Links."
    },
    {
      question: "How do I insert tables?",
      answer: "Click the Table button in the toolbar to insert a 3x3 table. Right-click or use the context menu to add/delete rows and columns, merge cells, or delete the table."
    },
    {
      question: "How do I add images?",
      answer: "Click the Image button in the toolbar and enter an image URL. The image will be embedded in your scene. Supports public URLs or data URLs for local images."
    },
    {
      question: "Does my work autosave?",
      answer: "Yes! Your scenes autosave every 2 seconds after you stop typing. Check the 'Last saved' timestamp at the bottom of the editor to verify."
    },
    {
      question: "How do I export my work?",
      answer: "Click the Export button to download your scene as Markdown (.md), Plain Text (.txt), or HTML (.html). Markdown format preserves all formatting and is portable to other editors."
    },
    {
      question: "What keyboard shortcuts are available?",
      answer: "Ctrl+B (bold), Ctrl+I (italic), Ctrl+Z (undo), Ctrl+Shift+Z (redo), F11 (fullscreen), Escape (exit fullscreen). Standard text editing shortcuts also work (Ctrl+A, Ctrl+C, Ctrl+V)."
    }
  ]
}
```

**Implementation**: Cloud Agent should update this as part of Sprint 7 Revision Task 7R-06.

---

## Priority 2: Add New Help Topics

### Topic 1: Creation Wizard

**Add to helpContent.js**:

```javascript
creationWizard: {
  title: "Creation Wizard",
  icon: "🪄",
  sections: [
    {
      question: "What is the Creation Wizard?",
      answer: "The Creation Wizard guides you through setting up a new story in 4 phases: Foundation (premise), Characters (protagonist/antagonist), World (setting/rules), and Structure (act outline). It uses AI to help develop your story foundation."
    },
    {
      question: "Phase 1: Foundation",
      answer: "Enter your story Title, Genre, and Premise (1-3 sentence summary). The AI analyzes your premise for clarity, conflict, and stakes, suggesting improvements."
    },
    {
      question: "Phase 2: Characters",
      answer: "Create Protagonist and Antagonist. For each character, define: Name, Role, True Character (inner traits/values/fears), Characterization (external appearance/behavior), and Primary Flaw. The wizard checks for dimensional depth."
    },
    {
      question: "Phase 3: World",
      answer: "Describe your story's setting (time, place, culture). If applicable, add Magic/Tech Rules (how special abilities work, limitations, costs). The wizard ensures rules are clear and consistent."
    },
    {
      question: "Phase 4: Structure",
      answer: "Choose an act structure (3-act, Hero's Journey, Save the Cat!, etc.). The wizard generates a beat-by-beat outline with key turning points. You can customize beats before generating scenes."
    },
    {
      question: "Can I skip phases?",
      answer: "You can exit anytime by clicking 'Save & Exit'. Incomplete setups work but may produce less focused AI-generated content. Completing all 4 phases gives best results."
    }
  ]
}
```

### Topic 2: NotebookLM Integration

**Add to helpContent.js**:

```javascript
notebooklm: {
  title: "NotebookLM Research",
  icon: "📚",
  sections: [
    {
      question: "What is NotebookLM?",
      answer: "NotebookLM is Google's AI research assistant. Upload sources (PDFs, notes, web pages) to create a knowledge base, then ask questions. It provides source-grounded answers with citations—perfect for research-heavy stories."
    },
    {
      question: "How do I set up NotebookLM?",
      answer: "1) Create a notebook at notebooklm.google.com 2) Upload your research sources 3) Copy the notebook URL 4) In Writers Factory, click 'NotebookLM Setup' on the Brainstorm page and paste the URL."
    },
    {
      question: "How do I query my notebook?",
      answer: "Click the 'Ask NotebookLM' button (📚 icon) in the toolbar or from the Brainstorm page. Type your question (e.g., 'What are the rules of magic in my world?'). NotebookLM searches your sources and provides citations."
    },
    {
      question: "What sources should I upload?",
      answer: "Upload anything relevant: character profiles, world-building docs, historical research, technical references, previous drafts, craft books, or inspiration materials. NotebookLM works best with 5-20 focused sources."
    },
    {
      question: "Does NotebookLM generate scenes?",
      answer: "No. NotebookLM is for research and Q&A only. To generate scenes, use the Scene Generator with cloud AI models (Claude, GPT, Gemini) or local Ollama models."
    }
  ]
}
```

### Topic 3: MCP Tools (Advanced)

**Add to helpContent.js**:

```javascript
mcpTools: {
  title: "MCP Tools (Advanced)",
  icon: "🔌",
  sections: [
    {
      question: "What is the MCP Server?",
      answer: "MCP (Model Context Protocol) exposes Writers Factory tools to external AI agents like Claude Desktop or Cursor AI. This allows AI assistants to query your manuscript, analyze characters, check craft, and more through a standardized protocol."
    },
    {
      question: "What tools are available?",
      answer: "10 tools: query_manuscript, list_characters, analyze_character_depth, analyze_pacing, get_story_metadata, search_scenes, generate_outline, validate_world_rules, calculate_costs, list_projects. See factory/mcp/README.md for full API reference."
    },
    {
      question: "How do I enable MCP?",
      answer: "The MCP server runs automatically at localhost:8000/mcp when the backend starts. To connect external tools, configure their MCP settings to point to this endpoint. See factory/mcp/MCP_SETUP_GUIDE.md for instructions."
    },
    {
      question: "Do I need MCP?",
      answer: "No. MCP is an advanced feature for power users who want to integrate Writers Factory with external AI tools. All features are available in the Writers Factory UI."
    }
  ]
}
```

---

## Priority 3: Installation Guide

### Document: `README.md` (Root of repository)

**Purpose**: Quick start guide for new users
**Audience**: Developers and technical writers
**Tone**: Professional, concise

**Content**:

```markdown
# Writers Factory

AI-assisted novel writing tool with dimensional character analysis, multi-model support, and craft-based story structure.

## Features

- **Creation Wizard**: 4-phase guided story setup (premise, characters, world, structure)
- **Character Analysis**: Dimensional depth scoring based on professional craft principles
- **Multi-Model Support**: Claude, GPT-4, Gemini, Qwen, DeepSeek, and local Ollama models
- **Economy Mode**: Automatically prefer free local models (90%+ cost savings)
- **Tournament Mode**: Compare 4 models side-by-side
- **Rich Text Editor**: TipTap-based WYSIWYM editor with Markdown storage
- **NotebookLM Integration**: Source-grounded research for world-building
- **MCP Protocol**: Connect external AI agents to your manuscript
- **Cost Tracking**: Real-time API spending dashboard

## Quick Start

### Prerequisites

- Python 3.9+ (`python --version`)
- Node.js 18+ (`node --version`)
- Git
- At least one AI API key (see API Keys section)

### Installation

```bash
# Clone repository
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core

# Install backend dependencies
cd webapp/backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend-v2
npm install

# Configure API keys (see next section)
```

### API Keys

Create `webapp/backend/.env`:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-key-here
```

Get keys:
- **Anthropic (Claude)**: https://console.anthropic.com/settings/keys
- **OpenAI (GPT)**: https://platform.openai.com/api-keys
- **Google (Gemini)**: https://aistudio.google.com/app/apikey

**Note**: You only need ONE API key to start. Claude recommended for prose.

### Running

**Terminal 1** (Backend):
```bash
cd webapp/backend
python simple_app.py
```

**Terminal 2** (Frontend):
```bash
cd webapp/frontend-v2
npm run dev
```

**Open**: http://localhost:5173

### Optional: Local Models (Free)

Install Ollama for unlimited free AI generation:

1. Download from https://ollama.ai
2. Install and run:
   ```bash
   ollama pull llama3
   ```
3. Restart backend - local models will appear automatically

## Usage

1. **Start Creation Wizard**: Click "Start Creation Wizard" on Brainstorm page
2. **Complete 4 Phases**: Foundation → Characters → World → Structure
3. **Generate Scenes**: Select beats from outline, click "Generate Scene"
4. **Edit & Polish**: Use TipTap editor with formatting toolbar
5. **Analyze Characters**: Open Character Panel to check depth (target: 80+)
6. **Export**: Download as Markdown, TXT, or HTML

## Project Structure

```
writers-factory-core/
├── webapp/
│   ├── backend/          # Flask/FastAPI backend
│   │   ├── simple_app.py # Main server
│   │   └── ...
│   └── frontend-v2/      # React frontend
│       ├── src/
│       │   ├── features/ # Feature components
│       │   └── ...
│       └── package.json
├── factory/
│   ├── agents/           # AI agent implementations
│   ├── mcp/              # MCP server
│   └── docs/             # Documentation
└── README.md
```

## Documentation

- **In-App Help**: Press `?` or click Help icon
- **MCP Server**: See `factory/mcp/README.md`
- **Character Analysis**: See `factory/docs/CHARACTER_DEPTH_GUIDE.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`

## Architecture

- **Frontend**: React 19 + Vite + TailwindCSS
- **Backend**: Python FastAPI + SQLite
- **Editor**: TipTap (ProseMirror) with Markdown storage
- **AI**: Multi-provider (Anthropic, OpenAI, Google, Ollama)
- **Protocol**: MCP (Model Context Protocol) for external integration

## Cost Optimization

- **Enable Economy Mode**: Toolbar → 💰 (turns green)
- **Use Local Models**: Install Ollama (100% free)
- **Choose Cheaper Models**: Claude Haiku, GPT-3.5, Gemini Flash
- **Track Spending**: Click Cost icon to see real-time breakdown

## Contributing

See `CONTRIBUTING.md` for development guidelines.

## License

MIT

## Support

- **GitHub Issues**: https://github.com/gcharris/writers-factory-core/issues
- **Documentation**: `factory/docs/`
- **In-App Help**: Press `?` in Writers Factory
```

---

## Priority 4: Troubleshooting Guide

### Document: `TROUBLESHOOTING.md` (Root of repository)

**Purpose**: Common problems and solutions
**Audience**: Users encountering errors
**Tone**: Helpful, systematic

**Sections**:

1. **Installation Issues**
   - Python not found
   - Node.js version too old
   - pip install fails (permissions)
   - npm install fails (peer dependencies)

2. **Runtime Issues**
   - Backend won't start (port 8000 in use)
   - Frontend shows "Network Error"
   - API key invalid
   - Ollama models not showing

3. **Feature Issues**
   - Scene won't save / autosave not working
   - Character depth score always 0
   - Export fails or downloads empty file
   - AI generation fails with timeout

4. **Performance Issues**
   - Editor laggy when typing
   - AI generation very slow
   - Frontend build slow to start

5. **Data Issues**
   - Lost work / scenes disappeared
   - Can't delete project
   - Character Panel shows outdated data

**Format**: Problem → Cause → Fix (step-by-step)

---

## Priority 5: Quick Reference Card

### Document: `QUICK_REFERENCE.md` (in `factory/docs/`)

**Purpose**: Printable cheat sheet for common operations
**Audience**: New users, quick lookup
**Format**: 1-2 pages, Markdown (easily convertible to PDF)

**Sections**:

1. **Keyboard Shortcuts**
2. **Toolbar Icons**
3. **Creation Wizard Phases**
4. **AI Model Comparison**
5. **Scene Editor Formatting**
6. **Character Depth Scoring**
7. **Export Formats**
8. **Cost Optimization Tips**

---

## Priority 6: Advanced Guides

### Guide 1: Character Depth System

**Document**: `factory/docs/CHARACTER_DEPTH_GUIDE.md`

**Content**:
- Theory: Complexity from contradiction
- Five depth checks explained
- True Character vs Characterization
- Internal vs External contradiction
- Scoring system (0-100)
- Examples: Flat vs dimensional characters
- How to improve scores

### Guide 2: MCP Server Setup

**Document**: `factory/mcp/MCP_SETUP_GUIDE.md`

**Content**:
- What is MCP
- Available tools (10 tools with API)
- Connecting Claude Desktop
- Connecting Cursor AI
- Custom integrations
- Security considerations

### Guide 3: Multi-Model Strategy

**Document**: `factory/docs/MODEL_SELECTION_GUIDE.md`

**Content**:
- Model comparison chart (cost, quality, speed)
- Use cases (drafting, dialogue, description, editing)
- Economy Mode explained
- Tournament Mode workflow
- Agent Profiles (assign models by task)
- Cost optimization strategies

---

## Implementation Timeline

### Week 1 (Nov 18-22): Critical Updates
- [ ] Cloud Agent: Update helpContent.js for TipTap (Sprint 7R-06)
- [ ] Cloud Agent: Add Creation Wizard, NotebookLM, MCP topics to help
- [ ] Me: Create README.md (quick start guide)

### Week 2 (Nov 25-29): Support Documentation
- [ ] Me: Create TROUBLESHOOTING.md
- [ ] Me: Create QUICK_REFERENCE.md
- [ ] Me: Create CHARACTER_DEPTH_GUIDE.md

### Week 3 (Dec 2-6): Advanced Guides
- [ ] Me: Create MCP_SETUP_GUIDE.md
- [ ] Me: Create MODEL_SELECTION_GUIDE.md
- [ ] Test all documentation (have someone follow guides)

### Week 4 (Dec 9-13): Polish & Finalize
- [ ] Revise based on testing feedback
- [ ] Create PDF versions of quick reference
- [ ] Review for consistency and completeness

---

## Summary

### In-Codebase Documentation (Category A)

**Immediate Priority** (Week 1):
1. ✅ Update help for TipTap editor
2. ✅ Add Creation Wizard help topic
3. ✅ Add NotebookLM help topic
4. ✅ Add MCP tools help topic
5. ✅ Create README.md (installation + quick start)

**High Priority** (Week 2):
6. ✅ Create TROUBLESHOOTING.md
7. ✅ Create QUICK_REFERENCE.md
8. ✅ Create CHARACTER_DEPTH_GUIDE.md

**Medium Priority** (Week 3):
9. ✅ Create MCP_SETUP_GUIDE.md
10. ✅ Create MODEL_SELECTION_GUIDE.md

**Total Effort**: ~12-15 hours
**Timeline**: Complete by mid-December
**Result**: Fully documented, GitHub-ready Writers Factory

---

**Next Steps**:
1. Cloud Agent completes Sprint 7 Revision (TipTap)
2. Cloud Agent updates help content (Task 7R-06)
3. I create README.md and TROUBLESHOOTING.md
4. Test with fresh user, iterate
