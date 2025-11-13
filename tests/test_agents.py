"""Tests for agent system."""

import pytest
from factory.agents.base_agent import BaseAgent, AgentConfig


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    async def generate(self, prompt: str, temperature: float = 0.8, max_tokens=None, **kwargs):
        return {
            "output": f"Mock response to: {prompt[:50]}",
            "tokens_input": len(prompt) // 4,
            "tokens_output": 100,
            "cost": 0.01,
            "model_version": "mock-1.0",
            "metadata": {}
        }


def test_agent_config():
    """Test agent configuration."""
    config = AgentConfig(
        name="test-agent",
        model="test-model",
        api_key="test-key",
        context_window=4096,
        max_output=2048,
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.002
    )

    assert config.name == "test-agent"
    assert config.model == "test-model"
    assert config.context_window == 4096


def test_agent_creation():
    """Test agent creation."""
    config = AgentConfig(
        name="mock-agent",
        model="mock-model",
        api_key="test-key"
    )

    agent = MockAgent(config)

    assert agent.name == "mock-agent"
    assert agent.model == "mock-model"
    assert agent._request_count == 0


@pytest.mark.asyncio
async def test_agent_generation():
    """Test agent generation."""
    config = AgentConfig(
        name="mock-agent",
        model="mock-model"
    )
    agent = MockAgent(config)

    result = await agent.generate("Test prompt")

    assert "output" in result
    assert "tokens_input" in result
    assert "tokens_output" in result
    assert "cost" in result


def test_agent_cost_calculation():
    """Test agent cost calculation."""
    config = AgentConfig(
        name="test",
        model="test",
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.002
    )
    agent = MockAgent(config)

    cost = agent.calculate_cost(1000, 2000)

    assert cost == pytest.approx(0.005)  # 1000 * 0.001 + 2000 * 0.002


def test_agent_stats():
    """Test agent statistics."""
    config = AgentConfig(name="test", model="test")
    agent = MockAgent(config)

    # Update stats
    agent.update_stats(100, 200, 0.01)
    agent.update_stats(150, 250, 0.015)

    stats = agent.get_stats()

    assert stats["request_count"] == 2
    assert stats["total_tokens"] == 700  # (100+200) + (150+250)
    assert stats["total_cost"] == pytest.approx(0.025)


def test_agent_stats_reset():
    """Test agent stats reset."""
    config = AgentConfig(name="test", model="test")
    agent = MockAgent(config)

    agent.update_stats(100, 200, 0.01)
    agent.reset_stats()

    stats = agent.get_stats()

    assert stats["request_count"] == 0
    assert stats["total_tokens"] == 0
    assert stats["total_cost"] == 0.0
