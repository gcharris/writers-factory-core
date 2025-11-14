# Skill System API Reference

Complete API documentation for Writers Factory Universal Skill System (Sprint 12).

## Base URL

```
http://localhost:8000/api/skills
```

## Authentication

Currently no authentication required (local development).
In production, use session-based auth or API keys.

---

## Endpoints

### 1. Execute Skill

Execute any registered skill via the orchestrator.

**Endpoint:** `POST /api/skills/execute`

**Request Body:**
```json
{
  "skill_name": "scene-analyzer",
  "input_data": {
    "scene_content": "The scene text to analyze...",
    "mode": "detailed",
    "phase": "phase2"
  },
  "context": {
    "project_id": "explants-v1",
    "scene_id": "scene-123"
  },
  "allow_fallback": true,
  "preferred_provider": "native_python"
}
```

**Parameters:**
- `skill_name` (string, required): Skill identifier (e.g., "scene-analyzer")
- `input_data` (object, required): Skill-specific input matching skill's input_schema
- `context` (object, optional): Additional context (project, scene, character)
- `allow_fallback` (boolean, optional, default: true): Allow fallback to other providers
- `preferred_provider` (string, optional): Force specific provider ("claude_skill", "native_python", "openai", "local_llm")

**Response (Success):**
```json
{
  "status": "success",
  "data": {
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
        "priority": "medium",
        "line_number": 15
      }
    ]
  },
  "metadata": {
    "provider": "native_python",
    "skill_name": "scene-analyzer",
    "execution_time_ms": 245,
    "cost_estimate": 0.0
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "error": {
    "code": "SKILL_EXECUTION_ERROR",
    "message": "Scene content is required"
  },
  "metadata": {
    "provider": "orchestrator"
  }
}
```

**Response (Fallback):**
```json
{
  "status": "fallback",
  "data": {
    "message": "Claude Skill unavailable, using Native Python fallback",
    "result": { ... }
  },
  "metadata": {
    "provider": "native_python",
    "fallback_from": "claude_skill",
    "execution_time_ms": 180
  }
}
```

**HTTP Status Codes:**
- `200 OK` - Success or fallback
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Execution failed

**Example:**
```bash
curl -X POST http://localhost:8000/api/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "scene-analyzer",
    "input_data": {
      "scene_content": "Mickey stepped into the airlock. The hiss of equalizing pressure reminded her of deployments—that moment between safe and not-safe, between one reality and another.",
      "mode": "detailed",
      "phase": "phase2"
    }
  }'
```

---

### 2. List Available Skills

Get all skills available to current user based on tier.

**Endpoint:** `GET /api/skills/list`

**Query Parameters:** None

**Response:**
```json
{
  "skills": [
    {
      "name": "explants-scene-analyzer-scorer",
      "skill_id": "scene-analyzer",
      "capability": "analyze",
      "description": "Analyzes scene quality using Explants craft standards. Scores voice authenticity, character consistency, metaphor discipline, anti-patterns, and phase appropriateness.",
      "available": true,
      "providers": ["claude_skill", "native_python"],
      "cost_tier": "premium"
    },
    {
      "name": "explants-scene-enhancement",
      "skill_id": "scene-enhancer",
      "capability": "enhance",
      "description": "Enhances scenes to meet Explants craft standards...",
      "available": true,
      "providers": ["claude_skill"],
      "cost_tier": "premium"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/skills/list
```

---

### 3. Get Skill Info

Get detailed information about a specific skill.

**Endpoint:** `GET /api/skills/{skill_name}/info`

**Path Parameters:**
- `skill_name` (string, required): Skill identifier

**Response:**
```json
{
  "name": "explants-scene-analyzer-scorer",
  "skill_id": "scene-analyzer",
  "capability": "analyze",
  "description": "Analyzes scene quality using Explants craft standards...",
  "available": true,
  "providers": ["claude_skill", "native_python"],
  "cost_tier": "premium",
  "input_schema": {
    "scene_content": "string - The scene text to analyze",
    "mode": "enum[detailed|quick|variant_comparison] - Analysis depth",
    "phase": "enum[phase1|phase2|phase3] - Voice complexity",
    "reference_files": "array[string] - Optional reference documents"
  },
  "output_schema": {
    "total_score": "integer - Overall score (0-100)",
    "category_scores": "object - Breakdown by category",
    "quality_tier": "string - Professional/Competent/Needs Work",
    "fixes": "array[object] - Specific improvement suggestions"
  },
  "examples": [
    {
      "input": {
        "scene_content": "Mickey checked her weapon...",
        "mode": "detailed",
        "phase": "phase2"
      },
      "output": {
        "total_score": 87,
        "quality_tier": "A Tier"
      }
    }
  ]
}
```

**HTTP Status Codes:**
- `200 OK` - Skill found
- `404 Not Found` - Skill doesn't exist

**Example:**
```bash
curl http://localhost:8000/api/skills/scene-analyzer/info
```

---

### 4. Check Provider Health

Check health status of all skill providers.

**Endpoint:** `GET /api/skills/health`

**Query Parameters:** None

**Response:**
```json
{
  "providers": {
    "claude_skill": {
      "available": false,
      "latency_ms": null,
      "error": "MCP not configured"
    },
    "native_python": {
      "available": true,
      "latency_ms": 12
    },
    "openai": {
      "available": false,
      "error": "API key not set"
    },
    "local_llm": {
      "available": false,
      "error": "Ollama not running"
    }
  },
  "overall_status": "degraded"
}
```

**Overall Status Values:**
- `healthy` - All providers available
- `degraded` - Some providers unavailable
- `unhealthy` - No providers available

**Example:**
```bash
curl http://localhost:8000/api/skills/health
```

---

## Skill-Specific Input Schemas

### Scene Analyzer

```json
{
  "scene_content": "string (required) - The scene text",
  "mode": "enum (optional, default: detailed) - detailed|quick|variant_comparison",
  "phase": "enum (optional, default: phase2) - phase1|phase2|phase3",
  "reference_files": "array[string] (optional) - Paths to reference files"
}
```

### Scene Enhancer

```json
{
  "scene_content": "string (required) - Original scene text",
  "fixes_to_apply": "array[object] (optional) - Specific fixes from analyzer",
  "enhancement_level": "enum (optional, default: standard) - minimal|standard|aggressive",
  "preserve_structure": "boolean (optional, default: true) - Keep original structure"
}
```

### Character Validator

```json
{
  "scene_content": "string (required) - Scene to validate",
  "character_bible": "object (required) - Character definition",
  "previous_scenes": "array[string] (optional) - Context scenes"
}
```

### Scene Writer

```json
{
  "scene_outline": "string (required) - Beat sheet or outline",
  "phase": "enum (required) - phase1|phase2|phase3",
  "context": "object (required) - Story context and previous scenes",
  "target_word_count": "integer (optional) - Desired length"
}
```

### Scene Multiplier

```json
{
  "scene_outline": "string (required) - Source outline",
  "variant_count": "integer (optional, default: 3) - Number of variants (3-5)",
  "variation_axis": "enum (required) - tone|pacing|focus|voice",
  "context": "object (required) - Story context"
}
```

### Scaffold Generator

```json
{
  "chapter_outline": "string (required) - Chapter-level outline",
  "scene_purpose": "string (required) - Why this scene exists",
  "story_context": "object (required) - Overall story info",
  "detail_level": "enum (optional, default: standard) - sparse|standard|rich"
}
```

---

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `SKILL_NOT_FOUND` | Skill doesn't exist in registry | Check skill name spelling |
| `SKILL_EXECUTION_ERROR` | Skill execution failed | Check input data format |
| `PROVIDER_UNAVAILABLE` | No providers available | Check provider health endpoint |
| `INVALID_INPUT` | Input validation failed | Review input schema |
| `AUTHENTICATION_REQUIRED` | Auth needed for premium skill | Upgrade tier or use fallback |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait and retry |

---

## Rate Limits

Currently no rate limits in local development.
In production:
- Standard tier: 100 requests/hour
- Premium tier: 1000 requests/hour

---

## Webhook Support

Not yet implemented. Coming in Phase B.

---

## Changelog

### Sprint 12 Phase A (2025-11-14)
- Initial release
- 4 core endpoints
- 6 Explants skills registered
- Native Python provider for Scene Analyzer

---

**Version:** 1.0.0
**Last Updated:** 2025-11-14
