"""Simple generation example.

Demonstrates basic usage of a single agent for text generation.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.agents.base_agent import AgentConfig
from factory.agents.chinese.deepseek import DeepSeekAgent


async def main():
    """Run simple generation example."""
    print("=== Simple Generation Example ===\n")

    # Configure agent
    config = AgentConfig(
        name="deepseek-v3",
        model="deepseek-chat",
        api_key="YOUR_DEEPSEEK_API_KEY",  # Replace with actual key
        context_window=64000,
        max_output=2000,
        cost_per_1k_input=0.00027,
        cost_per_1k_output=0.0011,
    )

    # Create agent
    agent = DeepSeekAgent(config)

    # Generate text
    prompt = """Write a short story (150-200 words) about a robot who learns to paint.
The story should have a beginning, middle, and end."""

    print(f"Prompt: {prompt}\n")
    print("Generating...")

    try:
        result = await agent.generate(
            prompt=prompt,
            temperature=0.8,
            max_tokens=300
        )

        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(result["output"])
        print("="*60)

        print(f"\nTokens: {result['tokens_input']} input + {result['tokens_output']} output")
        print(f"Cost: ${result['cost']:.4f}")
        print(f"Model: {result['model_version']}")

        # Show agent stats
        stats = agent.get_stats()
        print(f"\nAgent Stats:")
        print(f"  Requests: {stats['request_count']}")
        print(f"  Total cost: ${stats['total_cost']:.4f}")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Make sure to replace YOUR_DEEPSEEK_API_KEY with your actual API key")


if __name__ == "__main__":
    asyncio.run(main())
