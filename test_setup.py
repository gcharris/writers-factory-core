#!/usr/bin/env python3
"""Test Writers Factory setup and verify all components work.

This script tests the environment setup without requiring API keys.
Run this after setup to verify everything is configured correctly.

Usage:
    python3 test_setup.py
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all core modules can be imported."""
    print("🔄 Testing core imports...")

    try:
        from factory.core.agent_pool import AgentPool
        print("  ✅ AgentPool")
    except ImportError as e:
        print(f"  ❌ AgentPool: {e}")
        return False

    try:
        from factory.core.workflow_engine import WorkflowEngine
        print("  ✅ WorkflowEngine")
    except ImportError as e:
        print(f"  ❌ WorkflowEngine: {e}")
        return False

    try:
        from factory.knowledge.router import KnowledgeRouter
        print("  ✅ KnowledgeRouter")
    except ImportError as e:
        print(f"  ❌ KnowledgeRouter: {e}")
        return False

    try:
        from factory.knowledge.cache import QueryCache
        print("  ✅ QueryCache")
    except ImportError as e:
        print(f"  ❌ QueryCache: {e}")
        return False

    return True


def test_agent_pool():
    """Test that AgentPool can be initialized."""
    print("\n🔄 Testing AgentPool initialization...")

    try:
        from factory.core.agent_pool import AgentPool

        # Create pool (shouldn't require API keys to initialize)
        pool = AgentPool()
        print(f"  ✅ AgentPool created")

        # Try to list agents
        agents = pool.list_agents()
        print(f"  ✅ Found {len(agents)} registered agents")

        return True
    except Exception as e:
        print(f"  ❌ AgentPool error: {e}")
        return False


def test_workflow_engine():
    """Test that WorkflowEngine can be initialized."""
    print("\n🔄 Testing WorkflowEngine...")

    try:
        from factory.core.workflow_engine import WorkflowEngine, Workflow

        # Create engine
        engine = WorkflowEngine()
        print("  ✅ WorkflowEngine created")

        return True
    except Exception as e:
        print(f"  ❌ WorkflowEngine error: {e}")
        return False


def test_knowledge_router():
    """Test that KnowledgeRouter can be initialized."""
    print("\n🔄 Testing KnowledgeRouter...")

    try:
        from factory.knowledge.router import KnowledgeRouter, QueryType

        # Create router
        router = KnowledgeRouter(prefer_local=True)
        print("  ✅ KnowledgeRouter created")

        # Test query classification
        factual = router.classify_query("What is Mickey's background?")
        print(f"  ✅ Query classification: {factual.value}")

        return True
    except Exception as e:
        print(f"  ❌ KnowledgeRouter error: {e}")
        return False


def test_directory_structure():
    """Test that project directory structure exists."""
    print("\n🔄 Testing project directory structure...")

    required_dirs = [
        "project",
        "project/manuscript",
        "project/reference",
        "project/reference/characters",
        "project/reference/worldbuilding",
        "project/reference/research",
        "project/planning",
        "project/.session",
        ".venv",
        "config",
        "factory",
        "factory/core",
        "factory/agents",
        "factory/knowledge",
        "factory/storage",
        "docs/tasks"
    ]

    all_exist = True
    for dir_path in required_dirs:
        p = Path(dir_path)
        if p.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (missing)")
            all_exist = False

    return all_exist


def test_config_files():
    """Test that configuration files exist."""
    print("\n🔄 Testing configuration files...")

    required_files = [
        ("config/credentials.json", "API key configuration"),
        (".env.template", "Environment template"),
        (".gitignore", "Git ignore rules"),
        ("SETUP.md", "Setup documentation"),
        ("init_cognee.py", "Cognee initialization script"),
        ("requirements.txt", "Python dependencies")
    ]

    all_exist = True
    for file_path, description in required_files:
        p = Path(file_path)
        if p.exists():
            print(f"  ✅ {file_path} ({description})")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_exist = False

    return all_exist


def main():
    """Run all tests."""
    print("=" * 70)
    print("Writers Factory Core - Setup Verification")
    print("=" * 70)

    results = []

    # Run tests
    results.append(("Core Imports", test_imports()))
    results.append(("AgentPool", test_agent_pool()))
    results.append(("WorkflowEngine", test_workflow_engine()))
    results.append(("KnowledgeRouter", test_knowledge_router()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Config Files", test_config_files()))

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")

    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)

    if passed == total:
        print("\n🎉 All tests passed! Environment is ready.")
        print("\nNext steps:")
        print("  1. Add your API keys to config/credentials.json and .env")
        print("  2. Run: python3 init_cognee.py")
        print("  3. Run: pytest tests/ -v")
        print("  4. Try the Phase 1 demo: python3 demo_interactive.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        print("\nTroubleshooting:")
        print("  - Make sure virtual environment is activated: source .venv/bin/activate")
        print("  - Reinstall dependencies: uv pip install -r requirements.txt")
        print("  - Check SETUP.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
