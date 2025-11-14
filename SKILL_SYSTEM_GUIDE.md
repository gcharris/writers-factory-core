# Universal Skill System - User Guide

## Overview

The Universal Skill System transforms Writers Factory into an intelligent multi-agent platform. It provides access to 6 Explants writing craft skills through a unified interface.

**Sprint 12 - Phase A Implementation**

## Architecture

```
┌─────────────┐
│   Frontend  │  CraftPanel.jsx
│   (React)   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │  simple_app.py (/api/skills/*)
│   (FastAPI) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Orchestrator │  skill_orchestrator.py
│  (Routing)  │  - Provider selection
└──────┬──────┘  - Fallback handling
       │          - Cost optimization
       │
       ├─────────────┬────────────┬───────────┐
       ▼             ▼            ▼           ▼
┌──────────┐  ┌──────────┐  ┌────────┐  ┌────────┐
│  Claude  │  │  Native  │  │ OpenAI │  │ Local  │
│  Skills  │  │  Python  │  │  API   │  │  LLM   │
│  (MCP)   │  │  Agents  │  │        │  │        │
└──────────┘  └──────────┘  └────────┘  └────────┘
```

## Available Skills

### 1. Scene Analyzer & Scorer
**ID:** `scene-analyzer`
**Capability:** analyze
**Description:** Analyzes scene quality using Explants craft standards. Scores voice authenticity, character consistency, metaphor discipline, anti-patterns, and phase appropriateness.

**Providers:**
- Claude Skill (Premium tier)
- Native Python (All tiers)

**Input:**
```json
{
  "scene_content": "The scene text to analyze",
  "mode": "detailed|quick|variant_comparison",
  "phase": "phase1|phase2|phase3",
  "reference_files": ["optional references"]
}
```

**Output:**
```json
{
  "total_score": 85,
  "quality_tier": "A Tier (85-89)",
  "category_scores": {
    "voice_authenticity": 24,
    "character_consistency": 18,
    "metaphor_discipline": 17,
    "anti_pattern_compliance": 13,
    "phase_appropriateness": 13
  },
  "fixes": [
    {
      "pattern": "filter_word",
      "old_string": "She saw the gun",
      "suggested_fix": "The gun",
      "priority": "medium"
    }
  ]
}
```

---

### 2. Scene Enhancer
**ID:** `scene-enhancer`
**Capability:** enhance
**Description:** Enhances scenes to meet Explants craft standards. Fixes voice issues, strengthens metaphors, eliminates anti-patterns.

**Providers:**
- Claude Skill (Premium tier)
- (Native Python implementation: Phase B)

**Input:**
```json
{
  "scene_content": "Original scene text",
  "fixes_to_apply": [{"pattern": "...", "old_string": "..."}],
  "enhancement_level": "minimal|standard|aggressive",
  "preserve_structure": true
}
```

---

### 3. Mickey Bardot Character Identity Validator
**ID:** `character-validator`
**Capability:** validate
**Description:** Validates Mickey Bardot's character identity across scenes. Ensures psychological consistency and capability alignment.

**Providers:**
- Claude Skill (Premium tier)

---

### 4. Mickey Scene Writer
**ID:** `scene-writer`
**Capability:** generate
**Description:** Generates complete scenes with Mickey Bardot as POV character following Explants craft standards.

**Providers:**
- Claude Skill (Premium tier)

---

### 5. Scene Multiplier (Variant Generator)
**ID:** `scene-multiplier`
**Capability:** generate
**Description:** Generates multiple variants of a scene for comparison. Creates 3-5 versions with different approaches.

**Providers:**
- Claude Skill (Premium tier)

---

### 6. Smart Scaffold Generator
**ID:** `scaffold-generator`
**Capability:** generate
**Description:** Generates intelligent scene scaffolds (beat sheets with rich context). Creates detailed outlines that guide scene writing.

**Providers:**
- Claude Skill (Premium tier)

---

## Using the System

### Via Web UI

1. **Open Writers Factory** at `http://localhost:8000`
2. **Click "Craft" tab** in the top navigation
3. **Select skill** from dropdown
4. **Paste scene content** in text area
5. **Choose options** (mode, phase, etc.)
6. **Click "Execute Skill"**
7. **View results** with scores, fixes, and metadata

### Via API

```bash
curl -X POST http://localhost:8000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "scene-analyzer",
    "input_data": {
      "scene_content": "Your scene text here...",
      "mode": "detailed",
      "phase": "phase2"
    },
    "allow_fallback": true
  }'
```

### Via Python

```python
from factory.core.skill_orchestrator import SkillOrchestrator, SkillRequest

orchestrator = SkillOrchestrator(
    user_tier="premium",
    knowledge_path=Path("factory/knowledge")
)

request = SkillRequest(
    skill_name="scene-analyzer",
    input_data={
        "scene_content": "Your scene text...",
        "mode": "detailed",
        "phase": "phase2"
    }
)

response = await orchestrator.execute_skill(request)
print(f"Score: {response.data['total_score']}")
```

## Provider Selection

The orchestrator intelligently routes requests:

### Premium Users
1. Try Claude Skill first (best quality)
2. Fall back to Native Python if unavailable
3. Fall back to OpenAI if needed
4. Fall back to Local LLM as last resort

### Standard Users
1. Try Native Python first (free, good quality)
2. Fall back to Local LLM if available
3. Error if no fallback available

### Cost Optimization

- **Native Python:** Free, instant, deterministic
- **Claude Skills:** Premium quality, costs tokens
- **Local LLM:** Free, requires setup
- **OpenAI:** Pay-per-use

## Quality Tiers

| Score | Tier | Meaning |
|-------|------|---------|
| 95-100 | Gold Standard | Publication-ready |
| 90-94 | A+ | Excellent, minor polish needed |
| 85-89 | A | Strong, targeted revision needed |
| 80-84 | B+ | Competent, moderate revision |
| 75-79 | B | Adequate, significant revision |
| 60-74 | C | Needs significant work |
| 40-59 | D | Fundamental issues |
| 0-39 | F | Does not meet standards |

## Best Practices

### For Scene Analysis

1. **Use detailed mode** for comprehensive feedback
2. **Match phase** to your skill level:
   - Phase 1: Learning (more forgiving)
   - Phase 2: Professional (strict standards)
   - Phase 3: Advanced (very strict)
3. **Review all fixes** before applying
4. **Run analysis after** making changes

### For Scene Enhancement

1. **Analyze first** to identify issues
2. **Start with "minimal"** enhancement level
3. **Preserve structure** unless restructuring needed
4. **Compare before/after** carefully
5. **Re-analyze enhanced** scene to verify improvement

### For Character Validation

1. **Provide context** scenes for consistency checking
2. **Reference character bible** in resources
3. **Check across multiple scenes** for patterns

## Troubleshooting

### "Skill execution failed"
- Check backend is running: `http://localhost:8000/api/health`
- Verify scene content is not empty
- Try with `allow_fallback: true`

### "Provider unavailable"
- Check provider health: `GET /api/skills/health`
- Verify API keys if using Claude Skills
- Try forcing Native Python provider

### Low Scores
- Review anti-pattern violations first (highest impact)
- Check voice consistency issues
- Verify metaphor domain alignment
- Match phase to your skill level

## Next Steps

- See **ADDING_NEW_SKILLS.md** for creating custom skills
- See **API_REFERENCE.md** for complete API documentation
- See `factory/knowledge/README.md` for craft standards

---

**Version:** Sprint 12 Phase A
**Last Updated:** 2025-11-14
