import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

export function TournamentPanel({ currentScene, models }) {
  const [selectedModels, setSelectedModels] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [results, setResults] = useState(null);

  const toggleModel = (modelId) => {
    if (selectedModels.includes(modelId)) {
      setSelectedModels(selectedModels.filter(id => id !== modelId));
    } else if (selectedModels.length < 4) {
      setSelectedModels([...selectedModels, modelId]);
    }
  };

  const compareMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('http://localhost:8000/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          models: selectedModels
        })
      });
      if (!res.ok) throw new Error('Comparison failed');
      return res.json();
    },
    onSuccess: (data) => {
      setResults(data);
      toast.success('Comparison complete');
    },
    onError: () => {
      toast.error('Comparison failed');
    }
  });

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3">Tournament Compare</h3>

        {/* Model Selection */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-2 block">
            Select 2-4 models ({selectedModels.length}/4)
          </label>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {models.slice(0, 10).map(model => (
              <button
                key={model.id}
                onClick={() => toggleModel(model.id)}
                className={`w-full text-left px-2 py-1 rounded text-xs ${
                  selectedModels.includes(model.id)
                    ? 'bg-blue-600'
                    : 'bg-gray-700 hover:bg-gray-600'
                }`}
              >
                {model.id}
              </button>
            ))}
          </div>
        </div>

        {/* Prompt Input */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-1 block">Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Write a prompt to compare..."
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500 resize-none"
            rows={3}
          />
        </div>

        {/* Compare Button */}
        <button
          onClick={() => compareMutation.mutate()}
          disabled={selectedModels.length < 2 || !prompt || compareMutation.isPending}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium"
        >
          {compareMutation.isPending ? 'Comparing...' : 'Compare Models'}
        </button>
      </div>

      {/* Results Grid */}
      {results?.results && (
        <div className="flex-1 p-4 overflow-y-auto">
          <div className="grid grid-cols-1 gap-4">
            {Object.entries(results.results).map(([model, output]) => (
              <div key={model} className="border border-gray-700 rounded">
                <div className="bg-gray-700 px-3 py-2 font-medium text-sm">
                  {model}
                </div>
                <div className="p-3 text-sm bg-gray-800 whitespace-pre-wrap">
                  {output}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
