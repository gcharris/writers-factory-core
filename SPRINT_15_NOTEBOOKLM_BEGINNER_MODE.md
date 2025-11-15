# Sprint 15: NotebookLM-Based Beginner Mode

**Status:** Ready for implementation
**Priority:** CRITICAL - Required for January course
**Timeline:** 3 weeks (December 2025)
**Dependencies:** Sprint 14 (Project Setup Wizard) ✅ Complete

---

## Executive Summary

**The Problem:**
Sprint 14's Project Setup Wizard requires 2,500-5,000 words of existing fiction to analyze voice and generate custom skills. This blocks beginners who arrive with concept only (0 words).

**The Solution:**
Use **NotebookLM as the voice source** on Day 1, extracting voice from personal writing (emails, social media, diary) to generate "starter skills" before any fiction is written. Then upgrade to "novel skills" at 2,500 words.

**Why This Works:**
- ✅ Everyone has written SOMETHING (even if it's emails/tweets)
- ✅ Personal from Day 1 (not generic templates)
- ✅ Aligns with course structure (Day 1 = NotebookLM collection)
- ✅ Natural progression (starter → novel skills feels like leveling up)
- ✅ One unified system (not two separate code paths)

---

## User Journey: Beginner Path

### **Day 1 Morning: The NotebookLM Collection Party (2-3 hours)**

**Student arrives with:** Concept only, 0 words of fiction written

**Student uploads to NotebookLM:**
1. **Personal writing**
   - Social media posts (Twitter, LinkedIn, blog)
   - Email excerpts (personal voice, not business)
   - Text messages (casual, authentic)
   - Diary/journal entries

2. **Previous attempts**
   - Old story drafts (even if unfinished)
   - High school essays
   - Blog posts or articles
   - Creative writing exercises

3. **Influences & inspiration**
   - Favorite author excerpts
   - YouTube video transcripts (talks they love)
   - Podcast episode summaries
   - Saved articles/notes

4. **Ideas & research**
   - Genre research (worldbuilding, craft)
   - Character inspiration notes
   - Plot ideas from conversations

**Goal:** 5,000-10,000 words of THEIR voice (any format)

**Why this works:**
- No "blank page" anxiety
- Captures authentic voice (emails often MORE authentic than polished prose)
- Makes NotebookLM central (as intended in course design)
- Dual purpose: Ideas + Voice extraction

---

### **Day 1 Afternoon: Voice Extraction & Starter Skills (1 hour)**

**Writers Factory new flow:**

```
1. Student clicks "Create New Project"
   ↓
2. Onboarding wizard asks:
   "Do you have 3-5 fiction passages (500+ words each)?"

   [Yes - I have fiction] → Sprint 14 path (existing)
   [No - I'm starting fresh] → Beginner path (NEW)
   ↓
3. Beginner path:
   "Let's extract your voice from personal writing!"

   Enter NotebookLM URL: ___________
   Select genre: [Thriller ▼]

   [Analyze My Voice] ←
   ↓
4. Backend queries NotebookLM:
   - Extracts student's writing samples
   - Identifies: emails, social posts, diary, etc.
   - Runs voice analysis (casual/personal mode)
   ↓
5. Generates "Starter Voice Profile":
   Voice Name: "Casual Direct"
   Confidence: Medium
   Based on: emails, social media, diary entries

   Primary characteristics:
   • Direct, conversational tone
   • Short sentences (avg 12 words)
   • Modern vocabulary
   • Minimal metaphors (email style)
   ↓
6. Generates 6 Starter Skills:
   ✓ scene-analyzer-starter
   ✓ scene-writer-starter
   ✓ scene-enhancer-starter
   ✓ character-validator-starter
   ✓ scene-multiplier-starter
   ✓ scaffold-generator-starter
   ↓
7. Project created with starter mode:

   ┌────────────────────────────────────┐
   │  🎉 PROJECT CREATED!               │
   │                                    │
   │  Your starter skills are ready!    │
   │  Based on: emails & social media   │
   │                                    │
   │  Write 2,500 words to unlock      │
   │  NOVEL SKILLS (personalized for   │
   │  fiction writing)                  │
   │                                    │
   │  Current progress: 0 / 2,500      │
   │  ░░░░░░░░░░░░░░░░░░░░ 0%          │
   └────────────────────────────────────┘
```

**Time:** ~10 minutes (automated)

---

### **Days 1-3: Write with Starter Skills**

**Student writes first draft using:**
- Scene-writer-starter (generates from outlines)
- Scene-analyzer-starter (scores quality)
- Scene-enhancer-starter (improves prose)

**Progress tracking:**
```
┌────────────────────────────────────┐
│  YOUR PROGRESS                     │
│                                    │
│  Words written: 1,247 / 2,500     │
│  ████████████░░░░░░░░ 50%         │
│                                    │
│  🎯 1,253 words until Novel Skills!│
│                                    │
│  Current mode: Starter Skills      │
│  Voice based on: Your emails       │
│                                    │
│  Starter skills are good, but      │
│  Novel Skills will be tuned to     │
│  YOUR fiction voice!               │
└────────────────────────────────────┘
```

**Key differences from novel mode:**
- Lower confidence scores (expected)
- AI reminds: "These are starter skills"
- Prompts encourage hitting 2,500-word threshold
- Skills work but feel "generic-ish" (intentional)

---

### **Day 3-4: The Upgrade Moment** 🎉

**Automatic prompt at 2,500 words:**

```
┌──────────────────────────────────────────┐
│  🎉 CONGRATULATIONS!                     │
│                                          │
│  You've written 2,500 words of fiction! │
│                                          │
│  READY TO UNLOCK NOVEL SKILLS?           │
│                                          │
│  Your Starter Skills were based on      │
│  emails and social media (casual voice).│
│                                          │
│  Now let's analyze your FICTION voice   │
│  and generate TRUE custom skills!        │
│                                          │
│  This upgrade will:                      │
│  ✓ Analyze your 2,500 words of fiction │
│  ✓ Extract your novel-specific voice   │
│  ✓ Generate 6 novel-tuned skills        │
│  ✓ Unlock advanced features             │
│  ✓ Show you how your voice evolved      │
│                                          │
│  Time required: ~5 minutes               │
│                                          │
│  [Upgrade to Novel Skills Now!]          │
│  [I'll do this later]                    │
└──────────────────────────────────────────┘
```

**Student clicks "Upgrade":**

```
Analyzing your 2,500 words...
████████████████████░░ 90%

Extracting fiction voice patterns...
✓ Sentence structure (fiction mode)
✓ Metaphor usage (creative vs email)
✓ POV handling (deep 3rd vs casual)
✓ Dialogue patterns
✓ Narrative pacing

Generating Novel Skills...
✓ scene-analyzer (novel-tuned)
✓ scene-writer (novel-tuned)
✓ scene-enhancer (novel-tuned)
✓ character-validator (novel-tuned)
✓ scene-multiplier (novel-tuned)
✓ scaffold-generator (novel-tuned)

UPGRADE COMPLETE! 🎉
```

**Voice Evolution Comparison:**

```
┌──────────────────────────────────────────┐
│  YOUR VOICE EVOLUTION                    │
│                                          │
│  STARTER VOICE (from emails):            │
│  • Casual, conversational               │
│  • Short sentences (avg 12 words)       │
│  • Minimal metaphors                     │
│  • Modern slang                          │
│                                          │
│  NOVEL VOICE (from your fiction):        │
│  • Compressed, literary                  │
│  • Varied sentences (avg 18 words)      │
│  • Rich metaphors (tech domain)         │
│  • Formal vocabulary                     │
│                                          │
│  YOUR GROWTH:                            │
│  You've developed a distinct fiction    │
│  voice! Your starter skills helped you  │
│  find your style.                        │
│                                          │
│  Novel Skills are now active! 🚀         │
└──────────────────────────────────────────┘
```

---

### **Days 4-7: Full Power Mode**

**Student continues with:**
- Novel-tuned skills (better quality)
- Advanced features unlocked
- Higher confidence scores
- Personalized analysis

**Same experience as experienced writers from this point forward.**

---

## Technical Architecture

### **Component 1: NotebookLM Content Extractor**

**File:** `factory/integrations/notebooklm_voice_extractor.py`

```python
class NotebookLMVoiceExtractor:
    """Extract voice profile from NotebookLM sources."""

    def __init__(self, notebooklm_client: NotebookLMClient):
        self.client = notebooklm_client

    async def extract_personal_voice(
        self,
        notebook_url: str,
        min_words: int = 3000
    ) -> PersonalVoiceData:
        """
        Query NotebookLM for user's personal writing.

        Extracts from:
        - Email excerpts
        - Social media posts
        - Diary/journal entries
        - Blog posts
        - Text messages

        Returns structured data for voice analysis.
        """

    async def categorize_sources(
        self,
        sources: List[NotebookSource]
    ) -> Dict[str, List[str]]:
        """
        Categorize notebook sources by type:
        - personal_writing (emails, diary, social)
        - fiction_attempts (old drafts)
        - influences (favorite authors)
        - research (craft, genre)
        """

    async def extract_text_by_category(
        self,
        notebook_url: str,
        category: str
    ) -> List[str]:
        """Get all text from specific category."""
```

---

### **Component 2: Dual Voice Profile System**

**File:** `factory/core/dual_voice_profiles.py`

```python
@dataclass
class StarterVoiceProfile(VoiceProfile):
    """Voice profile from personal writing (emails, social media)."""

    confidence_level: str  # "low", "medium" (never "high")
    source_types: List[str]  # ["email", "social_media", "diary"]
    upgrade_threshold: int = 2500  # Words of fiction needed
    is_starter: bool = True

    # Same structure as VoiceProfile but with caveats
    voice_name: str  # e.g., "Casual Direct"
    primary_characteristics: List[str]
    sentence_structure: Dict[str, Any]
    # ... rest of VoiceProfile fields

    warnings: List[str] = field(default_factory=lambda: [
        "Based on casual writing, not fiction",
        "May differ from your fiction voice",
        "Upgrade at 2,500 words for better accuracy"
    ])


@dataclass
class NovelVoiceProfile(VoiceProfile):
    """Voice profile from fiction writing."""

    confidence_level: str  # Can be "high"
    fiction_word_count: int  # Words analyzed
    is_starter: bool = False

    # Comparison to starter (if upgraded)
    previous_starter: Optional[StarterVoiceProfile] = None
    voice_evolution: Optional[Dict[str, Any]] = None
    # e.g., {
    #   "sentence_length_change": "+6 words avg",
    #   "metaphor_increase": "+45%",
    #   "formality_shift": "casual → literary"
    # }
```

---

### **Component 3: Starter Skills Generator**

**File:** `factory/core/starter_skill_generator.py`

```python
class StarterSkillGenerator:
    """Generate skills from personal (non-fiction) voice."""

    async def generate_starter_skills(
        self,
        project_name: str,
        starter_voice: StarterVoiceProfile,
        genre: str
    ) -> Dict[str, GeneratedSkill]:
        """
        Generate 6 skills tuned to personal voice.

        Different from novel skills:
        - Lower confidence prompts
        - Broader acceptance criteria
        - Reminders about starter mode
        - Encouragement to upgrade
        """

        skills = {}

        for skill_type in SKILL_TYPES:
            skill = await self._generate_starter_skill(
                skill_type=skill_type,
                voice=starter_voice,
                genre=genre,
                is_starter=True  # Special flag
            )
            skills[skill_type] = skill

        return skills

    def _add_starter_caveats(self, skill_prompt: str) -> str:
        """Add reminders that this is starter mode."""
        return f"""
{skill_prompt}

---
**NOTE: This is a STARTER SKILL based on casual writing.**
As the writer develops their fiction voice, this skill will
be upgraded to a NOVEL SKILL at 2,500 words.

For now, focus on getting words on the page. The upgrade
will fine-tune analysis for fiction-specific voice.
---
"""
```

---

### **Component 4: Progress Tracking & Upgrade System**

**File:** `factory/core/progress_upgrade_system.py`

```python
class ProgressUpgradeSystem:
    """Monitor progress and trigger upgrades."""

    def __init__(self, session_manager: SessionManager):
        self.session = session_manager

    async def track_word_count(
        self,
        project_id: str,
        new_scene_words: int
    ) -> UpgradeStatus:
        """
        Track cumulative word count.
        Returns upgrade status when threshold hit.
        """
        project = await self.session.get_project(project_id)

        project.total_words += new_scene_words

        if (project.is_starter_mode and
            project.total_words >= project.upgrade_threshold):
            return UpgradeStatus(
                ready=True,
                words=project.total_words,
                threshold=project.upgrade_threshold,
                message="🎉 Ready to upgrade to Novel Skills!"
            )

        return UpgradeStatus(
            ready=False,
            words=project.total_words,
            threshold=project.upgrade_threshold,
            progress_pct=(project.total_words / project.upgrade_threshold) * 100
        )

    async def perform_upgrade(
        self,
        project_id: str
    ) -> UpgradeResult:
        """
        Upgrade from starter to novel skills.

        1. Extract all written scenes (2,500+ words)
        2. Run VoiceProfileExtractor in fiction mode
        3. Generate NovelVoiceProfile
        4. Generate 6 novel-tuned skills
        5. Compare starter vs novel voice
        6. Switch project to novel mode
        """
        project = await self.session.get_project(project_id)

        # Get all scenes
        scenes = await self.get_all_scenes(project_id)
        scene_text = "\n\n".join([s.content for s in scenes])

        # Analyze fiction voice
        extractor = VoiceProfileExtractor(self.anthropic_client)
        novel_voice = await extractor.extract_voice_profile(
            example_passages=[scene_text],
            uploaded_docs=[],
            notebooklm_context=None
        )

        # Compare to starter
        comparison = self._compare_voices(
            project.starter_voice,
            novel_voice
        )

        # Generate novel skills
        generator = SkillGenerator(self.anthropic_client)
        novel_skills = await generator.generate_project_skills(
            project_name=project.name,
            voice_profile=novel_voice,
            genre=project.genre,
            notebooklm_context=None
        )

        # Update project
        project.voice_profile = novel_voice
        project.skills = novel_skills
        project.is_starter_mode = False
        project.upgrade_date = datetime.now()

        await self.session.save_project(project)

        return UpgradeResult(
            success=True,
            novel_voice=novel_voice,
            comparison=comparison,
            message="Successfully upgraded to Novel Skills! 🎉"
        )
```

---

### **Component 5: Frontend Upgrade Wizard**

**File:** `webapp/frontend-v2/src/features/upgrade/UpgradeWizard.jsx`

```jsx
function UpgradeWizard({ projectId, wordCount, threshold }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isUpgrading, setIsUpgrading] = useState(false);
  const [result, setResult] = useState(null);

  // Auto-open when threshold reached
  useEffect(() => {
    if (wordCount >= threshold) {
      setIsOpen(true);
    }
  }, [wordCount, threshold]);

  const handleUpgrade = async () => {
    setIsUpgrading(true);

    try {
      const response = await fetch('/api/setup/upgrade-to-novel-skills', {
        method: 'POST',
        body: JSON.stringify({ projectId }),
      });

      const data = await response.json();
      setResult(data);

      // Celebrate!
      confetti();

    } catch (error) {
      // Handle error
    } finally {
      setIsUpgrading(false);
    }
  };

  return (
    <Dialog open={isOpen} maxWidth="md">
      <DialogTitle>
        🎉 Ready to Unlock Novel Skills!
      </DialogTitle>

      <DialogContent>
        <Typography>
          You've written {wordCount} words of fiction!
        </Typography>

        <Box sx={{ my: 2 }}>
          <Alert severity="info">
            Your Starter Skills were based on emails and
            social media (casual voice).

            Novel Skills will be tuned to YOUR fiction voice!
          </Alert>
        </Box>

        {/* Show what will happen */}
        <List>
          <ListItem>
            <ListItemIcon>✓</ListItemIcon>
            <ListItemText>
              Analyze your 2,500 words of fiction
            </ListItemText>
          </ListItem>
          {/* ... more items */}
        </List>

        {/* Show comparison if upgraded */}
        {result && (
          <VoiceComparisonDisplay
            starter={result.starterVoice}
            novel={result.novelVoice}
            evolution={result.evolution}
          />
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={() => setIsOpen(false)}>
          I'll do this later
        </Button>
        <Button
          variant="contained"
          onClick={handleUpgrade}
          disabled={isUpgrading}
        >
          {isUpgrading ? 'Upgrading...' : 'Upgrade Now!'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
```

---

## API Endpoints

### **New Endpoint: Analyze from NotebookLM**

```
POST /api/setup/analyze-from-notebooklm

Request:
{
  "notebooklmUrl": "https://notebooklm.google.com/notebook/...",
  "genre": "thriller",
  "minWords": 3000
}

Response:
{
  "starterVoice": {
    "voiceName": "Casual Direct",
    "confidenceLevel": "medium",
    "sourceTypes": ["email", "social_media", "diary"],
    "upgradeThreshold": 2500,
    // ... rest of VoiceProfile fields
  },
  "wordCount": 5247,
  "sourceBreakdown": {
    "email": 2100,
    "social_media": 1847,
    "diary": 1300
  }
}
```

---

### **New Endpoint: Upgrade to Novel Skills**

```
POST /api/setup/upgrade-to-novel-skills

Request:
{
  "projectId": "my-thriller"
}

Response:
{
  "success": true,
  "novelVoice": {
    "voiceName": "Compressed Thriller",
    "confidenceLevel": "high",
    "fictionWordCount": 2637,
    // ... rest of NovelVoiceProfile
  },
  "comparison": {
    "sentenceLengthChange": "+6 words average",
    "metaphorIncrease": "+45%",
    "formalityShift": "casual → literary",
    "improvements": [
      "Richer vocabulary in fiction",
      "More varied sentence structure",
      "Stronger metaphor discipline"
    ]
  },
  "skills": {
    "scene-analyzer": { ... },
    "scene-writer": { ... },
    // ... 6 novel-tuned skills
  },
  "message": "Successfully upgraded to Novel Skills! 🎉"
}
```

---

## Implementation Phases

### **Week 1: NotebookLM Voice Extraction**

**Tasks:**
1. Enhance NotebookLMClient to categorize sources
2. Build NotebookLMVoiceExtractor
3. Create StarterVoiceProfile dataclass
4. Add source type detection (email vs social vs diary)
5. Write tests with mock notebook data

**Deliverables:**
- Can extract 5,000+ words from NotebookLM
- Categorizes sources correctly
- Generates starter voice profile

---

### **Week 2: Starter Skills & Progress Tracking**

**Tasks:**
1. Build StarterSkillGenerator
2. Add starter mode flags to skills
3. Create ProgressUpgradeSystem
4. Build word count tracking
5. Implement upgrade detection logic
6. Add backend API endpoints

**Deliverables:**
- Generates 6 starter skills with caveats
- Tracks word count accurately
- Triggers upgrade prompt at 2,500 words
- API endpoints functional

---

### **Week 3: Upgrade Wizard & Voice Comparison**

**Tasks:**
1. Build UpgradeWizard React component
2. Create VoiceComparisonDisplay
3. Add upgrade animation/celebration
4. Build voice evolution analyzer
5. Write end-to-end tests
6. Polish UX and error handling

**Deliverables:**
- Complete upgrade flow working
- Voice comparison shows meaningful insights
- Smooth user experience
- Beginner can go from 0 words to novel skills

---

## Success Criteria

**Sprint 15 is complete when:**

1. **Beginner can start with 0 words** ✓
   - Upload personal writing to NotebookLM
   - Extract starter voice profile
   - Generate starter skills

2. **Progress tracking works** ✓
   - Word count updates in real-time
   - Progress bar shows path to upgrade
   - Threshold detection accurate

3. **Upgrade flow is smooth** ✓
   - Automatic prompt at 2,500 words
   - Upgrade completes in <5 minutes
   - Skills switch seamlessly

4. **Voice comparison is insightful** ✓
   - Shows meaningful evolution
   - Celebrates growth
   - Educates about voice development

5. **End-to-end test passes** ✓
   - New user → NotebookLM → starter skills → write 2,500 words → upgrade → novel skills
   - No errors, smooth experience

---

## Risk Mitigation

### **Risk 1: NotebookLM doesn't have enough personal writing**

**Mitigation:**
- Min threshold: 3,000 words
- Clear error: "Need at least 3,000 words of personal writing"
- Suggestions: "Add more emails, social posts, or diary entries"
- Fallback: Let them write 500 words in app first, use that + notebook

### **Risk 2: Personal voice very different from fiction voice**

**Mitigation:**
- This is EXPECTED and GOOD
- Starter skills are explicitly "training wheels"
- Upgrade comparison celebrates the evolution
- Lower expectations for starter mode

### **Risk 3: Students resist upgrading**

**Mitigation:**
- Make upgrade feel like achievement (confetti, celebration)
- Show side-by-side comparison (starter vs novel analysis)
- Auto-prompt (can't be ignored)
- Peer pressure (show who's upgraded in class)

---

## Testing Plan

### **Unit Tests**

```python
# test_notebooklm_voice_extraction.py
def test_extract_from_notebook():
    """Test extraction from mock NotebookLM data."""

def test_categorize_sources():
    """Test source type detection."""

def test_minimum_word_threshold():
    """Test error when < 3,000 words."""

# test_starter_skills.py
def test_generate_starter_skills():
    """Test skill generation with starter voice."""

def test_starter_caveats_added():
    """Test that skills include starter warnings."""

# test_progress_upgrade.py
def test_word_count_tracking():
    """Test accurate word count accumulation."""

def test_upgrade_detection():
    """Test threshold triggers upgrade prompt."""

def test_upgrade_process():
    """Test full upgrade from starter to novel."""
```

---

### **Integration Tests**

```python
# test_beginner_e2e.py
async def test_complete_beginner_flow():
    """
    End-to-end test:
    1. Create project from NotebookLM
    2. Generate starter skills
    3. Write 2,500 words
    4. Trigger upgrade
    5. Verify novel skills generated
    """
```

---

### **User Acceptance Testing**

**Recruit 5 beta testers:**
- 2 complete beginners (0 writing experience)
- 2 intermediate (some creative writing)
- 1 experienced (has published)

**Test scenario:**
1. Day 1: Upload personal writing to NotebookLM
2. Day 1: Generate starter skills
3. Days 1-3: Write 2,500 words using starter skills
4. Day 3: Upgrade to novel skills
5. Days 4-5: Continue with novel skills

**Success metrics:**
- All 5 complete the flow without blocking errors
- At least 4/5 successfully upgrade
- At least 3/5 report "starter skills felt personal"
- At least 4/5 report "upgrade felt like achievement"

---

## Course Integration

**Updated Day 1 (per course proposal):**

**Morning:**
1. Installation verification (1hr)
2. Multi-agent demo (1hr)
3. **NotebookLM Collection Party** (1hr) ← ENHANCED
   - Students upload personal writing
   - Goal: 5,000+ words for voice extraction

**Afternoon:**
4. **Voice Extraction & Starter Skills** (1hr) ← NEW
   - Run voice analysis on NotebookLM
   - Generate starter skills
   - Create project in starter mode

5. **First Drafting** (1hr) ← MODIFIED
   - Use starter skills to write first 500 words
   - See progress bar toward upgrade

**End of Day 1:**
- ✅ Every student has personalized starter skills
- ✅ Every student has written 500+ words
- ✅ Clear path to upgrade visible

---

## Next Steps After Sprint 15

**Potential Sprint 16: Advanced Beginner Features**
1. Collaborative projects (2-3 students share voice)
2. Genre-specific starter templates
3. Multi-language support
4. Voice evolution tracking over time
5. "Voice journal" - track growth across projects

---

## Conclusion

Sprint 15 solves the critical beginner problem by:
- ✅ Using NotebookLM as voice source (0 words fiction required)
- ✅ Generating personalized starter skills from personal writing
- ✅ Creating natural progression (starter → novel at 2,500 words)
- ✅ Aligning perfectly with January course structure
- ✅ Making Writers Factory accessible to ALL writers

**This is the missing piece that makes Writers Factory production-ready for beginners while maintaining full power for experienced writers.**

**Ready to implement!** 🚀
