import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

export function KnowledgePanel() {
  const [question, setQuestion] = useState('');
  const [source, setSource] = useState('cognee');
  const [result, setResult] = useState(null);

  const queryMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('http://localhost:8000/api/knowledge/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, source })
      });
      if (!res.ok) throw new Error('Query failed');
      return res.json();
    },
    onSuccess: (data) => {
      setResult(data);
      toast.success('Query completed');
    },
    onError: () => {
      toast.error('Query failed');
    }
  });

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3">Knowledge Base</h3>

        {/* Source Selector */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-1 block">Source</label>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500"
          >
            <option value="cognee">Cognee (Local)</option>
            <option value="notebooklm">NotebookLM</option>
          </select>
        </div>

        {/* Question Input */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-1 block">Question</label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about your story..."
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500 resize-none"
            rows={4}
          />
        </div>

        {/* Query Button */}
        <button
          onClick={() => queryMutation.mutate()}
          disabled={!question || queryMutation.isPending}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium"
        >
          {queryMutation.isPending ? 'Querying...' : 'Ask'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="flex-1 p-4 overflow-y-auto">
          <div className="text-sm text-gray-400 mb-2">Answer:</div>
          <div className="bg-gray-700 p-3 rounded text-sm whitespace-pre-wrap mb-4">
            {result.answer}
          </div>

          {result.references && result.references.length > 0 && (
            <>
              <div className="text-sm text-gray-400 mb-2">References:</div>
              <div className="space-y-2">
                {result.references.map((ref, idx) => (
                  <div key={idx} className="text-xs bg-gray-700 p-2 rounded">
                    {ref}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
