import { useState } from 'react';
import { X, Zap, Users, Globe, Lightbulb, Sparkles } from 'lucide-react';
import { PathSelectionStep } from './PathSelectionStep';

export function WelcomeModal({ onClose, onComplete }) {
  const [step, setStep] = useState(0);

  const steps = [
    {
      title: "Welcome to Writers Factory! 📚",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300 text-lg leading-relaxed">
            Write, draft, and revise your novel in just one week using advanced AI-powered tools.
          </p>

          <div className="grid grid-cols-2 gap-4 mt-6">
            <FeatureCard
              icon={<Zap size={24} className="text-yellow-400" />}
              title="23 AI Models"
              description="Compare outputs from Claude, GPT, Gemini, and more"
            />
            <FeatureCard
              icon={<Users size={24} className="text-blue-400" />}
              title="Character Analysis"
              description="Detect contradictions and dimensional depth"
            />
            <FeatureCard
              icon={<Globe size={24} className="text-green-400" />}
              title="Free Local Models"
              description="Use Ollama for unlimited free generation"
            />
            <FeatureCard
              icon={<Lightbulb size={24} className="text-purple-400" />}
              title="Knowledge Base"
              description="Query NotebookLM for craft advice"
            />
          </div>
        </div>
      )
    },
    {
      title: "How Writers Factory Works",
      content: (
        <div className="space-y-6">
          <Step
            number="1"
            title="Brainstorm Your Story"
            description="Use the Creation Wizard to define your story foundation, characters, world, and structure."
            icon="✨"
          />
          <Step
            number="2"
            title="Generate Scenes"
            description="Use AI models to generate scene drafts. Compare outputs side-by-side to find the best version."
            icon="🎬"
          />
          <Step
            number="3"
            title="Edit & Refine"
            description="Edit scenes in the professional markdown editor. Use AI to enhance, rewrite, or polish your work."
            icon="✍️"
          />
          <Step
            number="4"
            title="Analyze & Improve"
            description="Check character depth, analyze pacing, and ensure consistency across your manuscript."
            icon="📊"
          />
          <Step
            number="5"
            title="Export Your Novel"
            description="Export your finished manuscript to Markdown, HTML, or plain text."
            icon="📥"
          />
        </div>
      )
    },
    {
      title: "Choose Your Path",
      content: (
        <PathSelectionStep
          onComplete={(path) => {
            onComplete(path);
            onClose();
          }}
        />
      )
    }
  ];

  const currentStep = steps[step];

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-gray-800 border-b border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles size={28} className="text-blue-400" />
            <h2 className="text-2xl font-bold">{currentStep.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-200 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-8">
          {currentStep.content}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-800 border-t border-gray-700 p-6 flex items-center justify-between">
          <div className="flex gap-2">
            {steps.map((_, idx) => (
              <div
                key={idx}
                className={`h-2 w-12 rounded-full transition-colors ${
                  idx === step ? 'bg-blue-500' : 'bg-gray-600'
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            {step > 0 && (
              <button
                onClick={() => setStep(step - 1)}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Back
              </button>
            )}

            {step < steps.length - 1 ? (
              <button
                onClick={() => setStep(step + 1)}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
              >
                Next
              </button>
            ) : (
              <button
                onClick={() => {
                  onComplete('skip');
                  onClose();
                }}
                className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Skip for Now
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
      <div className="mb-2">{icon}</div>
      <h4 className="font-semibold mb-1">{title}</h4>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  );
}

function Step({ number, title, description, icon }) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center font-bold text-xl">
        {icon}
      </div>
      <div>
        <h4 className="font-semibold text-lg mb-1">{title}</h4>
        <p className="text-gray-400">{description}</p>
      </div>
    </div>
  );
}

function StartOption({ title, description, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full p-6 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 hover:border-blue-500 rounded-lg text-left transition-all transform hover:scale-[1.02]"
    >
      <h4 className="font-semibold text-lg mb-2">{title}</h4>
      <p className="text-gray-400 text-sm">{description}</p>
    </button>
  );
}
