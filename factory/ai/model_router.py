"""
Model Router - Route operations to appropriate AI models

Default: Llama 3.3 (local via Ollama) - FREE
Optional: Claude, GPT, Gemini (user-configured)

Task-specific routing ensures cost-effective usage.
"""

import json
import os
from typing import Optional, Dict, Any
from pathlib import Path


class ModelRouter:
    """Route operations to appropriate models based on task and configuration."""

    # Default model assignments for different task types
    TASK_DEFAULTS = {
        "setup_wizard": "llama3.3",           # Free local for wizard
        "knowledge_extraction": "llama3.3",    # Free local for extraction
        "knowledge_query": "llama3.3",         # Free local for queries
        "scene_writing": "claude-sonnet-4.5",  # Premium for creative work
        "scene_analysis": "llama3.3",          # Free local for analysis
        "voice_analysis": "claude-sonnet-4.5", # Premium for nuance
        "character_extraction": "llama3.3",    # Free local for extraction
        "plot_extraction": "llama3.3",         # Free local for extraction
    }

    # Model capabilities and costs
    MODEL_INFO = {
        "llama3.3": {
            "provider": "ollama",
            "cost_per_1k_tokens": 0.0,  # Free local
            "quality": "good",
            "speed": "fast",
            "requires_ollama": True,
        },
        "claude-sonnet-4.5": {
            "provider": "anthropic",
            "cost_per_1k_tokens": 0.015,  # $15 per 1M tokens
            "quality": "excellent",
            "speed": "medium",
            "requires_api_key": True,
        },
        "gpt-4o": {
            "provider": "openai",
            "cost_per_1k_tokens": 0.030,  # $30 per 1M tokens
            "quality": "excellent",
            "speed": "medium",
            "requires_api_key": True,
        },
        "gemini-2.0-flash": {
            "provider": "google",
            "cost_per_1k_tokens": 0.00075,  # $0.75 per 1M tokens
            "quality": "very-good",
            "speed": "very-fast",
            "requires_api_key": True,
        },
    }

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize Model Router.

        Args:
            project_id: Optional project ID to load project-specific config
        """
        self.project_id = project_id
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load project configuration or return defaults."""
        if not self.project_id:
            return {"models": {}, "fallback_model": "llama3.3"}

        config_path = Path(f"projects/{self.project_id}/config.json")

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config
            except Exception as e:
                print(f"Warning: Could not load project config: {e}")

        return {"models": {}, "fallback_model": "llama3.3"}

    def get_model_for_task(self, task_type: str) -> str:
        """
        Get the appropriate model for a given task.

        Args:
            task_type: Type of task (e.g., "setup_wizard", "scene_writing")

        Returns:
            Model identifier string (e.g., "llama3.3", "claude-sonnet-4.5")
        """
        # Check if user has configured a specific model for this task
        if "models" in self.config and task_type in self.config["models"]:
            return self.config["models"][task_type]

        # Use task default
        if task_type in self.TASK_DEFAULTS:
            return self.TASK_DEFAULTS[task_type]

        # Fallback to configured fallback or default
        return self.config.get("fallback_model", "llama3.3")

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.

        Args:
            model: Model identifier

        Returns:
            Dictionary with model info (provider, cost, quality, etc.)
        """
        return self.MODEL_INFO.get(model, {
            "provider": "unknown",
            "cost_per_1k_tokens": 0.0,
            "quality": "unknown",
            "speed": "unknown",
        })

    def is_model_available(self, model: str) -> bool:
        """
        Check if a model is available for use.

        Args:
            model: Model identifier

        Returns:
            True if model is available, False otherwise
        """
        info = self.get_model_info(model)

        # Check for Ollama models
        if info.get("requires_ollama"):
            # Will be checked by ollama_setup.py
            return True  # Optimistically return True, actual check happens at runtime

        # Check for API key models
        if info.get("requires_api_key"):
            provider = info.get("provider")
            # Check for API keys in environment or config
            env_key = f"{provider.upper()}_API_KEY"
            return os.getenv(env_key) is not None

        return True

    def get_recommended_model(self, task_type: str, budget: str = "free") -> str:
        """
        Get recommended model based on task and budget.

        Args:
            task_type: Type of task
            budget: "free", "low", "medium", "high"

        Returns:
            Recommended model identifier
        """
        if budget == "free":
            return "llama3.3"

        if budget == "low":
            # Prefer Gemini Flash for low-budget scenarios
            if self.is_model_available("gemini-2.0-flash"):
                return "gemini-2.0-flash"
            return "llama3.3"

        if budget in ["medium", "high"]:
            # For creative tasks, prefer Claude
            if task_type in ["scene_writing", "voice_analysis"]:
                if self.is_model_available("claude-sonnet-4.5"):
                    return "claude-sonnet-4.5"

            # For other tasks, use defaults
            return self.get_model_for_task(task_type)

        return "llama3.3"

    def estimate_cost(self, model: str, estimated_tokens: int) -> float:
        """
        Estimate cost for using a model.

        Args:
            model: Model identifier
            estimated_tokens: Estimated number of tokens

        Returns:
            Estimated cost in dollars
        """
        info = self.get_model_info(model)
        cost_per_1k = info.get("cost_per_1k_tokens", 0.0)
        return (estimated_tokens / 1000) * cost_per_1k

    def get_task_summary(self) -> Dict[str, str]:
        """
        Get summary of which models are assigned to which tasks.

        Returns:
            Dictionary mapping task types to model names
        """
        return {
            task: self.get_model_for_task(task)
            for task in self.TASK_DEFAULTS.keys()
        }


# Convenience function for quick model lookup
def get_model(task_type: str, project_id: Optional[str] = None) -> str:
    """
    Quick function to get model for a task.

    Args:
        task_type: Type of task
        project_id: Optional project ID

    Returns:
        Model identifier
    """
    router = ModelRouter(project_id)
    return router.get_model_for_task(task_type)


if __name__ == "__main__":
    # Test the router
    router = ModelRouter()

    print("Model Router - Task Assignments")
    print("=" * 50)

    for task, model in router.get_task_summary().items():
        info = router.get_model_info(model)
        cost = f"${info['cost_per_1k_tokens']:.4f}/1K" if info['cost_per_1k_tokens'] > 0 else "FREE"
        print(f"{task:25} -> {model:20} ({cost})")

    print("\n" + "=" * 50)
    print(f"Total cost for 100K token wizard: ${router.estimate_cost('llama3.3', 100000):.2f}")
    print(f"Total cost for 100K token scenes: ${router.estimate_cost('claude-sonnet-4.5', 100000):.2f}")
