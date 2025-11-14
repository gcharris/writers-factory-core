# Cloud Agent Sprint 7 Revision: TipTap Migration

**Assigned to**: Cloud Agent (deepseek-chat via cloud.anthropic.com)
**Priority**: CRITICAL (blocks January course)
**Estimated Duration**: 4-6 hours
**Dependencies**: Sprint 6 complete ✅

---

## Context

**Problem**: Sprint 7's Toast UI Editor has React 17 peer dependency, blocking build with React 19.

**User Requirement**: "This is a program for writers not programmers and they need a very good writing environment. This is a key necessity."

**Solution**: Replace Toast UI with TipTap (ProseMirror-based WYSIWYM editor)

**Why TipTap**:
- ✅ Writer-first UX (not code-centric like Monaco)
- ✅ React 19 compatible (no peer dependency issues)
- ✅ Professional prose editing (inline formatting, block menus, rich text)
- ✅ Bidirectional Markdown support (official extension)
- ✅ ProseMirror ecosystem (collaboration, track changes, comments available)
- ✅ Familiar to students (looks like Google Docs/Word)

---

## Sprint 7 Revision Tasks

### Task 7R-01: Remove Toast UI Dependencies

**Files to modify**:
- `webapp/frontend-v2/package.json`

**Actions**:
1. Remove these dependencies:
   ```json
   "@toast-ui/editor": "^3.2.2",
   "@toast-ui/react-editor": "^3.2.2"
   ```

2. Add TipTap dependencies:
   ```json
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
   ```

3. Run `npm install` to verify clean install with React 19

**Success Criteria**:
- ✅ `npm install` completes without peer dependency errors
- ✅ No React version conflicts
- ✅ Build succeeds (`npm run build`)

---

### Task 7R-02: Create TipTap Scene Editor Component

**File to create**: `webapp/frontend-v2/src/features/editor/TipTapEditor.jsx`

**Requirements**:

**1. Core Editor Setup**:
```jsx
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Markdown from '@tiptap/extension-markdown'
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import TaskList from '@tiptap/extension-task-list'
import TaskItem from '@tiptap/extension-task-item'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Placeholder from '@tiptap/extension-placeholder'
import CharacterCount from '@tiptap/extension-character-count'

const editor = useEditor({
  extensions: [
    StarterKit.configure({
      heading: { levels: [1, 2, 3, 4, 5, 6] },
      bulletList: { HTMLAttributes: { class: 'list-disc ml-4' } },
      orderedList: { HTMLAttributes: { class: 'list-decimal ml-4' } },
      blockquote: { HTMLAttributes: { class: 'border-l-4 border-gray-300 pl-4 italic' } },
      codeBlock: { HTMLAttributes: { class: 'bg-gray-100 p-4 rounded font-mono text-sm' } },
      horizontalRule: { HTMLAttributes: { class: 'my-4 border-t-2 border-gray-300' } }
    }),
    Markdown.configure({
      html: false,
      tightLists: true,
      tightListClass: 'tight',
      bulletListMarker: '-',
      linkify: true,
      breaks: true,
      transformPastedText: true,
      transformCopiedText: true
    }),
    Table.configure({ resizable: true }),
    TableRow,
    TableCell,
    TableHeader,
    TaskList,
    TaskItem.configure({ nested: true }),
    Image.configure({ inline: true, allowBase64: true }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: { class: 'text-blue-600 underline' }
    }),
    Placeholder.configure({
      placeholder: 'Start writing your scene...'
    }),
    CharacterCount
  ],
  content: props.initialContent || '',
  editable: !props.readOnly,
  autofocus: true,
  editorProps: {
    attributes: {
      class: 'prose prose-lg max-w-none focus:outline-none min-h-[500px] p-4'
    }
  },
  onUpdate: ({ editor }) => {
    const markdown = editor.storage.markdown.getMarkdown()
    props.onChange?.(markdown)
  }
})
```

**2. Formatting Toolbar**:
Create inline toolbar with these buttons:
- **Text formatting**: Bold, Italic, Strike, Code
- **Headings**: H1, H2, H3, H4
- **Lists**: Bullet List, Numbered List, Task List
- **Blocks**: Blockquote, Code Block, Horizontal Rule
- **Insert**: Table, Image, Link
- **Undo/Redo**: History controls

**Toolbar UI**:
```jsx
<div className="border-b border-gray-300 bg-gray-50 p-2 flex gap-1 flex-wrap sticky top-0 z-10">
  {/* Text Formatting */}
  <div className="flex gap-1 border-r border-gray-300 pr-2">
    <ToolbarButton
      onClick={() => editor.chain().focus().toggleBold().run()}
      active={editor.isActive('bold')}
      icon={<Bold />}
      title="Bold (Ctrl+B)"
    />
    <ToolbarButton
      onClick={() => editor.chain().focus().toggleItalic().run()}
      active={editor.isActive('italic')}
      icon={<Italic />}
      title="Italic (Ctrl+I)"
    />
    {/* ... more buttons ... */}
  </div>

  {/* Headings */}
  <div className="flex gap-1 border-r border-gray-300 pr-2">
    <select
      onChange={(e) => {
        const level = parseInt(e.target.value)
        if (level > 0) editor.chain().focus().toggleHeading({ level }).run()
        else editor.chain().focus().setParagraph().run()
      }}
      value={editor.isActive('heading') ? editor.getAttributes('heading').level : 0}
      className="px-2 py-1 border border-gray-300 rounded text-sm"
    >
      <option value="0">Paragraph</option>
      <option value="1">Heading 1</option>
      <option value="2">Heading 2</option>
      <option value="3">Heading 3</option>
      <option value="4">Heading 4</option>
    </select>
  </div>

  {/* Lists */}
  <div className="flex gap-1 border-r border-gray-300 pr-2">
    {/* Bullet, Numbered, Task lists */}
  </div>

  {/* Insert */}
  <div className="flex gap-1 border-r border-gray-300 pr-2">
    <ToolbarButton
      onClick={() => editor.chain().focus().insertTable({ rows: 3, cols: 3 }).run()}
      icon={<Table />}
      title="Insert Table"
    />
    <ToolbarButton
      onClick={() => {
        const url = window.prompt('Image URL')
        if (url) editor.chain().focus().setImage({ src: url }).run()
      }}
      icon={<Image />}
      title="Insert Image"
    />
    <ToolbarButton
      onClick={() => {
        const url = window.prompt('Link URL')
        if (url) editor.chain().focus().setLink({ href: url }).run()
      }}
      active={editor.isActive('link')}
      icon={<Link />}
      title="Insert Link"
    />
  </div>

  {/* Undo/Redo */}
  <div className="flex gap-1">
    <ToolbarButton
      onClick={() => editor.chain().focus().undo().run()}
      disabled={!editor.can().undo()}
      icon={<Undo />}
      title="Undo (Ctrl+Z)"
    />
    <ToolbarButton
      onClick={() => editor.chain().focus().redo().run()}
      disabled={!editor.can().redo()}
      icon={<Redo />}
      title="Redo (Ctrl+Shift+Z)"
    />
  </div>
</div>
```

**3. Word Count Display**:
```jsx
<div className="border-t border-gray-300 bg-gray-50 p-2 text-sm text-gray-600 flex justify-between">
  <span>Words: {editor.storage.characterCount.words()}</span>
  <span>Characters: {editor.storage.characterCount.characters()}</span>
</div>
```

**4. Props Interface**:
```jsx
TipTapEditor.propTypes = {
  initialContent: PropTypes.string,      // Markdown string
  onChange: PropTypes.func,              // (markdown: string) => void
  readOnly: PropTypes.bool,              // Disable editing
  placeholder: PropTypes.string,         // Placeholder text
  className: PropTypes.string            // Additional CSS classes
}
```

**Success Criteria**:
- ✅ Editor renders with toolbar
- ✅ All formatting buttons work
- ✅ Markdown round-trip (load MD → edit → save MD) preserves formatting
- ✅ Word count updates in real-time
- ✅ Keyboard shortcuts work (Ctrl+B, Ctrl+I, etc.)
- ✅ Tables, images, links insert correctly
- ✅ Task lists render with checkboxes

---

### Task 7R-03: Update SceneEditor Component

**File to modify**: `webapp/frontend-v2/src/features/editor/SceneEditor.jsx`

**Actions**:

1. **Remove Toast UI imports**:
```jsx
// DELETE THESE:
import { Editor } from '@toast-ui/react-editor'
import '@toast-ui/editor/dist/toastui-editor.css'
```

2. **Add TipTap import**:
```jsx
import TipTapEditor from './TipTapEditor'
```

3. **Replace editor component** (around line 200):
```jsx
// OLD (Toast UI):
<Editor
  ref={editorRef}
  initialValue={scene.content || ''}
  previewStyle="vertical"
  height="600px"
  initialEditType="wysiwyg"
  useCommandShortcut={true}
  onChange={handleEditorChange}
/>

// NEW (TipTap):
<TipTapEditor
  initialContent={scene.content || ''}
  onChange={handleEditorChange}
  placeholder="Start writing your scene..."
  className="border border-gray-300 rounded"
/>
```

4. **Update handleEditorChange**:
```jsx
// OLD:
const handleEditorChange = () => {
  const content = editorRef.current?.getInstance()?.getMarkdown()
  // ... save logic ...
}

// NEW:
const handleEditorChange = (markdown) => {
  // markdown is already provided by TipTap onChange callback
  // ... save logic ...
}
```

5. **Remove editorRef** (no longer needed):
```jsx
// DELETE:
const editorRef = useRef(null)
```

**Success Criteria**:
- ✅ SceneEditor component compiles without errors
- ✅ Scenes load correctly in TipTap editor
- ✅ Scene content saves to backend
- ✅ Auto-save triggers on content change
- ✅ No references to Toast UI remain

---

### Task 7R-04: Keep Export Functions from Sprint 7

**File to verify**: `webapp/frontend-v2/src/utils/exporters.js`

**Actions**:
1. Verify this file still works with TipTap (it should - operates on Markdown strings)
2. Test export to MD/TXT/HTML
3. Ensure HTML export handles TipTap's Markdown dialect

**No changes needed** unless bugs discovered during testing.

**Success Criteria**:
- ✅ Export to Markdown works
- ✅ Export to TXT works
- ✅ Export to HTML works
- ✅ Exported files preserve formatting

---

### Task 7R-05: Styling and Polish

**Files to modify**:
- `webapp/frontend-v2/src/features/editor/TipTapEditor.jsx` (styling)
- `webapp/frontend-v2/src/index.css` (global Tailwind prose classes)

**Requirements**:

**1. Prose Styling** (for editor content):
Add to `src/index.css`:
```css
/* TipTap Prose Styling */
.prose {
  @apply text-gray-900 leading-relaxed;
}

.prose h1 {
  @apply text-3xl font-bold mt-6 mb-4;
}

.prose h2 {
  @apply text-2xl font-bold mt-5 mb-3;
}

.prose h3 {
  @apply text-xl font-bold mt-4 mb-2;
}

.prose h4 {
  @apply text-lg font-semibold mt-3 mb-2;
}

.prose p {
  @apply mb-4;
}

.prose strong {
  @apply font-bold;
}

.prose em {
  @apply italic;
}

.prose code {
  @apply bg-gray-100 px-1 py-0.5 rounded text-sm font-mono;
}

.prose pre {
  @apply bg-gray-100 p-4 rounded overflow-x-auto;
}

.prose blockquote {
  @apply border-l-4 border-gray-300 pl-4 italic text-gray-700;
}

.prose ul {
  @apply list-disc ml-6 mb-4;
}

.prose ol {
  @apply list-decimal ml-6 mb-4;
}

.prose li {
  @apply mb-1;
}

.prose a {
  @apply text-blue-600 underline hover:text-blue-800;
}

.prose img {
  @apply max-w-full h-auto my-4 rounded;
}

.prose table {
  @apply border-collapse border border-gray-300 my-4 w-full;
}

.prose th {
  @apply border border-gray-300 bg-gray-100 px-4 py-2 font-semibold text-left;
}

.prose td {
  @apply border border-gray-300 px-4 py-2;
}

.prose hr {
  @apply my-6 border-t-2 border-gray-300;
}

/* Task List Styling */
.prose ul[data-type="taskList"] {
  @apply list-none ml-0;
}

.prose ul[data-type="taskList"] li {
  @apply flex items-start gap-2;
}

.prose ul[data-type="taskList"] li input[type="checkbox"] {
  @apply mt-1;
}
```

**2. Toolbar Button Component**:
Create reusable toolbar button:
```jsx
const ToolbarButton = ({ onClick, active, disabled, icon, title }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    title={title}
    className={`
      px-2 py-1 rounded border transition-colors
      ${active ? 'bg-blue-100 border-blue-400' : 'bg-white border-gray-300'}
      ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'}
    `}
  >
    {icon}
  </button>
)
```

**3. Distraction-Free Mode** (optional - keep if from Sprint 7):
If Cloud Agent implemented distraction-free mode in Sprint 7, keep it:
- Full-screen toggle button
- Hide toolbar/word count when in distraction-free mode
- ESC to exit

**Success Criteria**:
- ✅ Editor looks professional (clean, readable, polished)
- ✅ Toolbar buttons have hover states
- ✅ Active states show which formatting is applied
- ✅ Prose content is readable (good typography)
- ✅ Dark mode support (if implemented in Sprint 7)

---

### Task 7R-06: Testing and Documentation

**Actions**:

**1. Manual Testing Checklist**:
Create `TIPTAP_TESTING_CHECKLIST.md`:
```markdown
# TipTap Editor Testing Checklist

## Basic Functionality
- [ ] Editor loads with empty scene
- [ ] Editor loads with existing scene content
- [ ] Typing in editor works
- [ ] Auto-save triggers after edits
- [ ] Word count updates in real-time

## Formatting
- [ ] Bold (Ctrl+B)
- [ ] Italic (Ctrl+I)
- [ ] Strike
- [ ] Code
- [ ] Headings (H1-H4)
- [ ] Bullet lists
- [ ] Numbered lists
- [ ] Task lists
- [ ] Blockquotes
- [ ] Code blocks
- [ ] Horizontal rules

## Insert Features
- [ ] Insert table
- [ ] Resize table
- [ ] Insert image (URL)
- [ ] Insert link
- [ ] Edit link
- [ ] Remove link

## Undo/Redo
- [ ] Undo (Ctrl+Z)
- [ ] Redo (Ctrl+Shift+Z)

## Export
- [ ] Export to Markdown preserves formatting
- [ ] Export to TXT works
- [ ] Export to HTML works

## Edge Cases
- [ ] Very long content (10,000+ words)
- [ ] Special characters (em dashes, quotes)
- [ ] Nested lists
- [ ] Mixed formatting (bold + italic)
- [ ] Paste from Word/Google Docs

## Browser Compatibility
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari

## Performance
- [ ] No lag when typing
- [ ] Toolbar responsive
- [ ] Auto-save doesn't block UI
```

**2. Update README**:
Add section to `factory/mcp/README.md` or create `TIPTAP_EDITOR_GUIDE.md`:
```markdown
# TipTap Markdown Editor

Writers Factory uses **TipTap** (ProseMirror-based WYSIWYM editor) for scene editing.

## Features
- **Rich text editing**: Bold, italic, headings, lists
- **Markdown export**: Saves to `.md` format
- **Tables**: Insert and resize tables
- **Images**: Insert images via URL
- **Links**: Hyperlinks with preview
- **Task lists**: Checkboxes for to-do lists
- **Word count**: Real-time word/character count
- **Keyboard shortcuts**: Standard shortcuts (Ctrl+B, Ctrl+I, etc.)

## Why TipTap?
- **Writer-first UX**: WYSIWYM (What You See Is What You Mean)
- **Not code-centric**: No syntax highlighting clutter
- **Bidirectional Markdown**: Load and save Markdown seamlessly
- **Extensible**: ProseMirror ecosystem supports collaboration, comments, track changes

## Architecture
- **Core**: TipTap React wrapper
- **Extensions**: StarterKit, Markdown, Table, TaskList, Image, Link, Placeholder, CharacterCount
- **Storage format**: Markdown (`.md` files)
- **Export formats**: Markdown, TXT, HTML
```

**Success Criteria**:
- ✅ All checklist items pass
- ✅ Documentation created
- ✅ No critical bugs found

---

## Definition of Done

### Build and Install
- [ ] `npm install` completes without errors
- [ ] No React version conflicts
- [ ] `npm run build` succeeds
- [ ] `npm run dev` starts dev server

### Functionality
- [ ] TipTap editor renders in SceneEditor
- [ ] All formatting toolbar buttons work
- [ ] Markdown round-trip preserves formatting
- [ ] Auto-save works
- [ ] Word count displays correctly
- [ ] Export to MD/TXT/HTML works

### Code Quality
- [ ] No console errors
- [ ] No Toast UI references remain
- [ ] PropTypes defined for TipTapEditor
- [ ] Code follows existing style conventions

### Testing
- [ ] Manual testing checklist completed
- [ ] Edge cases tested
- [ ] Browser compatibility verified

### Documentation
- [ ] TipTap editor guide created
- [ ] Testing checklist documented
- [ ] Code comments added for complex logic

---

## Deliverables

### New Files
1. `webapp/frontend-v2/src/features/editor/TipTapEditor.jsx` (est. 350+ lines)
2. `TIPTAP_TESTING_CHECKLIST.md` (est. 100 lines)
3. `TIPTAP_EDITOR_GUIDE.md` (est. 80 lines)

### Modified Files
1. `webapp/frontend-v2/package.json` (remove Toast UI, add TipTap deps)
2. `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (replace Toast UI with TipTap)
3. `webapp/frontend-v2/src/index.css` (add prose styling)

### Removed
1. All references to `@toast-ui/editor` and `@toast-ui/react-editor`

---

## Success Metrics

### Before (Sprint 7 with Toast UI)
- ❌ Build fails with peer dependency error
- ❌ Cannot use with React 19
- ❌ Course blocked

### After (Sprint 7 Revision with TipTap)
- ✅ Build succeeds
- ✅ React 19 compatible
- ✅ Writer-first editing experience
- ✅ Ready for January course

---

## Timeline

**Estimated Duration**: 4-6 hours

**Breakdown**:
- Task 7R-01 (Dependencies): 0.5 hours
- Task 7R-02 (TipTap Component): 2 hours
- Task 7R-03 (SceneEditor Update): 0.5 hours
- Task 7R-04 (Export Verification): 0.5 hours
- Task 7R-05 (Styling): 1 hour
- Task 7R-06 (Testing & Docs): 1.5 hours

**Start Date**: November 14, 2025
**Target Completion**: November 15, 2025

---

## Notes for Cloud Agent

### Keep from Sprint 7
- Export functions (`exporters.js`) - already work with Markdown
- Word count logic - integrate into TipTap CharacterCount
- Auto-save behavior - keep existing debounce/API calls

### Abandon from Sprint 7
- All Toast UI code
- Toast UI configuration
- Toast UI CSS imports

### Key Implementation Details

**Markdown Round-Trip**:
TipTap's Markdown extension handles bidirectional conversion:
- **Load**: `editor.commands.setContent(markdownString)` → TipTap parses MD to ProseMirror doc
- **Save**: `editor.storage.markdown.getMarkdown()` → TipTap serializes doc to MD

**Toolbar State**:
TipTap provides `editor.isActive()` API:
```jsx
<button
  className={editor.isActive('bold') ? 'active' : ''}
  onClick={() => editor.chain().focus().toggleBold().run()}
>
  Bold
</button>
```

**Word Count**:
CharacterCount extension provides:
```jsx
editor.storage.characterCount.words()       // Word count
editor.storage.characterCount.characters()  // Character count
```

**Tables**:
Table extension provides commands:
```jsx
editor.chain().focus().insertTable({ rows: 3, cols: 3 }).run()
editor.chain().focus().deleteTable().run()
editor.chain().focus().addRowBefore().run()
editor.chain().focus().addColumnAfter().run()
```

### Reference Implementation
See TipTap docs for examples:
- Toolbar: https://tiptap.dev/docs/editor/guide/menus/toolbar
- Markdown: https://tiptap.dev/docs/editor/extensions/nodes/markdown
- Tables: https://tiptap.dev/docs/editor/extensions/nodes/table

---

**Priority**: CRITICAL
**Blocks**: January 2025 course launch
**Review Required**: Yes (after completion)
**Estimated Value**: $800-1,000 worth of work
