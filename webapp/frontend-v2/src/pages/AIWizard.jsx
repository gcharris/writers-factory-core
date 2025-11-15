import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2 } from 'lucide-react';
import { ChatMessage } from '../features/wizard/ChatMessage';
import { ProgressSteps } from '../features/wizard/ProgressSteps';
import { toast } from 'sonner';

const CATEGORIES = [
  "Characters",
  "Story Structure",
  "World Building",
  "Themes & Philosophy",
  "Voice & Craft",
  "Antagonism & Conflict",
  "Key Beats & Pacing",
  "Research & Setting Specifics",
];

export function AIWizard({ projectId, notebookUrl, onComplete }) {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [steps, setSteps] = useState(
    CATEGORIES.map((name, idx) => ({
      name,
      status: idx === 0 ? 'in_progress' : 'pending'
    }))
  );
  const [userInput, setUserInput] = useState('');
  const [waitingForInput, setWaitingForInput] = useState(false);
  const [currentInputType, setCurrentInputType] = useState('text');
  const [currentOptions, setCurrentOptions] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initialize WebSocket connection
    const wsUrl = `ws://localhost:8000/ws/wizard/${projectId}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log('WebSocket connected');
      // Send initial configuration
      ws.current.send(JSON.stringify({
        type: 'init',
        notebook_url: notebookUrl
      }));
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      toast.error('Connection error. Please try again.');
    };

    ws.current.onclose = () => {
      console.log('WebSocket closed');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [projectId, notebookUrl]);

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'ai_message':
        // Add AI message to chat
        setMessages(prev => [...prev, {
          id: Date.now(),
          sender: 'ai',
          content: data.content,
          type: data.requires_input && data.options ? 'options' : 'text',
          options: data.options
        }]);

        // Check if waiting for input
        if (data.requires_input) {
          setWaitingForInput(true);
          setCurrentInputType(data.input_type || 'text');
          setCurrentOptions(data.options);
        } else {
          setWaitingForInput(false);
          setIsProcessing(true);
        }
        break;

      case 'progress':
        // Update progress steps
        if (data.category_index !== undefined) {
          setSteps(prev => prev.map((step, idx) => ({
            ...step,
            status: idx < data.category_index ? 'complete' :
                    idx === data.category_index ? 'in_progress' : 'pending'
          })));
        }
        break;

      case 'complete':
        // Wizard complete
        toast.success('Setup complete! Initializing your project...');
        setSteps(prev => prev.map(step => ({ ...step, status: 'complete' })));

        // Wait a moment then redirect or call onComplete
        setTimeout(() => {
          if (onComplete) {
            onComplete(data.results);
          } else {
            navigate('/editor');
          }
        }, 2000);
        break;

      case 'redirect':
        navigate(data.content);
        break;

      case 'error':
        toast.error(data.content);
        setWaitingForInput(false);
        setIsProcessing(false);
        break;

      default:
        console.log('Unknown message type:', data.type);
    }
  };

  const sendUserResponse = (response) => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      toast.error('Connection lost. Please refresh the page.');
      return;
    }

    // Add user message to chat
    setMessages(prev => [...prev, {
      id: Date.now(),
      sender: 'user',
      content: response
    }]);

    // Send response to backend
    ws.current.send(JSON.stringify({
      type: 'user_response',
      content: response
    }));

    // Reset input state
    setUserInput('');
    setWaitingForInput(false);
    setCurrentOptions(null);
    setIsProcessing(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;
    sendUserResponse(userInput);
  };

  const handleOptionSelect = (option) => {
    sendUserResponse(option);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex">
      {/* Left Sidebar: Progress */}
      <div className="w-72 bg-gray-800 border-r border-gray-700 p-6">
        <div className="mb-6">
          <h2 className="text-xl font-bold text-white mb-2">Project Setup</h2>
          <p className="text-sm text-gray-400">
            Organizing your story knowledge from NotebookLM
          </p>
        </div>

        <div className="mb-4">
          <h3 className="text-sm font-semibold text-gray-400 mb-3">Progress</h3>
          <ProgressSteps steps={steps} />
        </div>

        <div className="mt-6 p-4 bg-gray-700/50 rounded-lg border border-gray-600">
          <p className="text-xs text-gray-400">
            The AI wizard is extracting and organizing information from your NotebookLM.
            You'll be asked to validate findings and fill in any gaps.
          </p>
        </div>
      </div>

      {/* Right: Chat Interface */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="h-16 border-b border-gray-700 flex items-center px-6 bg-gray-800">
          <h1 className="text-lg font-semibold text-white">AI Setup Wizard</h1>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map(msg => (
            <ChatMessage
              key={msg.id}
              sender={msg.sender}
              content={msg.content}
              type={msg.type}
              options={msg.options}
              onOptionSelect={handleOptionSelect}
            />
          ))}

          {isProcessing && !waitingForInput && (
            <div className="flex items-center gap-3 text-gray-400">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>AI is analyzing your notebook...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-700 p-4 bg-gray-800">
          {waitingForInput && currentInputType === 'text' ? (
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Type your response..."
                className="flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                autoFocus
              />
              <button
                type="submit"
                disabled={!userInput.trim()}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-semibold transition-colors flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </form>
          ) : (
            <div className="text-center text-gray-500 py-2">
              {isProcessing ? 'Processing...' : 'Waiting for AI...'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
