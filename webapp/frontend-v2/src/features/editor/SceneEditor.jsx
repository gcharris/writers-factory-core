import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Editor from '@monaco-editor/react';
import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { useDebounce } from '../../hooks/useDebounce';

export function SceneEditor({ sceneId }) {
  const [content, setContent] = useState('');
  const [lastSaved, setLastSaved] = useState(null);
  const debouncedContent = useDebounce(content, 2000); // 2s autosave delay
  const queryClient = useQueryClient();

  // Load scene
  const { data: scene, isLoading } = useQuery({
    queryKey: ['scene', sceneId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`);
      if (!res.ok) throw new Error('Failed to load scene');
      return res.json();
    },
    enabled: !!sceneId
  });

  // Update content when scene loads
  useEffect(() => {
    if (scene?.content) {
      setContent(scene.content);
    }
  }, [scene]);

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async (newContent) => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
      if (!res.ok) throw new Error('Save failed');
      return res.json();
    },
    onSuccess: () => {
      setLastSaved(new Date());
      queryClient.invalidateQueries(['manuscript-tree']); // Update word counts
    },
    onError: () => {
      toast.error('Failed to save');
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
        saveMutation.mutate(content);
        toast.success('Saved');
      }
    };
    window.addEventListener('keydown', handleSave);
    return () => window.removeEventListener('keydown', handleSave);
  }, [content]);

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
    <div className="h-full flex flex-col bg-gray-900">
      {/* Editor Header */}
      <div className="h-10 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
        <div className="text-sm font-medium">{scene?.title}</div>
        <div className="text-xs text-gray-500">
          {saveMutation.isPending ? 'Saving...' : lastSaved ? `Saved ${lastSaved.toLocaleTimeString()}` : ''}
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1">
        <Editor
          height="100%"
          defaultLanguage="markdown"
          theme="vs-dark"
          value={content}
          onChange={(value) => setContent(value || '')}
          options={{
            fontSize: 14,
            lineNumbers: 'on',
            wordWrap: 'on',
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            padding: { top: 16, bottom: 16 },
          }}
        />
      </div>
    </div>
  );
}
