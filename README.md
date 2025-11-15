# Writers Factory Core

A **model-agnostic multi-agent novel writing system** for computational storytelling.

## What is this?

Writers Factory Core is a clean, reusable framework that allows writers to:

- **Run tournaments** - Send the same prompt to 10+ different AI models simultaneously
- **Compare outputs** - View side-by-side results from Claude, GPT-4, Gemini, DeepSeek, and more
- **Track analytics** - Monitor costs, performance, and quality metrics
- **Build workflows** - Create custom generation pipelines for characters, worlds, and scenes
- **Integrate knowledge** - Connect to multiple knowledge base systems for context-aware generation

## Getting Started: Project Setup Wizard ✨

**New to Writers Factory?** Start by creating your custom project with the Setup Wizard:

1. **Launch Writers Factory**
   ```bash
   npm run dev
   ```

2. **Click "Create New Project"** in the UI (or visit http://localhost:5173/setup)

3. **Follow the 6-step wizard:**
   - Enter project details (name & genre)
   - Paste 3-5 example scenes that represent YOUR voice
   - Upload reference materials (optional: style guides, character sheets)
   - AI analyzes your voice and extracts patterns
   - Review & test your custom analyzer
   - Create project!

4. **You'll Get 6 AI Skills Custom-Built for YOUR Voice:**
   - `scene-analyzer` - Scores scenes using YOUR quality criteria
   - `scene-enhancer` - Makes surgical fixes matching YOUR style
   - `character-validator` - Ensures character consistency
   - `scene-writer` - Writes new scenes in YOUR voice
   - `scene-multiplier` - Creates 5 variations per scene
   - `scaffold-generator` - Expands outlines with story knowledge

**Why This Matters:** Generic AI tools use one-size-fits-all prompts. Writers Factory generates skills tuned to YOUR writing patterns, metaphor domains, and quality standards.

**📖 [Read the Complete Setup Wizard Guide](docs/setup-wizard-guide.md)**

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp config/credentials.example.json config/credentials.json
# Edit config/credentials.json with your API keys
```

### Basic Usage

```python
from factory.core.orchestrator import Tournament

# Create a tournament
tournament = Tournament(
    name="opening-scene",
    prompt="Write an opening scene for a sci-fi thriller...",
    agents=["claude-sonnet-4.5", "gpt-4o", "gemini-2-flash", "deepseek-v3"],
    max_tokens=2000
)

# Run the tournament
results = await tournament.run()

# View results
for result in results:
    print(f"{result.agent_name}: {result.score}/100")
    print(result.output)
```

## Features

### 🎯 Model Agnostic
- Add/remove LLMs via configuration, not code
- Support for 15+ models out of the box
- Easy integration of new providers

### 🏆 Tournament System
- Parallel execution across multiple models
- Automatic cost tracking
- Performance analytics
- Side-by-side comparison

### 🧠 Knowledge Integration
- Cognee (local semantic graph)
- Gemini File Search (cloud semantic search)
- NotebookLM (external queries)
- Smart routing based on query type

### 🔧 Extensible Workflows
- Pre-built workflows for common tasks
- Project genesis (characters, world, structure)
- Multi-model generation and comparison
- Custom workflow creation

### 📊 Analytics
- Cost per generation
- Response time tracking
- Quality metrics
- Win rate by model

## Supported Models

### Anthropic
- Claude Opus 4
- Claude Sonnet 4.5
- Claude Sonnet 3.5

### OpenAI
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo

### Google
- Gemini 2.0 Flash
- Gemini 1.5 Pro

### Chinese LLMs
- Qwen (通义千问)
- DeepSeek
- Doubao (豆包)
- Baichuan (百川)
- Kimi (月之暗面)

### Open Source
- Mistral
- Llama 3
- And more...

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Adding New Agents](docs/ADDING_AGENTS.md)
- [Creating Workflows](docs/CREATING_WORKFLOWS.md)
- [API Reference](docs/API_REFERENCE.md)

## CLI Interface

```bash
# Initialize a new project
factory init

# Run a workflow
factory workflow run project-genesis

# List available agents
factory agent list

# Test an agent connection
factory agent test claude-sonnet-4.5

# View past sessions
factory session list

# Show session details
factory session show <session-id>
```

## Project Structure

```
writers-factory-core/
├── factory/
│   ├── core/              # Core engine (orchestrator, workflows)
│   ├── agents/            # LLM integrations
│   ├── knowledge/         # Knowledge base systems
│   ├── workflows/         # Pre-built workflows
│   ├── storage/           # Database and persistence
│   └── ui/                # CLI interface
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Usage examples
```

## Use Cases

### Novel Writing
- Generate multiple versions of scenes
- Compare character voice across models
- Create world-building content
- Develop story structures

### Creative Exploration
- Experiment with different AI personalities
- Find which models excel at specific tasks
- Hybridize outputs from multiple models

### Cost Optimization
- Mix expensive and cheap models strategically
- Track cost-per-quality metrics
- Identify best value models for your use case

## Requirements

- Python 3.9+
- API keys for desired LLM providers
- SQLite (included with Python)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see LICENSE file for details

## Support

- [GitHub Issues](https://github.com/gcharris/writers-factory-core/issues)
- [Documentation](docs/)

## Acknowledgments

Built for writers who want to harness the power of multiple AI models for computational storytelling.

---

**Start writing smarter, not harder.**
