import { Sparkles, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export function ChatMessage({ sender, content, type, options, onOptionSelect }) {
  const isAI = sender === 'ai';

  if (type === 'options' && options) {
    return (
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <div className="flex-1">
          <div className="bg-gray-800 rounded-lg p-4 mb-3">
            <ReactMarkdown className="prose prose-invert prose-sm max-w-none">
              {content}
            </ReactMarkdown>
          </div>
          <div className="space-y-2">
            {options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => onOptionSelect && onOptionSelect(option.value || option)}
                className="w-full text-left p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors border border-gray-600 hover:border-blue-500"
              >
                {option.label || option}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (isAI) {
    return (
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <div className="flex-1 bg-gray-800 rounded-lg p-4">
          <ReactMarkdown className="prose prose-invert prose-sm max-w-none">
            {content}
          </ReactMarkdown>
        </div>
      </div>
    );
  }

  // User message
  return (
    <div className="flex items-start gap-3 justify-end">
      <div className="flex-1 bg-blue-600 rounded-lg p-4 max-w-2xl">
        <p className="text-white">{content}</p>
      </div>
      <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
        <User className="w-4 h-4 text-white" />
      </div>
    </div>
  );
}
