# Writers Factory Core - Environment Setup

This guide will help you set up the development environment for the Writers Factory multi-model AI novel writing system.

## Prerequisites

- Python 3.11+
- Git
- UV package manager (or pip)

## Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core
```

### 2. Create Virtual Environment

Using UV (recommended):
```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
```

Using standard venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Using UV (faster):
```bash
uv pip install -r requirements.txt
uv pip install cognee
```

Using pip:
```bash
pip install -r requirements.txt
pip install cognee
```

This installs:
- **Core**: 87 packages (aiohttp, anthropic, openai, google-generativeai, rich, click, pydantic, pytest, etc.)
- **Cognee**: 90 additional packages (lancedb, fastembed, kuzu, networkx, fastapi, etc.)
- **Total**: 177 packages (~300MB)

### 4. Configure API Keys

Copy the template and add your actual API keys:

```bash
cp config/credentials.json.template config/credentials.json
cp .env.template .env
```

Edit `config/credentials.json` and replace placeholders:

```json
{
  "anthropic": {
    "api_key": "sk-ant-...",  // Your actual Anthropic API key
    "models": ["claude-opus-4", "claude-sonnet-4.5", "claude-sonnet-3.5"]
  },
  "openai": {
    "api_key": "sk-...",  // Your actual OpenAI API key
    "organization": "",  // Optional
    "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
  },
  "google": {
    "api_key": "AIza...",  // Your actual Google API key
    "models": ["gemini-2-flash", "gemini-1.5-pro"]
  }
  // Add keys for xAI, Qwen, DeepSeek, Doubao, Baichuan, Kimi as needed
}
```

Edit `.env` and set your API keys:

```bash
# Required for core functionality
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...

# Optional - Chinese LLMs
QWEN_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
DOUBAO_API_KEY=...
BAICHUAN_API_KEY=...
KIMI_API_KEY=...

# Optional - xAI
XAI_API_KEY=xai-...

# Optional - NotebookLM
NOTEBOOKLM_NOTEBOOK_ID=your_notebook_id
NOTEBOOKLM_ENABLED=false

# Paths (defaults should work)
COGNEE_DATA_DIR=.cognee
DATABASE_PATH=.factory/analytics.db
SESSION_PATH=project/.session
```

**IMPORTANT**: Never commit `config/credentials.json` or `.env` to Git. These are in `.gitignore`.

### 5. Initialize Project Directory

The project structure is already created:

```
project/
├── manuscript/          # Your novel chapters
├── reference/          # Reference materials
│   ├── characters/     # Character profiles
│   ├── worldbuilding/  # World details
│   └── research/       # Research notes
├── planning/           # Story outlines
└── .session/           # Auto-save session data (gitignored)
```

Add your reference materials to these directories before starting.

### 6. Initialize Cognee

Cognee needs to be initialized before first use:

```bash
python3 -c "import asyncio; from cognee import add, cognify; asyncio.run(add('Initialize'))"
```

This creates the local semantic graph database in `.cognee/` (~17MB).

### 7. Verify Setup

Run basic tests to ensure everything works:

```bash
# Test imports
python3 -c "from factory.core import workflow_engine; from factory.agents import agent_pool; print('✅ Core imports work')"

# Test agent pool
python3 -c "from factory.agents.agent_pool import AgentPool; pool = AgentPool(); print(f'✅ Agent pool loaded: {len(pool.list_agents())} agents')"

# Test knowledge router
python3 -c "from factory.knowledge.router import KnowledgeRouter; router = KnowledgeRouter(); print('✅ Knowledge router initialized')"

# Run test suite
pytest tests/ -v
```

Expected output:
- ✅ All imports work
- ✅ 16 agents loaded (Anthropic, OpenAI, Google, xAI, Chinese LLMs)
- ✅ Knowledge router initialized
- ✅ 19/19 tests passing

## Directory Structure

```
writers-factory-core/
├── factory/                 # Core source code
│   ├── agents/             # 16 LLM agent integrations
│   ├── core/               # Workflow engine
│   ├── knowledge/          # Knowledge router (Cognee/NotebookLM)
│   ├── multi_model_generation/  # Tournament system (Phase 1)
│   ├── storage/            # SQLite analytics database
│   └── ui/                 # CLI interface (Phase 1: basic, Phase 2: Rich TUI)
├── config/                 # Configuration
│   └── credentials.json    # API keys (gitignored)
├── docs/                   # Documentation
│   └── tasks/             # Task specifications
│       ├── PHASE_2_INSTRUCTIONS.md  # Detailed Phase 2 specs
│       └── START_PHASE_2.md         # Quick start guide
├── project/               # Your writing project
│   ├── manuscript/        # Novel chapters
│   ├── reference/         # Reference materials
│   ├── planning/          # Story outlines
│   └── .session/          # Auto-save data (gitignored)
├── tests/                 # Test suite (19 tests)
├── .cognee/               # Cognee database (gitignored)
├── .factory/              # Runtime data (gitignored)
├── .venv/                 # Virtual environment (gitignored)
├── .env                   # Environment variables (gitignored)
├── requirements.txt       # Python dependencies
└── SETUP.md              # This file
```

## Usage

### Phase 1 (Tournament System - Complete)

Run interactive demo:
```bash
python3 demo_interactive.py
```

This demonstrates the multi-model comparison system where the same prompt runs across multiple LLMs in parallel.

### Phase 2 (Stage-Based Workflow - In Development)

Phase 2 adds a full-screen Rich TUI with 5-stage pipeline:

```
Creation → Writing → Enhancing → Analyzing → Scoring
```

**Launch (when complete)**:
```bash
factory init              # Start Creation Wizard
factory work              # Open stage-based workflow
factory compare           # Run model comparison tool
```

**Features**:
- Full-screen Rich TUI with status bar
- Auto-save every 30s with crash recovery
- Knowledge queries from any stage (Cognee/NotebookLM)
- Scene generation, enhancement, voice testing
- Model comparison with side-by-side diff
- Creation Wizard (Save the Cat! 15 beats)

See [docs/tasks/PHASE_2_INSTRUCTIONS.md](docs/tasks/PHASE_2_INSTRUCTIONS.md) for complete specifications.

## Troubleshooting

### ModuleNotFoundError

If you see `ModuleNotFoundError: No module named 'X'`:
```bash
source .venv/bin/activate  # Make sure venv is activated
uv pip install -r requirements.txt
uv pip install cognee
```

### API Key Errors

If you see authentication errors:
1. Check that `config/credentials.json` has your actual keys (not placeholders)
2. Check that `.env` has your actual keys
3. Ensure keys are valid and have sufficient credits

### Cognee Initialization Issues

If Cognee fails to initialize:
```bash
rm -rf .cognee  # Remove existing database
python3 -c "import asyncio; from cognee import add, cognify; asyncio.run(add('Initialize'))"
```

### Test Failures

If tests fail:
1. Ensure virtual environment is activated
2. Check that all dependencies are installed
3. Verify API keys are configured
4. Run tests with verbose output: `pytest tests/ -v -s`

## Getting Help

- **Documentation**: See [docs/](docs/) directory
- **GitHub Issues**: https://github.com/gcharris/writers-factory-core/issues
- **Phase 2 Tasks**: See [docs/tasks/PHASE_2_INSTRUCTIONS.md](docs/tasks/PHASE_2_INSTRUCTIONS.md)

## Next Steps

1. **Phase 1 Demo**: Run `python3 demo_interactive.py` to see the tournament system
2. **Add Reference Materials**: Put character profiles, worldbuilding notes in `project/reference/`
3. **Phase 2 Development**: See [docs/tasks/START_PHASE_2.md](docs/tasks/START_PHASE_2.md)
4. **Test Phase 2**: When Cloud Agent completes Phase 2, test with `factory init`

---

**Environment Status**:
- ✅ UV virtual environment ready
- ✅ 177 Python packages installed
- ✅ Cognee installed (17MB local knowledge graph)
- ✅ API key templates created
- ✅ Project directory structure ready
- ⏳ User needs to add actual API keys
- ⏳ Phase 2 Rich TUI in development by Cloud Agent
