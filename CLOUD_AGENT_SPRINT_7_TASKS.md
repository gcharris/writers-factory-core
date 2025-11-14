# 📋 Cloud Agent Sprint 7: Professional Markdown Editor

**Sprint**: 7 of 8
**Timeline**: 2-3 days
**Priority**: CRITICAL (Required for January course)
**Status**: Ready to start

---

## 🎯 Sprint Goal

Replace the basic textarea scene editor with a **professional markdown editor** featuring WYSIWYG editing, formatting toolbar, real-time preview, word count, and export functionality.

**Why Critical**: Graduate students taking the "AI and the One-Week Novel" course in January need a professional writing environment to create their novels/novellas.

**What Students Need**:
- Rich text formatting (bold, italic, headers, lists)
- Real-time markdown preview
- Persistent word count display
- Distraction-free writing mode
- Export to .md, .docx, PDF

---

## 📚 Technology Choice: Toast UI Editor

**Selected Editor**: [Toast UI Editor](https://github.com/nhn/tui.editor)

**Why Toast UI?**
- ✅ React component available (`@toast-ui/react-editor`)
- ✅ WYSIWYG + Markdown modes (switchable)
- ✅ Beautiful, professional UI
- ✅ Lightweight (~200KB gzipped)
- ✅ Active maintenance (NHN Corp)
- ✅ MIT license (free)
- ✅ Extensive plugin ecosystem
- ✅ Export plugins available

**Alternatives Considered**:
- MarkText: Electron app (not web-compatible)
- MDXEditor: Good but heavier, React 18+ only
- SimpleMDE: Minimalist but dated UI

**Documentation**: https://nhn.github.io/tui.editor/latest/

---

## ✅ Tasks (5 total)

### Task 7-01: Install Toast UI Editor & Basic Integration ⭐ CRITICAL

**Files**:
- `package.json` (MODIFY - add dependency)
- `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (MODIFY)

**Requirements**:

**1. Install Dependencies**

Add to `webapp/frontend-v2/package.json`:
```json
{
  "dependencies": {
    "@toast-ui/react-editor": "^3.2.2",
    "@toast-ui/editor": "^3.2.2"
  }
}
```

Then run:
```bash
cd webapp/frontend-v2
npm install
```

**2. Replace Textarea with Toast UI Editor**

Modify `SceneEditor.jsx` (currently around line 40-60):

**BEFORE**:
```jsx
<textarea
  value={content}
  onChange={(e) => handleContentChange(e.target.value)}
  className="w-full h-full bg-gray-900 text-gray-100 p-4 resize-none focus:outline-none"
  placeholder="Start writing your scene..."
/>
```

**AFTER**:
```jsx
import { Editor } from '@toast-ui/react-editor';
import '@toast-ui/editor/dist/toastui-editor.css';
import '@toast-ui/editor/dist/theme/toastui-editor-dark.css';

// Inside component:
const editorRef = useRef(null);

// Initialize editor content
useEffect(() => {
  if (editorRef.current && content) {
    const editorInstance = editorRef.current.getInstance();
    editorInstance.setMarkdown(content);
  }
}, [sceneId]); // Only run when scene changes

// Editor component
<Editor
  ref={editorRef}
  initialValue={content || "Start writing your scene..."}
  previewStyle="vertical"  // Side-by-side edit + preview
  height="100%"
  initialEditType="wysiwyg"  // Start in WYSIWYG mode
  useCommandShortcut={true}
  usageStatistics={false}
  theme="dark"
  onChange={() => {
    const editorInstance = editorRef.current.getInstance();
    const markdown = editorInstance.getMarkdown();
    handleContentChange(markdown);
  }}
  toolbarItems={[
    ['heading', 'bold', 'italic', 'strike'],
    ['hr', 'quote'],
    ['ul', 'ol', 'task'],
    ['table', 'link'],
    ['code', 'codeblock']
  ]}
/>
```

**3. Add Dark Theme Styles**

Add to `webapp/frontend-v2/src/index.css` (or create `webapp/frontend-v2/src/features/editor/EditorStyles.css`):

```css
/* Toast UI Editor Dark Theme Overrides */
.toastui-editor-defaultUI {
  border: none !important;
}

.toastui-editor-main-container {
  background-color: #1f2937 !important;
}

.toastui-editor-md-container,
.toastui-editor-ww-container {
  background-color: #111827 !important;
  color: #e5e7eb !important;
}

.toastui-editor-toolbar {
  background-color: #374151 !important;
  border-bottom: 1px solid #4b5563 !important;
}

.toastui-editor-toolbar-icons {
  color: #9ca3af !important;
}

.toastui-editor-toolbar-icons:hover {
  background-color: #4b5563 !important;
  color: #f3f4f6 !important;
}

/* Preview panel */
.toastui-editor-md-preview {
  background-color: #1f2937 !important;
  color: #e5e7eb !important;
}
```

**Success Criteria**:
- ✅ Toast UI Editor replaces textarea
- ✅ Dark theme applied consistently
- ✅ Toolbar shows with formatting options
- ✅ Content saves to backend (autosave still works)
- ✅ Editor loads existing scene content
- ✅ No console errors

---

### Task 7-02: Formatting Toolbar Customization ⭐ HIGH

**File**: `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (MODIFY)

**Requirements**:

**1. Enhanced Toolbar**

Replace the basic toolbar with a custom one optimized for novel writing:

```jsx
toolbarItems={[
  // Text formatting
  ['heading', 'bold', 'italic', 'strike'],

  // Paragraph tools
  ['hr', 'quote'],

  // Lists
  ['ul', 'ol'],

  // Advanced
  ['table', 'link', 'image'],

  // Code (for technical notes)
  ['code', 'codeblock'],

  // Custom buttons (we'll add these)
  [
    {
      el: createWordCountButton(),
      tooltip: 'Word Count',
      style: 'color: #10b981'
    },
    {
      el: createExportButton(),
      tooltip: 'Export Scene',
      style: 'color: #3b82f6'
    }
  ]
]}
```

**2. Add Custom Toolbar Buttons**

Add these functions before the component:

```jsx
function createWordCountButton() {
  const button = document.createElement('button');
  button.className = 'toastui-editor-toolbar-icons';
  button.innerHTML = '<span id="word-count-display">0 words</span>';
  button.style.cssText = 'color: #10b981; cursor: default; pointer-events: none;';
  return button;
}

function createExportButton() {
  const button = document.createElement('button');
  button.className = 'toastui-editor-toolbar-icons';
  button.innerHTML = '📥 Export';
  button.onclick = () => {
    // Export functionality (Task 7-04)
  };
  return button;
}
```

**3. Add Mode Toggle**

Add a toggle button to switch between WYSIWYG and Markdown:

```jsx
<div className="flex items-center gap-2 px-4 py-2 bg-gray-800 border-b border-gray-700">
  <button
    onClick={() => {
      const editor = editorRef.current.getInstance();
      editor.changeMode(editMode === 'wysiwyg' ? 'markdown' : 'wysiwyg');
      setEditMode(editMode === 'wysiwyg' ? 'markdown' : 'wysiwyg');
    }}
    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm"
  >
    {editMode === 'wysiwyg' ? 'Switch to Markdown' : 'Switch to WYSIWYG'}
  </button>

  <span className="text-gray-400 text-sm">
    {editMode === 'wysiwyg' ? 'Visual Editor' : 'Markdown Editor'}
  </span>
</div>

<Editor ref={editorRef} ... />
```

**Success Criteria**:
- ✅ Custom toolbar with novel-writing tools
- ✅ Mode toggle works (WYSIWYG ↔ Markdown)
- ✅ Custom buttons render correctly
- ✅ Toolbar is accessible and intuitive

---

### Task 7-03: Word Count & Writing Stats ⭐ HIGH

**File**: `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (MODIFY)

**Requirements**:

**1. Real-Time Word Count**

Add state and effect for word count:

```jsx
const [stats, setStats] = useState({
  words: 0,
  characters: 0,
  charactersNoSpaces: 0,
  paragraphs: 0,
  readingTime: 0
});

// Update stats on content change
const updateStats = (markdown: string) => {
  const text = markdown.replace(/[#*`_~[\]()]/g, ''); // Remove markdown syntax
  const words = text.trim().split(/\s+/).filter(w => w.length > 0).length;
  const characters = text.length;
  const charactersNoSpaces = text.replace(/\s/g, '').length;
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim().length > 0).length;
  const readingTime = Math.ceil(words / 200); // 200 words per minute

  setStats({
    words,
    characters,
    charactersNoSpaces,
    paragraphs,
    readingTime
  });

  // Update toolbar word count display
  const wordCountDisplay = document.getElementById('word-count-display');
  if (wordCountDisplay) {
    wordCountDisplay.textContent = `${words.toLocaleString()} words`;
  }
};

// In onChange handler:
onChange={() => {
  const editorInstance = editorRef.current.getInstance();
  const markdown = editorInstance.getMarkdown();
  updateStats(markdown);
  handleContentChange(markdown);
}}
```

**2. Stats Panel**

Add a stats panel below the editor:

```jsx
<div className="px-4 py-2 bg-gray-800 border-t border-gray-700 flex items-center justify-between text-sm">
  <div className="flex items-center gap-6 text-gray-400">
    <div>
      <span className="font-semibold text-gray-300">{stats.words.toLocaleString()}</span> words
    </div>
    <div>
      <span className="font-semibold text-gray-300">{stats.characters.toLocaleString()}</span> characters
    </div>
    <div>
      <span className="font-semibold text-gray-300">{stats.paragraphs}</span> paragraphs
    </div>
    <div>
      <span className="font-semibold text-gray-300">{stats.readingTime}</span> min read
    </div>
  </div>

  <div className="text-gray-400">
    Last saved: {lastSaved ? new Date(lastSaved).toLocaleTimeString() : 'Never'}
  </div>
</div>
```

**Success Criteria**:
- ✅ Word count updates in real-time
- ✅ Stats panel shows words, characters, paragraphs, reading time
- ✅ Last saved timestamp displayed
- ✅ Performance is smooth (no lag on typing)

---

### Task 7-04: Export Functionality ⭐ MEDIUM

**Files**:
- `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (MODIFY)
- `webapp/frontend-v2/src/utils/exporters.js` (NEW)

**Requirements**:

**1. Create Export Utilities**

Create `webapp/frontend-v2/src/utils/exporters.js`:

```javascript
/**
 * Export utilities for Writers Factory.
 * Handles exporting scenes/manuscripts to various formats.
 */

/**
 * Export content to Markdown file (.md)
 */
export function exportToMarkdown(title, content) {
  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.md`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Export content to plain text file (.txt)
 */
export function exportToText(title, content) {
  // Remove markdown formatting
  const plainText = content
    .replace(/[#*`_~[\]()]/g, '')
    .replace(/\n\n+/g, '\n\n');

  const blob = new Blob([plainText], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Export content to HTML file (.html)
 */
export function exportToHTML(title, content) {
  // Use Toast UI Editor's built-in converter
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    body {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      font-family: Georgia, serif;
      line-height: 1.6;
      color: #333;
    }
    h1 { font-size: 2em; margin-bottom: 0.5em; }
    h2 { font-size: 1.5em; margin-top: 1em; }
    p { margin: 1em 0; }
  </style>
</head>
<body>
  <h1>${title}</h1>
  ${convertMarkdownToHTML(content)}
</body>
</html>
  `.trim();

  const blob = new Blob([htmlContent], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.html`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Convert markdown to HTML (basic implementation)
 * For production, use a library like marked.js or remark
 */
function convertMarkdownToHTML(markdown) {
  return markdown
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(.+)$/gim, '<p>$1</p>');
}

/**
 * Sanitize filename (remove invalid characters)
 */
function sanitizeFilename(filename) {
  return filename
    .replace(/[<>:"/\\|?*]/g, '')
    .replace(/\s+/g, '_')
    .substring(0, 100);
}

/**
 * Export entire manuscript (all scenes combined)
 */
export async function exportManuscript(format = 'md') {
  // Fetch manuscript tree
  const response = await fetch('http://localhost:8000/api/manuscript/tree');
  const data = await response.json();

  let fullContent = `# ${data.title}\n\n`;

  // Iterate through acts, chapters, scenes
  for (const act of data.acts) {
    fullContent += `\n\n# ${act.title}\n\n`;

    for (const chapter of act.chapters) {
      fullContent += `\n## ${chapter.title}\n\n`;

      for (const scene of chapter.scenes) {
        // Fetch scene content
        const sceneResp = await fetch(`http://localhost:8000/api/manuscript/explants-v1/scenes/${scene.id}`);
        const sceneData = await sceneResp.json();

        fullContent += `\n### ${scene.title}\n\n`;
        fullContent += sceneData.content + '\n\n';
      }
    }
  }

  // Export based on format
  switch (format) {
    case 'md':
      exportToMarkdown(data.title, fullContent);
      break;
    case 'txt':
      exportToText(data.title, fullContent);
      break;
    case 'html':
      exportToHTML(data.title, fullContent);
      break;
    default:
      exportToMarkdown(data.title, fullContent);
  }
}
```

**2. Add Export Menu to SceneEditor**

Add export dropdown to toolbar:

```jsx
import { exportToMarkdown, exportToText, exportToHTML } from '../../utils/exporters';

// In component:
const [showExportMenu, setShowExportMenu] = useState(false);

const handleExport = (format) => {
  const editor = editorRef.current.getInstance();
  const content = editor.getMarkdown();
  const title = sceneTitle || 'Untitled Scene';

  switch (format) {
    case 'md':
      exportToMarkdown(title, content);
      toast.success('Scene exported as Markdown');
      break;
    case 'txt':
      exportToText(title, content);
      toast.success('Scene exported as plain text');
      break;
    case 'html':
      exportToHTML(title, content);
      toast.success('Scene exported as HTML');
      break;
  }

  setShowExportMenu(false);
};

// In JSX:
<div className="relative">
  <button
    onClick={() => setShowExportMenu(!showExportMenu)}
    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm flex items-center gap-2"
  >
    📥 Export
  </button>

  {showExportMenu && (
    <div className="absolute top-full right-0 mt-1 bg-gray-700 border border-gray-600 rounded shadow-lg z-10">
      <button
        onClick={() => handleExport('md')}
        className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm"
      >
        Export as Markdown (.md)
      </button>
      <button
        onClick={() => handleExport('txt')}
        className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm"
      >
        Export as Text (.txt)
      </button>
      <button
        onClick={() => handleExport('html')}
        className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm"
      >
        Export as HTML (.html)
      </button>
    </div>
  )}
</div>
```

**Success Criteria**:
- ✅ Export dropdown shows 3 formats (MD, TXT, HTML)
- ✅ Each format downloads correctly
- ✅ Filenames are sanitized and sensible
- ✅ Toast notification confirms export

---

### Task 7-05: Distraction-Free Mode ⭐ MEDIUM

**File**: `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (MODIFY)

**Requirements**:

**1. Add Distraction-Free Toggle**

Add state and button:

```jsx
const [isFullscreen, setIsFullscreen] = useState(false);

const toggleFullscreen = () => {
  setIsFullscreen(!isFullscreen);

  // Optional: Actually use browser fullscreen API
  if (!isFullscreen) {
    document.documentElement.requestFullscreen?.();
  } else {
    document.exitFullscreen?.();
  }
};

// Add keyboard shortcut
useEffect(() => {
  const handleKeyboard = (e) => {
    if (e.key === 'F11') {
      e.preventDefault();
      toggleFullscreen();
    }
    if (e.key === 'Escape' && isFullscreen) {
      toggleFullscreen();
    }
  };

  window.addEventListener('keydown', handleKeyboard);
  return () => window.removeEventListener('keydown', handleKeyboard);
}, [isFullscreen]);
```

**2. Add Fullscreen Button**

```jsx
<button
  onClick={toggleFullscreen}
  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm flex items-center gap-2"
  title="Distraction-free mode (F11)"
>
  {isFullscreen ? '🗗 Exit Fullscreen' : '🗖 Fullscreen'}
</button>
```

**3. Conditional Layout**

Wrap editor in conditional layout:

```jsx
<div className={isFullscreen ? 'fixed inset-0 z-50 bg-gray-900' : ''}>
  {isFullscreen && (
    <div className="absolute top-4 right-4 z-10">
      <button
        onClick={toggleFullscreen}
        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded text-sm"
      >
        Exit Fullscreen (Esc)
      </button>
    </div>
  )}

  <Editor
    ref={editorRef}
    height={isFullscreen ? '100vh' : '100%'}
    {...otherProps}
  />

  {!isFullscreen && <StatsPanel />}
</div>
```

**Success Criteria**:
- ✅ Fullscreen button toggles distraction-free mode
- ✅ F11 keyboard shortcut works
- ✅ Escape exits fullscreen
- ✅ Editor expands to full viewport
- ✅ Stats panel hidden in fullscreen (or minimal overlay)

---

## 🧪 Testing Checklist

After completing all tasks, test:

### Basic Functionality
1. ✅ Toast UI Editor loads without errors
2. ✅ Dark theme applied consistently
3. ✅ Toolbar buttons work (bold, italic, headers, lists)
4. ✅ Content saves to backend (autosave)
5. ✅ Switching scenes loads correct content

### Formatting Tools
6. ✅ WYSIWYG mode formats text correctly
7. ✅ Markdown mode shows raw markdown
8. ✅ Mode toggle switches between WYSIWYG/Markdown
9. ✅ Preview panel shows formatted output

### Word Count
10. ✅ Word count updates in real-time
11. ✅ Stats panel shows accurate numbers
12. ✅ Last saved timestamp updates

### Export
13. ✅ Export to Markdown downloads .md file
14. ✅ Export to Text downloads .txt file
15. ✅ Export to HTML downloads .html file (opens in browser)
16. ✅ Filenames are sanitized

### Distraction-Free
17. ✅ Fullscreen button works
18. ✅ F11 keyboard shortcut works
19. ✅ Escape exits fullscreen
20. ✅ Editor is usable in fullscreen mode

---

## 📦 Deliverables

### New Files (1):
1. `webapp/frontend-v2/src/utils/exporters.js` (~150 lines)

### Modified Files (2):
1. `webapp/frontend-v2/package.json` (+2 dependencies)
2. `webapp/frontend-v2/src/features/editor/SceneEditor.jsx` (+200-300 lines)

### Expected Line Count:
- SceneEditor.jsx modifications: ~250 lines
- exporters.js: ~150 lines
- CSS additions: ~50 lines

**Total new/modified code**: ~450 lines

---

## 💡 Implementation Tips

### Tip 1: Test Incrementally
After each task, test the editor:
1. Task 7-01: Verify basic editor works
2. Task 7-02: Verify toolbar customizations
3. Task 7-03: Verify word count accuracy
4. Task 7-04: Test each export format
5. Task 7-05: Test fullscreen mode

### Tip 2: Dark Theme is Critical
Students will be writing for hours. Dark theme reduces eye strain. Test that ALL parts of the editor use dark colors.

### Tip 3: Performance Matters
Word count should update without lag. Use debouncing if needed:
```jsx
const debouncedUpdateStats = useCallback(
  debounce((markdown) => updateStats(markdown), 300),
  []
);
```

### Tip 4: Mobile Considerations
While primarily desktop, test that the editor works on tablets. Toast UI is responsive by default.

### Tip 5: Autosave Integration
Ensure the existing autosave mechanism still works with Toast UI. Test by:
1. Type in editor
2. Wait 2 seconds
3. Refresh browser
4. Content should persist

---

## 🎯 Success Criteria

Sprint 7 is complete when:

1. ✅ Toast UI Editor replaces textarea
2. ✅ Dark theme applied throughout
3. ✅ Custom toolbar with novel-writing tools
4. ✅ Real-time word count and stats
5. ✅ Export to MD/TXT/HTML works
6. ✅ Distraction-free mode functional
7. ✅ Autosave still works
8. ✅ Build succeeds without errors
9. ✅ No console warnings
10. ✅ Testing checklist passes

---

## 📝 Notes for Students (January Course)

After Sprint 7, students will have:
- **Professional writing environment** (like Scrivener, but in browser)
- **WYSIWYG editing** (no markdown knowledge required)
- **Real-time stats** (word count, reading time)
- **Easy export** (take their work with them)
- **Distraction-free mode** (focus on writing)

This makes Writers Factory a **complete writing tool**, not just an AI assistant.

---

**Document Created**: November 14, 2025
**Sprint**: 7 of 8
**Estimated Effort**: 2-3 days
**Status**: Ready to start
**Priority**: CRITICAL for January course
