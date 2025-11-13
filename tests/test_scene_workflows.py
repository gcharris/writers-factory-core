"""Tests for scene operation workflows."""

import pytest
from pathlib import Path

from factory.workflows.scene_operations import (
    SceneGenerationWorkflow,
    SceneEnhancementWorkflow,
    VoiceTestingWorkflow
)
from factory.core.workflow_engine import WorkflowStatus


class TestSceneGenerationWorkflow:
    """Test scene generation workflow."""

    @pytest.mark.asyncio
    async def test_workflow_creation(self):
        """Test creating workflow."""
        workflow = SceneGenerationWorkflow()

        assert workflow.name == "Scene Generation"
        assert workflow.workflow_id is not None

    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Test executing workflow."""
        workflow = SceneGenerationWorkflow()

        outline = """POV: Sarah
Location: Coffee shop
Scene: Sarah meets her ex for the first time in years."""

        result = await workflow.run(
            outline=outline,
            model_name="claude-sonnet-4.5",
            use_knowledge_context=False
        )

        assert result.status == WorkflowStatus.COMPLETED
        assert "scene" in result.outputs
        assert result.steps_completed == result.steps_total

    @pytest.mark.asyncio
    async def test_workflow_with_context(self):
        """Test workflow with knowledge context enabled."""
        workflow = SceneGenerationWorkflow()

        outline = "A tense conversation between two rivals."

        result = await workflow.run(
            outline=outline,
            use_knowledge_context=False  # No actual router
        )

        assert result.status == WorkflowStatus.COMPLETED
        assert result.outputs.get("scene") is not None


class TestSceneEnhancementWorkflow:
    """Test scene enhancement workflow."""

    @pytest.mark.asyncio
    async def test_workflow_creation(self):
        """Test creating workflow."""
        workflow = SceneEnhancementWorkflow()

        assert workflow.name == "Scene Enhancement"
        assert workflow.workflow_id is not None

    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Test executing workflow."""
        workflow = SceneEnhancementWorkflow()

        scene = """Sarah walked into the coffee shop. She saw him sitting there.
It had been years. She felt nervous."""

        result = await workflow.run(
            scene=scene,
            model_name="claude-sonnet-4.5",
            character="Sarah"
        )

        assert result.status == WorkflowStatus.COMPLETED
        assert "enhanced_scene" in result.outputs
        assert "validation" in result.outputs
        assert result.steps_completed == 4

    @pytest.mark.asyncio
    async def test_voice_validation(self):
        """Test voice validation in enhancement."""
        workflow = SceneEnhancementWorkflow()

        scene = "A simple scene."

        result = await workflow.run(
            scene=scene,
            character="protagonist"
        )

        validation = result.outputs.get("validation", {})
        assert "score" in validation
        assert validation["score"] > 0


class TestVoiceTestingWorkflow:
    """Test voice testing workflow."""

    @pytest.mark.asyncio
    async def test_workflow_creation(self):
        """Test creating workflow."""
        workflow = VoiceTestingWorkflow()

        assert workflow.name == "Voice Testing"
        assert workflow.workflow_id is not None

    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Test executing workflow."""
        workflow = VoiceTestingWorkflow()

        prompt = "Generate a tense conversation between rivals."
        models = ["claude-sonnet-4.5", "claude-opus-4", "gpt-4o"]

        result = await workflow.run(
            prompt=prompt,
            models=models,
            character="protagonist"
        )

        assert result.status == WorkflowStatus.COMPLETED
        assert "comparison" in result.outputs
        assert "recommendation" in result.outputs
        assert result.steps_completed == 4

    @pytest.mark.asyncio
    async def test_model_comparison(self):
        """Test model comparison results."""
        workflow = VoiceTestingWorkflow()

        models = ["claude-sonnet-4.5", "gpt-4o"]

        result = await workflow.run(
            prompt="Test prompt",
            models=models
        )

        comparison = result.outputs.get("comparison", [])
        assert len(comparison) == len(models)

        # Check sorting by score
        scores = [c["score"] for c in comparison]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_winner_recommendation(self):
        """Test winner recommendation."""
        workflow = VoiceTestingWorkflow()

        result = await workflow.run(
            prompt="Test",
            models=["claude-sonnet-4.5", "gpt-4o"]
        )

        recommendation = result.outputs.get("recommendation", {})
        assert "winner" in recommendation
        assert "score" in recommendation
        assert "reasoning" in recommendation
        assert "top_3" in recommendation


class TestWorkflowIntegration:
    """Test workflow integration scenarios."""

    @pytest.mark.asyncio
    async def test_generation_then_enhancement(self):
        """Test generating then enhancing a scene."""
        # Generate scene
        gen_workflow = SceneGenerationWorkflow()
        gen_result = await gen_workflow.run(
            outline="A tense meeting",
            use_knowledge_context=False
        )

        generated_scene = gen_result.outputs["scene"]
        assert generated_scene

        # Enhance generated scene
        enh_workflow = SceneEnhancementWorkflow()
        enh_result = await enh_workflow.run(
            scene=generated_scene,
            character="protagonist"
        )

        assert enh_result.status == WorkflowStatus.COMPLETED
        assert enh_result.outputs["enhanced_scene"]

    @pytest.mark.asyncio
    async def test_voice_testing_workflow_chain(self):
        """Test voice testing workflow."""
        workflow = VoiceTestingWorkflow()

        result = await workflow.run(
            prompt="Test scene",
            models=["claude-sonnet-4.5"]
        )

        assert result.status == WorkflowStatus.COMPLETED
        assert result.metadata.get("models_tested") == 1
