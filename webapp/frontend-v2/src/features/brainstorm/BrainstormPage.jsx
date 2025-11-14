import { useState } from 'react';
import { Sparkles, FileUp, BookOpen, Lightbulb, Zap, Users, Globe, BookMarked } from 'lucide-react';
import { CreationWizard } from './CreationWizard';
import { NotebookLMGuide } from './NotebookLMGuide';
import { TemplateLibrary } from './TemplateLibrary';

export function BrainstormPage({ onProjectCreated }) {
  const [showWizard, setShowWizard] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);

  const handleWizardComplete = (projectData) => {
    setShowWizard(false);
    onProjectCreated(projectData);
  };

  const handleImport = () => {
    // Trigger file upload
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.md,.docx';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (file) {
        // TODO: Implement import logic
        console.log('Importing file:', file.name);
      }
    };
    input.click();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
      <div className="max-w-6xl mx-auto px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 mb-4 px-4 py-2 bg-blue-600/20 border border-blue-500/30 rounded-full">
            <Sparkles size={16} className="text-blue-400" />
            <span className="text-sm text-blue-300 font-medium">Writers Factory AI</span>
          </div>

          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Brainstorm Your Next Story
          </h1>

          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed">
            Harness the power of multiple AI models to craft compelling narratives.
            Start with a structured creation wizard or import your existing work.
          </p>

          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => setShowWizard(true)}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-semibold text-lg shadow-lg shadow-blue-500/25 transition-all transform hover:scale-105"
            >
              <div className="flex items-center gap-2">
                <Sparkles size={20} />
                <span>Start Creation Wizard</span>
              </div>
            </button>

            <button
              onClick={handleImport}
              className="px-8 py-4 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold text-lg transition-all"
            >
              <div className="flex items-center gap-2">
                <FileUp size={20} />
                <span>Import Manuscript</span>
              </div>
            </button>
          </div>
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          <ActionCard
            icon={<Sparkles size={32} className="text-purple-400" />}
            title="Creation Wizard"
            description="Guided 4-phase process to build your story foundation, characters, world, and structure."
            onClick={() => setShowWizard(true)}
            highlight
          />

          <ActionCard
            icon={<FileUp size={32} className="text-blue-400" />}
            title="Import Existing Work"
            description="Upload your manuscript and continue writing with AI assistance."
            onClick={handleImport}
          />

          <ActionCard
            icon={<BookOpen size={32} className="text-green-400" />}
            title="NotebookLM Setup"
            description="Learn how to set up your knowledge base for AI-powered research and ideation."
            onClick={() => setShowGuide(true)}
          />

          <ActionCard
            icon={<BookMarked size={32} className="text-pink-400" />}
            title="Template Library"
            description="Start with proven story structures: Hero's Journey, Mystery, Romance, Sci-Fi."
            onClick={() => setShowTemplates(true)}
          />
        </div>

        {/* Features Grid */}
        <div className="border-t border-gray-700 pt-16">
          <h2 className="text-3xl font-bold text-center mb-12">
            Why Writers Factory?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Zap size={28} className="text-yellow-400" />}
              title="Multi-Model Power"
              description="Compare outputs from Claude, GPT-4, Gemini, and local models side-by-side."
            />

            <FeatureCard
              icon={<Users size={28} className="text-blue-400" />}
              title="Character Consistency"
              description="AI remembers your characters' voices, traits, and development arcs."
            />

            <FeatureCard
              icon={<Globe size={28} className="text-green-400" />}
              title="World Building"
              description="Maintain rich, consistent settings across your entire manuscript."
            />

            <FeatureCard
              icon={<Lightbulb size={28} className="text-purple-400" />}
              title="Knowledge Base"
              description="Integrate NotebookLM for research-backed storytelling."
            />

            <FeatureCard
              icon={<BookOpen size={28} className="text-pink-400" />}
              title="Smart Autosave"
              description="Never lose your work with intelligent 2-second debounced saving."
            />

            <FeatureCard
              icon={<Sparkles size={28} className="text-cyan-400" />}
              title="Economy Mode"
              description="Use free local models for drafts, premium cloud models for polish."
            />
          </div>
        </div>

        {/* Footer CTA */}
        <div className="mt-16 text-center">
          <p className="text-gray-400 mb-4">
            Ready to write your masterpiece?
          </p>
          <button
            onClick={() => setShowWizard(true)}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all"
          >
            Get Started Now
          </button>
        </div>
      </div>

      {/* Modals */}
      {showWizard && (
        <CreationWizard
          onComplete={handleWizardComplete}
          onCancel={() => setShowWizard(false)}
        />
      )}

      {showGuide && (
        <NotebookLMGuide onClose={() => setShowGuide(false)} />
      )}

      {showTemplates && (
        <TemplateLibrary
          onSelect={(template) => {
            setShowTemplates(false);
            setShowWizard(true);
            // TODO: Pre-fill wizard with template data
          }}
          onClose={() => setShowTemplates(false)}
        />
      )}
    </div>
  );
}

function ActionCard({ icon, title, description, onClick, highlight }) {
  return (
    <button
      onClick={onClick}
      className={`p-6 rounded-xl text-left transition-all transform hover:scale-105 ${
        highlight
          ? 'bg-gradient-to-br from-purple-600/20 to-blue-600/20 border-2 border-purple-500/50 shadow-lg shadow-purple-500/25'
          : 'bg-gray-800 border border-gray-700 hover:border-gray-600'
      }`}
    >
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-400 leading-relaxed">{description}</p>
    </button>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="text-center">
      <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-gray-800 border border-gray-700 mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
    </div>
  );
}
