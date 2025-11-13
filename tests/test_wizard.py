"""Tests for creation wizard."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from factory.wizard import CreationWizard, WizardPhase, WizardResult


class TestCreationWizard:
    """Test creation wizard."""

    def test_wizard_creation(self):
        """Test creating wizard."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            assert wizard.project_path == Path(tmpdir)
            assert wizard.current_phase == WizardPhase.FOUNDATION
            assert len(wizard.responses) == 0

    def test_get_phase_questions(self):
        """Test getting questions for each phase."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            # Foundation questions
            foundation_q = wizard.get_phase_questions(WizardPhase.FOUNDATION)
            assert len(foundation_q) > 0
            assert any("genre" in q.lower() for q in foundation_q)
            
            # Character questions
            character_q = wizard.get_phase_questions(WizardPhase.CHARACTER)
            assert len(character_q) > 0
            assert any("protagonist" in q.lower() for q in character_q)

    def test_record_response(self):
        """Test recording responses."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            wizard.record_response("What is your story about?", "A space adventure")
            
            assert len(wizard.responses) == 1
            assert wizard.responses["What is your story about?"] == "A space adventure"

    def test_advance_phase(self):
        """Test advancing through phases."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            assert wizard.current_phase == WizardPhase.FOUNDATION
            
            advanced = wizard.advance_phase()
            assert advanced is True
            assert wizard.current_phase == WizardPhase.CHARACTER
            
            wizard.advance_phase()
            assert wizard.current_phase == WizardPhase.PLOT

    def test_generate_story_bible(self):
        """Test generating story bible."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            # Add some responses
            wizard.record_response("What genre best fits your story?", "Science Fiction")
            wizard.record_response("Who is your protagonist?", "A space explorer")
            wizard.record_response("What is the core theme?", "Finding home")
            
            result = wizard.generate_story_bible()
            
            assert isinstance(result, WizardResult)
            assert len(result.story_bible) > 0
            assert result.word_count > 0
            assert "Science Fiction" in result.story_bible
            assert "space explorer" in result.story_bible

    def test_save_story_bible(self):
        """Test saving story bible to file."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            wizard.record_response("What genre?", "Fantasy")
            result = wizard.generate_story_bible()
            
            output_path = wizard.save_story_bible(result)
            
            assert output_path.exists()
            assert output_path.name == "story_bible.md"
            
            content = output_path.read_text()
            assert "Fantasy" in content

    def test_story_beats_included(self):
        """Test that 15-beat narrative structure is included."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))

            assert len(wizard.STORY_BEATS) == 15
            assert "Opening Image" in wizard.STORY_BEATS
            assert "Midpoint" in wizard.STORY_BEATS
            assert "Final Image" in wizard.STORY_BEATS


class TestWizardPhases:
    """Test wizard phase progression."""

    def test_all_phases_have_questions(self):
        """Test that all phases have questions defined."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            for phase in WizardPhase:
                questions = wizard.get_phase_questions(phase)
                assert len(questions) > 0, f"Phase {phase} has no questions"

    def test_complete_workflow(self):
        """Test complete wizard workflow."""
        with TemporaryDirectory() as tmpdir:
            wizard = CreationWizard(Path(tmpdir))
            
            # Go through all phases
            for phase in WizardPhase:
                questions = wizard.get_phase_questions(phase)
                for q in questions[:2]:  # Answer first 2 questions of each phase
                    wizard.record_response(q, f"Answer for {q}")
                wizard.advance_phase()
            
            # Generate bible
            result = wizard.generate_story_bible()
            
            assert result.word_count > 100
            assert len(result.responses) > 0
