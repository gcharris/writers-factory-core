# Cloud Agent Tasks - Writers Factory Core
**Date**: 2025-11-13
**Duration**: 8-12 hours of work
**Deliverable**: Complete, working `writers-factory-core` repository

---

## 🎯 Mission

Build a **clean, reusable novel writing factory system** from scratch. This will be a separate repository that can be:
- Used by other writers (no Explants-specific content)
- Integrated into the main Explants project
- Distributed as open-source

You will work **completely autonomously** - no human input needed until final review.

---

## 📋 Prerequisites

**Before starting, read these files for context:**
1. `WRITERS_FACTORY_ARCHITECTURE.md` - Complete system architecture
2. `Novel Writing Factory System Overview & Implementation Blueprint.md` - Original vision
3. `WRITING_FACTORY_INVENTORY.md` - Existing tools to integrate with

---

## 🏗️ Repository Structure to Create

```
writers-factory-core/
│
├── factory/
│   ├── core/                        # Core engine
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # Master coordinator
│   │   ├── workflow_engine.py       # Workflow execution
│   │   ├── session_manager.py       # Session state
│   │   ├── agent_pool.py            # Multi-model management
│   │   └── config/
│   │       ├── agents.yaml          # Agent registry
│   │       └── settings.yaml
│   │
│   ├── agents/                      # LLM integrations
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Abstract base
│   │   ├── chinese/                 # NEW: Chinese LLMs
│   │   │   ├── __init__.py
│   │   │   ├── qwen.py
│   │   │   ├── deepseek.py
│   │   │   ├── doubao.py
│   │   │   ├── baichuan.py
│   │   │   └── kimi.py
│   │   └── README.md
│   │
│   ├── knowledge/                   # Knowledge base
│   │   ├── __init__.py
│   │   ├── router.py                # Smart routing
│   │   ├── cache.py                 # Query caching
│   │   └── README.md
│   │
│   ├── workflows/                   # Pre-built workflows
│   │   ├── __init__.py
│   │   ├── base_workflow.py         # Workflow base class
│   │   ├── project_genesis/         # NEW: Start new project
│   │   │   ├── __init__.py
│   │   │   ├── workflow.py
│   │   │   ├── character_generator.py
│   │   │   ├── world_generator.py
│   │   │   └── structure_generator.py
│   │   ├── multi_model_generation/  # NEW: Compare models
│   │   │   ├── __init__.py
│   │   │   └── workflow.py
│   │   └── README.md
│   │
│   ├── storage/                     # Data persistence
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── schema.sql
│   │   └── README.md
│   │
│   └── ui/                          # User interface
│       ├── __init__.py
│       ├── cli.py                   # Main CLI
│       └── README.md
│
├── tests/                           # Test suite
│   ├── test_workflow_engine.py
│   ├── test_agents.py
│   ├── test_knowledge_router.py
│   └── test_workflows.py
│
├── docs/                            # Documentation
│   ├── ARCHITECTURE.md
│   ├── QUICKSTART.md
│   ├── ADDING_AGENTS.md
│   ├── CREATING_WORKFLOWS.md
│   └── API_REFERENCE.md
│
├── examples/                        # Usage examples
│   ├── simple_generation.py
│   ├── multi_model_comparison.py
│   └── project_setup.py
│
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── pyproject.toml
```

---

## 📝 Detailed Task Breakdown

### Phase 1: Foundation (2 hours)

#### Task 1.1: Repository Setup
```bash
# Create directory
mkdir -p ~/writers-factory-core
cd ~/writers-factory-core

# Initialize git
git init
git config user.name "Claude Cloud Agent"
git config user.email "claude@anthropic.com"

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.env
.venv
*.db
*.sqlite3
.DS_Store
.idea/
.vscode/
*.log
EOF

# Initial commit
git add .gitignore
git commit -m "Initial commit: Repository structure"
```

#### Task 1.2: Create Directory Structure
```bash
# Create all directories
mkdir -p factory/core/config
mkdir -p factory/agents/chinese
mkdir -p factory/knowledge
mkdir -p factory/workflows/{project_genesis,multi_model_generation}
mkdir -p factory/storage
mkdir -p factory/ui
mkdir -p tests
mkdir -p docs
mkdir -p examples

# Create all __init__.py files
find factory -type d -exec touch {}/__init__.py \;

# Commit structure
git add .
git commit -m "Add directory structure"
```

#### Task 1.3: Create README.md
Create a comprehensive README explaining:
- What this is
- How to install
- Quick start example
- Link to full documentation

Commit: `git commit -m "Add README.md"`

#### Task 1.4: Create requirements.txt
```txt
# Core dependencies
pyyaml>=6.0
pydantic>=2.0
aiohttp>=3.8
anthropic>=0.21.0
openai>=1.12.0
google-generativeai>=0.4.0
httpx>=0.26.0

# Storage
sqlalchemy>=2.0

# CLI
click>=8.1
rich>=13.0

# Testing
pytest>=7.4
pytest-asyncio>=0.21
```

Commit: `git commit -m "Add requirements.txt"`

---

### Phase 2: Core Engine (3 hours)

#### Task 2.1: Create `factory/core/workflow_engine.py`

**Specification:**
- `Workflow` base class with standard interface
- `WorkflowEngine` that executes workflows
- State management (pause/resume)
- Step dependency system
- Error handling and rollback
- Progress tracking

**Key Classes:**
```python
class WorkflowStep:
    """Single step in a workflow."""
    name: str
    function: callable
    dependencies: List[str]

class Workflow:
    """Base workflow class."""
    def add_step(self, step: WorkflowStep)
    def execute(self) -> WorkflowResult
    def pause(self)
    def resume(self)

class WorkflowEngine:
    """Execute workflows with dependency resolution."""
    def run_workflow(self, workflow: Workflow) -> WorkflowResult
```

**Include:**
- Full docstrings
- Type hints
- Error handling
- Logging

Commit: `git commit -m "Add workflow engine"`

#### Task 2.2: Create `factory/core/agent_pool.py`

**Specification:**
- Manage multiple LLM agents
- Dynamic enable/disable
- Load balancing
- Cost tracking
- Parallel execution support

**Key Classes:**
```python
class AgentPool:
    """Manage pool of LLM agents."""
    def register_agent(self, agent: BaseAgent)
    def get_agent(self, name: str) -> BaseAgent
    def get_enabled_agents(self) -> List[BaseAgent]
    def execute_parallel(self, prompt: str, agents: List[str])
```

Commit: `git commit -m "Add agent pool manager"`

#### Task 2.3: Create `factory/core/config/agents.yaml`

**Specification:**
Create agent registry with 15+ agents:
- Anthropic: Claude Opus, Sonnet 4.5, Sonnet 3.5
- OpenAI: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
- Google: Gemini 2.0 Flash, Gemini 1.5 Pro
- xAI: Grok
- Chinese: Qwen, DeepSeek, Doubao, Baichuan, Kimi
- Open Source: Mistral, Llama 3

**Format:**
```yaml
agents:
  claude-sonnet-4.5:
    provider: anthropic
    model: claude-sonnet-4-5-20250929
    enabled: true
    context_window: 200000
    cost_per_1k_input: 0.003
    cost_per_1k_output: 0.015
    strengths: [creative, narrative, philosophy]
    handler: factory.agents.anthropic.ClaudeSonnet45
```

Commit: `git commit -m "Add agent registry configuration"`

---

### Phase 3: Chinese LLM Integrations (2 hours)

#### Task 3.1: Create `factory/agents/base_agent.py`

**Specification:**
- Abstract base class for all agents
- Standard interface for generation
- Cost tracking
- Token counting
- Error handling

```python
class BaseAgent(ABC):
    def __init__(self, config: dict)

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> AgentResponse

    def count_tokens(self, text: str) -> int
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float
```

Commit: `git commit -m "Add BaseAgent abstract class"`

#### Task 3.2: Create Chinese LLM Integrations

For each agent, create a file in `factory/agents/chinese/`:

**`qwen.py`** - Qwen API integration
**`deepseek.py`** - DeepSeek API integration
**`doubao.py`** - Doubao API integration
**`baichuan.py`** - Baichuan API integration
**`kimi.py`** - Kimi API integration

**Each agent should:**
- Inherit from `BaseAgent`
- Implement `generate()` method
- Handle API authentication
- Parse responses
- Track costs
- Include full docstrings

**Example structure:**
```python
class QwenAgent(BaseAgent):
    """Qwen (通义千问) API integration."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"

    async def generate(self, prompt: str, **kwargs) -> AgentResponse:
        # Implementation
        pass
```

Commit after each agent: `git commit -m "Add [Agent] integration"`

#### Task 3.3: Create `factory/agents/README.md`

Document:
- How to add new agents
- Agent registry format
- API key configuration
- Testing new agents

Commit: `git commit -m "Add agents documentation"`

---

### Phase 4: Knowledge Router (1.5 hours)

#### Task 4.1: Create `factory/knowledge/router.py`

**Specification:**
Smart routing between knowledge systems:
- Cognee (local semantic graph)
- Gemini File Search (cloud semantic search)
- NotebookLM (external queries)

**Features:**
- Query type classification
- Automatic fallback chain
- Caching layer
- Cost optimization

**Key Classes:**
```python
class KnowledgeRouter:
    """Route queries to appropriate knowledge system."""

    def classify_query(self, query: str) -> QueryType
    def route_query(self, query: str) -> KnowledgeSource
    async def query(self, query: str) -> QueryResult
```

Commit: `git commit -m "Add knowledge router"`

#### Task 4.2: Create `factory/knowledge/cache.py`

**Specification:**
- LRU cache for query results
- TTL-based expiration
- Cache warming
- Statistics

Commit: `git commit -m "Add query cache"`

---

### Phase 5: Workflows (2.5 hours)

#### Task 5.1: Create `factory/workflows/base_workflow.py`

**Specification:**
Base class for all workflows with:
- Standard lifecycle (setup → execute → cleanup)
- State management
- Progress callbacks
- Error recovery

```python
class BaseWorkflow(ABC):
    @abstractmethod
    async def setup(self)

    @abstractmethod
    async def execute(self) -> WorkflowResult

    @abstractmethod
    async def cleanup(self)
```

Commit: `git commit -m "Add base workflow class"`

#### Task 5.2: Create Project Genesis Workflow

**Files to create:**
- `factory/workflows/project_genesis/workflow.py` - Main workflow
- `factory/workflows/project_genesis/character_generator.py` - Generate characters
- `factory/workflows/project_genesis/world_generator.py` - Generate world/setting
- `factory/workflows/project_genesis/structure_generator.py` - Generate 3/4-act structure

**Workflow Steps:**
1. Gather initial prompts (genre, themes, basic idea)
2. Generate 3-5 main characters with backstories
3. Generate world/setting details
4. Generate 3-act or 4-act structure
5. Populate project directory structure
6. Create initial reference files

**Use multi-model generation:**
- Generate each component with 3 different models
- Let user select best version
- Store all variants for reference

Commit: `git commit -m "Add project genesis workflow"`

#### Task 5.3: Create Multi-Model Generation Workflow

**File:** `factory/workflows/multi_model_generation/workflow.py`

**Specification:**
- Accept prompt + context
- Accept list of agent names
- Execute generation in parallel
- Collect all results
- Score results (if scoring function provided)
- Return ranked results with metadata

```python
class MultiModelGenerationWorkflow(BaseWorkflow):
    async def execute(self,
                     prompt: str,
                     agents: List[str],
                     context: dict = None) -> MultiModelResult
```

Commit: `git commit -m "Add multi-model generation workflow"`

---

### Phase 6: Storage & Analytics (1.5 hours)

#### Task 6.1: Create `factory/storage/schema.sql`

**Specification:**
SQLite schema for:
- Sessions (workflow runs)
- Results (agent outputs)
- Scores (quality metrics)
- Costs (API usage)
- Analytics (aggregated stats)

```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    workflow_name TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT
);

CREATE TABLE results (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    agent_name TEXT,
    prompt TEXT,
    output TEXT,
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost REAL,
    response_time_ms INTEGER
);

-- More tables...
```

Commit: `git commit -m "Add database schema"`

#### Task 6.2: Create `factory/storage/database.py`

**Specification:**
Database management class:
- Connection management
- CRUD operations
- Query builders
- Analytics queries

Commit: `git commit -m "Add database management"`

---

### Phase 7: CLI Interface (1 hour)

#### Task 7.1: Create `factory/ui/cli.py`

**Specification:**
Rich CLI using Click + Rich library:

```bash
# Main commands
factory init                    # Initialize new project
factory workflow run <name>     # Run workflow
factory agent list              # List available agents
factory agent test <name>       # Test agent connection
factory session list            # List past sessions
factory session show <id>       # Show session details
```

**Features:**
- Colorful output (Rich library)
- Progress bars
- Tables for comparison
- Interactive prompts

Commit: `git commit -m "Add CLI interface"`

---

### Phase 8: Documentation (1 hour)

#### Task 8.1: Create Complete Documentation

**Files:**
- `docs/ARCHITECTURE.md` - System architecture overview
- `docs/QUICKSTART.md` - 5-minute getting started guide
- `docs/ADDING_AGENTS.md` - How to add new LLM agents
- `docs/CREATING_WORKFLOWS.md` - How to create custom workflows
- `docs/API_REFERENCE.md` - Complete API reference

Commit: `git commit -m "Add documentation"`

---

### Phase 9: Tests & Examples (1 hour)

#### Task 9.1: Create Test Suite

**Files:**
- `tests/test_workflow_engine.py` - Test workflow execution
- `tests/test_agents.py` - Test agent integrations
- `tests/test_knowledge_router.py` - Test routing logic
- `tests/test_workflows.py` - Test built-in workflows

Use pytest with async support.

Commit: `git commit -m "Add test suite"`

#### Task 9.2: Create Examples

**Files:**
- `examples/simple_generation.py` - Basic single-model generation
- `examples/multi_model_comparison.py` - Compare 3 models
- `examples/project_setup.py` - Full project genesis example

Commit: `git commit -m "Add usage examples"`

---

## ✅ Final Steps

### Task 10.1: Create CHANGELOG.md
Document all features implemented.

### Task 10.2: Create CONTRIBUTING.md
Guidelines for contributing to the project.

### Task 10.3: Final Review
- Run all tests
- Verify all imports work
- Check documentation completeness
- Ensure all files have docstrings

### Task 10.4: Tag Release
```bash
git tag -a v0.1.0 -m "Initial release: Writers Factory Core"
```

---

## 📊 Deliverables Checklist

By end of work, you should have:

- [ ] Complete directory structure
- [ ] Workflow engine with dependency resolution
- [ ] Agent pool manager
- [ ] 5 Chinese LLM integrations (Qwen, DeepSeek, Doubao, Baichuan, Kimi)
- [ ] Knowledge router with caching
- [ ] Project genesis workflow (complete)
- [ ] Multi-model generation workflow
- [ ] SQLite database with schema
- [ ] Rich CLI interface
- [ ] Complete documentation (5 docs)
- [ ] Test suite (4 test files)
- [ ] Usage examples (3 examples)
- [ ] All code committed to git
- [ ] Tagged as v0.1.0

---

## 🎯 Success Criteria

**The system should be able to:**
1. Initialize a new project from scratch
2. Generate characters/world/structure using multiple models
3. Run any workflow and track progress
4. Store all results in database
5. Query analytics (costs, performance, quality)
6. Work without any project-specific data

**When done:**
- Save git log to `GIT_LOG.txt`
- Save directory tree to `STRUCTURE.txt`
- Save test results to `TEST_RESULTS.txt`
- Create `HANDOFF.md` with overview of what was built

---

## 🚀 After You're Done

The human will:
1. Review your work
2. Create GitHub repository
3. Push your commits
4. Begin integration testing

You will have built a **complete, working, reusable novel writing factory** from scratch!

Good luck! 🎉
