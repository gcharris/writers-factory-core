import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

const TEMPLATES = [
  { id: 'generate', label: 'Generate New Scene', endpoint: '/api/scene/generate' },
  { id: 'enhance', label: 'Enhance Scene', endpoint: '/api/scene/enhance' },
  { id: 'continue', label: 'Continue Scene', endpoint: '/api/scene/generate' },
  { id: 'voice', label: 'Voice Test', endpoint: '/api/scene/enhance' },
];

export function AIToolsPanel({ currentScene, models }) {
  const [selectedTemplate, setSelectedTemplate] = useState('generate');
  const [selectedModel, setSelectedModel] = useState('claude-sonnet-4.5');
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);

  const generateMutation = useMutation({
    mutationFn: async () => {
      const template = TEMPLATES.find(t => t.id === selectedTemplate);
      const res = await fetch(`http://localhost:8000${template.endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          model: selectedModel,
          scene_text: currentScene?.content,
          context: currentScene?.notes
        })
      });
      if (!res.ok) throw new Error('Generation failed');
      return res.json();
    },
    onSuccess: (data) => {
      setResult(data);
      toast.success('Generated successfully');
    },
    onError: () => {
      toast.error('Generation failed');
    }
  });

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3">AI Tools</h3>

        {/* Template Selector */}
        <div className="space-y-2 mb-4">
          {TEMPLATES.map(template => (
            <button
              key={template.id}
              onClick={() => setSelectedTemplate(template.id)}
              className={`w-full text-left px-3 py-2 rounded text-sm ${
                selectedTemplate === template.id
                  ? 'bg-blue-600'
                  : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              {template.label}
            </button>
          ))}
        </div>

        {/* Model Selector */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-1 block">Model</label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500"
          >
            {/* Local Models */}
            {models.filter(m => m.is_local).length > 0 && (
              <optgroup label="🦙 Local Models (FREE)">
                {models.filter(m => m.is_local).map(model => (
                  <option key={model.id} value={model.id}>
                    {model.id} - FREE
                  </option>
                ))}
              </optgroup>
            )}

            {/* Cloud Models */}
            {models.filter(m => !m.is_local).length > 0 && (
              <optgroup label="☁️ Cloud Models">
                {models.filter(m => !m.is_local).map(model => (
                  <option key={model.id} value={model.id}>
                    {model.id} - ${((model.cost_input || 0) + (model.cost_output || 0)).toFixed(4)}/1k
                  </option>
                ))}
              </optgroup>
            )}
          </select>
        </div>

        {/* Prompt Input */}
        <div className="mb-4">
          <label className="text-sm text-gray-400 mb-1 block">Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe what you want..."
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500 resize-none"
            rows={4}
          />
        </div>

        {/* Generate Button */}
        <button
          onClick={() => generateMutation.mutate()}
          disabled={!prompt || generateMutation.isPending}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded font-medium"
        >
          {generateMutation.isPending ? 'Generating...' : 'Generate'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="flex-1 p-4 overflow-y-auto">
          <div className="text-sm text-gray-400 mb-2">Result:</div>
          <div className="bg-gray-700 p-3 rounded text-sm whitespace-pre-wrap">
            {result.scene || result.enhanced_scene || 'No output'}
          </div>
        </div>
      )}
    </div>
  );
}
