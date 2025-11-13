# Architecture Overview

Writers Factory Core system architecture and design principles.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI / UI Layer                          │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Engine                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Base        │  │  Multi-Model │  │  Project     │     │
│  │  Workflow    │  │  Generation  │  │  Genesis     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                     Agent Pool                              │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐   │
│  │Claude │  │ GPT-4 │  │Gemini │  │DeepSeek│ │ Qwen │   │
│  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│              Knowledge & Storage Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Knowledge   │  │   Database   │  │   Cache      │     │
│  │  Router      │  │   (SQLite)   │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Core Principles

### 1. Model Agnostic
- Agents configured via YAML
- Easy addition/removal of models
- Unified interface across providers

### 2. Workflow-Based
- Everything is a composable workflow
- Standard lifecycle (setup → execute → cleanup)
- Step dependency resolution

### 3. Knowledge-Aware
- Smart routing between knowledge sources
- Automatic context adaptation
- Caching for performance

### 4. Cost-Conscious
- Track every API call
- Per-agent cost analytics
- Cost-per-win metrics

### 5. Observable
- Complete logging
- Analytics database
- Reproducible sessions

## Key Classes

### BaseAgent
Abstract base for all LLM integrations
- `generate()`: Generate text
- `count_tokens()`: Estimate tokens
- `calculate_cost()`: Calculate costs

### AgentPool
Manages multiple agents
- `register_agent()`: Add agent
- `execute_parallel()`: Run multiple agents
- `get_stats()`: Get analytics

### WorkflowEngine
Executes workflows
- `run_workflow()`: Execute workflow
- `_topological_sort()`: Resolve dependencies
- `_execute_parallel()`: Parallel execution

### Database
Persistent storage
- `insert_session()`: Record session
- `insert_result()`: Store result
- `get_agent_stats()`: Query analytics

## Data Flow

1. **User Request** → CLI/Code
2. **Workflow Created** → With context and agents
3. **Agent Pool** → Registers and validates agents
4. **Parallel Execution** → All agents generate concurrently
5. **Results Collected** → Stored in database
6. **Analytics Updated** → Cost and performance tracked
7. **Results Returned** → To user for comparison

## Configuration

### agents.yaml
Defines all available agents with:
- Provider and model
- Cost per 1K tokens
- Context window
- Strengths
- Handler class

### settings.yaml
System-wide settings:
- Generation defaults
- Workflow behavior
- Knowledge routing
- Storage options

## Extension Points

### Add New Agent
1. Create agent class inheriting BaseAgent
2. Implement generate() method
3. Add to agents.yaml
4. Register with AgentPool

### Add New Workflow
1. Inherit from BaseWorkflow
2. Implement setup/execute/cleanup
3. Define workflow steps
4. Add to workflows/ directory

### Add Knowledge Source
1. Implement query interface
2. Add to KnowledgeRouter
3. Update routing logic
4. Configure in settings.yaml

## Security

- API keys in credentials.json (gitignored)
- No credentials in code
- Connection timeouts
- Rate limiting support

## Performance

- Parallel agent execution
- Query result caching
- Database indexing
- Async/await throughout

## Future Enhancements

- Web UI dashboard
- Real-time monitoring
- Advanced analytics
- Auto-hybridization
- Batch processing
