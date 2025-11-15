# Project Setup Wizard Guide

**Sprint 14 Phase B** - Complete guide to creating custom writing projects with AI-powered skills

---

## Overview

The Project Setup Wizard transforms Writers Factory from a single-project tool into a platform that works for ANY writer's unique voice and genre. In 6 simple steps, you'll create a custom writing environment with AI skills tuned specifically to YOUR writing style.

### What You'll Get

After completing the wizard, you'll have:

- **6 Custom AI Skills** - Scene analyzer, enhancer, character validator, writer, multiplier, and scaffold generator
- **Voice-Specific Prompts** - Each skill understands YOUR writing patterns, not generic templates
- **Quality Criteria** - 100-point scoring system calibrated to YOUR voice and genre
- **Project Structure** - Organized workspace with knowledge base, scenes directory, and references

---

## Quick Start

### Launch the Wizard

```bash
# Start Writers Factory
cd writers-factory-core
npm run dev

# Navigate to "Create New Project" in the UI
# or visit: http://localhost:5173/setup
```

### What You'll Need

**Required:**
- Project name (e.g., "the-explants", "my-romance-novel")
- Genre selection
- 3-5 example passages (500-1000 words each) that represent your voice

**Optional:**
- NotebookLM notebook URLs (for story knowledge extraction)
- Reference materials (style guides, character sheets, world bibles)
- Anti-patterns or style rules to avoid

**Time Required:** 10-15 minutes total
- 5 minutes: Input gathering
- 5-10 minutes: AI analysis & skill generation (automated)

---

## Step-by-Step Walkthrough

### Step 1: Project Details (1 minute)

![Step 1: Project Details]

**What to Enter:**

1. **Project Name**
   - Use lowercase with dashes: `my-novel-project`
   - Examples: `the-explants`, `midnight-chronicles`, `hearts-collide`
   - This becomes your project folder name

2. **Genre**
   - Select from: Literary, Thriller, Romance, Sci-Fi, Fantasy, Mystery, Horror, Historical, Other
   - Helps calibrate quality criteria and metaphor analysis

3. **Project Goals** (optional)
   - Describe what you want to achieve
   - Example: "Complete 80,000-word literary thriller with tight noir voice"

**Tips:**
- Choose a descriptive project name—you'll reference it often
- Genre affects quality scoring: romance prioritizes emotional beats, thriller focuses on pacing

---

### Step 2: Voice Input (3-5 minutes)

![Step 2: Voice Input]

**What to Provide:**

#### Example Passages (3-5 required)

Paste 500-1000 word excerpts that represent your writing voice. These will be analyzed for:
- Sentence structure (length, compression, variety)
- Vocabulary patterns (formality, complexity)
- POV style (depth, filter words, consciousness mode)
- Metaphor domains (gambling, nature, tech, etc.)
- Dialogue rhythms

**Best Practices:**

✅ **Do:**
- Use passages YOU wrote (not examples from published authors)
- Include variety: dialogue, action, description, introspection
- Choose passages you're proud of—these set the standard
- Include 3-5 passages (more data = better analysis)

❌ **Don't:**
- Use first drafts (unedited work can skew analysis)
- Mix multiple authors' styles
- Use passages shorter than 500 words (insufficient data)

**Example Selection:**
```
Passage 1: Character introspection + dialogue (800 words)
Passage 2: Action scene (600 words)
Passage 3: World-building description (700 words)
Passage 4: Emotional climax (650 words)
```

#### NotebookLM URLs (optional)

If you use Google's NotebookLM for story knowledge:
- Paste notebook URLs: `https://notebooklm.google.com/notebook/abc123...`
- The wizard will extract character/world/plot knowledge
- Powers the "scene-writer" skill with story-aware scaffolding

**Why This Helps:**
NotebookLM integration lets skills reference your characters, settings, and plot threads when analyzing or generating scenes.

---

### Step 3: Reference Materials (2 minutes, optional)

![Step 3: Reference Materials]

**What to Upload:**

#### Documents (optional)
- **Style Guides**: Your voice rules (e.g., "avoid adverbs", "short sentences")
- **Character Sheets**: Profiles for consistency checking
- **World Bible**: Setting details for scene validation

**Supported Formats:** .txt, .md, .pdf, .docx (up to 10MB each)

#### Style Guide / Anti-Patterns (optional)

Paste rules to avoid or enforce:

```
Examples:

"Avoid filter words: felt, seemed, appeared"
"Use show-don't-tell for emotions"
"Dialogue should sound natural, not exposition-heavy"
"Metaphors limited to gambling/card domains (20% max)"
"Compress to 60-70% of typical literary prose"
```

**How It's Used:**
- Scene analyzer will penalize violations of these rules
- Scene enhancer will make surgical fixes to match guidelines
- Anti-patterns stored in `.claude/skills/*/references/anti-patterns.md`

---

### Step 4: AI Analysis (2-3 minutes, automated)

![Step 4: AI Analysis]

**What Happens:**

The wizard uses Claude Sonnet 4.5 to analyze your passages and extract:

1. **Voice Name**: Generated label for your style (e.g., "Mickey Bardot Compressed Noir")

2. **Primary Characteristics**: 5-7 defining traits
   - Example (Sci-Fi Noir): "Compressed sentence structure", "Economical dialogue", "Noir metaphors"
   - Example (Romance): "Warm emotional tone", "Playful dialogue", "Layered subtext"

3. **Sentence Structure**:
   - Average length: 12-18 words (literary), 8-12 (compressed)
   - Compression level: 60-70% (tight), 90-100% (expansive)
   - Variety: High/medium/low

4. **POV Style**:
   - Depth: Surface/deep/psychic
   - Consciousness mode: 30-40% (filtered), 70-80% (immersive)
   - Filter word patterns

5. **Metaphor Domains**:
   - Identified domains (gambling, nature, tech, warfare, etc.)
   - Usage percentages (gambling: 20%, nature: 10%)
   - Keyword lists for each domain

**What You See:**

While analyzing, you'll see: "Analyzing your voice... (1-2 minutes)"

When complete, the wizard displays:
- Voice profile card with all extracted characteristics
- Metaphor domain breakdown with percentages
- Sentence structure metrics
- POV depth analysis

**Review Carefully:**
This profile determines how your skills will analyze and generate text. If it misunderstood your voice, go back and refine your example passages.

---

### Step 5: Review & Test (2-3 minutes, automated + optional test)

![Step 5: Review & Test]

**What Happens:**

The wizard generates your 6 custom skills:

1. **scene-analyzer-[your-project]**
   - Scores scenes 0-100 based on YOUR voice characteristics
   - Detailed breakdown: Voice (30pts), Character (20pts), Craft (30pts), Impact (20pts)

2. **scene-enhancer-[your-project]**
   - Makes surgical fixes to match your voice
   - Preserves structure while adjusting compression, metaphors, POV depth

3. **character-validator-[your-project]**
   - Checks character consistency (voice, behavior, knowledge)
   - Cross-references with NotebookLM character data if available

4. **scene-writer-[your-project]**
   - Writes NEW scenes in your voice
   - Uses story knowledge from NotebookLM
   - Follows your quality criteria

5. **scene-multiplier-[your-project]**
   - Creates 5 variations of a scene using verbalized sampling
   - Explores different creative choices while maintaining voice

6. **scaffold-generator-[your-project]**
   - Transforms minimal outlines into detailed scene scaffolds
   - Includes story context, character states, tension levels

**Test Your Analyzer (Optional):**

Paste a scene from your manuscript and click "Test Analyzer" to see:
- Overall score (0-100)
- Quality tier (Excellent/Good/Needs Work/Weak)
- Category scores (Voice, Character, Craft, Impact)
- Specific feedback

**Example Test Output:**
```
Overall Score: 87/100 (Excellent)
Quality Tier: Excellent

Category Scores:
- Voice Authenticity: 27/30
- Character Consistency: 18/20
- Scene Craft: 26/30
- Emotional Impact: 16/20

Analysis: "Strong compressed voice with effective gambling metaphors.
Minor inconsistency in dialogue rhythm. Consider tightening final paragraph."
```

---

### Step 6: Finalize (30 seconds)

![Step 6: Finalize]

**What You See:**

Summary of your project:
- Project name
- Genre
- Number of voice passages
- Custom skills generated
- NotebookLM integration status

**What Will Be Created:**

```
projects/your-project-name/
├── .claude/
│   └── skills/
│       ├── scene-analyzer-your-project/
│       │   ├── SKILL.md (custom prompt)
│       │   └── references/
│       │       ├── voice-profile.md
│       │       ├── anti-patterns.md
│       │       ├── quality-criteria.md
│       │       └── metaphor-domains.md
│       ├── scene-enhancer-your-project/
│       ├── character-validator-your-project/
│       ├── scene-writer-your-project/
│       ├── scene-multiplier-your-project/
│       └── scaffold-generator-your-project/
├── knowledge/
│   └── craft/
│       ├── voice-gold-standard.md
│       └── story-context.md (if NotebookLM used)
├── scenes/
│   └── (your manuscript goes here)
├── references/
│   └── (uploaded docs saved here)
├── config.json (project metadata)
└── README.md (usage guide)
```

**Click "Create Project":**

The wizard will:
1. Create directory structure
2. Save all 6 skills with references
3. Generate knowledge base
4. Register skills with the orchestrator

**Success:** You'll see "Project created successfully!" with a link to your project dashboard.

---

## Using Your Custom Skills

### Access via UI

1. **Select Your Project**: Choose from project dropdown in navbar
2. **Navigate to Craft Panel**: Use skills on any scene
3. **Select Skill**: Dropdown shows your project-specific skills first

### Access via CLI

```bash
# Analyze a scene
claude-skill execute scene-analyzer-your-project \
  --scene "path/to/scene.md" \
  --mode detailed

# Enhance a scene
claude-skill execute scene-enhancer-your-project \
  --scene "path/to/scene.md" \
  --output "enhanced.md"
```

### What's Different from Generic Skills

**Before (Generic Skills):**
- ❌ One-size-fits-all quality criteria
- ❌ Can't recognize your unique voice patterns
- ❌ Generic metaphor analysis
- ❌ No awareness of YOUR characters/world

**After (Custom Skills):**
- ✅ Quality criteria tuned to YOUR voice and genre
- ✅ Recognizes compressed vs expansive sentence styles
- ✅ Tracks your specific metaphor domains (gambling, tech, nature)
- ✅ References YOUR characters and world (if NotebookLM integrated)
- ✅ Enforces YOUR anti-patterns and style rules

---

## Troubleshooting

### Issue: Voice Analysis Failed

**Symptoms:** "Voice analysis failed" error in Step 4

**Solutions:**
1. Check that passages are 500+ words each
2. Ensure at least 3 passages provided
3. Verify passages are plain text (no formatting issues)
4. Try removing very short or unusual passages

### Issue: Skills Don't Match My Voice

**Symptoms:** Analyzer scores feel off, enhancer changes too much

**Solutions:**
1. **Refine Example Passages**: Go back to Step 2, use better examples
2. **Add Style Guide**: In Step 3, explicitly list voice rules
3. **Check Genre**: Literary vs Thriller affects quality criteria significantly
4. **Add More Passages**: 5 passages > 3 passages for accuracy

### Issue: NotebookLM Integration Not Working

**Symptoms:** Story context empty, skills don't reference characters

**Solutions:**
1. Verify NotebookLM URLs are correct format
2. Check that notebooks are shared/accessible
3. Ensure NotebookLM API credentials configured
4. Try skipping NotebookLM and manually adding knowledge to `knowledge/craft/story-context.md`

### Issue: Test Analyzer Gives Unexpected Scores

**Symptoms:** Good scenes score low, weak scenes score high

**Solutions:**
1. Test analyzer needs 200+ words to be accurate
2. Check that test scene matches your voice (not a different style)
3. Review extracted voice profile—may need better example passages
4. Adjust quality criteria in `.claude/skills/scene-analyzer-*/references/quality-criteria.md`

---

## Advanced Tips

### Optimizing Voice Extraction

**For Compressed Styles (Noir, Thriller):**
- Include scenes with tight action and crisp dialogue
- Avoid passages with excessive description
- Highlight metaphor usage in examples

**For Expansive Styles (Literary, Historical):**
- Include rich descriptive passages
- Show layered subtext and introspection
- Demonstrate sentence variety

### Customizing Skills After Creation

All skills can be manually edited:

1. Navigate to `.claude/skills/SKILL_NAME/SKILL.md`
2. Edit the prompt as needed
3. Skills use updated prompts immediately (no regeneration needed)

**Common Customizations:**
- Adjust scoring weights in analyzer
- Add specific fix patterns to enhancer
- Update character list in validator
- Refine story beats for writer

### Multi-Project Workflow

You can create multiple projects with different voices:

```
projects/
├── the-explants/          (sci-fi noir, compressed)
├── midnight-hearts/       (romance, warm & witty)
└── detective-chronicles/  (thriller, fast-paced)
```

Each project maintains its own:
- Custom skills
- Voice profile
- Quality criteria
- Knowledge base

Switch between projects in the UI dropdown—skills auto-route correctly.

---

## FAQ

**Q: Can I change my voice profile later?**
A: Yes. Re-run the wizard with new passages, or manually edit `knowledge/craft/voice-gold-standard.md`

**Q: How many projects can I create?**
A: Unlimited. Each project is independent.

**Q: Can I share my project with other writers?**
A: Yes! The entire `projects/your-project/` directory is portable. Just copy it.

**Q: What if I'm writing in a genre not listed?**
A: Choose "Other" and the wizard will adapt. Quality criteria will be more generic.

**Q: Can I use multiple authors' voices?**
A: Not recommended. Create separate projects for each voice/style.

**Q: Is NotebookLM required?**
A: No! It's optional. Skills work fine without it (just less story-aware).

**Q: Can I regenerate skills without starting over?**
A: Yes, but currently requires command-line tools. UI feature coming soon.

---

## Next Steps

### After Setup

1. **Analyze Your Manuscript**: Run analyzer on existing scenes to get baseline scores
2. **Enhance Weak Scenes**: Use enhancer to improve low-scoring sections
3. **Generate New Content**: Try scene-writer with outlines
4. **Experiment with Variations**: Use scene-multiplier to explore creative options

### Further Reading

- [Skill System Architecture](./ARCHITECTURE.md)
- [Voice Profile Deep Dive](./voice-profile-guide.md)
- [Advanced Skill Customization](./skill-customization.md)
- [NotebookLM Integration Guide](./notebooklm-integration.md)

---

## Support

**Found a bug?** Open an issue: https://github.com/gcharris/writers-factory-core/issues

**Have questions?** Check the docs: [Writers Factory Documentation](../README.md)

**Want to contribute?** See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Happy writing! Your custom AI writing environment is ready.** 🚀✍️
