"""Project setup example.

Demonstrates using the project genesis workflow to initialize a new writing project.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.core.agent_pool import AgentPool
from factory.workflows.project_genesis.workflow import ProjectGenesisWorkflow


async def main():
    """Run project setup example."""
    print("=== Project Genesis Example ===\n")

    # Create agent pool (mock for example)
    pool = AgentPool()

    # Project details
    project_name = "Quantum Dreams"
    genre = "science fiction thriller"
    themes = [
        "consciousness and identity",
        "technology and humanity",
        "quantum physics and reality"
    ]
    basic_idea = """A neuroscientist discovers a way to transfer human consciousness
into quantum computers, but finds that the digital copies develop their own
desires and agendas, leading to a conflict between biological and digital humanity."""

    print(f"Project: {project_name}")
    print(f"Genre: {genre}")
    print(f"Themes: {', '.join(themes)}")
    print(f"\nConcept: {basic_idea}\n")

    print("Initializing project...")
    print("(Note: This is a mock example - actual generation requires API keys)\n")

    try:
        # Create workflow
        workflow = ProjectGenesisWorkflow(
            agent_pool=pool,
            project_name=project_name,
            genre=genre,
            themes=themes,
            basic_idea=basic_idea,
            output_dir=Path(f"./{project_name}"),
            num_characters=5,
            act_structure=3
        )

        # Run workflow
        result = await workflow.run()

        # Display results
        if result.success:
            print("="*80)
            print("PROJECT INITIALIZED SUCCESSFULLY!")
            print("="*80)

            print(f"\nWorkflow ID: {result.workflow_id}")
            print(f"Duration: {result.duration:.2f}s")
            print(f"Steps Completed: {result.steps_completed}/{result.steps_total}")

            print("\nGenerated Components:")
            if "characters" in result.outputs:
                print(f"  - {len(result.outputs['characters'])} characters")
            if "world" in result.outputs:
                print(f"  - World/setting details")
            if "structure" in result.outputs:
                print(f"  - {len(result.outputs['structure']['acts'])}-act structure")

            print(f"\nProject directory created at: ./{project_name}/")
            print("\nDirectory structure:")
            print("  reference/")
            print("    characters/")
            print("    worldbuilding/")
            print("  manuscript/")
            print("  notes/")
            print("  PROJECT.md")

        else:
            print("Project initialization failed:")
            for error in result.errors:
                print(f"  - {error}")

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
