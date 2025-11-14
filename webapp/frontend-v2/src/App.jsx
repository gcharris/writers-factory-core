import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster, toast } from 'sonner';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { useState, useEffect } from 'react';
import { FileTree } from './features/explorer/FileTree';
import { SceneEditor } from './features/editor/SceneEditor';
import { AIToolsPanel } from './features/tools/AIToolsPanel';
import { KnowledgePanel } from './features/tools/KnowledgePanel';
import { TournamentPanel } from './features/tools/TournamentPanel';
import { SetupWizard } from './features/setup/SetupWizard';
import { OllamaStatus } from './features/ollama/OllamaStatus';
import { CostDashboard } from './features/cost/CostDashboard';
import { AgentProfiles } from './features/profiles/AgentProfiles';
import { BrainstormPage } from './features/brainstorm/BrainstormPage';
import { CharacterPanel } from './features/character/CharacterPanel';
import { ResearchPanel } from './features/research/ResearchPanel';
import { CraftPanel } from './features/craft/CraftPanel';
import { WelcomeModal } from './features/onboarding/WelcomeModal';
import { QuickStartBanner } from './features/onboarding/QuickStartBanner';
import { HelpPanel } from './features/help/HelpPanel';
import { Book } from 'lucide-react';
import { showFriendlyError } from './utils/errorHandler';

const queryClient = new QueryClient();

function App() {
  const [showSetup, setShowSetup] = useState(false);
  const [hasManuscript, setHasManuscript] = useState(null); // null = loading, true/false = determined
  const [selectedScene, setSelectedScene] = useState(null);
  const [rightPanel, setRightPanel] = useState('tools'); // 'tools' | 'knowledge' | 'tournament' | 'character' | 'research' | 'craft'
  const [models, setModels] = useState([]);
  const [economyMode, setEconomyMode] = useState(() => {
    const saved = localStorage.getItem('economy_mode');
    return saved === 'true';
  });
  const [showCostDashboard, setShowCostDashboard] = useState(false);
  const [showAgentProfiles, setShowAgentProfiles] = useState(false);
  const [showWelcome, setShowWelcome] = useState(() => {
    // Check if user has seen welcome (localStorage)
    return !localStorage.getItem('writers-factory-onboarded');
  });
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    // Check if setup needed
    const hasKeys = localStorage.getItem('api_keys');
    if (!hasKeys) {
      setShowSetup(true);
    }

    // Check if manuscript exists
    fetch('http://localhost:8000/api/manuscript/tree')
      .then(res => res.json())
      .then(data => {
        // If we have acts/chapters/scenes, we have a manuscript
        setHasManuscript(data.acts && data.acts.length > 0);
      })
      .catch(err => {
        console.error('Failed to check manuscript:', err);
        setHasManuscript(false); // Default to no manuscript on error
      });

    // Load models
    fetch('http://localhost:8000/api/models/available')
      .then(res => res.json())
      .then(data => setModels(data.models || []))
      .catch(err => console.error('Failed to load models:', err));
  }, []);

  const toggleEconomyMode = () => {
    const newMode = !economyMode;
    setEconomyMode(newMode);
    localStorage.setItem('economy_mode', newMode.toString());
  };

  const handleProjectCreated = (projectData) => {
    // Project created successfully, show the editor
    setHasManuscript(true);
    // Optionally reload manuscript tree
    queryClient.invalidateQueries(['manuscript-tree']);
  };

  const loadExampleProject = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/example/load', {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        toast.success('Example project loaded! Opening editor...');
        setHasManuscript(true);
        setShowWelcome(false);
        // Refresh manuscript tree
        queryClient.invalidateQueries(['manuscript-tree']);
      } else {
        throw new Error(data.error || 'Failed to load example project');
      }
    } catch (error) {
      console.error('Failed to load example project:', error);
      showFriendlyError(error, toast, { type: 'generation' });
    }
  };

  const handleWelcomeComplete = (choice) => {
    localStorage.setItem('writers-factory-onboarded', 'true');

    // Handle user choice
    switch (choice) {
      case 'wizard':
        // Navigate to brainstorm page (creation wizard)
        toast.success('Opening Creation Wizard...');
        setHasManuscript(false);
        break;
      case 'import':
        // Trigger import flow
        toast.info('Import feature coming soon!');
        break;
      case 'example':
        // Load example project
        loadExampleProject();
        break;
      case 'skip':
        // Do nothing, let user explore
        toast.info('Welcome! Feel free to explore.');
        break;
    }
  };

  if (showSetup) {
    return (
      <QueryClientProvider client={queryClient}>
        <SetupWizard onComplete={() => setShowSetup(false)} />
        <Toaster position="top-right" theme="dark" />
      </QueryClientProvider>
    );
  }

  // Show loading state while checking for manuscript
  if (hasManuscript === null) {
    return (
      <QueryClientProvider client={queryClient}>
        <div className="h-screen flex items-center justify-center bg-gray-900 text-gray-100">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading Writers Factory...</p>
          </div>
        </div>
        <Toaster position="top-right" theme="dark" />
      </QueryClientProvider>
    );
  }

  // Show Brainstorm page if no manuscript
  if (!hasManuscript) {
    return (
      <QueryClientProvider client={queryClient}>
        <BrainstormPage onProjectCreated={handleProjectCreated} />
        <Toaster position="top-right" theme="dark" />
      </QueryClientProvider>
    );
  }

  // Show main editor if manuscript exists
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
            <button
              onClick={() => setRightPanel('character')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'character' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Character
            </button>
            <button
              onClick={() => setRightPanel('research')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'research' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Research
            </button>
            <button
              onClick={() => setRightPanel('craft')}
              className={`px-3 py-1 rounded text-sm ${rightPanel === 'craft' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
            >
              Craft
            </button>

            {/* Separator */}
            <div className="h-6 w-px bg-gray-600" />

            {/* Economy Mode Toggle */}
            <button
              onClick={toggleEconomyMode}
              className={`px-3 py-1 rounded text-sm flex items-center gap-2 ${
                economyMode
                  ? 'bg-green-600 hover:bg-green-700'
                  : 'bg-gray-700 hover:bg-gray-600'
              }`}
              title={economyMode ? 'Economy mode ON - prefer local models' : 'Economy mode OFF'}
            >
              <span>{economyMode ? '💰' : '💸'}</span>
              <span>Economy</span>
            </button>

            {/* Cost Dashboard Button */}
            <button
              onClick={() => setShowCostDashboard(true)}
              className="px-3 py-1 rounded text-sm bg-gray-700 hover:bg-gray-600"
              title="View cost breakdown"
            >
              💵 Cost
            </button>

            {/* Agent Profiles Button */}
            <button
              onClick={() => setShowAgentProfiles(true)}
              className="px-3 py-1 rounded text-sm bg-gray-700 hover:bg-gray-600"
              title="Configure agent preferences"
            >
              ⚙️ Profiles
            </button>

            {/* Help Button */}
            <button
              onClick={() => setShowHelp(true)}
              className="px-3 py-1 rounded text-sm bg-gray-700 hover:bg-gray-600 flex items-center gap-2"
              title="Help & Documentation"
            >
              <Book size={16} />
              Help
            </button>
          </div>
        </div>

        {/* Ollama Status Banner */}
        <OllamaStatus />

        {/* Quick Start Banner */}
        <QuickStartBanner />

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
              {rightPanel === 'character' && <CharacterPanel />}
              {rightPanel === 'research' && <ResearchPanel projectId="explants-v1" />}
              {rightPanel === 'craft' && <CraftPanel projectId="explants-v1" />}
            </Panel>
          </PanelGroup>
        </div>
      </div>

      {/* Cost Dashboard Modal */}
      {showCostDashboard && <CostDashboard onClose={() => setShowCostDashboard(false)} />}

      {/* Agent Profiles Modal */}
      {showAgentProfiles && <AgentProfiles models={models} onClose={() => setShowAgentProfiles(false)} />}

      {/* Welcome Modal */}
      {showWelcome && (
        <WelcomeModal
          onClose={() => setShowWelcome(false)}
          onComplete={handleWelcomeComplete}
        />
      )}

      {/* Help Panel */}
      {showHelp && <HelpPanel onClose={() => setShowHelp(false)} />}

      <Toaster position="top-right" theme="dark" />
    </QueryClientProvider>
  );
}

export default App;
