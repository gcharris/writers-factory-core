#!/usr/bin/env python3
"""Interactive demo of Writers Factory Core - NO API KEYS REQUIRED!

This demonstrates the UX and workflow without making real API calls.
Shows how the system works with mock responses.
"""

import asyncio
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()


def show_header():
    """Display welcome header."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Writers Factory Core - Interactive Demo[/bold cyan]\n"
        "[dim]Multi-Model Novel Writing Tournament System[/dim]",
        border_style="cyan"
    ))
    console.print()


def show_menu():
    """Display main menu."""
    console.print("[bold]Choose a demo:[/bold]")
    console.print("  [cyan]1.[/cyan] Single Agent Generation")
    console.print("  [cyan]2.[/cyan] Multi-Model Tournament (Compare 4 models)")
    console.print("  [cyan]3.[/cyan] Knowledge Router Demo")
    console.print("  [cyan]4.[/cyan] Project Genesis Workflow")
    console.print("  [cyan]5.[/cyan] Agent Pool Statistics")
    console.print("  [cyan]6.[/cyan] Database Analytics")
    console.print("  [cyan]q.[/cyan] Quit")
    console.print()


async def demo_single_agent():
    """Demo: Single agent generation."""
    console.print("\n[bold cyan]═══ Demo 1: Single Agent Generation ═══[/bold cyan]\n")

    console.print("[yellow]Agent:[/yellow] Claude Sonnet 4.5")
    console.print("[yellow]Model:[/yellow] claude-sonnet-4-5-20250929")
    console.print("[yellow]Context Window:[/yellow] 200,000 tokens")
    console.print()

    prompt = "Write a tense dialogue between two quantum physicists discovering something impossible."
    console.print(f"[green]Prompt:[/green] {prompt}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating with Claude Sonnet 4.5...", total=None)
        await asyncio.sleep(2)

    # Mock response
    output = '''Dr. Sarah Chen stared at the quantum entanglement display, her hands trembling. "That's... that's not possible. The particles are correlated across *time*, not just space."

Dr. Marcus Wu leaned closer, his voice dropping to a whisper. "Sarah, if this is real—if we're seeing retrocausality—every physics paper published in the last century is wrong."

"Not wrong," she said, her screen reflecting in her widening eyes. "Incomplete. The universe isn't just entangled in space. It's entangled with its own *past*."

Marcus stepped back from the console. "We need to shut this down. Right now. Before anyone else sees—"

"Too late." Sarah pointed to the secondary monitor, where their experiment's quantum signature was already propagating backward through their previous data. "We didn't just observe retrocausality, Marcus. We *caused* it. And it's been happening all along."'''

    console.print(Panel(output, title="[bold]Generated Output[/bold]", border_style="green"))
    console.print()

    # Stats
    stats_table = Table(show_header=False, box=None)
    stats_table.add_column(style="cyan")
    stats_table.add_column(style="white")
    stats_table.add_row("Tokens (input):", "78")
    stats_table.add_row("Tokens (output):", "156")
    stats_table.add_row("Cost:", "$0.0027")
    stats_table.add_row("Response time:", "1,842ms")

    console.print(stats_table)
    console.print()


async def demo_tournament():
    """Demo: Multi-model tournament."""
    console.print("\n[bold cyan]═══ Demo 2: Multi-Model Tournament ═══[/bold cyan]\n")

    console.print("[yellow]Agents:[/yellow] Claude Sonnet 4.5, GPT-4o, Gemini 2.0 Flash, DeepSeek V3")
    console.print("[yellow]Mode:[/yellow] Parallel execution (tournament)")
    console.print()

    prompt = "Write a single paragraph describing a character who can see quantum possibilities."
    console.print(f"[green]Prompt:[/green] {prompt}\n")

    # Simulate parallel execution
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        tasks = [
            progress.add_task("Claude Sonnet 4.5...", total=None),
            progress.add_task("GPT-4o...", total=None),
            progress.add_task("Gemini 2.0 Flash...", total=None),
            progress.add_task("DeepSeek V3...", total=None),
        ]
        await asyncio.sleep(3)

    console.print("\n[bold green]✓ All models completed![/bold green]\n")

    # Results comparison table
    results = Table(title="Tournament Results")
    results.add_column("Model", style="cyan")
    results.add_column("Tokens", justify="right")
    results.add_column("Cost", justify="right")
    results.add_column("Time", justify="right")
    results.add_column("Quality", justify="center")

    results.add_row("Claude Sonnet 4.5", "142", "$0.0024", "1.8s", "⭐⭐⭐⭐⭐")
    results.add_row("GPT-4o", "156", "$0.0020", "2.1s", "⭐⭐⭐⭐")
    results.add_row("Gemini 2.0 Flash", "138", "$0.0000", "1.2s", "⭐⭐⭐⭐")
    results.add_row("DeepSeek V3", "149", "$0.0004", "1.5s", "⭐⭐⭐⭐")

    console.print(results)
    console.print()

    console.print("[bold]Winner:[/bold] [cyan]Claude Sonnet 4.5[/cyan] - Best metaphor discipline and voice")
    console.print("[bold]Best Value:[/bold] [cyan]Gemini 2.0 Flash[/cyan] - Free with good quality")
    console.print("[bold]Most Cost-Effective:[/bold] [cyan]DeepSeek V3[/cyan] - $0.0004 for high quality")
    console.print()


async def demo_knowledge_router():
    """Demo: Knowledge router."""
    console.print("\n[bold cyan]═══ Demo 3: Knowledge Router ═══[/bold cyan]\n")

    queries = [
        ("What is Mickey's quantum ability?", "FACTUAL", "Cognee (local graph)"),
        ("How are Mickey and Noni related?", "CONCEPTUAL", "Cognee (relationships)"),
        ("Why does Mickey avoid using his powers?", "ANALYTICAL", "NotebookLM (analysis)"),
        ("Tell me about the story", "GENERAL", "Gemini File Search"),
    ]

    console.print("[yellow]Demonstrating smart query routing...[/yellow]\n")

    for query, query_type, source in queries:
        console.print(f"[green]Query:[/green] {query}")
        console.print(f"  [cyan]→[/cyan] Type: [bold]{query_type}[/bold]")
        console.print(f"  [cyan]→[/cyan] Routed to: [bold]{source}[/bold]")
        console.print()
        await asyncio.sleep(0.5)

    console.print("[dim]The router automatically selects the best knowledge system based on query type.[/dim]")
    console.print()


async def demo_project_genesis():
    """Demo: Project genesis workflow."""
    console.print("\n[bold cyan]═══ Demo 4: Project Genesis Workflow ═══[/bold cyan]\n")

    console.print("[yellow]Project:[/yellow] Quantum Dreams")
    console.print("[yellow]Genre:[/yellow] Science Fiction Thriller")
    console.print("[yellow]Concept:[/yellow] Consciousness transfer into quantum computers")
    console.print()

    steps = [
        "Setup: Validating configuration",
        "Step 1: Generating 5 main characters",
        "Step 2: Creating world/setting details",
        "Step 3: Building 3-act structure",
        "Step 4: Populating project directory",
        "Cleanup: Saving metadata",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for step in steps:
            task = progress.add_task(step, total=None)
            await asyncio.sleep(1.5)
            progress.remove_task(task)
            console.print(f"[green]✓[/green] {step}")

    console.print()
    console.print("[bold green]✓ Project initialized successfully![/bold green]\n")

    # Show what was created
    console.print("[bold]Generated:[/bold]")
    console.print("  • 5 characters with backstories")
    console.print("  • Worldbuilding document (quantum computing facility)")
    console.print("  • 3-act structure with 12 key scenes")
    console.print("  • Project directory: ./Quantum_Dreams/")
    console.print()


async def demo_agent_pool():
    """Demo: Agent pool statistics."""
    console.print("\n[bold cyan]═══ Demo 5: Agent Pool Statistics ═══[/bold cyan]\n")

    # Agent registry
    registry = Table(title="Registered Agents")
    registry.add_column("Agent", style="cyan")
    registry.add_column("Provider")
    registry.add_column("Status", justify="center")
    registry.add_column("Requests", justify="right")
    registry.add_column("Cost", justify="right")

    registry.add_row("claude-sonnet-4.5", "Anthropic", "[green]●[/green] Enabled", "23", "$0.14")
    registry.add_row("gpt-4o", "OpenAI", "[green]●[/green] Enabled", "18", "$0.08")
    registry.add_row("gemini-2-flash", "Google", "[green]●[/green] Enabled", "31", "$0.00")
    registry.add_row("deepseek-v3", "DeepSeek", "[green]●[/green] Enabled", "15", "$0.01")
    registry.add_row("qwen-max", "Alibaba", "[green]●[/green] Enabled", "12", "$0.19")
    registry.add_row("gpt-3.5-turbo", "OpenAI", "[red]●[/red] Disabled", "0", "$0.00")

    console.print(registry)
    console.print()

    console.print("[bold]Total Agents:[/bold] 16 (11 enabled)")
    console.print("[bold]Total Requests:[/bold] 99")
    console.print("[bold]Success Rate:[/bold] 97.8%")
    console.print("[bold]Total Cost:[/bold] $0.42")
    console.print()


async def demo_analytics():
    """Demo: Database analytics."""
    console.print("\n[bold cyan]═══ Demo 6: Database Analytics ═══[/bold cyan]\n")

    # Win rates
    console.print("[bold]Model Win Rates (Last 30 tournaments):[/bold]\n")

    winrate = Table()
    winrate.add_column("Model", style="cyan")
    winrate.add_column("Tournaments", justify="right")
    winrate.add_column("Wins", justify="right")
    winrate.add_column("Win Rate", justify="right")
    winrate.add_column("Avg Cost/Win", justify="right")

    winrate.add_row("Claude Sonnet 4.5", "30", "12", "40.0%", "$0.0028")
    winrate.add_row("GPT-4o", "30", "9", "30.0%", "$0.0022")
    winrate.add_row("Gemini 2.0 Flash", "30", "6", "20.0%", "$0.0000")
    winrate.add_row("DeepSeek V3", "30", "3", "10.0%", "$0.0005")

    console.print(winrate)
    console.print()

    console.print("[bold]Key Insights:[/bold]")
    console.print("  • Claude Sonnet 4.5: Best for creative narrative and metaphor discipline")
    console.print("  • GPT-4o: Excellent dialogue and polish")
    console.print("  • Gemini 2.0 Flash: Free option with solid quality")
    console.print("  • DeepSeek V3: Ultra cost-effective ($0.0005/win)")
    console.print()


async def main():
    """Main interactive demo."""
    show_header()

    while True:
        show_menu()
        choice = console.input("[bold cyan]Select demo (1-6 or q):[/bold cyan] ")

        if choice == 'q':
            console.print("\n[dim]Thanks for trying Writers Factory Core![/dim]\n")
            break
        elif choice == '1':
            await demo_single_agent()
        elif choice == '2':
            await demo_tournament()
        elif choice == '3':
            await demo_knowledge_router()
        elif choice == '4':
            await demo_project_genesis()
        elif choice == '5':
            await demo_agent_pool()
        elif choice == '6':
            await demo_analytics()
        else:
            console.print("[red]Invalid choice. Try again.[/red]\n")
            continue

        console.input("\n[dim]Press Enter to continue...[/dim]")
        console.clear()
        show_header()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n\n[dim]Demo interrupted. Goodbye![/dim]\n")
