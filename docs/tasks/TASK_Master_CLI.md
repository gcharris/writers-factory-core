# Task: Build Master CLI (factory.py) Entry Point

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 4-5 hours
**Dependencies**: Storage/Session Management, UX Design

---

## Context

You are building the master command-line interface (`factory.py`) that serves as the single entry point for the entire Writers Factory system. This CLI orchestrates all workflows, coordinates between components, and provides a Rich-based TUI for writers.

Think of this as the "control center" that connects:
- 5 AI model agents (Claude, Gemini, GPT, Qwen, DeepSeek)
- 3 knowledge systems (Cognee, NotebookLM, Gemini File Search)
- 8 working systems (Scene Multiplier, Enhancement, Analyzer, Voice Tester, etc.)
- Session management, cost tracking, and user preferences

---

## Design Philosophy

### User Experience Principles

1. **Zero Configuration**: Works out of the box with sensible defaults
2. **Keyboard-First**: Every action accessible via shortcuts
3. **Context-Aware**: UI adapts to what user has created
4. **Cost-Conscious**: Always show costs before expensive operations
5. **Parallel-Friendly**: Support running multiple operations simultaneously
6. **Session-Based**: Save/resume anywhere
7. **Progressive Disclosure**: Advanced options hidden until needed

### Technical Principles

1. **Async-First**: All operations use async/await
2. **Composable**: Workflows built from smaller reusable components
3. **Testable**: Each component can be tested independently
4. **Observable**: Rich logging and telemetry
5. **Recoverable**: Graceful error handling with retry logic

---

## CLI Architecture

### Entry Point Structure

```
factory.py                      # Main entry point
├── Commands                    # Top-level commands
│   ├── init                    # Initialize new project
│   ├── wizard                  # Run Creation Wizard
│   ├── scene                   # Scene operations
│   ├── voice                   # Voice testing
│   ├── batch                   # Batch processing
│   ├── query                   # Knowledge base queries
│   ├── analyze                 # Consistency checking
│   └── export                  # Export to Word/PDF
│
├── Interactive Mode            # Full TUI interface
│   ├── Dashboard               # Main overview screen
│   ├── Stage Screens           # Creation/Writing/Enhancing/etc.
│   └── Tool Screens            # Model Comparison, KB Query, etc.
│
└── Background Workers          # Async services
    ├── Auto-save               # Session persistence
    ├── File Watcher            # Track manuscript changes
    └── Cost Tracker            # Real-time cost monitoring
```

### Command-Line Interface

**Basic Usage**:
```bash
# Interactive mode (TUI)
./factory.py

# Specific commands
./factory.py wizard                            # Run Creation Wizard
./factory.py scene generate --outline scene.md # Generate scene
./factory.py scene enhance --file chapter5.md  # Enhance existing scene
./factory.py voice test --models claude,gemini # Voice testing
./factory.py batch process --config batch.json # Batch processing
./factory.py query "Who is Mickey Bardot?"     # Query knowledge base
./factory.py analyze canon --volume 2          # Check consistency
./factory.py export --volume 1 --format docx   # Export to Word

# Session management
./factory.py resume                            # Resume last session
./factory.py sessions list                     # List recent sessions
./factory.py sessions load <session-id>        # Load specific session

# Configuration
./factory.py config show                       # Show current config
./factory.py config set model.writing claude   # Set preference
./factory.py config api-keys                   # Configure API keys
```

---

## Core Components

### 1. Main Application Class

```python
# factory/core/app.py
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
import asyncio
from typing import Optional

class WritersFactory:
    """Main application controller"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.console = Console()

        # Core components
        self.session = Session(project_path)
        self.cost_tracker = CostTracker(project_path / ".session")
        self.preferences = Preferences(project_path / ".session")

        # Knowledge systems
        self.cognee = CogneeKnowledgeGraph(project_path)
        self.notebooklm = NotebookLMClient(self.preferences.notebooklm_config)

        # Agents (lazy-loaded)
        self._agents: Dict[str, Agent] = {}

        # UI
        self.ui = UIManager(self.console)
        self.current_screen: Optional[Screen] = None

    async def start(self):
        """Start the application"""
        # Check for crash recovery
        if self.session.was_interrupted():
            if await self.ui.confirm_recovery(self.session):
                await self.session.resume()
            else:
                self.session = Session.new(self.project_path)

        # Start background workers
        asyncio.create_task(self._auto_save_worker())
        asyncio.create_task(self._file_watcher())

        # Show main dashboard
        await self.show_dashboard()

    async def show_dashboard(self):
        """Display main dashboard"""
        self.current_screen = DashboardScreen(self)
        await self.current_screen.render()

    def get_agent(self, model: str) -> Agent:
        """Get or create agent for model"""
        if model not in self._agents:
            self._agents[model] = self._create_agent(model)
        return self._agents[model]

    async def _auto_save_worker(self):
        """Background auto-save loop"""
        while True:
            await asyncio.sleep(self.preferences.auto_save_interval)
            if self.session.has_changes():
                await self.session.save()
                self.ui.update_save_indicator()

    async def _file_watcher(self):
        """Watch for file system changes"""
        watcher = ProjectFileWatcher(self.session)
        watcher.start()
```

### 2. Command Handler

```python
# factory/core/commands.py
import click
from pathlib import Path

@click.group()
@click.option('--project', default='.', help='Project directory')
@click.pass_context
def cli(ctx, project):
    """Writers Factory - Multi-Model AI Novel Writing System"""
    ctx.obj = WritersFactory(Path(project))

@cli.command()
@click.pass_obj
async def wizard(app: WritersFactory):
    """Run the Creation Wizard"""
    wizard = CreationWizard(app)
    await wizard.run()

@cli.group()
def scene():
    """Scene operations"""
    pass

@scene.command()
@click.option('--outline', type=click.Path(exists=True), required=True)
@click.option('--model', default=None, help='AI model to use')
@click.option('--variants', default=5, help='Number of variants')
@click.pass_obj
async def generate(app: WritersFactory, outline: str, model: str, variants: int):
    """Generate scene from outline"""
    # Load outline
    with open(outline) as f:
        outline_text = f.read()

    # Get model preference
    if not model:
        model = app.preferences.get_model_preference('writing')

    # Estimate cost
    estimated_cost = app.cost_tracker.estimate_scene_generation(
        model, len(outline_text), variants
    )

    if estimated_cost > 0.10:
        if not app.ui.confirm_cost(estimated_cost, model):
            return

    # Generate variants
    results = await app.workflows.scene_generation(
        outline=outline_text,
        model=model,
        variants=variants
    )

    # Show results
    app.ui.show_scene_variants(results)

@scene.command()
@click.option('--file', type=click.Path(exists=True), required=True)
@click.option('--model', default=None)
@click.pass_obj
async def enhance(app: WritersFactory, file: str, model: str):
    """Enhance existing scene"""
    with open(file) as f:
        scene_text = f.read()

    if not model:
        model = app.preferences.get_model_preference('enhancing')

    result = await app.workflows.scene_enhancement(
        scene=scene_text,
        model=model
    )

    app.ui.show_enhancement_result(result, file)

@cli.group()
def voice():
    """Voice testing and comparison"""
    pass

@voice.command()
@click.option('--models', required=True, help='Comma-separated model list')
@click.option('--prompt', type=click.Path(exists=True), required=True)
@click.pass_obj
async def test(app: WritersFactory, models: str, prompt: str):
    """Test multiple models with same prompt"""
    model_list = models.split(',')

    with open(prompt) as f:
        prompt_text = f.read()

    # Run voice consistency test
    results = await app.workflows.voice_testing(
        prompt=prompt_text,
        models=model_list
    )

    # Show comparison
    app.ui.show_voice_comparison(results)

@cli.command()
@click.argument('query')
@click.pass_obj
async def query(app: WritersFactory, query: str):
    """Query knowledge base"""
    # Auto-route to appropriate KB
    result = await app.knowledge_router.query(query)

    app.ui.show_query_result(result)

@cli.command()
@click.pass_obj
async def resume(app: WritersFactory):
    """Resume last session"""
    await app.session.load('current')
    await app.start()
```

### 3. Workflow Orchestrator

```python
# factory/core/workflows/__init__.py
from typing import List, Dict
import asyncio

class WorkflowOrchestrator:
    """Coordinates multi-step workflows"""

    def __init__(self, app: WritersFactory):
        self.app = app

    async def scene_generation(
        self,
        outline: str,
        model: str,
        variants: int = 5
    ) -> List[SceneVariant]:
        """
        Complete scene generation workflow:
        1. Query knowledge for context
        2. Generate variants
        3. Score each variant
        4. Return ranked results
        """
        # Step 1: Get context
        context = await self.app.knowledge_router.get_context_for_scene(outline)

        # Step 2: Generate variants in parallel
        agent = self.app.get_agent(model)

        tasks = [
            agent.generate_scene(outline, context)
            for _ in range(variants)
        ]

        variants_results = await asyncio.gather(*tasks)

        # Step 3: Score variants
        scorer = SceneScorer()
        scored_variants = [
            {
                'text': variant,
                'score': await scorer.score(variant, context),
                'model': model
            }
            for variant in variants_results
        ]

        # Step 4: Rank by score
        scored_variants.sort(key=lambda x: x['score'], reverse=True)

        # Log costs
        for variant in scored_variants:
            await self.app.cost_tracker.log_operation(
                operation='scene_generation',
                model=model,
                input_tokens=variant['input_tokens'],
                output_tokens=variant['output_tokens']
            )

        return scored_variants

    async def scene_enhancement(
        self,
        scene: str,
        model: str
    ) -> EnhancementResult:
        """
        Scene enhancement workflow:
        1. Analyze current scene
        2. Get voice requirements from KB
        3. Enhance scene
        4. Validate voice consistency
        """
        # Step 1: Analyze
        analysis = await self._analyze_scene(scene)

        # Step 2: Get voice requirements
        voice_guide = await self.app.cognee.query(
            "What are the voice requirements for Enhanced Mickey?"
        )

        # Step 3: Enhance
        agent = self.app.get_agent(model)
        enhanced = await agent.enhance_scene(scene, voice_guide, analysis)

        # Step 4: Validate
        validation = await self._validate_voice(enhanced, voice_guide)

        return EnhancementResult(
            original=scene,
            enhanced=enhanced,
            analysis=analysis,
            validation=validation
        )

    async def voice_testing(
        self,
        prompt: str,
        models: List[str]
    ) -> VoiceComparisonResult:
        """
        Voice testing workflow:
        1. Generate outputs from all models
        2. Score voice consistency
        3. Compare results
        4. Recommend best model
        """
        # Step 1: Generate in parallel
        tasks = {
            model: self.app.get_agent(model).generate_scene(prompt, {})
            for model in models
        }

        results = {}
        for model, task in tasks.items():
            results[model] = await task

        # Step 2: Score voice consistency
        voice_tester = VoiceConsistencyTester()

        scored_results = {}
        for model, output in results.items():
            score = await voice_tester.score(output)
            scored_results[model] = {
                'output': output,
                'score': score
            }

        # Step 3: Rank
        ranked = sorted(
            scored_results.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )

        return VoiceComparisonResult(
            prompt=prompt,
            models=models,
            results=scored_results,
            winner=ranked[0][0],
            rankings=ranked
        )

    async def batch_processing(
        self,
        config: BatchConfig
    ) -> BatchResult:
        """
        Batch processing workflow:
        1. Load all scaffolds
        2. Process each with scene generation
        3. Track progress
        4. Generate summary report
        """
        scaffolds = self._load_scaffolds(config.input_dir)

        results = []
        total = len(scaffolds)

        with self.app.ui.progress_bar(total=total) as progress:
            for i, scaffold in enumerate(scaffolds):
                result = await self.scene_generation(
                    outline=scaffold,
                    model=config.model,
                    variants=config.variants
                )

                results.append({
                    'scaffold': scaffold,
                    'best_variant': result[0],
                    'all_variants': result
                })

                progress.update(i + 1)

        # Generate report
        report = self._generate_batch_report(results)

        return BatchResult(
            results=results,
            report=report,
            total_cost=self.app.cost_tracker.session_total
        )
```

### 4. UI Manager (Rich-based TUI)

```python
# factory/core/ui/manager.py
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Confirm

class UIManager:
    """Manages Rich-based terminal UI"""

    def __init__(self, console: Console):
        self.console = console
        self.layout = Layout()
        self._setup_layout()

    def _setup_layout(self):
        """Initialize layout structure"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

    def show_dashboard(self, app: WritersFactory):
        """Render main dashboard"""
        # Header
        header = Panel(
            f"[bold blue]Writers Factory[/bold blue] - {app.session.project_name}",
            style="bold white on blue"
        )

        # Pipeline status
        pipeline = self._render_pipeline(app.session)

        # Recent activity
        activity = self._render_recent_activity(app.session)

        # Cost summary
        costs = self._render_cost_summary(app.cost_tracker)

        # Main content
        main = Layout()
        main.split_column(
            Layout(pipeline, name="pipeline", size=5),
            Layout(activity, name="activity"),
            Layout(costs, name="costs", size=10)
        )

        # Footer with shortcuts
        footer = Panel(
            "[bold]Shortcuts:[/bold] [C]reation | [W]riting | [E]nhancing | "
            "[A]nalyzing | [S]coring | [Q]uery | [P]ipeline | [M]odels | [X] Exit"
        )

        self.layout["header"].update(header)
        self.layout["main"].update(main)
        self.layout["footer"].update(footer)

        self.console.print(self.layout)

    def _render_pipeline(self, session: Session) -> Panel:
        """Render pipeline status bar"""
        stages = ["Creation", "Writing", "Enhancing", "Analyzing", "Scoring"]
        current = session.current_stage

        status_line = " → ".join([
            f"[bold green]{stage} ✓[/bold green]" if self._is_complete(session, stage)
            else f"[bold yellow]{stage} ⚡[/bold yellow]" if stage.lower() == current
            else f"[dim]{stage}[/dim]"
            for stage in stages
        ])

        return Panel(status_line, title="Pipeline", border_style="blue")

    def _render_cost_summary(self, tracker: CostTracker) -> Table:
        """Render cost summary table"""
        table = Table(title="Cost Summary", show_header=True)

        table.add_column("Period", style="cyan")
        table.add_column("Cost", style="green", justify="right")

        table.add_row("Session", f"${tracker.data.session_total:.2f}")
        table.add_row("Today", f"${tracker.data.daily_total:.2f}")
        table.add_row("Week", f"${tracker.data.weekly_total:.2f}")
        table.add_row("Month", f"${tracker.data.monthly_total:.2f}")

        return table

    def confirm_cost(self, cost: float, model: str) -> bool:
        """Show cost confirmation dialog"""
        return Confirm.ask(
            f"⚠️  This operation will cost approximately [bold]${cost:.2f}[/bold]\n"
            f"    (Model: {model})\n"
            f"    Continue?"
        )

    def show_scene_variants(self, variants: List[Dict]):
        """Display scene variants for selection"""
        self.console.print("\n[bold]Generated Scene Variants:[/bold]\n")

        for i, variant in enumerate(variants, 1):
            panel = Panel(
                variant['text'][:500] + "...",
                title=f"Variant {i} - Score: {variant['score']:.2f}",
                border_style="green" if i == 1 else "blue"
            )
            self.console.print(panel)

    def show_voice_comparison(self, results: VoiceComparisonResult):
        """Display voice testing comparison"""
        table = Table(title="Voice Consistency Comparison")

        table.add_column("Model", style="cyan")
        table.add_column("Score", style="green", justify="right")
        table.add_column("Winner", style="yellow")

        for model, data in results.ranked:
            table.add_row(
                model,
                f"{data['score']:.2f}",
                "🏆" if model == results.winner else ""
            )

        self.console.print(table)

    def update_save_indicator(self, elapsed_seconds: int):
        """Update auto-save indicator in footer"""
        # Update footer with save time
        pass

    def progress_bar(self, total: int):
        """Create progress bar for batch operations"""
        return Progress()
```

---

## Integration with Existing Systems

### Knowledge Router

```python
# factory/core/knowledge/router.py
class KnowledgeRouter:
    """Intelligently route queries to appropriate KB"""

    def __init__(self, app: WritersFactory):
        self.cognee = app.cognee
        self.notebooklm = app.notebooklm

    async def query(self, query: str) -> QueryResult:
        """Route query to best knowledge system"""

        # Classify query type
        query_type = self._classify_query(query)

        if query_type == "character_lookup":
            # Fast, local Cognee for character facts
            result = await self.cognee.query(query)
            source = "Project Knowledge (Cognee)"

        elif query_type == "writing_technique":
            # External NotebookLM for craft advice
            if self.notebooklm.is_configured():
                result = await self.notebooklm.query(query)
                source = "NotebookLM"
            else:
                result = await self.cognee.query(query)
                source = "Project Knowledge (Cognee)"

        else:
            # Default to Cognee
            result = await self.cognee.query(query)
            source = "Project Knowledge (Cognee)"

        return QueryResult(
            query=query,
            answer=result,
            source=source
        )

    def _classify_query(self, query: str) -> str:
        """Classify query to determine best KB"""
        # Simple keyword-based classification
        if any(word in query.lower() for word in ["who", "character", "relationship"]):
            return "character_lookup"
        elif any(word in query.lower() for word in ["how to", "technique", "craft"]):
            return "writing_technique"
        else:
            return "general"
```

---

## File Structure

```
factory.py                          # Main entry point (symlink)

factory/core/
├── __init__.py
├── app.py                          # WritersFactory class
├── commands.py                     # Click command handlers
│
├── workflows/
│   ├── __init__.py
│   ├── orchestrator.py             # WorkflowOrchestrator
│   ├── scene_generation.py
│   ├── scene_enhancement.py
│   ├── voice_testing.py
│   └── batch_processing.py
│
├── ui/
│   ├── __init__.py
│   ├── manager.py                  # UIManager
│   ├── screens/
│   │   ├── dashboard.py
│   │   ├── creation.py
│   │   ├── writing.py
│   │   ├── enhancing.py
│   │   ├── analyzing.py
│   │   └── scoring.py
│   └── components/
│       ├── pipeline_status.py
│       ├── cost_display.py
│       ├── model_selector.py
│       └── progress_tracker.py
│
├── knowledge/
│   └── router.py                   # KnowledgeRouter
│
└── utils/
    ├── keyboard.py                 # Keyboard input handler
    └── colors.py                   # Theme/color management
```

---

## Success Criteria

Your implementation should enable:

1. ✅ `./factory.py` launches interactive TUI
2. ✅ All workflows accessible via CLI commands
3. ✅ Keyboard-only navigation throughout UI
4. ✅ Cost warnings before expensive operations
5. ✅ Session auto-saves every 30 seconds
6. ✅ Crash recovery on restart
7. ✅ Parallel operations (multiple agents at once)
8. ✅ Real-time progress indicators
9. ✅ Clear, informative error messages
10. ✅ Context-aware UI (adapts to project state)

---

## Testing Strategy

### Unit Tests
- Command parsing
- Workflow orchestration logic
- UI component rendering
- Cost calculations

### Integration Tests
- Full workflow execution
- Multi-agent coordination
- Session save/load
- Error recovery

### User Acceptance Tests
- Common user scenarios
- Keyboard navigation
- Performance benchmarks

---

## Deliverables

1. **factory.py** - Executable entry point
2. **Core Application** - WritersFactory class
3. **Command Handlers** - All CLI commands
4. **Workflow Orchestrator** - Pre-built workflows
5. **UI Manager** - Rich-based TUI
6. **Documentation** - Usage guide, API reference
7. **Tests** - Unit and integration tests
8. **Example Workflows** - Demo scripts

---

## Questions? Clarifications Needed?

If any requirements are unclear, document your assumptions and proceed. Focus on creating an intuitive, powerful CLI that makes multi-model novel writing feel natural.
