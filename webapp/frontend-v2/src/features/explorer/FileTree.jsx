import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ChevronRight, ChevronDown, FileText, Plus, Edit2, Trash2, MoreVertical } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import { toast } from 'sonner';

export function FileTree({ onSceneSelect }) {
  const [expandedActs, setExpandedActs] = useState(new Set());
  const [expandedChapters, setExpandedChapters] = useState(new Set());
  const [contextMenu, setContextMenu] = useState(null);
  const [renameScene, setRenameScene] = useState(null);
  const [newTitle, setNewTitle] = useState('');
  const queryClient = useQueryClient();
  const contextMenuRef = useRef(null);

  const { data, isLoading } = useQuery({
    queryKey: ['manuscript-tree'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/manuscript/tree');
      return res.json();
    }
  });

  // Close context menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (contextMenuRef.current && !contextMenuRef.current.contains(event.target)) {
        setContextMenu(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Create scene mutation
  const createSceneMutation = useMutation({
    mutationFn: async ({ chapterId, title }) => {
      const res = await fetch('http://localhost:8000/api/scene/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chapter_id: chapterId,
          title: title || 'New Scene',
          content: ''
        })
      });
      if (!res.ok) throw new Error('Failed to create scene');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['manuscript-tree']);
      toast.success('Scene created successfully');
      setContextMenu(null);
    },
    onError: (error) => {
      toast.error(`Failed to create scene: ${error.message}`);
    }
  });

  // Rename scene mutation
  const renameSceneMutation = useMutation({
    mutationFn: async ({ sceneId, title }) => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}/rename`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      if (!res.ok) throw new Error('Failed to rename scene');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['manuscript-tree']);
      toast.success('Scene renamed successfully');
      setRenameScene(null);
      setNewTitle('');
    },
    onError: (error) => {
      toast.error(`Failed to rename scene: ${error.message}`);
    }
  });

  // Delete scene mutation
  const deleteSceneMutation = useMutation({
    mutationFn: async (sceneId) => {
      const res = await fetch(`http://localhost:8000/api/scene/${sceneId}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Failed to delete scene');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['manuscript-tree']);
      toast.success('Scene deleted successfully');
      setContextMenu(null);
    },
    onError: (error) => {
      toast.error(`Failed to delete scene: ${error.message}`);
    }
  });

  const toggleAct = (actId) => {
    const newSet = new Set(expandedActs);
    if (newSet.has(actId)) {
      newSet.delete(actId);
    } else {
      newSet.add(actId);
    }
    setExpandedActs(newSet);
  };

  const toggleChapter = (chapterId) => {
    const newSet = new Set(expandedChapters);
    if (newSet.has(chapterId)) {
      newSet.delete(chapterId);
    } else {
      newSet.add(chapterId);
    }
    setExpandedChapters(newSet);
  };

  const handleContextMenu = (e, item, type) => {
    e.preventDefault();
    e.stopPropagation();
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      item,
      type
    });
  };

  const handleNewScene = (chapterId) => {
    const title = prompt('Enter scene title:');
    if (title) {
      createSceneMutation.mutate({ chapterId, title });
    }
    setContextMenu(null);
  };

  const handleRename = (scene) => {
    setRenameScene(scene);
    setNewTitle(scene.title);
    setContextMenu(null);
  };

  const handleDelete = (sceneId) => {
    if (confirm('Are you sure you want to delete this scene? This cannot be undone.')) {
      deleteSceneMutation.mutate(sceneId);
    }
    setContextMenu(null);
  };

  const handleRenameSubmit = (e) => {
    e.preventDefault();
    if (newTitle.trim() && renameScene) {
      renameSceneMutation.mutate({ sceneId: renameScene.id, title: newTitle.trim() });
    }
  };

  if (isLoading) return <div className="p-4 text-gray-500">Loading...</div>;
  if (!data?.acts?.length) return <div className="p-4 text-gray-500">No manuscript loaded</div>;

  return (
    <div className="h-full overflow-y-auto text-sm relative">
      <div className="p-2 border-b border-gray-700 font-semibold text-gray-300">
        {data.title}
      </div>

      {data.acts.map(act => (
        <div key={act.id}>
          <div
            className="flex items-center gap-1 px-2 py-1 hover:bg-gray-700 cursor-pointer"
            onClick={() => toggleAct(act.id)}
          >
            {expandedActs.has(act.id) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            <span className="font-medium">{act.title}</span>
          </div>

          {expandedActs.has(act.id) && (
            <div className="ml-4">
              {act.chapters.map(chapter => (
                <div key={chapter.id}>
                  <div
                    className="flex items-center gap-1 px-2 py-1 hover:bg-gray-700 cursor-pointer group"
                    onClick={() => toggleChapter(chapter.id)}
                    onContextMenu={(e) => handleContextMenu(e, chapter, 'chapter')}
                  >
                    {expandedChapters.has(chapter.id) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    <span className="flex-1">{chapter.title}</span>
                    <button
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-600 rounded"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleNewScene(chapter.id);
                      }}
                      title="Add new scene"
                    >
                      <Plus size={12} />
                    </button>
                  </div>

                  {expandedChapters.has(chapter.id) && (
                    <div className="ml-4">
                      {chapter.scenes.map(scene => (
                        <div key={scene.id}>
                          {renameScene?.id === scene.id ? (
                            <form onSubmit={handleRenameSubmit} className="px-2 py-1">
                              <input
                                type="text"
                                value={newTitle}
                                onChange={(e) => setNewTitle(e.target.value)}
                                className="w-full px-2 py-1 bg-gray-700 text-gray-100 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
                                autoFocus
                                onBlur={handleRenameSubmit}
                              />
                            </form>
                          ) : (
                            <div
                              className="flex items-center gap-2 px-2 py-1 hover:bg-gray-700 cursor-pointer text-gray-300 group"
                              onClick={() => onSceneSelect(scene)}
                              onContextMenu={(e) => handleContextMenu(e, scene, 'scene')}
                            >
                              <FileText size={14} />
                              <span className="flex-1 truncate">{scene.title}</span>
                              <span className="text-xs text-gray-500">{scene.word_count}w</span>
                              <button
                                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-600 rounded"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleContextMenu(e, scene, 'scene');
                                }}
                              >
                                <MoreVertical size={12} />
                              </button>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

      {/* Context Menu */}
      {contextMenu && (
        <div
          ref={contextMenuRef}
          className="fixed bg-gray-800 border border-gray-700 rounded shadow-lg py-1 z-50 min-w-[160px]"
          style={{ left: contextMenu.x, top: contextMenu.y }}
        >
          {contextMenu.type === 'chapter' && (
            <button
              className="w-full px-3 py-2 text-left hover:bg-gray-700 flex items-center gap-2 text-sm"
              onClick={() => handleNewScene(contextMenu.item.id)}
            >
              <Plus size={14} />
              New Scene
            </button>
          )}
          {contextMenu.type === 'scene' && (
            <>
              <button
                className="w-full px-3 py-2 text-left hover:bg-gray-700 flex items-center gap-2 text-sm"
                onClick={() => handleRename(contextMenu.item)}
              >
                <Edit2 size={14} />
                Rename
              </button>
              <button
                className="w-full px-3 py-2 text-left hover:bg-gray-700 flex items-center gap-2 text-sm text-red-400"
                onClick={() => handleDelete(contextMenu.item.id)}
              >
                <Trash2 size={14} />
                Delete
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
