# Creating Custom Workflows

Guide to building custom workflows for specific writing tasks.

## Workflow Basics

A workflow is a series of steps that execute in order, with automatic:
- Dependency resolution
- Error handling
- State management
- Progress tracking

## Workflow Structure

All workflows inherit from `BaseWorkflow`:

```python
from factory.workflows.base_workflow import BaseWorkflow
from factory.core.workflow_engine import WorkflowResult, WorkflowStatus
from datetime import datetime

class MyWorkflow(BaseWorkflow):
    def __init__(self, **kwargs):
        super().__init__(
            name="my-workflow",
            context=kwargs
        )
        # Initialize workflow-specific attributes

    async def setup(self):
        \"\"\"Prepare workflow for execution.\"\"\"
        # Validate required context
        self.validate_context(["required_param"])

        # Initialize resources
        # Load configuration
        # Setup connections

    async def execute(self) -> WorkflowResult:
        \"\"\"Execute main workflow logic.\"\"\"
        result = WorkflowResult(
            workflow_id=self.workflow_id,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now(),
            steps_total=3
        )

        try:
            # Step 1
            step1_output = await self._step_one()
            result.outputs["step1"] = step1_output
            result.steps_completed += 1

            # Step 2
            step2_output = await self._step_two(step1_output)
            result.outputs["step2"] = step2_output
            result.steps_completed += 1

            # Step 3
            step3_output = await self._step_three(step2_output)
            result.outputs["step3"] = step3_output
            result.steps_completed += 1

            result.status = WorkflowStatus.COMPLETED
            result.completed_at = datetime.now()

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.errors.append(str(e))
            result.completed_at = datetime.now()

        return result

    async def cleanup(self):
        \"\"\"Clean up workflow resources.\"\"\"
        # Close connections
        # Save state
        # Release resources

    async def _step_one(self):
        # Implementation
        pass

    async def _step_two(self, previous_output):
        # Implementation
        pass

    async def _step_three(self, previous_output):
        # Implementation
        pass
```

## Example: Scene Revision Workflow

```python
from factory.workflows.base_workflow import BaseWorkflow
from factory.core.agent_pool import AgentPool
from factory.knowledge.router import KnowledgeRouter

class SceneRevisionWorkflow(BaseWorkflow):
    \"\"\"Revise a scene using multiple agents for different aspects.\"\"\"

    def __init__(
        self,
        agent_pool: AgentPool,
        knowledge_router: KnowledgeRouter,
        scene_text: str,
        character_name: str,
        **kwargs
    ):
        super().__init__(name="scene-revision", context=kwargs)
        self.agent_pool = agent_pool
        self.knowledge_router = knowledge_router
        self.scene_text = scene_text
        self.character_name = character_name

    async def setup(self):
        # Validate inputs
        if not self.scene_text:
            raise ValueError("scene_text is required")

        # Gather character context
        self.character_context = await self.knowledge_router.query(
            f"Tell me about {self.character_name}"
        )

    async def execute(self) -> WorkflowResult:
        result = WorkflowResult(
            workflow_id=self.workflow_id,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now(),
            steps_total=3
        )

        try:
            # Step 1: Dialogue revision
            dialogue_revision = await self._revise_dialogue()
            result.outputs["dialogue"] = dialogue_revision
            result.steps_completed += 1

            # Step 2: Description enhancement
            description_revision = await self._enhance_descriptions(
                dialogue_revision
            )
            result.outputs["description"] = description_revision
            result.steps_completed += 1

            # Step 3: Voice consistency check
            final_revision = await self._check_voice_consistency(
                description_revision
            )
            result.outputs["final"] = final_revision
            result.steps_completed += 1

            result.status = WorkflowStatus.COMPLETED
            result.completed_at = datetime.now()

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.errors.append(str(e))

        return result

    async def cleanup(self):
        pass

    async def _revise_dialogue(self) -> str:
        prompt = f\"\"\"Revise the dialogue in this scene for character {self.character_name}.

Character context: {self.character_context.answer}

Scene:
{self.scene_text}

Focus on making dialogue more natural and character-consistent.\"\"\"

        response = await self.agent_pool.execute_single(
            "claude-sonnet-4.5",
            prompt
        )

        return response.output

    async def _enhance_descriptions(self, text: str) -> str:
        prompt = f\"\"\"Enhance the descriptive passages in this scene.

Scene:
{text}

Make descriptions more vivid without being purple prose.\"\"\"

        response = await self.agent_pool.execute_single(
            "gpt-4o",
            prompt
        )

        return response.output

    async def _check_voice_consistency(self, text: str) -> str:
        prompt = f\"\"\"Check voice consistency for {self.character_name}.

Scene:
{text}

Ensure consistent voice and fix any inconsistencies.\"\"\"

        response = await self.agent_pool.execute_single(
            "claude-sonnet-4.5",
            prompt
        )

        return response.output
```

## Using WorkflowEngine for Complex Dependencies

For workflows with complex dependencies, use WorkflowEngine:

```python
from factory.core.workflow_engine import Workflow, WorkflowStep, WorkflowEngine

class ComplexWorkflow(Workflow):
    def define_steps(self):
        # Independent steps
        self.add_step(
            name="gather_character_data",
            function=self._gather_characters
        )
        self.add_step(
            name="gather_world_data",
            function=self._gather_world
        )

        # Depends on both character and world data
        self.add_step(
            name="generate_outline",
            function=self._generate_outline,
            dependencies=["gather_character_data", "gather_world_data"]
        )

        # Depends on outline
        self.add_step(
            name="generate_first_chapter",
            function=self._generate_chapter,
            dependencies=["generate_outline"]
        )

    async def _gather_characters(self, context):
        # Implementation
        return {"characters": [...]}

    async def _gather_world(self, context):
        # Implementation
        return {"world": {...}}

    async def _generate_outline(self, context):
        # Access previous step outputs
        characters = context["gather_character_data"]
        world = context["gather_world_data"]
        # Generate outline
        return {"outline": [...]}

    async def _generate_chapter(self, context):
        outline = context["generate_outline"]
        # Generate chapter
        return {"chapter": "..."}

# Execute
engine = WorkflowEngine()
workflow = ComplexWorkflow("complex-workflow")
result = await engine.run_workflow(workflow, parallel=True)
```

## Best Practices

1. **Validate Early**: Check all inputs in `setup()`
2. **Error Handling**: Wrap steps in try/except
3. **Logging**: Log progress for debugging
4. **Incremental Progress**: Update `steps_completed`
5. **Store Outputs**: Save all intermediate results
6. **Clean Resources**: Always cleanup in `cleanup()`
7. **Reusable Steps**: Extract common logic to methods
8. **Configuration**: Use context for parameters

## Testing Workflows

```python
import pytest
from factory.workflows.myworkflow import MyWorkflow

@pytest.mark.asyncio
async def test_workflow():
    workflow = MyWorkflow(
        required_param="value"
    )

    result = await workflow.run()

    assert result.status == WorkflowStatus.COMPLETED
    assert result.steps_completed == 3
    assert "final" in result.outputs
```

## Common Patterns

### Multi-Agent Comparison
```python
results = []
for agent in ["claude", "gpt4o", "gemini"]:
    output = await self.agent_pool.execute_single(agent, prompt)
    results.append(output)
# Compare and select best
```

### Iterative Refinement
```python
text = original_text
for i in range(3):  # 3 rounds of refinement
    text = await self._refine_step(text)
return text
```

### Conditional Execution
```python
if quality_score < threshold:
    text = await self._enhance(text)
else:
    text = text  # Use as-is
```

### Knowledge Integration
```python
context = await self.knowledge_router.query(query)
prompt = f"Context: {context.answer}\n\nTask: ..."
```
