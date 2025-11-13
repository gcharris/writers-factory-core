# Adding New Agents

Guide to integrating new LLM providers into Writers Factory Core.

## Overview

Adding a new agent involves:
1. Creating agent class
2. Registering in agents.yaml
3. Testing integration

## Step 1: Create Agent Class

Create a new file in the appropriate directory:
- US models: `factory/agents/`
- Chinese models: `factory/agents/chinese/`
- Open source: `factory/agents/opensource/`

```python
# factory/agents/chinese/newmodel.py

from typing import Any, Dict, Optional
import httpx
from factory.agents.base_agent import BaseAgent, AgentConfig

class NewModelAgent(BaseAgent):
    """Integration for NewModel API."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        if not config.api_key:
            raise ValueError("API key is required")

        self.api_key = config.api_key
        self.base_url = config.base_url or "https://api.provider.com/v1"

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.8,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        \"\"\"Generate text using NewModel API.\"\"\"

        max_tokens = max_tokens or self.config.max_output

        # Prepare request
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Make API call
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            data = response.json()

            # Extract results
            output_text = data["choices"][0]["message"]["content"]
            tokens_input = data["usage"]["prompt_tokens"]
            tokens_output = data["usage"]["completion_tokens"]

            # Calculate cost
            cost = self.calculate_cost(tokens_input, tokens_output)

            return {
                "output": output_text,
                "tokens_input": tokens_input,
                "tokens_output": tokens_output,
                "cost": cost,
                "model_version": data.get("model", self.model),
                "metadata": {
                    "finish_reason": data["choices"][0].get("finish_reason", ""),
                }
            }
```

## Step 2: Register in agents.yaml

Add configuration to `factory/core/config/agents.yaml`:

```yaml
new-model:
  provider: provider_name
  model: model-identifier
  enabled: true
  context_window: 32000
  max_output: 4000
  cost_per_1k_input: 0.001
  cost_per_1k_output: 0.002
  strengths:
    - strength1
    - strength2
    - strength3
  handler: factory.agents.chinese.newmodel.NewModelAgent
  description: "Brief description of the model"
```

## Step 3: Test Integration

Create a test script:

```python
# test_newmodel.py
import asyncio
from factory.agents.chinese.newmodel import NewModelAgent
from factory.agents.base_agent import AgentConfig

async def test_agent():
    config = AgentConfig(
        name="new-model",
        model="model-identifier",
        api_key="YOUR_API_KEY",
        context_window=32000,
        max_output=4000,
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.002
    )

    agent = NewModelAgent(config)

    # Test generation
    result = await agent.generate(
        prompt="Write a short poem about AI.",
        temperature=0.8,
        max_tokens=100
    )

    print(f"Output: {result['output']}")
    print(f"Tokens: {result['tokens_input']} + {result['tokens_output']}")
    print(f"Cost: ${result['cost']:.4f}")
    print(f"Model: {result['model_version']}")

    # Check stats
    stats = agent.get_stats()
    print(f"\nStats: {stats}")

if __name__ == "__main__":
    asyncio.run(test_agent())
```

Run test:
```bash
python test_newmodel.py
```

## Step 4: Add to Agent Pool

```python
from factory.core.agent_pool import AgentPool
from factory.agents.chinese.newmodel import NewModelAgent

pool = AgentPool()
pool.register_agent("new-model", agent, enabled=True)

# Use in workflows
result = await pool.execute_single(
    "new-model",
    "Your prompt here"
)
```

## API Compatibility

### OpenAI-Compatible APIs
Many providers use OpenAI-compatible endpoints:
- DeepSeek
- Doubao
- Baichuan
- Kimi

Use similar structure with different base URLs.

### Custom APIs
For unique APIs (like Qwen/DashScope):
- Study provider documentation
- Adapt request/response format
- Handle provider-specific features

## Best Practices

1. **Error Handling**: Catch and log all API errors
2. **Token Counting**: Use provider's token count when available
3. **Cost Calculation**: Update costs regularly from provider pricing
4. **Timeouts**: Set appropriate timeouts for model speed
5. **Retries**: Use inherited retry logic from BaseAgent
6. **Logging**: Log all API calls for debugging
7. **Documentation**: Add docstrings and examples

## Common Issues

### Authentication Errors
- Verify API key format
- Check key is active
- Confirm endpoint URL

### Token Limit Errors
- Validate context_window setting
- Check max_output doesn't exceed limits
- Implement truncation if needed

### Cost Tracking Issues
- Verify cost_per_1k values
- Check token counts are accurate
- Test with small prompts first

## Provider-Specific Notes

### Chinese LLMs
- May require Chinese API documentation
- Often use RMB pricing (convert to USD)
- May have regional restrictions

### Open Source Models
- May need local hosting
- Different authentication
- Performance variations

### Enterprise APIs
- May require account approval
- Special rate limits
- Custom endpoints
