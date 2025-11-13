"""Agent integration helpers for webapp backend.

Provides helper functions to bridge FastAPI backend with
Writers Factory agent implementations.
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

from factory.agents.base_agent import BaseAgent
from factory.core.config.loader import (
    load_agent_config,
    get_enabled_agents,
    get_api_key,
)
from factory.tools.model_comparison import ModelComparisonTool
from factory.knowledge.router import KnowledgeRouter
from factory.workflows.scene_operations import (
    SceneGenerationWorkflow,
    SceneEnhancementWorkflow,
)

logger = logging.getLogger(__name__)


class WebAppAgentBridge:
    """Bridge between webapp and Factory agents.

    Handles agent initialization, execution, and result formatting.
    """

    def __init__(self, project_path: Path):
        """Initialize agent bridge.

        Args:
            project_path: Path to current project
        """
        self.project_path = project_path
        self.config = load_agent_config()
        self.enabled_agents = get_enabled_agents()

        # Initialize tools
        self.comparison_tool = None
        self.knowledge_router = None

        # Cache for agent instances
        self._agent_cache: Dict[str, BaseAgent] = {}

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get or create agent instance.

        Args:
            agent_name: Agent identifier

        Returns:
            Agent instance or None if not available
        """
        # Check cache first
        if agent_name in self._agent_cache:
            return self._agent_cache[agent_name]

        # Check if agent is enabled
        if agent_name not in self.enabled_agents:
            logger.warning(f"Agent not enabled: {agent_name}")
            return None

        try:
            agent_config = self.enabled_agents[agent_name]
            provider = agent_config.get("provider")
            api_key = get_api_key(provider)

            if not api_key:
                logger.warning(f"No API key for provider: {provider}")
                return None

            # Create agent instance
            agent = BaseAgent(
                name=agent_name,
                config=agent_config,
                api_key=api_key,
            )

            # Cache it
            self._agent_cache[agent_name] = agent

            return agent

        except Exception as e:
            logger.error(f"Error creating agent {agent_name}: {e}")
            return None

    async def compare_models(
        self,
        prompt: str,
        models: List[str],
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run model comparison.

        Args:
            prompt: Writing prompt
            models: List of model identifiers (2-4)
            context: Optional context for generation

        Returns:
            Dictionary with comparison results
        """
        try:
            # Initialize comparison tool if needed
            if self.comparison_tool is None:
                self.comparison_tool = ModelComparisonTool()

            # Run comparison
            result = await self.comparison_tool.compare_models(
                prompt=prompt,
                models=models,
                context=context,
            )

            # Format results for webapp
            return {
                "success": True,
                "results": result.outputs,
                "diffs": result.diffs,
                "metadata": {
                    "prompt": result.prompt,
                    "model_count": len(result.outputs),
                },
            }

        except Exception as e:
            logger.error(f"Model comparison error: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": {},
            }

    async def generate_scene(
        self,
        prompt: str,
        model: str,
        context: Optional[str] = None,
        story_bible: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a scene using specified model.

        Args:
            prompt: Scene description/requirements
            model: Model identifier
            context: Optional context about the story
            story_bible: Optional story bible data

        Returns:
            Dictionary with generated scene
        """
        try:
            agent = self.get_agent(model)

            if not agent:
                return {
                    "success": False,
                    "error": f"Agent not available: {model}",
                }

            # Create workflow
            workflow = SceneGenerationWorkflow(
                agent=agent,
                project_path=self.project_path,
            )

            # Build full prompt
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nScene: {prompt}"

            # Execute workflow
            result = await workflow.execute({
                "prompt": full_prompt,
                "story_bible": story_bible,
            })

            return {
                "success": True,
                "scene": result.get("scene_text", ""),
                "metadata": {
                    "model": model,
                    "word_count": len(result.get("scene_text", "").split()),
                    "cost": result.get("cost", 0.0),
                },
            }

        except Exception as e:
            logger.error(f"Scene generation error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def enhance_scene(
        self,
        scene_text: str,
        focus: str,
        model: str,
        voice_sample: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enhance an existing scene.

        Args:
            scene_text: Original scene content
            focus: Enhancement focus (dialogue, description, pacing, etc.)
            model: Model identifier
            voice_sample: Optional voice reference text

        Returns:
            Dictionary with enhanced scene
        """
        try:
            agent = self.get_agent(model)

            if not agent:
                return {
                    "success": False,
                    "error": f"Agent not available: {model}",
                }

            # Create workflow
            workflow = SceneEnhancementWorkflow(
                agent=agent,
                project_path=self.project_path,
            )

            # Execute workflow
            result = await workflow.execute({
                "scene_text": scene_text,
                "focus": focus,
                "voice_sample": voice_sample,
            })

            return {
                "success": True,
                "enhanced_scene": result.get("enhanced_text", ""),
                "changes": result.get("changes", []),
                "metadata": {
                    "model": model,
                    "focus": focus,
                    "cost": result.get("cost", 0.0),
                },
            }

        except Exception as e:
            logger.error(f"Scene enhancement error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def query_knowledge(
        self,
        question: str,
        notebook_id: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Query knowledge base.

        Args:
            question: User's question
            notebook_id: Optional NotebookLM notebook ID
            source: Optional source preference (cognee/notebooklm)

        Returns:
            Dictionary with answer and references
        """
        try:
            # Initialize knowledge router if needed
            if self.knowledge_router is None:
                self.knowledge_router = KnowledgeRouter()

            # Query
            result = await self.knowledge_router.query(
                query=question,
                notebook_id=notebook_id,
                max_results=5,
            )

            return {
                "success": True,
                "answer": result.answer,
                "source": result.source.value,
                "confidence": result.confidence,
                "references": result.references,
            }

        except Exception as e:
            logger.error(f"Knowledge query error: {e}")
            return {
                "success": False,
                "error": str(e),
                "answer": "Error processing query",
            }


# Global bridge instance (initialized by app)
_bridge: Optional[WebAppAgentBridge] = None


def get_bridge(project_path: Path) -> WebAppAgentBridge:
    """Get or create agent bridge instance.

    Args:
        project_path: Path to current project

    Returns:
        WebAppAgentBridge instance
    """
    global _bridge

    if _bridge is None:
        _bridge = WebAppAgentBridge(project_path)

    return _bridge
