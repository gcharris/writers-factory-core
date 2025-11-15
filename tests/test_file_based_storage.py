"""Tests for file-based manuscript storage (Sprint 9).

Tests the new file-based storage architecture where:
- manifest.json contains structure and metadata only (NO content)
- Each scene is stored as an individual .md file
- Directory structure: scenes/ACT_*/CHAPTER_*/scene-id.md
- Compatible with direct editing in any text editor
"""

import pytest
import json
from pathlib import Path
from factory.core.manuscript.structure import Manuscript, Act, Chapter, Scene, Character
from factory.core.manuscript.storage import ManuscriptStorage


@pytest.fixture
def temp_manuscript_dir(tmp_path):
    """Create a temporary directory for manuscript storage."""
    manuscript_dir = tmp_path / "test_manuscript"
    manuscript_dir.mkdir()
    return manuscript_dir


@pytest.fixture
def sample_manuscript():
    """Create a sample manuscript for testing."""
    manuscript = Manuscript(
        title="Test Novel",
        author="Test Author"
    )

    # Add act
    act = Act(id="act-1", title="Act 1: Beginning")
    manuscript.acts.append(act)

    # Add chapter
    chapter = Chapter(id="chapter-1", title="Chapter 1: The Start")
    act.chapters.append(chapter)

    # Add scenes
    scene1 = Scene(
        id="scene-1",
        title="Scene 1: Opening",
        content="This is the opening scene. It sets the stage for the story.",
        notes="Remember to add more description"
    )
    scene2 = Scene(
        id="scene-2",
        title="Scene 2: Conflict",
        content="The protagonist faces their first challenge. Things get complicated.",
    )
    chapter.scenes.extend([scene1, scene2])

    # Add character
    char = Character(
        id="char-1",
        name="Alice",
        role="protagonist",
        core_traits=["brave", "curious"],
        values=["truth", "justice"]
    )
    manuscript.characters.append(char)

    return manuscript


class TestFileLBasedStorage:
    """Test suite for file-based manuscript storage."""

    def test_save_creates_individual_scene_files(self, temp_manuscript_dir, sample_manuscript):
        """Test that save() creates individual .md files for each scene."""
        storage = ManuscriptStorage(temp_manuscript_dir)

        # Save manuscript
        success = storage.save(sample_manuscript)
        assert success

        # Check that scene files were created
        scenes_dir = temp_manuscript_dir / "scenes"
        assert scenes_dir.exists()

        # Check act directory
        act_dir = scenes_dir / "act-1"
        assert act_dir.exists()

        # Check chapter directory
        chapter_dir = act_dir / "chapter-1"
        assert chapter_dir.exists()

        # Check scene files
        scene1_file = chapter_dir / "scene-1.md"
        scene2_file = chapter_dir / "scene-2.md"
        assert scene1_file.exists()
        assert scene2_file.exists()

        # Verify scene content
        scene1_content = scene1_file.read_text()
        assert "This is the opening scene" in scene1_content
        assert "Scene 1: Opening" in scene1_content

    def test_manifest_excludes_content(self, temp_manuscript_dir, sample_manuscript):
        """Test that manifest.json does NOT contain scene content."""
        storage = ManuscriptStorage(temp_manuscript_dir)
        storage.save(sample_manuscript)

        # Load manifest directly
        manifest_file = temp_manuscript_dir / "manuscript.json"
        with open(manifest_file, 'r') as f:
            manifest_data = json.load(f)

        # Check that scenes don't have content field
        act = manifest_data["acts"][0]
        chapter = act["chapters"][0]
        scene1 = chapter["scenes"][0]

        assert "content" not in scene1 or scene1["content"] == ""
        assert "file_path" in scene1
        assert scene1["file_path"].endswith("scene-1.md")

    def test_manifest_metadata(self, temp_manuscript_dir, sample_manuscript):
        """Test that manifest contains correct metadata for file-based storage."""
        storage = ManuscriptStorage(temp_manuscript_dir)
        storage.save(sample_manuscript)

        manifest_file = temp_manuscript_dir / "manuscript.json"
        with open(manifest_file, 'r') as f:
            manifest_data = json.load(f)

        # Check metadata
        metadata = manifest_data["_metadata"]
        assert metadata["version"] == "2.0"
        assert metadata["storage_type"] == "file_based"
        assert "saved_at" in metadata

    def test_load_reads_from_files(self, temp_manuscript_dir, sample_manuscript):
        """Test that load() reads scene content from individual files."""
        storage = ManuscriptStorage(temp_manuscript_dir)

        # Save manuscript
        storage.save(sample_manuscript)

        # Load it back
        loaded_manuscript = storage.load()

        assert loaded_manuscript is not None
        assert loaded_manuscript.title == "Test Novel"
        assert len(loaded_manuscript.acts) == 1

        # Check scene content was loaded
        scene1 = loaded_manuscript.acts[0].chapters[0].scenes[0]
        assert scene1.content == "This is the opening scene. It sets the stage for the story."
        assert scene1.word_count > 0

    def test_scene_file_format(self, temp_manuscript_dir, sample_manuscript):
        """Test that scene files have correct markdown format with metadata."""
        storage = ManuscriptStorage(temp_manuscript_dir)
        storage.save(sample_manuscript)

        # Read a scene file
        scene_file = temp_manuscript_dir / "scenes" / "act-1" / "chapter-1" / "scene-1.md"
        content = scene_file.read_text()

        # Check metadata header
        assert content.startswith("---")
        assert "id: scene-1" in content
        assert "title: Scene 1: Opening" in content
        assert "act: Act 1: Beginning" in content
        assert "chapter: Chapter 1: The Start" in content

        # Check content
        assert "This is the opening scene" in content

        # Check notes section
        assert "## Notes" in content
        assert "Remember to add more description" in content

    def test_save_scene_updates_individual_file(self, temp_manuscript_dir, sample_manuscript):
        """Test that save_scene() updates the individual scene file."""
        storage = ManuscriptStorage(temp_manuscript_dir)
        storage.save(sample_manuscript)

        # Update a scene
        new_content = "This is the UPDATED opening scene with new content!"
        success = storage.save_scene(sample_manuscript, "scene-1", new_content)
        assert success

        # Check that the file was updated
        scene_file = temp_manuscript_dir / "scenes" / "act-1" / "chapter-1" / "scene-1.md"
        file_content = scene_file.read_text()
        assert "UPDATED opening scene" in file_content

        # Load and verify
        loaded_manuscript = storage.load()
        scene1 = loaded_manuscript.acts[0].chapters[0].scenes[0]
        assert "UPDATED opening scene" in scene1.content

    def test_backward_compatibility_with_embedded_storage(self, temp_manuscript_dir, sample_manuscript):
        """Test that old embedded-content manuscripts can still be loaded."""
        # Create old-style manuscript with embedded content
        manifest_data = sample_manuscript.to_dict(include_content=True)
        manifest_data["_metadata"] = {
            "version": "1.0",
            "storage_type": "embedded"
        }

        manifest_file = temp_manuscript_dir / "manuscript.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest_data, f, indent=2)

        # Try to load it
        storage = ManuscriptStorage(temp_manuscript_dir)
        loaded = storage.load()

        assert loaded is not None
        assert loaded.title == "Test Novel"
        # Content should be loaded from manifest
        assert len(loaded.acts[0].chapters[0].scenes) == 2

    def test_directory_sanitization(self, temp_manuscript_dir):
        """Test that directory names with special characters are sanitized."""
        manuscript = Manuscript(title="Test", author="Author")
        act = Act(id="act:1/test", title="Act <1>: Test")
        chapter = Chapter(id="chapter*1?test", title="Chapter |1|: Test")
        scene = Scene(id="scene-1", title="Scene 1", content="Content")

        chapter.scenes.append(scene)
        act.chapters.append(chapter)
        manuscript.acts.append(act)

        storage = ManuscriptStorage(temp_manuscript_dir)
        success = storage.save(manuscript)
        assert success

        # Check that directories were created with sanitized names
        scenes_dir = temp_manuscript_dir / "scenes"
        assert any(scenes_dir.iterdir())  # At least one directory exists

    def test_word_count_tracking(self, temp_manuscript_dir, sample_manuscript):
        """Test that word counts are tracked correctly in file-based storage."""
        storage = ManuscriptStorage(temp_manuscript_dir)

        # Initial save
        storage.save(sample_manuscript)
        initial_word_count = sample_manuscript.acts[0].chapters[0].scenes[0].word_count

        # Update scene with more content
        new_content = "This is a much longer piece of content with many more words to increase the word count significantly."
        storage.save_scene(sample_manuscript, "scene-1", new_content)

        # Load and check word count
        loaded = storage.load()
        updated_word_count = loaded.acts[0].chapters[0].scenes[0].word_count

        assert updated_word_count > initial_word_count
        assert updated_word_count == len(new_content.split())

    def test_multiple_acts_and_chapters(self, temp_manuscript_dir):
        """Test file organization with multiple acts and chapters."""
        manuscript = Manuscript(title="Complex Novel", author="Author")

        # Create 2 acts with 2 chapters each
        for act_num in range(1, 3):
            act = Act(id=f"act-{act_num}", title=f"Act {act_num}")

            for chapter_num in range(1, 3):
                chapter = Chapter(id=f"chapter-{act_num}-{chapter_num}", title=f"Chapter {chapter_num}")

                # Add 2 scenes per chapter
                for scene_num in range(1, 3):
                    scene = Scene(
                        id=f"scene-{act_num}-{chapter_num}-{scene_num}",
                        title=f"Scene {scene_num}",
                        content=f"Content for Act {act_num}, Chapter {chapter_num}, Scene {scene_num}"
                    )
                    chapter.scenes.append(scene)

                act.chapters.append(chapter)

            manuscript.acts.append(act)

        storage = ManuscriptStorage(temp_manuscript_dir)
        success = storage.save(manuscript)
        assert success

        # Verify directory structure
        scenes_dir = temp_manuscript_dir / "scenes"
        act_dirs = list(scenes_dir.iterdir())
        assert len(act_dirs) == 2

        # Load and verify all content
        loaded = storage.load()
        assert len(loaded.acts) == 2
        assert len(loaded.acts[0].chapters) == 2
        assert len(loaded.acts[0].chapters[0].scenes) == 2

        # Verify content was loaded
        scene = loaded.acts[0].chapters[0].scenes[0]
        assert "Act 1" in scene.content

    def test_extract_content_from_md(self, temp_manuscript_dir):
        """Test that content extraction from markdown files works correctly."""
        storage = ManuscriptStorage(temp_manuscript_dir)

        # Create a sample markdown file with metadata
        markdown_content = """---
id: test-scene
title: Test Scene
act: Act 1
chapter: Chapter 1
word_count: 10
---

## Notes

This is a test note

---

This is the actual scene content that should be extracted.
It has multiple lines and should not include the metadata or notes."""

        # Test extraction
        extracted = storage._extract_content_from_md(markdown_content)

        assert "id: test-scene" not in extracted
        assert "## Notes" not in extracted
        assert "This is a test note" not in extracted
        assert "This is the actual scene content" in extracted
        assert "multiple lines" in extracted


class TestMigrationCompatibility:
    """Test that migration from old format to new format works correctly."""

    def test_migration_preserves_all_data(self, temp_manuscript_dir, sample_manuscript):
        """Test that migrating from embedded to file-based preserves all data."""
        # Save in old format (embedded content)
        manifest_data = sample_manuscript.to_dict(include_content=True)
        manifest_data["_metadata"] = {
            "version": "1.0",
            "storage_type": "embedded"
        }

        manifest_file = temp_manuscript_dir / "manuscript.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest_data, f)

        # Load and re-save in new format
        storage = ManuscriptStorage(temp_manuscript_dir)
        loaded = storage.load()
        storage.save(loaded)

        # Verify file-based storage was created
        scenes_dir = temp_manuscript_dir / "scenes"
        assert scenes_dir.exists()

        # Load again and verify all data
        reloaded = storage.load()
        assert reloaded.title == sample_manuscript.title
        assert len(reloaded.acts) == len(sample_manuscript.acts)
        assert len(reloaded.characters) == len(sample_manuscript.characters)

        # Verify scene content
        original_scene = sample_manuscript.acts[0].chapters[0].scenes[0]
        reloaded_scene = reloaded.acts[0].chapters[0].scenes[0]
        assert reloaded_scene.content == original_scene.content
        assert reloaded_scene.word_count == original_scene.word_count
