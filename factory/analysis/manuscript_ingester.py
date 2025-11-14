"""Manuscript Ingestion & Parsing - Sprint 13 Task 13-01.

Accepts manuscripts in multiple formats:
- DOCX (Microsoft Word)
- PDF
- Markdown
- Plain text
- Existing Writers Factory projects

Parses into analyzable chunks (chapters, scenes, paragraphs).
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import json
import re
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class ManuscriptChunk:
    """A chunk of manuscript for analysis.

    Attributes:
        chunk_id: Unique identifier for this chunk
        chunk_type: Type of chunk ("chapter", "scene", "paragraph", "dialogue")
        content: The actual text content
        metadata: Additional metadata (word count, chapter/scene info)
        parent_id: ID of parent chunk (e.g., chapter for a scene)
        order: Sequential order in manuscript
    """
    chunk_id: str
    chunk_type: str
    content: str
    metadata: Dict[str, Any]
    parent_id: Optional[str] = None
    order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class ManuscriptIngester:
    """Ingest manuscripts from various formats.

    Supports:
    - DOCX (Microsoft Word)
    - PDF
    - Markdown
    - Plain text
    - Existing Writers Factory projects (scenes/ directory)
    """

    def __init__(self):
        """Initialize ingester with parsers for each format."""
        self.parsers = {
            '.docx': self._parse_docx,
            '.pdf': self._parse_pdf,
            '.md': self._parse_markdown,
            '.markdown': self._parse_markdown,
            '.txt': self._parse_text
        }

    async def ingest(
        self,
        source: Union[str, Path],
        source_type: str = "auto"
    ) -> Dict[str, Any]:
        """Ingest manuscript from file or project.

        Args:
            source: File path or project ID
            source_type: "file", "project", or "auto" (auto-detect)

        Returns:
            {
                "manuscript_id": str,
                "title": str,
                "word_count": int,
                "chunks": List[ManuscriptChunk],
                "metadata": {...}
            }
        """
        source_path = Path(source) if isinstance(source, str) else source

        # Auto-detect source type
        if source_type == "auto":
            if self._is_project(source_path):
                source_type = "project"
            else:
                source_type = "file"

        # Ingest based on type
        if source_type == "project":
            return await self._ingest_project(source_path)
        else:
            return await self._ingest_file(source_path)

    def _is_project(self, path: Path) -> bool:
        """Check if path is a Writers Factory project.

        Args:
            path: Path to check

        Returns:
            True if path contains manifest.json (Writers Factory project)
        """
        manifest_path = path / "manifest.json"
        return manifest_path.exists()

    async def _ingest_project(self, project_path: Path) -> Dict[str, Any]:
        """Ingest existing Writers Factory project.

        Args:
            project_path: Path to project directory

        Returns:
            Manuscript data with chunks
        """
        # Read manifest.json
        manifest_path = project_path / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"No manifest.json found at {project_path}")

        manifest = json.loads(manifest_path.read_text())

        chunks = []
        chunk_order = 0

        # Walk through acts and chapters
        for act in manifest.get("acts", []):
            for chapter in act.get("chapters", []):
                for scene in chapter.get("scenes", []):
                    # Load scene file
                    scene_path = project_path / scene.get("file_path", "")
                    if not scene_path.exists():
                        logger.warning(f"Scene file not found: {scene_path}")
                        continue

                    content = scene_path.read_text()

                    # Parse scene metadata from frontmatter if present
                    frontmatter_metadata = self._parse_frontmatter(content)

                    # Remove frontmatter from content
                    content = self._remove_frontmatter(content)

                    # Create chunk
                    chunk = ManuscriptChunk(
                        chunk_id=scene.get("id", f"scene-{chunk_order}"),
                        chunk_type="scene",
                        content=content,
                        metadata={
                            **frontmatter_metadata,
                            "act": act.get("title", ""),
                            "chapter": chapter.get("title", ""),
                            "scene_title": scene.get("title", ""),
                            "word_count": scene.get("word_count", len(content.split()))
                        },
                        parent_id=chapter.get("id", f"chapter-{chunk_order}"),
                        order=chunk_order
                    )
                    chunks.append(chunk)
                    chunk_order += 1

        total_word_count = sum(c.metadata.get("word_count", 0) for c in chunks)

        return {
            "manuscript_id": manifest.get("id", self._generate_id(manifest.get("title", "manuscript"))),
            "title": manifest.get("title", "Untitled Manuscript"),
            "word_count": total_word_count,
            "chunks": chunks,
            "metadata": {
                "source_type": "project",
                "source_path": str(project_path),
                "acts": len(manifest.get("acts", [])),
                "chapters": sum(len(a.get("chapters", [])) for a in manifest.get("acts", [])),
                "scenes": len(chunks),
                "author": manifest.get("author", "Unknown")
            }
        }

    async def _ingest_file(self, file_path: Path) -> Dict[str, Any]:
        """Ingest manuscript from file.

        Args:
            file_path: Path to manuscript file

        Returns:
            Manuscript data with chunks
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Select parser based on extension
        parser = self.parsers.get(file_path.suffix.lower(), self._parse_text)

        # Parse file
        raw_content = parser(file_path)

        # Split into chunks
        chunks = self._split_into_chunks(raw_content)

        # Generate manuscript ID
        manuscript_id = self._generate_id(file_path.stem)

        total_word_count = sum(len(c.content.split()) for c in chunks)

        return {
            "manuscript_id": manuscript_id,
            "title": file_path.stem,
            "word_count": total_word_count,
            "chunks": chunks,
            "metadata": {
                "source_type": "file",
                "source_path": str(file_path),
                "file_format": file_path.suffix,
                "chapters": len(set(c.metadata.get("chapter", "") for c in chunks)),
                "scenes": len(chunks)
            }
        }

    def _parse_docx(self, file_path: Path) -> str:
        """Parse DOCX file.

        Args:
            file_path: Path to DOCX file

        Returns:
            Extracted text content
        """
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError:
            logger.warning("python-docx not installed, using fallback parser")
            # Fallback: Try to read as text
            return self._parse_text(file_path)

    def _parse_pdf(self, file_path: Path) -> str:
        """Parse PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content
        """
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return "\n\n".join(
                    page.extract_text() for page in reader.pages
                    if page.extract_text()
                )
        except ImportError:
            logger.warning("PyPDF2 not installed, using fallback parser")
            return self._parse_text(file_path)

    def _parse_markdown(self, file_path: Path) -> str:
        """Parse Markdown file.

        Args:
            file_path: Path to Markdown file

        Returns:
            Raw markdown content (not rendered)
        """
        return file_path.read_text(encoding='utf-8')

    def _parse_text(self, file_path: Path) -> str:
        """Parse plain text file.

        Args:
            file_path: Path to text file

        Returns:
            Raw text content
        """
        return file_path.read_text(encoding='utf-8')

    def _split_into_chunks(self, content: str) -> List[ManuscriptChunk]:
        """Split content into analyzable chunks.

        Strategy:
        1. Detect chapter boundaries (# Chapter, "Chapter N", etc.)
        2. Split chapters into scenes (*** scene breaks, blank lines)
        3. Preserve paragraph structure

        Args:
            content: Raw manuscript content

        Returns:
            List of manuscript chunks
        """
        chunks = []

        # Split by chapter markers
        chapters = self._detect_chapters(content)

        for i, chapter in enumerate(chapters):
            # Split chapter into scenes
            scenes = self._detect_scenes(chapter["content"])

            for j, scene in enumerate(scenes):
                if not scene.strip():
                    continue

                chunk = ManuscriptChunk(
                    chunk_id=f"chunk-{i}-{j}",
                    chunk_type="scene",
                    content=scene.strip(),
                    metadata={
                        "chapter": chapter.get("title", f"Chapter {i+1}"),
                        "scene_number": j+1,
                        "word_count": len(scene.split())
                    },
                    parent_id=f"chapter-{i}",
                    order=len(chunks)
                )
                chunks.append(chunk)

        return chunks if chunks else [ManuscriptChunk(
            chunk_id="chunk-0-0",
            chunk_type="scene",
            content=content.strip(),
            metadata={"chapter": "Chapter 1", "scene_number": 1, "word_count": len(content.split())},
            order=0
        )]

    def _detect_chapters(self, content: str) -> List[Dict]:
        """Detect chapter boundaries.

        Looks for patterns like:
        - "# Chapter 1" (Markdown)
        - "Chapter One"
        - "CHAPTER 1"
        - etc.

        Args:
            content: Manuscript content

        Returns:
            List of chapter dictionaries with title and content
        """
        chapter_patterns = [
            r'^#\s+Chapter\s+\d+',
            r'^#\s+Chapter\s+(?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)',
            r'^Chapter\s+(?:\d+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)',
            r'^CHAPTER\s+\d+',
            r'^\*\*Chapter\s+\d+\*\*',
        ]

        lines = content.split('\n')
        chapter_starts = []

        for i, line in enumerate(lines):
            for pattern in chapter_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    chapter_starts.append((i, line.strip()))
                    break

        if not chapter_starts:
            # No chapter markers found, treat whole content as one chapter
            return [{"title": "Chapter 1", "content": content}]

        chapters = []
        for i, (line_num, title) in enumerate(chapter_starts):
            # Determine end of chapter
            if i + 1 < len(chapter_starts):
                end_line = chapter_starts[i + 1][0]
            else:
                end_line = len(lines)

            chapter_content = '\n'.join(lines[line_num + 1:end_line])
            chapters.append({
                "title": title,
                "content": chapter_content
            })

        return chapters

    def _detect_scenes(self, chapter_content: str) -> List[str]:
        """Detect scene boundaries within chapter.

        Looks for:
        - "***" or "* * *" (scene breaks)
        - Multiple blank lines (3+)
        - Section breaks

        Args:
            chapter_content: Content of chapter

        Returns:
            List of scene contents
        """
        # Try scene break markers first
        if "***" in chapter_content:
            scenes = [s.strip() for s in chapter_content.split("***") if s.strip()]
            return scenes

        if "* * *" in chapter_content:
            scenes = [s.strip() for s in chapter_content.split("* * *") if s.strip()]
            return scenes

        # Try splitting on multiple blank lines
        if "\n\n\n" in chapter_content:
            scenes = [s.strip() for s in chapter_content.split("\n\n\n") if s.strip()]
            if len(scenes) > 1:
                return scenes

        # No scene breaks found, return whole chapter as one scene
        return [chapter_content.strip()]

    def _parse_frontmatter(self, content: str) -> Dict:
        """Parse YAML frontmatter from scene file.

        Args:
            content: Scene content with potential frontmatter

        Returns:
            Parsed metadata dictionary
        """
        if not content.startswith("---"):
            return {}

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}

        try:
            import yaml
            return yaml.safe_load(parts[1]) or {}
        except ImportError:
            logger.warning("PyYAML not installed, cannot parse frontmatter")
            return {}
        except Exception as e:
            logger.warning(f"Failed to parse frontmatter: {e}")
            return {}

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content.

        Args:
            content: Content with potential frontmatter

        Returns:
            Content without frontmatter
        """
        if not content.startswith("---"):
            return content

        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()

        return content

    def _generate_id(self, base: str) -> str:
        """Generate unique manuscript ID.

        Args:
            base: Base name for ID

        Returns:
            Unique ID string
        """
        # Sanitize base name
        base = re.sub(r'[^a-z0-9-]', '-', base.lower())
        base = re.sub(r'-+', '-', base).strip('-')

        # Add short UUID
        short_id = str(uuid.uuid4())[:8]

        return f"{base}-{short_id}"
