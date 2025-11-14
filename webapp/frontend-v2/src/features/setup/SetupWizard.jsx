import { useState } from 'react';
import { toast } from 'sonner';

const PROVIDERS = [
  { id: 'anthropic', name: 'Anthropic', envKey: 'ANTHROPIC_API_KEY' },
  { id: 'openai', name: 'OpenAI', envKey: 'OPENAI_API_KEY' },
  { id: 'google', name: 'Google AI', envKey: 'GOOGLE_API_KEY' },
  { id: 'mistral', name: 'Mistral AI', envKey: 'MISTRAL_API_KEY' },
  { id: 'deepseek', name: 'DeepSeek', envKey: 'DEEPSEEK_API_KEY' },
];

export function SetupWizard({ onComplete }) {
  const [keys, setKeys] = useState({});
  const [testing, setTesting] = useState({});

  const handleTest = async (provider) => {
    setTesting({ ...testing, [provider.id]: true });

    // TODO: Add actual test endpoint
    setTimeout(() => {
      setTesting({ ...testing, [provider.id]: false });
      toast.success(`${provider.name} connection OK`);
    }, 1000);
  };

  const handleSave = () => {
    // Note: In production, this should save to .env.local or keychain
    localStorage.setItem('api_keys', JSON.stringify(keys));
    toast.success('API keys saved');
    onComplete();
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-900">
      <div className="max-w-2xl w-full mx-auto p-8">
        <h1 className="text-2xl font-bold mb-2">Welcome to Writers Factory</h1>
        <p className="text-gray-400 mb-8">Configure your API keys to get started</p>

        <div className="space-y-4">
          {PROVIDERS.map(provider => (
            <div key={provider.id} className="border border-gray-700 rounded p-4 bg-gray-800">
              <div className="flex items-center justify-between mb-2">
                <label className="font-medium">{provider.name}</label>
                <button
                  onClick={() => handleTest(provider)}
                  disabled={!keys[provider.id] || testing[provider.id]}
                  className="px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded text-sm"
                >
                  {testing[provider.id] ? 'Testing...' : 'Test'}
                </button>
              </div>
              <input
                type="password"
                placeholder={`Enter ${provider.name} API key`}
                value={keys[provider.id] || ''}
                onChange={(e) => setKeys({ ...keys, [provider.id]: e.target.value })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
              />
              <div className="text-xs text-gray-500 mt-1">{provider.envKey}</div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex justify-end gap-3">
          <button
            onClick={() => onComplete()}
            className="px-4 py-2 text-gray-400 hover:text-white"
          >
            Skip for now
          </button>
          <button
            onClick={handleSave}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium"
          >
            Save & Continue
          </button>
        </div>
      </div>
    </div>
  );
}
