import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import Table from '@tiptap/extension-table';
import TableRow from '@tiptap/extension-table-row';
import TableCell from '@tiptap/extension-table-cell';
import TableHeader from '@tiptap/extension-table-header';
import TaskList from '@tiptap/extension-task-list';
import TaskItem from '@tiptap/extension-task-item';
import Highlight from '@tiptap/extension-highlight';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import { common, createLowlight } from 'lowlight';
import { useDebounce } from '../../hooks/useDebounce';
import { exportToMarkdown, exportToText, exportToHTML } from '../../utils/exporters';
import { showFriendlyError } from '../../utils/errorHandler';
import {
  Bold, Italic, Strikethrough, Code, Heading1, Heading2, Heading3,
  List, ListOrdered, Quote, Minus, Link as LinkIcon, Image as ImageIcon,
  Table as TableIcon, CheckSquare, Highlighter, Code2, Maximize2, Minimize2
} from 'lucide-react';
import './editor-styles.css';

const lowlight = createLowlight(common);

export function SceneEditor({ sceneId }) {
  const [lastSaved, setLastSaved] = useState(null);
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [stats, setStats] = useState({
    words: 0,
    characters: 0,
    charactersNoSpaces: 0,
    paragraphs: 0,
    readingTime: 0
  });
  const queryClient = useQueryClient();

  // Initialize TipTap editor
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        codeBlock: false, // Disable default code block to use CodeBlockLowlight
      }),
      Link.configure({
        openOnClick: false,
        HTMLAttributes: {
          class: 'text-blue-400 underline hover:text-blue-300',
        },
      }),
      Image.configure({
        HTMLAttributes: {
          class: 'max-w-full h-auto rounded',
        },
      }),
      Table.configure({
        resizable: true,
        HTMLAttributes: {
          class: 'border-collapse table-auto w-full',
        },
      }),
      TableRow,
      TableHeader,
      TableCell,
      TaskList.configure({
        HTMLAttributes: {
          class: 'not-prose',
        },
      }),
      TaskItem.configure({
        nested: true,
      }),
      Highlight.configure({
        multicolor: true,
      }),
      CodeBlockLowlight.configure({
        lowlight,
        HTMLAttributes: {
          class: 'bg-gray-800 rounded p-4 my-4',
        },
      }),
    ],
    editorProps: {
      attributes: {
        class: 'prose prose-invert max-w-none focus:outline-none min-h-[500px] px-8 py-6',
      },
    },
    onUpdate: ({ editor }) => {
      const text = editor.getText();
      updateStats(text);
    },
  });

  // Calculate writing stats
  const updateStats = (text) => {
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
  };

  // Load scene
  const { data: scene, isLoading } = useQuery({
    queryKey: ['scene', sceneId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`);
      if (!res.ok) {
        const error = new Error('Failed to load scene');
        error.status = res.status;
        throw error;
      }
      return res.json();
    },
    enabled: !!sceneId,
    onError: (error) => {
      showFriendlyError(error, toast, { type: 'scene' });
    }
  });

  // Update editor content when scene loads
  useEffect(() => {
    if (scene?.content && editor) {
      // Convert markdown to HTML for TipTap
      // For now, just set as HTML (TipTap handles markdown-style text well)
      editor.commands.setContent(scene.content);
      updateStats(editor.getText());
    }
  }, [scene?.id, editor]);

  // Get content for saving (convert to markdown)
  const getEditorContent = () => {
    if (!editor) return '';
    // Get HTML content
    const html = editor.getHTML();
    // For markdown export, we'll use the text with basic formatting
    // TipTap stores as HTML, we'll convert to markdown on export
    return html;
  };

  // Debounced content for autosave
  const currentContent = editor ? getEditorContent() : '';
  const debouncedContent = useDebounce(currentContent, 2000);

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async (newContent) => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
      if (!res.ok) {
        const error = new Error('Save failed');
        error.status = res.status;
        throw error;
      }
      return res.json();
    },
    onSuccess: () => {
      setLastSaved(new Date());
      queryClient.invalidateQueries(['manuscript-tree']);
    },
    onError: (error) => {
      showFriendlyError(error, toast, { type: 'scene' });
    }
  });

  // Autosave when content changes
  useEffect(() => {
    if (debouncedContent && debouncedContent !== scene?.content && editor) {
      saveMutation.mutate(debouncedContent);
    }
  }, [debouncedContent]);

  // Manual save on Cmd+S
  useEffect(() => {
    const handleSave = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        if (editor) {
          saveMutation.mutate(getEditorContent());
          toast.success('Saved');
        }
      }
    };
    window.addEventListener('keydown', handleSave);
    return () => window.removeEventListener('keydown', handleSave);
  }, [editor, sceneId]);

  // Fullscreen keyboard shortcuts
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

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);

    if (!isFullscreen) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  };

  const handleExport = (format) => {
    if (!editor) return;

    const title = scene?.title || 'Untitled Scene';
    const text = editor.getText();
    const html = editor.getHTML();

    switch (format) {
      case 'md':
        // Convert HTML to basic markdown
        exportToMarkdown(title, text);
        toast.success('Scene exported as Markdown');
        break;
      case 'txt':
        exportToText(title, text);
        toast.success('Scene exported as plain text');
        break;
      case 'html':
        exportToHTML(title, html);
        toast.success('Scene exported as HTML');
        break;
    }

    setShowExportMenu(false);
  };

  // Toolbar button component
  const ToolbarButton = ({ onClick, active, disabled, title, icon: Icon, children }) => (
    <button
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={`p-2 rounded transition-colors ${
        active
          ? 'bg-blue-600 text-white'
          : 'hover:bg-gray-700 text-gray-300'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {Icon ? <Icon size={18} /> : children}
    </button>
  );

  if (!sceneId) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        Select a scene to edit
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        Loading scene...
      </div>
    );
  }

  if (!editor) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        Initializing editor...
      </div>
    );
  }

  return (
    <div className={isFullscreen ? 'fixed inset-0 z-50 bg-gray-900 flex flex-col' : 'h-full flex flex-col bg-gray-900'}>
      {/* Editor Header */}
      <div className="h-10 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
        <div className="text-sm font-medium">{scene?.title}</div>
        <div className="text-xs text-gray-500">
          {saveMutation.isPending ? 'Saving...' : lastSaved ? `Saved ${lastSaved.toLocaleTimeString()}` : ''}
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex items-center gap-1 px-4 py-2 bg-gray-800 border-b border-gray-700 flex-wrap">
        {/* Text Formatting */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-2 mr-2">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBold().run()}
            active={editor.isActive('bold')}
            title="Bold (Cmd+B)"
            icon={Bold}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleItalic().run()}
            active={editor.isActive('italic')}
            title="Italic (Cmd+I)"
            icon={Italic}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleStrike().run()}
            active={editor.isActive('strike')}
            title="Strikethrough"
            icon={Strikethrough}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleCode().run()}
            active={editor.isActive('code')}
            title="Inline Code"
            icon={Code}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHighlight().run()}
            active={editor.isActive('highlight')}
            title="Highlight"
            icon={Highlighter}
          />
        </div>

        {/* Headings */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-2 mr-2">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
            active={editor.isActive('heading', { level: 1 })}
            title="Heading 1"
            icon={Heading1}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
            active={editor.isActive('heading', { level: 2 })}
            title="Heading 2"
            icon={Heading2}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()}
            active={editor.isActive('heading', { level: 3 })}
            title="Heading 3"
            icon={Heading3}
          />
        </div>

        {/* Lists */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-2 mr-2">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBulletList().run()}
            active={editor.isActive('bulletList')}
            title="Bullet List"
            icon={List}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleOrderedList().run()}
            active={editor.isActive('orderedList')}
            title="Numbered List"
            icon={ListOrdered}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleTaskList().run()}
            active={editor.isActive('taskList')}
            title="Task List"
            icon={CheckSquare}
          />
        </div>

        {/* Block Elements */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-2 mr-2">
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleBlockquote().run()}
            active={editor.isActive('blockquote')}
            title="Blockquote"
            icon={Quote}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().setHorizontalRule().run()}
            title="Horizontal Rule"
            icon={Minus}
          />
          <ToolbarButton
            onClick={() => editor.chain().focus().toggleCodeBlock().run()}
            active={editor.isActive('codeBlock')}
            title="Code Block"
            icon={Code2}
          />
        </div>

        {/* Export Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowExportMenu(!showExportMenu)}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm flex items-center gap-2 transition-colors"
          >
            📥 Export
          </button>

          {showExportMenu && (
            <div className="absolute top-full left-0 mt-1 bg-gray-700 border border-gray-600 rounded shadow-lg z-10 min-w-[200px]">
              <button
                onClick={() => handleExport('md')}
                className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm transition-colors"
              >
                Export as Markdown (.md)
              </button>
              <button
                onClick={() => handleExport('txt')}
                className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm transition-colors"
              >
                Export as Text (.txt)
              </button>
              <button
                onClick={() => handleExport('html')}
                className="block w-full text-left px-4 py-2 hover:bg-gray-600 text-sm transition-colors"
              >
                Export as HTML (.html)
              </button>
            </div>
          )}
        </div>

        {/* Fullscreen Toggle */}
        <button
          onClick={toggleFullscreen}
          className="ml-2 px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm flex items-center gap-2 transition-colors"
          title="Distraction-free mode (F11)"
        >
          {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
        </button>

        <div className="ml-auto text-sm">
          <span className="text-green-400 font-medium">{stats.words.toLocaleString()} words</span>
        </div>
      </div>

      {/* Editor Content */}
      <div className="flex-1 overflow-y-auto bg-gray-900">
        <EditorContent editor={editor} />
      </div>

      {/* Stats Panel */}
      {!isFullscreen && (
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
      )}

      {/* Minimal stats in fullscreen mode */}
      {isFullscreen && (
        <div className="px-4 py-2 bg-gray-900 border-t border-gray-800 flex items-center justify-center text-sm text-gray-500">
          <span className="font-semibold text-green-400">{stats.words.toLocaleString()}</span>
          <span className="mx-1">words</span>
          <span className="mx-2">•</span>
          <span>Press Esc to exit fullscreen</span>
        </div>
      )}
    </div>
  );
}
