import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { toast } from 'sonner';

const TASK_TYPES = [
  { id: 'draft', label: 'Draft', description: 'Initial scene drafts and rough text', icon: '📝' },
  { id: 'polish', label: 'Polish', description: 'Final polish and refinement', icon: '✨' },
  { id: 'dialogue', label: 'Dialogue', description: 'Character conversations', icon: '💬' },
  { id: 'action', label: 'Action', description: 'Action sequences and movement', icon: '⚡' },
  { id: 'description', label: 'Description', description: 'Setting and sensory details', icon: '🎨' },
  { id: 'brainstorm', label: 'Brainstorm', description: 'Ideas and variations', icon: '💡' },
];

export function AgentProfiles({ models, onClose }) {
  const [profiles, setProfiles] = useState(() => {
    const saved = localStorage.getItem('agent_profiles');
    if (saved) {
      return JSON.parse(saved);
    }
    // Default profiles
    return {
      draft: '',
      polish: '',
      dialogue: '',
      action: '',
      description: '',
      brainstorm: '',
    };
  });

  const handleProfileChange = (taskType, modelId) => {
    setProfiles(prev => ({
      ...prev,
      [taskType]: modelId
    }));
  };

  const handleSave = () => {
    localStorage.setItem('agent_profiles', JSON.stringify(profiles));
    toast.success('Agent profiles saved');
    onClose();
  };

  const handleReset = () => {
    const emptyProfiles = {
      draft: '',
      polish: '',
      dialogue: '',
      action: '',
      description: '',
      brainstorm: '',
    };
    setProfiles(emptyProfiles);
    localStorage.setItem('agent_profiles', JSON.stringify(emptyProfiles));
    toast.success('Profiles reset to defaults');
  };

  // Group models by local/cloud
  const localModels = models.filter(m => m.is_local);
  const cloudModels = models.filter(m => !m.is_local);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-800 rounded-lg p-6 max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold">Agent Profiles</h2>
            <p className="text-sm text-gray-400 mt-1">
              Set preferred models for different task types
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-700 rounded"
          >
            <X size={20} />
          </button>
        </div>

        {/* Task Type Settings */}
        <div className="space-y-4 mb-6">
          {TASK_TYPES.map(taskType => (
            <div key={taskType.id} className="bg-gray-700 rounded p-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span>{taskType.icon}</span>
                    <span className="font-semibold">{taskType.label}</span>
                  </div>
                  <p className="text-sm text-gray-400">{taskType.description}</p>
                </div>
              </div>

              <select
                value={profiles[taskType.id] || ''}
                onChange={(e) => handleProfileChange(taskType.id, e.target.value)}
                className="w-full px-3 py-2 bg-gray-600 border border-gray-500 rounded text-sm focus:outline-none focus:border-blue-500"
              >
                <option value="">Auto (use default)</option>

                {/* Local Models */}
                {localModels.length > 0 && (
                  <optgroup label="🦙 Local Models (FREE)">
                    {localModels.map(model => (
                      <option key={model.id} value={model.id}>
                        {model.id} - FREE
                      </option>
                    ))}
                  </optgroup>
                )}

                {/* Cloud Models */}
                {cloudModels.length > 0 && (
                  <optgroup label="☁️ Cloud Models">
                    {cloudModels.map(model => (
                      <option key={model.id} value={model.id}>
                        {model.id} - ${((model.cost_input || 0) + (model.cost_output || 0)).toFixed(4)}/1k
                      </option>
                    ))}
                  </optgroup>
                )}
              </select>
            </div>
          ))}
        </div>

        {/* Tips */}
        <div className="mb-6 p-4 bg-blue-900/20 border border-blue-700/50 rounded">
          <div className="text-sm text-blue-200">
            💡 <strong>Tips:</strong>
            <ul className="mt-2 ml-4 space-y-1 list-disc">
              <li>Use local models for drafts to save money</li>
              <li>Use premium cloud models for final polish</li>
              <li>Leave as "Auto" to respect Economy Mode settings</li>
            </ul>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <button
            onClick={handleReset}
            className="px-4 py-2 text-gray-400 hover:text-white"
          >
            Reset to Defaults
          </button>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium"
            >
              Save Profiles
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
