import { useQuery } from '@tanstack/react-query';
import { ChevronRight, ChevronDown, FileText } from 'lucide-react';
import { useState } from 'react';

export function FileTree({ onSceneSelect }) {
  const [expandedActs, setExpandedActs] = useState(new Set());
  const [expandedChapters, setExpandedChapters] = useState(new Set());

  const { data, isLoading } = useQuery({
    queryKey: ['manuscript-tree'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/manuscript/tree');
      return res.json();
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

  if (isLoading) return <div className="p-4 text-gray-500">Loading...</div>;
  if (!data?.acts?.length) return <div className="p-4 text-gray-500">No manuscript loaded</div>;

  return (
    <div className="h-full overflow-y-auto text-sm">
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
                    className="flex items-center gap-1 px-2 py-1 hover:bg-gray-700 cursor-pointer"
                    onClick={() => toggleChapter(chapter.id)}
                  >
                    {expandedChapters.has(chapter.id) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    <span>{chapter.title}</span>
                  </div>

                  {expandedChapters.has(chapter.id) && (
                    <div className="ml-4">
                      {chapter.scenes.map(scene => (
                        <div
                          key={scene.id}
                          className="flex items-center gap-2 px-2 py-1 hover:bg-gray-700 cursor-pointer text-gray-300"
                          onClick={() => onSceneSelect(scene)}
                        >
                          <FileText size={14} />
                          <span>{scene.title}</span>
                          <span className="ml-auto text-xs text-gray-500">{scene.word_count}w</span>
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
    </div>
  );
}
