#!/usr/bin/env python3
"""Import script for The Explants Volume 1 manuscript.

This script imports the existing Explants manuscript from markdown files
into the Writers Factory manuscript structure.

Usage:
    python3 scripts/import_explants.py [OPTIONS]

Options:
    --source PATH       Path to Volume 1 directory
    --output PATH       Output directory for manuscript
    --title TEXT        Manuscript title
    --author TEXT       Author name
    --dry-run          Show what would be imported without saving

Example:
    python3 scripts/import_explants.py \\
        --source "/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/The Explants Series/Volume 1/" \\
        --output "project/.manuscript/explants-v1" \\
        --author "Your Name"
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.tools import import_explants_volume_1
from factory.core.manuscript import ManuscriptStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Main import function."""
    parser = argparse.ArgumentParser(
        description="Import The Explants Volume 1 manuscript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to Volume 1 directory containing PART folders",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("project/.manuscript/explants-v1"),
        help="Output directory for manuscript (default: project/.manuscript/explants-v1)",
    )

    parser.add_argument(
        "--title",
        type=str,
        default="The Explants - Volume 1",
        help="Manuscript title",
    )

    parser.add_argument(
        "--author",
        type=str,
        default="",
        help="Author name",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without saving",
    )

    parser.add_argument(
        "--export-scenes",
        action="store_true",
        help="Also export individual scenes to markdown files",
    )

    args = parser.parse_args()

    # Validate source path
    if not args.source.exists():
        logger.error(f"Source directory does not exist: {args.source}")
        return 1

    if not args.source.is_dir():
        logger.error(f"Source path is not a directory: {args.source}")
        return 1

    # Import manuscript
    try:
        logger.info(f"Importing from: {args.source}")
        logger.info(f"Title: {args.title}")
        if args.author:
            logger.info(f"Author: {args.author}")

        manuscript = import_explants_volume_1(
            source_dir=args.source,
            title=args.title,
            author=args.author,
        )

        # Display summary
        summary = manuscript.structure_summary
        logger.info("=" * 60)
        logger.info("Import Summary:")
        logger.info(f"  Acts: {summary['acts']}")
        logger.info(f"  Chapters: {summary['chapters']}")
        logger.info(f"  Scenes: {summary['scenes']}")
        logger.info(f"  Total Words: {summary['words']:,}")
        logger.info("=" * 60)

        # Show detailed structure
        for act in manuscript.acts:
            logger.info(f"\n{act.title}:")
            for chapter in act.chapters:
                logger.info(f"  {chapter.title}: {len(chapter.scenes)} scenes")

        if args.dry_run:
            logger.info("\nDRY RUN - No files saved")
            return 0

        # Save manuscript
        logger.info(f"\nSaving to: {args.output}")
        storage = ManuscriptStorage(args.output)
        success = storage.save(manuscript)

        if not success:
            logger.error("Failed to save manuscript")
            return 1

        logger.info("✅ Manuscript saved successfully")

        # Export scenes if requested
        if args.export_scenes:
            logger.info("Exporting individual scenes...")
            success = storage.export_scenes(manuscript)

            if success:
                logger.info("✅ Scenes exported successfully")
            else:
                logger.warning("⚠️  Scene export failed")

        return 0

    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
