"""
Sprint 14 Phase B: End-to-End Tests for Project Setup Wizard

Tests the complete wizard flow from voice analysis to project creation.
"""

import pytest
import asyncio
from pathlib import Path
import json
import sys

# Add factory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from factory.core.voice_extractor import VoiceProfileExtractor
from factory.core.skill_generator import SkillGenerator
from factory.core.project_creator import ProjectCreator
from factory.core.skill_orchestrator import SkillOrchestrator, SkillRequest


# Sample Passages for Testing

EXPLANTS_PASSAGE = """
Mickey Bardot leaned against the crumbling brick wall, eyes tracking the patrol drone's lazy arc across the Detroit skyline. Three seconds. That's all she'd have when the pattern reset.

"You're gambling again," Trace whispered from the shadows. His voice carried that familiar mix of concern and resignation—the sound of someone who'd already lost the bet but couldn't stop watching the cards fall.

She didn't answer. Words were currency, and she was saving hers for when they'd count. Instead, she pulled the scrambler from her jacket, fingers finding the activation stud by muscle memory alone. The device hummed to life, its interference pattern spreading like ripples on still water.

Two seconds.

The patrol drone's sensors flickered, wavered, went blind. Mickey moved. Not running—running drew attention—but flowing through the space between moments like smoke through a cracked window. Her augmented vision painted the world in sharp contrasts: threat markers in red, safe zones in blue, the quantum tunnel entrance a pulsing green beacon fifty meters ahead.

One second.

She reached the tunnel threshold as the scrambler died. Behind her, the drone's sensors came back online with an angry buzz, but she was already through, already gone, already calculating the next impossible move in a game where the house always won.

Except she'd learned to count cards in a way the house had never imagined.
"""

ROMANCE_PASSAGE = """
Eleanor had promised herself she wouldn't look at the door every time the little bell chimed. Yet here she was, Thursday afternoon at The Dusty Cover, pretending to organize the poetry section while her heart performed acrobatics at every customer entrance.

"That's the third time you've shelved Neruda between the self-help books," Maeve observed from behind the register, her knowing smile sharper than the espresso she was pulling.

Eleanor snatched the wayward volume, face warming. "I'm... distracted."

"Distracted by a certain architect who stops by every Thursday at 3:47 PM for his standing appointment with the travel section?"

"It's 3:52," Eleanor muttered, returning Neruda to his rightful home among the romantics. "He's late."

The bell chimed. Eleanor's hands fumbled the book.

"Right on schedule," Maeve murmured, because of course it was exactly 3:47—Eleanor's watch was five minutes fast, a hedge against her perpetual lateness that now betrayed her careful performance of nonchalance.

James Kirkland filled the doorway like he was measuring it for renovation, all clean lines and thoughtful proportions. His eyes found hers immediately, as they always did, and the corner of his mouth quirked up in that almost-smile that suggested he'd been keeping track of Thursdays too.

"The poetry section seems unusually active today," he said, moving toward her with the kind of measured patience that designed buildings to stand for centuries.

Eleanor's heart stumbled over its practiced rhythm. They were going to have to stop pretending the travel books were what brought him here.

Soon. Maybe next Thursday.

Or possibly, terrifyingly, today.
"""

THRILLER_PASSAGE = """
The photographs were wrong. That's what Detective Sarah Chen noticed first—not the blood spatter pattern, not the positioning of the body, but the small inconsistencies in the background details that most people would miss. The clock on the wall read 3:47. The coroner had estimated time of death at 8:00 PM.

"Someone staged this," she said, more to herself than to her partner.

Rodriguez looked up from his notes, skeptical. "You saying this isn't our guy?"

"I'm saying our guy wants us to think he was interrupted. Look at the victim's hand." She pointed to the outstretched fingers, positioned just shy of the panic button under the desk. "That's theatrical. People in genuine panic don't pose."

She pulled out her phone, photographing the scene from multiple angles. The killer had been careful—too careful. Every element designed to tell a story of interrupted violence, sudden flight. But stories had patterns, and patterns had tells.

The photograph of the wife on the desk faced away from where the victim had fallen. A small thing. Insignificant. Except Sarah had worked enough homicides to know: people in offices kept family photos positioned for their own viewing, not their visitors'.

Someone had turned that frame. Recently. Deliberately.

"Pull the security footage from the building across the street," she instructed Rodriguez. "And get me a list of everyone with after-hours access to this floor."

"You think it's someone who works here?"

"I think whoever killed Douglas Harper knew exactly where the cameras were, which means they either work here or they studied the layout." She crouched beside the body, examining the wound angle. "And they wanted us to believe they panicked."

The clock's second hand swept past 3:47. Still wrong. Still lying.

Still telling her exactly what she needed to know.
"""


class TestCompleteSetupFlow:
    """Test complete wizard flow from start to finish."""

    @pytest.mark.asyncio
    async def test_explants_project_creation(self):
        """
        Create The Explants project via wizard.

        Verifies:
        - Voice analysis extracts sci-fi/noir characteristics
        - Skills generated with compression + gambling metaphors
        - Project structure created correctly
        - Skills are functional
        """
        # Step 1: Analyze voice
        extractor = VoiceProfileExtractor()
        voice_profile = await extractor.extract_voice_profile(
            passages=[EXPLANTS_PASSAGE],
            genre="sci-fi"
        )

        assert voice_profile is not None
        assert voice_profile.voice_name is not None
        assert len(voice_profile.primary_characteristics) > 0

        # Verify sci-fi/noir characteristics
        characteristics_text = " ".join(voice_profile.primary_characteristics).lower()
        assert any(term in characteristics_text for term in ["compressed", "tight", "noir", "tense"])

        # Step 2: Generate skills
        generator = SkillGenerator()
        skills = await generator.generate_all_skills(
            project_name="test-explants",
            voice_profile=voice_profile,
            knowledge_context=""
        )

        assert len(skills) == 6
        assert "scene-analyzer" in skills
        assert "scene-enhancer" in skills
        assert "scene-writer" in skills

        # Step 3: Create project structure
        creator = ProjectCreator(base_projects_dir=Path("./test_projects"))
        project_path = await creator.create_project(
            project_name="test-explants",
            voice_profile=voice_profile,
            generated_skills=skills,
            genre="sci-fi",
            knowledge_context="Sci-fi noir set in Detroit"
        )

        assert project_path.exists()
        assert (project_path / ".claude" / "skills").exists()
        assert (project_path / "knowledge" / "craft").exists()
        assert (project_path / "config.json").exists()

        # Verify all 6 skills created
        skills_dir = project_path / ".claude" / "skills"
        skill_folders = list(skills_dir.iterdir())
        assert len(skill_folders) == 6

        # Step 4: Test skill execution
        orchestrator = SkillOrchestrator()
        orchestrator.register_project_skills("test-explants", skills)

        # Test analyzer skill
        request = SkillRequest(
            skill_name="scene-analyzer-test-explants",
            input_data={
                "scene_content": EXPLANTS_PASSAGE[:500],
                "mode": "detailed"
            },
            context={"project_id": "test-explants"}
        )

        result = await orchestrator.execute_skill(request, project_id="test-explants")
        assert result.success is True
        assert result.data is not None

        # Cleanup
        import shutil
        shutil.rmtree(project_path)

    @pytest.mark.asyncio
    async def test_romance_project_creation(self):
        """
        Create romance novel project.

        Verifies:
        - Different voice extracted (warm vs compressed)
        - Skills customized for romance conventions
        - Genre-specific quality criteria
        """
        # Step 1: Analyze voice
        extractor = VoiceProfileExtractor()
        voice_profile = await extractor.extract_voice_profile(
            passages=[ROMANCE_PASSAGE],
            genre="romance"
        )

        assert voice_profile is not None

        # Verify romance characteristics (different from sci-fi noir)
        characteristics_text = " ".join(voice_profile.primary_characteristics).lower()
        # Romance should have warmer, more emotional characteristics
        assert any(term in characteristics_text for term in ["warm", "emotional", "playful", "romantic", "tension"])

        # Step 2: Generate skills
        generator = SkillGenerator()
        skills = await generator.generate_all_skills(
            project_name="test-romance",
            voice_profile=voice_profile,
            knowledge_context="Contemporary romance"
        )

        assert len(skills) == 6

        # Verify skills are differentiated from sci-fi
        analyzer_skill = skills.get("scene-analyzer")
        assert analyzer_skill is not None
        # Romance analyzer should mention different criteria
        skill_content = analyzer_skill.skill_md.lower()
        assert any(term in skill_content for term in ["romance", "emotional", "tension", "relationship"])

        # Step 3: Create project
        creator = ProjectCreator(base_projects_dir=Path("./test_projects"))
        project_path = await creator.create_project(
            project_name="test-romance",
            voice_profile=voice_profile,
            generated_skills=skills,
            genre="romance",
            knowledge_context="Contemporary romance with witty banter"
        )

        assert project_path.exists()
        assert (project_path / ".claude" / "skills").exists()

        # Cleanup
        import shutil
        shutil.rmtree(project_path)

    @pytest.mark.asyncio
    async def test_thriller_project_minimal_inputs(self):
        """
        Create thriller project with minimal inputs.

        Verifies:
        - Wizard handles sparse data gracefully
        - No NotebookLM, no uploads still works
        - Default quality criteria generated
        """
        # Step 1: Analyze voice (minimal input)
        extractor = VoiceProfileExtractor()
        voice_profile = await extractor.extract_voice_profile(
            passages=[THRILLER_PASSAGE],
            genre="thriller"
        )

        assert voice_profile is not None
        assert len(voice_profile.primary_characteristics) > 0

        # Step 2: Generate skills (minimal context)
        generator = SkillGenerator()
        skills = await generator.generate_all_skills(
            project_name="test-thriller",
            voice_profile=voice_profile,
            knowledge_context=""  # Empty context
        )

        assert len(skills) == 6

        # Verify skills still functional with minimal data
        for skill_type, skill in skills.items():
            assert skill.skill_md is not None
            assert len(skill.skill_md) > 100  # Has substantial content

        # Step 3: Create project with minimal data
        creator = ProjectCreator(base_projects_dir=Path("./test_projects"))
        project_path = await creator.create_project(
            project_name="test-thriller",
            voice_profile=voice_profile,
            generated_skills=skills,
            genre="thriller",
            knowledge_context="",  # Empty
            uploaded_docs=[]  # No docs
        )

        assert project_path.exists()

        # Verify project created with defaults
        config_path = project_path / "config.json"
        assert config_path.exists()

        with open(config_path) as f:
            config = json.load(f)
            assert config["project_name"] == "test-thriller"
            assert config["genre"] == "thriller"

        # Cleanup
        import shutil
        shutil.rmtree(project_path)


class TestSkillDifferentiation:
    """Test that skills are correctly differentiated by genre/voice."""

    @pytest.mark.asyncio
    async def test_skills_reflect_voice_differences(self):
        """
        Verify that sci-fi and romance projects get different skills.
        """
        # Generate both profiles
        extractor = VoiceProfileExtractor()

        scifi_profile = await extractor.extract_voice_profile(
            passages=[EXPLANTS_PASSAGE],
            genre="sci-fi"
        )

        romance_profile = await extractor.extract_voice_profile(
            passages=[ROMANCE_PASSAGE],
            genre="romance"
        )

        # Generate skills for both
        generator = SkillGenerator()

        scifi_skills = await generator.generate_all_skills(
            project_name="scifi-test",
            voice_profile=scifi_profile,
            knowledge_context=""
        )

        romance_skills = await generator.generate_all_skills(
            project_name="romance-test",
            voice_profile=romance_profile,
            knowledge_context=""
        )

        # Compare analyzer skills
        scifi_analyzer = scifi_skills["scene-analyzer"].skill_md.lower()
        romance_analyzer = romance_skills["scene-analyzer"].skill_md.lower()

        # They should be different
        assert scifi_analyzer != romance_analyzer

        # Sci-fi should mention compression, noir, pacing
        assert any(term in scifi_analyzer for term in ["compressed", "noir", "tight", "pacing", "tension"])

        # Romance should mention emotion, relationship, chemistry
        assert any(term in romance_analyzer for term in ["emotional", "romance", "relationship", "chemistry", "tension"])


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_empty_passages(self):
        """Verify graceful handling of empty passages."""
        extractor = VoiceProfileExtractor()

        with pytest.raises(Exception):
            await extractor.extract_voice_profile(
                passages=[],
                genre="literary"
            )

    @pytest.mark.asyncio
    async def test_invalid_genre(self):
        """Verify handling of unusual genre."""
        extractor = VoiceProfileExtractor()

        # Should still work with unusual genre
        voice_profile = await extractor.extract_voice_profile(
            passages=[EXPLANTS_PASSAGE],
            genre="experimental-fusion"
        )

        assert voice_profile is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
