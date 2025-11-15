#!/usr/bin/env python3
"""Migration script: Convert JSON-embedded storage to file-based storage.

Sprint 9: File-Based Editing Migration
==========================================

This script migrates existing Writers Factory manuscripts from the old
JSON-embedded format (where scene content is stored in manuscript.json)
to the new file-based format (individual .md files per scene).

WHAT IT DOES:
1. Loads existing manuscript.json (with embedded content)
2. Extracts each scene's content
3. Creates individual .md files organized by act/chapter
4. Saves new manifest.json WITHOUT content (just structure + metadata)
5. Creates backup of original manuscript.json

USAGE:
    python factory/scripts/migrate_to_file_based.py [manuscript_path]

    # Example:
    python factory/scripts/migrate_to_file_based.py webapp/.manuscript/explants-v1

SAFETY:
- Creates .backup file before making changes
- Non-destructive: can be rolled back
- Validates before overwriting

Author: Writers Factory Team
Date: November 2025
Sprint: 9 - File-Based Editing
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import factory modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from factory.core.manuscript.structure import Manuscript
from factory.core.manuscript.storage import ManuscriptStorage


def migrate_manuscript(manuscript_path: Path, dry_run: bool = False) -> bool:
    """Migrate a manuscript from JSON-embedded to file-based storage.

    Args:
        manuscript_path: Path to manuscript directory
        dry_run: If True, only show what would be done

    Returns:
        True if migration successful, False otherwise
    """
    manuscript_path = Path(manuscript_path)

    print(f"{'=' * 60}")
    print(f"Sprint 9: File-Based Storage Migration")
    print(f"{'=' * 60}")
    print(f"Manuscript: {manuscript_path}")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE MIGRATION'}")
    print()

    # Check if manuscript exists
    manifest_file = manuscript_path / "manuscript.json"
    if not manifest_file.exists():
        print(f"❌ Error: manuscript.json not found at {manuscript_path}")
        return False

    try:
        # Load existing manuscript
        print("📖 Loading existing manuscript...")
        with open(manifest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check storage version
        metadata = data.get("_metadata", {})
        storage_type = metadata.get("storage_type", "embedded")

        if storage_type == "file_based":
            print("✅ Already using file-based storage. No migration needed.")
            return True

        print(f"   Storage type: {storage_type}")
        print(f"   Version: {metadata.get('version', '1.0')}")

        # Parse manuscript
        data_copy = data.copy()
        data_copy.pop("_metadata", None)
        manuscript = Manuscript.from_dict(data_copy)

        # Count scenes
        total_scenes = 0
        total_words = 0
        for act in manuscript.acts:
            for chapter in act.chapters:
                total_scenes += len(chapter.scenes)
                for scene in chapter.scenes:
                    total_words += scene.word_count

        print(f"   Title: {manuscript.title}")
        print(f"   Author: {manuscript.author}")
        print(f"   Acts: {len(manuscript.acts)}")
        print(f"   Scenes: {total_scenes}")
        print(f"   Words: {total_words:,}")
        print()

        if dry_run:
            print("🔍 DRY RUN - Would create these files:")
            print()

            scenes_dir = manuscript_path / "scenes"
            for act in manuscript.acts:
                act_dir_name = ManuscriptStorage(manuscript_path)._sanitize_dirname(act.id)
                for chapter in act.chapters:
                    chapter_dir_name = ManuscriptStorage(manuscript_path)._sanitize_dirname(chapter.id)
                    for scene in chapter.scenes:
                        file_path = scenes_dir / act_dir_name / chapter_dir_name / f"{scene.id}.md"
                        print(f"   📄 {file_path.relative_to(manuscript_path)}")
                        print(f"      Title: {scene.title}")
                        print(f"      Words: {scene.word_count}")
                        print()

            print(f"✨ Would save manifest.json (structure only, no content)")
            print(f"✨ Would create backup: manuscript.json.backup")
            print()
            print("To execute migration, run without --dry-run flag")
            return True

        # Real migration
        print("🚀 Starting migration...")
        print()

        # Create backup
        backup_path = manifest_file.with_suffix('.json.backup')
        print(f"💾 Creating backup: {backup_path.name}")
        import shutil
        shutil.copy2(manifest_file, backup_path)
        print(f"   ✓ Backup created")
        print()

        # Create new file-based storage
        print("📝 Creating file-based storage...")
        storage = ManuscriptStorage(manuscript_path, backup_enabled=True)

        # Save with file-based storage
        success = storage.save(manuscript)

        if not success:
            print("❌ Migration failed during save")
            return False

        print(f"   ✓ Created {total_scenes} scene files")
        print(f"   ✓ Saved manifest.json (structure only)")
        print()

        # Verify migration
        print("🔍 Verifying migration...")
        loaded_manuscript = storage.load()

        if not loaded_manuscript:
            print("❌ Verification failed: Could not load migrated manuscript")
            return False

        # Check scene count
        loaded_scenes = 0
        loaded_words = 0
        for act in loaded_manuscript.acts:
            for chapter in act.chapters:
                loaded_scenes += len(chapter.scenes)
                for scene in chapter.scenes:
                    loaded_words += scene.word_count

        print(f"   Scenes: {loaded_scenes}/{total_scenes}")
        print(f"   Words: {loaded_words:,}/{total_words:,}")

        if loaded_scenes != total_scenes or loaded_words != total_words:
            print("⚠️  Warning: Scene or word count mismatch")
            print("   Migration may be incomplete")
            return False

        print(f"   ✓ All scenes loaded correctly")
        print()

        # Success
        print("=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print()
        print("WHAT CHANGED:")
        print(f"✓ {total_scenes} scenes converted to individual .md files")
        print(f"✓ manifest.json now contains structure only (no content)")
        print(f"✓ Original manuscript backed up to: {backup_path.name}")
        print()
        print("NEXT STEPS:")
        print("• Scenes can now be edited in any text editor (VS Code, Cursor AI, etc.)")
        print("• Scene files are located in: scenes/ACT_*/CHAPTER_*/")
        print("• Writers Factory will automatically use file-based storage")
        print()

        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for migration script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate Writers Factory manuscript to file-based storage"
    )
    parser.add_argument(
        "manuscript_path",
        type=str,
        help="Path to manuscript directory (e.g., webapp/.manuscript/explants-v1)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    manuscript_path = Path(args.manuscript_path)

    if not manuscript_path.exists():
        print(f"❌ Error: Path does not exist: {manuscript_path}")
        sys.exit(1)

    success = migrate_manuscript(manuscript_path, dry_run=args.dry_run)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
