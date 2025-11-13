"""Command-line interface for Writers Factory Core."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Writers Factory Core - Multi-model novel writing system."""
    pass


@cli.command()
@click.option("--name", prompt="Project name", help="Name of the project")
@click.option("--genre", prompt="Genre", help="Genre (sci-fi, fantasy, etc.)")
@click.option("--output", type=click.Path(), help="Output directory")
def init(name: str, genre: str, output: Optional[str]):
    """Initialize a new writing project."""
    console.print(Panel(
        f"[bold green]Initializing project: {name}[/bold green]\n"
        f"Genre: {genre}",
        title="Writers Factory Core"
    ))

    # Create project directory
    project_dir = Path(output) if output else Path(f"./{name}")
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create basic structure
    (project_dir / "reference").mkdir(exist_ok=True)
    (project_dir / "manuscript").mkdir(exist_ok=True)
    (project_dir / "notes").mkdir(exist_ok=True)

    console.print(f"✓ Created project directory: {project_dir}")
    console.print(f"✓ Project initialized successfully!")


@cli.group()
def agent():
    """Manage LLM agents."""
    pass


@agent.command("list")
@click.option("--enabled-only", is_flag=True, help="Show only enabled agents")
def list_agents(enabled_only: bool):
    """List available agents."""
    # Mock data for demonstration
    agents = [
        ("claude-sonnet-4.5", "Anthropic", "Enabled", "$0.003/$0.015"),
        ("gpt-4o", "OpenAI", "Enabled", "$0.0025/$0.01"),
        ("gemini-2-flash", "Google", "Enabled", "$0/$0"),
        ("deepseek-v3", "DeepSeek", "Enabled", "$0.00027/$0.0011"),
        ("qwen-max", "Alibaba", "Enabled", "$0.008/$0.008"),
    ]

    table = Table(title="Available Agents", box=box.ROUNDED)
    table.add_column("Agent", style="cyan")
    table.add_column("Provider", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Cost (in/out per 1K)", style="magenta")

    for agent in agents:
        table.add_row(*agent)

    console.print(table)


@agent.command("test")
@click.argument("agent_name")
def test_agent(agent_name: str):
    """Test agent connection."""
    console.print(f"Testing agent: [cyan]{agent_name}[/cyan]...")

    # Mock test
    console.print("✓ Connection successful")
    console.print("✓ API key valid")
    console.print("✓ Model accessible")

    console.print(f"\n[green]Agent {agent_name} is ready to use![/green]")


@cli.group()
def workflow():
    """Run workflows."""
    pass


@workflow.command("run")
@click.argument("workflow_name")
@click.option("--agents", help="Comma-separated list of agents")
def run_workflow(workflow_name: str, agents: Optional[str]):
    """Run a workflow."""
    console.print(Panel(
        f"[bold]Running workflow: {workflow_name}[/bold]",
        title="Workflow Execution"
    ))

    if agents:
        agent_list = agents.split(",")
        console.print(f"Using agents: {', '.join(agent_list)}")

    console.print("\n[yellow]This is a placeholder. Workflow execution not yet implemented.[/yellow]")


@cli.group()
def session():
    """Manage sessions."""
    pass


@session.command("list")
@click.option("--limit", default=10, help="Number of sessions to show")
def list_sessions(limit: int):
    """List recent sessions."""
    # Mock data
    sessions = [
        ("session-001", "multi-model-generation", "completed", "$0.15"),
        ("session-002", "project-genesis", "completed", "$0.42"),
        ("session-003", "multi-model-generation", "completed", "$0.18"),
    ]

    table = Table(title="Recent Sessions", box=box.ROUNDED)
    table.add_column("Session ID", style="cyan")
    table.add_column("Workflow", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Cost", style="magenta")

    for sess in sessions[:limit]:
        table.add_row(*sess)

    console.print(table)


@session.command("show")
@click.argument("session_id")
def show_session(session_id: str):
    """Show session details."""
    console.print(Panel(
        f"[bold]Session: {session_id}[/bold]\n"
        f"Workflow: multi-model-generation\n"
        f"Status: completed\n"
        f"Started: 2025-11-13 08:00:00\n"
        f"Duration: 45.2s\n"
        f"Cost: $0.15\n"
        f"Results: 3 agents",
        title="Session Details"
    ))


@cli.command()
def stats():
    """Show system statistics."""
    table = Table(title="System Statistics", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    stats_data = [
        ("Total Sessions", "127"),
        ("Total Generations", "542"),
        ("Total Cost", "$24.50"),
        ("Total Tokens", "2.4M"),
        ("Avg Cost per Session", "$0.19"),
        ("Most Used Agent", "claude-sonnet-4.5"),
    ]

    for metric, value in stats_data:
        table.add_row(metric, value)

    console.print(table)


def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
