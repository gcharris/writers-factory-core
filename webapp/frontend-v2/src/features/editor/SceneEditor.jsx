import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Editor } from '@toast-ui/react-editor';
import '@toast-ui/editor/dist/toastui-editor.css';
import { useEffect, useState, useRef } from 'react';
import { toast } from 'sonner';
import { useDebounce } from '../../hooks/useDebounce';
import { exportToMarkdown, exportToText, exportToHTML } from '../../utils/exporters';
import { showFriendlyError } from '../../utils/errorHandler';

export function SceneEditor({ sceneId }) {
  const [content, setContent] = useState('');
  const [lastSaved, setLastSaved] = useState(null);
  const [editMode, setEditMode] = useState('wysiwyg'); // 'wysiwyg' or 'markdown'
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [stats, setStats] = useState({
    words: 0,
    characters: 0,
    charactersNoSpaces: 0,
    paragraphs: 0,
    readingTime: 0
  });
  const debouncedContent = useDebounce(content, 2000); // 2s autosave delay
  const queryClient = useQueryClient();
  const editorRef = useRef(null);

  // Calculate writing stats from markdown content
  const updateStats = (markdown) => {
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

  // Update content when scene loads
  useEffect(() => {
    if (scene?.content) {
      setContent(scene.content);

      // Update editor content when scene changes
      if (editorRef.current) {
        const editorInstance = editorRef.current.getInstance();
        editorInstance.setMarkdown(scene.content);
      }

      // Update stats
      updateStats(scene.content);
    }
  }, [scene?.id]); // Only run when scene ID changes

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
      queryClient.invalidateQueries(['manuscript-tree']); // Update word counts
    },
    onError: (error) => {
      showFriendlyError(error, toast, { type: 'scene' });
    }
  });

  // Autosave when content changes
  useEffect(() => {
    if (debouncedContent && debouncedContent !== scene?.content) {
      saveMutation.mutate(debouncedContent);
    }
  }, [debouncedContent]);

  // Manual save on Cmd+S
  useEffect(() => {
    const handleSave = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        if (editorRef.current) {
          const editorInstance = editorRef.current.getInstance();
          const markdown = editorInstance.getMarkdown();
          saveMutation.mutate(markdown);
          toast.success('Saved');
        }
      }
    };
    window.addEventListener('keydown', handleSave);
    return () => window.removeEventListener('keydown', handleSave);
  }, [sceneId]);

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

  const handleEditorChange = () => {
    if (editorRef.current) {
      const editorInstance = editorRef.current.getInstance();
      const markdown = editorInstance.getMarkdown();
      setContent(markdown);
      updateStats(markdown);
    }
  };

  const toggleEditMode = () => {
    if (editorRef.current) {
      const editor = editorRef.current.getInstance();
      const newMode = editMode === 'wysiwyg' ? 'markdown' : 'wysiwyg';
      editor.changeMode(newMode);
      setEditMode(newMode);
    }
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);

    // Optional: Use browser fullscreen API
    if (!isFullscreen) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  };

  const handleExport = (format) => {
    if (editorRef.current) {
      const editor = editorRef.current.getInstance();
      const markdown = editor.getMarkdown();
      const title = scene?.title || 'Untitled Scene';

      switch (format) {
        case 'md':
          exportToMarkdown(title, markdown);
          toast.success('Scene exported as Markdown');
          break;
        case 'txt':
          exportToText(title, markdown);
          toast.success('Scene exported as plain text');
          break;
        case 'html':
          exportToHTML(title, markdown);
          toast.success('Scene exported as HTML');
          break;
      }

      setShowExportMenu(false);
    }
  };

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

  return (
    <div className={isFullscreen ? 'fixed inset-0 z-50 bg-gray-900 flex flex-col' : 'h-full flex flex-col bg-gray-900'}>
      {/* Editor Header */}
      <div className="h-10 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
        <div className="text-sm font-medium">{scene?.title}</div>
        <div className="text-xs text-gray-500">
          {saveMutation.isPending ? 'Saving...' : lastSaved ? `Saved ${lastSaved.toLocaleTimeString()}` : ''}
        </div>
      </div>

      {/* Mode Toggle Bar */}
      <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 border-b border-gray-700">
        <button
          onClick={toggleEditMode}
          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors"
        >
          {editMode === 'wysiwyg' ? 'Switch to Markdown' : 'Switch to WYSIWYG'}
        </button>

        <span className="text-gray-400 text-sm">
          {editMode === 'wysiwyg' ? 'Visual Editor' : 'Markdown Editor'}
        </span>

        {/* Export Dropdown */}
        <div className="relative ml-4">
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
          className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm flex items-center gap-2 transition-colors"
          title="Distraction-free mode (F11)"
        >
          {isFullscreen ? '🗗 Exit Fullscreen' : '🗖 Fullscreen'}
        </button>

        <div className="ml-auto text-sm">
          <span id="word-count-display" className="text-green-400 font-medium">0 words</span>
        </div>
      </div>

      {/* Toast UI Editor */}
      <div className="flex-1 overflow-hidden">
        <Editor
          ref={editorRef}
          initialValue={content || "Start writing your scene..."}
          previewStyle="vertical"
          height={isFullscreen ? 'calc(100vh - 120px)' : '100%'}
          initialEditType="wysiwyg"
          useCommandShortcut={true}
          usageStatistics={false}
          onChange={handleEditorChange}
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
            ['code', 'codeblock']
          ]}
        />
      </div>

      {/* Stats Panel - Always show in fullscreen with minimal styling */}
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
