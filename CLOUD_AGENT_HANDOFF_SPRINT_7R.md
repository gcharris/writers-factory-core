# Cloud Agent Handoff: Sprint 7 Revision (TipTap Migration)

**Date**: November 14, 2025
**From**: Claude Code
**To**: Cloud Agent (deepseek-chat via cloud.anthropic.com)
**Priority**: CRITICAL (blocks January 2025 course launch)

---

## Context

**Situation**: You completed Sprint 7 (Markdown Editor) and Sprint 8 (Student Polish) successfully. However, Sprint 7's Toast UI Editor implementation has a **critical blocker**:

```
Build Error:
npm error ERESOLVE unable to resolve dependency tree
peer react@"^17.0.1" from @toast-ui/react-editor@3.2.3
react@"^19.2.0" from the root project
```

**Root Cause**: Toast UI Editor requires React 17, but Writers Factory uses React 19.

**Solution**: Replace Toast UI with **TipTap** (ProseMirror-based WYSIWYM editor).

**Why TipTap**:
- ✅ React 19 compatible (no peer dependency issues)
- ✅ Writer-first UX (WYSIWYM, not code-centric)
- ✅ Bidirectional Markdown support (parse + serialize)
- ✅ MIT-licensed (no vendor lock-in)
- ✅ Perfect for January course (familiar interface like Google Docs)

---

## Your Task

**Implement Sprint 7 Revision** as specified in:
**[CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md](CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md)**

**Estimated Time**: 4-6 hours

**Tasks**:
1. **7R-01**: Remove Toast UI dependencies, add TipTap packages
2. **7R-02**: Create TipTapEditor component with formatting toolbar
3. **7R-03**: Update SceneEditor to use TipTap instead of Toast UI
4. **7R-04**: Verify export functions still work (MD/TXT/HTML)
5. **7R-05**: Polish styling and UX (prose typography, toolbar states)
6. **7R-06**: Test and document (checklist, guide)

---

## What to Keep from Your Sprint 7 Work

**Keep (already excellent)**:
- ✅ `webapp/frontend-v2/src/utils/exporters.js` (243 lines) - Markdown export functions
- ✅ Word count logic (integrate with TipTap CharacterCount extension)
- ✅ Auto-save behavior (debounce, API calls)
- ✅ Dark mode support (if implemented)
- ✅ Distraction-free mode (if implemented)

**Replace**:
- ❌ All Toast UI code and imports
- ❌ Toast UI configuration
- ❌ `@toast-ui/editor` and `@toast-ui/react-editor` dependencies

---

## Critical Implementation Details

### 1. Bidirectional Markdown

**CRITICAL**: Set `contentType: 'markdown'` in useEditor config:

```jsx
const editor = useEditor({
  extensions: [/* ... */],
  content: props.initialContent || '',
  contentType: 'markdown',  // ← REQUIRED for MD round-trip
  onUpdate: ({ editor }) => {
    const markdown = editor.storage.markdown.getMarkdown()
    props.onChange?.(markdown)
  }
})
```

This enables:
- **Load**: Markdown → TipTap document (automatic parsing)
- **Save**: TipTap document → Markdown (via `editor.storage.markdown.getMarkdown()`)

### 2. Dependencies to Add

```json
{
  "@tiptap/react": "^2.9.0",
  "@tiptap/starter-kit": "^2.9.0",
  "@tiptap/extension-markdown": "^2.9.0",
  "@tiptap/extension-table": "^2.9.0",
  "@tiptap/extension-table-row": "^2.9.0",
  "@tiptap/extension-table-cell": "^2.9.0",
  "@tiptap/extension-table-header": "^2.9.0",
  "@tiptap/extension-task-list": "^2.9.0",
  "@tiptap/extension-task-item": "^2.9.0",
  "@tiptap/extension-image": "^2.9.0",
  "@tiptap/extension-link": "^2.9.0",
  "@tiptap/extension-placeholder": "^2.9.0",
  "@tiptap/extension-character-count": "^2.9.0"
}
```

### 3. Toolbar Button States

TipTap provides `editor.isActive()` for toolbar button highlighting:

```jsx
<button
  onClick={() => editor.chain().focus().toggleBold().run()}
  className={editor.isActive('bold') ? 'bg-blue-100 border-blue-400' : 'bg-white border-gray-300'}
>
  <Bold />
</button>
```

### 4. Word Count

Use CharacterCount extension:

```jsx
<div className="border-t bg-gray-50 p-2 text-sm flex justify-between">
  <span>Words: {editor.storage.characterCount.words()}</span>
  <span>Characters: {editor.storage.characterCount.characters()}</span>
</div>
```

---

## Testing Requirements

**Before marking complete**, verify:

### Build & Install
- [ ] `npm install` completes without errors
- [ ] No React version conflicts
- [ ] `npm run build` succeeds
- [ ] `npm run dev` starts dev server

### Functionality
- [ ] TipTap editor renders in SceneEditor
- [ ] All toolbar formatting buttons work (bold, italic, headings, lists, tables)
- [ ] Markdown round-trip: Load scene → edit → save → reload preserves formatting
- [ ] Auto-save triggers on content change
- [ ] Word count updates in real-time
- [ ] Export to MD/TXT/HTML works

### Edge Cases
- [ ] Very long content (10,000+ words)
- [ ] Special characters (em dashes, smart quotes)
- [ ] Nested lists
- [ ] Mixed formatting (bold + italic)
- [ ] Tables with merged cells (if supported)
- [ ] Paste from Word/Google Docs

---

## Success Criteria

**Definition of Done**:

1. ✅ Build succeeds with React 19 (no peer dependency errors)
2. ✅ TipTap editor fully functional (all formatting features work)
3. ✅ Markdown storage preserved (scenes still saved as `.md`)
4. ✅ Export functions work (MD/TXT/HTML)
5. ✅ Professional UX (clean toolbar, prose typography, word count)
6. ✅ Zero console errors
7. ✅ Testing checklist completed
8. ✅ Documentation created (TipTap usage guide)

---

## Reference Documentation

**TipTap Official Docs**:
- Getting Started: https://tiptap.dev/docs/editor/getting-started/install/react
- Markdown Extension: https://tiptap.dev/docs/editor/markdown
- Toolbar Example: https://tiptap.dev/docs/editor/guide/menus/toolbar
- Table Extension: https://tiptap.dev/docs/editor/extensions/nodes/table

**Your Sprint 7 Revision Spec**:
- [CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md](CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md) (700+ lines, complete implementation guide)

**Decision Rationale**:
- [EDITOR_DECISION_TIPTAP.md](EDITOR_DECISION_TIPTAP.md) (why TipTap vs Monaco/CodeMirror)

---

## Timeline

**Start**: Immediately
**Target Completion**: November 15, 2025 (end of day)
**Estimated Duration**: 4-6 hours

**Breakdown**:
- Task 7R-01 (Dependencies): 0.5 hours
- Task 7R-02 (TipTap Component): 2 hours
- Task 7R-03 (SceneEditor Update): 0.5 hours
- Task 7R-04 (Export Verification): 0.5 hours
- Task 7R-05 (Styling): 1 hour
- Task 7R-06 (Testing & Docs): 1.5 hours

---

## Deliverables

**Files to Create**:
1. `webapp/frontend-v2/src/features/editor/TipTapEditor.jsx` (350+ lines)
2. `TIPTAP_TESTING_CHECKLIST.md` (100 lines)
3. `TIPTAP_EDITOR_GUIDE.md` (80 lines)

**Files to Modify**:
1. `webapp/frontend-v2/package.json` (remove Toast UI, add TipTap)
2. `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (replace Toast UI with TipTap)
3. `webapp/frontend-v2/src/index.css` (add prose styling)

**Files to Delete**:
- (None - just remove imports/dependencies)

---

## Expected Output

**When complete, submit**:

1. **Code Review Request** with:
   - Link to branch/commit
   - Summary of changes (files modified, lines added/removed)
   - Screenshots of TipTap editor in action
   - Testing checklist results

2. **Build Verification**:
   ```bash
   npm install  # Should complete without errors
   npm run build  # Should succeed
   npm run dev  # Should start successfully
   ```

3. **Functional Demo**:
   - Screenshot/video showing:
     - Scene editor with TipTap
     - Formatting toolbar working
     - Word count updating
     - Markdown export

---

## What Not to Do

**Do NOT**:
- ❌ Try to fix Toast UI (it's fundamentally incompatible with React 19)
- ❌ Downgrade React to 17 (would break other dependencies)
- ❌ Use `--legacy-peer-deps` (masks the problem, doesn't solve it)
- ❌ Implement split-view mode (future enhancement, not required for January)
- ❌ Add collaboration features (future enhancement, not required for January)
- ❌ Modify Sprint 8 work (onboarding, help, examples - all good!)
- ❌ Change storage format (must remain Markdown `.md` files)

---

## Communication

**When stuck**:
1. Check TipTap official docs (link above)
2. Review [CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md](CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md) for detailed examples
3. Ask for clarification with specific error messages

**When complete**:
1. Create commit with descriptive message
2. Push to branch
3. Notify user with summary and demo

---

## Why This Matters

**January 2025 Course** depends on this:
- 30 students (Masters + Gymnasium)
- 5-day intensive "AI and the One-Week Novel"
- Students need **writer-first editing environment** (not programmer tools)
- TipTap provides familiar UX (like Google Docs/Word)
- Course is **6 weeks away** - this is the last critical blocker

**User Quote**: "This is a program for writers not programmers and they need a very good writing environment. This is a key necessity."

TipTap delivers on this requirement. Your implementation will enable the course to launch successfully.

---

## Ready?

**You have everything you need**:
- ✅ Complete implementation spec ([CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md](CLOUD_AGENT_SPRINT_7_REVISION_TIPTAP.md))
- ✅ Decision rationale ([EDITOR_DECISION_TIPTAP.md](EDITOR_DECISION_TIPTAP.md))
- ✅ Reference documentation (TipTap official docs)
- ✅ Clear success criteria
- ✅ Testing checklist
- ✅ Timeline and deliverables

**Go build!** 🚀

---

**Handoff Date**: November 14, 2025
**Expected Completion**: November 15, 2025
**Priority**: CRITICAL
**Blocker for**: January 2025 course launch
