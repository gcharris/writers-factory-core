"""Tests for TUI components."""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from factory.tui import StatusBar, StageNavigator, WritersFactoryApp


class TestStatusBar:
    """Test StatusBar component."""
    
    def test_status_bar_creation(self):
        """Test creating status bar."""
        bar = StatusBar()
        assert bar.stage == "creation"
        assert bar.session_cost == 0.0
        
    def test_status_bar_update(self):
        """Test updating status bar values."""
        bar = StatusBar()
        bar.update(stage="writing", session_cost=1.50)
        
        assert bar.stage == "writing"
        assert bar.session_cost == 1.50
        
    def test_status_bar_render(self):
        """Test rendering status bar."""
        bar = StatusBar()
        bar.update(
            stage="writing",
            session_cost=2.50,
            last_save_time=datetime.now() - timedelta(seconds=45)
        )
        
        table = bar.render()
        assert table is not None
        
    def test_status_bar_save_status(self):
        """Test save status display."""
        bar = StatusBar()
        
        # Unsaved changes
        bar.update(has_unsaved_changes=True)
        table = bar.render()
        assert table is not None
        
        # Saved
        bar.update(
            has_unsaved_changes=False,
            last_save_time=datetime.now() - timedelta(seconds=30)
        )
        table = bar.render()
        assert table is not None


class TestStageNavigator:
    """Test StageNavigator component."""
    
    def test_navigator_creation(self):
        """Test creating navigator."""
        nav = StageNavigator()
        assert nav.current_stage == "creation"
        assert nav.stage_index == 0
        
    def test_navigator_next_stage(self):
        """Test moving to next stage."""
        nav = StageNavigator()
        
        assert nav.next_stage() == "writing"
        assert nav.next_stage() == "enhancing"
        assert nav.next_stage() == "analyzing"
        assert nav.next_stage() == "scoring"
        assert nav.next_stage() == "creation"  # Wraps around
        
    def test_navigator_prev_stage(self):
        """Test moving to previous stage."""
        nav = StageNavigator("scoring")
        
        assert nav.prev_stage() == "analyzing"
        assert nav.prev_stage() == "enhancing"
        assert nav.prev_stage() == "writing"
        assert nav.prev_stage() == "creation"
        assert nav.prev_stage() == "scoring"  # Wraps around
        
    def test_navigator_goto_stage(self):
        """Test jumping to specific stage."""
        nav = StageNavigator()
        
        assert nav.goto_stage("analyzing")
        assert nav.current_stage == "analyzing"
        
        # Invalid stage
        assert not nav.goto_stage("invalid")
        
    def test_navigator_stage_info(self):
        """Test getting stage information."""
        nav = StageNavigator()
        info = nav.get_stage_info("writing")
        
        assert info["title"] == "Writing"
        assert "tools" in info
        assert "color" in info
        assert len(info["tools"]) > 0
        
    def test_navigator_render_pipeline(self):
        """Test rendering pipeline."""
        nav = StageNavigator("writing")
        table = nav.render_pipeline()
        assert table is not None
        
    def test_navigator_render_stage_panel(self):
        """Test rendering stage panel."""
        nav = StageNavigator("enhancing")
        panel = nav.render_stage_panel()
        assert panel is not None


class TestWritersFactoryApp:
    """Test main application."""
    
    @pytest.mark.asyncio
    async def test_app_creation(self):
        """Test creating app."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            app = WritersFactoryApp(project_path)
            
            assert app.project_path == project_path
            assert app.session is not None
            assert app.cost_tracker is not None
            assert app.preferences is not None
            assert app.status_bar is not None
            assert app.navigator is not None
            
    @pytest.mark.asyncio
    async def test_app_layout(self):
        """Test creating layout."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            app = WritersFactoryApp(project_path)

            layout = app.make_layout()
            assert layout is not None
            assert layout.get("header") is not None
            assert layout.get("body") is not None
            assert layout.get("footer") is not None
            
    @pytest.mark.asyncio
    async def test_app_update_layout(self):
        """Test updating layout."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            app = WritersFactoryApp(project_path)
            
            layout = app.make_layout()
            app.update_layout(layout)
            # Should not raise
            
    @pytest.mark.asyncio
    async def test_app_handle_key_navigation(self):
        """Test keyboard navigation."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            app = WritersFactoryApp(project_path)
            
            initial_stage = app.navigator.current_stage
            await app.handle_key("tab")
            assert app.navigator.current_stage != initial_stage
            
    @pytest.mark.asyncio
    async def test_app_handle_key_quit(self):
        """Test quit key."""
        with TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            app = WritersFactoryApp(project_path)
            
            app.running = True
            await app.handle_key("q")
            assert not app.running
