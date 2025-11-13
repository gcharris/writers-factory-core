"""Smart knowledge routing system.

Routes queries to appropriate knowledge systems:
- Cognee (local semantic graph)
- Gemini File Search (cloud semantic search)
- NotebookLM (external queries)
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of knowledge queries."""
    FACTUAL = "factual"  # Specific facts (use Cognee/Gemini)
    CONCEPTUAL = "conceptual"  # Concepts and relationships (use Cognee)
    ANALYTICAL = "analytical"  # Complex analysis (use NotebookLM)
    GENERAL = "general"  # General queries (use any)


class KnowledgeSource(Enum):
    """Available knowledge sources."""
    COGNEE = "cognee"
    GEMINI_FILE_SEARCH = "gemini_file_search"
    NOTEBOOKLM = "notebooklm"


@dataclass
class QueryResult:
    """Result from a knowledge query."""
    source: KnowledgeSource
    answer: str
    confidence: float
    references: List[str]
    metadata: Dict[str, Any]


class KnowledgeRouter:
    """Routes knowledge queries to appropriate system."""

    def __init__(
        self,
        prefer_local: bool = True,
        enable_caching: bool = True,
        fallback_chain: Optional[List[str]] = None
    ):
        """Initialize knowledge router.

        Args:
            prefer_local: Prefer local Cognee over cloud systems
            enable_caching: Enable query result caching
            fallback_chain: Ordered list of systems to try
        """
        self.prefer_local = prefer_local
        self.enable_caching = enable_caching
        self.fallback_chain = fallback_chain or [
            "cognee",
            "gemini_file_search",
            "notebooklm"
        ]

        # Initialize systems (mock for now)
        self._systems = {}
        logger.info("Initialized knowledge router")

    def classify_query(self, query: str) -> QueryType:
        """Classify query type.

        Args:
            query: Query text

        Returns:
            QueryType classification
        """
        query_lower = query.lower()

        # Simple keyword-based classification
        if any(word in query_lower for word in ["what is", "who is", "when", "where"]):
            return QueryType.FACTUAL

        if any(word in query_lower for word in ["relationship", "connect", "related"]):
            return QueryType.CONCEPTUAL

        if any(word in query_lower for word in ["analyze", "compare", "explain why"]):
            return QueryType.ANALYTICAL

        return QueryType.GENERAL

    def route_query(self, query: str) -> KnowledgeSource:
        """Determine which knowledge source to use.

        Args:
            query: Query text

        Returns:
            Recommended knowledge source
        """
        query_type = self.classify_query(query)

        if query_type == QueryType.FACTUAL:
            # Prefer local for facts
            return KnowledgeSource.COGNEE if self.prefer_local else KnowledgeSource.GEMINI_FILE_SEARCH

        elif query_type == QueryType.CONCEPTUAL:
            # Graph database is best for relationships
            return KnowledgeSource.COGNEE

        elif query_type == QueryType.ANALYTICAL:
            # NotebookLM is best for complex analysis
            return KnowledgeSource.NOTEBOOKLM

        else:
            # General query - use preferred source
            return KnowledgeSource.COGNEE if self.prefer_local else KnowledgeSource.GEMINI_FILE_SEARCH

    async def query(
        self,
        query: str,
        max_results: int = 5,
        force_source: Optional[str] = None
    ) -> QueryResult:
        """Execute a knowledge query.

        Args:
            query: Query text
            max_results: Maximum results to return
            force_source: Force specific source (bypass routing)

        Returns:
            QueryResult with answer and metadata
        """
        # Determine source
        if force_source:
            source = KnowledgeSource(force_source)
        else:
            source = self.route_query(query)

        logger.info(f"Routing query to {source.value}: {query[:50]}...")

        # Execute query (mock implementation)
        try:
            result = await self._execute_query(source, query, max_results)
            return result
        except Exception as e:
            logger.error(f"Query failed on {source.value}: {e}")
            # Try fallback chain
            return await self._fallback_query(query, max_results, source)

    async def _execute_query(
        self,
        source: KnowledgeSource,
        query: str,
        max_results: int
    ) -> QueryResult:
        """Execute query on specific source.

        Args:
            source: Knowledge source to query
            query: Query text
            max_results: Maximum results

        Returns:
            QueryResult
        """
        # Mock implementation - replace with actual integrations
        return QueryResult(
            source=source,
            answer=f"Mock answer from {source.value} for: {query}",
            confidence=0.8,
            references=["reference1.md", "reference2.md"],
            metadata={"source": source.value, "query": query}
        )

    async def _fallback_query(
        self,
        query: str,
        max_results: int,
        failed_source: KnowledgeSource
    ) -> QueryResult:
        """Try fallback sources if primary fails.

        Args:
            query: Query text
            max_results: Maximum results
            failed_source: Source that failed

        Returns:
            QueryResult from fallback source
        """
        for source_name in self.fallback_chain:
            source = KnowledgeSource(source_name)
            if source == failed_source:
                continue

            try:
                logger.info(f"Trying fallback source: {source.value}")
                result = await self._execute_query(source, query, max_results)
                return result
            except Exception as e:
                logger.warning(f"Fallback {source.value} also failed: {e}")
                continue

        # All sources failed
        raise Exception(f"All knowledge sources failed for query: {query}")
