"""
Ollama Setup and Integration

Handles Ollama installation checks, model downloads, and API interactions.
Provides free local LLM inference via Llama 3.3.
"""

import asyncio
import subprocess
import sys
import json
from typing import Optional, Dict, Any, List
import httpx


class OllamaSetup:
    """Manage Ollama installation and model availability."""

    REQUIRED_MODEL = "llama3.3"
    OLLAMA_API_BASE = "http://localhost:11434"

    @staticmethod
    async def is_ollama_installed() -> bool:
        """
        Check if Ollama is installed and accessible.

        Returns:
            True if Ollama is installed, False otherwise
        """
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    async def get_installed_models() -> List[str]:
        """
        Get list of installed Ollama models.

        Returns:
            List of model names
        """
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return []

            # Parse output (format: "NAME  ID  SIZE  MODIFIED")
            lines = result.stdout.strip().split('\n')
            models = []

            for line in lines[1:]:  # Skip header
                if line.strip():
                    # First column is model name
                    model_name = line.split()[0]
                    models.append(model_name)

            return models

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    @staticmethod
    async def is_model_available(model_name: str) -> bool:
        """
        Check if a specific model is available locally.

        Args:
            model_name: Name of the model (e.g., "llama3.3")

        Returns:
            True if model is available, False otherwise
        """
        models = await OllamaSetup.get_installed_models()
        return any(model_name in model for model in models)

    @staticmethod
    async def download_model(model_name: str, progress_callback: Optional[callable] = None) -> bool:
        """
        Download and install an Ollama model.

        Args:
            model_name: Name of the model to download
            progress_callback: Optional callback for progress updates

        Returns:
            True if download successful, False otherwise
        """
        print(f"Downloading Ollama model: {model_name}")
        print("This may take a few minutes (4.7GB for Llama 3.3)...")

        try:
            process = subprocess.Popen(
                ["ollama", "pull", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream output
            for line in process.stdout:
                line = line.strip()
                if line:
                    print(f"  {line}")
                    if progress_callback:
                        progress_callback(line)

            process.wait()
            return process.returncode == 0

        except Exception as e:
            print(f"Error downloading model: {e}")
            return False

    @staticmethod
    async def ensure_ollama_ready(required_model: str = "llama3.3") -> Dict[str, Any]:
        """
        Ensure Ollama is installed and required model is available.

        Args:
            required_model: Model to check/download

        Returns:
            Dictionary with status info:
                - installed: bool
                - model_available: bool
                - message: str
                - action_needed: str or None
        """
        # Check if Ollama is installed
        if not await OllamaSetup.is_ollama_installed():
            return {
                "installed": False,
                "model_available": False,
                "message": "Ollama is not installed",
                "action_needed": "install_ollama",
                "install_url": "https://ollama.ai/download"
            }

        # Check if required model is available
        if not await OllamaSetup.is_model_available(required_model):
            return {
                "installed": True,
                "model_available": False,
                "message": f"Model '{required_model}' not found",
                "action_needed": "download_model",
                "model_name": required_model,
                "model_size": "4.7GB"
            }

        # All good!
        return {
            "installed": True,
            "model_available": True,
            "message": f"Ollama and '{required_model}' are ready",
            "action_needed": None
        }

    @staticmethod
    async def generate(
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate text using Ollama API.

        Args:
            model: Model name (e.g., "llama3.3")
            prompt: User prompt
            system: Optional system prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with:
                - response: str (generated text)
                - success: bool
                - error: str or None
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                    }
                }

                if system:
                    payload["system"] = system

                if max_tokens:
                    payload["options"]["num_predict"] = max_tokens

                response = await client.post(
                    f"{OllamaSetup.OLLAMA_API_BASE}/api/generate",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data.get("response", ""),
                        "success": True,
                        "error": None
                    }
                else:
                    return {
                        "response": "",
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }

        except Exception as e:
            return {
                "response": "",
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def chat(
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Chat with Ollama model using conversation history.

        Args:
            model: Model name
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with response info
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                    }
                }

                if max_tokens:
                    payload["options"]["num_predict"] = max_tokens

                response = await client.post(
                    f"{OllamaSetup.OLLAMA_API_BASE}/api/chat",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "message": data.get("message", {}),
                        "response": data.get("message", {}).get("content", ""),
                        "success": True,
                        "error": None
                    }
                else:
                    return {
                        "message": {},
                        "response": "",
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }

        except Exception as e:
            return {
                "message": {},
                "response": "",
                "success": False,
                "error": str(e)
            }


# Convenience functions
async def check_ollama() -> Dict[str, Any]:
    """Quick check of Ollama status."""
    return await OllamaSetup.ensure_ollama_ready()


async def generate_text(prompt: str, model: str = "llama3.3", system: Optional[str] = None) -> str:
    """
    Quick text generation with Ollama.

    Args:
        prompt: User prompt
        model: Model to use
        system: Optional system prompt

    Returns:
        Generated text or error message
    """
    result = await OllamaSetup.generate(model, prompt, system)

    if result["success"]:
        return result["response"]
    else:
        return f"Error: {result['error']}"


# Test/demo code
if __name__ == "__main__":
    async def main():
        print("Ollama Setup Check")
        print("=" * 50)

        # Check status
        status = await check_ollama()
        print(f"Ollama installed: {status['installed']}")
        print(f"Model available: {status['model_available']}")
        print(f"Message: {status['message']}")

        if status['action_needed'] == 'download_model':
            print(f"\nModel '{status['model_name']}' needs to be downloaded ({status['model_size']})")
            print("Run: ollama pull llama3.3")

        elif status['action_needed'] == 'install_ollama':
            print(f"\nPlease install Ollama from: {status['install_url']}")

        else:
            # Test generation
            print("\nTesting text generation...")
            response = await generate_text(
                "Explain what a knowledge graph is in one sentence.",
                model="llama3.3"
            )
            print(f"\nResponse: {response}")

    asyncio.run(main())
