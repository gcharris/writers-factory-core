# Prompt for Bug Squashing Agent

## Mission: Find and Fix ALL the Bugs 🔨

Sprint 14 is **code complete** but **NOT tested**. Test everything. Break it. Fix it.

---

## Start Here

📄 **Read:** `BUG_SQUASHING_SESSION.md` - Complete context, test commands, bug patterns

---

## Quick Context

**What works:**
- ✅ `/api/setup/analyze-voice` - Tested and working

**What needs testing:**
- ⚠️ `/api/setup/generate-skills` - NOT TESTED
- ⚠️ `/api/setup/test-skill` - NOT TESTED  
- ⚠️ `/api/setup/create-project` - NOT TESTED

---

## Your Approach

1. Test `/api/setup/generate-skills` (command in BUG_SQUASHING_SESSION.md)
2. It will break. Read error in `/tmp/backend_final.log`
3. Fix bug in `webapp/backend/routes/setup.py`
4. Restart server
5. Repeat for other endpoints
6. Create 3 complete projects end-to-end
7. Commit all fixes

---

## Common Bugs (from first 5)

- Missing Anthropic client initialization
- Wrong parameter names
- Objects vs lists  
- Missing dependencies

**Expect similar bugs in untested endpoints!**

---

## Success

- ✅ All 4 endpoints work
- ✅ Create 3 projects (thriller, romance, literary)
- ✅ All bugs documented and fixed

---

## First Command

```bash
cat BUG_SQUASHING_SESSION.md  # Read full context

# Then test:
curl -X POST http://127.0.0.1:8000/api/setup/generate-skills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-thriller",
    "genre": "thriller",
    "examplePassages": ["She left. Quick."],
    "uploadedDocs": [],
    "notebooklmUrls": []
  }'
```

---

**Philosophy:** Stop planning. Start using. Fix what breaks.

**Budget:** ~$900 - Spend it to test thoroughly!

**Location:** `/Users/gch2024/writers-factory-core`  
**Branch:** `claude/task-14-continued-01UMjgFnnqVSwjZjwerw3nGw`  
**Server:** http://127.0.0.1:8000

**Let's squash them all!** 🚀
