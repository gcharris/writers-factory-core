import { useState } from 'react';
import { X, ChevronLeft, ChevronRight, Check } from 'lucide-react';
import { toast } from 'sonner';
import { showFriendlyError } from '../../utils/errorHandler';

const PHASES = [
  { id: 'foundation', label: 'Foundation', icon: '📚' },
  { id: 'characters', label: 'Characters', icon: '👥' },
  { id: 'world', label: 'World', icon: '🌍' },
  { id: 'structure', label: 'Structure', icon: '📖' },
];

export function CreationWizard({ onComplete, onCancel }) {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [formData, setFormData] = useState({
    // Foundation
    title: '',
    genre: '',
    premise: '',
    themes: '',

    // Characters
    protagonist: '',
    antagonist: '',
    supportingCast: '',

    // World
    setting: '',
    worldRules: '',
    atmosphere: '',

    // Structure
    actStructure: '3-act',
    targetLength: 'novel',
    pacing: 'medium',
  });

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentPhase < PHASES.length - 1) {
      setCurrentPhase(currentPhase + 1);
    }
  };

  const handleBack = () => {
    if (currentPhase > 0) {
      setCurrentPhase(currentPhase - 1);
    }
  };

  const handleComplete = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/wizard/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Failed to create project');

      const data = await response.json();
      toast.success('Project created successfully!');
      onComplete(data);
    } catch (error) {
      showFriendlyError(error, toast, { type: 'generation' });
      console.error(error);
    }
  };

  const isPhaseComplete = (phaseIndex) => {
    switch (phaseIndex) {
      case 0: // Foundation
        return formData.title && formData.genre && formData.premise;
      case 1: // Characters
        return formData.protagonist;
      case 2: // World
        return formData.setting;
      case 3: // Structure
        return true; // Always complete (has defaults)
      default:
        return false;
    }
  };

  const canProceed = isPhaseComplete(currentPhase);

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={onCancel}>
      <div className="bg-gray-800 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden shadow-2xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Creation Wizard</h2>
            <button
              onClick={onCancel}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          {/* Progress Bar */}
          <div className="flex items-center gap-2">
            {PHASES.map((phase, index) => (
              <div key={phase.id} className="flex items-center flex-1">
                <div className="flex items-center gap-2 flex-1">
                  <div
                    className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold ${
                      index < currentPhase
                        ? 'bg-green-600 text-white'
                        : index === currentPhase
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-400'
                    }`}
                  >
                    {index < currentPhase ? <Check size={20} /> : <span>{phase.icon}</span>}
                  </div>
                  <div className={`text-sm ${index === currentPhase ? 'text-white font-semibold' : 'text-gray-400'}`}>
                    {phase.label}
                  </div>
                </div>
                {index < PHASES.length - 1 && (
                  <div
                    className={`h-1 w-8 mx-2 rounded ${
                      index < currentPhase ? 'bg-green-600' : 'bg-gray-700'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-200px)]">
          {currentPhase === 0 && <FoundationPhase formData={formData} updateField={updateField} />}
          {currentPhase === 1 && <CharactersPhase formData={formData} updateField={updateField} />}
          {currentPhase === 2 && <WorldPhase formData={formData} updateField={updateField} />}
          {currentPhase === 3 && <StructurePhase formData={formData} updateField={updateField} />}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex items-center justify-between">
          <button
            onClick={handleBack}
            disabled={currentPhase === 0}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed rounded-lg transition-colors flex items-center gap-2"
          >
            <ChevronLeft size={20} />
            <span>Back</span>
          </button>

          <div className="text-sm text-gray-400">
            Step {currentPhase + 1} of {PHASES.length}
          </div>

          {currentPhase < PHASES.length - 1 ? (
            <button
              onClick={handleNext}
              disabled={!canProceed}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg transition-colors flex items-center gap-2 font-medium"
            >
              <span>Next</span>
              <ChevronRight size={20} />
            </button>
          ) : (
            <button
              onClick={handleComplete}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center gap-2 font-medium"
            >
              <Check size={20} />
              <span>Create Project</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function FoundationPhase({ formData, updateField }) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold mb-4">📚 Story Foundation</h3>
        <p className="text-gray-400 mb-6">
          Let's start with the basics. What's your story about?
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Story Title <span className="text-red-400">*</span>
        </label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => updateField('title', e.target.value)}
          placeholder="e.g., The Last Guardian"
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Genre <span className="text-red-400">*</span>
        </label>
        <select
          value={formData.genre}
          onChange={(e) => updateField('genre', e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        >
          <option value="">Select a genre...</option>
          <option value="fantasy">Fantasy</option>
          <option value="sci-fi">Science Fiction</option>
          <option value="mystery">Mystery/Thriller</option>
          <option value="romance">Romance</option>
          <option value="horror">Horror</option>
          <option value="literary">Literary Fiction</option>
          <option value="ya">Young Adult</option>
          <option value="historical">Historical Fiction</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Story Premise <span className="text-red-400">*</span>
        </label>
        <textarea
          value={formData.premise}
          onChange={(e) => updateField('premise', e.target.value)}
          placeholder="What's the core story? (2-3 sentences)"
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={4}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Themes (Optional)
        </label>
        <input
          type="text"
          value={formData.themes}
          onChange={(e) => updateField('themes', e.target.value)}
          placeholder="e.g., redemption, sacrifice, identity"
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        />
      </div>
    </div>
  );
}

function CharactersPhase({ formData, updateField }) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold mb-4">👥 Characters</h3>
        <p className="text-gray-400 mb-6">
          Who will drive your story forward?
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Protagonist <span className="text-red-400">*</span>
        </label>
        <textarea
          value={formData.protagonist}
          onChange={(e) => updateField('protagonist', e.target.value)}
          placeholder="Describe your main character: name, age, background, goal, flaw..."
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={4}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Antagonist (Optional)
        </label>
        <textarea
          value={formData.antagonist}
          onChange={(e) => updateField('antagonist', e.target.value)}
          placeholder="Who or what opposes the protagonist?"
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={3}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Supporting Cast (Optional)
        </label>
        <textarea
          value={formData.supportingCast}
          onChange={(e) => updateField('supportingCast', e.target.value)}
          placeholder="Key supporting characters: allies, mentors, love interests..."
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={3}
        />
      </div>
    </div>
  );
}

function WorldPhase({ formData, updateField }) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold mb-4">🌍 World & Setting</h3>
        <p className="text-gray-400 mb-6">
          Where does your story take place?
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Setting <span className="text-red-400">*</span>
        </label>
        <textarea
          value={formData.setting}
          onChange={(e) => updateField('setting', e.target.value)}
          placeholder="Time period, location, physical environment..."
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={4}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          World Rules (Optional)
        </label>
        <textarea
          value={formData.worldRules}
          onChange={(e) => updateField('worldRules', e.target.value)}
          placeholder="Magic systems, technology level, societal norms, supernatural elements..."
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 resize-none"
          rows={3}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Atmosphere (Optional)
        </label>
        <input
          type="text"
          value={formData.atmosphere}
          onChange={(e) => updateField('atmosphere', e.target.value)}
          placeholder="e.g., dark and gritty, whimsical, hopeful"
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        />
      </div>
    </div>
  );
}

function StructurePhase({ formData, updateField }) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold mb-4">📖 Story Structure</h3>
        <p className="text-gray-400 mb-6">
          How will you organize your narrative?
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Act Structure
        </label>
        <select
          value={formData.actStructure}
          onChange={(e) => updateField('actStructure', e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        >
          <option value="3-act">Three Act (Setup, Confrontation, Resolution)</option>
          <option value="4-act">Four Act (includes additional Complication)</option>
          <option value="5-act">Five Act (Shakespearean)</option>
          <option value="heros-journey">Hero's Journey (12 stages)</option>
          <option value="save-the-cat">Save the Cat (15 beats)</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Target Length
        </label>
        <select
          value={formData.targetLength}
          onChange={(e) => updateField('targetLength', e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        >
          <option value="short-story">Short Story (5k-15k words)</option>
          <option value="novella">Novella (15k-40k words)</option>
          <option value="novel">Novel (60k-100k words)</option>
          <option value="epic">Epic Novel (100k+ words)</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Pacing
        </label>
        <select
          value={formData.pacing}
          onChange={(e) => updateField('pacing', e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
        >
          <option value="fast">Fast (action-driven, quick scenes)</option>
          <option value="medium">Medium (balanced)</option>
          <option value="slow">Slow (character-driven, descriptive)</option>
        </select>
      </div>

      <div className="mt-8 p-4 bg-blue-900/20 border border-blue-700/50 rounded-lg">
        <p className="text-sm text-blue-200">
          ✨ <strong>Almost there!</strong> Once you create your project, we'll generate an initial
          manuscript structure based on your inputs. You can then start writing with AI assistance.
        </p>
      </div>
    </div>
  );
}
