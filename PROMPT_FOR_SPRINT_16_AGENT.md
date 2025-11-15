# Prompt for Sprint 16 Implementation Agent

## Mission: Build Multi-Notebook Management UI 🎯

**Sprint:** 16 - Multi-Notebook Management & UI
**Priority:** HIGH - Required for January course
**Timeline:** 2 weeks
**Dependencies:** Sprint 15 ✅ Complete

---

## What You're Building

**The Problem:**
Sprint 11 built multi-notebook backend (storage, queries, auto-selection), but NO UI to manage notebooks. Users must edit JSON files manually.

**Your Solution:**
Build UI-driven notebook management so users can add/manage NotebookLM notebooks through the Setup Wizard and Project Settings - NO manual JSON editing required!

---

## Read These Files First

1. **SPRINT_16_MULTI_NOTEBOOK_MANAGEMENT.md** - Complete specification (1,200 lines)
2. **docs/NOTEBOOKLM_CURRENT_STATE.md** - What we already have (Sprint 11)
3. **SPRINT_15_NOTEBOOKLM_BEGINNER_MODE.md** - Sprint 15 integration points

---

## Your 2-Week Plan

### **Week 1: Backend API Endpoints**

**Goal:** Add CRUD operations for notebook management

**Build:**
1. `webapp/backend/routes/notebooks.py` (NEW)
   - `POST /api/research/notebooks/add` - Add notebook to project
   - `PUT /api/research/notebooks/{id}` - Update notebook metadata
   - `DELETE /api/research/notebooks/{id}` - Remove notebook
   - `POST /api/research/notebooks/test` - Test URL connectivity
   - `GET /api/research/notebooks/{id}/stats` - Get usage statistics

2. Update `webapp/backend/simple_app.py`
   - Import and register notebooks router
   - Update `/api/research/query` to track usage stats

3. Tests: `tests/test_notebook_management.py`

**Success:** All 5 endpoints working, notebooks.json updated via API

---

### **Week 2: Frontend Components**

**Goal:** Build UI for notebook management

**Build:**
1. `webapp/frontend-v2/src/features/setup/NotebookSetupStep.jsx` (NEW)
   - Checkbox list of notebook types (Ideas, Characters, Structure, Research)
   - URL input fields
   - "Test Connection" buttons
   - Validation and error handling
   - Integration with Setup Wizard (Step 4)

2. `webapp/frontend-v2/src/features/notebooks/NotebookManager.jsx` (NEW)
   - Display all notebooks in cards
   - Show usage statistics (query count, last used)
   - Add/Edit/Remove buttons
   - Tag display
   - Add to Project Settings

3. Update `webapp/frontend-v2/src/features/setup/ProjectSetupWizard.jsx`
   - Add Step 4: "Connect NotebookLM (Optional)"
   - Route to NotebookSetupStep component

4. E2E tests: `tests/test_notebook_ui.py`

**Success:** Complete UI workflow works end-to-end

---

## Key Technical Decisions

### **1. Notebook Types (Pre-defined Categories)**

```python
NOTEBOOK_TYPES = {
    "ideas": {
        "name": "Ideas & World-Building",
        "tags": ["ideas", "creative", "plot", "world-building"]
    },
    "characters": {
        "name": "Character Profiles",
        "tags": ["characters", "backstories", "relationships"]
    },
    "structure": {
        "name": "Story Structure",
        "tags": ["structure", "planning", "chapters", "acts"]
    },
    "research": {
        "name": "Research & References",
        "tags": ["research", "references", "sources"]
    },
    "custom": {
        "name": "Custom Notebook",
        "tags": []
    }
}
```

**Why:** Auto-categorization for better auto-selection in queries

---

### **2. Enhanced notebooks.json Schema**

```json
[
    {
        "id": "nb-abc123",
        "name": "Ideas & World-Building",
        "url": "https://notebooklm.google.com/notebook/abc",
        "description": "Creative flashes, plot development",
        "notebook_type": "ideas",
        "tags": ["ideas", "creative", "plot"],
        "use_count": 47,
        "last_used": "2025-11-15T14:30:00Z",
        "created_at": "2025-11-01T10:00:00Z"
    }
]
```

**New Fields:**
- `notebook_type` - Category (ideas/characters/structure/research/custom)
- `use_count` - Incremented on each query
- `last_used` - Updated on each query

---

### **3. URL Validation Strategy**

```python
def validate_notebooklm_url(url: str) -> bool:
    """Validate NotebookLM URL format."""
    return url.startswith("https://notebooklm.google.com/notebook/")
```

**Full connectivity test is optional** (too slow for real-time validation)
**Format validation is required** (instant feedback)

---

### **4. Usage Tracking**

**Update on every query:**
```python
# In /api/research/query endpoint
notebooks = _load_project_notebooks(project_id)
for nb in notebooks:
    if nb["id"] == selected_notebook_id:
        nb["use_count"] = nb.get("use_count", 0) + 1
        nb["last_used"] = datetime.now().isoformat()
_save_project_notebooks(project_id, notebooks)
```

---

## Common Pitfalls to Avoid

### **Pitfall 1: Not Handling Duplicate URLs**

**Wrong:** Allow same URL to be added multiple times
**Right:** Check for duplicates before adding

```python
if any(nb["url"] == url for nb in notebooks):
    raise HTTPException(400, "Notebook URL already exists")
```

---

### **Pitfall 2: Slow Connection Testing**

**Wrong:** Query NotebookLM for every URL validation
**Right:** Only validate format by default, test connection on user request

```python
# Fast (instant)
validate_url_format(url)  # Just regex check

# Slow (optional, user-triggered)
test_notebook_connection(url)  # Actual browser automation
```

---

### **Pitfall 3: Not Integrating with Sprint 15**

**Remember:** Sprint 15 beginner mode uses single NotebookLM URL

**Solution:** Same component, different modes

```jsx
// Beginner mode (Sprint 15)
<NotebookSetupStep
  beginnerMode={true}  // Single URL input only
  onComplete={extractVoiceAndGenerateStarterSkills}
/>

// Experienced mode (Sprint 16)
<NotebookSetupStep
  beginnerMode={false}  // Multi-notebook selection
  onComplete={handleNext}
/>
```

---

## Testing Strategy

### **Unit Tests (Week 1)**

```bash
pytest tests/test_notebook_management.py -v
```

**Coverage targets:**
- Notebook CRUD: 95%+
- URL validation: 100%
- Usage tracking: 90%+

**Test cases:**
- `test_add_notebook_success`
- `test_add_notebook_duplicate_url`
- `test_add_notebook_invalid_url`
- `test_update_notebook`
- `test_remove_notebook`
- `test_usage_tracking_increments`
- `test_notebook_not_found`

---

### **Integration Tests (Week 2)**

```bash
pytest tests/test_notebook_integration.py -v
```

**Test flow:**
1. Create project via Setup Wizard
2. Add 3 notebooks (Ideas, Characters, Structure)
3. Test URL validation
4. Query notebook (verify auto-selection)
5. Check usage stats updated
6. Remove notebook
7. Verify notebook deleted

---

### **User Acceptance Testing (Week 2)**

**Recruit 5 beta testers:**
- 2 with existing NotebookLM notebooks
- 2 beginners (Sprint 15 flow)
- 1 advanced user (custom notebooks)

**Give them:**
- Access to dev environment
- Instructions: "Set up project with NotebookLM notebooks"
- Survey after completion

**Success criteria:**
- 5/5 complete setup without blocking bugs
- 4/5 successfully add 2+ notebooks
- 4/5 report UI is intuitive

---

## Success Criteria

**Sprint 16 is DONE when:**

- [ ] 5 new API endpoints working (`/api/research/notebooks/*`)
- [ ] Setup Wizard includes NotebookLM step (Step 4)
- [ ] User can add 1-5 notebooks during setup
- [ ] URL validation works (format check)
- [ ] "Test Connection" button works (optional connectivity test)
- [ ] Notebooks saved to `notebooks.json` automatically
- [ ] Project Settings has Notebooks tab
- [ ] Can add/edit/remove notebooks via UI
- [ ] Usage statistics displayed (query count, last used)
- [ ] Integrates with Sprint 15 beginner mode
- [ ] All tests pass (unit + integration)
- [ ] 5 beta testers complete workflow successfully

---

## Integration with Existing Code

### **Sprint 11 Already Has:**

✅ `NotebookLMClient` - Query notebooks via Playwright
✅ `POST /api/research/query` - Query with auto-selection
✅ `GET /api/research/notebooks` - List notebooks
✅ `notebooks.json` storage format
✅ Tag-based auto-selection logic

**You're adding:**
- CRUD API for notebook management
- Usage statistics tracking
- Setup Wizard UI integration
- Project Settings UI
- URL validation

**Don't break:**
- Existing query endpoint
- Auto-selection logic
- Sprint 15 beginner flow

---

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│  USER: Project Setup                     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  SETUP WIZARD - Step 4 (NEW)            │
│  "Connect NotebookLM (Optional)"        │
│                                          │
│  ☑ Ideas & World-Building               │
│     [URL] [Test ✓]                      │
│  ☑ Character Profiles                   │
│     [URL] [Test ✓]                      │
│  ☑ Story Structure                      │
│     [URL] [Test ✓]                      │
│                                          │
│  [Skip] or [Continue]                   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  POST /api/research/notebooks/add       │
│  (For each selected notebook)           │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  notebooks.json (Auto-saved)            │
│                                          │
│  [                                       │
│    {                                     │
│      "id": "nb-abc",                     │
│      "name": "Ideas & World-Building",  │
│      "url": "https://...",              │
│      "tags": ["ideas", "creative"],     │
│      "use_count": 0,                    │
│      "last_used": null                  │
│    }                                     │
│  ]                                       │
└─────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  USER: Writing Scenes                    │
│  Query: "What is Mickey's arc?"         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  POST /api/research/query               │
│  (Auto-selects Character notebook)      │
│  (Updates use_count, last_used)         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  NotebookLMClient.query()               │
│  (Browser automation via Playwright)    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  USER: Sees answer with citations       │
└─────────────────────────────────────────┘
```

---

## Dependencies

**Python packages (already installed):**
- fastapi
- httpx
- playwright
- anthropic

**Frontend packages (already installed):**
- react
- @mui/material

**New dependencies:** None!

---

## Resources

**Code references:**
- Existing NotebookLM: `factory/research/notebooklm_client.py`
- Existing query endpoint: `webapp/backend/simple_app.py` (lines 756-820)
- Existing Setup Wizard: `webapp/frontend-v2/src/features/setup/ProjectSetupWizard.jsx`
- Sprint 15 components: `webapp/frontend-v2/src/features/beginner/`

**Documentation:**
- Sprint 16 spec: `SPRINT_16_MULTI_NOTEBOOK_MANAGEMENT.md`
- Current state: `docs/NOTEBOOKLM_CURRENT_STATE.md`
- Architecture: `docs/KNOWLEDGE_SYSTEMS_ARCHITECTURE.md`

**Budget:** Unlimited - use APIs freely for testing

---

## Communication

**Daily standups (async):**
Post to GitHub Discussions:
- What you completed yesterday
- What you're working on today
- Any blockers

**End of week demos:**
- Week 1: Show all 5 API endpoints working with Postman/curl
- Week 2: Show complete Setup Wizard flow with notebooks

**Final deliverable:**
- Pull request with all code
- E2E test passing
- Documentation updated
- 5 beta testers completed flow

---

## Let's Build This! 🚀

You're building the UI layer that makes multi-notebook architecture user-friendly. No more manual JSON editing!

**Start with Week 1: Backend API Endpoints**

First file to create: `webapp/backend/routes/notebooks.py`

Good luck! 🎯
