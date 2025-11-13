# Contributing to Writers Factory Core

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and constructive in all interactions. We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Code samples if applicable

### Suggesting Features

1. Check if the feature has been suggested in Issues
2. Create a new issue with:
   - Clear use case description
   - Why this feature would be useful
   - Proposed implementation approach (optional)
   - Examples of similar features in other tools (optional)

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Format code: `black factory/ tests/`
7. Check types: `mypy factory/`
8. Commit changes (`git commit -m 'Add amazing feature'`)
9. Push to branch (`git push origin feature/amazing-feature`)
10. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/writers-factory-core.git
cd writers-factory-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install dev dependencies
pip install black isort flake8 mypy pytest pytest-asyncio
```

## Code Style

### Python Style
- Follow PEP 8
- Use Black for formatting (line length 100)
- Use isort for import sorting
- Use type hints for all functions
- Write docstrings for all public classes and functions

### Docstring Format
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed. Can span multiple lines.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input
    """
    pass
```

### Testing
- Write tests for all new features
- Use pytest for testing
- Use pytest-asyncio for async tests
- Aim for >80% code coverage
- Mock external API calls

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues: "Fix #123"

## Project Structure

```
writers-factory-core/
├── factory/           # Main package
│   ├── core/         # Core engine
│   ├── agents/       # LLM integrations
│   ├── knowledge/    # Knowledge systems
│   ├── workflows/    # Pre-built workflows
│   ├── storage/      # Database
│   └── ui/           # CLI interface
├── tests/            # Test suite
├── docs/             # Documentation
├── examples/         # Usage examples
└── README.md         # Project overview
```

## Adding New Agents

See [docs/ADDING_AGENTS.md](docs/ADDING_AGENTS.md) for detailed guide.

Quick checklist:
1. Create agent class inheriting from BaseAgent
2. Implement `generate()` method
3. Add configuration to agents.yaml
4. Write tests in tests/test_agents.py
5. Add example usage
6. Update documentation

## Adding New Workflows

See [docs/CREATING_WORKFLOWS.md](docs/CREATING_WORKFLOWS.md) for detailed guide.

Quick checklist:
1. Create workflow class inheriting from BaseWorkflow
2. Implement setup/execute/cleanup methods
3. Add workflow to factory/workflows/
4. Write tests in tests/test_workflows.py
5. Add example usage
6. Update documentation

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=factory --cov-report=html

# Run specific test file
pytest tests/test_agents.py

# Run specific test
pytest tests/test_agents.py::test_agent_creation

# Run async tests
pytest -v -s tests/test_workflows.py
```

## Code Quality

```bash
# Format code
black factory/ tests/ examples/

# Sort imports
isort factory/ tests/ examples/

# Check style
flake8 factory/ tests/

# Check types
mypy factory/
```

## Documentation

- Update README.md if adding major features
- Add/update docstrings for all public APIs
- Update relevant docs in docs/ directory
- Add examples for new features
- Update CHANGELOG.md

## Pull Request Process

1. Update CHANGELOG.md with your changes
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Update README if needed
6. Request review from maintainers

### PR Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code formatted with Black
- [ ] Type hints added
- [ ] All tests passing

## Questions?

- Open an issue for questions
- Check existing issues and discussions
- Read the documentation in docs/

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Writers Factory Core!
