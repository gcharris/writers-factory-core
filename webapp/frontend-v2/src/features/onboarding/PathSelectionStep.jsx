import { useState } from 'react';
import { FileText, Notebook, HelpCircle } from 'lucide-react';
import { PathOption } from './PathOption';
import { NotebookLMRecommendation } from './NotebookLMRecommendation';

export function PathSelectionStep({ onComplete }) {
  const [selectedPath, setSelectedPath] = useState(null);
  const [showRecommendation, setShowRecommendation] = useState(false);

  const handlePathSelect = (path) => {
    setSelectedPath(path);
  };

  const handleContinue = () => {
    if (!selectedPath) return;

    if (selectedPath === 'new') {
      // Show recommendation modal for new writers
      setShowRecommendation(true);
    } else {
      // Proceed with selected path
      onComplete(selectedPath);
    }
  };

  const handleRecommendationChoice = (choice) => {
    setShowRecommendation(false);

    if (choice === 'guide') {
      // User chose to see NotebookLM guide
      onComplete('notebooklm-guide');
    } else if (choice === 'continue') {
      // User chose to continue with interactive Q&A
      onComplete('interactive-qa');
    }
  };

  return (
    <div className="space-y-6">
      <p className="text-gray-300 text-center mb-6">
        Choose the path that best matches your current situation:
      </p>

      <div className="space-y-4">
        {/* Path 1: Experienced Writer */}
        <PathOption
          icon={<FileText className="w-6 h-6" />}
          title="Experienced Writer"
          description="I have an existing manuscript to import"
          details={[
            "Import your work-in-progress or completed draft",
            "AI will analyze and extract knowledge automatically",
            "Continue writing with AI assistance"
          ]}
          selected={selectedPath === 'experienced'}
          onClick={() => handlePathSelect('experienced')}
        />

        {/* Path 2: Prepared Writer (RECOMMENDED) */}
        <PathOption
          icon={<Notebook className="w-6 h-6" />}
          title="Prepared Writer"
          description="I have a NotebookLM notebook ready"
          details={[
            "I've collected ideas, research, and notes in NotebookLM",
            "AI will extract and organize from my notebook",
            "RECOMMENDED for best results ⭐"
          ]}
          badge="Recommended"
          recommended={true}
          selected={selectedPath === 'prepared'}
          onClick={() => handlePathSelect('prepared')}
        />

        {/* Path 3: New Writer */}
        <PathOption
          icon={<HelpCircle className="w-6 h-6" />}
          title="New Writer"
          description="I don't have a notebook or manuscript yet"
          details={[
            "I'm starting from scratch with just an idea",
            "I'll need guidance on organizing my thoughts",
            "Show me how to get started"
          ]}
          selected={selectedPath === 'new'}
          onClick={() => handlePathSelect('new')}
        />
      </div>

      {/* Continue Button */}
      <div className="flex justify-end pt-4">
        <button
          onClick={handleContinue}
          disabled={!selectedPath}
          className={`px-6 py-3 rounded-lg font-semibold transition-all ${
            selectedPath
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-700 text-gray-500 cursor-not-allowed'
          }`}
        >
          Continue
        </button>
      </div>

      {/* NotebookLM Recommendation Modal */}
      {showRecommendation && (
        <NotebookLMRecommendation
          onChoice={handleRecommendationChoice}
          onClose={() => setShowRecommendation(false)}
        />
      )}
    </div>
  );
}
