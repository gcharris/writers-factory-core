import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Book, Plus, Send, Loader2, ExternalLink } from 'lucide-react';
import { toast } from 'sonner';

export function ResearchPanel({ projectId = "explants-v1" }) {
  const [question, setQuestion] = useState('');
  const [selectedNotebook, setSelectedNotebook] = useState(null);
  const [showAddNotebook, setShowAddNotebook] = useState(false);
  const queryClient = useQueryClient();

  // Fetch notebooks
  const { data: notebooksData, isLoading: loadingNotebooks } = useQuery({
    queryKey: ['notebooks', projectId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/research/notebooks?project_id=${projectId}`);
      return res.json();
    }
  });

  // Query mutation
  const queryMutation = useMutation({
    mutationFn: async ({ question, notebookId }) => {
      const res = await fetch('http://localhost:8000/api/research/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          notebook_id: notebookId,
          project_id: projectId
        })
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail);
      }
      return res.json();
    },
    onSuccess: (data) => {
      toast.success('Answer received');
    },
    onError: (error) => {
      toast.error(`Query failed: ${error.message}`);
    }
  });

  const handleQuery = () => {
    if (!question.trim()) return;

    queryMutation.mutate({
      question: question.trim(),
      notebookId: selectedNotebook
    });
  };

  const notebooks = notebooksData?.notebooks || [];

  return (
    <div className="h-full flex flex-col bg-gray-900">
      {/* Header */}
      <div className="p-4 border-b border-gray-700 bg-gray-800">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold text-gray-100 flex items-center">
            <Book size={18} className="mr-2" />
            Research
          </h2>
          <button
            onClick={() => setShowAddNotebook(true)}
            className="text-sm px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-1"
          >
            <Plus size={14} />
            Add Notebook
          </button>
        </div>

        {/* Notebook selector */}
        {notebooks.length > 0 ? (
          <select
            value={selectedNotebook || ''}
            onChange={(e) => setSelectedNotebook(e.target.value || null)}
            className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Auto-select notebook</option>
            {notebooks.map(nb => (
              <option key={nb.id} value={nb.id}>
                {nb.name}
              </option>
            ))}
          </select>
        ) : (
          <div className="text-sm text-gray-400 text-center py-2">
            No notebooks yet. Add one to get started!
          </div>
        )}
      </div>

      {/* Query input */}
      <div className="p-4 border-b border-gray-700 bg-gray-800">
        <div className="flex gap-2">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your research..."
            className="flex-1 px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500"
            rows={3}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.metaKey) {
                handleQuery();
              }
            }}
            disabled={notebooks.length === 0}
          />
          <button
            onClick={handleQuery}
            disabled={queryMutation.isPending || !question.trim() || notebooks.length === 0}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center"
            title={notebooks.length === 0 ? "Add a notebook first" : "Send query (Cmd+Enter)"}
          >
            {queryMutation.isPending ? (
              <Loader2 size={18} className="animate-spin" />
            ) : (
              <Send size={18} />
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {notebooks.length > 0 ? "Cmd+Enter to send" : "Add a notebook to start asking questions"}
        </p>
      </div>

      {/* Answer display */}
      <div className="flex-1 overflow-y-auto p-4">
        {queryMutation.data && (
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-4 mb-4">
            <div className="text-sm text-gray-400 mb-2 flex items-center gap-2">
              <Book size={14} />
              From: <span className="font-medium text-gray-300">{queryMutation.data.notebook_name}</span>
            </div>

            <div className="prose prose-invert prose-sm max-w-none mb-4 text-gray-200">
              {queryMutation.data.answer}
            </div>

            {queryMutation.data.sources && queryMutation.data.sources.length > 0 && (
              <div className="border-t border-gray-700 pt-3">
                <div className="text-xs font-semibold text-gray-400 mb-2 flex items-center gap-1">
                  <ExternalLink size={12} />
                  Sources:
                </div>
                {queryMutation.data.sources.map((source, idx) => (
                  <div key={idx} className="text-xs text-gray-400 mb-1 pl-4">
                    {idx + 1}. {source.title} {source.page && `(p. ${source.page})`}
                    {source.excerpt && (
                      <div className="text-gray-500 italic ml-2 mt-1">
                        &quot;{source.excerpt.substring(0, 100)}...&quot;
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {queryMutation.isPending && (
          <div className="text-center text-gray-400 py-8">
            <Loader2 size={24} className="animate-spin mx-auto mb-2" />
            Querying NotebookLM...
            <div className="text-xs text-gray-500 mt-2">This may take 10-30 seconds</div>
          </div>
        )}

        {!queryMutation.data && !queryMutation.isPending && (
          <div className="text-center text-gray-500 py-8">
            <Book size={32} className="mx-auto mb-3 opacity-50" />
            {notebooks.length > 0 ? (
              <p>Ask a question about your research</p>
            ) : (
              <>
                <p className="mb-2">No notebooks connected yet</p>
                <button
                  onClick={() => setShowAddNotebook(true)}
                  className="text-sm px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Add Your First Notebook
                </button>
              </>
            )}
          </div>
        )}
      </div>

      {/* Add notebook modal */}
      {showAddNotebook && (
        <AddNotebookModal
          projectId={projectId}
          onClose={() => setShowAddNotebook(false)}
          onSuccess={() => {
            queryClient.invalidateQueries(['notebooks', projectId]);
            setShowAddNotebook(false);
          }}
        />
      )}
    </div>
  );
}

// Add Notebook Modal component
function AddNotebookModal({ projectId, onClose, onSuccess }) {
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState('');

  const addMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/research/notebooks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Failed to add notebook');
      }
      return res.json();
    },
    onSuccess: () => {
      toast.success('Notebook added successfully');
      onSuccess();
    },
    onError: (error) => {
      toast.error(`Failed to add notebook: ${error.message}`);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    addMutation.mutate({
      project_id: projectId,
      name,
      url,
      description,
      tags: tags.split(',').map(t => t.trim()).filter(Boolean)
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 text-gray-100 rounded-lg p-6 max-w-md w-full mx-4 border border-gray-700">
        <h3 className="text-lg font-semibold mb-4">Add NotebookLM Notebook</h3>

        <form onSubmit={handleSubmit}>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Character Profiles"
                className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">NotebookLM URL</label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://notebooklm.google.com/notebook/..."
                className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Open your notebook in NotebookLM and copy the URL
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">Description (optional)</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Contains character backstories, motivations, and relationships"
                className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={2}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-300">Tags (comma-separated)</label>
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="characters, worldbuilding, research"
                className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="flex gap-2 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-600 rounded hover:bg-gray-700 text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={addMutation.isPending}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-600"
            >
              {addMutation.isPending ? 'Adding...' : 'Add Notebook'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
