# Task: Design UX for Writers Factory Multi-Model Novel Writing System

**Priority**: High
**Assigned To**: Cloud Agent
**Estimated Time**: 4-6 hours
**Dependencies**: None

---

## Context

You are designing the user interface for a multi-model AI novel writing factory. This system helps writers use multiple AI models (Claude, Gemini, GPT, Qwen, DeepSeek) with three knowledge graph backends to write, enhance, and analyze fiction manuscripts.

## Current System Architecture

**Factory Components:**
- Multi-agent framework (5+ AI models)
- 3 knowledge systems:
  - Self Knowledge Graph (Cognee - local, 17MB, instant)
  - Cloud Knowledge Graph (Gemini File Search - ~400MB, semantic)
  - NotebookLM (external integration)
- 8 working systems: Scene Multiplier, Scene Enhancement, Scene Analyzer/Scorer, Voice Consistency Tester, Smart Scaffold Generator, Batch Processor, Canon Consistency Checker, Gemini File Search

**User Journey Stages:**
1. **Creation** - Blank canvas → full story bible (wizard-guided)
2. **Writing** - Outline → scenes (multi-model generation)
3. **Enhancing** - Draft → polished (voice enforcement, enhancement)
4. **Analyzing** - Checking consistency (character, plot, voice)
5. **Scoring** - Quality metrics (scene scores, voice tests)

---

## UX Requirements

### 1. Agent Selection & Voice Testing Section

**Purpose**: Allow users to select AI models and compare their outputs

**Features:**
- **Model Selection Interface**
  - Checkboxes for available models (Claude, Gemini, GPT, Qwen, DeepSeek)
  - Show cost per 1K tokens for each
  - Show average quality scores (if available from past sessions)
  - "Select All" / "Deselect All" shortcuts

- **Voice Testing Dashboard**
  - Tournament-style comparison (5 models → pairwise comparisons → winner)
  - Side-by-side text comparison
  - Voice consistency scores (0-100)
  - Character authenticity metrics
  - User can mark favorites with ⭐

- **Model Performance Metrics**
  - Table showing: Model | Avg Cost | Avg Quality | Avg Speed | Win Rate
  - Historical trend graphs (optional, if time permits)
  - Recommendations: "For your character voice, Claude performs best"

- **Preference Memory**
  - "Remember this selection for [Writing/Enhancing/Analyzing]"
  - Quick profiles: "Budget Mode" (cheapest), "Quality Mode" (best scores), "Fast Mode" (fastest)

### 2. Stage Pipeline Section

**Purpose**: Visual workflow showing where user is in the writing process

**Visual Design:**
```
[Creation] → [Writing] → [Enhancing] → [Analyzing] → [Scoring]
    ✓           ⚡          pending      pending      pending
```

**Features:**
- Current stage highlighted with ⚡ or different color
- Completed stages marked with ✓
- Each stage clickable to jump there
- Progress indicators:
  - Creation: "Story Bible 80% complete (4/5 sections done)"
  - Writing: "Scene 45/120 (37%)"
  - Enhancing: "23 scenes enhanced, 22 remaining"

- **Non-linear workflow support**
  - Users can jump between stages
  - Warning if jumping ahead: "⚠️ No story bible detected. Run Creation wizard first?"
  - Breadcrumb showing: Home > Writing > Chapter 5 > Scene 5.3

- **Stage-Specific Modes**
  - Each stage opens dedicated interface with appropriate tools
  - Keyboard shortcut to return to pipeline view (ESC or 'p')

### 3. Knowledge Base Selection

**Purpose**: Choose which knowledge system to query for context

**Three Options:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Select Knowledge Base:                                           │
│                                                                   │
│  ○ Self Knowledge Graph      [Local • Instant • Free]           │
│     17MB indexed | Best for: character lookups, quick facts      │
│                                                                   │
│  ○ Cloud Knowledge Graph     [Cloud • Semantic • ~$0.02/query]  │
│     400MB indexed | Best for: deep analysis, relationships       │
│                                                                   │
│  ○ NotebookLM               [External • Research • Free]        │
│     External notebook | Best for: writing advice, genre research │
│                                                                   │
│  ○ Smart Auto-Route         [Recommended]                       │
│     Let AI choose best KB based on query type                    │
│                                                                   │
│  ☑ Query All (for comparison)                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Intelligence Features:**
- Auto-routing logic:
  - Character/plot queries → Self Knowledge Graph (fast)
  - Thematic/philosophical → Cloud Knowledge Graph (deep)
  - Writing technique → NotebookLM (expert advice)
- Show which KB was used for each response
- Allow manual override

### 4. Creation Wizard Entry Point

**Purpose**: Guide users from blank canvas to ready-to-write

**Features:**
- Prominent "Start Creation Wizard" button for new projects
- "Skip wizard - I have existing work" option
- Resume capability: "Continue wizard from Phase 2: Characters (saved 2 hours ago)"
- Progress bar showing: "Phase 2/5: Deep Character Construction"

**Note**: Full wizard design is in separate task (TASK_Creation_Wizard.md)

---

## Design Constraints

### Technical Stack
- **CLI-first**: Rich terminal UI (think `lazygit`, `htop`, `k9s` style)
- **Python 3.11+** with Rich library
- **SQLite** for session storage
- **Async/await** for parallel operations

### UX Principles
- **Context-aware**: UI adapts to what user has created
- **Cost-conscious**: Always show estimated costs before expensive operations
- **Parallel-friendly**: Support running multiple agents/queries simultaneously
- **Session-based**: Save/resume anywhere
- **Keyboard-first**: Power users should never need mouse
- **Progressive disclosure**: Advanced options hidden until needed

### Performance Targets
- UI refresh: <50ms
- Model selection: Instant
- Knowledge base query: <2s (local), <5s (cloud)
- Stage transition: <100ms

---

## Deliverables

Please design comprehensive documentation including:

### 1. Main Menu Structure
- ASCII mockup of home screen
- Navigation hierarchy
- Keyboard shortcuts legend

### 2. Stage-Specific Screens
For each stage (Creation, Writing, Enhancing, Analyzing, Scoring):
- Screen layout (ASCII mockup)
- Available tools/actions
- Information displayed
- Navigation flow

### 3. Agent Selection Interface
- Model comparison table design
- Voice testing tournament flow
- Preference saving UI

### 4. Knowledge Base Selector
- Clear visual distinction between KB options
- Auto-routing indicator
- Query result comparison view

### 5. Cost Dashboard
- Real-time cost tracking display
- Budget alerts ("⚠️ Approaching $10 session budget")
- Cost breakdown by model/operation

### 6. Session Manager
- Save/load/resume interface
- Session list with metadata
- Auto-save indicator

### 7. Navigation Flows
- Diagram showing: How to get to each screen, how to navigate between screens
- Keyboard shortcuts for all actions
- Modal behaviors (blocking vs. non-blocking)

### 8. Error & Loading States
- Loading spinners/progress bars
- Error message design
- Retry/cancel options

---

## Example Quality Level

Reference these excellent TUI applications:

- **lazygit** - Intuitive git operations, panel-based layout
- **htop** - Process monitoring, color-coded metrics
- **k9s** - Kubernetes management, context switching
- **bottom** - System monitor with graphs
- **gh dash** - GitHub CLI dashboard

Key qualities to emulate:
- Clear information hierarchy
- Consistent color coding (info=blue, success=green, warning=yellow, error=red)
- Helpful status bar at bottom
- Keyboard shortcuts visible or easily discoverable
- Fast, responsive interactions

---

## Current Directory Structure

```
factory/
├── core/              # Multi-agent framework (5 models integrated)
│   ├── agents/        # Claude, Gemini, GPT, Qwen, DeepSeek
│   ├── analysis/      # Voice testing, scoring
│   └── orchestration/ # Multi-agent coordination
├── knowledge/         # Knowledge graph systems
│   ├── cognee-system/ # Self Knowledge Graph
│   └── GEMINI_*.md    # Cloud Knowledge Graph docs
├── scripts/           # Utility scripts
├── workflows/         # Pre-built workflows (to be built)
└── ui/                # CLI interface (YOUR WORK HERE) ⬅️

project/
├── manuscript/        # User's writing
├── reference/         # Story bible
│   └── Reference_Library/
│       ├── Characters/
│       ├── Story_Structure/
│       ├── Themes_and_Philosophy/
│       └── World_Building/
└── output/            # Generated content
    ├── reports/       # Test results
    └── production/    # Final exports
```

---

## Implementation Notes

### File Structure to Create

```
factory/ui/
├── __init__.py
├── main_menu.py           # Entry point, main dashboard
├── stage_screens/
│   ├── creation.py        # Creation wizard interface
│   ├── writing.py         # Scene generation interface
│   ├── enhancing.py       # Enhancement interface
│   ├── analyzing.py       # Consistency checking interface
│   └── scoring.py         # Quality metrics interface
├── components/
│   ├── agent_selector.py  # Model selection component
│   ├── kb_selector.py     # Knowledge base picker
│   ├── cost_tracker.py    # Cost dashboard component
│   ├── progress_bar.py    # Custom progress indicators
│   └── session_manager.py # Save/load UI
├── layouts/
│   ├── panel.py           # Reusable panel layouts
│   ├── table.py           # Rich table formatters
│   └── modal.py           # Modal dialogs
└── utils/
    ├── keyboard.py        # Keyboard handler
    └── colors.py          # Theme/color management
```

### Rich Library Components to Use

- `Panel` - Bordered sections
- `Table` - Data tables with sorting
- `Progress` - Progress bars
- `Tree` - Hierarchical data
- `Syntax` - Code highlighting (for generated text)
- `Layout` - Split screen layouts
- `Live` - Auto-updating displays

---

## Success Criteria

Your design should enable:

1. ✅ New user can navigate entire system in <5 minutes
2. ✅ Power user can execute any operation with keyboard only
3. ✅ Cost is always visible before expensive operations
4. ✅ Multi-model comparison is intuitive and visual
5. ✅ Sessions can be saved/resumed at any point
6. ✅ Knowledge base selection is clear and guided
7. ✅ Stage pipeline shows progress at a glance

---

## Output Format

Please provide a comprehensive design document (markdown) including:

1. **Overview** - High-level UX philosophy
2. **Navigation Map** - Visual diagram of screen flow
3. **Screen Mockups** - ASCII art for each major screen
4. **Component Specs** - Detailed specs for reusable components
5. **Keyboard Shortcuts** - Complete shortcut reference
6. **Color/Theme Guide** - Consistent color usage
7. **Implementation Guide** - Pseudocode for key interactions
8. **User Scenarios** - Walkthrough of common workflows

Target length: 3,000-5,000 words with extensive ASCII mockups.

---

**Questions? Clarifications Needed?**

If any requirements are unclear, document your assumptions and proceed. Focus on creating an intuitive, efficient interface that makes multi-model novel writing feel natural and powerful.
