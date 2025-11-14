# Writers Factory Testing Plan

**Your Phased Approach** - From personal use → student testing → production app

---

## 🎯 Phase 1: Personal Testing (Next Few Days)

**Goal**: Use Writers Factory yourself, find bugs, verify core functionality

### Your Testing Workflow

**Setup** (one-time):
```bash
cd /Users/gch2024/writers-factory-core
./setup.sh
```

**Daily use**:
```bash
./start.sh
# Write in Writers Factory
# Report bugs as you find them
# Ctrl+C to stop
```

### Testing Checklist

#### 📝 **Core Writing Workflow**
- [ ] Create new project for The Explants Volume 2
- [ ] Import existing scenes from your manuscript folder
- [ ] Create new scene from scratch
- [ ] Edit existing scene
- [ ] Verify auto-save works
- [ ] Check word count updates
- [ ] Test file tree navigation

#### 🗂️ **File Management**
- [ ] Create new scene via right-click
- [ ] Rename scene
- [ ] Delete scene (and verify .md file deleted)
- [ ] Edit .md file externally (Typora/VS Code)
- [ ] Refresh Writers Factory, verify changes loaded

#### 🤖 **AI Features**
- [ ] Generate scene with local model (Ollama)
- [ ] Generate scene with cloud model (Claude/GPT)
- [ ] Enhance existing prose
- [ ] Try Tournament Mode (compare multiple models)
- [ ] Use Character Panel for analysis
- [ ] Check cost tracking

#### 💾 **Data Persistence**
- [ ] Close Writers Factory, reopen, verify scenes persist
- [ ] Edit scene, close without saving, verify auto-save worked
- [ ] Check manifest.json has no scene content (only metadata)
- [ ] Verify all scenes exist as .md files

### Bug Reporting

**When you find a bug**, create a note with:
1. **What you did** (exact steps)
2. **What happened** (the bug)
3. **What you expected** (correct behavior)
4. **Error messages** (check `.tmp/backend.log` and `.tmp/frontend.log`)

**Example**:
```
BUG: Scene deletion doesn't work
Steps: Right-click scene → Delete → Confirm
Result: Scene disappears from tree but .md file still exists
Expected: Both tree entry and .md file should be deleted
Logs: "Error deleting scene: Permission denied"
```

---

## 🎓 Phase 2: Student Testing (1-2 Weeks)

**Goal**: Have a few students use it, gather feedback, find edge cases

### Student Selection

**Ideal testers**:
- 2-3 students who are tech-savvy
- Mix of Mac/Windows users
- Interested in creative writing + AI
- Willing to give honest feedback

### Student Onboarding

**Send them**:
1. Repository link: `https://github.com/gcharris/writers-factory-core`
2. QUICK_START.md (clear setup instructions)
3. Testing tasks (see below)
4. Feedback form

**Onboarding meeting** (30 minutes):
- Live demo of setup process
- Show basic features
- Explain testing goals
- Answer questions

### Student Testing Tasks

#### Task 1: Installation (20 minutes)
**Goal**: Verify setup works across different environments

- Clone repository
- Run `./setup.sh`
- Document any errors
- Report time taken
- Report missing dependencies

**Questions**:
- Was setup process clear?
- Any confusing error messages?
- What would make it easier?

#### Task 2: Create Short Story (1 hour)
**Goal**: Test complete workflow from creation → writing → export

- Create new project: "Short Story"
- Plan structure (3-5 scenes)
- Write 500-1000 words per scene
- Use AI to generate one scene
- Use AI to enhance one scene
- Export manuscript (if export works)

**Questions**:
- Was the writing flow smooth?
- Did auto-save work reliably?
- Were AI suggestions helpful?
- Any frustrating moments?

#### Task 3: Collaboration Test (30 minutes)
**Goal**: Test external editing workflow

- Write scene in Writers Factory
- Edit same scene in VS Code/Typora
- Return to Writers Factory
- Verify changes appear

**Questions**:
- Did external edits sync properly?
- Any data loss?
- Confusing behavior?

#### Task 4: Breaking Things (20 minutes)
**Goal**: Find edge cases and crashes

Try to break it:
- Delete all scenes in a chapter
- Create scene with very long title (500 chars)
- Create 100 scenes rapidly
- Upload huge .md file (10MB)
- Use special characters in scene titles (emoji, Unicode)

**Report**:
- What caused crashes?
- What caused data loss?
- What caused confusion?

### Feedback Collection

**Create Google Form** with questions:
1. Overall experience (1-5 stars)
2. Ease of setup (1-5)
3. Writing workflow quality (1-5)
4. AI usefulness (1-5)
5. Most frustrating issue
6. Most helpful feature
7. What's missing?
8. Would you use this for a real project?

### Bug Prioritization

**P0 (Critical)**: Data loss, crashes, can't start app
**P1 (High)**: Core features broken (can't create scene, can't save)
**P2 (Medium)**: Annoying but workable (slow, UI glitch)
**P3 (Low)**: Nice-to-have improvements

---

## 🚀 Phase 3: Course Preparation (If Successful)

**If Phase 1 + 2 go well**, package for course students:

### Option A: Keep as Web App (Simpler)

**Provide students**:
1. GitHub repository link
2. QUICK_START.md guide
3. Pre-recorded setup video
4. Troubleshooting FAQ
5. Office hours for installation help

**Pros**:
- ✅ No packaging needed
- ✅ Easy to update/fix bugs
- ✅ Students learn Git workflow

**Cons**:
- ⚠️ Setup friction (some students will struggle)
- ⚠️ Requires terminal knowledge

### Option B: Desktop App (Easier for Students)

**Package as Electron app**:
1. Create `Writers Factory.app` (Mac)
2. Create `Writers Factory Setup.exe` (Windows)
3. Host on GitHub Releases

**Student experience**:
1. Download .app or .exe
2. Drag to Applications (Mac) or run installer (Windows)
3. Double-click to launch
4. Start writing

**Pros**:
- ✅ No setup friction
- ✅ "Just works"
- ✅ Professional feel

**Cons**:
- ⚠️ Packaging complexity (~2-3 days work)
- ⚠️ Need to support Mac + Windows
- ⚠️ Harder to update (need to download new version)

### Decision Point

**After student testing**, ask:
- How many students had setup issues?
- How much time did setup take?
- Did setup problems block anyone?

**If setup is easy** → Stay with web app
**If setup is painful** → Build desktop app

---

## 🐛 Common Issues to Test

### Backend Issues

- [ ] Python version mismatch (test with 3.9, 3.10, 3.11, 3.12)
- [ ] Missing Python packages
- [ ] Port 8000 already in use
- [ ] API key errors
- [ ] Ollama not installed/running
- [ ] File permission errors

### Frontend Issues

- [ ] Node version mismatch (test with 18, 20, 21)
- [ ] npm install fails
- [ ] Port 5173 already in use
- [ ] Browser compatibility (Chrome, Firefox, Safari)
- [ ] CORS errors
- [ ] React errors in console

### Data Issues

- [ ] Scene content loss
- [ ] Manifest corruption
- [ ] .md file not created
- [ ] .md file not deleted
- [ ] External edits not syncing
- [ ] Concurrent editing conflicts

### UX Issues

- [ ] Confusing UI elements
- [ ] Unclear error messages
- [ ] Missing feedback (e.g., "Saving...")
- [ ] Slow performance
- [ ] Unresponsive buttons

---

## 📊 Success Metrics

### Phase 1 (Personal Testing)
- [ ] You can write complete chapter in Writers Factory
- [ ] No data loss during normal use
- [ ] AI features work reliably
- [ ] External editing workflow smooth

### Phase 2 (Student Testing)
- [ ] 80%+ students successfully install
- [ ] 0 critical bugs (data loss, crashes)
- [ ] <5 high-priority bugs
- [ ] 4+ star average rating
- [ ] 70%+ would use for real project

### Phase 3 (Course Ready)
- [ ] All P0/P1 bugs fixed
- [ ] Clear documentation
- [ ] Easy setup (<10 minutes)
- [ ] Reliable AI integration
- [ ] Happy user feedback

---

## 🎬 Next Steps for You

### This Week
1. **Run `./setup.sh`** to set up Writers Factory
2. **Run `./start.sh`** to launch
3. **Create test project** or import Explants scenes
4. **Write for 30-60 minutes**, note any issues
5. **Document bugs** in a notes file
6. **Test file management** (create/rename/delete)
7. **Test AI features** (generate, enhance, tournament)

### Next Week
1. **Fix critical bugs** (if any found)
2. **Invite 2-3 test students**
3. **Send onboarding materials**
4. **Schedule onboarding call**
5. **Collect feedback** after they test

### Week 3-4
1. **Analyze feedback**
2. **Fix priority bugs**
3. **Decide**: Web app vs. desktop app
4. **If desktop app**: Start Electron packaging
5. **Prepare course materials**

---

## 💡 Testing Tips

### For You (Personal Testing)

1. **Use it for real work** - Write actual Explants scenes
2. **Try to break it** - Rapid clicks, weird inputs, edge cases
3. **Check logs** - Look at `.tmp/*.log` after errors
4. **External editing** - Edit in Typora, verify sync
5. **Different models** - Test local (Ollama) + cloud (Claude)

### For Students

1. **Fresh eyes** - They'll find things you miss
2. **Different environments** - Mac vs. Windows, different Node/Python versions
3. **Different workflows** - They'll use it differently than you
4. **Honest feedback** - Emphasize you want criticism, not praise
5. **Edge cases** - Students will do unexpected things

---

## 📝 Bug Tracking Template

Keep a `BUGS.md` file:

```markdown
# Writers Factory Bugs

## Critical (P0) - Fix Immediately
- [ ] BUG-001: Scene deletion crashes app
  - Steps: Right-click → Delete → Crash
  - Error: "Cannot read property 'id' of undefined"
  - Found by: Me (Nov 14)
  - Fixed: [commit hash]

## High Priority (P1) - Fix This Week
- [ ] BUG-002: External edits not syncing
  - Steps: Edit .md in VS Code → Reload WF → Old content shows
  - Found by: Student 1 (Nov 15)

## Medium Priority (P2) - Fix Before Course
- [ ] BUG-003: Slow startup (15 seconds)
  - Observation: Backend takes 10s to start
  - Found by: Me (Nov 14)

## Low Priority (P3) - Nice to Have
- [ ] BUG-004: File tree doesn't auto-expand
  - Observation: Have to manually expand acts every time
  - Found by: Student 2 (Nov 16)
```

---

## ✅ Ready to Test?

**Your immediate next steps**:

1. Open terminal
2. `cd /Users/gch2024/writers-factory-core`
3. `./setup.sh` (first time only)
4. `./start.sh`
5. Create project, start writing!
6. Report any issues you find

**Remember**: The goal is to find bugs NOW, not during the course!

**Good luck testing!** 🚀

---

**Questions while testing?** Create GitHub issues or make notes for later discussion.
