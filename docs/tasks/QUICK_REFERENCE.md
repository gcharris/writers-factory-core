# Quick Reference: Cloud Agent Deployment

## 🚀 Quick Deploy (3 Steps)

### 1. Upload Package to GitHub
```bash
cd ~/writers-factory-core
mkdir -p docs/tasks
cp "/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/factory/docs/cloud-agent-package/"* docs/tasks/
git add docs/tasks/
git commit -m "Add all task specifications for Cloud Agent"
git push origin main
```

### 2. Start Cloud Agent
Copy this prompt:
```
Please read the START_HERE.md file in the docs/tasks/ directory of the
writers-factory-core repository. Complete all 7 tasks sequentially,
committing and pushing after each one. Don't wait for approval between
tasks - work autonomously and report back when complete.
```

### 3. Wait for Report
Cloud Agent will complete all 7 tasks and report back with summary.

---

## 📦 What's in the Package

- **START_HERE.md** - First document to read
- **PROMPT_Cloud_Agent_Master_Instructions.md** - Complete work protocol
- **PROMPT_Cloud_Agent_Rebuild.md** - Architecture deep dive
- **7 x TASK_*.md** - Detailed specifications for each component
- **UPLOAD_INSTRUCTIONS.md** - How to deploy
- **INITIAL_PROMPT_FOR_CLOUD_AGENT.txt** - Ready-to-paste prompt

**Total**: 13 files, 244KB, ~200KB of specifications

---

## ✅ 7 Tasks (In Order)

1. **Storage & Session Management** (3-4h) - File-based JSON, auto-save, costs
2. **Master CLI (Rich TUI)** (4-5h) - 5-stage interface, status bar, keyboard nav
3. **Knowledge Router** (3-4h) - Cognee + NotebookLM integration
4. **Workflows Module** (4-5h) - Scene generation, enhancement, voice testing
5. **Model Comparison Tool** (3-4h) - Repurpose tournament system
6. **Creation Wizard** (6-8h) - Conversational questionnaire, Save the Cat!
7. **Integration & Polish** (2-3h) - Testing, docs, optimization

**Estimated Total**: 2-3 weeks

---

## 🎯 23 Success Criteria

### Core (5)
- Rich TUI launches with 5-stage pipeline
- Status bar shows progress/costs/auto-save
- TAB navigation between stages
- Auto-save every 30s (non-blocking)
- Cost warnings before expensive ops

### Knowledge (4)
- Ask questions from any stage
- Intelligent routing (Cognee/NotebookLM)
- No "Gemini File Search" exposed
- Cognee invisible to users

### Workflows (3)
- Scene generation with context
- Scene enhancement (voice/pacing/dialogue)
- Voice testing reports

### Model Comparison (4)
- Press 'C' → Comparison opens
- Side-by-side 2-4 models
- Visual diff
- User selects winner → Preference saved

### Creation Wizard (4)
- `factory init` → Conversational wizard
- Not form-like, feels natural
- Marathon runner progress
- Output: 4,000-6,000 word story bible

### Session Management (3)
- Crash recovery on restart
- Lose < 30s of work
- History of last 20 sessions

---

## 🏗️ Architecture At-a-Glance

```
Rich TUI (5-Stage Workflow)
         ↓
Creation → Writing → Enhancing → Analyzing → Scoring
         ↓
Core Systems:
- Agent Pool ✅ (keep)
- Knowledge Router 🏗️
- Storage & Sessions 🏗️
- Cost Tracker 🏗️
- Model Comparison 🏗️ (repurpose tournament)
```

**Key**: Tournament becomes **one tool** in Writing stage, not core.

---

## 📊 Expected Deliverables

### Code
```
factory/
├── core/storage/         # Session management
├── ui/                   # Rich TUI
├── knowledge/            # Cognee + NotebookLM
├── workflows/            # Generation, enhancement, testing
├── tools/                # Model comparison
└── wizard/               # Creation wizard
```

### Tests
```
factory/tests/
├── storage/              # Unit tests
├── ui/                   # UI tests
├── knowledge/            # Knowledge tests
├── workflows/            # Workflow tests
├── tools/                # Tool tests
├── wizard/               # Wizard tests
└── integration/          # End-to-end tests
```

### Docs
```
docs/
├── README.md             # Usage guide
├── ARCHITECTURE.md       # System design
├── API_REFERENCE.md      # API docs
└── TROUBLESHOOTING.md    # Common issues
```

---

## 🎬 What Cloud Agent Will Do

### Autonomous Work Cycle (Per Task)
1. Read task specification
2. Implement functionality
3. Write unit + integration tests
4. Commit with descriptive message
5. Push to repository
6. **Continue immediately to next task** (no approval needed)

### Final Report
When complete, Cloud Agent will provide:
- Summary of all commits
- Success criteria checklist (23/23 ✅)
- Test coverage report
- Known issues/assumptions
- Next steps recommendations

---

## 📍 Package Location

```
/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/
└── factory/docs/cloud-agent-package/
```

---

## 🔗 Repository

**Source**: https://github.com/gcharris/writers-factory-core
**Target Directory**: `docs/tasks/`

---

## ⏱️ Timeline

- **Week 1**: Storage + Master CLI (foundation)
- **Week 2**: Knowledge Router + Workflows + Model Comparison (integration)
- **Week 3**: Creation Wizard + Polish (final)

---

## 💡 Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Session Storage | File-based JSON | Easy backup, no schema migrations |
| Analytics Storage | SQLite | Efficient queries, existing code |
| Knowledge UI | Hidden (Cognee) + Opt-in (NotebookLM) | Simple UX |
| Tournament System | Repurpose as Model Comparison Tool | Hybrid architecture |
| UI Framework | Rich (Python TUI) | Keyboard-first, beautiful |
| Cost Warnings | Before ops > $0.10 | Prevent accidents |

---

## 🚨 Critical Reminders

1. **Autonomy**: Cloud Agent works without approval between tasks
2. **Testing**: Every feature needs unit + integration tests
3. **Commits**: Descriptive messages, push after each task
4. **Architecture**: Keep tournament code, repurpose as comparison tool
5. **Storage**: JSON for sessions, SQLite only for analytics
6. **Knowledge**: Cognee hidden, NotebookLM opt-in, no Gemini File Search exposed
7. **UI**: Rich TUI (NOT basic CLI), keyboard-first navigation

---

## ✨ Ready to Deploy!

1. Upload package to `writers-factory-core/docs/tasks/`
2. Start Cloud Agent with initial prompt
3. Wait 2-3 weeks for completion report
4. Test the final system

**That's it!** The Cloud Agent has everything needed to work autonomously and deliver a complete Writers Factory system.

🚀 **Let's build something amazing!**
