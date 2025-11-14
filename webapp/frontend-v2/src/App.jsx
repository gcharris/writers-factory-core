import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { useState, useEffect } from 'react';
import { FileTree } from './features/explorer/FileTree';
import { SceneEditor } from './features/editor/SceneEditor';
import { AIToolsPanel } from './features/tools/AIToolsPanel';
import { KnowledgePanel } from './features/tools/KnowledgePanel';
import { TournamentPanel } from './features/tools/TournamentPanel';
import { SetupWizard } from './features/setup/SetupWizard';

const queryClient = new QueryClient();

function App() {
  const [showSetup, setShowSetup] = useState(false);
  const [selectedScene, setSelectedScene] = useState(null);
  const [rightPanel, setRightPanel] = useState('tools'); // 'tools' | 'knowledge' | 'tournament'
  const [models, setModels] = useState([]);

  useEffect(() => {
    // Check if setup needed
    const hasKeys = localStorage.getItem('api_keys');
    if (!hasKeys) {
      setShowSetup(true);
    }

    // Load models
    fetch('http://localhost:8000/api/models/available')
      .then(res => res.json())
      .then(data => setModels(data.models || []))
      .catch(err => console.error('Failed to load models:', err));
  }, []);

  if (showSetup) {
    return (
      <QueryClientProvider client={queryClient}>
        <SetupWizard onComplete={() => setShowSetup(false)} />
        <Toaster position="top-right" theme="dark" />
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="h-screen flex flex-col bg-gray-900 text-gray-100">
        {/* Top Bar */}
        <div className="h-12 border-b border-gray-700 flex items-center justify-between px-4 bg-gray-800">
          <div className="flex items-center gap-4">
            <h1 className="font-bold">Writers Factory</h1>
            <select className="px-3 py-1 bg-gray-700 rounded text-sm focus:outline-none">
              <option>Explants V1</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setRightPanel('tools')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'tools' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Tools
            </button>
            <button
              onClick={() => setRightPanel('knowledge')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'knowledge' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Knowledge
            </button>
            <button
              onClick={() => setRightPanel('tournament')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'tournament' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Tournament
            </button>
          </div>
        </div>

        {/* Main Layout */}
        <div className="flex-1 overflow-hidden">
          <PanelGroup direction="horizontal">
            {/* Left: File Tree */}
            <Panel defaultSize={20} minSize={15} className="border-r border-gray-700 bg-gray-800">
              <FileTree onSceneSelect={setSelectedScene} />
            </Panel>

            <PanelResizeHandle className="w-1 hover:bg-blue-500 transition-colors" />

            {/* Center: Editor */}
            <Panel defaultSize={50} minSize={30}>
              <SceneEditor sceneId={selectedScene?.id} />
            </Panel>

            <PanelResizeHandle className="w-1 hover:bg-blue-500 transition-colors" />

            {/* Right: Tools Panel */}
            <Panel defaultSize={30} minSize={20} className="border-l border-gray-700 bg-gray-800">
              {rightPanel === 'tools' && <AIToolsPanel currentScene={selectedScene} models={models} />}
              {rightPanel === 'knowledge' && <KnowledgePanel />}
              {rightPanel === 'tournament' && <TournamentPanel currentScene={selectedScene} models={models} />}
            </Panel>
          </PanelGroup>
        </div>
      </div>
      <Toaster position="top-right" theme="dark" />
    </QueryClientProvider>
  );
}

export default App;
