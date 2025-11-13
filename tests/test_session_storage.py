"""Tests for session storage system."""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory

from factory.core.storage import (
    Session,
    CostTracker,
    PreferencesManager,
    HistoryManager,
)
from factory.core.storage.models import (
    SessionData,
    CostOperation,
    SessionHistoryEntry,
)


class TestSession:
    """Test Session class."""

    @pytest.mark.asyncio
    async def test_session_creation(self):
        """Test creating a new session."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path, auto_save_interval=60)

            assert session.data.project_name == project_path.name
            assert session.data.session_id is not None
            assert session.data.current_state.stage == "creation"
            assert session.data.current_state.screen == "dashboard"

    @pytest.mark.asyncio
    async def test_session_save_and_load(self):
        """Test saving and loading session."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)

            # Create and save session
            session1 = Session(project_path)
            session1.set_stage("writing")
            session1.set_screen("scene_editor")
            session1.data.mark_dirty()

            await session1.save()

            # Load session
            session2 = Session(project_path)
            assert session2.data.current_state.stage == "writing"
            assert session2.data.current_state.screen == "scene_editor"

    @pytest.mark.asyncio
    async def test_auto_save(self):
        """Test auto-save functionality."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path, auto_save_interval=1)  # 1 second

            # Start auto-save
            session.start_auto_save()

            # Make changes
            session.set_stage("writing")
            await asyncio.sleep(1.5)  # Wait for auto-save

            # Stop auto-save
            session.stop_auto_save()

            # Verify saved
            assert not session.data.dirty
            assert session.data.total_saves > 0

    @pytest.mark.asyncio
    async def test_atomic_write(self):
        """Test atomic write (no corruption)."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            # Verify no .tmp files left behind
            await session.save()

            tmp_files = list(project_path.glob("**/*.tmp"))
            assert len(tmp_files) == 0

    def test_was_interrupted(self):
        """Test crash detection."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            # New session - not interrupted
            assert not session.was_interrupted()

            # Simulate old activity
            session.data.last_activity = datetime.now() - timedelta(minutes=10)
            assert session.was_interrupted()

    @pytest.mark.asyncio
    async def test_open_files_tracking(self):
        """Test tracking open files."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            session.add_open_file("manuscript/chapter1.md", 42, 10)
            assert len(session.data.open_files) == 1
            assert session.data.open_files[0].path == "manuscript/chapter1.md"
            assert session.data.open_files[0].cursor_line == 42

            session.remove_open_file("manuscript/chapter1.md")
            assert len(session.data.open_files) == 0

    @pytest.mark.asyncio
    async def test_recent_queries(self):
        """Test recent query tracking."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            session.add_recent_query("What is X?", "notebooklm", "Answer to X")
            assert len(session.data.recent_queries) == 1
            assert session.data.recent_queries[0].query == "What is X?"

            # Add 11 queries (should keep only last 10)
            for i in range(11):
                session.add_recent_query(f"Query {i}", "notebooklm")

            assert len(session.data.recent_queries) == 10

    def test_model_preferences(self):
        """Test model preference management."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            # Default preference
            assert session.get_model_preference("writing") == "claude-sonnet-4.5"

            # Set preference
            session.set_model_preference("writing", "gpt-4o")
            assert session.get_model_preference("writing") == "gpt-4o"

    def test_save_status(self):
        """Test save status messages."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            session = Session(project_path)

            # Unsaved changes
            session.data.mark_dirty()
            assert "Unsaved" in session.get_save_status()

            # After save
            session.data.mark_clean()
            status = session.get_save_status()
            assert "ago" in status.lower() or "not saved" in status.lower()


class TestCostTracker:
    """Test CostTracker class."""

    @pytest.mark.asyncio
    async def test_cost_tracking(self):
        """Test basic cost tracking."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            tracker = CostTracker(session_path)

            await tracker.log_operation(
                operation_type="generation",
                model_name="claude-sonnet-4.5",
                tokens_input=100,
                tokens_output=200,
                cost=0.05,
                stage="writing"
            )

            assert tracker.get_session_cost() == 0.05
            assert len(tracker.data.operations) == 1

    @pytest.mark.asyncio
    async def test_daily_cost_summary(self):
        """Test daily cost aggregation."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            tracker = CostTracker(session_path)

            await tracker.log_operation(
                operation_type="generation",
                model_name="claude-sonnet-4.5",
                tokens_input=100,
                tokens_output=200,
                cost=0.05,
                stage="writing"
            )

            today_cost = tracker.get_today_cost()
            assert today_cost == 0.05

    def test_budget_warnings(self):
        """Test budget warning system."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            tracker = CostTracker(session_path)
            tracker.data.budget_daily = 1.0

            # Add operations to approach budget
            for i in range(4):
                tracker.data.add_operation(
                    CostOperation(
                        timestamp=datetime.now(),
                        operation_type="generation",
                        model_name="test",
                        tokens_input=100,
                        tokens_output=100,
                        cost=0.22,  # 4 * 0.22 = 0.88 (88% of budget)
                        stage="writing"
                    )
                )

            # Should warn (>80%)
            assert tracker.data.should_warn("daily")

            # Not over budget yet
            assert not tracker.data.is_over_budget("daily")


class TestPreferencesManager:
    """Test PreferencesManager class."""

    @pytest.mark.asyncio
    async def test_preferences_defaults(self):
        """Test default preferences."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            prefs = PreferencesManager(session_path)

            assert prefs.get_model_for_stage("writing") == "claude-sonnet-4.5"
            assert prefs.get_auto_save_interval() == 30

    @pytest.mark.asyncio
    async def test_preferences_save_load(self):
        """Test saving and loading preferences."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            # Create and modify preferences
            prefs1 = PreferencesManager(session_path)
            prefs1.set_model_for_stage("writing", "gpt-4o")
            prefs1.data.auto_save_interval = 60
            await prefs1.save()

            # Load preferences
            prefs2 = PreferencesManager(session_path)
            assert prefs2.get_model_for_stage("writing") == "gpt-4o"
            assert prefs2.data.auto_save_interval == 60


class TestHistoryManager:
    """Test HistoryManager class."""

    @pytest.mark.asyncio
    async def test_history_tracking(self):
        """Test session history tracking."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            history = HistoryManager(session_path)

            entry = SessionHistoryEntry(
                session_id="test-session",
                project_name="Test Project",
                started_at=datetime.now(),
                total_cost=1.50
            )

            await history.add_session(entry)

            recent = history.get_recent_sessions(5)
            assert len(recent) == 1
            assert recent[0].session_id == "test-session"

    @pytest.mark.asyncio
    async def test_history_limit(self):
        """Test history entry limit (20 max)."""
        with TemporaryDirectory() as tmpdir:
            session_path = Path(tmpdir) / ".session"
            session_path.mkdir()

            history = HistoryManager(session_path)

            # Add 25 sessions
            for i in range(25):
                entry = SessionHistoryEntry(
                    session_id=f"session-{i}",
                    project_name="Test",
                    started_at=datetime.now()
                )
                await history.add_session(entry)

            # Should keep only last 20
            assert len(history.data.entries) == 20
            # Most recent should be session-24
            assert history.data.entries[0].session_id == "session-24"
