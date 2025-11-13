# Writers Factory - Complete Architecture
**Date**: 2025-11-13
**Vision**: Multi-Model Tournament System for Computational Storytelling

---

## 🎯 Core Vision

A **model-agnostic narrative creation system** where:
1. Writers launch **tournaments** - same prompt to multiple LLMs
2. System orchestrates parallel generation across 10+ models
3. UX dashboard shows side-by-side comparisons
4. Writers hybridize, score, and select best outputs
5. Analytics track which models excel at which tasks
6. Entire system is **cloneable** for new projects

---

## 📁 Revised Directory Structure

```
writers-factory/
│
├── factory/                              # 🏭 THE FACTORY SYSTEM
│   │
│   ├── core/                             # Core tournament engine
│   │   ├── orchestrator.py               # Tournament coordinator
│   │   ├── agent_registry.py             # LLM registry & loader
│   │   ├── prompt_engine.py              # Prompt templates & adaptation
│   │   ├── context_assembler.py          # Knowledge base integration
│   │   ├── result_handler.py             # Output collection & storage
│   │   └── config/
│   │       ├── agents.yaml               # ⭐ Agent registry
│   │       ├── prompts/                  # Prompt templates library
│   │       └── settings.yaml
│   │
│   ├── agents/                           # LLM integrations
│   │   ├── __init__.py
│   │   ├── base_agent.py                 # Abstract base class
│   │   ├── anthropic/
│   │   │   ├── claude_opus.py
│   │   │   ├── claude_sonnet_4_5.py
│   │   │   ├── claude_sonnet_3_5.py
│   │   │   └── legacy/
│   │   ├── openai/
│   │   │   ├── gpt4o.py
│   │   │   ├── gpt4_turbo.py
│   │   │   └── gpt35_turbo.py
│   │   ├── google/
│   │   │   ├── gemini_2_flash.py
│   │   │   ├── gemini_1_5_pro.py
│   │   │   └── gemini_ultra.py
│   │   ├── xai/
│   │   │   └── grok.py
│   │   ├── chinese/                      # Qwen, DeepSeek, etc.
│   │   │   ├── deepseek.py
│   │   │   ├── qwen.py
│   │   │   ├── doubao.py
│   │   │   ├── baichuan.py
│   │   │   └── kimi.py
│   │   ├── opensource/                   # Mistral, Llama, etc.
│   │   │   ├── mistral.py
│   │   │   ├── llama3.py
│   │   │   └── falcon.py
│   │   └── registry.yaml                 # Agent metadata
│   │
│   ├── knowledge/                        # Knowledge base systems
│   │   ├── cognee/
│   │   │   ├── .venv-cognee/
│   │   │   ├── setup.py
│   │   │   ├── query.py
│   │   │   └── sync.py
│   │   ├── gemini_file_search/
│   │   │   ├── setup.py
│   │   │   ├── query.py
│   │   │   └── sync.py
│   │   ├── notebooklm/
│   │   │   └── query.py
│   │   └── router.py                     # Smart routing logic
│   │
│   ├── analysis/                         # Post-generation tools
│   │   ├── voice_validator.py
│   │   ├── metaphor_analyzer.py
│   │   ├── scoring_engine.py
│   │   ├── hybridizer.py                 # AI-assisted hybridization
│   │   └── analytics.py
│   │
│   ├── ui/                               # UX Dashboard (Phase 2)
│   │   ├── web/                          # React-based web UI
│   │   │   ├── src/
│   │   │   ├── public/
│   │   │   └── package.json
│   │   ├── cli/                          # Rich CLI interface
│   │   │   ├── factory_cli.py            # Main CLI
│   │   │   ├── tournament_ui.py          # Tournament TUI
│   │   │   └── results_viewer.py         # Results comparison
│   │   └── api/                          # Backend API
│   │       ├── server.py
│   │       └── routes/
│   │
│   ├── storage/                          # Data persistence
│   │   ├── database/
│   │   │   ├── schema.sql
│   │   │   └── migrations/
│   │   ├── tournaments/                  # Tournament results
│   │   └── analytics/                    # Usage analytics
│   │
│   ├── skills/                           # Claude Code skills
│   │   ├── _ACTIVE -> ../../.claude/skills/
│   │   └── development/
│   │
│   ├── scripts/                          # Utility scripts
│   │   ├── setup/
│   │   │   ├── install.sh
│   │   │   └── new_project.sh
│   │   └── maintenance/
│   │
│   └── docs/                             # Factory documentation
│       ├── SETUP.md
│       ├── AGENTS.md                     # Adding new LLMs
│       ├── TOURNAMENTS.md                # Running tournaments
│       ├── PROMPTS.md                    # Prompt engineering
│       ├── ANALYTICS.md                  # Understanding metrics
│       └── API_REFERENCE.md
│
├── project/                              # 📚 PROJECT DATA
│   │
│   ├── manuscript/                       # The actual writing
│   │   ├── volume-1/
│   │   ├── volume-2/
│   │   └── volume-3/
│   │
│   ├── reference/                        # Knowledge base
│   │   ├── characters/
│   │   ├── worldbuilding/
│   │   ├── voice-and-style/
│   │   ├── themes/
│   │   └── story-structure/
│   │
│   ├── tournaments/                      # 🎯 Tournament results
│   │   ├── active/                       # Current tournaments
│   │   ├── completed/                    # Finished tournaments
│   │   │   ├── tournament-001-scene-2.1.5/
│   │   │   │   ├── prompt.md
│   │   │   │   ├── context.json
│   │   │   │   ├── results/
│   │   │   │   │   ├── claude-sonnet-4.5.md
│   │   │   │   │   ├── gpt-4o.md
│   │   │   │   │   ├── gemini-2-flash.md
│   │   │   │   │   ├── deepseek-v3.md
│   │   │   │   │   └── qwen-max.md
│   │   │   │   ├── scores.json
│   │   │   │   ├── winner.md
│   │   │   │   └── notes.md
│   │   │   └── [more tournaments]/
│   │   └── templates/                    # Tournament templates
│   │
│   ├── output/                           # Generated content
│   │   ├── reports/
│   │   └── production/
│   │
│   └── archive/                          # Historical materials
│
├── .claude/                              # Claude Code config
│   └── skills/
│
├── .cursor/                              # Cursor AI config
│
├── .factory/                             # Factory runtime data
│   ├── cache/
│   ├── logs/
│   └── analytics.db                      # SQLite analytics DB
│
├── config/                               # Project-level config
│   ├── credentials.json                  # API keys
│   └── factory_settings.yaml
│
├── .gitignore
├── README.md                             # Project overview
└── FACTORY.md                            # Quick start guide
```

---

## 🏗️ System Architecture

### 1. Agent Registry System

**`factory/core/config/agents.yaml`**:
```yaml
agents:
  claude-sonnet-4.5:
    provider: anthropic
    model: claude-sonnet-4-5-20250929
    enabled: true
    context_window: 200000
    cost_per_1k_input: 0.003
    cost_per_1k_output: 0.015
    strengths:
      - creative_narrative
      - character_voice
      - philosophical_depth
    handler: factory.agents.anthropic.claude_sonnet_4_5.ClaudeSonnet45

  gpt-4o:
    provider: openai
    model: gpt-4o-2024-11-20
    enabled: true
    context_window: 128000
    cost_per_1k_input: 0.0025
    cost_per_1k_output: 0.01
    strengths:
      - dialogue
      - polish
      - consistency
    handler: factory.agents.openai.gpt4o.GPT4o

  gemini-2-flash:
    provider: google
    model: gemini-2.0-flash-exp
    enabled: true
    context_window: 1000000
    cost_per_1k_input: 0.00
    cost_per_1k_output: 0.00
    strengths:
      - long_context
      - reasoning
      - cost_effective
    handler: factory.agents.google.gemini_2_flash.Gemini2Flash

  deepseek-v3:
    provider: deepseek
    model: deepseek-chat
    enabled: true
    context_window: 64000
    cost_per_1k_input: 0.00027
    cost_per_1k_output: 0.0011
    strengths:
      - cost_effective
      - speed
      - creative
    handler: factory.agents.chinese.deepseek.DeepSeekV3

  # ... more agents
```

**Dynamic Loading**:
```python
from factory.core.agent_registry import AgentRegistry

# Load all enabled agents
registry = AgentRegistry("factory/core/config/agents.yaml")
enabled_agents = registry.get_enabled_agents()

# Disable agent for this tournament
registry.set_enabled("gpt-3.5-turbo", False)

# Get agent by name
agent = registry.get_agent("claude-sonnet-4.5")
```

---

### 2. Tournament Orchestration

**Tournament Definition**:
```python
from factory.core.orchestrator import Tournament

tournament = Tournament(
    name="scene-2.1.5-blackjack",
    prompt_template="scene_generation_v2",
    agents=["claude-sonnet-4.5", "gpt-4o", "gemini-2-flash", "deepseek-v3"],
    context={
        "character": "Mickey Bardot",
        "scene_type": "blackjack_game",
        "phase": 2,
        "key_beats": ["quantum_bleed", "noni_observation"]
    },
    knowledge_sources=["characters/mickey", "worldbuilding/quantum"],
    max_tokens=2000,
    temperature=0.8
)

# Run tournament (parallel execution)
results = await tournament.run()

# Results include:
# - Raw outputs from each agent
# - Token usage & cost
# - Response times
# - Auto-scored metrics
```

**Parallel Execution**:
```python
# factory/core/orchestrator.py
async def run_tournament(self):
    """Execute tournament with parallel agent calls."""

    # Prepare context for each agent
    contexts = await self._prepare_contexts()

    # Launch all agents in parallel
    tasks = []
    for agent_name in self.agents:
        agent = self.registry.get_agent(agent_name)
        context = contexts[agent_name]
        tasks.append(agent.generate(self.prompt, context))

    # Wait for all to complete (with timeout)
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle results, errors, timeouts
    return self._process_results(results)
```

---

### 3. Prompt Engine & Context Assembly

**Prompt Templates** (`factory/core/config/prompts/`):
```
prompts/
├── scene_generation/
│   ├── basic.md
│   ├── enhanced_voice.md
│   └── philosophical_heavy.md
├── dialogue/
│   ├── witty.md
│   └── tense.md
└── enhancement/
    └── polish_v2.md
```

**Context Assembler**:
```python
from factory.core.context_assembler import ContextAssembler

assembler = ContextAssembler(
    knowledge_systems=["cognee", "gemini_file_search", "notebooklm"]
)

# Smart routing based on query type
context = await assembler.gather(
    query="Tell me about Mickey's quantum abilities",
    max_tokens=10000,
    prefer_local=True  # Use Cognee if available
)

# Per-agent adaptation (trim for smaller windows)
adapted = assembler.adapt_for_agent(
    context=context,
    agent="gpt-3.5-turbo",  # 16k window
    reserve_for_output=2000
)
```

---

### 4. UX Dashboard Architecture

#### Phase 1: Rich CLI (Immediate)
```bash
# Launch tournament
./factory.py tournament create \
  --name "scene-2.1.5" \
  --agents "claude,gpt4o,gemini,deepseek" \
  --prompt "scene_generation_v2" \
  --context "characters/mickey,worldbuilding/quantum"

# Monitor live progress
./factory.py tournament watch scene-2.1.5

# Compare results (side-by-side TUI)
./factory.py results compare scene-2.1.5

# Score and annotate
./factory.py results score scene-2.1.5 \
  --winner "claude-sonnet-4.5" \
  --notes "Best metaphor discipline"

# View analytics
./factory.py analytics show --agent "claude-sonnet-4.5"
```

#### Phase 2: Web Dashboard (Future)
- React-based SPA
- Real-time tournament monitoring
- Drag-and-drop agent selection
- Side-by-side diff viewer
- Annotation and scoring UI
- Analytics dashboards
- Export to manuscript

---

### 5. Analytics & Feedback System

**Analytics Database** (`.factory/analytics.db`):
```sql
-- Tournaments
CREATE TABLE tournaments (
    id TEXT PRIMARY KEY,
    name TEXT,
    prompt_template TEXT,
    created_at TIMESTAMP,
    status TEXT
);

-- Results
CREATE TABLE results (
    id TEXT PRIMARY KEY,
    tournament_id TEXT,
    agent_name TEXT,
    output_text TEXT,
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost REAL,
    response_time_ms INTEGER,
    created_at TIMESTAMP
);

-- Scores
CREATE TABLE scores (
    result_id TEXT,
    dimension TEXT,  -- voice, metaphor, structure, etc.
    score INTEGER,
    notes TEXT,
    scored_by TEXT,  -- human or auto
    scored_at TIMESTAMP
);

-- Winners
CREATE TABLE winners (
    tournament_id TEXT,
    result_id TEXT,
    reason TEXT,
    selected_at TIMESTAMP
);
```

**Analytics Queries**:
```python
# Which agent wins most often?
analytics.agent_win_rate("claude-sonnet-4.5")

# Which agent is most cost-effective?
analytics.cost_per_win()

# Which prompt template performs best?
analytics.template_success_rate("scene_generation_v2")

# Average response time by agent
analytics.agent_performance_metrics()
```

---

## 🚀 Implementation Phases

### Phase 1: Core Engine (Week 1-2)
- [x] Agent registry system *(already have 5 agents!)*
- [ ] Tournament orchestrator
- [ ] Parallel execution engine
- [ ] Result storage system
- [ ] Basic CLI interface

### Phase 2: Knowledge Integration (Week 2-3)
- [x] Cognee integration *(done!)*
- [x] Gemini File Search integration *(done!)*
- [x] NotebookLM integration *(done!)*
- [ ] Smart context routing
- [ ] Per-agent context adaptation

### Phase 3: Prompt System (Week 3)
- [ ] Prompt template library
- [ ] Per-agent prompt adaptation
- [ ] Template versioning
- [ ] Prompt analytics

### Phase 4: Analytics (Week 4)
- [ ] SQLite analytics database
- [ ] Cost tracking
- [ ] Performance metrics
- [ ] Win rate analytics
- [ ] Export reports

### Phase 5: Enhanced CLI (Week 4-5)
- [ ] Rich TUI with live updates
- [ ] Side-by-side comparison viewer
- [ ] Scoring and annotation interface
- [ ] Batch tournament support

### Phase 6: Web Dashboard (Week 6+)
- [ ] React frontend
- [ ] REST API backend
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics UI
- [ ] Export to manuscript

---

## 📦 Cloning for New Projects

### New Project Setup:
```bash
# 1. Clone repository
git clone <repo> new-novel-project
cd new-novel-project

# 2. Run new project script
./factory/scripts/setup/new_project.sh "My New Novel"

# This:
# - Wipes project/ directory
# - Creates fresh manuscript/reference structure
# - Resets analytics database
# - Keeps factory/ intact
# - Updates README with new project name

# 3. Configure project
./factory.py init
# Prompts for:
#   - Project name
#   - Genre
#   - Key characters
#   - Worldbuilding elements
#   - Voice/style preferences

# 4. Add API keys
cp config/credentials.example.json config/credentials.json
# Edit with your keys

# 5. Ready to write!
./factory.py tournament create --name "opening-scene"
```

---

## 💡 Key Features

### 1. Model Agnostic
- Add/remove LLMs via config, not code
- Support 10+ providers out of box
- Easy to add new models

### 2. Tournament-First
- Compare multiple models simultaneously
- Objective scoring and analytics
- Learn which models excel at which tasks

### 3. Knowledge-Aware
- Three knowledge systems integrated
- Smart routing based on query type
- Automatic context adaptation

### 4. Cost Conscious
- Track costs per tournament
- Cost-per-win analytics
- Mix expensive + cheap models strategically

### 5. Reproducible
- Every tournament logged
- Full prompt/context/result storage
- Can replay any tournament

### 6. Extensible
- Plugin architecture for new agents
- Custom scoring dimensions
- Custom prompt templates

---

## 🎯 Success Metrics

After Phase 1 completion:
- ✅ Can run 5-model tournament in < 2 minutes
- ✅ All results stored with full metadata
- ✅ CLI provides clear winner recommendation
- ✅ Analytics track costs and performance

After Phase 5 completion:
- ✅ Can manage 10+ concurrent tournaments
- ✅ Rich TUI shows live progress
- ✅ Side-by-side comparison of results
- ✅ Export winning scenes to manuscript

After Phase 6 completion:
- ✅ Web dashboard for non-technical users
- ✅ One-click tournament launch
- ✅ Visual analytics and insights
- ✅ Production-ready for other writers

---

## 💭 Next Steps

Ready to build this? Here's my recommended order:

1. **Tonight/Tomorrow**: Reorganize repo with this structure
2. **This Week**: Build Phase 1 (Core Engine + CLI)
3. **Next Week**: Integrate existing tools into tournament system
4. **Week 3**: Polish and test with Explants Volume 2
5. **Week 4+**: Enhanced features and web dashboard

Sound good?
