"""Tests for manuscript structure and storage."""

import pytest
import json
from pathlib import Path
import tempfile
import shutil

from factory.core.manuscript import (
    Scene,
    Chapter,
    Act,
    Manuscript,
    ManuscriptStorage,
)


class TestScene:
    """Tests for Scene class."""

    def test_scene_creation(self):
        """Test creating a scene."""
        scene = Scene(
            id="scene-1",
            title="Opening Scene",
            content="It was a dark and stormy night.",
        )

        assert scene.id == "scene-1"
        assert scene.title == "Opening Scene"
        assert scene.content == "It was a dark and stormy night."
        assert scene.word_count == 7  # Auto-calculated

    def test_scene_word_count_calculation(self):
        """Test automatic word count calculation."""
        scene = Scene(
            id="scene-1",
            title="Test",
            content="This is a test scene with ten words in it.",
        )

        assert scene.word_count == 10

    def test_scene_update_content(self):
        """Test updating scene content."""
        scene = Scene(id="scene-1", title="Test", content="Original content.")

        scene.update_content("New content with more words in it.")

        assert scene.content == "New content with more words in it."
        assert scene.word_count == 7

    def test_scene_to_dict(self):
        """Test converting scene to dictionary."""
        scene = Scene(
            id="scene-1",
            title="Test Scene",
            content="Content",
            notes="Some notes",
        )

        data = scene.to_dict()

        assert data["id"] == "scene-1"
        assert data["title"] == "Test Scene"
        assert data["content"] == "Content"
        assert data["notes"] == "Some notes"
        assert "metadata" in data

    def test_scene_from_dict(self):
        """Test creating scene from dictionary."""
        data = {
            "id": "scene-1",
            "title": "Test Scene",
            "content": "Content here",
            "word_count": 2,
            "notes": "Notes",
            "metadata": {"status": "draft"},
        }

        scene = Scene.from_dict(data)

        assert scene.id == "scene-1"
        assert scene.title == "Test Scene"
        assert scene.content == "Content here"
        assert scene.word_count == 2
        assert scene.notes == "Notes"
        assert scene.metadata["status"] == "draft"


class TestChapter:
    """Tests for Chapter class."""

    def test_chapter_creation(self):
        """Test creating a chapter."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        assert chapter.id == "chapter-1"
        assert chapter.title == "Chapter One"
        assert len(chapter.scenes) == 0

    def test_add_scene(self):
        """Test adding a scene to a chapter."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        scene = chapter.add_scene(
            title="Opening",
            content="The story begins.",
        )

        assert len(chapter.scenes) == 1
        assert scene.title == "Opening"
        assert scene.content == "The story begins."
        assert scene.id  # Should have generated ID

    def test_get_scene(self):
        """Test retrieving a scene by ID."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        scene1 = chapter.add_scene(title="Scene 1")
        scene2 = chapter.add_scene(title="Scene 2")

        retrieved = chapter.get_scene(scene2.id)

        assert retrieved is not None
        assert retrieved.title == "Scene 2"

    def test_get_scene_not_found(self):
        """Test retrieving non-existent scene."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        retrieved = chapter.get_scene("non-existent")

        assert retrieved is None

    def test_remove_scene(self):
        """Test removing a scene."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        scene = chapter.add_scene(title="Scene 1")
        assert len(chapter.scenes) == 1

        removed = chapter.remove_scene(scene.id)

        assert removed is True
        assert len(chapter.scenes) == 0

    def test_remove_scene_not_found(self):
        """Test removing non-existent scene."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        removed = chapter.remove_scene("non-existent")

        assert removed is False

    def test_total_word_count(self):
        """Test calculating total word count."""
        chapter = Chapter(id="chapter-1", title="Chapter One")

        chapter.add_scene(title="Scene 1", content="Five words in scene one.")
        chapter.add_scene(title="Scene 2", content="Six words in scene two here.")

        assert chapter.total_word_count == 11

    def test_chapter_to_dict(self):
        """Test converting chapter to dictionary."""
        chapter = Chapter(id="chapter-1", title="Chapter One")
        chapter.add_scene(title="Scene 1", content="Content")

        data = chapter.to_dict()

        assert data["id"] == "chapter-1"
        assert data["title"] == "Chapter One"
        assert len(data["scenes"]) == 1
        assert data["scenes"][0]["title"] == "Scene 1"

    def test_chapter_from_dict(self):
        """Test creating chapter from dictionary."""
        data = {
            "id": "chapter-1",
            "title": "Chapter One",
            "scenes": [
                {
                    "id": "scene-1",
                    "title": "Scene 1",
                    "content": "Content",
                    "word_count": 1,
                    "notes": "",
                    "metadata": {},
                }
            ],
            "notes": "",
            "metadata": {},
        }

        chapter = Chapter.from_dict(data)

        assert chapter.id == "chapter-1"
        assert chapter.title == "Chapter One"
        assert len(chapter.scenes) == 1
        assert chapter.scenes[0].title == "Scene 1"


class TestAct:
    """Tests for Act class."""

    def test_act_creation(self):
        """Test creating an act."""
        act = Act(id="act-1", title="Act One")

        assert act.id == "act-1"
        assert act.title == "Act One"
        assert len(act.chapters) == 0

    def test_add_chapter(self):
        """Test adding a chapter to an act."""
        act = Act(id="act-1", title="Act One")

        chapter = act.add_chapter(title="Chapter One")

        assert len(act.chapters) == 1
        assert chapter.title == "Chapter One"
        assert chapter.id

    def test_get_chapter(self):
        """Test retrieving a chapter by ID."""
        act = Act(id="act-1", title="Act One")

        chapter1 = act.add_chapter(title="Chapter 1")
        chapter2 = act.add_chapter(title="Chapter 2")

        retrieved = chapter2_retrieved = act.get_chapter(chapter2.id)

        assert retrieved is not None
        assert retrieved.title == "Chapter 2"

    def test_remove_chapter(self):
        """Test removing a chapter."""
        act = Act(id="act-1", title="Act One")

        chapter = act.add_chapter(title="Chapter 1")
        assert len(act.chapters) == 1

        removed = act.remove_chapter(chapter.id)

        assert removed is True
        assert len(act.chapters) == 0

    def test_total_word_count(self):
        """Test calculating total word count."""
        act = Act(id="act-1", title="Act One")

        chapter1 = act.add_chapter(title="Chapter 1")
        chapter1.add_scene(title="Scene 1", content="Five words in this scene.")

        chapter2 = act.add_chapter(title="Chapter 2")
        chapter2.add_scene(title="Scene 2", content="Six words in this one too.")

        assert act.total_word_count == 11

    def test_act_to_dict(self):
        """Test converting act to dictionary."""
        act = Act(id="act-1", title="Act One")
        chapter = act.add_chapter(title="Chapter 1")
        chapter.add_scene(title="Scene 1", content="Content")

        data = act.to_dict()

        assert data["id"] == "act-1"
        assert data["title"] == "Act One"
        assert len(data["chapters"]) == 1
        assert data["chapters"][0]["title"] == "Chapter 1"

    def test_act_from_dict(self):
        """Test creating act from dictionary."""
        data = {
            "id": "act-1",
            "title": "Act One",
            "chapters": [
                {
                    "id": "chapter-1",
                    "title": "Chapter 1",
                    "scenes": [],
                    "notes": "",
                    "metadata": {},
                }
            ],
            "notes": "",
            "metadata": {},
        }

        act = Act.from_dict(data)

        assert act.id == "act-1"
        assert act.title == "Act One"
        assert len(act.chapters) == 1


class TestManuscript:
    """Tests for Manuscript class."""

    def test_manuscript_creation(self):
        """Test creating a manuscript."""
        manuscript = Manuscript(
            title="Test Novel",
            author="Test Author",
        )

        assert manuscript.title == "Test Novel"
        assert manuscript.author == "Test Author"
        assert len(manuscript.acts) == 0

    def test_add_act(self):
        """Test adding an act."""
        manuscript = Manuscript(title="Test Novel")

        act = manuscript.add_act(title="Act One")

        assert len(manuscript.acts) == 1
        assert act.title == "Act One"
        assert act.id

    def test_add_chapter(self):
        """Test adding a chapter to an act."""
        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")

        chapter = manuscript.add_chapter(act.id, title="Chapter One")

        assert chapter is not None
        assert chapter.title == "Chapter One"
        assert len(act.chapters) == 1

    def test_add_chapter_invalid_act(self):
        """Test adding chapter to non-existent act."""
        manuscript = Manuscript(title="Test Novel")

        chapter = manuscript.add_chapter("invalid-act", title="Chapter One")

        assert chapter is None

    def test_add_scene(self):
        """Test adding a scene to a chapter."""
        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")

        scene = manuscript.add_scene(
            chapter.id,
            title="Opening Scene",
            content="It begins.",
        )

        assert scene is not None
        assert scene.title == "Opening Scene"
        assert len(chapter.scenes) == 1

    def test_get_act(self):
        """Test retrieving an act."""
        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")

        retrieved = manuscript.get_act(act.id)

        assert retrieved is not None
        assert retrieved.title == "Act One"

    def test_get_chapter(self):
        """Test retrieving a chapter."""
        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")

        retrieved = manuscript.get_chapter(chapter.id)

        assert retrieved is not None
        assert retrieved.title == "Chapter One"

    def test_get_scene(self):
        """Test retrieving a scene."""
        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")
        scene = manuscript.add_scene(chapter.id, title="Opening Scene")

        retrieved = manuscript.get_scene(scene.id)

        assert retrieved is not None
        assert retrieved.title == "Opening Scene"

    def test_total_word_count(self):
        """Test calculating total word count."""
        manuscript = Manuscript(title="Test Novel")

        act1 = manuscript.add_act(title="Act One")
        chapter1 = manuscript.add_chapter(act1.id, title="Chapter 1")
        manuscript.add_scene(
            chapter1.id,
            title="Scene 1",
            content="Five words in this scene.",
        )

        act2 = manuscript.add_act(title="Act Two")
        chapter2 = manuscript.add_chapter(act2.id, title="Chapter 2")
        manuscript.add_scene(
            chapter2.id,
            title="Scene 2",
            content="Six words in this one too.",
        )

        assert manuscript.total_word_count == 11

    def test_structure_summary(self):
        """Test getting structure summary."""
        manuscript = Manuscript(title="Test Novel")

        act1 = manuscript.add_act(title="Act One")
        chapter1 = manuscript.add_chapter(act1.id, title="Chapter 1")
        manuscript.add_scene(chapter1.id, title="Scene 1", content="Some content here.")

        act2 = manuscript.add_act(title="Act Two")
        chapter2 = manuscript.add_chapter(act2.id, title="Chapter 2")
        manuscript.add_scene(chapter2.id, title="Scene 2", content="More content.")
        manuscript.add_scene(chapter2.id, title="Scene 3", content="Even more.")

        summary = manuscript.structure_summary

        assert summary["acts"] == 2
        assert summary["chapters"] == 2
        assert summary["scenes"] == 3
        assert summary["words"] == 7

    def test_manuscript_to_dict(self):
        """Test converting manuscript to dictionary."""
        manuscript = Manuscript(title="Test Novel", author="Test Author")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")
        manuscript.add_scene(chapter.id, title="Scene 1", content="Content")

        data = manuscript.to_dict()

        assert data["title"] == "Test Novel"
        assert data["author"] == "Test Author"
        assert len(data["acts"]) == 1
        assert data["acts"][0]["title"] == "Act One"

    def test_manuscript_from_dict(self):
        """Test creating manuscript from dictionary."""
        data = {
            "title": "Test Novel",
            "author": "Test Author",
            "acts": [
                {
                    "id": "act-1",
                    "title": "Act One",
                    "chapters": [
                        {
                            "id": "chapter-1",
                            "title": "Chapter 1",
                            "scenes": [
                                {
                                    "id": "scene-1",
                                    "title": "Scene 1",
                                    "content": "Content",
                                    "word_count": 1,
                                    "notes": "",
                                    "metadata": {},
                                }
                            ],
                            "notes": "",
                            "metadata": {},
                        }
                    ],
                    "notes": "",
                    "metadata": {},
                }
            ],
            "notes": "",
            "metadata": {},
        }

        manuscript = Manuscript.from_dict(data)

        assert manuscript.title == "Test Novel"
        assert manuscript.author == "Test Author"
        assert len(manuscript.acts) == 1
        assert manuscript.acts[0].title == "Act One"
        assert len(manuscript.acts[0].chapters) == 1
        assert len(manuscript.acts[0].chapters[0].scenes) == 1


class TestManuscriptStorage:
    """Tests for ManuscriptStorage class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path)

    def test_storage_creation(self, temp_dir):
        """Test creating storage."""
        storage = ManuscriptStorage(temp_dir / "test-manuscript")

        assert storage.storage_path == temp_dir / "test-manuscript"
        assert storage.backup_enabled is True

    def test_save_and_load(self, temp_dir):
        """Test saving and loading manuscript."""
        storage_path = temp_dir / "test-manuscript"
        storage = ManuscriptStorage(storage_path)

        # Create manuscript
        manuscript = Manuscript(title="Test Novel", author="Test Author")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")
        manuscript.add_scene(
            chapter.id,
            title="Opening Scene",
            content="It was a dark and stormy night.",
        )

        # Save
        result = storage.save(manuscript)
        assert result is True

        # Load
        loaded = storage.load()
        assert loaded is not None
        assert loaded.title == "Test Novel"
        assert loaded.author == "Test Author"
        assert len(loaded.acts) == 1
        assert loaded.acts[0].title == "Act One"
        assert len(loaded.acts[0].chapters) == 1
        assert len(loaded.acts[0].chapters[0].scenes) == 1

    def test_save_creates_backup(self, temp_dir):
        """Test that save creates backup."""
        storage_path = temp_dir / "test-manuscript"
        storage = ManuscriptStorage(storage_path, backup_enabled=True)

        manuscript = Manuscript(title="Test Novel")

        # First save
        storage.save(manuscript)

        # Second save should create backup
        manuscript.author = "Updated Author"
        storage.save(manuscript)

        backup_path = storage_path / (storage.MANIFEST_FILE + storage.BACKUP_SUFFIX)
        assert backup_path.exists()

    def test_load_nonexistent(self, temp_dir):
        """Test loading non-existent manuscript."""
        storage = ManuscriptStorage(temp_dir / "nonexistent")

        loaded = storage.load()

        assert loaded is None

    def test_exists(self, temp_dir):
        """Test checking if manuscript exists."""
        storage_path = temp_dir / "test-manuscript"
        storage = ManuscriptStorage(storage_path)

        assert storage.exists() is False

        manuscript = Manuscript(title="Test Novel")
        storage.save(manuscript)

        assert storage.exists() is True

    def test_delete(self, temp_dir):
        """Test deleting manuscript."""
        storage_path = temp_dir / "test-manuscript"
        storage = ManuscriptStorage(storage_path)

        manuscript = Manuscript(title="Test Novel")
        storage.save(manuscript)

        assert storage.exists() is True

        result = storage.delete()

        assert result is True
        assert storage.exists() is False

    def test_export_scenes(self, temp_dir):
        """Test exporting scenes to markdown files."""
        storage_path = temp_dir / "test-manuscript"
        storage = ManuscriptStorage(storage_path)

        manuscript = Manuscript(title="Test Novel")
        act = manuscript.add_act(title="Act One")
        chapter = manuscript.add_chapter(act.id, title="Chapter One")
        scene = manuscript.add_scene(
            chapter.id,
            title="Opening Scene",
            content="It was a dark and stormy night.",
        )

        result = storage.export_scenes(manuscript)

        assert result is True

        scene_file = storage_path / storage.SCENES_DIR / f"{scene.id}.md"
        assert scene_file.exists()

        content = scene_file.read_text()
        assert "Opening Scene" in content
        assert "It was a dark and stormy night." in content

    def test_create_new(self, temp_dir):
        """Test creating new manuscript storage."""
        storage_path = temp_dir / "test-manuscript"

        storage = ManuscriptStorage.create_new(
            storage_path,
            title="New Novel",
            author="New Author",
        )

        assert storage.exists() is True

        loaded = storage.load()
        assert loaded is not None
        assert loaded.title == "New Novel"
        assert loaded.author == "New Author"
