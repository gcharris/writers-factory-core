# Task: Implement Storage and Session Management System

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 3-4 hours
**Dependencies**: None (foundational component)

---

## Context

You are implementing the storage and session management system for the Writers Factory. This is a self-hosted, file-based system that needs to auto-save user work, maintain session state, and track costs - all without database overhead.

The system must be:
- **Fast**: Auto-save without blocking UI
- **Reliable**: Never lose work, even on crashes
- **Simple**: File-based storage, no SQLite/database complexity
- **Transparent**: Users always know save status
- **Cloneable**: Easy to backup, migrate, or start fresh

---

## Current Architecture

### Directory Structure

```
project/
├── .session/                    # Session state (gitignored)
│   ├── current.json            # Active session data
│   ├── history.json            # Session history
│   ├── costs.json              # Cost tracking
│   └── preferences.json        # User preferences
│
├── manuscript/                  # User's writing (auto-tracked)
├── reference/                   # Story bible (auto-tracked)
├── planning/                    # Outlines (auto-tracked)
└── output/                      # Generated content
    └── reports/
```

### What Needs to be Saved

**Session State** (`current.json`):
- Current stage (Creation/Writing/Enhancing/Analyzing/Scoring)
- Current screen/view
- Open files and cursor positions
- Active model selections (per stage)
- Recent queries (last 10)
- Breadcrumb trail
- Timestamp of last activity

**Cost Tracking** (`costs.json`):
- Session costs by model
- Operation history (timestamp, model, tokens, cost)
- Daily/weekly/monthly totals
- Budget warnings threshold

**Preferences** (`preferences.json`):
- Model preferences per stage
- NotebookLM configuration (if linked)
- Keyboard shortcut customizations
- UI theme/color preferences
- Auto-save interval (default: 30s)

**History** (`history.json`):
- Last 20 sessions with metadata
- Session duration
- Total costs per session
- Files created/modified per session

---

## Requirements

### 1. Auto-Save System

**Behavior**:
- Auto-save every 30 seconds (configurable)
- Auto-save after significant actions:
  - File created/modified
  - Stage changed
  - Model changed
  - Expensive operation completed
- Visual indicator in status bar: `● Auto-saved 12s ago`
- Never block UI during save
- Graceful handling if save fails (retry logic)

**Implementation Approach**:
```python
# Async auto-save worker
async def auto_save_worker():
    while True:
        await asyncio.sleep(AUTO_SAVE_INTERVAL)
        if session.has_changes():
            await session.save()
            ui.update_save_indicator()

# Manual save trigger (for significant actions)
async def on_significant_action(action_type: str):
    await session.save()
    await cost_tracker.log_action(action_type)
```

### 2. Session State Management

**Session Object Structure**:
```json
{
  "session_id": "2024-11-13-143022",
  "project_name": "The Explants",
  "created_at": "2024-11-13T14:30:22Z",
  "last_activity": "2024-11-13T15:45:10Z",

  "current_state": {
    "stage": "writing",
    "screen": "scene_editor",
    "breadcrumb": ["Home", "Writing", "Chapter 5", "Scene 5.3"]
  },

  "open_files": [
    {
      "path": "project/manuscript/volume-2/ACT_4/chapter-5.md",
      "cursor_line": 142,
      "cursor_col": 23
    }
  ],

  "model_preferences": {
    "writing": "claude",
    "enhancing": "gemini",
    "analyzing": "claude"
  },

  "recent_queries": [
    {
      "query": "What is Mickey's relationship with Noni?",
      "timestamp": "2024-11-13T15:30:00Z",
      "source": "cognee"
    }
  ]
}
```

**API**:
```python
class Session:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.session_path = project_path / ".session"
        self.data: SessionData = self._load_or_create()

    async def save(self):
        """Save session state to disk"""

    async def load(self, session_id: str = "current"):
        """Load session from disk"""

    def set_stage(self, stage: str):
        """Update current stage"""

    def set_model_preference(self, stage: str, model: str):
        """Save model preference for a stage"""

    def add_recent_query(self, query: str, source: str):
        """Track recent query"""

    def has_changes(self) -> bool:
        """Check if session has unsaved changes"""
```

### 3. Cost Tracking System

**Cost Data Structure**:
```json
{
  "session_total": 2.47,
  "daily_total": 8.32,
  "weekly_total": 45.19,
  "monthly_total": 127.88,

  "operations": [
    {
      "timestamp": "2024-11-13T15:30:00Z",
      "operation": "scene_generation",
      "model": "claude-sonnet-3.5",
      "input_tokens": 12450,
      "output_tokens": 3200,
      "cost": 0.15
    }
  ],

  "by_model": {
    "claude-sonnet-3.5": 1.50,
    "gemini-flash": 0.72,
    "gpt-4": 0.25
  },

  "budget": {
    "daily_limit": 50.0,
    "weekly_limit": 200.0,
    "monthly_limit": 500.0,
    "warnings_enabled": true
  }
}
```

**API**:
```python
class CostTracker:
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
        """Log API operation and calculate cost"""
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.data.operations.append({...})
        self.data.session_total += cost
        await self.save()

    def get_estimated_cost(
        self,
        model: str,
        estimated_tokens: int
    ) -> float:
        """Estimate cost before operation"""

    def should_warn_budget(self) -> Optional[str]:
        """Check if approaching budget limits"""
        # Returns warning message if within 80% of limit

    async def reset_session(self):
        """Start new session cost tracking"""
```

### 4. File Change Tracking

**Purpose**: Automatically detect when manuscript/reference files change

**Implementation**:
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectFileWatcher(FileSystemEventHandler):
    def __init__(self, session: Session):
        self.session = session
        self.tracked_dirs = [
            "project/manuscript",
            "project/reference",
            "project/planning"
        ]

    def on_modified(self, event):
        if not event.is_directory:
            self.session.mark_file_modified(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.session.mark_file_created(event.src_path)
```

### 5. Session History

**Purpose**: Track past sessions for analytics and recovery

**History Entry Structure**:
```json
{
  "session_id": "2024-11-13-143022",
  "start_time": "2024-11-13T14:30:22Z",
  "end_time": "2024-11-13T17:15:30Z",
  "duration_minutes": 165,
  "total_cost": 2.47,

  "files_modified": [
    "project/manuscript/volume-2/ACT_4/chapter-5.md"
  ],

  "files_created": [
    "project/output/reports/voice-test-2024-11-13.md"
  ],

  "operations_count": {
    "scene_generation": 3,
    "scene_enhancement": 2,
    "voice_test": 1
  }
}
```

### 6. Crash Recovery

**Requirements**:
- If system crashes, on restart:
  - Load last saved session state
  - Show "Session recovered" message
  - Offer to continue from last state or start fresh
  - Display any unsaved changes warning

**Implementation**:
```python
async def startup_check():
    """Check for crash recovery on startup"""
    session = Session(project_path)

    if session.was_interrupted():
        print("⚠️  Previous session was interrupted")
        print(f"   Last saved: {session.last_save_time}")
        print(f"   Duration: {session.duration_minutes} minutes")

        choice = prompt("Continue from last session? [Y/n]")

        if choice.lower() != 'n':
            return session  # Resume
        else:
            return Session.new(project_path)  # Fresh start
```

---

## Technical Specifications

### File Format

**Use JSON for all storage**:
- Human-readable for debugging
- Easy to backup/version control
- No schema migration issues
- Simple to parse/modify

### Concurrency

**Thread-safe operations**:
```python
import asyncio
from pathlib import Path
import aiofiles
import json

class ThreadSafeJSONStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock = asyncio.Lock()

    async def load(self) -> dict:
        async with self.lock:
            async with aiofiles.open(self.file_path, 'r') as f:
                content = await f.read()
                return json.loads(content)

    async def save(self, data: dict):
        async with self.lock:
            # Atomic write: write to temp file, then rename
            temp_path = self.file_path.with_suffix('.tmp')
            async with aiofiles.open(temp_path, 'w') as f:
                await f.write(json.dumps(data, indent=2))
            temp_path.replace(self.file_path)
```

### Error Handling

**Graceful degradation**:
```python
async def safe_save(self, data: dict):
    """Save with error handling and retry"""
    max_retries = 3

    for attempt in range(max_retries):
        try:
            await self._save(data)
            return True
        except IOError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            else:
                logger.error(f"Failed to save after {max_retries} attempts: {e}")
                ui.show_error("⚠️  Auto-save failed. Please save manually.")
                return False
```

### Performance

**Optimization strategies**:
- Only save if data actually changed (dirty flag)
- Debounce frequent saves (30s interval)
- Use atomic writes (temp file → rename)
- Compress history.json if > 1MB
- Limit history to last 20 sessions

---

## File Structure to Create

```
factory/core/storage/
├── __init__.py
├── session.py              # Session class
├── cost_tracker.py         # CostTracker class
├── preferences.py          # Preferences management
├── history.py              # Session history
├── file_watcher.py         # File change detection
└── json_store.py           # Thread-safe JSON storage

factory/core/storage/models/
├── __init__.py
├── session_data.py         # Pydantic models for session
├── cost_data.py            # Pydantic models for costs
└── history_data.py         # Pydantic models for history
```

---

## Integration Points

### UI Integration

**Status Bar Updates**:
```python
# In UI code
@session.on_save
def update_status_bar():
    elapsed = time.time() - session.last_save_time
    status_bar.set_save_indicator(f"● Auto-saved {elapsed}s ago")

@cost_tracker.on_update
def update_cost_display():
    status_bar.set_cost(f"Session: ${cost_tracker.session_total:.2f}")
```

### Cost Warning Integration

**Before expensive operations**:
```python
async def generate_scene(prompt: str, model: str):
    # Estimate cost
    estimated_tokens = estimate_tokens(prompt)
    estimated_cost = cost_tracker.get_estimated_cost(model, estimated_tokens)

    # Warn user
    if estimated_cost > 0.10:
        confirm = ui.confirm(
            f"⚠️  This operation will cost approximately ${estimated_cost:.2f}\n"
            f"    ({model}, ~{estimated_tokens} tokens)\n"
            f"    Continue? [Y/n]"
        )
        if not confirm:
            return None

    # Check budget
    warning = cost_tracker.should_warn_budget()
    if warning:
        ui.show_warning(warning)

    # Proceed with operation
    result = await agent.generate(prompt)

    # Log actual cost
    await cost_tracker.log_operation(
        operation="scene_generation",
        model=model,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens
    )

    return result
```

---

## Success Criteria

Your implementation should enable:

1. ✅ User can work for hours without manually saving
2. ✅ If system crashes, user loses < 30 seconds of work
3. ✅ User always knows when last save occurred
4. ✅ Cost tracking is automatic and accurate
5. ✅ Budget warnings appear before expensive operations
6. ✅ Session can be resumed after restart
7. ✅ No database installation/configuration required
8. ✅ Save operations never block UI
9. ✅ History shows past 20 sessions with details
10. ✅ All session data is human-readable JSON

---

## Testing Requirements

### Unit Tests

```python
# test_session.py
async def test_session_save_load():
    session = Session(tmp_path)
    session.set_stage("writing")
    await session.save()

    loaded = Session(tmp_path)
    assert loaded.current_stage == "writing"

# test_cost_tracker.py
async def test_cost_calculation():
    tracker = CostTracker(tmp_path)
    await tracker.log_operation(
        "scene_generation",
        "claude-sonnet-3.5",
        input_tokens=10000,
        output_tokens=2000
    )
    assert tracker.session_total > 0

# test_crash_recovery.py
async def test_recovery_on_crash():
    session = Session(tmp_path)
    session.set_stage("writing")
    await session.save()

    # Simulate crash (don't call session.close())
    del session

    # New session should detect interrupted session
    recovered = Session(tmp_path)
    assert recovered.was_interrupted()
```

### Integration Tests

```python
async def test_auto_save_workflow():
    """Test full auto-save cycle"""
    session = Session(tmp_path)

    # Start auto-save worker
    asyncio.create_task(auto_save_worker(session))

    # Make changes
    session.set_stage("writing")
    session.set_model_preference("writing", "claude")

    # Wait for auto-save
    await asyncio.sleep(31)

    # Verify saved
    loaded = Session(tmp_path)
    assert loaded.current_stage == "writing"
    assert loaded.model_preferences["writing"] == "claude"
```

---

## Deliverables

Please implement:

1. **Core Storage Classes** (`factory/core/storage/`)
   - Session management
   - Cost tracking
   - Preferences
   - History
   - File watcher

2. **Pydantic Models** (`factory/core/storage/models/`)
   - Type-safe data structures
   - Validation
   - Serialization

3. **Tests** (`factory/core/tests/storage/`)
   - Unit tests for all classes
   - Integration tests for workflows
   - Crash recovery tests

4. **Documentation**
   - API reference for each class
   - Usage examples
   - Integration guide for UI components

5. **Example Usage**
   - Demo script showing typical workflows
   - CLI tool for inspecting session data

---

## Implementation Notes

### Atomic Writes

Always use atomic writes to prevent corruption:

```python
async def atomic_write(file_path: Path, content: str):
    """Write to temp file, then rename"""
    temp_path = file_path.with_suffix('.tmp')
    async with aiofiles.open(temp_path, 'w') as f:
        await f.write(content)
    temp_path.replace(file_path)  # Atomic on POSIX systems
```

### Dirty Flag Pattern

Only save when necessary:

```python
class Session:
    def __init__(self):
        self._dirty = False

    def set_stage(self, stage: str):
        if self.current_stage != stage:
            self.current_stage = stage
            self._dirty = True

    def has_changes(self) -> bool:
        return self._dirty

    async def save(self):
        if not self._dirty:
            return  # Skip save

        await self._do_save()
        self._dirty = False
```

### Cost Model Pricing

Use current API pricing (as of Nov 2024):

```python
COST_PER_1K_TOKENS = {
    "claude-sonnet-3.5": {"input": 0.003, "output": 0.015},
    "claude-opus-3": {"input": 0.015, "output": 0.075},
    "gemini-flash": {"input": 0.00007, "output": 0.00021},
    "gemini-pro": {"input": 0.00035, "output": 0.00105},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = COST_PER_1K_TOKENS[model]
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    return input_cost + output_cost
```

---

## Questions? Clarifications Needed?

If any requirements are unclear, document your assumptions and proceed. Focus on creating a robust, simple, file-based system that never loses user work.
