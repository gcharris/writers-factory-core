import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import {
  ChevronLeft,
  ChevronRight,
  Check,
  Loader2,
  Upload,
  X,
  FileText,
  Sparkles,
  TestTube,
  CheckCircle2
} from 'lucide-react';
import { toast } from 'sonner';

const STEPS = [
  { id: 'details', label: 'Project Details', icon: FileText },
  { id: 'voice', label: 'Voice Input', icon: Sparkles },
  { id: 'materials', label: 'Reference Materials', icon: Upload },
  { id: 'analysis', label: 'AI Analysis', icon: Loader2 },
  { id: 'review', label: 'Review & Test', icon: TestTube },
  { id: 'finalize', label: 'Finalize', icon: CheckCircle2 }
];

const GENRES = [
  'literary',
  'thriller',
  'romance',
  'sci-fi',
  'fantasy',
  'mystery',
  'horror',
  'historical',
  'other'
];

export function ProjectSetupWizard({ onComplete }) {
  const [activeStep, setActiveStep] = useState(0);
  const [projectData, setProjectData] = useState({
    name: '',
    genre: 'literary',
    goals: '',
    examplePassages: [],
    uploadedDocs: [],
    notebooklmUrls: [],
    styleGuide: '',
    antiPatterns: [],
    voiceProfile: null,
    generatedSkills: null
  });

  // Wizard state
  const [currentPassage, setCurrentPassage] = useState('');
  const [currentNotebookLM, setCurrentNotebookLM] = useState('');
  const [testScene, setTestScene] = useState('');
  const [testResults, setTestResults] = useState(null);

  // Mutations
  const analyzeVoiceMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/setup/analyze-voice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Voice analysis failed');
      return res.json();
    },
    onSuccess: (data) => {
      setProjectData(prev => ({ ...prev, voiceProfile: data.voiceProfile }));
      toast.success('Voice profile extracted successfully!');
    },
    onError: (error) => {
      toast.error(`Analysis failed: ${error.message}`);
    }
  });

  const generateSkillsMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/setup/generate-skills', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Skill generation failed');
      return res.json();
    },
    onSuccess: (data) => {
      setProjectData(prev => ({ ...prev, generatedSkills: data.skills }));
      toast.success('6 custom skills generated!');
    },
    onError: (error) => {
      toast.error(`Skill generation failed: ${error.message}`);
    }
  });

  const testSkillMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/setup/test-skill', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Skill test failed');
      return res.json();
    },
    onSuccess: (data) => {
      setTestResults(data);
      toast.success('Scene analyzed successfully!');
    },
    onError: (error) => {
      toast.error(`Test failed: ${error.message}`);
    }
  });

  const createProjectMutation = useMutation({
    mutationFn: async (data) => {
      const res = await fetch('http://localhost:8000/api/setup/create-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Project creation failed');
      return res.json();
    },
    onSuccess: (data) => {
      toast.success(`Project "${data.projectId}" created successfully!`);
      setTimeout(() => onComplete(data), 2000);
    },
    onError: (error) => {
      toast.error(`Project creation failed: ${error.message}`);
    }
  });

  // Step handlers
  const handleNext = () => {
    // Validation
    if (activeStep === 0) {
      if (!projectData.name.trim()) {
        toast.error('Please enter a project name');
        return;
      }
    }

    if (activeStep === 1) {
      if (projectData.examplePassages.length < 3) {
        toast.error('Please add at least 3 example passages');
        return;
      }
    }

    // Auto-trigger AI analysis on step 3
    if (activeStep === 3) {
      analyzeVoiceMutation.mutate({
        examplePassages: projectData.examplePassages,
        uploadedDocs: projectData.uploadedDocs,
        notebooklmUrls: projectData.notebooklmUrls,
        styleGuide: projectData.styleGuide,
        genre: projectData.genre
      });
    }

    // Auto-generate skills on step 4
    if (activeStep === 4 && !projectData.generatedSkills) {
      generateSkillsMutation.mutate({
        name: projectData.name,
        genre: projectData.genre,
        examplePassages: projectData.examplePassages,
        uploadedDocs: projectData.uploadedDocs,
        notebooklmUrls: projectData.notebooklmUrls,
        voiceProfile: projectData.voiceProfile
      });
    }

    setActiveStep(prev => Math.min(prev + 1, STEPS.length - 1));
  };

  const handleBack = () => {
    setActiveStep(prev => Math.max(prev - 1, 0));
  };

  const addPassage = () => {
    if (!currentPassage.trim()) {
      toast.error('Please enter passage content');
      return;
    }
    if (currentPassage.trim().split(/\s+/).length < 100) {
      toast.error('Passages should be at least 100 words');
      return;
    }
    setProjectData(prev => ({
      ...prev,
      examplePassages: [...prev.examplePassages, currentPassage]
    }));
    setCurrentPassage('');
    toast.success(`Passage ${projectData.examplePassages.length + 1} added`);
  };

  const removePassage = (index) => {
    setProjectData(prev => ({
      ...prev,
      examplePassages: prev.examplePassages.filter((_, i) => i !== index)
    }));
  };

  const addNotebookLM = () => {
    if (!currentNotebookLM.trim()) {
      toast.error('Please enter a NotebookLM URL');
      return;
    }
    setProjectData(prev => ({
      ...prev,
      notebooklmUrls: [...prev.notebooklmUrls, currentNotebookLM]
    }));
    setCurrentNotebookLM('');
    toast.success('NotebookLM URL added');
  };

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    const uploadedDocs = await Promise.all(
      files.map(async (file) => ({
        filename: file.name,
        content: await file.text()
      }))
    );
    setProjectData(prev => ({
      ...prev,
      uploadedDocs: [...prev.uploadedDocs, ...uploadedDocs]
    }));
    toast.success(`${files.length} file(s) uploaded`);
  };

  const handleTestAnalyzer = () => {
    if (!testScene.trim()) {
      toast.error('Please enter a test scene');
      return;
    }
    testSkillMutation.mutate({
      projectId: projectData.name,
      skillType: 'scene-analyzer',
      testScene
    });
  };

  const handleCreateProject = () => {
    createProjectMutation.mutate(projectData);
  };

  // Render step content
  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return <ProjectDetailsStep projectData={projectData} setProjectData={setProjectData} />;
      case 1:
        return (
          <VoiceInputStep
            projectData={projectData}
            currentPassage={currentPassage}
            setCurrentPassage={setCurrentPassage}
            addPassage={addPassage}
            removePassage={removePassage}
            currentNotebookLM={currentNotebookLM}
            setCurrentNotebookLM={setCurrentNotebookLM}
            addNotebookLM={addNotebookLM}
          />
        );
      case 2:
        return (
          <ReferenceMaterialsStep
            projectData={projectData}
            setProjectData={setProjectData}
            handleFileUpload={handleFileUpload}
          />
        );
      case 3:
        return (
          <AIAnalysisStep
            isAnalyzing={analyzeVoiceMutation.isPending}
            voiceProfile={projectData.voiceProfile}
          />
        );
      case 4:
        return (
          <ReviewAndTestStep
            isGenerating={generateSkillsMutation.isPending}
            generatedSkills={projectData.generatedSkills}
            testScene={testScene}
            setTestScene={setTestScene}
            handleTestAnalyzer={handleTestAnalyzer}
            isTesting={testSkillMutation.isPending}
            testResults={testResults}
          />
        );
      case 5:
        return (
          <FinalizeStep
            projectData={projectData}
            handleCreateProject={handleCreateProject}
            isCreating={createProjectMutation.isPending}
          />
        );
      default:
        return null;
    }
  };

  const canProceed = () => {
    switch (activeStep) {
      case 0:
        return projectData.name.trim() && projectData.genre;
      case 1:
        return projectData.examplePassages.length >= 3;
      case 3:
        return projectData.voiceProfile !== null;
      case 4:
        return projectData.generatedSkills !== null;
      default:
        return true;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white py-8">
      <div className="max-w-5xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Create New Project</h1>
          <p className="text-gray-400">
            Set up a custom writing project with AI-powered skills tailored to your voice
          </p>
        </div>

        {/* Stepper */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {STEPS.map((step, index) => {
              const Icon = step.icon;
              const isActive = index === activeStep;
              const isComplete = index < activeStep;
              return (
                <div key={step.id} className="flex items-center flex-1">
                  <div className="flex flex-col items-center flex-1">
                    <div
                      className={`
                        w-12 h-12 rounded-full flex items-center justify-center border-2 mb-2
                        ${isComplete ? 'bg-green-600 border-green-600' :
                          isActive ? 'bg-blue-600 border-blue-600' :
                          'bg-gray-800 border-gray-700'}
                      `}
                    >
                      {isComplete ? (
                        <Check className="w-6 h-6" />
                      ) : (
                        <Icon className="w-6 h-6" />
                      )}
                    </div>
                    <div className={`text-sm font-medium ${isActive ? 'text-white' : 'text-gray-500'}`}>
                      {step.label}
                    </div>
                  </div>
                  {index < STEPS.length - 1 && (
                    <div
                      className={`h-0.5 flex-1 ${
                        isComplete ? 'bg-green-600' : 'bg-gray-700'
                      }`}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div className="bg-gray-800 rounded-lg p-8 min-h-[400px]">
          {renderStepContent()}
        </div>

        {/* Navigation */}
        <div className="mt-8 flex justify-between">
          <button
            onClick={handleBack}
            disabled={activeStep === 0}
            className="px-6 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-600 disabled:cursor-not-allowed rounded flex items-center gap-2"
          >
            <ChevronLeft className="w-5 h-5" />
            Back
          </button>
          <button
            onClick={handleNext}
            disabled={!canProceed() || activeStep === STEPS.length - 1}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-600 disabled:cursor-not-allowed rounded flex items-center gap-2"
          >
            Next
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}

// Step 1: Project Details
function ProjectDetailsStep({ projectData, setProjectData }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Project Details</h2>
        <p className="text-gray-400 mb-6">
          Tell us about your writing project
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Project Name</label>
        <input
          type="text"
          value={projectData.name}
          onChange={(e) => setProjectData(prev => ({ ...prev, name: e.target.value }))}
          placeholder="e.g., the-explants, my-romance-novel"
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
        />
        <p className="text-xs text-gray-500 mt-1">
          Use lowercase with dashes (e.g., my-novel-project)
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Genre</label>
        <select
          value={projectData.genre}
          onChange={(e) => setProjectData(prev => ({ ...prev, genre: e.target.value }))}
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
        >
          {GENRES.map(genre => (
            <option key={genre} value={genre}>
              {genre.charAt(0).toUpperCase() + genre.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Project Goals (Optional)</label>
        <textarea
          value={projectData.goals}
          onChange={(e) => setProjectData(prev => ({ ...prev, goals: e.target.value }))}
          placeholder="What are you hoping to achieve with this project?"
          rows={4}
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 resize-none"
        />
      </div>
    </div>
  );
}

// Step 2: Voice Input
function VoiceInputStep({
  projectData,
  currentPassage,
  setCurrentPassage,
  addPassage,
  removePassage,
  currentNotebookLM,
  setCurrentNotebookLM,
  addNotebookLM
}) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Voice Input</h2>
        <p className="text-gray-400 mb-6">
          Provide 3-5 example passages (500-1000 words each) that represent your writing voice
        </p>
      </div>

      {/* Added Passages */}
      {projectData.examplePassages.length > 0 && (
        <div className="space-y-2">
          <label className="block text-sm font-medium mb-2">
            Added Passages ({projectData.examplePassages.length}/5)
          </label>
          {projectData.examplePassages.map((passage, index) => (
            <div key={index} className="flex items-start gap-2 bg-gray-700 p-3 rounded">
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-300 mb-1">
                  Passage {index + 1} ({passage.split(/\s+/).length} words)
                </div>
                <div className="text-xs text-gray-500 line-clamp-2">
                  {passage.substring(0, 150)}...
                </div>
              </div>
              <button
                onClick={() => removePassage(index)}
                className="p-1 hover:bg-gray-600 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Add Passage */}
      {projectData.examplePassages.length < 5 && (
        <div>
          <label className="block text-sm font-medium mb-2">
            Add Passage {projectData.examplePassages.length + 1}
          </label>
          <textarea
            value={currentPassage}
            onChange={(e) => setCurrentPassage(e.target.value)}
            placeholder="Paste a 500-1000 word passage that represents your voice..."
            rows={8}
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 resize-none"
          />
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-gray-500">
              {currentPassage.split(/\s+/).filter(w => w).length} words
            </span>
            <button
              onClick={addPassage}
              disabled={projectData.examplePassages.length >= 5}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded text-sm"
            >
              Add Passage ({projectData.examplePassages.length}/5)
            </button>
          </div>
        </div>
      )}

      {/* NotebookLM URLs */}
      <div>
        <label className="block text-sm font-medium mb-2">NotebookLM URLs (Optional)</label>
        <div className="space-y-2">
          {projectData.notebooklmUrls.map((url, index) => (
            <div key={index} className="flex items-center gap-2 bg-gray-700 p-2 rounded text-sm">
              <span className="flex-1 truncate">{url}</span>
              <button
                onClick={() => {
                  setProjectData(prev => ({
                    ...prev,
                    notebooklmUrls: prev.notebooklmUrls.filter((_, i) => i !== index)
                  }));
                }}
                className="p-1 hover:bg-gray-600 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
          <div className="flex gap-2">
            <input
              type="url"
              value={currentNotebookLM}
              onChange={(e) => setCurrentNotebookLM(e.target.value)}
              placeholder="https://notebooklm.google.com/notebook/..."
              className="flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 text-sm"
            />
            <button
              onClick={addNotebookLM}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm"
            >
              Add
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Step 3: Reference Materials
function ReferenceMaterialsStep({ projectData, setProjectData, handleFileUpload }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Reference Materials</h2>
        <p className="text-gray-400 mb-6">
          Upload style guides, character sheets, or world bibles (optional)
        </p>
      </div>

      {/* File Upload */}
      <div>
        <label className="block text-sm font-medium mb-2">Upload Documents</label>
        <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center">
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-500" />
          <input
            type="file"
            multiple
            accept=".txt,.md,.pdf,.docx"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <span className="text-blue-500 hover:text-blue-400">Choose files</span>
            <span className="text-gray-500"> or drag and drop</span>
          </label>
          <p className="text-xs text-gray-500 mt-2">
            TXT, MD, PDF, DOCX up to 10MB each
          </p>
        </div>
      </div>

      {/* Uploaded Files */}
      {projectData.uploadedDocs.length > 0 && (
        <div>
          <label className="block text-sm font-medium mb-2">Uploaded Files</label>
          <div className="space-y-2">
            {projectData.uploadedDocs.map((doc, index) => (
              <div key={index} className="flex items-center gap-2 bg-gray-700 p-3 rounded">
                <FileText className="w-5 h-5 text-gray-400" />
                <span className="flex-1 text-sm">{doc.filename}</span>
                <button
                  onClick={() => {
                    setProjectData(prev => ({
                      ...prev,
                      uploadedDocs: prev.uploadedDocs.filter((_, i) => i !== index)
                    }));
                  }}
                  className="p-1 hover:bg-gray-600 rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Style Guide */}
      <div>
        <label className="block text-sm font-medium mb-2">Style Guide / Anti-Patterns (Optional)</label>
        <textarea
          value={projectData.styleGuide}
          onChange={(e) => setProjectData(prev => ({ ...prev, styleGuide: e.target.value }))}
          placeholder="List patterns to avoid, style preferences, or writing rules..."
          rows={6}
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 resize-none"
        />
        <p className="text-xs text-gray-500 mt-1">
          Example: "Avoid adverbs, use show-don't-tell, keep dialogue tight"
        </p>
      </div>
    </div>
  );
}

// Step 4: AI Analysis
function AIAnalysisStep({ isAnalyzing, voiceProfile }) {
  if (isAnalyzing || !voiceProfile) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-16 h-16 animate-spin text-blue-500 mb-4" />
        <h2 className="text-2xl font-bold mb-2">Analyzing Your Voice...</h2>
        <p className="text-gray-400">This will take 1-2 minutes</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Voice Profile Extracted</h2>
        <p className="text-gray-400 mb-6">
          Here's what we discovered about your writing voice
        </p>
      </div>

      {/* Voice Name */}
      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 p-6 rounded-lg border border-blue-700/50">
        <h3 className="text-xl font-bold mb-2">{voiceProfile.voiceName || 'Your Unique Voice'}</h3>
      </div>

      {/* Primary Characteristics */}
      <div>
        <h4 className="font-semibold mb-3">Primary Characteristics</h4>
        <div className="grid grid-cols-2 gap-3">
          {(voiceProfile.primaryCharacteristics || []).map((char, index) => (
            <div key={index} className="bg-gray-700 p-3 rounded text-sm">
              {char}
            </div>
          ))}
        </div>
      </div>

      {/* Sentence Structure */}
      {voiceProfile.sentenceStructure && (
        <div className="bg-gray-700 p-4 rounded">
          <h4 className="font-semibold mb-2">Sentence Structure</h4>
          <div className="text-sm text-gray-300 space-y-1">
            <div>Average Length: {voiceProfile.sentenceStructure.avgLength || 'N/A'} words</div>
            <div>Compression: {voiceProfile.sentenceStructure.compression || 'N/A'}</div>
            <div>Variety: {voiceProfile.sentenceStructure.variety || 'N/A'}</div>
          </div>
        </div>
      )}

      {/* POV Style */}
      {voiceProfile.povStyle && (
        <div className="bg-gray-700 p-4 rounded">
          <h4 className="font-semibold mb-2">POV Style</h4>
          <div className="text-sm text-gray-300 space-y-1">
            <div>Depth: {voiceProfile.povStyle.depth || 'N/A'}</div>
            <div>Consciousness Mode: {voiceProfile.povStyle.consciousnessMode || 'N/A'}%</div>
          </div>
        </div>
      )}

      {/* Metaphor Domains */}
      {voiceProfile.metaphorDomains && voiceProfile.metaphorDomains.length > 0 && (
        <div>
          <h4 className="font-semibold mb-3">Metaphor Domains</h4>
          <div className="grid grid-cols-2 gap-3">
            {voiceProfile.metaphorDomains.map((domain, index) => (
              <div key={index} className="bg-gray-700 p-3 rounded">
                <div className="font-medium text-sm">{domain.name}</div>
                <div className="text-xs text-gray-400 mt-1">{domain.percentage}% usage</div>
                <div className="text-xs text-gray-500 mt-1">{domain.keywords?.join(', ')}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Step 5: Review & Test
function ReviewAndTestStep({
  isGenerating,
  generatedSkills,
  testScene,
  setTestScene,
  handleTestAnalyzer,
  isTesting,
  testResults
}) {
  if (isGenerating || !generatedSkills) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-16 h-16 animate-spin text-blue-500 mb-4" />
        <h2 className="text-2xl font-bold mb-2">Generating Your 6 Custom Skills...</h2>
        <p className="text-gray-400">This will take 2-3 minutes</p>
      </div>
    );
  }

  const skillTypes = [
    'scene-analyzer',
    'scene-enhancer',
    'character-validator',
    'scene-writer',
    'scene-multiplier',
    'scaffold-generator'
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Review & Test Your Skills</h2>
        <p className="text-gray-400 mb-6">
          6 custom skills have been generated for your project
        </p>
      </div>

      {/* Generated Skills Checklist */}
      <div>
        <h4 className="font-semibold mb-3">Generated Skills</h4>
        <div className="space-y-2">
          {skillTypes.map(skillType => (
            <div key={skillType} className="flex items-center gap-3 bg-gray-700 p-3 rounded">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
              <span className="flex-1 font-medium">{skillType}</span>
              <span className="text-xs text-gray-400">Ready</span>
            </div>
          ))}
        </div>
      </div>

      {/* Test Analyzer */}
      <div className="border-t border-gray-700 pt-6">
        <h4 className="font-semibold mb-3">Test Your Analyzer</h4>
        <p className="text-sm text-gray-400 mb-4">
          Paste a scene to see how your custom analyzer scores it
        </p>
        <textarea
          value={testScene}
          onChange={(e) => setTestScene(e.target.value)}
          placeholder="Paste a scene from your manuscript..."
          rows={6}
          className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-500 resize-none mb-3"
        />
        <button
          onClick={handleTestAnalyzer}
          disabled={isTesting || !testScene.trim()}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded flex items-center gap-2"
        >
          {isTesting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <TestTube className="w-4 h-4" />
              Test Analyzer
            </>
          )}
        </button>
      </div>

      {/* Test Results */}
      {testResults && (
        <div className="bg-gray-700 p-4 rounded">
          <h4 className="font-semibold mb-3">Analysis Results</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Overall Score:</span>
              <span className="font-bold text-lg">{testResults.overall_score}/100</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Quality Tier:</span>
              <span className="font-medium">{testResults.quality_tier || 'N/A'}</span>
            </div>
            {testResults.category_scores && (
              <div className="mt-4">
                <div className="text-gray-400 mb-2">Category Scores:</div>
                <div className="space-y-1">
                  {Object.entries(testResults.category_scores).map(([category, score]) => (
                    <div key={category} className="flex justify-between">
                      <span>{category}:</span>
                      <span>{score}/30</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Step 6: Finalize
function FinalizeStep({ projectData, handleCreateProject, isCreating }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Finalize Your Project</h2>
        <p className="text-gray-400 mb-6">
          Review your project setup and create your custom writing environment
        </p>
      </div>

      {/* Summary */}
      <div className="bg-gray-700 p-6 rounded-lg space-y-4">
        <div>
          <div className="text-sm text-gray-400 mb-1">Project Name</div>
          <div className="font-medium">{projectData.name}</div>
        </div>
        <div>
          <div className="text-sm text-gray-400 mb-1">Genre</div>
          <div className="font-medium capitalize">{projectData.genre}</div>
        </div>
        <div>
          <div className="text-sm text-gray-400 mb-1">Voice Passages</div>
          <div className="font-medium">{projectData.examplePassages.length} passages</div>
        </div>
        <div>
          <div className="text-sm text-gray-400 mb-1">Custom Skills</div>
          <div className="font-medium">6 skills generated</div>
        </div>
        {projectData.notebooklmUrls.length > 0 && (
          <div>
            <div className="text-sm text-gray-400 mb-1">NotebookLM Integration</div>
            <div className="font-medium">{projectData.notebooklmUrls.length} notebook(s) linked</div>
          </div>
        )}
      </div>

      {/* What Will Be Created */}
      <div className="bg-gray-700 p-4 rounded">
        <h4 className="font-semibold mb-3">What Will Be Created</h4>
        <div className="text-sm space-y-1 font-mono text-gray-300">
          <div>projects/{projectData.name}/</div>
          <div className="ml-4">├── .claude/skills/ (6 custom skills)</div>
          <div className="ml-4">├── knowledge/craft/ (voice profile, story context)</div>
          <div className="ml-4">├── scenes/ (manuscript directory)</div>
          <div className="ml-4">├── config.json (project configuration)</div>
          <div className="ml-4">└── README.md (usage guide)</div>
        </div>
      </div>

      {/* Create Button */}
      <div className="flex justify-center pt-4">
        <button
          onClick={handleCreateProject}
          disabled={isCreating}
          className="px-8 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg font-medium flex items-center gap-2"
        >
          {isCreating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Creating Project...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Create Project
            </>
          )}
        </button>
      </div>
    </div>
  );
}
