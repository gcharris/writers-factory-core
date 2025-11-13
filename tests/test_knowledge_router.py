"""Tests for knowledge router."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from factory.knowledge.router import (
    KnowledgeRouter,
    KnowledgeSource,
    QueryType,
    QueryResult
)


class TestQueryClassification:
    """Test query type classification."""

    def test_classify_factual_query(self):
        """Test classifying factual queries."""
        router = KnowledgeRouter()

        assert router.classify_query("What is Sarah's age?") == QueryType.FACTUAL
        assert router.classify_query("Who is the protagonist?") == QueryType.FACTUAL
        assert router.classify_query("When does the story take place?") == QueryType.FACTUAL
        assert router.classify_query("Where is the setting?") == QueryType.FACTUAL

    def test_classify_analytical_query(self):
        """Test classifying analytical queries."""
        router = KnowledgeRouter()

        assert router.classify_query("Why does Sarah betray John?") == QueryType.ANALYTICAL
        assert router.classify_query("Analyze the theme of redemption") == QueryType.ANALYTICAL
        assert router.classify_query("Compare character arcs") == QueryType.ANALYTICAL

    def test_classify_conceptual_query(self):
        """Test classifying conceptual queries."""
        router = KnowledgeRouter()

        assert router.classify_query("Show me the relationship between characters") == QueryType.CONCEPTUAL
        assert router.classify_query("How are themes connected?") == QueryType.CONCEPTUAL
        assert router.classify_query("Find related plot points") == QueryType.CONCEPTUAL

    def test_classify_general_query(self):
        """Test classifying general queries."""
        router = KnowledgeRouter()

        assert router.classify_query("Tell me about the story") == QueryType.GENERAL
        assert router.classify_query("Summary please") == QueryType.GENERAL


class TestRouting:
    """Test query routing logic."""

    def test_route_to_cognee_by_default(self):
        """Test that most queries route to Cognee."""
        router = KnowledgeRouter(notebooklm_enabled=False)

        assert router.route_query("What is Sarah's age?") == KnowledgeSource.COGNEE
        assert router.route_query("How do characters relate?") == KnowledgeSource.COGNEE
        assert router.route_query("Tell me about the story") == KnowledgeSource.COGNEE

    def test_route_analytical_to_notebooklm_when_enabled(self):
        """Test analytical queries route to NotebookLM when enabled."""
        router = KnowledgeRouter(
            notebooklm_enabled=True,
            notebooklm_notebook_id="test-notebook-123"
        )

        assert router.route_query("Why does Sarah betray John?") == KnowledgeSource.NOTEBOOKLM
        assert router.route_query("Analyze the themes") == KnowledgeSource.NOTEBOOKLM

    def test_route_analytical_to_cognee_when_notebooklm_disabled(self):
        """Test analytical queries route to Cognee when NotebookLM disabled."""
        router = KnowledgeRouter(notebooklm_enabled=False)

        assert router.route_query("Why does Sarah betray John?") == KnowledgeSource.COGNEE
        assert router.route_query("Analyze the themes") == KnowledgeSource.COGNEE


class TestQueryExecution:
    """Test query execution."""

    @pytest.mark.asyncio
    async def test_query_cognee(self):
        """Test querying Cognee."""
        router = KnowledgeRouter()

        result = await router.query("What is the main theme?")

        assert result.source == KnowledgeSource.COGNEE
        assert result.answer is not None
        assert result.confidence > 0
        assert len(result.references) > 0

    @pytest.mark.asyncio
    async def test_query_notebooklm_when_enabled(self):
        """Test querying NotebookLM when enabled."""
        router = KnowledgeRouter(
            notebooklm_enabled=True,
            notebooklm_notebook_id="test-123"
        )

        result = await router.query("Why is the protagonist conflicted?")

        assert result.source == KnowledgeSource.NOTEBOOKLM
        assert result.answer is not None
        assert result.confidence > 0

    @pytest.mark.asyncio
    async def test_query_notebooklm_when_disabled_falls_back(self):
        """Test querying NotebookLM when disabled falls back to Cognee."""
        router = KnowledgeRouter(notebooklm_enabled=False)

        # Force NotebookLM query even though disabled - should fall back to Cognee
        result = await router.query("Analyze the story", force_source="notebooklm")

        # Should have fallen back to Cognee
        assert result.source == KnowledgeSource.COGNEE


class TestHidingImplementationDetails:
    """Test that implementation details are hidden from users."""

    def test_gemini_not_in_knowledge_sources(self):
        """Test that Gemini File Search is not a user-facing option."""
        # KnowledgeSource should only have COGNEE and NOTEBOOKLM
        sources = [s.value for s in KnowledgeSource]

        assert "cognee" in sources
        assert "notebooklm" in sources
        assert "gemini_file_search" not in sources  # Hidden from users!


class TestNotebookLMOptIn:
    """Test NotebookLM opt-in behavior."""

    def test_notebooklm_disabled_by_default(self):
        """Test NotebookLM is disabled by default."""
        router = KnowledgeRouter()

        assert router.notebooklm_enabled is False
        assert router.notebooklm_notebook_id is None

    def test_notebooklm_enabled_with_notebook_id(self):
        """Test NotebookLM can be enabled with notebook ID."""
        router = KnowledgeRouter(
            notebooklm_enabled=True,
            notebooklm_notebook_id="my-notebook-123"
        )

        assert router.notebooklm_enabled is True
        assert router.notebooklm_notebook_id == "my-notebook-123"

    @pytest.mark.asyncio
    async def test_analytical_query_uses_cognee_when_notebooklm_disabled(self):
        """Test analytical queries use Cognee when NotebookLM disabled."""
        router = KnowledgeRouter(notebooklm_enabled=False)

        result = await router.query("Why does this happen?")

        # Should fall back to Cognee
        assert result.source == KnowledgeSource.COGNEE

    @pytest.mark.asyncio
    async def test_analytical_query_uses_notebooklm_when_enabled(self):
        """Test analytical queries use NotebookLM when enabled."""
        router = KnowledgeRouter(
            notebooklm_enabled=True,
            notebooklm_notebook_id="test-123"
        )

        result = await router.query("Why does this happen?")

        assert result.source == KnowledgeSource.NOTEBOOKLM
