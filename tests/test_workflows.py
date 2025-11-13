"""Tests for workflows."""

import pytest
from datetime import datetime
from factory.workflows.base_workflow import BaseWorkflow
from factory.core.workflow_engine import WorkflowResult, WorkflowStatus


class TestWorkflow(BaseWorkflow):
    """Test workflow implementation."""

    async def setup(self):
        self.validate_context(["test_param"])

    async def execute(self) -> WorkflowResult:
        result = WorkflowResult(
            workflow_id=self.workflow_id,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now(),
            steps_total=2
        )

        try:
            # Step 1
            result.outputs["step1"] = "result1"
            result.steps_completed += 1

            # Step 2
            result.outputs["step2"] = "result2"
            result.steps_completed += 1

            result.status = WorkflowStatus.COMPLETED
            result.completed_at = datetime.now()

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.errors.append(str(e))

        return result

    async def cleanup(self):
        pass


@pytest.mark.asyncio
async def test_workflow_lifecycle():
    """Test workflow lifecycle."""
    workflow = TestWorkflow(
        name="test",
        context={"test_param": "value"}
    )

    result = await workflow.run()

    assert result.status == WorkflowStatus.COMPLETED
    assert result.steps_completed == 2
    assert "step1" in result.outputs
    assert "step2" in result.outputs


@pytest.mark.asyncio
async def test_workflow_validation():
    """Test workflow context validation."""
    workflow = TestWorkflow(
        name="test",
        context={}  # Missing required test_param
    )

    with pytest.raises(ValueError, match="Missing required context keys"):
        await workflow.setup()


@pytest.mark.asyncio
async def test_workflow_error_handling():
    """Test workflow error handling."""
    class FailingWorkflow(BaseWorkflow):
        async def setup(self):
            pass

        async def execute(self) -> WorkflowResult:
            raise Exception("Test error")

        async def cleanup(self):
            pass

    workflow = FailingWorkflow("failing")

    # Should not raise - error should be captured
    result = await workflow.run()

    assert result.status == WorkflowStatus.FAILED
    assert len(result.errors) > 0
