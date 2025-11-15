"""
Category Templates - Define structure for 8 knowledge categories

Each template includes:
- Field definitions with queries for NotebookLM
- Required vs optional fields
- Prompt-if-empty flags for critical information
- Auto-populate flags for fields filled during writing

Categories:
1. Characters
2. Story_Structure
3. World_Building
4. Themes_and_Philosophy
5. Voice_and_Craft
6. Antagonism_and_Conflict
7. Key_Beats_and_Pacing
8. Research_and_Setting_Specifics
"""

from typing import Dict, List, Any


# ============================================================================
# 1. CHARACTER TEMPLATE
# ============================================================================

CHARACTER_TEMPLATE = {
    "name": "character_profile",
    "category": "Characters",
    "sections": [
        {
            "section": "Basic Information",
            "fields": [
                {
                    "name": "full_name",
                    "query": "What is {character_name}'s full name?",
                    "required": True,
                    "prompt_if_empty": False
                },
                {
                    "name": "role_in_story",
                    "query": "What is {character_name}'s role in the story? (protagonist, antagonist, supporting, etc.)",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "first_appearance",
                    "query": "When/where does {character_name} first appear?",
                    "required": False,
                    "auto_populate": True,
                    "note": "Will be auto-populated during writing"
                }
            ]
        },
        {
            "section": "Core Dimensions",
            "fields": [
                {
                    "name": "internal_conflicts",
                    "query": "What are {character_name}'s internal conflicts?",
                    "required": True,
                    "prompt_if_empty": True,
                    "examples": ["belief vs. reality", "duty vs. desire", "fear vs. courage"]
                },
                {
                    "name": "fears_and_insecurities",
                    "query": "What are {character_name}'s fears and insecurities?",
                    "required": False,
                    "prompt_if_empty": True
                },
                {
                    "name": "motivations_and_goals",
                    "query": "What motivates {character_name}? What are their goals?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "core_beliefs",
                    "query": "What does {character_name} believe about the world?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        },
        {
            "section": "Character Arc and Growth",
            "fields": [
                {
                    "name": "starting_state",
                    "query": "What is {character_name}'s starting state/situation?",
                    "required": False,
                    "prompt_if_empty": False
                },
                {
                    "name": "transformation",
                    "query": "How does {character_name} transform during the story?",
                    "required": False,
                    "auto_populate": True,
                    "note": "Will be tracked during writing"
                },
                {
                    "name": "ending_state",
                    "query": "What is {character_name}'s ending state?",
                    "required": False,
                    "auto_populate": True,
                    "note": "Will be filled as you write"
                }
            ]
        },
        {
            "section": "Relationships",
            "fields": [
                {
                    "name": "key_relationships",
                    "query": "What are {character_name}'s key relationships with other characters?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        }
    ]
}


# ============================================================================
# 2. STORY STRUCTURE TEMPLATE
# ============================================================================

STORY_STRUCTURE_TEMPLATE = {
    "name": "story_structure",
    "category": "Story_Structure",
    "sections": [
        {
            "section": "Core Story Elements",
            "fields": [
                {
                    "name": "premise",
                    "query": "What is the core premise of the story in one sentence?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "main_conflict",
                    "query": "What is the main conflict or central problem?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "stakes",
                    "query": "What are the stakes? What happens if the protagonist fails?",
                    "required": True,
                    "prompt_if_empty": True
                }
            ]
        },
        {
            "section": "Act Structure",
            "fields": [
                {
                    "name": "act_breakdown",
                    "query": "How is the story divided into acts? Describe the purpose of each act.",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                },
                {
                    "name": "key_turning_points",
                    "query": "What are the key turning points or plot twists?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        },
        {
            "section": "Resolution",
            "fields": [
                {
                    "name": "climax",
                    "query": "What is the climax of the story?",
                    "required": False,
                    "auto_populate": True
                },
                {
                    "name": "resolution",
                    "query": "How is the story resolved?",
                    "required": False,
                    "auto_populate": True
                }
            ]
        }
    ]
}


# ============================================================================
# 3. WORLD BUILDING TEMPLATE
# ============================================================================

WORLD_BUILDING_TEMPLATE = {
    "name": "world_building",
    "category": "World_Building",
    "sections": [
        {
            "section": "Setting Basics",
            "fields": [
                {
                    "name": "time_period",
                    "query": "When does the story take place? What is the time period?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "primary_locations",
                    "query": "What are the primary locations where the story takes place?",
                    "required": True,
                    "prompt_if_empty": True,
                    "format": "list"
                },
                {
                    "name": "world_type",
                    "query": "What type of world is this? (realistic, fantasy, sci-fi, alternate history, etc.)",
                    "required": True,
                    "prompt_if_empty": False
                }
            ]
        },
        {
            "section": "World Rules and Logic",
            "fields": [
                {
                    "name": "unique_rules",
                    "query": "What are the unique rules or logic of this world? (magic systems, technology, social rules, etc.)",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                },
                {
                    "name": "world_constraints",
                    "query": "What are the limitations or constraints in this world?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        },
        {
            "section": "Atmosphere and Tone",
            "fields": [
                {
                    "name": "atmosphere",
                    "query": "What is the atmosphere or mood of this world?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        }
    ]
}


# ============================================================================
# 4. THEMES AND PHILOSOPHY TEMPLATE
# ============================================================================

THEMES_PHILOSOPHY_TEMPLATE = {
    "name": "themes_philosophy",
    "category": "Themes_and_Philosophy",
    "sections": [
        {
            "section": "Core Themes",
            "fields": [
                {
                    "name": "primary_theme",
                    "query": "What is the primary theme or central idea of the story?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "secondary_themes",
                    "query": "What are the secondary themes explored in the story?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        },
        {
            "section": "Philosophical Questions",
            "fields": [
                {
                    "name": "central_questions",
                    "query": "What philosophical questions does the story explore?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        },
        {
            "section": "Symbolism",
            "fields": [
                {
                    "name": "symbols_and_metaphors",
                    "query": "What symbols or metaphors are used in the story?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        }
    ]
}


# ============================================================================
# 5. VOICE AND CRAFT TEMPLATE
# ============================================================================

VOICE_CRAFT_TEMPLATE = {
    "name": "voice_craft",
    "category": "Voice_and_Craft",
    "sections": [
        {
            "section": "Narrative Voice",
            "fields": [
                {
                    "name": "pov_style",
                    "query": "What is the point of view? (first person, third person limited, third person omniscient, etc.)",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "narrative_voice",
                    "query": "Describe the narrative voice and tone.",
                    "required": True,
                    "prompt_if_empty": True,
                    "examples": ["lyrical", "sparse", "conversational", "formal"]
                }
            ]
        },
        {
            "section": "Writing Style",
            "fields": [
                {
                    "name": "sentence_structure",
                    "query": "What is the typical sentence structure? (short/punchy, long/flowing, varied, etc.)",
                    "required": False,
                    "prompt_if_empty": False
                },
                {
                    "name": "prose_patterns",
                    "query": "What patterns characterize the prose? (metaphor-heavy, direct action, internal monologue, etc.)",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        }
    ]
}


# ============================================================================
# 6. ANTAGONISM AND CONFLICT TEMPLATE
# ============================================================================

ANTAGONISM_CONFLICT_TEMPLATE = {
    "name": "antagonism_conflict",
    "category": "Antagonism_and_Conflict",
    "sections": [
        {
            "section": "Primary Opposition",
            "fields": [
                {
                    "name": "primary_antagonist",
                    "query": "Who or what is the primary antagonist or opposing force?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "antagonist_motivation",
                    "query": "What motivates the antagonist? What do they want?",
                    "required": True,
                    "prompt_if_empty": True
                }
            ]
        },
        {
            "section": "Types of Conflict",
            "fields": [
                {
                    "name": "external_conflicts",
                    "query": "What are the external conflicts? (character vs. character, character vs. nature, etc.)",
                    "required": True,
                    "prompt_if_empty": False,
                    "format": "list"
                },
                {
                    "name": "internal_conflicts",
                    "query": "What are the internal conflicts? (character vs. self)",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        },
        {
            "section": "Tension Sources",
            "fields": [
                {
                    "name": "sources_of_tension",
                    "query": "What are the main sources of tension throughout the story?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                }
            ]
        }
    ]
}


# ============================================================================
# 7. KEY BEATS AND PACING TEMPLATE
# ============================================================================

KEY_BEATS_PACING_TEMPLATE = {
    "name": "beats_pacing",
    "category": "Key_Beats_and_Pacing",
    "sections": [
        {
            "section": "Story Beats",
            "fields": [
                {
                    "name": "inciting_incident",
                    "query": "What is the inciting incident that starts the story?",
                    "required": True,
                    "prompt_if_empty": True
                },
                {
                    "name": "key_plot_beats",
                    "query": "What are the key plot beats or major story moments?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list"
                },
                {
                    "name": "midpoint",
                    "query": "What happens at the midpoint of the story?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        },
        {
            "section": "Pacing Strategy",
            "fields": [
                {
                    "name": "pacing_approach",
                    "query": "What is the overall pacing approach? (fast-paced thriller, slow-burn mystery, etc.)",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        }
    ]
}


# ============================================================================
# 8. RESEARCH AND SETTING SPECIFICS TEMPLATE
# ============================================================================

RESEARCH_SETTING_TEMPLATE = {
    "name": "research_setting",
    "category": "Research_and_Setting_Specifics",
    "sections": [
        {
            "section": "Research Areas",
            "fields": [
                {
                    "name": "research_topics",
                    "query": "What topics require research for this story?",
                    "required": False,
                    "prompt_if_empty": False,
                    "format": "list",
                    "examples": ["historical period", "scientific concepts", "cultural practices"]
                }
            ]
        },
        {
            "section": "Specific Details",
            "fields": [
                {
                    "name": "historical_facts",
                    "query": "What historical facts or real-world details are important?",
                    "required": False,
                    "prompt_if_empty": False
                },
                {
                    "name": "technical_details",
                    "query": "What technical or specialized knowledge is needed?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        },
        {
            "section": "Accuracy Notes",
            "fields": [
                {
                    "name": "accuracy_requirements",
                    "query": "Where does the story need to be historically/technically accurate vs. where can it take creative liberties?",
                    "required": False,
                    "prompt_if_empty": False
                }
            ]
        }
    ]
}


# ============================================================================
# TEMPLATE REGISTRY
# ============================================================================

ALL_TEMPLATES = {
    "Characters": CHARACTER_TEMPLATE,
    "Story_Structure": STORY_STRUCTURE_TEMPLATE,
    "World_Building": WORLD_BUILDING_TEMPLATE,
    "Themes_and_Philosophy": THEMES_PHILOSOPHY_TEMPLATE,
    "Voice_and_Craft": VOICE_CRAFT_TEMPLATE,
    "Antagonism_and_Conflict": ANTAGONISM_CONFLICT_TEMPLATE,
    "Key_Beats_and_Pacing": KEY_BEATS_PACING_TEMPLATE,
    "Research_and_Setting_Specifics": RESEARCH_SETTING_TEMPLATE,
}


def get_template(category: str) -> Dict[str, Any]:
    """
    Get template for a category.

    Args:
        category: Category name

    Returns:
        Template dictionary
    """
    return ALL_TEMPLATES.get(category, {})


def get_all_categories() -> List[str]:
    """Get list of all category names."""
    return list(ALL_TEMPLATES.keys())


def get_required_fields(category: str) -> List[Dict[str, Any]]:
    """
    Get required fields for a category.

    Args:
        category: Category name

    Returns:
        List of required field definitions
    """
    template = get_template(category)
    required = []

    for section in template.get("sections", []):
        for field in section.get("fields", []):
            if field.get("required", False):
                required.append(field)

    return required


if __name__ == "__main__":
    # Test template access
    print("Available Categories:")
    for cat in get_all_categories():
        print(f"  - {cat}")

    print("\nCharacter Template Required Fields:")
    for field in get_required_fields("Characters"):
        print(f"  - {field['name']}: {field['query']}")
