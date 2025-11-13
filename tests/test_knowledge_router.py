"""Tests for knowledge router."""

import pytest
from factory.knowledge.router import KnowledgeRouter, QueryType, KnowledgeSource


def test_knowledge_router_creation():
    """Test knowledge router creation."""
    router = KnowledgeRouter(prefer_local=True)

    assert router.prefer_local is True
    assert router.enable_caching is True


def test_query_classification():
    """Test query type classification."""
    router = KnowledgeRouter()

    # Factual queries
    assert router.classify_query("What is Mickey's age?") == QueryType.FACTUAL
    assert router.classify_query("Who is the protagonist?") == QueryType.FACTUAL

    # Conceptual queries
    assert router.classify_query("How are Mickey and Noni related?") == QueryType.CONCEPTUAL
    assert router.classify_query("What's the connection between X and Y?") == QueryType.CONCEPTUAL

    # Analytical queries
    assert router.classify_query("Why does the character do this?") == QueryType.ANALYTICAL
    assert router.classify_query("Analyze the themes") == QueryType.ANALYTICAL


def test_query_routing():
    """Test query routing logic."""
    router = KnowledgeRouter(prefer_local=True)

    # Factual queries should prefer Cognee if local
    source = router.route_query("What is X?")
    assert source == KnowledgeSource.COGNEE

    # Conceptual queries should use Cognee (graph database)
    source = router.route_query("How are X and Y related?")
    assert source == KnowledgeSource.COGNEE

    # Analytical queries should use NotebookLM
    source = router.route_query("Analyze why X happens")
    assert source == KnowledgeSource.NOTEBOOKLM


@pytest.mark.asyncio
async def test_query_execution():
    """Test query execution."""
    router = KnowledgeRouter()

    result = await router.query("Test query", max_results=5)

    assert result.source in [
        KnowledgeSource.COGNEE,
        KnowledgeSource.GEMINI_FILE_SEARCH,
        KnowledgeSource.NOTEBOOKLM
    ]
    assert result.answer is not None
    assert isinstance(result.confidence, float)
    assert isinstance(result.references, list)


@pytest.mark.asyncio
async def test_forced_source():
    """Test forcing a specific knowledge source."""
    router = KnowledgeRouter()

    result = await router.query("Test query", force_source="cognee")

    assert result.source == KnowledgeSource.COGNEE
