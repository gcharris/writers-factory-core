# Task: Build Model Comparison Tool (Testing Lab)

**Priority**: Medium
**Assigned To**: Cloud Agent
**Estimated Time**: 3-4 hours
**Dependencies**: UX Design, Storage/Session Management

---

## Context

You are building the Model Comparison Tool - a dedicated feature for testing and comparing AI models side-by-side. This is separate from the simple model selector used for routine work.

**Purpose**: Allow writers to periodically test multiple AI models with the same prompt to determine which produces the best results for their specific needs (voice consistency, style, quality, etc.).

**User Story**: "I want to test whether Claude or Gemini writes better scenes for my protagonist's voice, so I can confidently choose which model to use for my Writing stage."

---

## Design Requirements

### Key Distinctions

**This is NOT**:
- The simple model selector dropdown (that's in the toolbar)
- A tournament bracket system (too complex)
- Automatic model selection (user decides)

**This IS**:
- A dedicated testing screen/tool
- Side-by-side comparison interface
- Manual evaluation with scoring assistance
- A way to make informed model choices

### User Flow

```
1. User opens Model Comparison Tool from main menu
2. Enters test prompt/scene outline
3. Selects 2-5 models to test
4. Clicks "Generate"
5. System generates outputs in parallel
6. Displays results side-by-side
7. Shows quality scores (voice, plot, style)
8. User reviews, compares, marks favorite
9. Optionally saves preferred model to preferences
```

---

## UI Design

### Comparison Tool Screen

```
╔═══════════════════════════════════════════════════════════════════════╗
║ MODEL COMPARISON LAB                                      [Cost: $0.45] ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║ Test Prompt:                                                            ║
║ ┌───────────────────────────────────────────────────────────────────┐ ║
║ │ Mickey confronts Vance about the true cost of consciousness       │ ║
║ │ upload. She's suspicious, analytical, defensive.                  │ ║
║ │                                                                     │ ║
║ │ POV: Enhanced Mickey                                               │ ║
║ │ Target: 500 words                                                  │ ║
║ └───────────────────────────────────────────────────────────────────┘ ║
║                                                                         ║
║ Select Models to Test:                                                 ║
║   [✓] Claude Sonnet 3.5    ($0.003/1K in, $0.015/1K out)             ║
║   [✓] Gemini Flash          ($0.00007/1K in, $0.00021/1K out)        ║
║   [✓] GPT-4 Turbo           ($0.01/1K in, $0.03/1K out)              ║
║   [ ] Qwen 2.5              ($0.002/1K in, $0.008/1K out)            ║
║   [ ] DeepSeek              ($0.001/1K in, $0.005/1K out)            ║
║                                                                         ║
║ [Generate Outputs]  [Load Previous Test]  [Clear]                     ║
║                                                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║ Keyboard: [Space] Select model | [G] Generate | [ESC] Back | [?] Help ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Results Display (After Generation)

```
╔═══════════════════════════════════════════════════════════════════════╗
║ COMPARISON RESULTS                               3 models • Total: $0.42 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║ ┌─────────────────────────────────────────────────────────────────┐   ║
║ │ [1] Claude Sonnet 3.5              Score: 87/100         $0.18  │   ║
║ ├─────────────────────────────────────────────────────────────────┤   ║
║ │ The lie tastes different now. Not bitter—mathematical. Each     │   ║
║ │ word Vance speaks a variable in an equation I'm solving in      │   ║
║ │ real-time. His pitch about consciousness upload gleams with      │   ║
║ │ the seductive logic of escape velocity.                         │   ║
║ │                                                                   │   ║
║ │ "You're selling computational substrate," I say. "Ones and      │   ║
║ │ zeros optimized for processing speed. Not consciousness."       │   ║
║ │ ...                                                               │   ║
║ │                                                                   │   ║
║ │ ✓ Voice: 92  ✓ Style: 85  ✓ Plot: 84  ⚠️ Length: 520 words     │   ║
║ │ [Mark as Favorite] [View Full] [Regenerate]                     │   ║
║ └─────────────────────────────────────────────────────────────────┘   ║
║                                                                         ║
║ ┌─────────────────────────────────────────────────────────────────┐   ║
║ │ [2] Gemini Flash                   Score: 81/100         $0.03  │   ║
║ ├─────────────────────────────────────────────────────────────────┤   ║
║ │ Vance's words shimmer with promise, but I see the code behind   │   ║
║ │ them. The upload he's selling isn't consciousness transferred—  │   ║
║ │ it's consciousness simulated. A difference that matters.        │   ║
║ │                                                                   │   ║
║ │ "What happens to the morphic field?" I ask. "The quantum       │   ║
║ │ entanglement that makes me... me?"                              │   ║
║ │ ...                                                               │   ║
║ │                                                                   │   ║
║ │ ✓ Voice: 78  ✓ Style: 82  ✓ Plot: 83  ✓ Length: 495 words     │   ║
║ │ [Mark as Favorite] [View Full] [Regenerate]                     │   ║
║ └─────────────────────────────────────────────────────────────────┘   ║
║                                                                         ║
║ ┌─────────────────────────────────────────────────────────────────┐   ║
║ │ [3] GPT-4 Turbo                    Score: 75/100         $0.21  │   ║
║ ├─────────────────────────────────────────────────────────────────┤   ║
║ │ I listen to Vance's pitch carefully, analyzing every word. He   │   ║
║ │ talks about consciousness upload like it's the next evolution   │   ║
║ │ of humanity. But something doesn't feel right.                  │   ║
║ │                                                                   │   ║
║ │ "This isn't actual consciousness transfer," I interrupt. "It's  │   ║
║ │ just copying and simulation."                                    │   ║
║ │ ...                                                               │   ║
║ │                                                                   │   ║
║ │ ⚠️ Voice: 68  ✓ Style: 80  ✓ Plot: 77  ✓ Length: 510 words    │   ║
║ │ [Mark as Favorite] [View Full] [Regenerate]                     │   ║
║ └─────────────────────────────────────────────────────────────────┘   ║
║                                                                         ║
║ [Export Report] [Save Favorite to Preferences] [Run Another Test]     ║
║                                                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║ Winner: Claude Sonnet 3.5 (highest voice consistency score)           ║
║ [1-3] Select output | [F] Mark favorite | [E] Export | [N] New test   ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Core Components

### 1. Comparison Tool Controller

```python
# factory/core/ui/screens/model_comparison.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import List, Dict

class ModelComparisonTool:
    """Model comparison and testing tool"""

    def __init__(self, app: 'WritersFactory'):
        self.app = app
        self.console = Console()
        self.current_test: Optional[ComparisonTest] = None

    async def run(self):
        """Main entry point for comparison tool"""
        while True:
            # Show input screen
            test_config = await self._get_test_configuration()

            if not test_config:
                break  # User cancelled

            # Run test
            results = await self._run_comparison_test(test_config)

            # Display results
            await self._display_results(results)

            # Ask if user wants to run another test
            if not await self._confirm_another_test():
                break

    async def _get_test_configuration(self) -> Optional[Dict]:
        """Get test configuration from user"""
        self._render_input_screen()

        # Get prompt
        prompt = self.console.input("\nEnter test prompt: ")

        if not prompt.strip():
            return None

        # Select models
        available_models = ["claude", "gemini", "gpt", "qwen", "deepseek"]

        self.console.print("\nSelect models to test (space to toggle):")

        selected = []
        for i, model in enumerate(available_models):
            cost = self._get_model_cost_info(model)
            self.console.print(f"  [ ] {model.title()}  {cost}")

        # Simple selection (enhanced version would use Rich interactive selection)
        selection = self.console.input("\nEnter model numbers (comma-separated): ")

        for idx in selection.split(','):
            try:
                selected.append(available_models[int(idx) - 1])
            except:
                pass

        if len(selected) < 2:
            self.console.print("[red]Please select at least 2 models[/red]")
            return None

        return {
            'prompt': prompt,
            'models': selected
        }

    async def _run_comparison_test(self, config: Dict) -> ComparisonResult:
        """Execute comparison test"""
        prompt = config['prompt']
        models = config['models']

        self.console.print(f"\n[yellow]Generating outputs from {len(models)} models...[/yellow]")

        # Generate outputs in parallel
        outputs = {}
        tasks = {}

        for model in models:
            agent = self.app.get_agent(model)
            tasks[model] = agent.generate_scene(prompt)

        # Wait for all to complete
        for model, task in tasks.items():
            try:
                output = await task
                outputs[model] = output
            except Exception as e:
                self.console.print(f"[red]Error with {model}: {e}[/red]")
                outputs[model] = None

        # Score outputs
        self.console.print("[yellow]Scoring outputs...[/yellow]")

        scored_outputs = await self._score_outputs(outputs, prompt)

        # Calculate costs
        total_cost = sum(
            self._calculate_output_cost(model, output)
            for model, output in outputs.items()
            if output
        )

        return ComparisonResult(
            prompt=prompt,
            models=models,
            outputs=scored_outputs,
            total_cost=total_cost
        )

    async def _score_outputs(
        self,
        outputs: Dict[str, str],
        prompt: str
    ) -> List[ScoredOutput]:
        """Score all outputs"""
        scorer = SceneScorer(self.app)

        scored = []

        for model, output in outputs.items():
            if not output:
                continue

            score = await scorer.score(
                scene=output,
                outline=prompt,
                character_voice=True,
                plot_consistency=True,
                style_consistency=True
            )

            scored.append(ScoredOutput(
                model=model,
                output=output,
                total_score=score.total_score,
                breakdown=score.breakdown,
                word_count=len(output.split())
            ))

        # Sort by total score
        scored.sort(key=lambda x: x.total_score, reverse=True)

        return scored

    async def _display_results(self, results: ComparisonResult):
        """Display comparison results"""
        self.console.clear()

        # Header
        header = Panel(
            f"[bold]COMPARISON RESULTS[/bold]\n"
            f"{len(results.models)} models • Total cost: ${results.total_cost:.2f}",
            style="bold blue"
        )
        self.console.print(header)

        # Display each output
        for i, output in enumerate(results.outputs, 1):
            self._render_output_panel(i, output)

        # Winner
        winner = results.outputs[0]
        self.console.print(
            f"\n[bold green]Winner:[/bold green] {winner.model.title()} "
            f"(score: {winner.total_score:.0f}/100)"
        )

        # Actions
        self.console.print("\n[bold]Actions:[/bold]")
        self.console.print("  [E] Export report")
        self.console.print("  [F] Save favorite to preferences")
        self.console.print("  [N] Run another test")
        self.console.print("  [Q] Return to main menu")

        action = self.console.input("\nSelect action: ").lower()

        if action == 'e':
            await self._export_report(results)
        elif action == 'f':
            await self._save_to_preferences(winner.model)
        elif action == 'n':
            return  # Will run another test

    def _render_output_panel(self, rank: int, output: ScoredOutput):
        """Render a single output panel"""
        # Truncate output for display
        preview = output.output[:300] + "..." if len(output.output) > 300 else output.output

        # Score indicators
        breakdown = output.breakdown
        indicators = []

        for criterion, score in breakdown.items():
            icon = "✓" if score >= 80 else "⚠️" if score >= 60 else "✗"
            indicators.append(f"{icon} {criterion.title()}: {score:.0f}")

        indicators_str = "  ".join(indicators)

        # Word count check
        word_diff = output.word_count - 500  # Assuming target is 500
        length_str = f"Length: {output.word_count} words"
        if abs(word_diff) > 50:
            length_str = f"⚠️ {length_str} ({word_diff:+d})"
        else:
            length_str = f"✓ {length_str}"

        # Panel
        panel_title = f"[{rank}] {output.model.title()}    Score: {output.total_score:.0f}/100    ${output.cost:.2f}"

        panel = Panel(
            f"{preview}\n\n{indicators_str}  {length_str}",
            title=panel_title,
            border_style="green" if rank == 1 else "blue"
        )

        self.console.print(panel)

    async def _export_report(self, results: ComparisonResult):
        """Export comparison report to markdown"""
        report_path = self.app.project_path / "output" / "reports" / f"model-comparison-{timestamp()}.md"

        report = f"""# Model Comparison Report

**Date**: {datetime.now().isoformat()}
**Total Cost**: ${results.total_cost:.2f}

## Test Prompt

```
{results.prompt}
```

## Results

"""

        for i, output in enumerate(results.outputs, 1):
            report += f"""### Rank {i}: {output.model.title()}

**Score**: {output.total_score:.0f}/100
**Cost**: ${output.cost:.2f}
**Word Count**: {output.word_count}

**Breakdown**:
{chr(10).join(f"- {k.title()}: {v:.0f}" for k, v in output.breakdown.items())}

**Output**:
```
{output.output}
```

---

"""

        # Save report
        with open(report_path, 'w') as f:
            f.write(report)

        self.console.print(f"\n[green]Report saved to {report_path}[/green]")

    async def _save_to_preferences(self, model: str):
        """Save model preference"""
        stages = ["writing", "enhancing", "analyzing"]

        self.console.print(f"\nSave {model.title()} as preferred model for:")

        for i, stage in enumerate(stages, 1):
            self.console.print(f"  {i}. {stage.title()}")

        selection = self.console.input("Select stage (or press Enter to skip): ")

        if selection.isdigit():
            stage = stages[int(selection) - 1]
            self.app.preferences.set_model_preference(stage, model)
            self.console.print(f"[green]✓ Saved {model.title()} as {stage} model[/green]")

    async def _confirm_another_test(self) -> bool:
        """Ask if user wants to run another test"""
        return Confirm.ask("\nRun another comparison test?")

    def _get_model_cost_info(self, model: str) -> str:
        """Get cost info string for model"""
        costs = {
            "claude": "($0.003/1K in, $0.015/1K out)",
            "gemini": "($0.00007/1K in, $0.00021/1K out)",
            "gpt": "($0.01/1K in, $0.03/1K out)",
            "qwen": "($0.002/1K in, $0.008/1K out)",
            "deepseek": "($0.001/1K in, $0.005/1K out)"
        }
        return costs.get(model, "")
```

### 2. Data Models

```python
# factory/core/ui/models/comparison.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ScoredOutput:
    """Single model output with score"""
    model: str
    output: str
    total_score: float
    breakdown: Dict[str, float]  # criterion -> score
    word_count: int
    cost: float

@dataclass
class ComparisonResult:
    """Results from a comparison test"""
    prompt: str
    models: List[str]
    outputs: List[ScoredOutput]  # Sorted by score
    total_cost: float

    @property
    def winner(self) -> ScoredOutput:
        """Get winning model"""
        return self.outputs[0]
```

### 3. Scene Scorer

```python
# factory/core/analysis/scene_scorer.py
from typing import Dict

class SceneScorer:
    """Score scenes across multiple criteria"""

    def __init__(self, app: 'WritersFactory'):
        self.app = app

    async def score(
        self,
        scene: str,
        outline: str,
        character_voice: bool = True,
        plot_consistency: bool = True,
        style_consistency: bool = True
    ) -> SceneScore:
        """Score a scene"""

        breakdown = {}

        if character_voice:
            breakdown['voice'] = await self._score_voice(scene)

        if plot_consistency:
            breakdown['plot'] = await self._score_plot(scene, outline)

        if style_consistency:
            breakdown['style'] = await self._score_style(scene)

        # Calculate total (weighted average)
        total = sum(breakdown.values()) / len(breakdown)

        return SceneScore(
            total_score=total,
            breakdown=breakdown
        )

    async def _score_voice(self, scene: str) -> float:
        """Score voice consistency"""
        tester = VoiceConsistencyTester()
        result = await tester.test_scene(scene, "Enhanced Mickey")
        return result.total_score

    async def _score_plot(self, scene: str, outline: str) -> float:
        """Score plot consistency with outline"""
        # Check if scene hits key beats from outline
        # Simplified version - can be enhanced
        return 85.0

    async def _score_style(self, scene: str) -> float:
        """Score style consistency"""
        # Check for compressed phrasing, direct metaphors, etc.
        # Simplified version - can be enhanced
        return 82.0

@dataclass
class SceneScore:
    """Scene scoring result"""
    total_score: float
    breakdown: Dict[str, float]
```

---

## Integration with Main CLI

```python
# In factory/core/commands.py

@cli.group()
def models():
    """Model management and comparison"""
    pass

@models.command()
@click.pass_obj
async def compare(app: WritersFactory):
    """Open Model Comparison Tool"""
    tool = ModelComparisonTool(app)
    await tool.run()

@models.command()
@click.pass_obj
def list(app: WritersFactory):
    """List available models with costs"""
    # Show table of models and pricing
    pass

@models.command()
@click.option('--stage', required=True)
@click.option('--model', required=True)
@click.pass_obj
def set_preference(app: WritersFactory, stage: str, model: str):
    """Set model preference for a stage"""
    app.preferences.set_model_preference(stage, model)
    app.console.print(f"[green]✓ Set {model} as {stage} model[/green]")
```

---

## File Structure

```
factory/core/ui/screens/
├── model_comparison.py         # ModelComparisonTool class

factory/core/ui/models/
├── comparison.py               # ScoredOutput, ComparisonResult

factory/core/analysis/
├── scene_scorer.py             # SceneScorer class
```

---

## Success Criteria

Your implementation should enable:

1. ✅ User can test 2-5 models side-by-side
2. ✅ Results display clearly with scores
3. ✅ Winner automatically identified
4. ✅ Reports can be exported
5. ✅ Preferences can be saved from comparison
6. ✅ Cost is calculated and displayed
7. ✅ Keyboard navigation throughout
8. ✅ Previous tests can be loaded
9. ✅ Clear visual distinction between outputs
10. ✅ Integrated with main CLI

---

## Deliverables

1. **ModelComparisonTool** - Main comparison interface
2. **SceneScorer** - Multi-criteria scoring system
3. **Data Models** - ScoredOutput, ComparisonResult
4. **CLI Integration** - Commands for comparison tool
5. **Tests** - Unit tests for scoring and comparison
6. **Documentation** - User guide for model comparison

---

## Questions? Clarifications Needed?

If any requirements are unclear, document your assumptions and proceed. Focus on creating an intuitive tool for evaluating models that helps users make informed decisions.
