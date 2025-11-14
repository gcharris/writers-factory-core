# Cloud Agent Sprint 4 Tasks

**Date**: November 14, 2025
**Status**: Ready to start
**Previous Work**: Sprint 1+2+3 ALL APPROVED ✅ (Grade: A+)

---

## 🎉 Sprint 3 Review Results

**Your work was EXCELLENT AGAIN!** Here's what Claude Code found:

- ✅ All 6 tasks delivered (100% complete)
- ✅ Code quality: A+ (99/100)
- ✅ Perfect integration with Ollama backend
- ✅ Build succeeds (100kB gzipped, 1.12s)
- ✅ All features working flawlessly

**Approved for merge to main** 🚀

---

## 🎯 Sprint 4: Brainstorm Landing Page + Creation Wizard

Now that the core editing and AI tools are solid, add the **"Brainstorm"** landing page - a user-friendly starting point for new projects with the Creation Wizard.

**Timeline**: 2-3 days
**Priority**: HIGH (this becomes the app's home screen)

---

## 📋 Tasks

### Task 4-01: Brainstorm Landing Page Layout

**Create**: `src/features/brainstorm/BrainstormPage.jsx`

Build the main "Brainstorm" landing page as the app's home screen when no manuscript is loaded.

**Layout Structure**:

```jsx
export function BrainstormPage({ onProjectCreated }) {
  const [showWizard, setShowWizard] = useState(false);

  return (
    <div className="h-screen flex flex-col bg-gray-900 text-gray-100">
      {/* Header */}
      <div className="h-16 border-b border-gray-700 bg-gray-800 flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <span className="text-2xl">✨</span>
          <h1 className="text-xl font-bold">Writers Factory</h1>
        </div>
        <div className="text-sm text-gray-400">
          Ready to create your masterpiece?
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto py-12 px-6 space-y-12">
          {/* Hero Section */}
          <div className="text-center space-y-4">
            <h2 className="text-4xl font-bold">Start Your Novel</h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Use the Creation Wizard to build your story foundation, or import an existing manuscript.
            </p>
          </div>

          {/* Action Cards */}
          <div className="grid grid-cols-2 gap-6">
            {/* Creation Wizard Card */}
            <button
              onClick={() => setShowWizard(true)}
              className="p-8 bg-gradient-to-br from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-lg text-left transition-all"
            >
              <div className="text-3xl mb-3">🎨</div>
              <h3 className="text-xl font-bold mb-2">Creation Wizard</h3>
              <p className="text-blue-100 text-sm">
                Interactive Q&A to define your story's foundation, characters, and world.
              </p>
            </button>

            {/* Import Manuscript Card */}
            <button
              className="p-8 bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-600 rounded-lg text-left transition-all"
            >
              <div className="text-3xl mb-3">📚</div>
              <h3 className="text-xl font-bold mb-2">Import Manuscript</h3>
              <p className="text-gray-400 text-sm">
                Load an existing project from disk to continue editing.
              </p>
            </button>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-3 gap-6 pt-8">
            <div className="text-center space-y-2">
              <div className="text-2xl">🤖</div>
              <h4 className="font-semibold">23 AI Models</h4>
              <p className="text-sm text-gray-400">Compare outputs from multiple LLMs</p>
            </div>
            <div className="text-center space-y-2">
              <div className="text-2xl">🦙</div>
              <h4 className="font-semibold">Local Models</h4>
              <p className="text-sm text-gray-400">Use Ollama for FREE generations</p>
            </div>
            <div className="text-center space-y-2">
              <div className="text-2xl">📖</div>
              <h4 className="font-semibold">Knowledge Base</h4>
              <p className="text-sm text-gray-400">Query your research with AI</p>
            </div>
          </div>

          {/* NotebookLM Setup Link */}
          <div className="p-6 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <div className="flex items-start gap-4">
              <div className="text-2xl">📓</div>
              <div>
                <h4 className="font-semibold mb-1">NotebookLM Integration</h4>
                <p className="text-sm text-gray-400 mb-3">
                  Connect your Google NotebookLM for source-grounded research and character development.
                </p>
                <button className="text-sm text-blue-400 hover:text-blue-300">
                  Setup Guide →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Creation Wizard Modal */}
      {showWizard && (
        <CreationWizard onComplete={onProjectCreated} onClose={() => setShowWizard(false)} />
      )}
    </div>
  );
}
```

**Update**: `src/App.jsx`

Add logic to show BrainstormPage when no manuscript is loaded:

```jsx
import { BrainstormPage } from './features/brainstorm/BrainstormPage';

function App() {
  const [hasManuscript, setHasManuscript] = useState(false);

  // Check if manuscript exists on mount
  useEffect(() => {
    fetch('http://localhost:8000/api/manuscript/tree')
      .then(res => res.json())
      .then(data => {
        setHasManuscript(data.acts && data.acts.length > 0);
      });
  }, []);

  // Show brainstorm page if no manuscript
  if (!hasManuscript) {
    return (
      <QueryClientProvider client={queryClient}>
        <BrainstormPage onProjectCreated={() => setHasManuscript(true)} />
        <Toaster position="top-right" theme="dark" />
      </QueryClientProvider>
    );
  }

  // Otherwise show main editor...
  return (/* existing App.jsx code */);
}
```

**Acceptance**:
- ✅ Beautiful landing page with clear CTAs
- ✅ 2 main action cards (Wizard + Import)
- ✅ Features grid showcases key capabilities
- ✅ NotebookLM integration highlighted
- ✅ Shows when no manuscript exists
- ✅ Hides when manuscript loaded

---

### Task 4-02: Creation Wizard - Multi-Step Flow

**Create**: `src/features/brainstorm/CreationWizard.jsx`

Build interactive wizard that walks users through story creation.

**Phases**:
1. **Foundation** (genre, theme, tone)
2. **Characters** (protagonist, antagonist, supporting)
3. **World** (setting, rules, conflicts)
4. **Structure** (acts, key scenes)

**Implementation**:

```jsx
const WIZARD_PHASES = [
  {
    id: 'foundation',
    title: 'Story Foundation',
    icon: '🏗️',
    questions: [
      { id: 'genre', label: 'What genre is your story?', type: 'select', options: ['Science Fiction', 'Fantasy', 'Thriller', 'Literary Fiction', 'Mystery', 'Romance'] },
      { id: 'theme', label: 'What is the central theme?', type: 'textarea', placeholder: 'e.g., The cost of progress, redemption, identity...' },
      { id: 'tone', label: 'What tone do you want?', type: 'select', options: ['Dark & Serious', 'Light & Humorous', 'Balanced', 'Philosophical'] },
    ]
  },
  {
    id: 'characters',
    title: 'Main Characters',
    icon: '👥',
    questions: [
      { id: 'protagonist', label: 'Describe your protagonist', type: 'textarea', placeholder: 'Name, background, key traits...' },
      { id: 'antagonist', label: 'Describe your antagonist', type: 'textarea', placeholder: 'Who or what opposes the protagonist?' },
      { id: 'supporting', label: 'Key supporting characters', type: 'textarea', placeholder: 'List 2-3 important side characters...' },
    ]
  },
  {
    id: 'world',
    title: 'World & Setting',
    icon: '🌍',
    questions: [
      { id: 'setting', label: 'Where does your story take place?', type: 'textarea', placeholder: 'Time period, location, unique features...' },
      { id: 'rules', label: 'What are the rules of this world?', type: 'textarea', placeholder: 'Magic system, technology, social structures...' },
      { id: 'conflict', label: 'What is the central conflict?', type: 'textarea', placeholder: 'The main problem driving the story...' },
    ]
  },
  {
    id: 'structure',
    title: 'Story Structure',
    icon: '📐',
    questions: [
      { id: 'acts', label: 'How many acts?', type: 'number', default: 3 },
      { id: 'opening', label: 'How does the story open?', type: 'textarea', placeholder: 'First scene or chapter...' },
      { id: 'climax', label: 'What is the climax?', type: 'textarea', placeholder: 'The big turning point...' },
    ]
  }
];

export function CreationWizard({ onComplete, onClose }) {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);

  const phase = WIZARD_PHASES[currentPhase];
  const progress = ((currentPhase + 1) / WIZARD_PHASES.length) * 100;

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleNext = async () => {
    if (currentPhase < WIZARD_PHASES.length - 1) {
      setCurrentPhase(prev => prev + 1);
    } else {
      // Final phase - generate project
      setIsGenerating(true);
      try {
        const res = await fetch('http://localhost:8000/api/wizard/complete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ answers })
        });
        const data = await res.json();
        onComplete(data);
      } catch (error) {
        toast.error('Failed to create project');
      } finally {
        setIsGenerating(false);
      }
    }
  };

  const handleBack = () => {
    if (currentPhase > 0) {
      setCurrentPhase(prev => prev - 1);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-800 rounded-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold flex items-center gap-3">
              <span>{phase.icon}</span>
              {phase.title}
            </h2>
            <button onClick={onClose} className="text-gray-400 hover:text-white">
              ✕
            </button>
          </div>
          {/* Progress Bar */}
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-blue-600 transition-all" style={{ width: `${progress}%` }} />
          </div>
          <div className="text-sm text-gray-400 mt-2">
            Phase {currentPhase + 1} of {WIZARD_PHASES.length}
          </div>
        </div>

        {/* Questions */}
        <div className="p-6 space-y-6">
          {phase.questions.map(question => (
            <div key={question.id}>
              <label className="block text-sm font-medium mb-2">{question.label}</label>
              {question.type === 'textarea' ? (
                <textarea
                  value={answers[question.id] || ''}
                  onChange={(e) => handleAnswer(question.id, e.target.value)}
                  placeholder={question.placeholder}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm resize-y min-h-[100px]"
                />
              ) : question.type === 'select' ? (
                <select
                  value={answers[question.id] || ''}
                  onChange={(e) => handleAnswer(question.id, e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm"
                >
                  <option value="">Select...</option>
                  {question.options.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              ) : (
                <input
                  type={question.type}
                  value={answers[question.id] || question.default || ''}
                  onChange={(e) => handleAnswer(question.id, e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm"
                />
              )}
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="p-6 border-t border-gray-700 flex items-center justify-between">
          <button
            onClick={handleBack}
            disabled={currentPhase === 0}
            className="px-4 py-2 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Back
          </button>
          <button
            onClick={handleNext}
            disabled={isGenerating}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium disabled:opacity-50"
          >
            {isGenerating ? 'Creating...' : currentPhase === WIZARD_PHASES.length - 1 ? 'Create Project' : 'Next →'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Backend** (`webapp/backend/simple_app.py`):

Add endpoint to process wizard completion:

```python
@app.post("/api/wizard/complete")
async def wizard_complete(request: dict):
    """Complete the creation wizard and generate project."""
    try:
        answers = request.get("answers", {})

        # Create new project directory
        project_name = f"project_{answers.get('genre', 'story').lower().replace(' ', '_')}"
        project_dir = project_path / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Save wizard answers as project brief
        brief_path = project_dir / "creative_brief.json"
        with open(brief_path, 'w') as f:
            json.dump(answers, f, indent=2)

        # Generate initial outline using AI (optional - can be added later)
        # For now, just return success

        return {
            "success": True,
            "project_name": project_name,
            "project_path": str(project_dir),
            "message": "Project created! You can now start writing."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Acceptance**:
- ✅ 4-phase wizard flow
- ✅ Progress bar shows current phase
- ✅ Back/Next navigation
- ✅ All question types work (text, textarea, select, number)
- ✅ Final phase creates project
- ✅ Saves creative brief to disk
- ✅ Returns to editor after completion

---

### Task 4-03: NotebookLM Setup Guide

**Create**: `src/features/brainstorm/NotebookLMGuide.jsx`

Modal explaining how to set up NotebookLM integration.

```jsx
export function NotebookLMGuide({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-800 rounded-lg max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">NotebookLM Setup Guide</h2>
            <button onClick={onClose} className="text-gray-400 hover:text-white">✕</button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* What is NotebookLM */}
          <section>
            <h3 className="text-lg font-semibold mb-2">What is NotebookLM?</h3>
            <p className="text-gray-400 text-sm">
              Google's NotebookLM is an AI research assistant that lets you upload documents and ask questions.
              It provides <strong>source-grounded answers</strong> with citations, drastically reducing hallucinations.
            </p>
          </section>

          {/* Setup Steps */}
          <section>
            <h3 className="text-lg font-semibold mb-3">Setup Steps</h3>
            <ol className="space-y-3 text-sm">
              <li className="flex gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center font-semibold">1</span>
                <div>
                  <strong>Create a NotebookLM notebook</strong>
                  <p className="text-gray-400 mt-1">
                    Go to <a href="https://notebooklm.google.com" target="_blank" className="text-blue-400 hover:underline">notebooklm.google.com</a> and create a new notebook
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center font-semibold">2</span>
                <div>
                  <strong>Upload your research documents</strong>
                  <p className="text-gray-400 mt-1">
                    Character profiles, world-building notes, plot outlines, research articles, etc.
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center font-semibold">3</span>
                <div>
                  <strong>Get your Notebook ID</strong>
                  <p className="text-gray-400 mt-1">
                    Copy the notebook ID from the URL (the long string after /notebook/)
                  </p>
                </div>
              </li>
              <li className="flex gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center font-semibold">4</span>
                <div>
                  <strong>Configure in Writers Factory</strong>
                  <p className="text-gray-400 mt-1">
                    Go to Settings → NotebookLM and paste your notebook ID
                  </p>
                </div>
              </li>
            </ol>
          </section>

          {/* Example Use Cases */}
          <section>
            <h3 className="text-lg font-semibold mb-3">Example Queries</h3>
            <div className="space-y-2 text-sm">
              <div className="p-3 bg-gray-700 rounded">
                <strong>Query:</strong> "What are Mickey's key personality traits?"<br/>
                <span className="text-gray-400">Answer: Based on your character profile...</span>
              </div>
              <div className="p-3 bg-gray-700 rounded">
                <strong>Query:</strong> "What happened in Chapter 3?"<br/>
                <span className="text-gray-400">Answer: According to your outline...</span>
              </div>
              <div className="p-3 bg-gray-700 rounded">
                <strong>Query:</strong> "How does quantum entanglement work in this world?"<br/>
                <span className="text-gray-400">Answer: From your world-building doc...</span>
              </div>
            </div>
          </section>

          {/* Benefits */}
          <section className="p-4 bg-blue-900/20 border border-blue-700/50 rounded">
            <h4 className="font-semibold mb-2">Why Use NotebookLM?</h4>
            <ul className="space-y-1 text-sm text-gray-300">
              <li>✅ Source-grounded answers (no hallucinations)</li>
              <li>✅ Automatic citations to your documents</li>
              <li>✅ Perfect for complex world-building</li>
              <li>✅ Free to use (Google product)</li>
              <li>✅ Integrates with Writers Factory Knowledge panel</li>
            </ul>
          </section>
        </div>

        <div className="p-6 border-t border-gray-700">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium"
          >
            Got it!
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Update**: Link from BrainstormPage:

```jsx
const [showNotebookLMGuide, setShowNotebookLMGuide] = useState(false);

// In NotebookLM card:
<button
  onClick={() => setShowNotebookLMGuide(true)}
  className="text-sm text-blue-400 hover:text-blue-300"
>
  Setup Guide →
</button>

{showNotebookLMGuide && <NotebookLMGuide onClose={() => setShowNotebookLMGuide(false)} />}
```

**Acceptance**:
- ✅ Clear explanation of NotebookLM
- ✅ Step-by-step setup instructions
- ✅ Example use cases
- ✅ Benefits highlighted
- ✅ External link to notebooklm.google.com
- ✅ Opens from Brainstorm page

---

### Task 4-04: Import Manuscript Flow

**Update**: `src/features/brainstorm/BrainstormPage.jsx`

Add functionality to import existing manuscript:

```jsx
const handleImport = async () => {
  try {
    // Trigger file picker (for now, just show coming soon)
    toast.info('Import functionality coming soon! For now, use the import script.');

    // Future implementation:
    // const res = await fetch('http://localhost:8000/api/manuscript/import', {
    //   method: 'POST',
    //   body: formData
    // });
  } catch (error) {
    toast.error('Import failed');
  }
};

// In Import card:
<button
  onClick={handleImport}
  className="p-8 bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-600 rounded-lg text-left transition-all"
>
  {/* ... */}
</button>
```

**Backend** (`webapp/backend/simple_app.py`):

Add placeholder endpoint (will be fully implemented later):

```python
@app.post("/api/manuscript/import")
async def import_manuscript(request: dict):
    """Import an existing manuscript."""
    try:
        # For now, just check if manuscript exists
        manuscript_path = project_path / ".manuscript" / "explants-v1"

        if manuscript_path.exists():
            return {
                "success": True,
                "message": "Manuscript found and loaded"
            }
        else:
            return {
                "success": False,
                "error": "No manuscript found. Use the import script first."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Acceptance**:
- ✅ Import button shows in Brainstorm page
- ✅ Clicking shows "coming soon" toast
- ✅ Backend endpoint ready for future implementation
- ✅ Doesn't break existing functionality

---

### Task 4-05: Template Library Preview

**Create**: `src/features/brainstorm/TemplateLibrary.jsx`

Show a preview of available story templates (expandable in future sprints).

```jsx
const TEMPLATES = [
  {
    id: 'hero-journey',
    name: "Hero's Journey",
    icon: '⚔️',
    description: 'Classic hero's journey structure with mentor, trials, and transformation',
    genre: 'Fantasy / Adventure'
  },
  {
    id: 'mystery',
    name: 'Mystery/Detective',
    icon: '🔍',
    description: 'Investigation structure with clues, red herrings, and revelation',
    genre: 'Mystery / Thriller'
  },
  {
    id: 'romance',
    name: 'Romance Arc',
    icon: '💕',
    description: 'Meet-cute, conflict, separation, and reunion structure',
    genre: 'Romance'
  },
  {
    id: 'scifi',
    name: 'First Contact',
    icon: '🛸',
    description: 'Discovery, communication, conflict, and resolution with alien species',
    genre: 'Science Fiction'
  },
];

export function TemplateLibrary({ onSelect, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-800 rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Story Templates</h2>
            <button onClick={onClose} className="text-gray-400 hover:text-white">✕</button>
          </div>
          <p className="text-sm text-gray-400 mt-2">
            Choose a template to pre-fill the Creation Wizard with proven story structures
          </p>
        </div>

        <div className="p-6 grid grid-cols-2 gap-4">
          {TEMPLATES.map(template => (
            <button
              key={template.id}
              onClick={() => {
                onSelect(template);
                onClose();
              }}
              className="p-6 bg-gray-700 hover:bg-gray-600 border border-gray-600 hover:border-gray-500 rounded-lg text-left transition-all"
            >
              <div className="text-3xl mb-3">{template.icon}</div>
              <h3 className="font-bold mb-1">{template.name}</h3>
              <p className="text-xs text-gray-400 mb-2">{template.genre}</p>
              <p className="text-sm text-gray-300">{template.description}</p>
            </button>
          ))}
        </div>

        <div className="p-6 border-t border-gray-700">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
```

**Update**: Add "Use Template" button to BrainstormPage:

```jsx
const [showTemplates, setShowTemplates] = useState(false);

// Add button near Creation Wizard card:
<button
  onClick={() => setShowTemplates(true)}
  className="text-sm text-blue-400 hover:text-blue-300"
>
  Or start from a template →
</button>

{showTemplates && (
  <TemplateLibrary
    onSelect={(template) => {
      // Pre-fill wizard with template data
      setShowWizard(true);
    }}
    onClose={() => setShowTemplates(false)}
  />
)}
```

**Acceptance**:
- ✅ 4 templates shown in grid
- ✅ Each template has icon, name, genre, description
- ✅ Clicking template opens wizard with pre-filled data
- ✅ Clean modal layout
- ✅ Easy to expand with more templates

---

## 🎯 Success Criteria

**Sprint 4 Complete When**:
- ✅ Brainstorm landing page shows when no manuscript
- ✅ Creation Wizard has 4-phase flow
- ✅ Wizard creates project and saves brief
- ✅ NotebookLM setup guide accessible
- ✅ Import manuscript button present
- ✅ Template library preview available
- ✅ App returns to editor after project creation

---

## 📁 File Changes Expected

**New Files**:
- `src/features/brainstorm/BrainstormPage.jsx`
- `src/features/brainstorm/CreationWizard.jsx`
- `src/features/brainstorm/NotebookLMGuide.jsx`
- `src/features/brainstorm/TemplateLibrary.jsx`

**Modified Files**:
- `src/App.jsx` (add BrainstormPage routing)
- `webapp/backend/simple_app.py` (add `/api/wizard/complete`, `/api/manuscript/import`)

---

## 🧪 Testing

After implementation:

1. **Test Brainstorm Page**:
   - Start app with no manuscript
   - Should show Brainstorm landing page
   - Check all cards render correctly

2. **Test Creation Wizard**:
   - Click "Creation Wizard" button
   - Walk through all 4 phases
   - Fill in answers
   - Click "Create Project"
   - Should return to editor

3. **Test NotebookLM Guide**:
   - Click "Setup Guide" link
   - Verify all instructions clear
   - External link works
   - Close button works

4. **Test Template Library**:
   - Click "Use Template"
   - Should show 4 templates
   - Clicking template opens wizard
   - Verify template data pre-fills

---

## 💡 Design Notes

**Visual Style**:
- Continue dark theme (gray-900/800/700)
- Use gradient for primary CTA (Creation Wizard card)
- Icons for visual interest
- Clean, spacious layout (not cramped)

**User Experience**:
- Brainstorm page feels welcoming, not intimidating
- Creation Wizard shows progress clearly
- No dead-ends (always a way forward or back)
- Templates are optional, not required

**Content Tone**:
- Friendly and encouraging
- Clear, jargon-free language
- Emphasize capabilities without overwhelming

---

## 🚀 Ready to Start?

You have all the context:
- ✅ Sprint 1+2+3 code is solid foundation
- ✅ Design patterns established
- ✅ Backend integration patterns clear
- ✅ Just need to add the Brainstorm page layer

**Estimated time**: 2-3 days (5 tasks)

**Expected outcome**: Beautiful landing page that guides new users into the app!

Let's make Sprint 4 as excellent as Sprint 1+2+3! ✨🎨

---

**Document Created**: November 14, 2025
**For**: Cloud Agent (Sprint 4)
**Previous Grade**: A+ on Sprint 1+2+3
**Status**: Ready to start immediately
