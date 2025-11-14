import { X, ExternalLink, CheckCircle } from 'lucide-react';

export function NotebookLMGuide({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-gray-800 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-hidden shadow-2xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-6 border-b border-gray-700 flex items-center justify-between">
          <h2 className="text-2xl font-bold">NotebookLM Setup Guide</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          <div className="mb-6">
            <p className="text-gray-300 leading-relaxed mb-4">
              NotebookLM is Google's AI-powered research assistant that helps you build
              a knowledge base for your story. Integrate it with Writers Factory for
              AI-assisted world building and research.
            </p>
          </div>

          {/* Step-by-step guide */}
          <div className="space-y-6">
            <SetupStep
              number={1}
              title="Create a NotebookLM Notebook"
              description="Go to NotebookLM and create a new notebook for your story project."
              link="https://notebooklm.google.com"
              linkText="Open NotebookLM"
            />

            <SetupStep
              number={2}
              title="Add Source Materials"
              description="Upload research documents, character notes, world-building files, or any reference materials relevant to your story."
              items={[
                'Character profiles and backstories',
                'World-building documents (maps, histories, cultures)',
                'Research articles and reference materials',
                'Plot outlines and story beats',
              ]}
            />

            <SetupStep
              number={3}
              title="Organize Your Knowledge"
              description="Use NotebookLM's AI to:"
              items={[
                'Generate summaries of your source materials',
                'Create study guides for your world',
                'Ask questions about your story universe',
                'Get AI-generated insights and connections',
              ]}
            />

            <SetupStep
              number={4}
              title="Integrate with Writers Factory"
              description="Use the Knowledge Panel in Writers Factory to query your NotebookLM knowledge base while writing."
              note="The Knowledge Panel will use NotebookLM's API to answer questions about your story world."
            />
          </div>

          {/* Tips Section */}
          <div className="mt-8 p-5 bg-purple-900/20 border border-purple-700/50 rounded-lg">
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <span>💡</span>
              <span>Pro Tips</span>
            </h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
                <span>Keep your source materials updated as your story evolves</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
                <span>Use descriptive filenames for easy reference</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
                <span>Regularly ask NotebookLM questions to test consistency</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
                <span>Export NotebookLM summaries to use as AI prompts</span>
              </li>
            </ul>
          </div>

          {/* Example Queries */}
          <div className="mt-6 p-5 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">Example Knowledge Queries</h3>
            <div className="space-y-2 text-sm">
              <QueryExample query="What are the social customs in the Capital city?" />
              <QueryExample query="How does the magic system work in my world?" />
              <QueryExample query="What are Sarah's key character traits and fears?" />
              <QueryExample query="What historical events led to the current conflict?" />
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex items-center justify-between">
          <a
            href="https://notebooklm.google.com"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors flex items-center gap-2 font-medium"
          >
            <ExternalLink size={16} />
            <span>Open NotebookLM</span>
          </a>

          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors font-medium"
          >
            Got It
          </button>
        </div>
      </div>
    </div>
  );
}

function SetupStep({ number, title, description, items, link, linkText, note }) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-bold">
        {number}
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <p className="text-gray-300 mb-3">{description}</p>

        {items && (
          <ul className="space-y-1 ml-4 mb-3">
            {items.map((item, idx) => (
              <li key={idx} className="text-sm text-gray-400 flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        )}

        {link && (
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 text-sm"
          >
            <ExternalLink size={14} />
            <span>{linkText}</span>
          </a>
        )}

        {note && (
          <p className="text-sm text-gray-500 italic mt-2">{note}</p>
        )}
      </div>
    </div>
  );
}

function QueryExample({ query }) {
  return (
    <div className="px-3 py-2 bg-gray-700/50 rounded border border-gray-600 text-gray-300">
      "{query}"
    </div>
  );
}
