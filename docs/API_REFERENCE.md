# API Reference

Complete API documentation for Writers Factory Core.

## Core Classes

### BaseAgent

Abstract base class for all LLM agents.

```python
from factory.agents.base_agent import BaseAgent, AgentConfig

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig)

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.8,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]

    def count_tokens(self, text: str) -> int
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float
    def get_stats(self) -> Dict[str, Any]
    def reset_stats(self) -> None
```

**AgentConfig**:
- `name`: Agent identifier
- `model`: Model name
- `api_key`: API key
- `context_window`: Maximum context tokens
- `max_output`: Maximum output tokens
- `cost_per_1k_input`: Cost per 1000 input tokens
- `cost_per_1k_output`: Cost per 1000 output tokens

### AgentPool

Manages multiple LLM agents.

```python
from factory.core.agent_pool import AgentPool

class AgentPool:
    def __init__(self)

    def register_agent(self, name: str, agent: Any, enabled: bool = True) -> None
    def unregister_agent(self, name: str) -> None
    def get_agent(self, name: str) -> Optional[Any]
    def list_agents(self, enabled_only: bool = False) -> List[str]
    def enable_agent(self, name: str) -> None
    def disable_agent(self, name: str) -> None

    async def execute_single(
        self, agent_name: str, prompt: str, **kwargs
    ) -> AgentResponse

    async def execute_parallel(
        self, prompt: str, agents: Optional[List[str]] = None, **kwargs
    ) -> ParallelResult

    def get_stats(self, agent_name: Optional[str] = None) -> Dict[str, Any]
    def get_summary(self) -> Dict[str, Any]
```

### WorkflowEngine

Executes workflows with dependency resolution.

```python
from factory.core.workflow_engine import WorkflowEngine, Workflow

class WorkflowEngine:
    def __init__(self)

    async def run_workflow(
        self, workflow: Workflow, parallel: bool = True
    ) -> WorkflowResult

    def pause(self) -> None
    def resume(self) -> None
```

### Database

SQLite database for analytics.

```python
from factory.storage.database import Database

class Database:
    def __init__(self, db_path: str = ".factory/analytics.db")

    def insert_session(
        self, session_id: str, workflow_name: str, status: str, context: Optional[Dict] = None
    ) -> None

    def insert_result(
        self, result_id: str, session_id: str, agent_name: str, prompt: str, output: str, ...
    ) -> None

    def insert_winner(
        self, session_id: str, result_id: str, reason: Optional[str] = None
    ) -> None

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]
    def get_session_results(self, session_id: str) -> List[Dict[str, Any]]
    def get_agent_stats(self, agent_name: Optional[str] = None) -> List[Dict[str, Any]]
    def get_session_costs(self, limit: int = 50) -> List[Dict[str, Any]]
    def get_agent_win_rates(self) -> List[Dict[str, Any]]
    def get_daily_costs(self, days: int = 30) -> List[Dict[str, Any]]

    def cleanup_old_sessions(self, days: int = 90) -> int
    def close(self) -> None
```

### KnowledgeRouter

Routes queries to knowledge sources.

```python
from factory.knowledge.router import KnowledgeRouter

class KnowledgeRouter:
    def __init__(
        self, prefer_local: bool = True, enable_caching: bool = True
    )

    def classify_query(self, query: str) -> QueryType
    def route_query(self, query: str) -> KnowledgeSource

    async def query(
        self, query: str, max_results: int = 5, force_source: Optional[str] = None
    ) -> QueryResult
```

### QueryCache

LRU cache for query results.

```python
from factory.knowledge.cache import QueryCache

class QueryCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600)

    def get(self, query: str, params: Optional[Dict] = None) -> Optional[Any]
    def set(self, query: str, result: Any, params: Optional[Dict] = None) -> None
    def clear(self) -> None
    def get_stats(self) -> Dict[str, Any]
```

## Workflow Classes

### BaseWorkflow

Base class for all workflows.

```python
from factory.workflows.base_workflow import BaseWorkflow

class BaseWorkflow(Workflow, ABC):
    def __init__(self, name: str, workflow_id: Optional[str] = None, context: Optional[Dict] = None)

    async def setup(self) -> None
    async def execute(self) -> WorkflowResult
    async def cleanup(self) -> None
    async def run(self) -> WorkflowResult

    def validate_context(self, required_keys: list) -> None
```

### MultiModelGenerationWorkflow

Generate content with multiple models.

```python
from factory.workflows.multi_model_generation.workflow import MultiModelGenerationWorkflow

class MultiModelGenerationWorkflow(BaseWorkflow):
    def __init__(
        self,
        agent_pool: AgentPool,
        prompt: str,
        agents: List[str],
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    )

    def get_ranked_results(
        self, scoring_function: Optional[callable] = None
    ) -> List[Dict[str, Any]]
```

### ProjectGenesisWorkflow

Initialize new writing projects.

```python
from factory.workflows.project_genesis.workflow import ProjectGenesisWorkflow

class ProjectGenesisWorkflow(BaseWorkflow):
    def __init__(
        self,
        agent_pool: AgentPool,
        project_name: str,
        genre: str,
        themes: List[str],
        basic_idea: str,
        output_dir: Optional[Path] = None,
        num_characters: int = 5,
        act_structure: int = 3
    )
```

## Data Classes

### AgentResponse

```python
@dataclass
class AgentResponse:
    agent_name: str
    output: str
    tokens_input: int
    tokens_output: int
    cost: float
    response_time_ms: int
    model_version: str
    timestamp: datetime
    metadata: Dict[str, Any]
    error: Optional[str]

    @property
    def success(self) -> bool
    @property
    def total_tokens(self) -> int
```

### WorkflowResult

```python
@dataclass
class WorkflowResult:
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime]
    steps_completed: int
    steps_total: int
    outputs: Dict[str, Any]
    errors: List[str]
    metadata: Dict[str, Any]

    @property
    def duration(self) -> Optional[float]
    @property
    def success(self) -> bool
```

## Enums

### WorkflowStatus
```python
PENDING, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED
```

### QueryType
```python
FACTUAL, CONCEPTUAL, ANALYTICAL, GENERAL
```

### KnowledgeSource
```python
COGNEE, GEMINI_FILE_SEARCH, NOTEBOOKLM
```

## Usage Examples

See examples/ directory for complete working examples:
- `examples/simple_generation.py`
- `examples/multi_model_comparison.py`
- `examples/project_setup.py`
