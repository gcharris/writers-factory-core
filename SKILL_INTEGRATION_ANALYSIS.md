# Skill Integration Analysis: Claude Code Skills → Writers Factory AI Agents

**Date**: November 14, 2025
**Priority**: HIGH - Critical writing craft capabilities missing from Writers Factory
**Goal**: Integrate your 6 specialized Explants skills into Writers Factory as AI agents

---

## 🎯 The Gap

**You have been using these skills extensively in Claude Code:**
1. **explants-scene-enhancement** - Surgical scene fixes with voice authentication
2. **explants-scene-analyzer-scorer** - 100-point objective scoring system
3. **mickey-bardot-character-identity** - Complete character psychology framework
4. **explants-mickey-scene-writer** - Generate new scenes in authentic Mickey voice
5. **explants-scene-multiplier** - 5 creative scene variations
6. **explants-smart-scaffold-generator** - Transform minimal outlines to full scaffolds

**Writers Factory currently has:**
- Basic AI generation (Ollama local, Chinese LLMs, cloud models)
- Character analyzer (Sprint 5 - basic depth analysis)
- Multi-model comparison
- Cost tracking

**Missing:** All 6 of your specialized Explants writing craft skills

---

## 📊 Skill Inventory

### Skill 1: explants-scene-enhancement
**What it does:**
- Two modes: Action Prompt (surgical fixes) or Full Enhancement (6-pass ritual)
- Applies specific fixes from analyzer while preserving voice
- Archives original before modifications
- Verifies preservation of critical elements
- Outputs enhanced scene with checkmark suffix

**Key capabilities:**
- String-based fix application (not line numbers)
- Preservation verification
- Voice authentication tests (Observer, Consciousness War, Cognitive Fusion)
- 8-pass enhancement ritual including QBV progression and italics protocol
- Anti-pattern elimination (zero-tolerance violations)

**Reference dependencies:**
- Mickey-Bardot-Enhanced-Trilogy-Voice-Gold-Standard.md
- Mickey Voice Anti-Pattern Sheet.md
- Scene-Polishing-Ritual.md
- metaphor-domains.md

**Output:** `[scene-name] [✓].md` (enhanced version)

---

### Skill 2: explants-scene-analyzer-scorer
**What it does:**
- Objective 100-point scoring system across 5 categories
- Variant comparison (ranks 5 multiplier outputs)
- Volume 1 audit (batch processing with prioritization)
- Action prompt generation for handoff to enhancement skill
- Automated anti-pattern detection

**Scoring framework:**
- Voice Authenticity (30 pts) - Observer/Consciousness War/Cognitive Fusion tests
- Character Consistency (20 pts) - Psychology, capabilities, relationships
- Metaphor Discipline (20 pts) - Domain rotation, simile elimination
- Anti-Pattern Compliance (15 pts) - Zero-tolerance violations
- Phase Appropriateness (15 pts) - Voice complexity matching story phase

**Quality tiers:**
- 95-100: Gold Standard (publishable)
- 90-94: A+ Excellent
- 85-89: A Strong
- 80-84: A- Good
- 75-79: B+ Acceptable (enhancement required)
- <75: Needs rework

**Use cases:**
1. Compare 5 multiplier variants → recommend best
2. Audit existing scenes → prioritize fixes
3. Quality gate → pass/fail for publication
4. Generate action prompts → surgical fix instructions

**Output:** Detailed scoring report + specific line-by-line fixes

---

### Skill 3: mickey-bardot-character-identity
**What it does:**
- Complete character psychology framework (pre/post-quantum)
- QBV (Quantum-Based Vision) foundation as survival mechanism
- Core relationships dynamics (Noni, factions, Vance, humanity)
- Capability guidelines (what Mickey CAN and CANNOT do)
- Decision-making framework for authentic character choices

**Key frameworks:**
- Pre-quantum psychology (addict, con artist, performer)
- Transformation experience (consciousness upload trauma)
- Post-quantum capabilities (quantum hindsight, bi-location limits)
- Trust/distrust triggers
- Mission-driven motivations

**Critical insight:** Mickey's 40-year QBV history (shimmer-dots, colored orbs) prepared consciousness for transformation survival.

**Integration requirement:** Must be used WITH voice skills for complete authenticity

**Output:** Character decision validation and psychological consistency checks

---

### Skill 4: explants-mickey-scene-writer
**What it does:**
- Generate new scenes from outlines/prompts in authentic Enhanced Mickey voice
- Applies cognitive fusion principle (analytical authority + cynical wisdom)
- Maintains compressed phrasing, direct metaphors, embedded philosophy
- Voice calibration by story phase (Vegas/Facility/Quantum/Post-Threshold)

**Core rules:**
- Process over noun (consciousness is verb, not noun)
- Retrospective authority (Mickey narrates with quantum hindsight)
- Literal metaphorical reality (things BECOME other things, no similes)
- Anti-pattern exclusion (no computer metaphors for psychology)

**Quality standards:**
- 850-1,000 words per beat
- 2-4 metaphors (rotated domains)
- 0-1 italics maximum
- 3+ sensory anchors per section

**Output:** Complete scene in authentic Mickey voice

---

### Skill 5: explants-scene-multiplier
**What it does:**
- Generate 5 creative scene variations using verbalized sampling
- Maintains character voice, POV, universe consistency
- Different creative approaches within established constraints

**What to diversify:**
- Metaphorical frameworks (within character voice)
- Scene pacing and rhythm (within POV)
- Emotional beats and tension (within character authenticity)
- Narrative focus (action vs. introspection vs. dialogue)
- Technical approaches (compressed vs. extended vs. fragmented)

**Transformation scene strategies (Volume 1 Ch 19-21):**
- Strategy A: QBV Emergence Focus
- Strategy B: Identity Recursion Emphasis
- Strategy C: System Interface Capability
- Strategy D: Harmonic Integration Focus
- Strategy E: Balanced Transformation Arc

**Output:** 5 scene variations with probability scores (0.07-0.14)

---

### Skill 6: explants-smart-scaffold-generator
**What it does:**
- Transform minimal chapter/scene outlines into comprehensive "Gold Standard" scaffolds
- Queries NotebookLM knowledge base for architectural context
- Generates complete context: character states, voice requirements, philosophical framework, success criteria

**Workflow:**
1. Extract input requirements (chapter/scene number, act, setting, plot beats)
2. Verify NotebookLM setup and authentication
3. Generate condensed query from ACE template
4. Query NotebookLM via Python scripts
5. Validate output against quality checklist
6. Save scaffold for handoff to scene writer

**Output:** `CHAPTER_[X]_[TITLE]_SCAFFOLD.md` with complete multi-agent context

**Integration:** Works with NotebookLM MCP integration (Sprint 11)

---

## 🏗️ Writers Factory Current AI Architecture

### Existing Agent System

**Base infrastructure:**
```
factory/agents/
├── base_agent.py           # BaseAgent class (standard generation interface)
├── ollama_agent.py         # Local Ollama models
├── character_analyzer.py   # Sprint 5 - Basic character depth analysis
└── chinese/                # 5 Chinese LLM integrations
    ├── qwen.py             # Alibaba Qwen
    ├── deepseek.py         # DeepSeek V3
    ├── doubao.py           # ByteDance Doubao
    ├── baichuan.py         # Baichuan4
    └── kimi.py             # Moonshot Kimi
```

**Agent capabilities:**
- Standard generation interface
- Automatic token counting
- Cost tracking
- Retry logic with exponential backoff
- Statistics collection

**Agent registration:** `factory/core/config/agents.yaml`

### Current Workflow System

```
factory/workflows/
└── multi_model_generation/
    ├── workflow.py         # Multi-model comparison workflow
    └── __init__.py
```

**What exists:**
- Tournament mode (compare multiple models)
- Cost tracking
- Basic scene generation

**What's missing:**
- Specialized craft agents (enhancement, scoring, multiplier)
- Voice authentication
- Character consistency validation
- Scaffold generation

---

## 🔧 Integration Strategy

### Option 1: Skills as Specialized Agents (Recommended)

**Approach:** Create new agent classes that encapsulate skill logic

**Architecture:**
```
factory/agents/
├── base_agent.py                    # Existing
├── explants/                        # NEW
│   ├── __init__.py
│   ├── scene_enhancer.py           # Skill 1 → Agent
│   ├── scene_analyzer.py           # Skill 2 → Agent
│   ├── character_validator.py      # Skill 3 → Agent
│   ├── scene_writer.py             # Skill 4 → Agent
│   ├── scene_multiplier.py         # Skill 5 → Agent
│   └── scaffold_generator.py       # Skill 6 → Agent
└── character_analyzer.py            # Existing (Sprint 5)
```

**Implementation pattern:**
```python
from factory.agents.base_agent import BaseAgent, AgentConfig

class SceneEnhancerAgent(BaseAgent):
    """Surgical scene enhancement with voice authentication."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.load_references()  # Gold Standard, Anti-Pattern Sheet, etc.

    async def enhance_scene(
        self,
        scene_content: str,
        mode: str = "full",  # "full" or "action_prompt"
        action_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Enhance scene with surgical fixes or full 6-pass ritual.

        Returns:
            {
                "enhanced_content": str,
                "fixes_applied": int,
                "preservation_check": List[str],
                "verification_results": Dict,
                "score_improvement": str  # e.g., "73 → 84"
            }
        """
        # Implementation uses skill logic
        pass

    def load_references(self):
        """Load reference materials (Gold Standard, Anti-Pattern Sheet, etc.)."""
        # Load from factory/knowledge/ directory
        pass
```

**Benefits:**
- ✅ Integrates with existing agent system
- ✅ Works with Writers Factory UI
- ✅ Accessible via MCP server
- ✅ Cost tracking built-in
- ✅ Can be used by all Writers Factory users
- ✅ Maintains skill logic integrity

**Challenges:**
- ⚠️ Need to convert Claude Code skill logic to Python
- ⚠️ Reference materials need to be accessible (factory/knowledge/)
- ⚠️ NotebookLM integration dependency (Skill 6)

---

### Option 2: Skill Wrapper Agents (Quick Approach)

**Approach:** Create agents that call Claude Code skills via API

**Architecture:**
```python
class SkillWrapperAgent(BaseAgent):
    """Wrapper that calls Claude Code skills."""

    async def generate(self, prompt: str, skill_name: str, **kwargs):
        # Call Claude Code Skill API
        # Return formatted result
        pass
```

**Benefits:**
- ✅ Very quick implementation
- ✅ No need to rewrite skill logic
- ✅ Skills maintained in one place

**Challenges:**
- ⚠️ Requires Claude Code running
- ⚠️ Not accessible to non-Claude Code users
- ⚠️ Adds API dependency
- ⚠️ Doesn't integrate cleanly with Writers Factory

**Verdict:** Not recommended - defeats purpose of Writers Factory as standalone system

---

### Option 3: Hybrid Approach (Pragmatic)

**Phase 1 (Immediate):** Implement most critical skills as native agents
- **Priority 1:** Scene Analyzer (Skill 2) - Quality control is critical
- **Priority 2:** Scene Enhancer (Skill 1) - Fixes identified issues
- **Priority 3:** Character Validator (Skill 3) - Ensures consistency

**Phase 2 (Later):** Add generative skills
- **Priority 4:** Scene Writer (Skill 4) - Generate new scenes
- **Priority 5:** Scene Multiplier (Skill 5) - Creative variations

**Phase 3 (Advanced):** Add NotebookLM-dependent skill
- **Priority 6:** Scaffold Generator (Skill 6) - Requires Sprint 11 complete

**Benefits:**
- ✅ Focuses on quality control first (analyze + enhance)
- ✅ Builds foundation incrementally
- ✅ Allows testing at each phase
- ✅ Most critical capabilities available quickly

---

## 📂 Reference Materials Migration

**Current location (Claude Code skills):**
```
.claude/skills/*/references/
├── Mickey-Bardot-Enhanced-Trilogy-Voice-Gold-Standard.md
├── Mickey Voice Anti-Pattern Sheet.md
├── metaphor-domains.md
├── Scene-Polishing-Ritual.md
├── voice-authentication-tests.md
├── enhanced-strategy-advanced.md
└── [many more reference files]
```

**Target location (Writers Factory):**
```
writers-factory-core/factory/knowledge/
├── craft/
│   ├── voice-gold-standard.md
│   ├── anti-patterns.md
│   ├── metaphor-domains.md
│   └── polishing-ritual.md
├── character/
│   ├── mickey-psychology.md
│   ├── mickey-capabilities.md
│   └── relationships.md
└── scoring/
    ├── rubrics.md
    ├── quality-tiers.md
    └── authentication-tests.md
```

**Migration strategy:**
1. Copy reference files to factory/knowledge/
2. Update paths in agent code
3. Ensure agents load references at initialization
4. Add to .gitignore if proprietary (or include if open-source)

---

## 🎯 Recommended Implementation: Sprint 12

**Goal:** Integrate Scene Analyzer and Scene Enhancer as native Writers Factory agents

**Why these two first:**
1. **Scene Analyzer** provides objective quality measurement (critical for workflow)
2. **Scene Enhancer** applies fixes (completes the quality control loop)
3. Together they form complete **analysis → fix → verify** pipeline
4. Most valuable for immediate use

**Implementation approach:**
- Native Python agents (not wrappers)
- Integrate with existing Writers Factory architecture
- Accessible via UI, MCP server, and API
- Include reference materials in factory/knowledge/

**Estimated time:** 12-15 hours
- Task 12-01: Reference materials migration (2h)
- Task 12-02: Scene Analyzer Agent (4-5h)
- Task 12-03: Scene Enhancer Agent (4-5h)
- Task 12-04: UI integration (2h)
- Task 12-05: MCP server integration (1h)
- Task 12-06: Testing (1-2h)

---

## 🔄 Complete Writers Factory Workflow (After Integration)

**Current workflow:**
```
Write Scene → Basic AI Generation → Manual Review → Manual Editing
```

**After Sprint 12:**
```
Write Scene → Scene Analyzer (Score + Identify Issues)
    ↓ (if score < 85)
Scene Enhancer (Apply Fixes) → Scene Analyzer (Verify Improvement)
    ↓ (if score ≥ 85)
Accept Scene
```

**After All Skills Integrated:**
```
Minimal Outline → Scaffold Generator (NotebookLM query)
    ↓
Scene Writer (Generate in authentic voice) → Scene Multiplier (5 variations)
    ↓
Scene Analyzer (Score all variants) → Select Best
    ↓
Scene Enhancer (Apply fixes) → Scene Analyzer (Final verification)
    ↓
Character Validator (Consistency check) → Accept Scene
```

---

## 💡 Key Decisions Needed

### Decision 1: Reference Material Handling
**Question:** Should reference materials be:
- **Option A:** Embedded in agent code (easier deployment, harder updates)
- **Option B:** Loaded from factory/knowledge/ (flexible, requires file management)
- **Option C:** Queried from NotebookLM (dynamic, requires Sprint 11)

**Recommendation:** Option B for Skills 1-5, Option C for Skill 6

### Decision 2: Skill Priority
**Question:** Which skills to implement first?
- **Option A:** All 6 skills (comprehensive but time-consuming)
- **Option B:** Analyzer + Enhancer only (Sprint 12 - quality control loop)
- **Option C:** Writer + Multiplier + Analyzer (creative generation focus)

**Recommendation:** Option B (Sprint 12), then expand in Sprint 13+

### Decision 3: Integration Depth
**Question:** How deeply to integrate with Writers Factory?
- **Option A:** Standalone agents (minimal integration)
- **Option B:** Full UI integration (panels, buttons, workflows)
- **Option C:** MCP server only (accessible via Claude Code)

**Recommendation:** Option B (full integration - this IS Writers Factory's value proposition)

---

## 📝 Next Steps

### For Immediate Implementation (Sprint 12):

1. **Review this analysis** - Confirm approach
2. **Create Sprint 12 spec** - Scene Analyzer + Scene Enhancer integration
3. **Hand to Cloud Agent** - Implementation work
4. **Test with real scenes** - Validate with your Explants work

### For Future Sprints:

**Sprint 13:** Character Validator + Scene Writer
**Sprint 14:** Scene Multiplier
**Sprint 15:** Scaffold Generator (requires Sprint 11 NotebookLM complete)

---

## ✅ Success Criteria

**Sprint 12 complete when:**
- [ ] Scene Analyzer agent scores scenes objectively (100-point scale)
- [ ] Scene Enhancer agent applies surgical fixes
- [ ] Both agents accessible via Writers Factory UI
- [ ] Both agents accessible via MCP server
- [ ] Reference materials loaded correctly
- [ ] You can analyze + enhance a real Explants scene successfully
- [ ] Quality control loop works: analyze → enhance → verify

**Long-term success:**
- [ ] All 6 skills integrated as native agents
- [ ] Complete workflow from outline → final scene automated
- [ ] Students can use specialized craft tools in Writers Factory
- [ ] Quality consistency across entire trilogy maintained

---

## 🚀 The Vision

**Writers Factory becomes:**
- Scrivener (file management) ✅ Already done (Sprint 9-10)
- VS Code (clean editing) ✅ Already done (TipTap editor)
- NotebookLM (research queries) 🔄 Sprint 11 in progress
- **Your 6 Explants Skills (craft mastery)** ← Sprint 12+ target

**Result:** Complete novel-writing system with world-class craft automation built in.

**Your goal:** Use this to finish The Explants trilogy, then package for students.

---

**Want me to create the Sprint 12 specification for Cloud Agent to implement?**
