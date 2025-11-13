# Cloud Agent Package Summary

Complete package for autonomous Cloud Agent implementation of Writers Factory.

---

## Package Contents

### 📋 Quick Start
- **START_HERE.md** - First document for Cloud Agent to read
- **INITIAL_PROMPT_FOR_CLOUD_AGENT.txt** - Copy-paste prompt to start the conversation

### 📖 Master Instructions
- **PROMPT_Cloud_Agent_Master_Instructions.md** (20KB)
  - Complete work protocol
  - All 7 tasks with deliverables
  - Commit message format
  - Testing requirements
  - Success criteria (23 checkpoints)
  - Final report template

- **PROMPT_Cloud_Agent_Rebuild.md** (22KB)
  - Hybrid architecture vision
  - What exists vs what to build
  - Integration points
  - Technical specifications

### 📝 Task Specifications (7 Tasks)

1. **TASK_Storage_Session_Management.md** (16KB)
   - File-based JSON storage
   - Auto-save system
   - Cost tracking
   - Session history
   - Crash recovery

2. **TASK_Master_CLI.md** (23KB)
   - Rich TUI implementation
   - 5-stage navigation
   - Status bar design
   - Keyboard shortcuts
   - Cost dashboard

3. **TASK_Knowledge_Router.md** (20KB)
   - Cognee integration (local)
   - NotebookLM integration (optional)
   - Intelligent query routing
   - Knowledge system architecture

4. **TASK_Workflows_Module.md** (23KB)
   - Scene generation workflow
   - Scene enhancement workflow
   - Voice testing workflow
   - Cost integration

5. **TASK_Model_Comparison_Tool.md** (24KB)
   - Repurpose tournament system
   - Side-by-side comparison
   - Visual diff
   - User preference tracking

6. **TASK_Creation_Wizard.md** (35KB)
   - Conversational questionnaire
   - 5 phases (Foundation → Character → Plot → World → Symbolism)
   - Save the Cat! 15-beat structure
   - Find Your Voice tool
   - Story bible output (4,000-6,000 words)

7. **Integration & Polish** (in master instructions)
   - End-to-end testing
   - Documentation
   - Performance optimization

### 📚 Reference
- **TASK_UX_Design.md** (12KB)
  - Already completed by previous agent
  - Reference for UI implementation

### 📦 Upload Guide
- **UPLOAD_INSTRUCTIONS.md**
  - How to upload files to writers-factory-core
  - GitHub UI method
  - Command line method
  - Verification steps

---

## Total Package

- **Files**: 11 documents
- **Size**: ~197KB of specifications
- **Estimated Implementation**: 2-3 weeks
- **Tasks**: 7 sequential tasks
- **Tests Required**: Unit + Integration tests for all components

---

## How to Use This Package

### Step 1: Upload to Repository

Choose one method:

**Option A: GitHub UI** (Easiest)
1. Go to https://github.com/gcharris/writers-factory-core
2. Create `docs/tasks/` directory
3. Upload all files from this package
4. Commit: "Add all task specifications for Cloud Agent"

**Option B: Command Line**
```bash
cd ~/writers-factory-core
mkdir -p docs/tasks
cp cloud-agent-package/* docs/tasks/
git add docs/tasks/
git commit -m "Add all task specifications for Cloud Agent"
git push origin main
```

### Step 2: Start Cloud Agent

1. Open new conversation with Cloud Agent
2. Copy content from `INITIAL_PROMPT_FOR_CLOUD_AGENT.txt`
3. Paste into Cloud Agent conversation
4. Cloud Agent will read START_HERE.md and begin Task 1

### Step 3: Wait for Completion

Cloud Agent will:
- Work autonomously through all 7 tasks
- Commit and push after each task
- Continue without waiting for approval
- Report back when complete with final summary

---

## Expected Cloud Agent Workflow

### Week 1: Foundation
✅ Task 1: Storage & Session Management (3-4 hours)
✅ Task 2: Master CLI - Rich TUI (4-5 hours)

### Week 2: Integration
✅ Task 3: Knowledge Router (3-4 hours)
✅ Task 4: Workflows Module (4-5 hours)
✅ Task 5: Model Comparison Tool (3-4 hours)

### Week 3: Polish
✅ Task 6: Creation Wizard (6-8 hours)
✅ Task 7: Integration & Polish (2-3 hours)

### Final Deliverable
✅ Complete system with all 23 success criteria met
✅ Full test suite (unit + integration)
✅ Documentation updated
✅ Final report with commit summary

---

## Success Criteria (23 Total)

### Core Functionality (5)
1. Launch `factory start` → Rich TUI with 5-stage pipeline
2. Status bar shows stage progress, costs, auto-save
3. TAB/SHIFT+TAB navigates between stages
4. Auto-save runs every 30s without blocking
5. Cost tracking warns before expensive operations

### Knowledge System (4)
6. User can ask questions from any stage
7. Questions route to Cognee/NotebookLM intelligently
8. Users never see "Gemini File Search" option
9. Cognee is invisible to users

### Writing Workflows (3)
10. Generate scenes with knowledge context
11. Enhance existing scenes (voice, pacing, dialogue)
12. Run voice tests on scenes

### Model Comparison Tool (4)
13. Press 'C' in Writing stage → Comparison opens
14. Side-by-side shows 2-4 model outputs
15. Visual diff highlights differences
16. User selects winner → Preference saved

### Creation Wizard (4)
17. `factory init` → Conversational wizard starts
18. Wizard feels conversational, not form-like
19. 5 phases with marathon runner progress indicator
20. Output: 4,000-6,000 word story bible

### Session Management (3)
21. System crash → Session recovers on restart
22. User loses < 30 seconds of work
23. History shows last 20 sessions

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RICH TUI INTERFACE                        │
│  Status Bar: Creation ✓ | Writing ⚡ | Enhancing | Analyzing│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              5-STAGE WORKFLOW (Primary System)               │
│  Creation → Writing → Enhancing → Analyzing → Scoring       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     CORE SYSTEMS                             │
│  • Agent Pool ✅ (keep existing)                             │
│  • Knowledge Router 🏗️ (build)                              │
│  • Storage & Sessions 🏗️ (build)                            │
│  • Cost Tracker 🏗️ (build)                                  │
│  • Model Comparison Tool 🏗️ (repurpose tournament)          │
└─────────────────────────────────────────────────────────────┘
```

**Key Principle**: Tournament system becomes **one tool** within Writing stage, not the core architecture.

---

## Key Decisions Documented

### Storage Strategy
- **Sessions/Manuscript**: File-based JSON (easy backup, version control)
- **Analytics/Metrics**: SQLite (efficient queries, existing code)

### Knowledge System
- **Cognee**: Local, 17MB, hidden from users
- **NotebookLM**: External, optional, user-configured
- **Gemini File Search**: Not exposed to users

### Cost Tracking
- Warn before operations > $0.10
- Budget warnings at 80% of daily/weekly/monthly limits
- Log all operations with token counts

### UI Design
- Rich TUI (NOT basic CLI)
- Keyboard-first navigation
- Non-blocking async operations
- Status bar with auto-save indicator

---

## Package Location

```
/Users/gch2024/Documents/Documents - Mac Mini/Explant drafts current/
└── factory/docs/cloud-agent-package/
    ├── START_HERE.md
    ├── INITIAL_PROMPT_FOR_CLOUD_AGENT.txt
    ├── PACKAGE_SUMMARY.md (this file)
    ├── UPLOAD_INSTRUCTIONS.md
    ├── PROMPT_Cloud_Agent_Master_Instructions.md
    ├── PROMPT_Cloud_Agent_Rebuild.md
    ├── TASK_Storage_Session_Management.md
    ├── TASK_Master_CLI.md
    ├── TASK_Knowledge_Router.md
    ├── TASK_Workflows_Module.md
    ├── TASK_Model_Comparison_Tool.md
    ├── TASK_Creation_Wizard.md
    └── TASK_UX_Design.md
```

---

## Ready to Deploy!

This package contains everything the Cloud Agent needs to work autonomously for 2-3 weeks and deliver a complete, tested, documented Writers Factory system.

**Next steps**:
1. Upload package to `writers-factory-core/docs/tasks/`
2. Start Cloud Agent with initial prompt
3. Wait for completion report
4. Test the final system

🚀 Let's build something amazing!
