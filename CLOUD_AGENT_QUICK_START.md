# Cloud Agent Quick Start

**Primary Document**: Read `CLOUD_AGENT_SPRINT_1_2.md` for full details

---

## TL;DR

Build a **Cursor AI-style web UI** for Writers Factory.

**Tech Stack**: React + Vite + Tailwind + Monaco Editor
**Backend**: Already done (FastAPI, 23 AI models, real AI integration)
**Your Job**: Build the frontend

---

## Sprint 1 (3-4 days)

Create `webapp/frontend-v2/` with:

1. **S1-01**: React + Vite scaffold with 3-pane layout
2. **S1-02**: Manuscript Explorer (Acts → Chapters → Scenes tree)
3. **S1-03**: Monaco Editor with autosave
4. **S1-04**: Setup Wizard for API keys

**Also**: Add 3 backend endpoints to `webapp/backend/simple_app.py`:
- GET /api/manuscript/tree
- GET /api/scene/{id}
- PUT /api/scene/{id}

---

## Sprint 2 (2-3 days)

Add to right panel:

1. **S2-01**: AI Tools tab (Generate, Enhance, Continue templates)
2. **S2-02**: Knowledge tab (Cognee/NotebookLM query)
3. **S2-03**: Tournament Compare (2-4 model comparison grid)

---

## Design Requirements

✅ **SIMPLE** - Cursor AI style, not fancy webapp
✅ **DARK THEME** - Gray backgrounds, minimal colors
✅ **TEXT-FOCUSED** - No graphics or animations
✅ **CLEAN** - Professional writer's tool

❌ **NO** fancy graphics
❌ **NO** colorful dashboards
❌ **NO** cluttered UI

---

## Key Files to Read

1. `webapp/backend/simple_app.py` - Existing API endpoints
2. `factory/core/manuscript/structure.py` - Manuscript models
3. `PHASE_3_REVIEW.md` - What's already built
4. `COMPLETE_INVENTORY.md` - Full system overview

---

## Testing

**Backend** (should already pass):
```bash
pytest tests/ -v
# Should show: 156 tests passing
```

**Frontend** (after you build):
```bash
cd webapp/frontend-v2
npm run dev
# Open http://localhost:5173
```

---

## Success Criteria

**Sprint 1 Done**:
- [ ] Tree navigation works
- [ ] Click scene → loads in Monaco editor
- [ ] Autosave after 2s
- [ ] Cmd+S manual save
- [ ] Setup wizard on first run

**Sprint 2 Done**:
- [ ] AI Tools generate/enhance works
- [ ] Knowledge query works (both sources)
- [ ] Tournament compare shows 2-4 outputs
- [ ] Clean, simple UI throughout

---

## Important Notes

- **Keep existing frontend** at `webapp/frontend/` as backup
- **Create new** at `webapp/frontend-v2/`
- **Don't modify** factory/ or tests/ (backend already works)
- **Do modify** `webapp/backend/simple_app.py` (add 3 endpoints)
- **Use Monaco Editor** (same as VS Code uses)
- **Dark theme only** (writer-friendly)

---

## Timeline

- **Sprint 1**: ~3-4 days
- **Sprint 2**: ~2-3 days
- **Total**: ~5-7 days

---

## Questions?

Read `CLOUD_AGENT_SPRINT_1_2.md` for:
- Complete component code
- API endpoint implementations
- File structure
- Testing requirements
- Detailed acceptance criteria

**Ready to code!** 🚀
