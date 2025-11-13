#!/usr/bin/env python3
"""
Test script for Writers Factory Web Application

Verifies that all components can import and basic functionality works.
"""

import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all backend imports work."""
    print("Testing imports...")

    try:
        from webapp.backend.app import app
        print("  ✅ FastAPI app imports successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import FastAPI app: {e}")
        return False

    try:
        from factory.wizard.wizard import CreationWizard
        print("  ✅ CreationWizard imports successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import CreationWizard: {e}")
        return False

    try:
        from factory.tools.model_comparison import ModelComparisonTool
        print("  ✅ ModelComparisonTool imports successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import ModelComparisonTool: {e}")
        return False

    try:
        from factory.knowledge.router import KnowledgeRouter
        print("  ✅ KnowledgeRouter imports successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import KnowledgeRouter: {e}")
        return False

    return True


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")

    webapp_dir = Path(__file__).parent

    files = [
        webapp_dir / "backend" / "app.py",
        webapp_dir / "frontend" / "index.html",
        webapp_dir / "frontend" / "static" / "app.js",
        webapp_dir / "launch.py",
        webapp_dir / "README.md"
    ]

    all_exist = True
    for file_path in files:
        if file_path.exists():
            print(f"  ✅ {file_path.relative_to(webapp_dir)}")
        else:
            print(f"  ❌ {file_path.relative_to(webapp_dir)} NOT FOUND")
            all_exist = False

    return all_exist


def test_agent_config():
    """Test that agent configuration can be loaded."""
    print("\nTesting agent configuration...")

    try:
        from factory.core.config.loader import load_agent_config
        config = load_agent_config()

        agents = config.get("agents", {})
        print(f"  ✅ Loaded {len(agents)} agents")

        enabled_agents = [name for name, cfg in agents.items() if cfg.get("enabled", True)]
        print(f"  ✅ {len(enabled_agents)} agents enabled")

        return True
    except Exception as e:
        print(f"  ❌ Failed to load agent config: {e}")
        return False


def test_credentials():
    """Test that credentials can be loaded."""
    print("\nTesting credentials...")

    try:
        from factory.core.config.loader import load_credentials
        creds = load_credentials()

        providers = list(creds.keys())
        print(f"  ✅ Found credentials for {len(providers)} providers")
        for provider in providers:
            print(f"     - {provider}")

        return True
    except Exception as e:
        print(f"  ❌ Failed to load credentials: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Writers Factory Web Application - Test Suite")
    print("=" * 70)
    print()

    results = {
        "Imports": test_imports(),
        "File Structure": test_file_structure(),
        "Agent Config": test_agent_config(),
        "Credentials": test_credentials()
    }

    print()
    print("=" * 70)
    print("Test Results")
    print("=" * 70)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")

    print()

    if all(results.values()):
        print("🎉 All tests passed! Web app is ready to launch.")
        print()
        print("To start the web application:")
        print("  python3 webapp/launch.py")
        return 0
    else:
        print("⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
