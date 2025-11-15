# Writers Factory Knowledge Base

This directory contains reference materials for writing craft agents.

## Structure

```
knowledge/
├── craft/           # Writing craft standards
│   ├── anti-patterns.md
│   ├── voice-gold-standard.md
│   └── metaphor-domains.md
├── character/       # Character-specific reference
│   └── (to be added)
└── scoring/         # Quality assessment
    └── quality-tiers.md
```

## Purpose

These reference materials are used by:

1. **Scene Analyzer Agent** (`factory/agents/explants/scene_analyzer.py`)
   - Anti-pattern detection
   - Voice authenticity scoring
   - Metaphor discipline checking

2. **Scene Enhancer Agent** (future)
   - Fixing anti-patterns
   - Improving voice consistency
   - Strengthening metaphors

3. **Character Validator Agent** (future)
   - Checking character consistency
   - Validating psychological coherence

## Usage

Agents load these files at initialization:

```python
from pathlib import Path

knowledge_path = Path(__file__).parent.parent.parent / "knowledge"
craft_path = knowledge_path / "craft"
```

## Content Guidelines

Reference materials should:
- Define standards clearly
- Provide examples (good and bad)
- Explain the "why" behind rules
- Be implementation-agnostic
- Support both AI and human use

## Sprint 12 Implementation

This knowledge base was created as part of Sprint 12: Universal Skill System.

**Related Components:**
- MCP Skill Bridge: `factory/mcp/claude_skill_bridge.py`
- Skill Orchestrator: `factory/core/skill_orchestrator.py`
- Native Scene Analyzer: `factory/agents/explants/scene_analyzer.py`
- Backend API: `webapp/backend/simple_app.py` (skill endpoints)
- Frontend UI: `webapp/frontend-v2/src/features/craft/CraftPanel.jsx`

## Extending

To add new reference materials:

1. Create appropriately named `.md` file in correct subdirectory
2. Follow existing format (title, principles, examples)
3. Update this README
4. Update relevant agent code to use new material
5. Test agent can load and use the material

## Version

- Created: Sprint 12
- Last Updated: 2025-11-14
