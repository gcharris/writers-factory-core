import { useState } from 'react';
import { Search, Book, X, ChevronRight } from 'lucide-react';
import { helpTopics, quickTips } from './helpContent';

export function HelpPanel({ onClose }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTopic, setSelectedTopic] = useState(null);

  // Filter topics based on search
  const filteredTopics = searchQuery
    ? Object.entries(helpTopics).filter(([key, topic]) =>
        topic.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        topic.sections.some(s =>
          s.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
          s.answer.toLowerCase().includes(searchQuery.toLowerCase())
        )
      )
    : Object.entries(helpTopics);

  // Random quick tip
  const randomTip = quickTips[Math.floor(Math.random() * quickTips.length)];

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-4xl w-full max-h-[90vh] flex flex-col border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Book size={28} className="text-blue-400" />
            <h2 className="text-2xl font-bold">Help & Documentation</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-200 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Search */}
        <div className="p-6 border-b border-gray-700">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search help topics..."
              className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Quick Tip */}
          <div className="mt-4 p-3 bg-blue-900/20 border border-blue-700/50 rounded-lg text-sm text-blue-300">
            {randomTip}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {!selectedTopic ? (
            // Topic List
            <div className="grid grid-cols-2 gap-4">
              {filteredTopics.map(([key, topic]) => (
                <button
                  key={key}
                  onClick={() => setSelectedTopic(key)}
                  className="p-6 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 hover:border-blue-500 rounded-lg text-left transition-all group"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">{topic.icon}</span>
                    <ChevronRight size={20} className="text-gray-400 group-hover:text-blue-400 transition-colors" />
                  </div>
                  <h3 className="font-semibold text-lg">{topic.title}</h3>
                  <p className="text-sm text-gray-400 mt-1">
                    {topic.sections.length} topics
                  </p>
                </button>
              ))}
            </div>
          ) : (
            // Topic Detail
            <div>
              <button
                onClick={() => setSelectedTopic(null)}
                className="mb-6 text-blue-400 hover:text-blue-300 flex items-center gap-2"
              >
                ← Back to all topics
              </button>

              <div className="flex items-center gap-3 mb-6">
                <span className="text-4xl">{helpTopics[selectedTopic].icon}</span>
                <h3 className="text-2xl font-bold">{helpTopics[selectedTopic].title}</h3>
              </div>

              <div className="space-y-6">
                {helpTopics[selectedTopic].sections.map((section, idx) => (
                  <div key={idx} className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                    <h4 className="font-semibold text-lg mb-2">{section.question}</h4>
                    <p className="text-gray-300 leading-relaxed">{section.answer}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-700 text-center text-sm text-gray-400">
          Need more help? Visit{' '}
          <a href="https://github.com/anthropics/claude-code" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
            GitHub
          </a>
          {' '}for documentation
        </div>
      </div>
    </div>
  );
}
