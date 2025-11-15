"""Plot Tracker - Track plot threads and detect plot holes.

Identifies:
- Main plot and subplots
- Setup, development, resolution
- Plot holes and loose threads
- Causal relationships
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class PlotThread:
    """Extracted plot thread.

    Attributes:
        thread_id: Unique identifier
        name: Thread name/description
        type: main_plot, subplot, romance, mystery, etc.
        status: setup, developing, resolved, abandoned
        first_mention: Chunk ID where thread starts
        mentions: List of chunk IDs where thread appears
        resolution: Description of resolution (if resolved)
        dependencies: Other threads this depends on
    """
    thread_id: str
    name: str
    type: str = "subplot"
    status: str = "developing"
    first_mention: str = ""
    mentions: List[str] = field(default_factory=list)
    resolution: str = ""
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class PlotTracker:
    """Track plot threads throughout manuscript."""

    def __init__(self, llm_provider=None):
        """Initialize plot tracker.

        Args:
            llm_provider: Optional LLM for intelligent extraction
        """
        self.llm = llm_provider
        self.threads: Dict[str, PlotThread] = {}
        self.thread_counter = 0

    async def extract(self, chunks: List[Any]) -> List[PlotThread]:
        """Extract and track plot threads.

        Args:
            chunks: List of ManuscriptChunk objects

        Returns:
            List of PlotThread objects
        """
        logger.info("Tracking plot threads")

        # Pass 1: Identify major plot threads
        await self._identify_threads(chunks)

        # Pass 2: Track thread development
        await self._track_development(chunks)

        # Pass 3: Detect plot holes
        await self._detect_plot_holes(chunks)

        return list(self.threads.values())

    async def _identify_threads(self, chunks: List[Any]):
        """Identify major plot threads.

        Args:
            chunks: Manuscript chunks
        """
        # Use early chunks to identify main threads
        early_chunks = chunks[:min(5, len(chunks))]

        if self.llm:
            threads = await self._identify_threads_llm(early_chunks)
            for thread_info in threads:
                thread = PlotThread(
                    thread_id=f"thread-{self.thread_counter}",
                    name=thread_info.get("name", "Unnamed Thread"),
                    type=thread_info.get("type", "subplot"),
                    first_mention=early_chunks[0].chunk_id if early_chunks else ""
                )
                self.threads[thread.thread_id] = thread
                self.thread_counter += 1
        else:
            # Heuristic: Create placeholder main plot thread
            thread = PlotThread(
                thread_id="thread-0",
                name="Main Plot",
                type="main_plot",
                first_mention=chunks[0].chunk_id if chunks else ""
            )
            self.threads[thread.thread_id] = thread
            self.thread_counter = 1

    async def _identify_threads_llm(self, chunks: List[Any]) -> List[Dict]:
        """Identify plot threads using LLM.

        Args:
            chunks: Early manuscript chunks

        Returns:
            List of thread descriptions
        """
        text = "\n\n".join(chunk.content[:1000] for chunk in chunks)[:3000]

        prompt = f"""Analyze this text and identify the main plot threads.
For each thread, provide:
- Name: Brief description
- Type: main_plot, subplot, romance, mystery, etc.

Return in format:
Name: [thread name]
Type: [thread type]

(separate each thread with a blank line)

Text:
{text}

Plot Threads:"""

        try:
            result = await self.llm.generate(prompt)
            threads = []

            # Parse result
            current_thread = {}
            for line in result.split('\n'):
                line = line.strip()
                if not line:
                    if current_thread:
                        threads.append(current_thread)
                        current_thread = {}
                    continue

                if line.startswith('Name:'):
                    current_thread['name'] = line.replace('Name:', '').strip()
                elif line.startswith('Type:'):
                    current_thread['type'] = line.replace('Type:', '').strip()

            if current_thread:
                threads.append(current_thread)

            return threads[:5]  # Limit to 5 main threads
        except Exception as e:
            logger.warning(f"Thread identification failed: {e}")
            return []

    async def _track_development(self, chunks: List[Any]):
        """Track how threads develop across manuscript.

        Args:
            chunks: Manuscript chunks
        """
        # For each thread, find where it's mentioned
        for thread_id, thread in self.threads.items():
            for chunk in chunks:
                # Simple keyword matching (could be enhanced with LLM)
                if self._thread_mentioned_in_chunk(thread, chunk):
                    thread.mentions.append(chunk.chunk_id)

    def _thread_mentioned_in_chunk(self, thread: PlotThread, chunk: Any) -> bool:
        """Check if thread is mentioned in chunk.

        Args:
            thread: Plot thread
            chunk: Manuscript chunk

        Returns:
            True if thread is mentioned
        """
        # Simple keyword check
        keywords = thread.name.lower().split()
        content_lower = chunk.content.lower()

        # Thread mentioned if any keyword appears
        return any(keyword in content_lower for keyword in keywords if len(keyword) > 3)

    async def _detect_plot_holes(self, chunks: List[Any]):
        """Detect potential plot holes.

        Args:
            chunks: Manuscript chunks
        """
        # Check each thread for resolution
        for thread_id, thread in self.threads.items():
            if not thread.mentions:
                thread.status = "abandoned"
                logger.warning(f"Thread '{thread.name}' appears to be abandoned")
            elif len(thread.mentions) == 1:
                thread.status = "setup"
                logger.info(f"Thread '{thread.name}' only has setup, no development")
            elif len(thread.mentions) < len(chunks) * 0.1:
                # Thread mentioned in less than 10% of scenes - might be forgotten
                thread.status = "developing"
                logger.warning(f"Thread '{thread.name}' has limited development")
            else:
                # Check if resolved in final chapters
                final_chunks = chunks[-min(5, len(chunks)):]
                final_chunk_ids = [c.chunk_id for c in final_chunks]

                if any(mention in final_chunk_ids for mention in thread.mentions):
                    thread.status = "resolved"
                    thread.resolution = "Thread appears in final chapters"
                else:
                    thread.status = "developing"
                    logger.warning(f"Thread '{thread.name}' may not be resolved")
