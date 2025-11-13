"""Manuscript storage and persistence.

Handles saving and loading manuscripts to/from JSON files,
with support for backup and atomic writes.
"""

import json
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from factory.core.manuscript.structure import Manuscript


class ManuscriptStorage:
    """Handles manuscript persistence to JSON files.

    Storage format:
    - Main file: manuscript.json
    - Backup file: manuscript.json.backup
    - Individual scene files: scenes/{scene_id}.md (optional)

    Attributes:
        storage_path: Path to storage directory
        backup_enabled: Whether to create backup before saving
    """

    MANIFEST_FILE = "manuscript.json"
    BACKUP_SUFFIX = ".backup"
    SCENES_DIR = "scenes"

    def __init__(self, storage_path: Path, backup_enabled: bool = True):
        """Initialize manuscript storage.

        Args:
            storage_path: Directory for manuscript storage
            backup_enabled: Create backup before each save
        """
        self.storage_path = Path(storage_path)
        self.backup_enabled = backup_enabled

    def save(self, manuscript: Manuscript) -> bool:
        """Save manuscript to JSON file.

        Uses atomic write (temp file + rename) to prevent corruption.

        Args:
            manuscript: Manuscript to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure storage directory exists
            self.storage_path.mkdir(parents=True, exist_ok=True)

            manifest_path = self.storage_path / self.MANIFEST_FILE

            # Create backup if file exists
            if self.backup_enabled and manifest_path.exists():
                self._create_backup(manifest_path)

            # Convert to dictionary
            data = manuscript.to_dict()

            # Add metadata
            data["_metadata"] = {
                "saved_at": datetime.now().isoformat(),
                "version": "1.0",
            }

            # Atomic write: write to temp file, then rename
            temp_path = self.storage_path / f"{self.MANIFEST_FILE}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(manifest_path)

            return True

        except Exception as e:
            print(f"Error saving manuscript: {e}")
            return False

    def load(self) -> Optional[Manuscript]:
        """Load manuscript from JSON file.

        Returns:
            Manuscript instance if successful, None otherwise
        """
        try:
            manifest_path = self.storage_path / self.MANIFEST_FILE

            if not manifest_path.exists():
                return None

            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Remove internal metadata before creating manuscript
            data.pop("_metadata", None)

            return Manuscript.from_dict(data)

        except Exception as e:
            print(f"Error loading manuscript: {e}")

            # Try to load from backup
            if self.backup_enabled:
                return self._load_from_backup()

            return None

    def exists(self) -> bool:
        """Check if manuscript file exists.

        Returns:
            True if manifest file exists
        """
        manifest_path = self.storage_path / self.MANIFEST_FILE
        return manifest_path.exists()

    def delete(self) -> bool:
        """Delete manuscript and all associated files.

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.storage_path.exists():
                shutil.rmtree(self.storage_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting manuscript: {e}")
            return False

    def export_scenes(self, manuscript: Manuscript) -> bool:
        """Export individual scenes to markdown files.

        Creates a scenes/ directory with one .md file per scene.

        Args:
            manuscript: Manuscript to export

        Returns:
            True if successful, False otherwise
        """
        try:
            scenes_dir = self.storage_path / self.SCENES_DIR
            scenes_dir.mkdir(parents=True, exist_ok=True)

            for act in manuscript.acts:
                for chapter in act.chapters:
                    for scene in chapter.scenes:
                        scene_file = scenes_dir / f"{scene.id}.md"

                        # Create markdown content
                        content = self._format_scene_markdown(
                            scene.title,
                            scene.content,
                            act.title,
                            chapter.title,
                            scene.notes,
                        )

                        scene_file.write_text(content, encoding="utf-8")

            return True

        except Exception as e:
            print(f"Error exporting scenes: {e}")
            return False

    def _create_backup(self, manifest_path: Path) -> None:
        """Create backup of manifest file.

        Args:
            manifest_path: Path to manifest file
        """
        backup_path = Path(str(manifest_path) + self.BACKUP_SUFFIX)
        shutil.copy2(manifest_path, backup_path)

    def _load_from_backup(self) -> Optional[Manuscript]:
        """Attempt to load from backup file.

        Returns:
            Manuscript instance if successful, None otherwise
        """
        try:
            backup_path = self.storage_path / (self.MANIFEST_FILE + self.BACKUP_SUFFIX)

            if not backup_path.exists():
                return None

            with open(backup_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.pop("_metadata", None)
            return Manuscript.from_dict(data)

        except Exception as e:
            print(f"Error loading from backup: {e}")
            return None

    def _format_scene_markdown(
        self,
        scene_title: str,
        content: str,
        act_title: str,
        chapter_title: str,
        notes: str,
    ) -> str:
        """Format scene as markdown.

        Args:
            scene_title: Scene title
            content: Scene content
            act_title: Act title
            chapter_title: Chapter title
            notes: Scene notes

        Returns:
            Formatted markdown string
        """
        lines = [
            f"# {scene_title}",
            "",
            f"**Act**: {act_title}",
            f"**Chapter**: {chapter_title}",
            "",
        ]

        if notes:
            lines.extend([
                "## Notes",
                "",
                notes,
                "",
            ])

        lines.extend([
            "## Content",
            "",
            content,
        ])

        return "\n".join(lines)

    @classmethod
    def create_new(cls, storage_path: Path, title: str, author: str = "") -> "ManuscriptStorage":
        """Create new manuscript storage with empty manuscript.

        Args:
            storage_path: Directory for storage
            title: Manuscript title
            author: Author name

        Returns:
            ManuscriptStorage instance with saved empty manuscript
        """
        storage = cls(storage_path)
        manuscript = Manuscript(title=title, author=author)
        storage.save(manuscript)
        return storage
