"""Tests for manuscript importer."""

import pytest
import tempfile
import shutil
from pathlib import Path

from factory.tools import (
    ManuscriptImporter,
    import_from_directory,
    import_explants_volume_1,
)


class TestManuscriptImporter:
    """Tests for ManuscriptImporter class."""

    @pytest.fixture
    def temp_manuscript_dir(self):
        """Create temporary manuscript directory with test files."""
        temp_path = Path(tempfile.mkdtemp())

        # Create PART 1 directory with scenes
        part1_dir = temp_path / "PART 1"
        part1_dir.mkdir()

        # Create scene files
        (part1_dir / "1.1.1 Opening Scene.md").write_text(
            "This is the opening scene with some content."
        )
        (part1_dir / "1.1.2 Second Scene.md").write_text(
            "This is the second scene in chapter one."
        )
        (part1_dir / "1.2.1 Chapter Two Opening.md").write_text(
            "Chapter two begins here with new content."
        )

        # Create PART 2 directory with scenes
        part2_dir = temp_path / "PART 2"
        part2_dir.mkdir()

        (part2_dir / "2.1.1 Act Two Begins.md").write_text(
            "Act two starts with this exciting scene."
        )
        (part2_dir / "2.1.2 Midpoint Scene.md").write_text(
            "The midpoint of the story happens here."
        )

        yield temp_path

        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path)

    def test_importer_creation(self, temp_manuscript_dir):
        """Test creating importer."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        assert importer.source_path == temp_manuscript_dir

    def test_importer_invalid_path(self):
        """Test importer with invalid path."""
        with pytest.raises(ValueError, match="does not exist"):
            ManuscriptImporter(Path("/nonexistent/path"))

    def test_importer_file_path(self, temp_manuscript_dir):
        """Test importer with file instead of directory."""
        file_path = temp_manuscript_dir / "test.txt"
        file_path.write_text("test")

        with pytest.raises(ValueError, match="not a directory"):
            ManuscriptImporter(file_path)

    def test_find_part_directories(self, temp_manuscript_dir):
        """Test finding PART directories."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        part_dirs = importer._find_part_directories()

        assert len(part_dirs) == 2
        assert 1 in part_dirs
        assert 2 in part_dirs
        assert part_dirs[1].name == "PART 1"
        assert part_dirs[2].name == "PART 2"

    def test_find_scene_files(self, temp_manuscript_dir):
        """Test finding scene files."""
        importer = ManuscriptImporter(temp_manuscript_dir)
        part1_dir = temp_manuscript_dir / "PART 1"

        scenes = importer._find_scene_files(part1_dir)

        assert len(scenes) == 3

        # Check that we have the expected scenes (order may vary)
        scene_titles = [title for _, _, _, title, _ in scenes]
        assert "Opening Scene" in scene_titles
        assert "Second Scene" in scene_titles
        assert "Chapter Two Opening" in scene_titles

        # Check structure of one scene
        act_num, chapter_num, scene_num, title, file_path = scenes[0]
        assert act_num == 1
        assert chapter_num in [1, 2]
        assert scene_num in [1, 2]
        assert title in ["Opening Scene", "Second Scene", "Chapter Two Opening"]

    def test_import_manuscript(self, temp_manuscript_dir):
        """Test importing complete manuscript."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        manuscript = importer.import_manuscript(
            title="Test Novel",
            author="Test Author",
        )

        assert manuscript.title == "Test Novel"
        assert manuscript.author == "Test Author"
        assert len(manuscript.acts) == 2

        # Check Act 1
        act1 = manuscript.acts[0]
        assert act1.title == "Act 1"
        assert len(act1.chapters) == 2

        # Check Chapter 1.1
        chapter11 = act1.chapters[0]
        assert chapter11.title == "Chapter 1"
        assert len(chapter11.scenes) == 2

        # Check scene content
        scene = chapter11.scenes[0]
        assert scene.title == "Opening Scene"
        assert "opening scene" in scene.content.lower()
        assert scene.word_count > 0

        # Check Act 2
        act2 = manuscript.acts[1]
        assert act2.title == "Act 2"
        assert len(act2.chapters) == 1
        assert len(act2.chapters[0].scenes) == 2

    def test_import_manuscript_custom_prefixes(self, temp_manuscript_dir):
        """Test importing with custom act/chapter prefixes."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        manuscript = importer.import_manuscript(
            title="Test Novel",
            act_prefix="Part",
            chapter_prefix="Section",
        )

        assert manuscript.acts[0].title == "Part 1"
        assert manuscript.acts[0].chapters[0].title == "Section 1"

    def test_import_flat_structure(self):
        """Test importing from flat directory structure."""
        temp_path = Path(tempfile.mkdtemp())

        try:
            # Create scene files directly in root
            (temp_path / "1.1.1 Scene One.md").write_text("Content one")
            (temp_path / "1.1.2 Scene Two.md").write_text("Content two")

            importer = ManuscriptImporter(temp_path)
            manuscript = importer.import_manuscript(title="Flat Test")

            assert len(manuscript.acts) == 1
            assert len(manuscript.acts[0].chapters) == 1
            assert len(manuscript.acts[0].chapters[0].scenes) == 2

        finally:
            if temp_path.exists():
                shutil.rmtree(temp_path)

    def test_clean_scene_content(self, temp_manuscript_dir):
        """Test cleaning scene content."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        # Test with extra whitespace
        content = "  \n\n  Test content here  \n\n  "
        cleaned = importer._clean_scene_content(content)

        assert cleaned == "Test content here"

    def test_import_scene_word_count(self, temp_manuscript_dir):
        """Test that imported scenes have correct word count."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        manuscript = importer.import_manuscript(title="Test")

        # Get first scene
        scene = manuscript.acts[0].chapters[0].scenes[0]

        # Verify word count was calculated
        assert scene.word_count > 0
        assert scene.word_count == len(scene.content.split())

    def test_structure_summary(self, temp_manuscript_dir):
        """Test manuscript structure summary after import."""
        importer = ManuscriptImporter(temp_manuscript_dir)

        manuscript = importer.import_manuscript(title="Test")

        summary = manuscript.structure_summary

        assert summary["acts"] == 2
        assert summary["chapters"] == 3
        assert summary["scenes"] == 5
        assert summary["words"] > 0


class TestImportFunctions:
    """Tests for convenience import functions."""

    @pytest.fixture
    def temp_manuscript_dir(self):
        """Create temporary manuscript directory."""
        temp_path = Path(tempfile.mkdtemp())

        # Create PART 1 directory with one scene
        part1_dir = temp_path / "PART 1"
        part1_dir.mkdir()
        (part1_dir / "1.1.1 Test Scene.md").write_text("Test content here.")

        yield temp_path

        if temp_path.exists():
            shutil.rmtree(temp_path)

    def test_import_from_directory(self, temp_manuscript_dir):
        """Test import_from_directory function."""
        manuscript = import_from_directory(
            source_dir=temp_manuscript_dir,
            title="Generic Import",
            author="Test Author",
        )

        assert manuscript.title == "Generic Import"
        assert manuscript.author == "Test Author"
        assert len(manuscript.acts) > 0

    def test_import_explants_volume_1(self, temp_manuscript_dir):
        """Test import_explants_volume_1 function."""
        manuscript = import_explants_volume_1(
            source_dir=temp_manuscript_dir,
            author="Test Author",
        )

        assert manuscript.title == "The Explants - Volume 1"
        assert manuscript.author == "Test Author"
        assert len(manuscript.acts) > 0

    def test_import_with_custom_title(self, temp_manuscript_dir):
        """Test import with custom title."""
        manuscript = import_explants_volume_1(
            source_dir=temp_manuscript_dir,
            title="Custom Title",
        )

        assert manuscript.title == "Custom Title"


class TestSceneFilePatterns:
    """Tests for scene file pattern matching."""

    def test_valid_scene_patterns(self):
        """Test various valid scene file patterns."""
        importer = ManuscriptImporter(Path.cwd())  # Path doesn't matter for pattern test

        valid_patterns = [
            "1.1.1 Opening Scene.md",
            "1.2.3 Middle Scene Title.md",
            "2.1.1 Act Two Begins.md",
            "3.10.25 Long Chapter Many Scenes.md",
        ]

        pattern = importer.SCENE_FILE_PATTERN

        for filename in valid_patterns:
            match = pytest.importorskip("re").match(pattern, filename)
            assert match is not None, f"Failed to match: {filename}"

    def test_invalid_scene_patterns(self):
        """Test invalid scene file patterns."""
        importer = ManuscriptImporter(Path.cwd())

        invalid_patterns = [
            "Scene Without Numbers.md",
            "1.1 Missing Scene Number.md",
            "1.1.1.md",  # No title
            "1.1.1 No Extension",
            "a.b.c Invalid Numbers.md",
        ]

        pattern = importer.SCENE_FILE_PATTERN

        for filename in invalid_patterns:
            match = pytest.importorskip("re").match(pattern, filename)
            assert match is None, f"Should not match: {filename}"


class TestPartDirectoryPatterns:
    """Tests for PART directory pattern matching."""

    def test_valid_part_patterns(self):
        """Test various valid PART directory patterns."""
        importer = ManuscriptImporter(Path.cwd())

        valid_patterns = [
            "PART 1",
            "PART 2",
            "PART 10",
            "part 1",  # Case insensitive
            "Part 3",
        ]

        pattern = importer.PART_DIR_PATTERN

        for dirname in valid_patterns:
            match = pytest.importorskip("re").match(pattern, dirname, pytest.importorskip("re").IGNORECASE)
            assert match is not None, f"Failed to match: {dirname}"

    def test_invalid_part_patterns(self):
        """Test invalid PART directory patterns."""
        importer = ManuscriptImporter(Path.cwd())

        invalid_patterns = [
            "CHAPTER 1",
            "ACT 1",
            "PART",
            "PART A",
            "1 PART",
        ]

        pattern = importer.PART_DIR_PATTERN

        for dirname in invalid_patterns:
            match = pytest.importorskip("re").match(pattern, dirname, pytest.importorskip("re").IGNORECASE)
            assert match is None, f"Should not match: {dirname}"
