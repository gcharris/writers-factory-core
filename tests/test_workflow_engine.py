"""Tests for workflow engine."""

import pytest
from datetime import datetime

from factory.core.workflow_engine import (
    Workflow,
    WorkflowEngine,
    WorkflowStep,
    WorkflowStatus,
    StepStatus,
)


class MockWorkflow(Workflow):
    """Mock workflow for testing."""

    def define_steps(self):
        self.add_step("step1", lambda ctx: "result1")
        self.add_step("step2", lambda ctx: "result2", dependencies=["step1"])
        self.add_step("step3", lambda ctx: "result3", dependencies=["step2"])


@pytest.mark.asyncio
async def test_workflow_execution():
    """Test basic workflow execution."""
    engine = WorkflowEngine()
    workflow = MockWorkflow("test-workflow")

    result = await engine.run_workflow(workflow, parallel=False)

    assert result.status == WorkflowStatus.COMPLETED
    assert result.steps_completed == 3
    assert result.success


@pytest.mark.asyncio
async def test_workflow_step_dependencies():
    """Test workflow with step dependencies."""
    workflow = Workflow("test")

    workflow.add_step("a", lambda ctx: "a")
    workflow.add_step("b", lambda ctx: "b", dependencies=["a"])
    workflow.add_step("c", lambda ctx: "c", dependencies=["a", "b"])

    engine = WorkflowEngine()
    result = await engine.run_workflow(workflow)

    assert result.success
    assert len(workflow._step_outputs) == 3


def test_workflow_step_creation():
    """Test workflow step creation."""
    step = WorkflowStep(
        name="test_step",
        function=lambda ctx: "result",
        dependencies=["dep1", "dep2"],
        timeout=30,
        retry_count=3
    )

    assert step.name == "test_step"
    assert step.dependencies == ["dep1", "dep2"]
    assert step.timeout == 30
    assert step.retry_count == 3
    assert step.status == StepStatus.PENDING


def test_workflow_validation():
    """Test workflow validation."""
    workflow = Workflow("test")
    workflow.add_step("step1", lambda ctx: "result")
    workflow.add_step("step2", lambda ctx: "result", dependencies=["nonexistent"])

    engine = WorkflowEngine()

    with pytest.raises(ValueError, match="depends on unknown step"):
        engine._validate_workflow(workflow)


@pytest.mark.asyncio
async def test_workflow_error_handling():
    """Test workflow error handling."""
    def failing_step(ctx):
        raise Exception("Test error")

    workflow = Workflow("test")
    workflow.add_step("failing", failing_step, required=True)

    engine = WorkflowEngine()
    result = await engine.run_workflow(workflow)

    assert result.status == WorkflowStatus.FAILED
    assert len(result.errors) > 0
