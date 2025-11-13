# Phase 2: Build Stage-Based Workflow Interface

**Date**: 2025-11-13
**Assigned To**: Cloud Agent
**Estimated Time**: 1-2 weeks
**Status**: Ready to start

---

## Context: What You Already Built (Phase 1)

You successfully completed Phase 1 with a tournament-based multi-model comparison system:

✅ **Keep and Use**:
- `factory/core/workflow_engine.py` - Excellent workflow engine with dependency resolution
- `factory/core/agent_pool.py` - Perfect multi-model orchestration (16 agents configured)
- `factory/agents/` - All agent integrations working
- `factory/storage/database.py` - SQLite analytics (keep for metrics only)
- `factory/knowledge/router.py` - Knowledge routing (we'll enhance this)
- `factory/workflows/multi_model_generation/` - Tournament system (we'll repurpose this)

✅ **What Works**:
- Multi-model generation (run same prompt across multiple models)
- Cost tracking and analytics
- Agent pool management
- Database analytics

---

## What We're Building Now: Stage-Based Workflow System

**Vision**: A daily writing interface where authors work through stages (Creation → Writing → Enhancing → Analyzing → Scoring), with specialized tools at each stage. The tournament system becomes **one tool** within the Writing stage, not the core architecture.

**Primary Use Case**:
> "I sit down to write. The system remembers where I was (auto-saved 30s ago). I'm in the Writing stage, working on Chapter 5. I can generate scenes, enhance them, test voice consistency, query my knowledge base, or run a model comparison tournament. Everything auto-saves. If it crashes, I lose < 30 seconds of work."

---

## Architecture Transformation

### Current (Phase 1)
```
User → CLI Command → Tournament Workflow → Agent Pool → SQLite Database
```

### Target (Phase 2)
```
User
  ↓
Rich TUI (Full-Screen Interface)
  ↓
┌─────────────────────────────────────────────────────────────┐
│ Status Bar: Creation ✓ | Writing ⚡ (45/120) | Enhancing   │
│                              Session: $2.47   ● Auto-saved 12s ago │
└─────────────────────────────────────────────────────────────┘
  ↓
5-Stage Workflow Pipeline
  ├─ Creation (wizard)
  ├─ Writing (scene generation, enhancement, voice testing)
  │    └─ Model Comparison Tool ← tournament system wrapped
  ├─ Enhancing (surgical fixes)
  ├─ Analyzing (scene evaluation)
  └─ Scoring (comparative analysis)
  ↓
┌─────────────────────────────────────────────────────────────┐
│ Storage Layer                                                │
│ ├─ File-Based: project/.session/ (auto-save, crash recovery)│
│ └─ SQLite: factory/storage/ (analytics, metrics)            │
└─────────────────────────────────────────────────────────────┘
```

---

## Task 1: File-Based Session Storage (CRITICAL - Foundation)

**Priority**: Do this FIRST - everything else depends on it

**Location**: `factory/core/storage/`

### What to Build

#### 1.1 Directory Structure
```
factory/core/storage/
├── __init__.py
├── session.py              # Session class
├── cost_tracker.py         # CostTracker class
├── preferences.py          # Preferences management
├── history.py              # Session history
├── file_watcher.py         # File change detection
├── json_store.py           # Thread-safe JSON storage
└── models/
    ├── __init__.py
    ├── session_data.py     # Pydantic models for session
    ├── cost_data.py        # Pydantic models for costs
    └── history_data.py     # Pydantic models for history
```

#### 1.2 Project Session Directory (Created by System)
```
project/
├── .session/                # Auto-created, gitignored
│   ├── current.json         # Active session state
│   ├── history.json         # Last 20 sessions
│   ├── costs.json           # Cost tracking
│   └── preferences.json     # User preferences
├── manuscript/              # User's writing
├── reference/               # Story bible
└── planning/                # Outlines
```

### 1.3 Session Class Specification

**File**: `factory/core/storage/session.py`

```python
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import asyncio
import aiofiles
import json

class Session:
    """Manages session state with auto-save and crash recovery."""

    def __init__(self, project_path: Path):
        """Initialize session.

        Args:
            project_path: Path to project root (contains .session/)
        """
        self.project_path = project_path
        self.session_path = project_path / ".session"
        self.session_path.mkdir(exist_ok=True)

        # Session data
        self.session_id: str = self._generate_session_id()
        self.data: SessionData = self._load_or_create()
        self._dirty: bool = False  # Track if needs saving
        self._auto_save_task: Optional[asyncio.Task] = None

    def _generate_session_id(self) -> str:
        """Generate unique session ID: YYYY-MM-DD-HHMMSS"""
        return datetime.now().strftime("%Y-%m-%d-%H%M%S")

    async def save(self) -> bool:
        """Save session to disk (atomic write).

        Returns:
            True if saved successfully, False otherwise
        """
        if not self._dirty:
            return True  # No changes, skip save

        try:
            await self._atomic_write(
                self.session_path / "current.json",
                self.data.model_dump_json(indent=2)
            )
            self._dirty = False
            self.data.last_save_time = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False

    async def _atomic_write(self, file_path: Path, content: str):
        """Write to temp file, then rename (atomic on POSIX)."""
        temp_path = file_path.with_suffix('.tmp')
        async with aiofiles.open(temp_path, 'w') as f:
            await f.write(content)
        temp_path.replace(file_path)  # Atomic rename

    def _load_or_create(self) -> SessionData:
        """Load existing session or create new one."""
        current_file = self.session_path / "current.json"

        if current_file.exists():
            with open(current_file, 'r') as f:
                data = json.load(f)
                return SessionData(**data)
        else:
            # Create new session
            return SessionData(
                session_id=self.session_id,
                project_name=self.project_path.name,
                created_at=datetime.now(),
                current_state=CurrentState(
                    stage="creation",
                    screen="dashboard",
                    breadcrumb=["Home"]
                )
            )

    def was_interrupted(self) -> bool:
        """Check if previous session was interrupted (not cleanly closed)."""
        return (
            self.data.completed_at is None and
            self.data.last_activity is not None
        )

    async def start_auto_save(self, interval: int = 30):
        """Start auto-save background task.

        Args:
            interval: Save interval in seconds (default: 30)
        """
        async def auto_save_loop():
            while True:
                await asyncio.sleep(interval)
                if self.has_changes():
                    await self.save()
                    logger.debug(f"Auto-saved session {self.session_id}")

        self._auto_save_task = asyncio.create_task(auto_save_loop())

    def stop_auto_save(self):
        """Stop auto-save background task."""
        if self._auto_save_task:
            self._auto_save_task.cancel()

    # State management methods

    def set_stage(self, stage: str):
        """Update current stage.

        Args:
            stage: One of: creation, writing, enhancing, analyzing, scoring
        """
        if self.data.current_state.stage != stage:
            self.data.current_state.stage = stage
            self.data.last_activity = datetime.now()
            self._dirty = True

    def set_model_preference(self, stage: str, model: str):
        """Save model preference for a stage."""
        self.data.model_preferences[stage] = model
        self._dirty = True

    def add_recent_query(self, query: str, source: str):
        """Track recent knowledge query."""
        self.data.recent_queries.append({
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "source": source
        })
        # Keep only last 10
        self.data.recent_queries = self.data.recent_queries[-10:]
        self._dirty = True

    def add_open_file(self, file_path: str, cursor_line: int = 0, cursor_col: int = 0):
        """Track open file with cursor position."""
        self.data.open_files = [
            f for f in self.data.open_files
            if f["path"] != file_path
        ]  # Remove if exists

        self.data.open_files.append({
            "path": file_path,
            "cursor_line": cursor_line,
            "cursor_col": cursor_col
        })
        self._dirty = True

    def has_changes(self) -> bool:
        """Check if session has unsaved changes."""
        return self._dirty

    @property
    def last_save_elapsed(self) -> int:
        """Seconds since last save."""
        if self.data.last_save_time:
            return int((datetime.now() - self.data.last_save_time).total_seconds())
        return 0
```

### 1.4 SessionData Models

**File**: `factory/core/storage/models/session_data.py`

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class CurrentState(BaseModel):
    """Current UI state."""
    stage: str  # creation, writing, enhancing, analyzing, scoring
    screen: str  # dashboard, scene_editor, model_comparison, etc.
    breadcrumb: List[str] = Field(default_factory=list)

class OpenFile(BaseModel):
    """Open file with cursor position."""
    path: str
    cursor_line: int = 0
    cursor_col: int = 0

class RecentQuery(BaseModel):
    """Recent knowledge query."""
    query: str
    timestamp: str
    source: str  # cognee, notebooklm

class SessionData(BaseModel):
    """Complete session state."""
    session_id: str
    project_name: str
    created_at: datetime
    last_activity: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_save_time: Optional[datetime] = None

    current_state: CurrentState
    open_files: List[OpenFile] = Field(default_factory=list)
    model_preferences: Dict[str, str] = Field(default_factory=dict)
    recent_queries: List[RecentQuery] = Field(default_factory=list)
```

### 1.5 CostTracker Class

**File**: `factory/core/storage/cost_tracker.py`

```python
class CostTracker:
    """Track costs with budget warnings."""

    def __init__(self, session_path: Path):
        self.costs_path = session_path / "costs.json"
        self.data: CostData = self._load_or_create()

    async def log_operation(
        self,
        operation: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ):
        """Log API operation and calculate cost.

        Args:
            operation: Operation type (scene_generation, enhancement, etc.)
            model: Model name
            input_tokens: Input token count
            output_tokens: Output token count
        """
        cost = self._calculate_cost(model, input_tokens, output_tokens)

        self.data.operations.append(Operation(
            timestamp=datetime.now(),
            operation=operation,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost
        ))

        self.data.session_total += cost
        self.data.daily_total += cost
        self.data.weekly_total += cost
        self.data.monthly_total += cost

        # Track by model
        if model not in self.data.by_model:
            self.data.by_model[model] = 0
        self.data.by_model[model] += cost

        await self.save()

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on model pricing."""
        pricing = COST_PER_1K_TOKENS.get(model, {"input": 0, "output": 0})
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost

    def get_estimated_cost(self, model: str, estimated_tokens: int) -> float:
        """Estimate cost before operation."""
        pricing = COST_PER_1K_TOKENS.get(model, {"input": 0, "output": 0})
        # Assume 70/30 split input/output
        input_cost = (estimated_tokens * 0.7 / 1000) * pricing["input"]
        output_cost = (estimated_tokens * 0.3 / 1000) * pricing["output"]
        return input_cost + output_cost

    def should_warn_budget(self) -> Optional[str]:
        """Check if approaching budget limits (80% threshold)."""
        warnings = []

        if self.data.budget.daily_limit:
            if self.data.daily_total >= self.data.budget.daily_limit * 0.8:
                warnings.append(
                    f"⚠️  Daily budget: ${self.data.daily_total:.2f} / ${self.data.budget.daily_limit:.2f} (80%)"
                )

        if self.data.budget.weekly_limit:
            if self.data.weekly_total >= self.data.budget.weekly_limit * 0.8:
                warnings.append(
                    f"⚠️  Weekly budget: ${self.data.weekly_total:.2f} / ${self.data.budget.weekly_limit:.2f} (80%)"
                )

        if self.data.budget.monthly_limit:
            if self.data.monthly_total >= self.data.budget.monthly_limit * 0.8:
                warnings.append(
                    f"⚠️  Monthly budget: ${self.data.monthly_total:.2f} / ${self.data.budget.monthly_limit:.2f} (80%)"
                )

        return "\n".join(warnings) if warnings else None

# Model pricing (as of Nov 2024)
COST_PER_1K_TOKENS = {
    "claude-sonnet-4.5": {"input": 0.003, "output": 0.015},
    "claude-opus-4": {"input": 0.015, "output": 0.075},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gemini-2-flash": {"input": 0, "output": 0},
    "gemini-1.5-pro": {"input": 0.00035, "output": 0.00105},
    "deepseek-v3": {"input": 0.00027, "output": 0.0011},
    "qwen-max": {"input": 0.008, "output": 0.008},
}
```

### 1.6 Success Criteria for Task 1

Before moving to Task 2, verify:

- [ ] `factory/core/storage/` directory created with all files
- [ ] Session class loads/saves to `project/.session/current.json`
- [ ] Auto-save runs every 30 seconds (non-blocking)
- [ ] CostTracker logs operations and calculates costs accurately
- [ ] Atomic writes (temp file → rename) implemented
- [ ] Dirty flag pattern (only save when changed) works
- [ ] Crash recovery detects interrupted sessions
- [ ] Session history tracks last 20 sessions
- [ ] Unit tests pass for Session and CostTracker
- [ ] Integration test: auto-save cycle works end-to-end

**Commit Message**:
```
[Task 1] Add file-based session storage with auto-save

- Session class with atomic writes and dirty flag pattern
- CostTracker with budget warnings (80% threshold)
- Auto-save every 30s (non-blocking async)
- Crash recovery on startup
- Session history (last 20 sessions)
- Pydantic models for type safety
- Unit tests + integration tests (all passing)

Closes: TASK_Storage_Session_Management
```

---

## Task 2: Rich TUI Interface (Full-Screen)

**Priority**: Do this SECOND - provides the user interface

**Location**: `factory/ui/`

### What to Build

This is NOT a basic CLI. This is a **full-screen terminal user interface** using Rich's Live display.

#### 2.1 Directory Structure
```
factory/ui/
├── __init__.py
├── tui.py                  # Main TUI application class
├── components/
│   ├── __init__.py
│   ├── status_bar.py       # Status bar component
│   ├── stage_view.py       # Base class for stage views
│   ├── dashboard.py        # Main dashboard
│   └── cost_dashboard.py   # Cost tracking view
├── stages/
│   ├── __init__.py
│   ├── creation_stage.py   # Creation wizard UI
│   ├── writing_stage.py    # Writing stage UI
│   ├── enhancing_stage.py  # Enhancing stage UI
│   ├── analyzing_stage.py  # Analyzing stage UI
│   └── scoring_stage.py    # Scoring stage UI
└── keyboard.py             # Keyboard input handler
```

#### 2.2 Status Bar Specification

**Exact Format**:
```
Creation ✓ | Writing ⚡ (45/120) | Enhancing | Analyzing | Scoring   Session: $2.47   ● Auto-saved 12s ago
```

**Requirements**:
- Always visible at top of screen
- Updates in real-time
- Stage indicators:
  - `✓` = completed
  - `⚡` = active (with progress if applicable)
  - No symbol = pending
- Cost updates in real-time
- Auto-save indicator updates every second

**File**: `factory/ui/components/status_bar.py`

```python
from rich.console import Console, RenderableType
from rich.text import Text
from rich.panel import Panel
from datetime import datetime

class StatusBar:
    """Status bar showing pipeline progress, costs, and auto-save status."""

    def __init__(self, session: Session, cost_tracker: CostTracker):
        self.session = session
        self.cost_tracker = cost_tracker

    def render(self) -> Panel:
        """Render status bar."""
        # Stage indicators
        stages = ["creation", "writing", "enhancing", "analyzing", "scoring"]
        stage_texts = []

        for stage in stages:
            if stage == self.session.data.current_state.stage:
                # Active stage
                icon = "⚡"
                style = "bold yellow"
                # Add progress if available
                progress = self._get_stage_progress(stage)
                if progress:
                    text = f"{stage.capitalize()} {icon} ({progress})"
                else:
                    text = f"{stage.capitalize()} {icon}"
            elif self._is_stage_completed(stage):
                # Completed stage
                icon = "✓"
                style = "bold green"
                text = f"{stage.capitalize()} {icon}"
            else:
                # Pending stage
                style = "dim"
                text = stage.capitalize()

            stage_texts.append(Text(text, style=style))

        # Join with pipes
        stage_display = Text(" | ").join(stage_texts)

        # Cost and save info
        cost_text = Text(f"   Session: ${self.cost_tracker.data.session_total:.2f}", style="cyan")
        save_elapsed = self.session.last_save_elapsed
        save_text = Text(f"   ● Auto-saved {save_elapsed}s ago", style="green")

        # Combine
        full_text = Text.assemble(stage_display, cost_text, save_text)

        return Panel(full_text, style="bold white on blue", box=box.ROUNDED)

    def _get_stage_progress(self, stage: str) -> Optional[str]:
        """Get progress for stage (e.g., '45/120' for writing)."""
        # Example: For writing stage, show scenes completed/total
        if stage == "writing":
            # Get from session data
            completed = self.session.data.metadata.get("scenes_completed", 0)
            total = self.session.data.metadata.get("scenes_total", 0)
            if total > 0:
                return f"{completed}/{total}"
        return None

    def _is_stage_completed(self, stage: str) -> bool:
        """Check if stage is marked complete."""
        return self.session.data.metadata.get(f"{stage}_completed", False)
```

#### 2.3 Main TUI Application

**File**: `factory/ui/tui.py`

```python
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from typing import Optional
import asyncio

class WritersFactoryTUI:
    """Main TUI application with full-screen interface."""

    def __init__(self, project_path: Path):
        self.console = Console()
        self.project_path = project_path

        # Initialize session and cost tracker
        self.session = Session(project_path)
        self.cost_tracker = CostTracker(self.session.session_path)

        # UI components
        self.layout = self._create_layout()
        self.status_bar = StatusBar(self.session, self.cost_tracker)
        self.current_stage_view: Optional[StageView] = None

        # Keyboard handler
        self.keyboard = KeyboardHandler(self)

    def _create_layout(self) -> Layout:
        """Create main layout structure."""
        layout = Layout()
        layout.split_column(
            Layout(name="status_bar", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1)
        )
        return layout

    async def run(self):
        """Run the TUI application."""
        # Check for crash recovery
        if self.session.was_interrupted():
            if not await self._handle_crash_recovery():
                return

        # Start auto-save
        await self.session.start_auto_save(interval=30)

        # Load stage view
        await self._load_stage_view(self.session.data.current_state.stage)

        # Run main loop
        with Live(self.layout, console=self.console, refresh_per_second=4, screen=True):
            try:
                await self._main_loop()
            except KeyboardInterrupt:
                pass
            finally:
                await self._cleanup()

    async def _handle_crash_recovery(self) -> bool:
        """Handle crash recovery dialog.

        Returns:
            True to continue, False to exit
        """
        self.console.print("\n[yellow]⚠️  Previous session was interrupted[/yellow]")
        self.console.print(f"   Last saved: {self.session.data.last_save_time}")
        self.console.print(f"   Stage: {self.session.data.current_state.stage}")

        response = input("\nContinue from last session? [Y/n]: ")

        if response.lower() == 'n':
            # Start fresh
            self.session = Session(self.project_path)
            return True

        return True

    async def _main_loop(self):
        """Main event loop."""
        while True:
            # Update layout
            self.layout["status_bar"].update(self.status_bar.render())

            if self.current_stage_view:
                self.layout["main"].update(self.current_stage_view.render())

            self.layout["footer"].update(self._render_footer())

            # Handle keyboard input (non-blocking)
            key = await self.keyboard.get_key()
            if key:
                await self._handle_key(key)

            await asyncio.sleep(0.1)  # 10 FPS

    async def _handle_key(self, key: str):
        """Handle keyboard input.

        Args:
            key: Key pressed (TAB, C, H, E, Q, etc.)
        """
        # Global shortcuts
        if key == "Q":
            raise KeyboardInterrupt
        elif key == "TAB":
            await self._next_stage()
        elif key == "SHIFT+TAB":
            await self._previous_stage()
        elif key == "C":
            await self._open_model_comparison()
        elif key == "H":
            await self._show_help()
        elif key == "CTRL+S":
            await self.session.save()
        else:
            # Pass to current stage view
            if self.current_stage_view:
                await self.current_stage_view.handle_key(key)

    async def _next_stage(self):
        """Navigate to next stage."""
        stages = ["creation", "writing", "enhancing", "analyzing", "scoring"]
        current_idx = stages.index(self.session.data.current_state.stage)
        next_idx = (current_idx + 1) % len(stages)

        await self._load_stage_view(stages[next_idx])

    async def _previous_stage(self):
        """Navigate to previous stage."""
        stages = ["creation", "writing", "enhancing", "analyzing", "scoring"]
        current_idx = stages.index(self.session.data.current_state.stage)
        prev_idx = (current_idx - 1) % len(stages)

        await self._load_stage_view(stages[prev_idx])

    async def _load_stage_view(self, stage: str):
        """Load stage view.

        Args:
            stage: Stage name (creation, writing, enhancing, analyzing, scoring)
        """
        # Import dynamically
        if stage == "creation":
            from factory.ui.stages.creation_stage import CreationStageView
            self.current_stage_view = CreationStageView(self.session, self.cost_tracker)
        elif stage == "writing":
            from factory.ui.stages.writing_stage import WritingStageView
            self.current_stage_view = WritingStageView(self.session, self.cost_tracker)
        # ... etc for other stages

        self.session.set_stage(stage)

    def _render_footer(self) -> Panel:
        """Render footer with keyboard shortcuts."""
        shortcuts = "TAB: Next Stage | SHIFT+TAB: Prev Stage | C: Model Comparison | H: Help | Q: Quit"
        return Panel(Text(shortcuts, style="dim"), style="dim", box=box.SIMPLE)

    async def _cleanup(self):
        """Cleanup before exit."""
        # Stop auto-save
        self.session.stop_auto_save()

        # Final save
        await self.session.save()

        # Mark session complete
        self.session.data.completed_at = datetime.now()
        await self.session.save()

        self.console.print("\n[green]✓ Session saved successfully[/green]")
```

#### 2.4 Keyboard Handler

**File**: `factory/ui/keyboard.py`

```python
import asyncio
import sys
import tty
import termios
from typing import Optional

class KeyboardHandler:
    """Non-blocking keyboard input handler."""

    def __init__(self, tui):
        self.tui = tui
        self._key_queue = asyncio.Queue()
        self._listener_task: Optional[asyncio.Task] = None

    async def get_key(self) -> Optional[str]:
        """Get pressed key (non-blocking).

        Returns:
            Key string (TAB, SHIFT+TAB, C, etc.) or None
        """
        try:
            key = self._key_queue.get_nowait()
            return self._normalize_key(key)
        except asyncio.QueueEmpty:
            return None

    def _normalize_key(self, raw_key: bytes) -> str:
        """Normalize raw key input to string.

        Args:
            raw_key: Raw bytes from keyboard

        Returns:
            Normalized key string
        """
        # Handle special keys
        if raw_key == b'\t':
            return "TAB"
        elif raw_key == b'\x1b[Z':  # Shift+Tab
            return "SHIFT+TAB"
        elif raw_key == b'\x11':  # Ctrl+Q
            return "Q"
        elif raw_key == b'\x13':  # Ctrl+S
            return "CTRL+S"
        else:
            # Regular character
            return raw_key.decode('utf-8').upper()

    def start_listening(self):
        """Start keyboard listener task."""
        self._listener_task = asyncio.create_task(self._listen_loop())

    async def _listen_loop(self):
        """Background task to listen for keyboard input."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            while True:
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1).encode('utf-8')
                    await self._key_queue.put(key)
                await asyncio.sleep(0.05)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
```

### 2.5 Success Criteria for Task 2

Before moving to Task 3, verify:

- [ ] Full-screen Rich TUI launches (not basic CLI)
- [ ] Status bar shows stage pipeline with correct indicators (✓, ⚡)
- [ ] Status bar updates in real-time (costs, auto-save timer)
- [ ] TAB/SHIFT+TAB navigates between stages
- [ ] Keyboard shortcuts work (C, H, E, Q, CTRL+S)
- [ ] UI does NOT block during operations (async)
- [ ] Auto-save indicator counts up every second
- [ ] Stage views render correctly
- [ ] Crash recovery dialog shows on interrupted session
- [ ] Footer shows keyboard shortcuts
- [ ] Can quit gracefully with Q

**Commit Message**:
```
[Task 2] Add Rich TUI with full-screen interface

- Full-screen terminal UI using Rich Live display
- Status bar with pipeline progress and auto-save indicator
- 5-stage navigation (TAB/SHIFT+TAB)
- Keyboard-first interface (C, H, E, Q, CTRL+S)
- Non-blocking async event loop
- Crash recovery dialog
- Stage view architecture (base class + 5 stage views)
- Real-time updates (4 FPS)

Closes: TASK_Master_CLI
```

---

## Task 3: Knowledge Router Improvements

**Priority**: Do this THIRD

**What to Change**: The knowledge router exists but has mock implementations and exposes all 3 sources. We need:

1. **Hide Cognee from users** - They just "ask questions", system routes automatically
2. **Make NotebookLM opt-in** - Configured during Creation Wizard
3. **Real integrations** - Replace mock implementations

**File**: `factory/knowledge/router.py`

### Changes Needed

```python
# CHANGE 1: Don't expose Gemini File Search as user-selectable option
class KnowledgeSource(Enum):
    """Available knowledge sources (internal only)."""
    COGNEE = "cognee"  # Local, always available
    NOTEBOOKLM = "notebooklm"  # External, opt-in
    # REMOVE: GEMINI_FILE_SEARCH (used internally by Cognee if needed)

# CHANGE 2: Real Cognee integration
async def _query_cognee(self, query: str, max_results: int) -> QueryResult:
    """Query Cognee (local semantic graph).

    TODO: Replace with real Cognee integration
    - Use existing Cognee installation (17MB)
    - Query semantic graph
    - Return results with references
    """
    # REAL implementation here
    pass

# CHANGE 3: Real NotebookLM integration
async def _query_notebooklm(self, query: str, max_results: int) -> QueryResult:
    """Query NotebookLM (external).

    TODO: Replace with real NotebookLM integration
    - Use notebook ID from session preferences
    - Query via NotebookLM API
    - Return results with audio summary option
    """
    # REAL implementation here
    pass
```

**Commit Message**:
```
[Task 3] Improve knowledge router with real integrations

- Hide Cognee from users (automatic routing)
- NotebookLM as opt-in (configured in preferences)
- Real Cognee integration (semantic graph queries)
- Real NotebookLM integration (API queries with audio)
- Remove Gemini File Search from user-facing options

Closes: TASK_Knowledge_Router (partial)
```

---

## Task 4: Scene Workflows

**Priority**: Do this FOURTH

**Location**: `factory/workflows/scene_operations/`

### What to Build

```
factory/workflows/scene_operations/
├── __init__.py
├── generation.py       # SceneGenerationWorkflow
├── enhancement.py      # SceneEnhancementWorkflow
└── voice_testing.py    # VoiceTestingWorkflow
```

**Specification**: See full details in `TASK_Workflows_Module.md`

Key features:
- Scene generation with knowledge context
- Scene enhancement (voice, pacing, dialogue)
- Voice testing with character consistency checks

**Commit Message**:
```
[Task 4] Add scene operation workflows

- SceneGenerationWorkflow (with knowledge context)
- SceneEnhancementWorkflow (voice, pacing, dialogue)
- VoiceTestingWorkflow (character consistency)
- Integration with Knowledge Router
- Cost tracking for all operations

Closes: TASK_Workflows_Module
```

---

## Task 5: Model Comparison Tool (Repurpose Tournament)

**Priority**: Do this FIFTH

**Location**: `factory/tools/model_comparison.py`

### What to Build

Wrap the existing tournament system (from `factory/workflows/multi_model_generation/`) as a user-facing tool within the Writing stage.

```python
class ModelComparisonTool:
    """Side-by-side model comparison (wraps tournament system)."""

    def __init__(self, agent_pool: AgentPool):
        self.agent_pool = agent_pool

    async def compare_models(
        self,
        prompt: str,
        models: List[str],  # 2-4 models
        context: Optional[str] = None
    ) -> ComparisonResult:
        """Run side-by-side comparison.

        Uses the existing tournament workflow but presents results
        in a visual side-by-side format with diff highlighting.
        """
        # Use existing multi_model_generation workflow
        from factory.workflows.multi_model_generation.workflow import MultiModelGenerationWorkflow

        workflow = MultiModelGenerationWorkflow(...)
        results = await workflow.execute(prompt, models, context)

        # Add visual diff
        diff_results = self._compute_visual_diff(results)

        return ComparisonResult(
            models=models,
            outputs=results.outputs,
            costs=results.costs,
            diffs=diff_results,
            winner=None  # User selects
        )
```

**Commit Message**:
```
[Task 5] Add Model Comparison Tool (tournament wrapper)

- Wraps existing tournament system as user tool
- Side-by-side visual comparison (2-4 models)
- Visual diff highlighting
- User preference tracking (winner selection)
- Accessible via 'C' keyboard shortcut in Writing stage

Closes: TASK_Model_Comparison_Tool
```

---

## Task 6: Creation Wizard

**Priority**: Do this SIXTH (Most complex)

**Location**: `factory/wizard/`

**Specification**: See full 35KB specification in `TASK_Creation_Wizard.md`

This is the LARGEST task - a conversational wizard with:
- 5 phases (Foundation, Character, Plot, World, Symbolism)
- 80+ questions total
- Save the Cat! 15-beat structure
- "Find Your Voice" tool
- NotebookLM linking option
- Output: 4,000-6,000 word story bible

**Commit Message**:
```
[Task 6] Add Creation Wizard (Save the Cat! 15 beats)

- 5-phase conversational wizard
- Phase 1: Foundation (15-25 questions, marathon runner progress)
- Phase 2: Character Construction (30-40 questions, Find Your Voice tool)
- Phase 3: Plot Architecture (25-35 questions, Save the Cat! 15 beats)
- Phase 4: World & Context (15-20 questions, opening cliché warnings)
- Phase 5: Symbolic Layering (10-15 questions, optional)
- Output: 4,000-6,000 word story bible
- NotebookLM linking (opt-in)

Closes: TASK_Creation_Wizard
```

---

## Task 7: Integration & Polish

**Priority**: Do this LAST

### What to Do

1. **End-to-end testing**
   - Run full user journey: `factory init` → wizard → writing → enhancing
   - Test crash recovery (kill process, restart)
   - Test long session (2+ hours, check for memory leaks)

2. **Performance optimization**
   - Ensure auto-save doesn't block UI
   - Optimize knowledge query response times
   - Profile async operations

3. **Documentation updates**
   - Update README with new features
   - Create ARCHITECTURE.md explaining hybrid system
   - Add troubleshooting guide

**Commit Message**:
```
[Task 7] Integration testing and polish

- End-to-end testing (all stages working)
- Performance optimization (non-blocking auto-save)
- Crash recovery testing (verified < 30s data loss)
- Long session testing (2+ hours, no memory leaks)
- Documentation updates (README, ARCHITECTURE, TROUBLESHOOTING)

Closes: Phase 2 Implementation
```

---

## Final Success Criteria (All 23 Checkpoints)

### Core Functionality (5)
- [ ] 1. User can launch `factory start` and see Rich TUI with 5-stage pipeline
- [ ] 2. Status bar shows stage progress, costs, and auto-save status
- [ ] 3. User can navigate between stages with TAB/SHIFT+TAB
- [ ] 4. Auto-save runs every 30 seconds without blocking UI
- [ ] 5. Cost tracking logs all operations and warns before expensive operations

### Knowledge System (4)
- [ ] 6. User can ask questions from any stage
- [ ] 7. Questions route to Cognee (local) or NotebookLM (if configured)
- [ ] 8. Users never see "Gemini File Search" option
- [ ] 9. Cognee is invisible (users just "ask questions")

### Writing Workflows (3)
- [ ] 10. User can generate scenes with knowledge context
- [ ] 11. User can enhance existing scenes (voice, pacing, dialogue)
- [ ] 12. User can run voice tests on scenes

### Model Comparison Tool (4)
- [ ] 13. User can press 'C' in Writing stage → Model Comparison opens
- [ ] 14. Side-by-side comparison shows 2-4 model outputs
- [ ] 15. Visual diff highlights differences
- [ ] 16. User can select winner → Preference saved

### Creation Wizard (4)
- [ ] 17. User can run `factory init` → Conversational wizard starts
- [ ] 18. Wizard feels conversational, not form-like
- [ ] 19. 5 phases with progress indicator (marathon runner)
- [ ] 20. Output: 4,000-6,000 word story bible

### Session Management (3)
- [ ] 21. If system crashes, session recovers on restart
- [ ] 22. User loses < 30 seconds of work
- [ ] 23. History shows last 20 sessions

---

## Timeline Estimate

| Task | Estimated Time | Cumulative |
|------|---------------|------------|
| Task 1: Session Storage | 6-8 hours | Day 1-2 |
| Task 2: Rich TUI | 8-10 hours | Day 3-4 |
| Task 3: Knowledge Router | 4-6 hours | Day 5 |
| Task 4: Scene Workflows | 6-8 hours | Day 6-7 |
| Task 5: Model Comparison | 4-6 hours | Day 8 |
| Task 6: Creation Wizard | 12-16 hours | Day 9-11 |
| Task 7: Integration & Polish | 4-6 hours | Day 12-13 |
| **TOTAL** | **44-60 hours** | **~2 weeks** |

---

## Work Protocol

### For Each Task:
1. Read the task specification completely
2. Read the relevant TASK_*.md file in `docs/tasks/` for full details
3. Implement the functionality
4. Write unit tests (pytest)
5. Write integration tests where applicable
6. Test manually to verify it works
7. Commit with descriptive message (use template above)
8. Push to repository
9. **Continue immediately to next task** (no approval needed)

### Commit Message Format:
```
[Task N] Brief description

- Bullet point of what was implemented
- Another key feature added
- Tests added/updated

Closes: TASK_<name>
```

---

## Questions?

If anything is unclear:
1. Read the full task specification in `docs/tasks/TASK_*.md`
2. Review the UX design spec in `docs/UX_DESIGN_SPECIFICATION.md`
3. Check existing code in `factory/` for patterns
4. Document your assumption and proceed
5. Only ask if genuinely blocked on a critical decision

---

## Important Notes

1. **Keep existing code**: Don't delete `factory/workflows/multi_model_generation/` - repurpose it as Model Comparison Tool
2. **SQLite analytics**: Keep the existing database for analytics/metrics
3. **Agent pool**: Keep all 16 agent integrations - they're perfect
4. **Workflow engine**: Keep the excellent workflow engine - build on it
5. **Tests**: All existing tests should continue passing

---

**You have full autonomy. Work through Tasks 1-7 sequentially. When complete, create a final report summarizing all changes.**

Good luck! 🚀
