"""Multi-model comparison example.

Demonstrates generating the same content with multiple models and comparing results.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.core.agent_pool import AgentPool
from factory.agents.base_agent import AgentConfig
from factory.agents.chinese.deepseek import DeepSeekAgent
from factory.agents.chinese.qwen import QwenAgent


async def main():
    """Run multi-model comparison example."""
    print("=== Multi-Model Comparison Example ===\n")

    # Create agent pool
    pool = AgentPool()

    # Register DeepSeek agent
    deepseek_config = AgentConfig(
        name="deepseek-v3",
        model="deepseek-chat",
        api_key="YOUR_DEEPSEEK_API_KEY",
        cost_per_1k_input=0.00027,
        cost_per_1k_output=0.0011,
    )
    pool.register_agent("deepseek-v3", DeepSeekAgent(deepseek_config))

    # Register Qwen agent
    qwen_config = AgentConfig(
        name="qwen-max",
        model="qwen-max",
        api_key="YOUR_QWEN_API_KEY",
        cost_per_1k_input=0.008,
        cost_per_1k_output=0.008,
    )
    pool.register_agent("qwen-max", QwenAgent(qwen_config))

    # Prompt for generation
    prompt = """Write a compelling opening paragraph for a science fiction novel.
The setting is a space station in orbit around Jupiter."""

    print(f"Prompt: {prompt}\n")
    print("Generating with multiple models...\n")

    try:
        # Execute parallel generation
        result = await pool.execute_parallel(
            prompt=prompt,
            agents=["deepseek-v3", "qwen-max"],
            temperature=0.8,
            max_tokens=200
        )

        # Display results
        print("="*80)
        print("RESULTS:")
        print("="*80)

        for i, response in enumerate(result.responses, 1):
            print(f"\n{i}. {response.agent_name.upper()}")
            print("-" * 80)

            if response.success:
                print(response.output)
                print(f"\nStats: {response.total_tokens} tokens, "
                      f"${response.cost:.4f}, {response.response_time_ms}ms")
            else:
                print(f"Error: {response.error}")

        # Summary
        print("\n" + "="*80)
        print("SUMMARY:")
        print("="*80)
        print(f"Session ID: {result.session_id}")
        print(f"Duration: {result.duration_ms}ms")
        print(f"Total Cost: ${result.total_cost:.4f}")
        print(f"Total Tokens: {result.total_tokens}")
        print(f"Successful: {len(result.successful_responses)}/{len(result.responses)}")

        # Pool stats
        print("\n" + "="*80)
        print("POOL STATISTICS:")
        print("="*80)
        summary = pool.get_summary()
        print(f"Total Agents: {summary['total_agents']}")
        print(f"Enabled: {summary['enabled_agents']}")
        print(f"Total Requests: {summary['total_requests']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Cost: ${summary['total_cost']:.4f}")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Make sure to replace API keys with your actual keys")


if __name__ == "__main__":
    asyncio.run(main())
