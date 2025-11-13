# Task: Design Creation Wizard Pipeline for Writers Factory

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 6-8 hours
**Dependencies**: UX Design task (can work in parallel)

---

## Context

You are designing a guided wizard to take a writer from "blank canvas" to "ready to write" - essentially building a complete story bible through an intelligent, conversational AI process.

This wizard is **optional** but highly valuable for writers starting fresh. It should embody best practices from successful novelists and editors, making expert writing knowledge accessible to beginners.

---

## Source Material

### Primary Reference: NotebookLM Notebook on Writing Bestsellers

**URL**: https://notebooklm.google.com/notebook/8b1f262a-fe2a-45f3-8c3b-39689c9d3123

This notebook contains distilled advice from:
- Save the Cat! (Blake Snyder) - 15-beat structure
- Story Genius (Lisa Cron) - Character-first narrative
- Multiple bestselling authors on craft
- Editors on what makes manuscripts publishable

**Key Principles to Embed:**

1. **3-Phase Approach**
   - Phase 1: Foundational Preparation (mindset, commitment, audience)
   - Phase 2: Deep Character & Narrative Construction
   - Phase 3: Execution & Sustained Improvement

2. **Character-First Philosophy**
   - Readers enter stories through protagonist
   - Must be 3-dimensional with contradictions
   - Supporting cast serves protagonist's journey

3. **Structure Matters**
   - Even "pantsers" benefit from framework
   - Save the Cat! 15 beats proven in bestsellers
   - Pacing and stakes must escalate

4. **Serve the Audience**
   - Write what readers want, not just what you want
   - Understand genre conventions
   - Create participation (show don't tell)

5. **Layered Storytelling**
   - Surface narrative (plot events)
   - Symbolic layer (objects as meaning)
   - Allegorical depth (philosophical themes)

---

## Wizard Structure

The wizard should be **conversational**, not form-like. The AI asks questions, analyzes responses, provides relevant expert advice, and adapts based on what the writer says.

### Phase 1: Foundation (15-25 questions, ~25 minutes)

**Goal**: Establish core concept, genre, theme, and mindset

**Visual Progress Indicator**: 🏃 Marathon Runner (shows training progress)
- Phase 1: Stretching & Warm-up
- Phase 2: Building Stamina
- Phase 3: Distance Training
- Phase 4: Fine-tuning Form
- Phase 5: Race Strategy

#### 1.1 Mindset & Commitment Assessment

```
WIZARD: "Let's start at the beginning. Writing a novel is like training for a
marathon - it requires preparation, stamina, and deep commitment.

Why do you want to write this novel?"

[AI analyzes response for:]
- Passion vs. external validation
- Deep commitment vs. casual interest
- Clarity of purpose

[If response shows weak commitment:]
WIZARD: "I hear some hesitation. Remember, success isn't guaranteed, and
writing a novel is a marathon. Lisa Cron says you must love the *process*
itself, not just the idea of being called a 'writer.'

Are you ready to commit to the messy, difficult, rewarding journey?"
```

**Questions:**
1. Why are you writing this novel?

2. **[NEW] Cognitive Fitness Check**: "Have you successfully completed a 50,000+ word
   project before? If not, consider building your 'concentration stamina' with
   shorter projects first - like training cardiovascular fitness before a marathon."

3. Who is your target audience? (age, gender, interests)

4. Are you writing for the audience or for yourself? (both is okay, but must prioritize audience)

5. **[BRANCHING] Fiction or non-fiction?**
   - If Fiction → Continue to Q6
   - If Non-Fiction → Branch to 1.1.5

6. What genre is this? (provides context for expectations)

7. Have you written creatively before? (adjusts wizard depth)

#### 1.1.5 Non-Fiction Branch (Skip if fiction)

```
WIZARD: "Great! Non-fiction requires three essential components: excellent
communication, deep subject knowledge ('head knowledge'), and emotional
conviction ('heart knowledge'). Let's make sure you have all three."
```

**Additional Questions for Non-Fiction:**

**Q5a**: "Beyond communicating well, how will you demonstrate **deep knowledge
of your subject matter**? What expertise, research, or credentials do you bring?"

**Q5b**: "What is your **deep emotional conviction** about this topic? What
personal experience or passion makes you the right person to write this?"

**Q5c**: "How will you balance credible sources (head) with compelling emotion
(heart) to avoid being purely academic OR purely opinionated?"

```
WIZARD: "Perfect. Non-fiction that combines research credibility with authentic
passion becomes both believable and moving. Let's continue building your foundation."
```

[Resume at Q6 for genre-specific conventions]

#### 1.2 High Concept Development

```
WIZARD: "Great! Now let's crystallize your concept. Can you describe your
story in one sentence - the 'logline'?"

[AI evaluates logline for:]
- Protagonist present
- Clear goal/stakes
- Unique hook
- Compelling conflict

[If weak:]
WIZARD: "That's a start. Try this formula:
'When [INCITING INCIDENT], a [FLAWED PROTAGONIST] must [GOAL]
or else [STAKES].'

For example: 'When her daughter is kidnapped, a guilt-ridden former spy
must infiltrate the criminal network she once led, or lose her child forever.'"
```

**Questions:**
6. Describe your story in one sentence (logline)
7. What 2-3 published books is this similar to? ("It's X meets Y")
8. What makes your story unique? (the hook)
9. Why will readers care about this protagonist?
10. What's the emotional experience you want readers to have? (thrilled, heartbroken, inspired, terrified)

#### 1.3 Theme Identification

```
WIZARD: "Stories that resonate have something to *say*. What life lesson
will your protagonist learn by the end?"

[AI helps extract theme from response]

WIZARD: "Excellent. That theme - 'redemption requires facing your past' -
will be your North Star. In Save the Cat!, this becomes the 'Theme Stated'
beat around 5% into your novel. A character (often not the hero) will
hint at this truth early, but your protagonist won't understand it until
the end."
```

**Questions:**
11. What life lesson will your protagonist learn?

12. **[NEW]** "What unique life experience or specialized knowledge do *you*
    possess that is essential to telling this story? Why are *you* the right
    person to write this?" (Ensures authentic voice and unique perspective)

13. What question does your story ask? (e.g., "Can love survive betrayal?")

14. What do you want readers to think about after finishing?

15. Is there a social/philosophical issue you're exploring?

16. Complete this: "This is a story about ___________" (theme in one word/phrase)

```
WIZARD: "Remember: You must have something you *must* say, not just something
you *want* to say. Go do interesting things. Read widely. Experience life.
The best stories come from writers who have lived enough to have a genuine
perspective worth sharing."
```

---

### Phase 2: Deep Character Construction (30-40 questions, ~40 minutes)

**Goal**: Create dimensional protagonist and supporting cast using expert techniques

#### 2.1 True Character vs. Characterization

```
WIZARD: "Let's build your protagonist from the inside out. First, forget
appearance and mannerisms. Who are they at their CORE?

McKee distinguishes between:
- TRUE CHARACTER: Who they are at heart (loyal, ambitious, fearful, honest)
- CHARACTERIZATION: Observable qualities (tall, stutters, always late)

We need both, but True Character comes first."
```

**Questions:**
17. What 3-4 words describe your protagonist's true character? (core traits)

18. Now describe observable qualities: appearance, speech, mannerisms

19. **[NEW - AUTHENTICITY CHECK]** "Does this character's voice and manner reflect
    *YOUR* authentic view of the world, or are you modeling them on another
    fictional character you've read?

    ⚠️ WARNING: The biggest mistake aspiring authors make is trying to sound like
    OTHER AUTHORS instead of themselves. Readers can see right through a fraud.
    Sound like YOURSELF."

20. Where's the **contradiction**? (This creates dimension)
    - Internal contradiction: (e.g., "ambitious but guilt-ridden")
    - True Character vs. Characterization: (e.g., "deeply lonely but always smiling")

```
WIZARD: "Perfect! That contradiction - 'fiercely independent but desperate
for validation' - makes them dimensional. Readers will feel the tension.

[Optional] Would you like to use the 'Find Your Voice' tool to test whether
this character sounds authentically like YOU? This tool generates sample
dialogue/narration and helps you discover your natural voice."
```

#### 2.1.5 Find Your Voice Tool (Optional)

```
WIZARD: "Let's make sure this character voice is authentically YOURS. I'm going
to generate 3 short writing samples in different styles. Tell me which feels
most natural - or if none of them do, we'll iterate until we find YOUR voice."

[AI generates 3 variations of a scene with this character:]
- Sample A: More literary/poetic
- Sample B: More direct/compressed
- Sample C: More descriptive/expansive

USER: [Selects one or asks for more variations]

WIZARD: "Great! You're drawn to [STYLE]. Let's remember that - your narration
should sound like this, not like someone else's novel. This is YOUR voice."
```

**Links to Model Comparison Tool**: This "Find Your Voice" exercise uses the same
underlying technology as the Model Comparison Tool, but focuses on style/voice
discovery rather than model selection.

#### 2.2 Character Flaw & Growth

**Questions:**
19. What is your protagonist's fatal flaw? (the weakness that hurts them/others)
20. How has this flaw harmed them in the past?
21. How will this flaw make the story's central conflict worse?
22. What mistaken belief drives this flaw? (e.g., "I must control everything or I'll fail")
23. What truth must they learn to overcome it? (links to theme)

#### 2.3 Character Preparation Exercises

```
WIZARD: "Now we're going to go deep. I'm going to give you transformational
writing prompts to help you BECOME this character.

Lisa Cron recommends journaling AS your character to achieve authenticity.
Don't skip this - it's the difference between stick figures and fully
realized humans."
```

**Prompts:**

1. **Daily Routine Journal**
   ```
   Write a first-person journal entry as [CHARACTER] describing an ordinary
   day BEFORE the story begins. Include:
   - Morning routine (what do they eat, how do they prepare for the day?)
   - Work/daily activities
   - Evening wind-down
   - What they think about as they fall asleep

   ⭐ IMPORTANT: Don't skip mundane details! What's on their desk? What do they
   have for breakfast? What are the main subjects of conversation? Years later,
   these 'mundane' details often become the most fascinating and useful elements
   of your reference material.

   [AI generates this if writer struggles, then asks for edits]
   ```

2. **Wound Exploration**
   ```
   Journal as [CHARACTER] about the moment that created their flaw. What happened?
   How did it change them? What did they decide about themselves/the world?
   ```

3. **Level 2 Awareness Exercise**
   ```
   Now journal as [CHARACTER] from the perspective of someone who HURT them.
   Write from that person's POV explaining their actions. This develops
   psychological complexity.
   ```

4. **Worst Fear Confrontation**
   ```
   Describe [CHARACTER]'s worst nightmare. What terrifies them most? Why?
   ```

**Questions:**
24. [AI provides character journal prompt - user writes or AI drafts for approval]
25. [AI asks follow-ups based on journal: "You said they wake up anxious. Why?"]
26-30. [Repeat for each preparatory exercise]

#### 2.4 Supporting Cast Design

```
WIZARD: "Your protagonist creates the rest of the cast. Each supporting
character exists to:
1. Reveal a different dimension of your protagonist
2. Serve the protagonist's journey toward their goal

For a 4-dimensional protagonist, you typically need ~4 supporting characters."
```

**Questions:**
31. Who is the character closest to your protagonist? (reveals vulnerability)
32. Who opposes them? (antagonist reveals strength/flaw under pressure)
33. Who represents what they COULD become? (mentor or dark mirror)
34. Who needs them? (tests their growth)
35-40. [For each supporting character: Name, role, how they reveal protagonist dimension]

---

### Phase 3: Plot Architecture (25-35 questions, ~35 minutes)

**Goal**: Structure narrative using Save the Cat! 15-beat framework

#### 3.1 Architect vs. Gardener

```
WIZARD: "Some writers (architects) plot meticulously. Others (gardeners)
discover the story as they write. Neither is wrong, but structure helps EVERYONE.

George R.R. Martin is a famous gardener - but even he knows his major plot
points before writing. We'll create a flexible framework, not a straitjacket."
```

**Questions:**
41. Do you prefer detailed outlines or discovering as you write?
42. [If pantser] "Would a loose framework of major plot points help prevent writer's block?"

#### 3.2 Save the Cat! 15-Beat Walkthrough

The wizard walks through each beat, asking targeted questions and showing examples from successful novels in the same genre.

```
WIZARD: "We're going to map your story to the 15 beats found in bestsellers.
Each beat has a specific purpose and timing. Ready?"
```

**Beat 1: Opening Image (0-1%)**
```
Q43: "What does your protagonist's life look like BEFORE the transformation?
Paint a visual snapshot - what are they doing, where are they, what's their
emotional state?"

[AI suggests: "Show them in their 'ordinary world' exhibiting their flaw"]
```

**Beat 2: Theme Stated (5%)**
```
Q44: "Around chapter 1-2, someone will hint at the life lesson your protagonist
needs to learn. Who says it? What do they say?"

[AI connects to theme from Phase 1]
```

**Beat 3: Setup (1-10%)**
```
Q45: "What's your protagonist's status quo? What are their:
- Daily life/routine?
- Relationships?
- Goals and frustrations?
- The 'Six Things That Need Fixing' in their life?"
```

**Beat 4: Catalyst (10%)**
```
Q46: "What life-changing event FORCES your protagonist to act? This isn't a
small problem - it's an earthquake that makes the old life impossible.

Examples from your genre [AI pulls from KB]: ..."

Q47: "How does this event connect to their flaw?"
```

**Beat 5: Debate (10-20%)**
```
Q48: "After the catalyst, your protagonist resists change. What are their
doubts? Why do they hesitate to enter the new world?"
```

**Beat 6: Break Into 2 (20%)**
```
Q49: "What decision does your protagonist make that officially starts the
adventure? They CHOOSE to leave their comfort zone - what's the specific moment?"
```

**Beat 7: B Story (22%)**
```
Q50: "Who or what is the 'love story'? (Not necessarily romantic - could be
a friendship, mentor, or internal discovery.) This character/thread will teach
the theme."
```

**Beat 8: Fun and Games (20-50%)**
```
Q51: "This is the 'promise of the premise' - the fun part readers came for.
If this is a heist story, this is where we see cool heists. What are 3-5
exciting sequences here?"
```

**Beat 9: Midpoint (50%)**
```
Q52: "The center of your novel - this is CRITICAL for pacing. Is this a:

    A) FALSE VICTORY - Your protagonist seems to be winning/succeeding, but
       it's actually a trap or hollow success. (Example: They catch the suspect,
       but it's the wrong person.)

    B) FALSE DEFEAT - Your protagonist seems to be failing/lost, but there's
       actually hope they don't see yet. (Example: They lose everything, but
       this forces them to try a new approach.)

Which fits your story?"

Q52b: "IMPORTANT: Your midpoint choice determines Beat 10's trajectory:
       - False Victory → Downward path (things get worse)
       - False Defeat → Upward path (things improve before All Is Lost)

       Confirm your choice makes sense for this structure."

Q53: "What happens at this midpoint that RAISES THE STAKES?"
```

**Beat 10: Bad Guys Close In (50-75%)**
```
Q54: "After the midpoint, everything gets worse [if False Victory] or starts
improving [if False Defeat] before the All Is Lost beat.

External enemies close in AND/OR internal doubts tear the team apart. What goes wrong?"

[AI validates trajectory matches Beat 9 choice]
```

**Beat 11: All Is Lost (75%)**
```
Q55: "Rock bottom. The lowest point. Often includes a 'whiff of death' (literal
or symbolic - a relationship dies, hope dies, old self dies). What is your
protagonist's All Is Lost moment?"
```

**Beat 12: Dark Night of the Soul (75-80%)**
```
Q56: "Your protagonist processes everything. They're broken. They finally
UNDERSTAND the theme/lesson. What do they realize?"
```

**Beat 13: Break Into 3 (80%)**
```
Q57: "The 'AHA!' moment. They realize what they must DO to fix everything.
What's the plan? What do they finally understand?"
```

**Beat 14: Finale (80-99%)**
```
Q58: "The climax. They execute the plan, having learned the theme. They prove
they've transformed. How do they defeat the antagonist/solve the problem using
their NEW self?"

Q59: "How do all story threads tie together here?"
```

**Beat 15: Final Image (99-100%)**
```
Q60: "Mirror to Opening Image. Show the AFTER snapshot. Your protagonist in
the same situation as the opening, but transformed. What does this look like?"
```

#### 3.3 Act Structure & Pacing

```
WIZARD: "Let's think about pacing. Tension should follow a progressively
increasing line throughout your novel - not flat, not random spikes, but
ESCALATING.

Imagine graphing tension (low/medium/high) across your chapters. Flat spots
where 3 consecutive chapters sit at the same tension level will feel slow.
You need variation AND escalation."
```

**Questions:**
61. How many chapters do you envision? (typical: 25-40)

62. [AI calculates beats per act based on answer]

63. Where are your major set pieces? (action scenes, revelations, confrontations)

64. How will you escalate stakes? (each act should raise them)

65. **[NEW - PACING CONCEPT]**: "As you outline, imagine the tension level of each
    chapter. Are there any 'rest periods' where multiple chapters sit at low tension?
    That's where readers might lose interest. Where can you add complications?"

```
WIZARD: "Pro tip: Visual writers sometimes struggle to identify pacing issues
by just reading. If you ever feel like pacing is off but can't pinpoint why,
try visualizing your 15 beats on a tension graph. You'll immediately see flat
spots or missing escalation.

[Future feature: We'll add a pacing visualization tool for this]"
```

---

### Phase 4: World & Context (15-20 questions, ~15 minutes)

**Goal**: Build believable setting without info-dumping

#### 4.1 Setting Foundation

**Questions:**
65. When does this story take place? (contemporary, historical period, future, fantasy era)
66. Where is it set? (city/country, or invented world)
67. What makes this setting unique?
68. What are 3 sensory details readers will experience repeatedly? (sights, sounds, smells)

#### 4.2 Worldbuilding Strategy

```
WIZARD: "Here's the trap: You know EVERYTHING about your world. Readers know
NOTHING. But DUMPING info kills pacing.

The solution: SPRINKLE hints. TRUST readers to piece it together. Create
participation."
```

**Questions:**
69. What crucial context must readers know in chapter 1? (list 5 things max)

70. What can wait until chapter 5? (should be most things)

71. **[NEW - POV CONTEXT]**: "Remember: Context must be revealed through what
    your POV character EXPERIENCES (their sensory and psychological moment),
    not through exposition FOR THE READER.

    ❌ Bad: 'The quantum implant, invented in 2031, allowed users to...'
    ✅ Good: 'The implant's cold insertion point pulsed behind her ear.'

    Story prioritizes EXPERIENCE over EXPLANATION. Trust readers to infer."

72. What can readers infer from context clues?

73. [If fantasy/sci-fi] What are your world's 3 most important rules? (magic system, technology, society)

#### 4.3 Opening Chapter Strategy

```
WIZARD: "Your first chapter is CRITICAL. Agents/readers decide in 10 pages if
they'll continue.

Priority: STORY (moment-to-moment experience) over NARRATIVE CONTEXT (backstory).

❌ AVOID THESE CLICHÉS (Instant rejection):
- Character waking up / alarm clock
- Character looking in mirror (describing themselves)
- Weather description opening
- Flashbacks in chapter 1
- Convenient exposition dialogues ("As you know, Bob...")
- Prologues that front-load worldbuilding

✅ INSTEAD: Drop readers into a moment that's MOVING."
```

**Questions:**
74. What's happening in the first scene? (action, not setup)

75. **[NEW - CLICHÉ CHECK]**: "Is your opening free of these clichés?
    - Waking up
    - Looking in mirror
    - Long weather description
    - Prologue explaining the world

    If any are present, what's a more dynamic starting point?"

76. Whose POV? (usually protagonist)

77. What does the protagonist WANT in this specific moment?

78. What's stopping them?

79. How does this scene hint at the catalyst without revealing it?

---

### Phase 5: Symbolic Layering (Optional, 10-15 questions, ~10 minutes)

**Goal**: Add depth through symbolism (advanced users only)

```
WIZARD: "This phase is optional but powerful. Symbolism turns simple objects
into carriers of meaning. It's subtle persuasion - when readers uncover it
themselves, they invest more deeply."
```

#### 5.1 Symbol Identification

**Questions:**
78. Are there any recurring objects/images in your story?
79. What could these represent beyond their literal meaning?
80. How will these symbols evolve as the character grows?

**Example:**
```
WIZARD: "You mentioned your protagonist always carries their dead mother's
compass. Great symbol potential!

- Early: Represents being lost, seeking direction
- Middle: They rely on it obsessively (flaw: can't trust themselves)
- End: They give it away (learned to find their own direction)

This is symbolism through EVOLUTION and RECURRENCE."
```

#### 5.2 Layer Development

**Questions:**
81. What's your surface narrative? (the literal plot)
82. What's your symbolic layer? (what the plot represents)
83. Is there an allegorical level? (larger social/philosophical meaning)
84. How will symbols develop through: Recurrence, Evolution, Juxtaposition?

---

## Wizard Behavior & Intelligence

### Conversational Features

1. **Adaptive Follow-ups**
   ```python
   # After user responds
   ai_analysis = analyze_response(user_input, current_context)

   if ai_analysis["contradicts_previous"]:
       ask_clarification()
   if ai_analysis["vague"]:
       prompt_for_specifics()
   if ai_analysis["brilliant"]:
       affirm_and_build_on_it()
   ```

2. **Detect Contradictions**
   ```
   USER: "My protagonist is fiercely independent"
   [Later]
   USER: "The catalyst is their mentor dying, leaving them lost"

   WIZARD: "Wait - you said Emma is fiercely independent, but now you're
   suggesting she's lost without her mentor. That's a GREAT contradiction
   for creating dimension! Is she *actually* independent, or does she BELIEVE
   she is while depending on her mentor? Let's explore this..."
   ```

3. **Make Connections**
   ```
   WIZARD: "I'm noticing a pattern. Your protagonist's flaw (inability to trust)
   connects perfectly to:
   - Your theme (redemption requires vulnerability)
   - Your catalyst (betrayal by partner)
   - Your All Is Lost beat (loses last ally)

   This cohesion will make your story RESONATE. Readers will feel the inevitability."
   ```

### Knowledge Base Integration

**During wizard, query NotebookLM for:**

1. **Genre-Specific Advice**
   ```
   When user selects "Thriller" →
   Query: "What are conventions of thriller genre? Pacing, stakes, typical structure?"

   WIZARD: "Since you're writing a thriller, readers expect:
   - Ticking clock (deadline pressure)
   - Stakes that escalate to life/death
   - Midpoint that raises danger
   [Source: Writing bestseller notebook]"
   ```

2. **Expert Quotes**
   ```
   When discussing character flaws →
   Query: "What do experts say about character flaws in fiction?"

   WIZARD: "Lisa Cron says: 'Readers expect fictional characters to have
   weaknesses to empathize with them.' Your protagonist's flaw makes them
   RELATABLE."
   ```

3. **Specific Techniques**
   ```
   When user struggles with opening →
   Query: "How to write compelling first chapter?"

   WIZARD: "Let me share what successful authors do..."
   ```

### AI-Generated Content

The wizard can **generate** content for the user:

1. **Character Journals**
   ```
   WIZARD: "Would you like me to draft a journal entry as Emma to get you started?
   You can edit it to match your vision."

   [AI generates based on all info gathered]
   [User edits/approves]
   ```

2. **Beat Summaries**
   ```
   WIZARD: "Based on everything you've told me, here's a rough outline of your
   Midpoint beat:

   'Emma infiltrates the gala, believing she's about to catch the killer. She
   succeeds - but discovers the killer is working for her own partner. FALSE
   VICTORY turns to betrayal. Stakes: Now she's hunted by both sides.'

   Does this capture it?"
   ```

3. **Scene Prompts**
   ```
   WIZARD: "Here are 3 possible openings based on your answers:

   A) Emma in her apartment, receiving the call about her sister's death
   B) Emma mid-argument with her partner, phone rings with the news
   C) Emma at the crime scene, realizing too late who the victim is

   Which feels most powerful?"
   ```

---

## Output Artifacts

At the end, wizard generates structured files in `project/reference/`:

### 1. Character Profiles
```
project/reference/Reference_Library/Characters/Core_Cast/
├── [PROTAGONIST_NAME]_Profile.md
├── [SUPPORTING_1]_Profile.md
├── [SUPPORTING_2]_Profile.md
└── [ANTAGONIST]_Profile.md
```

**Template:**
```markdown
# [Character Name]

## True Character
- Core traits: [List]
- Fatal flaw: [Description]
- Mistaken belief: [What they believe that's wrong]

## Characterization
- Age:
- Appearance:
- Mannerisms:
- Speech patterns:

## Contradiction
[How their true character contradicts itself or characterization]

## Story Role
- Serves protagonist by: [How they reveal dimension]
- Goal in story:
- Relationship to protagonist:

## Character Arc
- Starting point:
- Transformation:
- Ending point:

## Journal Entries
[Paste preparatory journal work]

## Voice Sample
[AI-generated dialogue sample]
```

### 2. Story Structure
```
project/reference/Reference_Library/Story_Structure/
└── Plot_Outline_15_Beats.md
```

**Template:**
```markdown
# Story Structure - [TITLE]

## Save the Cat! 15 Beats

### Beat 1: Opening Image (0-1%)
[User's response from wizard]

### Beat 2: Theme Stated (5%)
[User's response]

[... all 15 beats ...]

## Act Structure
- Act 1 (Setup): Chapters 1-X
- Act 2A (Rising Action): Chapters X-Y
- Act 2B (Complications): Chapters Y-Z
- Act 3 (Resolution): Chapters Z-END

## Scene Ideas
[AI-generated suggestions based on beats]
```

### 3. World Building
```
project/reference/Reference_Library/World_Building/
└── Setting_And_Context.md
```

### 4. Themes & Philosophy
```
project/reference/Reference_Library/Themes_and_Philosophy/
└── Theme_And_Symbols.md
```

**Template:**
```markdown
# Theme & Symbolism

## Core Theme
[One sentence theme statement]

## Life Lesson
What protagonist learns: [Description]

## Symbols
### [Symbol Name]
- Literal meaning:
- Symbolic meaning:
- Evolution through story:

## Layering
- Surface narrative: [Plot summary]
- Symbolic layer: [What it represents]
- Allegorical meaning: [Larger themes]
```

---

## Technical Implementation

### Wizard Flow Engine

```python
class CreationWizard:
    def __init__(self):
        self.phases = [
            FoundationPhase(),
            CharacterPhase(),
            PlotPhase(),
            WorldPhase(),
            SymbolismPhase(optional=True)
        ]
        self.context = WizardContext()  # Stores all responses
        self.kb_client = NotebookLMClient()
        self.ai_analyzer = AIAnalyzer()

    def run(self):
        print_welcome()

        for phase in self.phases:
            if phase.optional and not user_wants_phase():
                continue

            phase_context = self.run_phase(phase)
            self.context.update(phase_context)

            self.save_progress()  # Auto-save after each phase

        self.generate_artifacts()

    def run_phase(self, phase):
        print_phase_intro(phase)

        for question in phase.questions:
            # Ask question
            response = self.ask_question(question)

            # AI analyzes response
            analysis = self.ai_analyzer.analyze(
                response,
                self.context,
                question.context
            )

            # Provide feedback / follow-ups
            if analysis.needs_clarification:
                response = self.ask_follow_up(analysis.clarification_prompt)

            # Query knowledge base if relevant
            if question.kb_relevant:
                expert_advice = self.kb_client.query(
                    question.kb_query_template.format(context=self.context)
                )
                self.show_expert_advice(expert_advice)

            # Make connections
            connections = self.ai_analyzer.find_connections(
                response,
                self.context
            )
            if connections:
                self.highlight_connections(connections)

            # Store response
            self.context.add_response(question.id, response, analysis)

        return phase_context

    def generate_artifacts(self):
        generator = ArtifactGenerator(self.context)

        # Generate character profiles
        for character in self.context.characters:
            generator.create_character_profile(character)

        # Generate plot outline
        generator.create_plot_outline(self.context.beats)

        # Generate world building doc
        generator.create_world_doc(self.context.world)

        # Generate theme guide
        generator.create_theme_doc(self.context.theme, self.context.symbols)

        print_completion_summary()
```

### Question Flow with Branching

```python
class Question:
    def __init__(self, id, text, follow_up_logic=None, kb_query=None):
        self.id = id
        self.text = text
        self.follow_up_logic = follow_up_logic
        self.kb_query = kb_query

    def should_ask_follow_up(self, response, context):
        if self.follow_up_logic:
            return self.follow_up_logic(response, context)
        return False

# Example
Q_PROTAGONIST_NAME = Question(
    id="protagonist_name",
    text="What's your protagonist's name?",
    follow_up_logic=lambda r, c: len(r.strip()) < 2  # Too short
)

Q_PROTAGONIST_FLAW = Question(
    id="protagonist_flaw",
    text="What is your protagonist's fatal flaw?",
    kb_query="What makes a good character flaw in {genre} fiction?",
    follow_up_logic=lambda r, c: "perfect" in r.lower()  # Red flag!
)
```

### Session Saving

```python
class WizardSession:
    def save(self):
        session_data = {
            "timestamp": datetime.now(),
            "phase": self.current_phase,
            "context": self.context.to_dict(),
            "progress": f"{self.questions_answered}/{self.total_questions}"
        }

        with open(f"project/.wizard_session_{self.session_id}.json", "w") as f:
            json.dump(session_data, f)

    def load(session_id):
        # Resume from saved session
        pass
```

---

## Progressive Disclosure

### Quick Mode vs. Deep Mode

```
WIZARD: "I can guide you through this in two ways:

○ QUICK MODE (~30 min)  - Essential questions only, AI fills gaps
○ DEEP MODE (~2-3 hours) - Complete character/plot development

Which would you prefer?"
```

### Skip Options

```
WIZARD: "You seem experienced! Would you like to:
○ Answer all questions (thorough)
○ Skip basics, focus on structure (faster)
○ Import existing character work (I'll analyze and integrate it)
"
```

---

## Example Walkthrough

**Let's walk through a sample wizard session for a thriller:**

```
WIZARD: "Welcome to the Creation Wizard! I'll guide you from blank canvas to
complete story bible. This takes 60-90 minutes. Ready?

Let's start with the basics. What's your story about?"

USER: "A detective trying to solve her sister's murder"

WIZARD: "Compelling setup. So we're in thriller/mystery territory. Got it.

Now, why are you writing THIS story? What draws you to it?"

USER: "I've always been fascinated by how grief changes people, and I want
to explore that in a mystery context"

WIZARD: "Beautiful. So this is really a story about grief, using a murder
mystery as the vehicle. That emotional core will make it resonate.

Let me check something: Are you writing this primarily for an audience of
thriller readers, or is this more personal exploration?"

USER: "I want readers to feel something, but yeah, I want it to work as a
proper thriller too"

WIZARD: "Perfect answer. You're serving the audience (thriller conventions)
while bringing something unique (the grief angle).

Let's nail down your premise. Complete this sentence:
'When [INCITING EVENT], a [FLAWED PROTAGONIST] must [GOAL] or else [STAKES]'

Try it with your detective:"

USER: "When her estranged sister is murdered, a detective struggling with
guilt must solve the case before the killer strikes again, or lose the only
chance to make peace with her past"

WIZARD: "EXCELLENT. You've got:
- Inciting event: Sister murdered
- Flaw hint: Guilt (we'll dig deeper)
- Goal: Solve murder
- Stakes: Temporal (before next victim) + Emotional (peace with past)

That logline works. I'm noting 'estranged' and 'guilt' - those will be important.

Now let's talk theme. What life lesson will your detective learn by the end?"

USER: "That you can't fix the past, but you can choose how to move forward"

WIZARD: "Powerful. So the theme is about acceptance and agency. Beautiful.

In Save the Cat! terms, someone will 'state' this theme around chapter 1-2,
but your protagonist won't UNDERSTAND it until the Dark Night of the Soul.

Who might say this to her early on? Her partner? Captain? A witness?"

USER: "Maybe her therapist, who she's required to see"

WIZARD: "Perfect. Mandated therapy = she's resisting help. Great character detail.

Now let's build your detective from the inside out. Who is she AT HEART?

Forget appearance for now. Give me 3-4 core traits..."

[Wizard continues through all phases, adapting based on responses]
```

---

## Deliverables

Please provide:

1. **Complete Question Flow** (~85 questions total)
   - Organized by phase
   - With branching logic
   - Follow-up triggers

2. **AI Analysis Prompts**
   - How to detect contradictions
   - Connection-making logic
   - When to provide examples

3. **Knowledge Base Query Strategy**
   - Specific queries for each question type
   - How to present expert advice
   - Examples from bestseller notebook

4. **Output Templates**
   - Markdown templates for all artifact types
   - With all fields mapped to wizard questions

5. **Example Walkthrough**
   - Full session for a sample novel (thriller or fantasy)
   - Show AI responses, follow-ups, connections made

6. **Implementation Pseudocode**
   - Python-like structure
   - Key classes and methods
   - Session management

---

## Success Criteria

Your design should:

1. ✅ Guide complete beginner to professional-level story bible
2. ✅ Incorporate expert writing advice naturally
3. ✅ Adapt based on user responses (not rigid form)
4. ✅ Generate usable artifacts (not just notes)
5. ✅ Be resumable at any point
6. ✅ Feel conversational, not interrogative
7. ✅ Create confidence in writer

---

**Target Output**: 4,000-6,000 word design document with complete question flow, AI logic, and implementation guide.

---

**Questions? Proceed with assumptions and document them.**

Focus on making this feel like working with an expert writing coach who knows the craft deeply and can guide you through the messy creative process.
