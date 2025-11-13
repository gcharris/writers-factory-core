#!/usr/bin/env python3
"""Initialize Cognee database for Writers Factory.

This script initializes Cognee with your API keys configured.
Run this after you've added your API keys to .env or config/credentials.json.

Usage:
    python3 init_cognee.py
"""

import asyncio
import os
import sys
from pathlib import Path


async def init_cognee():
    """Initialize Cognee database."""
    try:
        # Check if API keys are set
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not openai_key and not anthropic_key:
            print("❌ ERROR: No API keys found.")
            print()
            print("Cognee requires an LLM API key to initialize.")
            print("Please set either:")
            print("  - OPENAI_API_KEY in your .env file")
            print("  - ANTHROPIC_API_KEY in your .env file")
            print()
            print("Then run this script again.")
            sys.exit(1)

        print("🔄 Initializing Cognee...")
        print(f"   Using: {'OpenAI' if openai_key else 'Anthropic'}")

        from cognee import add, cognify

        # Add a simple initialization document
        await add("Writers Factory Core - Knowledge System Initialized")

        print("✅ Cognee initialized successfully!")
        print(f"   Database location: {Path('.cognee').absolute()}")
        print()
        print("Next steps:")
        print("  1. Add your reference materials to project/reference/")
        print("  2. Run: python3 -c \"from cognee import add; import asyncio; asyncio.run(add('path/to/file.md'))\"")
        print("  3. Test with: python3 -c \"from factory.knowledge.router import KnowledgeRouter; print('OK')\"")

    except ImportError as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Make sure Cognee is installed:")
        print("  uv pip install cognee")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Check that your API keys are valid and have sufficient credits.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_cognee())
