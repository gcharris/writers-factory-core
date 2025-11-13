# Quick Start Guide

Get started with Writers Factory Core in 5 minutes.

## Installation

```bash
# Clone repository
git clone https://github.com/gcharris/writers-factory-core.git
cd writers-factory-core

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

## Configuration

1. Create credentials file:
```bash
cp config/credentials.example.json config/credentials.json
```

2. Add your API keys to `config/credentials.json`:
```json
{
  "anthropic_api_key": "YOUR_ANTHROPIC_KEY",
  "openai_api_key": "YOUR_OPENAI_KEY",
  "google_api_key": "YOUR_GOOGLE_KEY",
  "deepseek_api_key": "YOUR_DEEPSEEK_KEY"
}
```

## Basic Usage

### 1. Simple Generation

```python
import asyncio
from factory.core.agent_pool import AgentPool
from factory.agents.base_agent import AgentConfig
from factory.agents.chinese.deepseek import DeepSeekAgent

# Create agent
config = AgentConfig(
    name="deepseek-v3",
    model="deepseek-chat",
    api_key="YOUR_KEY"
)
agent = DeepSeekAgent(config)

# Generate
async def main():
    result = await agent.generate("Write a short story about a robot.")
    print(result["output"])
    print(f"Cost: ${result['cost']:.4f}")

asyncio.run(main())
```

### 2. Multi-Model Comparison

```python
from factory.workflows.multi_model_generation.workflow import MultiModelGenerationWorkflow
from factory.core.agent_pool import AgentPool

# Setup agent pool
pool = AgentPool()
# ... register agents ...

# Run workflow
workflow = MultiModelGenerationWorkflow(
    agent_pool=pool,
    prompt="Write an opening scene for a sci-fi thriller.",
    agents=["claude-sonnet-4.5", "gpt-4o", "deepseek-v3"],
    temperature=0.8,
    max_tokens=1000
)

result = await workflow.run()

# View results
for response in result.outputs["responses"]:
    print(f"\n{response['agent']}:")
    print(response['output'][:200] + "...")
    print(f"Cost: ${response['cost']:.4f}")
```

### 3. Using the CLI

```bash
# Initialize project
factory init --name "My Novel" --genre "sci-fi"

# List agents
factory agent list

# Run multi-model generation
factory workflow run multi-model --agents "claude,gpt4o,gemini"

# View statistics
factory stats
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
- See [ADDING_AGENTS.md](ADDING_AGENTS.md) to add new models
- Check [CREATING_WORKFLOWS.md](CREATING_WORKFLOWS.md) for custom workflows
- Review [API_REFERENCE.md](API_REFERENCE.md) for complete API docs

## Troubleshooting

### Import errors
```bash
pip install -r requirements.txt
```

### API key errors
Check `config/credentials.json` has valid keys

### Connection timeouts
Increase timeout in agent config:
```python
config = AgentConfig(..., timeout=300)
```
