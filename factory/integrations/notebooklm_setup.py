"""NotebookLM Setup Integration - Extract project knowledge during setup.

Integrates with NotebookLM to extract:
- Character profiles and relationships
- Story world and settings
- Plot threads and themes
- Voice characteristics
- Key metaphors and motifs
"""

from typing import List, Optional
import logging

from factory.research.notebooklm_client import NotebookLMClient, AuthenticationError, QueryTimeoutError

logger = logging.getLogger(__name__)


class NotebookLMSetupIntegration:
    """
    Integrates NotebookLM knowledge extraction into project setup.

    Uses the NotebookLM client to query user notebooks with predefined
    questions, consolidating the knowledge into a context string for
    skill generation.
    """

    def __init__(self):
        """Initialize NotebookLM setup integration."""
        self.nlm_client = NotebookLMClient()

    async def extract_project_knowledge(
        self,
        notebooklm_urls: List[str],
        timeout: int = 30
    ) -> str:
        """
        Extract relevant knowledge from NotebookLM notebooks.

        Queries each notebook with predefined questions about:
        - Characters, traits, relationships, arcs
        - Story world, settings, locations
        - Plot threads and themes
        - Voice and writing style
        - Metaphors, symbols, motifs

        Args:
            notebooklm_urls: List of NotebookLM notebook URLs
            timeout: Timeout in seconds for each query

        Returns:
            Consolidated knowledge context string (markdown formatted)

        Raises:
            AuthenticationError: If not authenticated with NotebookLM
            QueryTimeoutError: If queries take too long
        """

        if not notebooklm_urls:
            logger.info("No NotebookLM URLs provided, skipping knowledge extraction")
            return ""

        # Predefined queries to extract knowledge
        queries = [
            "Summarize the main characters, their traits, relationships, and arcs.",
            "Describe the story world, settings, and key locations.",
            "What are the main plot threads and themes?",
            "What voice or writing style characteristics are evident?",
            "What are the key metaphors, symbols, or recurring motifs?"
        ]

        knowledge_sections = []

        logger.info(f"Extracting knowledge from {len(notebooklm_urls)} notebook(s)")

        for i, url in enumerate(notebooklm_urls):
            logger.info(f"Querying notebook {i+1}/{len(notebooklm_urls)}: {url}")

            notebook_knowledge = []

            for j, query in enumerate(queries):
                try:
                    logger.info(f"  Query {j+1}/{len(queries)}: {query[:50]}...")

                    response = await self.nlm_client.query(
                        question=query,
                        notebook_url=url,
                        timeout=timeout
                    )

                    # Format as markdown section
                    section = f"### {query}\n\n{response['answer']}\n"

                    # Add sources if available
                    if response.get('sources'):
                        section += "\n**Sources:**\n"
                        for source in response['sources'][:3]:  # Limit to 3 sources
                            title = source.get('title', 'Unknown')
                            excerpt = source.get('excerpt', '')[:200]  # Truncate
                            section += f"- {title}: _{excerpt}_\n"
                        section += "\n"

                    notebook_knowledge.append(section)

                except QueryTimeoutError as e:
                    logger.warning(f"Query timed out: {e}")
                    notebook_knowledge.append(f"### {query}\n\n_Query timed out_\n\n")
                except Exception as e:
                    logger.error(f"Query failed: {e}")
                    notebook_knowledge.append(f"### {query}\n\n_Query failed: {str(e)}_\n\n")

            # Add notebook section
            notebook_name = f"Notebook {i+1}"
            knowledge_sections.append(
                f"## {notebook_name}\n\n" + "\n".join(notebook_knowledge)
            )

        # Consolidate all knowledge
        consolidated = "# Project Knowledge from NotebookLM\n\n"
        consolidated += "\n---\n\n".join(knowledge_sections)

        logger.info(f"Knowledge extraction complete. Total length: {len(consolidated)} chars")

        return consolidated

    async def extract_voice_context(
        self,
        notebooklm_urls: List[str],
        timeout: int = 30
    ) -> str:
        """
        Extract ONLY voice-related context from NotebookLM.

        This is a focused extraction for voice profile generation,
        asking specifically about writing style and voice.

        Args:
            notebooklm_urls: List of NotebookLM notebook URLs
            timeout: Timeout in seconds for each query

        Returns:
            Voice context string

        Raises:
            AuthenticationError: If not authenticated with NotebookLM
        """

        if not notebooklm_urls:
            return ""

        voice_queries = [
            "Describe the narrative voice and writing style in detail. How would you characterize the sentence structure, vocabulary, and tone?",
            "What are the distinctive characteristics of the prose? Consider metaphor use, POV depth, and any unique stylistic patterns.",
            "Are there any writing patterns or anti-patterns explicitly mentioned or demonstrated? What should be avoided?"
        ]

        voice_sections = []

        logger.info(f"Extracting voice context from {len(notebooklm_urls)} notebook(s)")

        for url in notebooklm_urls:
            for query in voice_queries:
                try:
                    response = await self.nlm_client.query(
                        question=query,
                        notebook_url=url,
                        timeout=timeout
                    )

                    voice_sections.append(f"**{query}**\n\n{response['answer']}\n")

                except Exception as e:
                    logger.warning(f"Voice query failed: {e}")
                    continue

        if not voice_sections:
            return ""

        return "# Voice Context from NotebookLM\n\n" + "\n\n".join(voice_sections)

    async def extract_character_context(
        self,
        notebooklm_urls: List[str],
        timeout: int = 30
    ) -> str:
        """
        Extract ONLY character-related context from NotebookLM.

        Focused extraction for character knowledge.

        Args:
            notebooklm_urls: List of NotebookLM notebook URLs
            timeout: Timeout in seconds for each query

        Returns:
            Character context string

        Raises:
            AuthenticationError: If not authenticated with NotebookLM
        """

        if not notebooklm_urls:
            return ""

        character_queries = [
            "List all main characters with their core traits, motivations, and key relationships.",
            "What are the character arcs? How do characters change throughout the story?",
            "Describe the voice and speaking patterns of each major character."
        ]

        character_sections = []

        logger.info(f"Extracting character context from {len(notebooklm_urls)} notebook(s)")

        for url in notebooklm_urls:
            for query in character_queries:
                try:
                    response = await self.nlm_client.query(
                        question=query,
                        notebook_url=url,
                        timeout=timeout
                    )

                    character_sections.append(f"**{query}**\n\n{response['answer']}\n")

                except Exception as e:
                    logger.warning(f"Character query failed: {e}")
                    continue

        if not character_sections:
            return ""

        return "# Character Context from NotebookLM\n\n" + "\n\n".join(character_sections)

    async def extract_world_context(
        self,
        notebooklm_urls: List[str],
        timeout: int = 30
    ) -> str:
        """
        Extract ONLY world/setting context from NotebookLM.

        Focused extraction for world building knowledge.

        Args:
            notebooklm_urls: List of NotebookLM notebook URLs
            timeout: Timeout in seconds for each query

        Returns:
            World context string

        Raises:
            AuthenticationError: If not authenticated with NotebookLM
        """

        if not notebooklm_urls:
            return ""

        world_queries = [
            "Describe the story world, including key locations, settings, and the overall environment.",
            "What are the rules, systems, or unique aspects of this world?",
            "What historical events or world details are important to the story?"
        ]

        world_sections = []

        logger.info(f"Extracting world context from {len(notebooklm_urls)} notebook(s)")

        for url in notebooklm_urls:
            for query in world_queries:
                try:
                    response = await self.nlm_client.query(
                        question=query,
                        notebook_url=url,
                        timeout=timeout
                    )

                    world_sections.append(f"**{query}**\n\n{response['answer']}\n")

                except Exception as e:
                    logger.warning(f"World query failed: {e}")
                    continue

        if not world_sections:
            return ""

        return "# World Context from NotebookLM\n\n" + "\n\n".join(world_sections)

    async def is_authenticated(self) -> bool:
        """
        Check if user is authenticated with NotebookLM.

        Returns:
            True if authenticated, False otherwise
        """
        return await self.nlm_client._is_authenticated()

    async def authenticate(self) -> bool:
        """
        Authenticate with NotebookLM (opens browser for login).

        Returns:
            True if authentication successful

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info("Starting NotebookLM authentication...")
        result = await self.nlm_client.authenticate()
        logger.info("NotebookLM authentication complete")
        return result
