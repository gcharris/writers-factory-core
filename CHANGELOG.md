# Changelog

All notable changes to Writers Factory Core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-13

### Added

#### Core Engine
- Workflow engine with dependency resolution and parallel execution
- Agent pool manager for multi-model orchestration
- Step-based workflow system with pause/resume capabilities
- Automatic cost tracking and performance monitoring

#### Agent Integrations
- BaseAgent abstract class for standardized LLM integration
- Chinese LLM integrations:
  - Qwen (通义千问) - Alibaba
  - DeepSeek V3
  - Doubao (豆包) - ByteDance
  - Baichuan (百川)
  - Kimi (月之暗面) - Moonshot AI
- Comprehensive agent registry with 15+ model configurations
- OpenAI-compatible API support for multiple providers

#### Knowledge Systems
- Knowledge router with smart query classification
- Support for multiple knowledge sources:
  - Cognee (local semantic graph)
  - Gemini File Search (cloud semantic search)
  - NotebookLM (external queries)
- LRU query cache with TTL expiration
- Automatic fallback chain for failed queries

#### Workflows
- BaseWorkflow with standard lifecycle (setup/execute/cleanup)
- Multi-model generation workflow for parallel comparison
- Project genesis workflow for initializing new writing projects
- Extensible workflow system for custom workflows

#### Storage & Analytics
- SQLite database for session and result tracking
- Comprehensive analytics views:
  - Agent performance metrics
  - Cost tracking and summaries
  - Win rate analytics
  - Daily cost breakdowns
- Automatic session cleanup

#### CLI Interface
- Rich CLI with colorful tables and panels
- Commands for:
  - Project initialization
  - Agent management
  - Workflow execution
  - Session viewing
  - Statistics display

#### Documentation
- Complete architecture overview
- Quick start guide
- Adding agents guide
- Creating workflows guide
- API reference documentation
- README with examples

#### Tests & Examples
- Unit tests for all major components
- Example scripts:
  - Simple single-agent generation
  - Multi-model comparison
  - Project setup workflow
- pytest configuration with async support

### Features
- Model-agnostic design via YAML configuration
- Parallel agent execution for tournaments
- Automatic token counting and cost calculation
- Request retry with exponential backoff
- Comprehensive logging throughout
- Type hints on all functions
- Detailed docstrings

### Configuration
- agents.yaml with 15+ pre-configured models
- settings.yaml for system-wide configuration
- Organized agent groups (premium, balanced, budget, etc.)
- Easy enable/disable per agent

### Infrastructure
- Complete project structure with proper Python package layout
- requirements.txt with all dependencies
- setup.py and pyproject.toml for package installation
- .gitignore for Python projects
- Black, isort, flake8, mypy configuration

## [Unreleased]

### Planned Features
- Web UI dashboard for tournament monitoring
- Real-time progress updates via WebSocket
- Advanced analytics and visualizations
- Auto-hybridization of model outputs
- Batch processing support
- Additional LLM provider integrations
- Enhanced caching strategies
- Model fine-tuning support

### Known Issues
- API authentication requires manual key entry
- Mock implementations for some knowledge system integrations
- Limited error messages for some edge cases
- No built-in rate limiting yet

### Future Enhancements
- Support for local model hosting
- Integration with vector databases
- Advanced prompt template system
- Collaborative features for team workflows
- Export to various manuscript formats
- Version control for generated content
