import { X, Check } from 'lucide-react';

const TEMPLATES = [
  {
    id: 'heros-journey',
    name: "Hero's Journey",
    icon: '⚔️',
    genre: 'Fantasy / Adventure',
    description: 'The classic monomyth structure used in Star Wars, Lord of the Rings, and The Matrix.',
    structure: '12 Stages',
    stages: [
      'Ordinary World',
      'Call to Adventure',
      'Refusal of the Call',
      'Meeting the Mentor',
      'Crossing the Threshold',
      'Tests, Allies, Enemies',
      'Approach to the Inmost Cave',
      'Ordeal',
      'Reward',
      'The Road Back',
      'Resurrection',
      'Return with the Elixir',
    ],
    bestFor: 'Epic quests, character transformation, adventure stories',
  },
  {
    id: 'mystery',
    name: 'Mystery Structure',
    icon: '🔍',
    genre: 'Mystery / Thriller',
    description: 'Classic detective story structure with clues, red herrings, and revelations.',
    structure: '8 Key Beats',
    stages: [
      'The Crime',
      'Initial Investigation',
      'First Clues',
      'Red Herrings',
      'Breakthrough Discovery',
      'Confrontation',
      'Revelation',
      'Resolution',
    ],
    bestFor: 'Detective stories, whodunits, crime thrillers',
  },
  {
    id: 'romance',
    name: 'Romance Arc',
    icon: '💕',
    genre: 'Romance',
    description: 'Emotional journey from meeting to happily ever after (or not).',
    structure: '7 Phases',
    stages: [
      'The Meet-Cute',
      'Building Attraction',
      'The First Kiss',
      'Deepening Connection',
      'The Black Moment',
      'Grand Gesture',
      'Happy Ending / Resolution',
    ],
    bestFor: 'Love stories, romantic subplots, relationship-driven narratives',
  },
  {
    id: 'sci-fi',
    name: 'Sci-Fi Exploration',
    icon: '🚀',
    genre: 'Science Fiction',
    description: 'World-building focused structure for exploring new realities and ideas.',
    structure: '6 Movements',
    stages: [
      'The Status Quo',
      'Discovery / Inciting Incident',
      'Exploration & Learning',
      'Consequences Emerge',
      'Crisis Point',
      'New Equilibrium',
    ],
    bestFor: 'Hard sci-fi, space opera, speculative fiction',
  },
];

export function TemplateLibrary({ onSelect, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-gray-800 rounded-xl max-w-6xl w-full max-h-[90vh] overflow-hidden shadow-2xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-6 border-b border-gray-700 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Story Template Library</h2>
            <p className="text-gray-400">Choose a proven structure to kickstart your story</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Templates Grid */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {TEMPLATES.map((template) => (
              <TemplateCard
                key={template.id}
                template={template}
                onSelect={() => onSelect(template)}
              />
            ))}
          </div>

          {/* Info Section */}
          <div className="mt-8 p-5 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <h3 className="text-lg font-semibold mb-2">💡 How Templates Work</h3>
            <p className="text-sm text-gray-300 mb-3">
              Templates provide a proven structure for your story. When you select one, the
              Creation Wizard will pre-fill suggestions based on the template's beats and stages.
            </p>
            <p className="text-sm text-gray-400">
              Remember: templates are starting points, not rigid rules. Adapt them to fit your
              unique vision!
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function TemplateCard({ template, onSelect }) {
  return (
    <div className="bg-gray-700 rounded-lg p-6 border border-gray-600 hover:border-blue-500 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-4xl">{template.icon}</span>
          <div>
            <h3 className="text-xl font-semibold">{template.name}</h3>
            <p className="text-sm text-gray-400">{template.genre}</p>
          </div>
        </div>
        <div className="px-3 py-1 bg-blue-600/20 text-blue-300 rounded-full text-xs font-medium">
          {template.structure}
        </div>
      </div>

      <p className="text-gray-300 mb-4 leading-relaxed">
        {template.description}
      </p>

      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-400 mb-2">Key Stages:</h4>
        <div className="grid grid-cols-2 gap-2">
          {template.stages.slice(0, 6).map((stage, idx) => (
            <div key={idx} className="text-xs text-gray-400 flex items-start gap-1">
              <Check size={12} className="text-green-400 mt-0.5 flex-shrink-0" />
              <span>{stage}</span>
            </div>
          ))}
        </div>
        {template.stages.length > 6 && (
          <p className="text-xs text-gray-500 mt-2">
            + {template.stages.length - 6} more stages...
          </p>
        )}
      </div>

      <div className="mb-4 p-3 bg-gray-800 rounded border border-gray-600">
        <p className="text-xs text-gray-400">
          <span className="font-semibold text-gray-300">Best for:</span> {template.bestFor}
        </p>
      </div>

      <button
        onClick={onSelect}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-medium"
      >
        Use This Template
      </button>
    </div>
  );
}
