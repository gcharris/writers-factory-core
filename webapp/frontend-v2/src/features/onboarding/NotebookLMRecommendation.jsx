import { Lightbulb, BookOpen, MessageSquare, X } from 'lucide-react';

export function NotebookLMRecommendation({ onChoice, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-2xl w-full border border-blue-500/50 shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 border-b border-blue-500/50 p-6">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center">
                <Lightbulb className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">Recommendation</h3>
                <p className="text-blue-300 text-sm">Build a NotebookLM notebook first</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-200 transition-colors"
            >
              <X size={24} />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          <div>
            <h4 className="text-lg font-semibold text-white mb-3">
              Why use NotebookLM first?
            </h4>
            <p className="text-gray-300 mb-4">
              NotebookLM is a free tool from Google that helps you organize your thoughts
              before you start writing. It makes the AI wizard much more effective!
            </p>

            <ul className="space-y-2">
              <li className="flex items-start gap-3 text-gray-300">
                <span className="text-blue-400 mt-1">✓</span>
                <span>Collect ideas freely (no structure required)</span>
              </li>
              <li className="flex items-start gap-3 text-gray-300">
                <span className="text-blue-400 mt-1">✓</span>
                <span>Upload research, inspirations, and examples</span>
              </li>
              <li className="flex items-start gap-3 text-gray-300">
                <span className="text-blue-400 mt-1">✓</span>
                <span>Save random thoughts, character notes, and plot ideas</span>
              </li>
              <li className="flex items-start gap-3 text-gray-300">
                <span className="text-blue-400 mt-1">✓</span>
                <span>Let AI help you explore and organize your ideas</span>
              </li>
              <li className="flex items-start gap-3 text-gray-300">
                <span className="text-blue-400 mt-1">✓</span>
                <span>Then bring it all into Writers Factory when ready</span>
              </li>
            </ul>
          </div>

          <div className="border-t border-gray-700 pt-6">
            <h4 className="text-lg font-semibold text-white mb-4">
              Choose your next step:
            </h4>

            <div className="space-y-3">
              {/* Option 1: Show Guide (Recommended) */}
              <button
                onClick={() => onChoice('guide')}
                className="w-full p-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg text-left transition-all transform hover:scale-[1.02] border-2 border-blue-500"
              >
                <div className="flex items-start gap-3">
                  <BookOpen className="w-6 h-6 text-white flex-shrink-0 mt-1" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h5 className="font-semibold text-white">Show me how to set up NotebookLM</h5>
                      <span className="px-2 py-0.5 text-xs font-semibold bg-yellow-500 text-black rounded">
                        RECOMMENDED
                      </span>
                    </div>
                    <p className="text-sm text-blue-100">
                      I'll open the setup guide. You can bookmark it and return when ready.
                    </p>
                  </div>
                </div>
              </button>

              {/* Option 2: Continue Anyway */}
              <button
                onClick={() => onChoice('continue')}
                className="w-full p-4 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 hover:border-gray-500 rounded-lg text-left transition-all"
              >
                <div className="flex items-start gap-3">
                  <MessageSquare className="w-6 h-6 text-gray-400 flex-shrink-0 mt-1" />
                  <div className="flex-1">
                    <h5 className="font-semibold text-white mb-1">Continue with interactive questions</h5>
                    <p className="text-sm text-gray-400">
                      Skip NotebookLM and answer questions manually (less rich but workable)
                    </p>
                  </div>
                </div>
              </button>
            </div>
          </div>

          <div className="bg-gray-700/30 rounded-lg p-4 border border-gray-600">
            <p className="text-sm text-gray-400">
              <strong className="text-gray-300">Tip:</strong> Most successful writers spend 2-7 days
              collecting ideas in NotebookLM before starting. The AI wizard will extract and organize
              everything automatically, saving you hours of manual work.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
