# Editor Decision: TipTap for Writers Factory

**Date**: November 14, 2025
**Decision**: Replace Toast UI with **TipTap**
**Reason**: User requirement for "very good writing environment" for writers (not programmers)

---

## The Problem

**Sprint 7** (Markdown Editor with Toast UI) has a critical blocker:
- Toast UI requires React 17
- Writers Factory uses React 19
- Build fails with peer dependency error

**Impact**: Cannot use Writers Factory until this is resolved
**Timeline**: 6 weeks until January course

---

## Options Evaluated

### Option 1: Monaco Editor (VS Code's Editor)
**Pros**:
- ✅ Already in dependencies (`@monaco-editor/react`)
- ✅ React 19 compatible
- ✅ Excellent for code/technical content
- ✅ Syntax highlighting for Markdown

**Cons**:
- ❌ **Code-centric UX** (built for programmers)
- ❌ Not designed for prose writing
- ❌ Minimal formatting toolbar
- ❌ Writers see code, not formatted text

**Verdict**: **REJECTED** - Violates user requirement ("not for programmers")

---

### Option 2: CodeMirror 6
**Pros**:
- ✅ React 19 compatible
- ✅ Modern, modular architecture
- ✅ Markdown highlighting available

**Cons**:
- ❌ **Source-mode focused** (writers see MD syntax)
- ❌ Requires assembly (multiple packages/plugins)
- ❌ Not writer-first UX
- ❌ More implementation complexity

**Verdict**: **REJECTED** - Still too code-centric

---

### Option 3: TipTap (ProseMirror-based WYSIWYM)
**Pros**:
- ✅ **Writer-first UX** (WYSIWYM - formatted text, not code)
- ✅ React 19 compatible
- ✅ **Professional prose editing** (inline formatting, block menus)
- ✅ **Bidirectional Markdown** (official extension)
- ✅ Familiar interface (looks like Google Docs/Word)
- ✅ **ProseMirror ecosystem** (collaboration, track changes, comments)
- ✅ Production-proven (used by many writing apps)
- ✅ Extensible (large plugin ecosystem)
- ✅ Lower learning curve for students

**Cons**:
- ⚠️ Requires more dependencies (~12 packages)
- ⚠️ Larger bundle size than Monaco

**Verdict**: ✅ **RECOMMENDED** - Best match for user requirements

---

## Decision Matrix

| Criterion | Monaco | CodeMirror 6 | TipTap | Weight |
|-----------|--------|--------------|--------|--------|
| **Writer-first UX** | ❌ Weak | ⚠️ Medium | ✅ **Strong** | 🔴 CRITICAL |
| **"Not for programmers"** | ❌ Fails | ⚠️ Marginal | ✅ **Passes** | 🔴 CRITICAL |
| React 19 compatible | ✅ Yes | ✅ Yes | ✅ Yes | 🔴 CRITICAL |
| Markdown round-trip | ⚠️ Basic | ✅ Good | ✅ **Official** | 🟡 Important |
| Familiar to students | ❌ No | ❌ No | ✅ **Yes** | 🟡 Important |
| Collaboration support | ⚠️ Custom | ⚠️ Possible | ✅ **Built-in** | 🟢 Nice-to-have |
| Implementation time | 🟢 Fast | 🟡 Medium | 🟡 Medium | 🟡 Important |
| Bundle size | 🟢 Small | 🟢 Small | 🟡 Medium | 🟢 Nice-to-have |

**Result**: TipTap wins on **all critical criteria** and most important criteria.

---

## Why TipTap is the Right Choice

### 1. Matches User Requirements (CRITICAL)
**User quote**: "This is a program for writers not programmers and they need a very good writing environment. This is a key necessity."

**TipTap delivers**:
- Writers see **formatted text**, not Markdown syntax
- Familiar interface (like Google Docs, not VS Code)
- Professional prose editing tools
- Lower learning curve

**Monaco/CodeMirror fail**:
- Writers see code/syntax
- Programmer-centric UX
- Unfamiliar to creative writers

### 2. Perfect for January Course
**Target audience**: Graduate engineering students writing novels

**TipTap advantages**:
- ✅ Intuitive (students won't struggle with editor)
- ✅ Professional appearance (builds confidence)
- ✅ Rich features students expect (tables, lists, formatting)
- ✅ Familiar (reduces cognitive load)

**Monaco disadvantage**:
- ❌ Students complain: "Why does this look like VS Code?"
- ❌ Focus on Markdown syntax, not story
- ❌ Steeper learning curve

### 3. Future-Proof Architecture
**ProseMirror ecosystem** provides:
- **Collaboration**: Real-time co-editing (potential future feature)
- **Track changes**: Revision history (useful for editing workflow)
- **Comments**: Inline annotations (useful for instructor feedback)
- **Custom extensions**: Can add craft-specific tools (e.g., beat markers)

**Monaco/CodeMirror**:
- Limited prose-specific features
- Collaboration requires custom implementation

### 4. Production-Proven
TipTap is used by:
- Notion (note-taking)
- GitBook (documentation)
- Grammarly (writing assistant)
- Many CMS platforms

**This means**:
- Mature, battle-tested
- Active development
- Large community
- Lots of examples/plugins

---

## Implementation Plan

**See**: [CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md](CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md)

**Summary**:
- **Task 7R-01**: Remove Toast UI, add TipTap dependencies
- **Task 7R-02**: Create TipTapEditor component with toolbar
- **Task 7R-03**: Update SceneEditor to use TipTap
- **Task 7R-04**: Verify export functions still work
- **Task 7R-05**: Polish styling and UX
- **Task 7R-06**: Test and document

**Estimated time**: 4-6 hours
**Risk level**: Low (TipTap is well-documented, React 19 compatible)

---

## What You Get with TipTap

### For Writers
- **WYSIWYM editing**: See formatted text while writing
- **Intuitive toolbar**: Bold, italic, headings, lists, tables
- **No Markdown knowledge required**: Just write naturally
- **Professional appearance**: Looks like a real writing tool

### For Instructors
- **Easy to teach**: Familiar interface (like Google Docs)
- **Rich content**: Students can use tables, images, links
- **Export flexibility**: Save as MD/TXT/HTML
- **Future collaboration**: ProseMirror supports real-time co-editing

### For Developers (You)
- **Clean API**: TipTap is well-designed, easy to extend
- **React 19 compatible**: No build issues
- **Markdown storage**: Still saves to `.md` files (portable)
- **Extensible**: Can add custom extensions for craft features

---

## Risks and Mitigations

### Risk 1: Larger Bundle Size
**Impact**: Medium (TipTap + extensions = ~200KB)
**Mitigation**:
- Use code splitting (load editor only when needed)
- Acceptable for modern web apps
- Writers Factory is not bandwidth-constrained

### Risk 2: Learning TipTap API
**Impact**: Low (Cloud Agent can handle this)
**Mitigation**:
- Excellent documentation
- Many examples available
- Simple API for basic use cases

### Risk 3: Migration from Toast UI
**Impact**: Low (both use Markdown as storage)
**Mitigation**:
- Markdown is portable (no lock-in)
- Export functions already work with MD
- No data migration needed

---

## Comparison: Before vs After

### Before (Toast UI)
```
Writer opens scene editor
↓
Sees code-like interface with MD syntax
↓
Types: **bold** for bold text
↓
Preview shows formatted text in separate pane
↓
Cognitive load: Must think in Markdown
```

### After (TipTap)
```
Writer opens scene editor
↓
Sees formatted text (like Google Docs)
↓
Clicks Bold button or types Ctrl+B
↓
Text is immediately bold (WYSIWYM)
↓
Cognitive load: Just write naturally
```

**Result**: Writers focus on story, not syntax.

---

## Final Recommendation

✅ **Use TipTap** for Writers Factory markdown editor

**Reasons**:
1. ✅ Matches user requirement ("not for programmers")
2. ✅ Provides "very good writing environment" (key necessity)
3. ✅ React 19 compatible (solves build issue)
4. ✅ Writer-first UX (WYSIWYM, not code-centric)
5. ✅ Perfect for January course (familiar, intuitive)
6. ✅ Future-proof (ProseMirror ecosystem)
7. ✅ Production-proven (used by major apps)

**Timeline**: 4-6 hours to implement (Sprint 7 Revision)
**Risk**: Low
**Value**: High (enables January course launch)

---

**Decision approved by**: Claude Code (with context from Cloud Agent analysis)
**Next step**: Cloud Agent implements Sprint 7 Revision
**Expected completion**: November 15, 2025
