"""Manuscript structure data models.

Provides hierarchical data models for organizing novels:
- Scene: Individual scene with content
- Chapter: Collection of scenes
- Act: Collection of chapters
- Manuscript: Complete work with multiple acts
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path
import uuid


@dataclass
class Scene:
    """Individual scene in a chapter.

    Attributes:
        id: Unique identifier
        title: Scene title
        content: Scene text content
        word_count: Number of words in content
        notes: Optional notes about the scene
        metadata: Additional metadata (tags, status, etc.)
    """

    id: str
    title: str
    content: str = ""
    word_count: int = 0
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate word count if not provided."""
        if self.content and self.word_count == 0:
            self.word_count = len(self.content.split())

    def update_content(self, content: str) -> None:
        """Update scene content and recalculate word count.

        Args:
            content: New scene content
        """
        self.content = content
        self.word_count = len(content.split())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "notes": self.notes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scene":
        """Create Scene from dictionary.

        Args:
            data: Dictionary with scene data

        Returns:
            Scene instance
        """
        return cls(
            id=data["id"],
            title=data["title"],
            content=data.get("content", ""),
            word_count=data.get("word_count", 0),
            notes=data.get("notes", ""),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Chapter:
    """Chapter containing multiple scenes.

    Attributes:
        id: Unique identifier
        title: Chapter title
        scenes: List of scenes in this chapter
        notes: Optional notes about the chapter
        metadata: Additional metadata
    """

    id: str
    title: str
    scenes: List[Scene] = field(default_factory=list)
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_scene(self, title: str, content: str = "", scene_id: Optional[str] = None) -> Scene:
        """Add a new scene to this chapter.

        Args:
            title: Scene title
            content: Scene content
            scene_id: Optional specific ID (generates UUID if not provided)

        Returns:
            Created Scene instance
        """
        scene = Scene(
            id=scene_id or str(uuid.uuid4()),
            title=title,
            content=content,
        )
        self.scenes.append(scene)
        return scene

    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get scene by ID.

        Args:
            scene_id: Scene identifier

        Returns:
            Scene if found, None otherwise
        """
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None

    def remove_scene(self, scene_id: str) -> bool:
        """Remove scene by ID.

        Args:
            scene_id: Scene identifier

        Returns:
            True if removed, False if not found
        """
        for i, scene in enumerate(self.scenes):
            if scene.id == scene_id:
                self.scenes.pop(i)
                return True
        return False

    @property
    def total_word_count(self) -> int:
        """Calculate total word count for all scenes.

        Returns:
            Sum of word counts
        """
        return sum(scene.word_count for scene in self.scenes)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "title": self.title,
            "scenes": [scene.to_dict() for scene in self.scenes],
            "notes": self.notes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chapter":
        """Create Chapter from dictionary.

        Args:
            data: Dictionary with chapter data

        Returns:
            Chapter instance
        """
        chapter = cls(
            id=data["id"],
            title=data["title"],
            notes=data.get("notes", ""),
            metadata=data.get("metadata", {}),
        )
        chapter.scenes = [Scene.from_dict(s) for s in data.get("scenes", [])]
        return chapter


@dataclass
class Act:
    """Act containing multiple chapters.

    Attributes:
        id: Unique identifier
        title: Act title
        chapters: List of chapters in this act
        notes: Optional notes about the act
        metadata: Additional metadata
    """

    id: str
    title: str
    chapters: List[Chapter] = field(default_factory=list)
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_chapter(self, title: str, chapter_id: Optional[str] = None) -> Chapter:
        """Add a new chapter to this act.

        Args:
            title: Chapter title
            chapter_id: Optional specific ID (generates UUID if not provided)

        Returns:
            Created Chapter instance
        """
        chapter = Chapter(
            id=chapter_id or str(uuid.uuid4()),
            title=title,
        )
        self.chapters.append(chapter)
        return chapter

    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """Get chapter by ID.

        Args:
            chapter_id: Chapter identifier

        Returns:
            Chapter if found, None otherwise
        """
        for chapter in self.chapters:
            if chapter.id == chapter_id:
                return chapter
        return None

    def remove_chapter(self, chapter_id: str) -> bool:
        """Remove chapter by ID.

        Args:
            chapter_id: Chapter identifier

        Returns:
            True if removed, False if not found
        """
        for i, chapter in enumerate(self.chapters):
            if chapter.id == chapter_id:
                self.chapters.pop(i)
                return True
        return False

    @property
    def total_word_count(self) -> int:
        """Calculate total word count for all chapters.

        Returns:
            Sum of word counts
        """
        return sum(chapter.total_word_count for chapter in self.chapters)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "title": self.title,
            "chapters": [chapter.to_dict() for chapter in self.chapters],
            "notes": self.notes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Act":
        """Create Act from dictionary.

        Args:
            data: Dictionary with act data

        Returns:
            Act instance
        """
        act = cls(
            id=data["id"],
            title=data["title"],
            notes=data.get("notes", ""),
            metadata=data.get("metadata", {}),
        )
        act.chapters = [Chapter.from_dict(c) for c in data.get("chapters", [])]
        return act


@dataclass
class Manuscript:
    """Complete manuscript with acts, chapters, and scenes.

    Attributes:
        title: Manuscript title
        author: Author name
        acts: List of acts in this manuscript
        notes: Optional notes about the manuscript
        metadata: Additional metadata (genre, status, version, etc.)
    """

    title: str
    author: str = ""
    acts: List[Act] = field(default_factory=list)
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_act(self, title: str, act_id: Optional[str] = None) -> Act:
        """Add a new act to this manuscript.

        Args:
            title: Act title
            act_id: Optional specific ID (generates UUID if not provided)

        Returns:
            Created Act instance
        """
        act = Act(
            id=act_id or str(uuid.uuid4()),
            title=title,
        )
        self.acts.append(act)
        return act

    def add_chapter(self, act_id: str, title: str, chapter_id: Optional[str] = None) -> Optional[Chapter]:
        """Add a chapter to a specific act.

        Args:
            act_id: Act identifier
            title: Chapter title
            chapter_id: Optional specific ID

        Returns:
            Created Chapter instance, or None if act not found
        """
        act = self.get_act(act_id)
        if act:
            return act.add_chapter(title, chapter_id)
        return None

    def add_scene(self, chapter_id: str, title: str, content: str = "", scene_id: Optional[str] = None) -> Optional[Scene]:
        """Add a scene to a specific chapter.

        Args:
            chapter_id: Chapter identifier
            title: Scene title
            content: Scene content
            scene_id: Optional specific ID

        Returns:
            Created Scene instance, or None if chapter not found
        """
        for act in self.acts:
            chapter = act.get_chapter(chapter_id)
            if chapter:
                return chapter.add_scene(title, content, scene_id)
        return None

    def get_act(self, act_id: str) -> Optional[Act]:
        """Get act by ID.

        Args:
            act_id: Act identifier

        Returns:
            Act if found, None otherwise
        """
        for act in self.acts:
            if act.id == act_id:
                return act
        return None

    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """Get chapter by ID (searches all acts).

        Args:
            chapter_id: Chapter identifier

        Returns:
            Chapter if found, None otherwise
        """
        for act in self.acts:
            chapter = act.get_chapter(chapter_id)
            if chapter:
                return chapter
        return None

    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get scene by ID (searches all acts and chapters).

        Args:
            scene_id: Scene identifier

        Returns:
            Scene if found, None otherwise
        """
        for act in self.acts:
            for chapter in act.chapters:
                scene = chapter.get_scene(scene_id)
                if scene:
                    return scene
        return None

    @property
    def total_word_count(self) -> int:
        """Calculate total word count for entire manuscript.

        Returns:
            Sum of word counts
        """
        return sum(act.total_word_count for act in self.acts)

    @property
    def structure_summary(self) -> Dict[str, int]:
        """Get summary of manuscript structure.

        Returns:
            Dictionary with counts of acts, chapters, scenes, words
        """
        total_chapters = sum(len(act.chapters) for act in self.acts)
        total_scenes = sum(
            len(chapter.scenes)
            for act in self.acts
            for chapter in act.chapters
        )

        return {
            "acts": len(self.acts),
            "chapters": total_chapters,
            "scenes": total_scenes,
            "words": self.total_word_count,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "title": self.title,
            "author": self.author,
            "acts": [act.to_dict() for act in self.acts],
            "notes": self.notes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Manuscript":
        """Create Manuscript from dictionary.

        Args:
            data: Dictionary with manuscript data

        Returns:
            Manuscript instance
        """
        manuscript = cls(
            title=data["title"],
            author=data.get("author", ""),
            notes=data.get("notes", ""),
            metadata=data.get("metadata", {}),
        )
        manuscript.acts = [Act.from_dict(a) for a in data.get("acts", [])]
        return manuscript
