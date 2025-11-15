"""Claude Skill Bridge for MCP Protocol.

This module provides a bridge between Writers Factory and Claude Skills,
allowing the application to call Claude Code's 6 Explants writing craft skills
via the MCP (Model Context Protocol) interface.

Sprint 12 - Task 12-01
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import subprocess
import json
import sys


class CostTier(Enum):
    """Cost tiers for skills."""
    FREE = "free"
    STANDARD = "standard"
    PREMIUM = "premium"


@dataclass
class SkillDefinition:
    """Metadata definition for a Claude Skill.

    Attributes:
        name: Full Claude Skill name (e.g., "explants-scene-analyzer-scorer")
        skill_id: Short identifier (e.g., "scene-analyzer")
        capability: Primary capability (analyze, enhance, generate, validate)
        version: Skill version
        description: Human-readable description
        requires_auth: Whether authentication is required
        cost_tier: Cost tier for this skill
        input_schema: Expected input format
        output_schema: Expected output format
    """
    name: str
    skill_id: str
    capability: str
    version: str = "1.0"
    description: str = ""
    requires_auth: bool = True
    cost_tier: CostTier = CostTier.PREMIUM
    input_schema: Dict[str, str] = field(default_factory=dict)
    output_schema: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "skill_id": self.skill_id,
            "capability": self.capability,
            "version": self.version,
            "description": self.description,
            "requires_auth": self.requires_auth,
            "cost_tier": self.cost_tier.value,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema
        }


class MCPSkillBridge:
    """Bridge to Claude Skills via MCP protocol.

    This class manages the connection to Claude Skills and provides methods
    to call them via the MCP protocol. It handles authentication, error handling,
    and fallback responses.
    """

    def __init__(self, user_tier: str = "standard"):
        """Initialize MCP Skill Bridge.

        Args:
            user_tier: User's subscription tier (standard, premium)
        """
        self.user_tier = user_tier
        self.skills_registry: Dict[str, SkillDefinition] = {}
        self._register_skills()

    def _register_skills(self):
        """Register all 6 Explants Claude Skills with metadata."""

        # 1. Scene Analyzer & Scorer
        self.skills_registry["scene-analyzer"] = SkillDefinition(
            name="explants-scene-analyzer-scorer",
            skill_id="scene-analyzer",
            capability="analyze",
            description="Analyzes scene quality using Explants craft standards. Scores voice authenticity, character consistency, metaphor discipline, anti-patterns, and phase appropriateness.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "scene_content": "string - The scene text to analyze",
                "mode": "enum[detailed|quick|variant_comparison] - Analysis depth",
                "reference_files": "array[string] - Optional reference documents"
            },
            output_schema={
                "total_score": "integer - Overall score (0-100)",
                "category_scores": "object - Breakdown by category",
                "quality_tier": "string - Professional/Competent/Needs Work",
                "fixes": "array[object] - Specific improvement suggestions"
            }
        )

        # 2. Scene Enhancer
        self.skills_registry["scene-enhancer"] = SkillDefinition(
            name="explants-scene-enhancement",
            skill_id="scene-enhancer",
            capability="enhance",
            description="Enhances scenes to meet Explants craft standards. Fixes voice issues, strengthens metaphors, eliminates anti-patterns, and ensures character consistency.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "scene_content": "string - Original scene text",
                "fixes_to_apply": "array[object] - Fixes from analyzer",
                "enhancement_level": "enum[minimal|standard|aggressive] - Enhancement intensity",
                "preserve_structure": "boolean - Keep original structure"
            },
            output_schema={
                "enhanced_scene": "string - Improved scene text",
                "changes_made": "array[string] - List of changes",
                "improvement_score": "integer - Quality improvement delta"
            }
        )

        # 3. Mickey Bardot Character Identity Validator
        self.skills_registry["character-validator"] = SkillDefinition(
            name="mickey-bardot-character-identity",
            skill_id="character-validator",
            capability="validate",
            description="Validates Mickey Bardot's character identity across scenes. Ensures psychological consistency, capability alignment, and relationship dynamics remain true to character bible.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "scene_content": "string - Scene to validate",
                "character_bible": "object - Mickey's character definition",
                "previous_scenes": "array[string] - Context scenes"
            },
            output_schema={
                "is_consistent": "boolean - Overall consistency check",
                "violations": "array[object] - Character breaks",
                "recommendations": "array[string] - Fixes to maintain identity"
            }
        )

        # 4. Mickey Scene Writer
        self.skills_registry["scene-writer"] = SkillDefinition(
            name="explants-mickey-scene-writer",
            skill_id="scene-writer",
            capability="generate",
            description="Generates complete scenes with Mickey Bardot as POV character. Follows Explants craft standards and maintains character consistency.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "scene_outline": "string - Beat sheet or outline",
                "phase": "enum[phase1|phase2|phase3] - Voice complexity",
                "context": "object - Story context and previous scenes",
                "target_word_count": "integer - Desired length"
            },
            output_schema={
                "scene_content": "string - Generated scene text",
                "word_count": "integer - Actual word count",
                "metadata": "object - Scene metadata (characters, setting, etc.)"
            }
        )

        # 5. Scene Multiplier (Variant Generator)
        self.skills_registry["scene-multiplier"] = SkillDefinition(
            name="explants-scene-multiplier",
            skill_id="scene-multiplier",
            capability="generate",
            description="Generates multiple variants of a scene for comparison. Creates 3-5 versions with different approaches while maintaining craft standards.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "scene_outline": "string - Source outline",
                "variant_count": "integer - Number of variants (3-5)",
                "variation_axis": "enum[tone|pacing|focus|voice] - What to vary",
                "context": "object - Story context"
            },
            output_schema={
                "variants": "array[object] - Generated scene variants",
                "comparison_matrix": "object - Quality comparison",
                "recommendation": "string - Which variant works best"
            }
        )

        # 6. Smart Scaffold Generator
        self.skills_registry["scaffold-generator"] = SkillDefinition(
            name="explants-smart-scaffold-generator",
            skill_id="scaffold-generator",
            capability="generate",
            description="Generates intelligent scene scaffolds (beat sheets with rich context). Creates detailed outlines that guide scene writing while preserving creative freedom.",
            cost_tier=CostTier.PREMIUM,
            input_schema={
                "chapter_outline": "string - Chapter-level outline",
                "scene_purpose": "string - Why this scene exists",
                "story_context": "object - Overall story info",
                "detail_level": "enum[sparse|standard|rich] - Scaffold density"
            },
            output_schema={
                "scaffold": "object - Detailed scene scaffold",
                "beats": "array[object] - Individual story beats",
                "technical_notes": "array[string] - Craft guidance"
            }
        )

    async def call_skill(
        self,
        skill_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Call a Claude Skill via MCP protocol.

        Args:
            skill_id: Short skill identifier (e.g., "scene-analyzer")
            input_data: Input data matching skill's input_schema
            context: Optional context data

        Returns:
            Skill response following MCP format:
            {
                "status": "success" | "error" | "fallback",
                "data": {...},  # Matches output_schema
                "metadata": {
                    "provider": "claude_skill",
                    "skill_name": str,
                    "execution_time_ms": int,
                    "cost_estimate": float
                },
                "error": {...}  # If status == "error"
            }
        """
        # Check if skill exists
        if skill_id not in self.skills_registry:
            return self._error_response(
                code="SKILL_NOT_FOUND",
                message=f"Skill '{skill_id}' not found in registry"
            )

        skill = self.skills_registry[skill_id]

        # Check entitlement
        if not self._check_entitlement(skill):
            return self._fallback_response(
                skill_id=skill_id,
                reason="User tier does not have access to this skill"
            )

        # Call the actual Claude Skill
        try:
            result = await self._call_claude_skill(skill, input_data, context)
            return result
        except Exception as e:
            return self._error_response(
                code="SKILL_EXECUTION_ERROR",
                message=str(e)
            )

    async def _call_claude_skill(
        self,
        skill: SkillDefinition,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Actually invoke the Claude Skill via MCP.

        This is a placeholder that would integrate with Claude Code's skill system.
        In production, this would use the MCP protocol to invoke skills.

        Args:
            skill: Skill definition
            input_data: Input data
            context: Optional context

        Returns:
            MCP-formatted response
        """
        # TODO: Actual MCP integration
        # For now, return a mock success response
        return {
            "status": "success",
            "data": {
                "message": f"Skill '{skill.name}' executed successfully (mock)",
                "input_received": input_data
            },
            "metadata": {
                "provider": "claude_skill",
                "skill_name": skill.name,
                "execution_time_ms": 0,
                "cost_estimate": 0.0
            }
        }

    def _check_entitlement(self, skill: SkillDefinition) -> bool:
        """Check if user has access to this skill.

        Args:
            skill: Skill to check

        Returns:
            True if user can access this skill
        """
        if skill.cost_tier == CostTier.FREE:
            return True
        elif skill.cost_tier == CostTier.STANDARD:
            return self.user_tier in ["standard", "premium"]
        elif skill.cost_tier == CostTier.PREMIUM:
            return self.user_tier == "premium"
        return False

    def _fallback_response(self, skill_id: str, reason: str) -> Dict[str, Any]:
        """Generate fallback response when skill unavailable.

        Args:
            skill_id: Skill that was requested
            reason: Why fallback is needed

        Returns:
            MCP-formatted fallback response
        """
        return {
            "status": "fallback",
            "data": {
                "message": f"Skill '{skill_id}' not available: {reason}",
                "fallback_suggestion": "Consider upgrading to premium tier or using native Python agent"
            },
            "metadata": {
                "provider": "fallback",
                "skill_name": skill_id,
                "reason": reason
            }
        }

    def _error_response(self, code: str, message: str) -> Dict[str, Any]:
        """Generate standardized error response.

        Args:
            code: Error code
            message: Error message

        Returns:
            MCP-formatted error response
        """
        return {
            "status": "error",
            "error": {
                "code": code,
                "message": message
            },
            "metadata": {
                "provider": "claude_skill_bridge"
            }
        }

    def list_skills(self) -> List[Dict[str, Any]]:
        """List all available skills with metadata.

        Returns:
            List of skill definitions as dictionaries
        """
        return [
            skill.to_dict()
            for skill in self.skills_registry.values()
        ]

    def get_skill_info(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Skill definition as dictionary, or None if not found
        """
        skill = self.skills_registry.get(skill_id)
        return skill.to_dict() if skill else None
