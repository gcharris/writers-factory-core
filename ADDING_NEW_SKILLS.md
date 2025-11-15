# Adding New Skills to Writers Factory

Guide for developers adding new writing craft skills to the Universal Skill System.

## Overview

There are two ways to add skills:
1. **Native Python Agent** - Create a Python class implementing the skill
2. **Claude Skill (MCP)** - Register an external Claude Code skill

This guide covers Native Python agents (most common).

---

## Quick Start

### 1. Create Your Agent Class

**Location:** `factory/agents/[category]/[skill_name].py`

**Template:**
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class YourSkillResult:
    """Result dataclass for your skill."""
    # Define your output structure
    score: int
    analysis: str
    suggestions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "analysis": self.analysis,
            "suggestions": self.suggestions
        }


class YourSkillAgent:
    """Description of what your skill does."""

    def __init__(self, knowledge_path: Optional[Path] = None):
        """Initialize agent with optional knowledge base.

        Args:
            knowledge_path: Path to reference materials
        """
        self.knowledge_path = knowledge_path or Path(__file__).parent.parent.parent / "knowledge"
        self._load_references()

    def _load_references(self):
        """Load reference materials from knowledge base."""
        # Load any reference files you need
        pass

    async def execute(
        self,
        input_text: str,
        mode: str = "standard",
        **kwargs
    ) -> Dict[str, Any]:
        """Execute skill (MCP-compatible interface).

        Args:
            input_text: Primary input (scene, dialogue, etc.)
            mode: Execution mode
            **kwargs: Additional skill-specific parameters

        Returns:
            MCP-formatted response:
            {
                "status": "success" | "error",
                "data": {...},  # YourSkillResult.to_dict()
                "metadata": {...}
            }
        """
        try:
            # 1. Validate input
            if not input_text or not input_text.strip():
                return self._error_response("Input text is required")

            # 2. Process input
            result = self._process(input_text, mode, **kwargs)

            # 3. Return MCP-formatted response
            return {
                "status": "success",
                "data": result.to_dict(),
                "metadata": {
                    "provider": "native_python",
                    "skill_name": "your-skill-name",
                    "execution_time_ms": 0,  # Track if needed
                    "cost_estimate": 0.0
                }
            }
        except Exception as e:
            return self._error_response(str(e))

    def _process(self, input_text: str, mode: str, **kwargs) -> YourSkillResult:
        """Core processing logic."""
        # Implement your skill logic here
        score = self._calculate_score(input_text)
        analysis = self._analyze(input_text)
        suggestions = self._generate_suggestions(input_text)

        return YourSkillResult(
            score=score,
            analysis=analysis,
            suggestions=suggestions
        )

    def _calculate_score(self, input_text: str) -> int:
        """Calculate score (0-100)."""
        # Your scoring logic
        return 85

    def _analyze(self, input_text: str) -> str:
        """Generate analysis."""
        return "Analysis text..."

    def _generate_suggestions(self, input_text: str) -> List[str]:
        """Generate improvement suggestions."""
        return ["Suggestion 1", "Suggestion 2"]

    def _error_response(self, message: str) -> Dict[str, Any]:
        """Generate error response."""
        return {
            "status": "error",
            "error": {
                "code": "EXECUTION_ERROR",
                "message": message
            },
            "metadata": {
                "provider": "native_python"
            }
        }
```

---

### 2. Register with Orchestrator

**File:** `factory/core/skill_orchestrator.py`

**Add to `_register_native_agents()` method:**
```python
def _register_native_agents(self):
    """Register native Python skill implementations."""
    # Existing registrations...

    # Your new skill
    from factory.agents.your_category.your_skill import YourSkillAgent

    self.native_agents["your-skill-name"] = {
        "agent_class": YourSkillAgent,
        "description": "What your skill does",
        "capability": "analyze",  # or "enhance", "generate", "validate"
        "input_schema": {
            "input_text": "string - Primary input",
            "mode": "enum[standard|detailed] - Processing mode"
        },
        "output_schema": {
            "score": "integer - Quality score (0-100)",
            "analysis": "string - Analysis text",
            "suggestions": "array[string] - Improvement suggestions"
        }
    }
```

---

### 3. Add to MCP Bridge (Optional)

If you want to expose your skill to Claude Code via MCP:

**File:** `factory/mcp/claude_skill_bridge.py`

**Add to `_register_skills()` method:**
```python
self.skills_registry["your-skill-name"] = SkillDefinition(
    name="your-skill-full-name",
    skill_id="your-skill-name",
    capability="analyze",
    description="What your skill does",
    cost_tier=CostTier.PREMIUM,  # or STANDARD, FREE
    input_schema={
        "input_text": "string - Primary input",
        "mode": "string - Processing mode"
    },
    output_schema={
        "score": "integer - Quality score",
        "analysis": "string - Analysis text",
        "suggestions": "array[string] - Suggestions"
    }
)
```

---

### 4. Write Tests

**File:** `tests/test_your_skill.py`

```python
import pytest
from factory.agents.your_category.your_skill import YourSkillAgent


@pytest.mark.asyncio
async def test_basic_execution():
    """Test basic skill execution."""
    agent = YourSkillAgent()

    result = await agent.execute(
        input_text="Sample input text",
        mode="standard"
    )

    assert result["status"] == "success"
    assert "score" in result["data"]
    assert 0 <= result["data"]["score"] <= 100


@pytest.mark.asyncio
async def test_empty_input():
    """Test error handling for empty input."""
    agent = YourSkillAgent()

    result = await agent.execute(input_text="")

    assert result["status"] == "error"
    assert "message" in result["error"]


@pytest.mark.asyncio
async def test_with_reference_knowledge():
    """Test skill uses reference knowledge."""
    from pathlib import Path

    knowledge_path = Path("factory/knowledge")
    agent = YourSkillAgent(knowledge_path=knowledge_path)

    result = await agent.execute(
        input_text="Sample text",
        mode="detailed"
    )

    assert result["status"] == "success"
```

---

### 5. Update Documentation

**Add to `SKILL_SYSTEM_GUIDE.md`:**
```markdown
### X. Your Skill Name
**ID:** `your-skill-name`
**Capability:** analyze
**Description:** What your skill does and why it's useful.

**Providers:**
- Native Python (All tiers)

**Input:**
\`\`\`json
{
  "input_text": "Primary input",
  "mode": "standard|detailed"
}
\`\`\`

**Output:**
\`\`\`json
{
  "score": 85,
  "analysis": "Analysis text...",
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}
\`\`\`
```

---

## Integration Checklist

Before considering your skill complete:

### Code Quality
- [ ] Agent class follows template structure
- [ ] Implements `execute()` method with MCP-compatible interface
- [ ] Returns proper status/data/metadata structure
- [ ] Has error handling for invalid inputs
- [ ] Includes docstrings for all public methods

### Functionality
- [ ] Core logic works correctly
- [ ] Scores/analysis are meaningful
- [ ] Suggestions are actionable
- [ ] Uses reference knowledge if applicable
- [ ] Handles edge cases gracefully

### Integration
- [ ] Registered with orchestrator
- [ ] Added to MCP bridge (if exposing via Claude Code)
- [ ] Works through `/api/skills/execute` endpoint
- [ ] Appears in `/api/skills/list` response
- [ ] Can be called from CraftPanel UI

### Testing
- [ ] Unit tests for core logic
- [ ] Integration test via orchestrator
- [ ] API endpoint test
- [ ] Frontend UI test (manual)
- [ ] Reference knowledge loading test

### Documentation
- [ ] Added to SKILL_SYSTEM_GUIDE.md
- [ ] Input/output schemas documented
- [ ] Usage examples provided
- [ ] Known limitations noted

---

## Example: Scene Analyzer

See `factory/agents/explants/scene_analyzer.py` for a complete reference implementation.

**Key features:**
- Comprehensive scoring system (5 categories)
- Anti-pattern detection with regex
- Reference knowledge integration
- Detailed fix suggestions
- Multiple execution modes

---

## Best Practices

### 1. Make It Deterministic
Native Python skills should be deterministic when possible:
- Use regex patterns, not LLM calls
- Apply consistent scoring rubrics
- Generate reproducible suggestions

### 2. Use Reference Knowledge
Store standards in `factory/knowledge/`:
- Anti-patterns
- Style guides
- Character bibles
- Quality rubrics

### 3. Provide Actionable Output
Users need to know:
- What's wrong (specific issues)
- Where it's wrong (line numbers, quotes)
- How to fix it (concrete suggestions)
- Why it matters (explanation)

### 4. Support Progressive Enhancement
Different modes for different needs:
- `quick` - Fast audit, major issues only
- `standard` - Balanced analysis
- `detailed` - Comprehensive deep-dive

### 5. Handle Errors Gracefully
Return structured errors:
```python
{
    "status": "error",
    "error": {
        "code": "INVALID_INPUT",
        "message": "Scene content is required",
        "details": {"field": "scene_content"}
    }
}
```

---

## Advanced Topics

### Using LLMs in Native Skills

If your skill needs AI:
```python
from factory.agents.ollama_agent import OllamaAgent

class YourSkillAgent:
    def __init__(self):
        self.llm = OllamaAgent(model_name="mistral")

    async def _generate_with_llm(self, prompt: str) -> str:
        response = await self.llm.generate(prompt)
        return response["content"]
```

### Caching Results

For expensive operations:
```python
from functools import lru_cache

class YourSkillAgent:
    @lru_cache(maxsize=100)
    def _expensive_analysis(self, text: str) -> str:
        # Expensive computation
        return result
```

### Progressive Disclosure

Start simple, add complexity:
1. Basic score calculation
2. Add category breakdown
3. Add specific issue detection
4. Add fix suggestions
5. Add before/after examples

---

## Getting Help

- Review existing agents in `factory/agents/`
- Check orchestrator code: `factory/core/skill_orchestrator.py`
- See API reference: `API_REFERENCE.md`
- Test with: `pytest tests/`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-14
