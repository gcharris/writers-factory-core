"""Tests for model comparison tool."""

import pytest

from factory.tools import ModelComparisonTool, ComparisonResult


class TestModelComparisonTool:
    """Test model comparison tool."""

    def test_tool_creation(self):
        """Test creating tool."""
        tool = ModelComparisonTool()

        assert tool is not None
        assert tool.comparison_history == []

    @pytest.mark.asyncio
    async def test_compare_two_models(self):
        """Test comparing two models."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Write a short story about space",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        assert isinstance(result, ComparisonResult)
        assert len(result.outputs) == 2
        assert result.total_cost > 0
        assert len(result.diffs) > 0

    @pytest.mark.asyncio
    async def test_compare_four_models(self):
        """Test comparing maximum 4 models."""
        tool = ModelComparisonTool()

        models = ["claude-sonnet-4.5", "claude-opus-4", "gpt-4o", "gemini-2-flash"]

        result = await tool.compare_models(
            prompt="Test prompt",
            models=models
        )

        assert len(result.outputs) == 4
        assert len(result.models_compared) == 4
        # Should have 6 pairwise diffs (4 choose 2)
        assert len(result.diffs) == 6

    @pytest.mark.asyncio
    async def test_compare_less_than_two_models_fails(self):
        """Test that comparing less than 2 models fails."""
        tool = ModelComparisonTool()

        with pytest.raises(ValueError, match="at least 2 models"):
            await tool.compare_models(
                prompt="Test",
                models=["claude-sonnet-4.5"]
            )

    @pytest.mark.asyncio
    async def test_compare_more_than_four_models_fails(self):
        """Test that comparing more than 4 models fails."""
        tool = ModelComparisonTool()

        with pytest.raises(ValueError, match="Maximum 4 models"):
            await tool.compare_models(
                prompt="Test",
                models=["m1", "m2", "m3", "m4", "m5"]
            )


class TestDiffComputation:
    """Test diff computation."""

    @pytest.mark.asyncio
    async def test_diffs_computed_for_all_pairs(self):
        """Test diffs computed for all model pairs."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Test",
            models=["claude-sonnet-4.5", "gpt-4o", "gemini-2-flash"]
        )

        # 3 models = 3 pairs
        assert len(result.diffs) == 3

        # Check specific pairs exist
        assert any(
            ("claude-sonnet-4.5", "gpt-4o") == pair or ("gpt-4o", "claude-sonnet-4.5") == pair
            for pair in result.diffs.keys()
        )

    def test_render_diff(self):
        """Test rendering visual diff."""
        tool = ModelComparisonTool()

        # Create mock result with diff
        from factory.tools.model_comparison import ModelOutput

        result = ComparisonResult(
            prompt="Test",
            outputs=[
                ModelOutput("model1", "text A", 0.05, 100, 200, 1.5),
                ModelOutput("model2", "text B", 0.05, 100, 200, 1.5)
            ],
            diffs={
                ("model1", "model2"): [
                    "--- model1",
                    "+++ model2",
                    "@@ -1,1 +1,1 @@",
                    "-text A",
                    "+text B"
                ]
            }
        )

        panel = tool.render_diff(result, "model1", "model2")

        assert panel is not None


class TestPreferenceTracking:
    """Test preference tracking."""

    @pytest.mark.asyncio
    async def test_save_preference(self):
        """Test saving winner preference."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Test",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        await tool.save_preference(result, "claude-sonnet-4.5", "Better prose")

        assert result.winner == "claude-sonnet-4.5"
        assert result.user_notes == "Better prose"

    @pytest.mark.asyncio
    async def test_save_invalid_winner_fails(self):
        """Test that saving invalid winner fails."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Test",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        with pytest.raises(ValueError, match="Winner must be one of"):
            await tool.save_preference(result, "non-existent-model")

    @pytest.mark.asyncio
    async def test_preference_stats(self):
        """Test preference statistics."""
        tool = ModelComparisonTool()

        # Run multiple comparisons
        result1 = await tool.compare_models("Test 1", ["model-a", "model-b"])
        await tool.save_preference(result1, "model-a")

        result2 = await tool.compare_models("Test 2", ["model-a", "model-c"])
        await tool.save_preference(result2, "model-a")

        result3 = await tool.compare_models("Test 3", ["model-b", "model-c"])
        await tool.save_preference(result3, "model-c")

        stats = tool.get_preference_stats()

        assert stats["model-a"] == 2
        assert stats["model-c"] == 1
        assert stats.get("model-b", 0) == 0

    def test_render_preference_stats(self):
        """Test rendering preference statistics."""
        tool = ModelComparisonTool()

        # Empty stats
        panel = tool.render_preference_stats()
        assert panel is not None


class TestComparisonRendering:
    """Test comparison rendering."""

    @pytest.mark.asyncio
    async def test_render_comparison(self):
        """Test rendering comparison results."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Test prompt",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        panel = tool.render_comparison(result)

        assert panel is not None

    @pytest.mark.asyncio
    async def test_render_comparison_with_winner(self):
        """Test rendering comparison with winner."""
        tool = ModelComparisonTool()

        result = await tool.compare_models(
            prompt="Test",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        await tool.save_preference(result, "claude-sonnet-4.5")

        panel = tool.render_comparison(result)

        assert panel is not None
        assert result.winner == "claude-sonnet-4.5"


class TestComparisonHistory:
    """Test comparison history tracking."""

    @pytest.mark.asyncio
    async def test_history_tracking(self):
        """Test that comparisons are tracked in history."""
        tool = ModelComparisonTool()

        assert len(tool.comparison_history) == 0

        await tool.compare_models("Test 1", ["m1", "m2"])
        assert len(tool.comparison_history) == 1

        await tool.compare_models("Test 2", ["m3", "m4"])
        assert len(tool.comparison_history) == 2

    @pytest.mark.asyncio
    async def test_history_contains_results(self):
        """Test history contains complete results."""
        tool = ModelComparisonTool()

        await tool.compare_models("First prompt", ["model-a", "model-b"])

        assert len(tool.comparison_history) == 1
        result = tool.comparison_history[0]
        assert result.prompt == "First prompt"
        assert result.models_compared == ["model-a", "model-b"]
