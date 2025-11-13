"""Base workflow class for all workflows."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from factory.core.workflow_engine import Workflow, WorkflowResult

logger = logging.getLogger(__name__)


class BaseWorkflow(Workflow, ABC):
    """Base class for all workflows with standard lifecycle.

    Provides:
    - Setup phase for initialization
    - Execute phase for main workflow
    - Cleanup phase for resource cleanup
    - Error handling and recovery
    """

    def __init__(
        self,
        name: str,
        workflow_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize workflow.

        Args:
            name: Workflow name
            workflow_id: Unique identifier
            context: Initial context
        """
        super().__init__(name, workflow_id, context)
        self._setup_complete = False
        self._cleanup_complete = False

    @abstractmethod
    async def setup(self) -> None:
        """Setup workflow resources.

        This method should:
        - Validate configuration
        - Initialize resources
        - Prepare context
        """
        pass

    @abstractmethod
    async def execute(self) -> WorkflowResult:
        """Execute the main workflow logic.

        Returns:
            WorkflowResult with execution details
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup workflow resources.

        This method should:
        - Close connections
        - Save state
        - Release resources
        """
        pass

    async def run(self) -> WorkflowResult:
        """Run complete workflow lifecycle.

        Returns:
            WorkflowResult from execution
        """
        try:
            # Setup
            logger.info(f"Setting up workflow '{self.name}'")
            await self.setup()
            self._setup_complete = True

            # Execute
            logger.info(f"Executing workflow '{self.name}'")
            result = await self.execute()

            return result

        finally:
            # Always cleanup
            if not self._cleanup_complete:
                logger.info(f"Cleaning up workflow '{self.name}'")
                await self.cleanup()
                self._cleanup_complete = True

    def validate_context(self, required_keys: list) -> None:
        """Validate required context keys exist.

        Args:
            required_keys: List of required context keys

        Raises:
            ValueError: If required keys are missing
        """
        missing = [key for key in required_keys if key not in self.context]
        if missing:
            raise ValueError(f"Missing required context keys: {missing}")
