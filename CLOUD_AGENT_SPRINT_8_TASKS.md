# 📋 Cloud Agent Sprint 8: Student-Facing Polish

**Sprint**: 8 of 8 (FINAL!)
**Timeline**: 2-3 days
**Priority**: HIGH (Required for January course)
**Status**: Ready to start

---

## 🎯 Sprint Goal

Polish Writers Factory for graduate engineering students taking "AI and the One-Week Novel" course in January 2025. Add onboarding, help documentation, example project, and UX improvements to make the platform immediately accessible to first-time users.

**Target Users**: Graduate engineering students
- **Technical background**: Yes (engineering)
- **Writing experience**: Variable (some beginners)
- **Time constraint**: 1 week to write a novel/novella
- **Learning curve tolerance**: Low (need to start writing immediately)

**What Students Need**:
- Clear onboarding (what is this platform?)
- Quick start guide (how do I begin?)
- Example project (see how it works)
- Help documentation (when stuck)
- Friendly error messages (what went wrong?)

---

## ✅ Tasks (5 total)

### Task 8-01: Welcome Modal & Onboarding ⭐ CRITICAL

**Files**:
- `webapp/frontend-v2/src/features/onboarding/WelcomeModal.jsx` (NEW)
- `webapp/frontend-v2/src/App.jsx` (MODIFY)

**Requirements**:

**1. Create Welcome Modal Component**

Create `webapp/frontend-v2/src/features/onboarding/WelcomeModal.jsx`:

```jsx
import { useState } from 'react';
import { X, Book, Zap, Users, Globe, Lightbulb, Sparkles } from 'lucide-react';

export function WelcomeModal({ onClose, onComplete }) {
  const [step, setStep] = useState(0);

  const steps = [
    {
      title: "Welcome to Writers Factory! 📚",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300 text-lg leading-relaxed">
            Write, draft, and revise your novel in just one week using advanced AI-powered tools.
          </p>

          <div className="grid grid-cols-2 gap-4 mt-6">
            <FeatureCard
              icon={<Zap size={24} className="text-yellow-400" />}
              title="23 AI Models"
              description="Compare outputs from Claude, GPT, Gemini, and more"
            />
            <FeatureCard
              icon={<Users size={24} className="text-blue-400" />}
              title="Character Analysis"
              description="Detect contradictions and dimensional depth"
            />
            <FeatureCard
              icon={<Globe size={24} className="text-green-400" />}
              title="Free Local Models"
              description="Use Ollama for unlimited free generation"
            />
            <FeatureCard
              icon={<Lightbulb size={24} className="text-purple-400" />}
              title="Knowledge Base"
              description="Query NotebookLM for craft advice"
            />
          </div>
        </div>
      )
    },
    {
      title: "How Writers Factory Works",
      content: (
        <div className="space-y-6">
          <Step
            number="1"
            title="Brainstorm Your Story"
            description="Use the Creation Wizard to define your story foundation, characters, world, and structure."
            icon="✨"
          />
          <Step
            number="2"
            title="Generate Scenes"
            description="Use AI models to generate scene drafts. Compare outputs side-by-side to find the best version."
            icon="🎬"
          />
          <Step
            number="3"
            title="Edit & Refine"
            description="Edit scenes in the professional markdown editor. Use AI to enhance, rewrite, or polish your work."
            icon="✍️"
          />
          <Step
            number="4"
            title="Analyze & Improve"
            description="Check character depth, analyze pacing, and ensure consistency across your manuscript."
            icon="📊"
          />
          <Step
            number="5"
            title="Export Your Novel"
            description="Export your finished manuscript to Markdown, HTML, or plain text."
            icon="📥"
          />
        </div>
      )
    },
    {
      title: "Three Ways to Start",
      content: (
        <div className="space-y-4">
          <StartOption
            title="🎯 Creation Wizard (Recommended)"
            description="Guided 4-phase process to build your story from scratch. Perfect for beginners."
            onClick={() => {
              onComplete('wizard');
              onClose();
            }}
          />
          <StartOption
            title="📂 Import Manuscript"
            description="Already have a manuscript? Import your existing work to continue writing with AI assistance."
            onClick={() => {
              onComplete('import');
              onClose();
            }}
          />
          <StartOption
            title="📖 Explore Example Project"
            description="See how Writers Factory works with a pre-loaded demo novel (The Explants - Volume 1 excerpt)."
            onClick={() => {
              onComplete('example');
              onClose();
            }}
          />
        </div>
      )
    }
  ];

  const currentStep = steps[step];

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-gray-800 border-b border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sparkles size={28} className="text-blue-400" />
            <h2 className="text-2xl font-bold">{currentStep.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-200 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-8">
          {currentStep.content}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-800 border-t border-gray-700 p-6 flex items-center justify-between">
          <div className="flex gap-2">
            {steps.map((_, idx) => (
              <div
                key={idx}
                className={`h-2 w-12 rounded-full transition-colors ${
                  idx === step ? 'bg-blue-500' : 'bg-gray-600'
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            {step > 0 && (
              <button
                onClick={() => setStep(step - 1)}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Back
              </button>
            )}

            {step < steps.length - 1 ? (
              <button
                onClick={() => setStep(step + 1)}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
              >
                Next
              </button>
            ) : (
              <button
                onClick={() => {
                  onComplete('skip');
                  onClose();
                }}
                className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Skip for Now
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
      <div className="mb-2">{icon}</div>
      <h4 className="font-semibold mb-1">{title}</h4>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  );
}

function Step({ number, title, description, icon }) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center font-bold text-xl">
        {icon}
      </div>
      <div>
        <h4 className="font-semibold text-lg mb-1">{title}</h4>
        <p className="text-gray-400">{description}</p>
      </div>
    </div>
  );
}

function StartOption({ title, description, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full p-6 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 hover:border-blue-500 rounded-lg text-left transition-all transform hover:scale-[1.02]"
    >
      <h4 className="font-semibold text-lg mb-2">{title}</h4>
      <p className="text-gray-400 text-sm">{description}</p>
    </button>
  );
}
```

**2. Integrate Welcome Modal in App.jsx**

Add to `App.jsx`:

```jsx
import { WelcomeModal } from './features/onboarding/WelcomeModal';

function App() {
  const [showWelcome, setShowWelcome] = useState(() => {
    // Check if user has seen welcome (localStorage)
    return !localStorage.getItem('writers-factory-onboarded');
  });

  const handleWelcomeComplete = (choice) => {
    localStorage.setItem('writers-factory-onboarded', 'true');

    // Handle user choice
    switch (choice) {
      case 'wizard':
        // Navigate to brainstorm page (creation wizard)
        setHasManuscript(false);
        break;
      case 'import':
        // Trigger import flow
        // TODO: Implement
        break;
      case 'example':
        // Load example project
        loadExampleProject();
        break;
      case 'skip':
        // Do nothing, let user explore
        break;
    }
  };

  return (
    <>
      {showWelcome && (
        <WelcomeModal
          onClose={() => setShowWelcome(false)}
          onComplete={handleWelcomeComplete}
        />
      )}

      {/* Rest of app... */}
    </>
  );
}
```

**Success Criteria**:
- ✅ Welcome modal shows on first visit
- ✅ Modal has 3 steps (welcome, how it works, start options)
- ✅ Progress indicator shows current step
- ✅ Back/Next navigation works
- ✅ Start options trigger correct actions
- ✅ localStorage prevents modal from showing again

---

### Task 8-02: Help Documentation Panel ⭐ HIGH

**Files**:
- `webapp/frontend-v2/src/features/help/HelpPanel.jsx` (NEW)
- `webapp/frontend-v2/src/features/help/helpContent.js` (NEW)
- `webapp/frontend-v2/src/App.jsx` (MODIFY - add help button)

**Requirements**:

**1. Create Help Content**

Create `webapp/frontend-v2/src/features/help/helpContent.js`:

```javascript
export const helpTopics = {
  gettingStarted: {
    title: "Getting Started",
    icon: "🚀",
    sections: [
      {
        question: "How do I create a new story?",
        answer: "Click the 'Start Creation Wizard' button on the Brainstorm page. The wizard will guide you through 4 phases: Foundation (title, genre, premise), Characters (protagonist, antagonist), World (setting, rules), and Structure (act structure, pacing)."
      },
      {
        question: "Can I import an existing manuscript?",
        answer: "Yes! Click 'Import Manuscript' and select your .txt, .md, or .docx file. Writers Factory will parse your manuscript and organize it into acts, chapters, and scenes."
      },
      {
        question: "What is the Brainstorm page?",
        answer: "The Brainstorm page is your starting point for new projects. It offers four options: Creation Wizard (guided story setup), Import Manuscript (bring existing work), NotebookLM Setup (knowledge base), and Template Library (pre-built story structures)."
      }
    ]
  },

  aiModels: {
    title: "AI Models",
    icon: "🤖",
    sections: [
      {
        question: "Which AI models are available?",
        answer: "Writers Factory supports 23+ models including Claude (Anthropic), GPT-4 (OpenAI), Gemini (Google), Qwen, DeepSeek, and local models via Ollama. Each model has different strengths for different tasks."
      },
      {
        question: "What is Economy Mode?",
        answer: "Economy Mode automatically prefers free local models (via Ollama) when available. This can save 90%+ on costs. Toggle Economy Mode in the top toolbar. Green means local models will be used when possible."
      },
      {
        question: "How do I use Ollama for free generation?",
        answer: "Install Ollama from ollama.ai, then run 'ollama pull llama3' to download a model. Writers Factory will automatically detect Ollama and show local models in the model selector. These are 100% free!"
      },
      {
        question: "What is Tournament Mode?",
        answer: "Tournament Mode generates the same scene with 4 different models simultaneously, then displays them side-by-side for comparison. This helps you find the best AI model for your writing style."
      }
    ]
  },

  sceneEditor: {
    title: "Scene Editor",
    icon: "✍️",
    sections: [
      {
        question: "How do I format text?",
        answer: "The scene editor supports markdown formatting. Use **bold**, *italic*, # headers, and more. You can also switch to WYSIWYG mode for visual editing. The toolbar provides formatting buttons."
      },
      {
        question: "Does my work autosave?",
        answer: "Yes! Writers Factory autosaves your scenes every 2 seconds after you stop typing. Look for the 'Last saved' timestamp at the bottom of the editor."
      },
      {
        question: "How do I export my work?",
        answer: "Click the 'Export' button in the scene editor to download your scene as Markdown (.md), Plain Text (.txt), or HTML (.html). You can also export the entire manuscript from the Manuscript menu."
      },
      {
        question: "What is distraction-free mode?",
        answer: "Press F11 or click the Fullscreen button to enter distraction-free mode. This hides all panels and expands the editor to full screen. Press Escape or F11 to exit."
      }
    ]
  },

  characterAnalysis: {
    title: "Character Analysis",
    icon: "👥",
    sections: [
      {
        question: "What is the Character Panel?",
        answer: "The Character Panel analyzes your characters for dimensional depth using professional craft principles. It checks for internal/external contradictions, flaw depth, and ensures your protagonist is the most dimensional character."
      },
      {
        question: "What is a 'depth score'?",
        answer: "Depth score (0-100) measures character complexity. Scores below 50 indicate a flat character, 50-80 is developing, and 80+ is dimensional. The score is based on 5 checks: external contradiction, internal contradiction, flaw depth, values/fears, and appearance/speech."
      },
      {
        question: "What does 'True Character vs Characterization' mean?",
        answer: "True Character is your character's inner core (traits, values, fears). Characterization is what others observe (appearance, mannerisms, speech). Professional characters have contradictions between these two layers."
      },
      {
        question: "How do I improve a flat character?",
        answer: "Add contradictions! Give them opposing traits (ambitious yet guilty), or create dissonance between their True Character (loyal) and Characterization (appears untrustworthy). The Character Panel provides specific recommendations."
      }
    ]
  },

  costTracking: {
    title: "Cost Tracking",
    icon: "💰",
    sections: [
      {
        question: "How much does Writers Factory cost?",
        answer: "Writers Factory itself is free! You pay for cloud AI models (Claude, GPT, Gemini) based on usage. Local models via Ollama are completely free. Enable Economy Mode to minimize costs."
      },
      {
        question: "Where can I see my costs?",
        answer: "Click the '$X.XX' cost indicator in the top toolbar to open the Cost Dashboard. It shows total spent, savings from local models, generation counts, and a breakdown by model."
      },
      {
        question: "How can I reduce costs?",
        answer: "Use Economy Mode (prefers local models), use Agent Profiles (assign cheaper models to drafts), use Tournament Mode selectively (4x cost), and use local Ollama models for first drafts."
      }
    ]
  },

  troubleshooting: {
    title: "Troubleshooting",
    icon: "🔧",
    sections: [
      {
        question: "Ollama models aren't showing up",
        answer: "Make sure Ollama is running (check localhost:11434 in your browser). Restart Writers Factory backend if needed. You should see a green 'Ollama Running' banner at the top when connected."
      },
      {
        question: "My scene didn't save",
        answer: "Check the 'Last saved' timestamp in the editor. If it says 'Never', there may be a backend connection issue. Try refreshing the page. Your work is autosaved to the backend every 2 seconds."
      },
      {
        question: "AI generation failed",
        answer: "Check that your API keys are configured (see Settings > API Keys). If using a cloud model, verify your API key is valid and has credits. If using Ollama, make sure Ollama is running."
      },
      {
        question: "The app won't load",
        answer: "Make sure the backend is running: 'python webapp/backend/simple_app.py'. The backend should be accessible at localhost:8000. Check the browser console for errors."
      }
    ]
  }
};

export const quickTips = [
  "💡 Press F11 for distraction-free writing mode",
  "💡 Use Ollama for unlimited free AI generation",
  "💡 Tournament Mode compares 4 models at once",
  "💡 Economy Mode can save 90%+ on AI costs",
  "💡 Character depth score 80+ = dimensional",
  "💡 Your work autosaves every 2 seconds",
  "💡 Export scenes as Markdown, HTML, or text",
  "💡 NotebookLM provides source-grounded research",
  "💡 Use Agent Profiles to assign models by task",
  "💡 Creation Wizard guides you through story setup"
];
```

**2. Create Help Panel Component**

Create `webapp/frontend-v2/src/features/help/HelpPanel.jsx`:

```jsx
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
          Need more help? Join the{' '}
          <a href="#" className="text-blue-400 hover:underline">community forum</a>
          {' '}or{' '}
          <a href="#" className="text-blue-400 hover:underline">report an issue</a>
        </div>
      </div>
    </div>
  );
}
```

**3. Add Help Button to App**

In `App.jsx`, add help button to toolbar:

```jsx
import { HelpPanel } from './features/help/HelpPanel';

const [showHelp, setShowHelp] = useState(false);

// In toolbar:
<button
  onClick={() => setShowHelp(true)}
  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm flex items-center gap-2"
  title="Help & Documentation"
>
  <Book size={16} />
  Help
</button>

{showHelp && <HelpPanel onClose={() => setShowHelp(false)} />}
```

**Success Criteria**:
- ✅ Help button in top toolbar
- ✅ Help panel shows 6 topic categories
- ✅ Search filters topics
- ✅ Clicking topic shows detailed Q&A
- ✅ Back button returns to topic list
- ✅ Random quick tip displayed

---

### Task 8-03: Example Project (Demo Novel) ⭐ MEDIUM

**Files**:
- `webapp/backend/simple_app.py` (MODIFY - add example project endpoint)
- `webapp/backend/example_project.json` (NEW - example data)

**Requirements**:

**1. Create Example Project Data**

Create `webapp/backend/example_project.json`:

```json
{
  "title": "The Explants - Volume 1 (Excerpt)",
  "author": "Example Project",
  "description": "A demo novel showcasing Writers Factory features. This is an excerpt from The Explants, a sci-fi novel about consciousness, quantum mechanics, and what it means to be human.",
  "acts": [
    {
      "id": "act-1",
      "title": "Act 1: The Awakening",
      "chapters": [
        {
          "id": "ch-1",
          "title": "Chapter 1: New Beginnings",
          "scenes": [
            {
              "id": "scene-1",
              "title": "1.1 Mickey's First Day",
              "content": "Mickey Bardot stared at the quantum interface, its swirling patterns of light and probability dancing before her eyes. She'd seen similar displays a thousand times in her work as a consciousness researcher, but this was different. This was *her* consciousness, mapped and measured, reduced to mathematical certainties and quantum states.\n\n\"Ready?\" Dr. Chen's voice was gentle, almost apologetic.\n\nMickey nodded, not trusting herself to speak. The implant surgery had been routine—they'd done thousands by now—but knowing that didn't make it any less terrifying. In a few moments, she would become one of them: an Explant. A human consciousness expanded beyond the confines of flesh and bone, interfaced directly with quantum computing systems that could process thoughts at speeds her biological brain couldn't even comprehend.\n\n\"Beginning calibration,\" Dr. Chen said, fingers dancing across the holographic controls.\n\nThe world *shifted*.\n\nIt wasn't like anything Mickey had imagined. Not a sudden jolt or flash of light. It was more like... becoming aware of a room she'd always been in but had never noticed before. A space that existed alongside reality, overlapping it, *interpenetrating* it.\n\nShe could see the quantum states now. Not as abstract mathematical constructs, but as *things*. Real, tangible, *present*. The air itself was alive with possibility, every atom vibrating with potential futures, collapsing and reforming in an endless dance of probability.\n\n\"How do you feel?\" Dr. Chen asked.\n\nMickey opened her mouth to answer, then realized she didn't have to. The thought itself was enough. Her consciousness reached out through the quantum interface, found Dr. Chen's implant, and *connected*.\n\n*Different,* she thought-spoke. *I feel different.*\n\n*That's normal,* Dr. Chen's response came back, not as words but as pure meaning. *It takes time to adjust. Your brain is still learning to process the expanded input.*\n\n*How much time?*\n\n*Weeks. Months. For some people, never. There's no predicting how consciousness will adapt to this kind of enhancement.*\n\nMickey felt a flutter of anxiety—or was it excitement? The emotions themselves felt different now, as if she were experiencing them from two places at once. Her biological brain registered the familiar rush of neurotransmitters, while her quantum-enhanced consciousness observed the whole process with a strange, detached clarity.\n\nShe was both the experience and the observer of the experience. Both the wave and the particle. Both Mickey and something more.\n\n\"Welcome to the Q-space, Mickey,\" Dr. Chen said aloud, a smile in her voice. \"Your life starts now.\"",
              "word_count": 445
            },
            {
              "id": "scene-2",
              "title": "1.2 The First Connection",
              "content": "The faculty lounge had always been Mickey's refuge. A quiet corner where she could grade papers, sip terrible coffee, and pretend the weight of her research wasn't crushing her under its implications. But now, walking into the familiar space with her new quantum-enhanced vision, it felt like entering an alien world.\n\n*Too much,* she thought, closing her eyes against the overwhelming sensory input. Every surface *hummed* with quantum information. She could see the electromagnetic fields from phones and laptops, watch photons bouncing off surfaces, trace the decay of radioactive isotopes in the concrete walls.\n\n\"First day after calibration?\" a voice asked.\n\nMickey opened her eyes—carefully, slowly—to see Professor Sarah Kim sitting at their usual table. Sarah's quantum signature was... complex. Layered. Years of enhancement had transformed her consciousness into something baroque and beautiful, a crystalline structure of thought and possibility that made Mickey's newly-upgraded mind look like a child's scribble by comparison.\n\n\"That obvious?\" Mickey managed, sliding into the seat across from her.\n\nSarah smiled. \"You're looking at *everything* like it's the first time. Classic new Explant behavior. Don't worry, you'll learn to filter the noise. Eventually, it becomes second nature.\"\n\n\"How long did it take you?\"\n\n\"Six months before I could walk into a crowded room without wanting to scream. A year before I could hold a conversation without getting distracted by everyone's quantum states. Two years before I stopped seeing the universe as a chaotic mess of probability and started seeing the patterns.\"\n\nMickey groaned. \"I'm giving a lecture tomorrow. On consciousness and quantum mechanics. The irony is not lost on me.\"\n\n\"Want some advice?\" Sarah leaned forward, her quantum signature pulsing with something that felt like... concern? Empathy? Mickey was still learning to read these new forms of communication. \"Don't try to explain what you're experiencing now. Your old vocabulary doesn't apply anymore. You'll just confuse your students and yourself.\"\n\n\"Then what do I do?\"\n\n\"Teach what you *knew* before. The mathematical frameworks, the philosophical implications, the experimental results. Leave the direct experience of Q-space for later, when you have the language for it.\"\n\nMickey nodded, then felt a sudden spike of... something. Not quite emotion, not quite thought. More like a warning, a premonition, a quantum probability collapsing into certainty.\n\nSarah felt it too. Her expression shifted, darkened.\n\n\"Mickey,\" she said slowly, \"when they briefed you on the implant, did they mention the *others*?\"\n\n\"Others?\"\n\n\"The entities in Q-space. The things that aren't human but also aren't... not human. The consciousness patterns that exist in the quantum foam itself.\"\n\nMickey felt her blood run cold. \"No. They definitely didn't mention that.\"\n\nSarah's quantum signature flared with what could only be described as grim amusement. \"Well. Welcome to the real initiation, Mickey. The calibration is just the beginning. Now comes the part where you learn what it *really* means to be an Explant.\"\n\nAnd in that moment, Mickey felt it. A presence in Q-space. Vast. Ancient. Aware.\n\nWatching her.\n\n*Welcome, young one,* a voice that was not a voice whispered through the quantum foam. *We've been waiting for you.*",
              "word_count": 582
            }
          ]
        }
      ]
    }
  ],
  "characters": [
    {
      "id": "char-mickey",
      "name": "Mickey Bardot",
      "role": "protagonist",
      "core_traits": ["brilliant", "driven", "curious", "guilty", "doubtful"],
      "observable_traits": ["confident", "composed", "professional"],
      "values": ["Truth", "Understanding", "Human potential"],
      "fears": ["Losing her humanity", "Making a catastrophic mistake", "Being wrong about consciousness"],
      "appearance": "Mid-30s, athletic build, sharp features, always wears practical clothes",
      "speech_pattern": "Direct, technical, uses scientific metaphors",
      "fatal_flaw": "Hubris disguised as scientific curiosity",
      "mistaken_belief": "She can control the uncontrollable through sheer intellectual force",
      "transformation_goal": "Learn to accept uncertainty and embrace the limits of knowledge"
    }
  ]
}
```

**2. Add Example Project Endpoint**

In `webapp/backend/simple_app.py`:

```python
@app.post("/api/example/load")
async def load_example_project():
    """Load the example project (The Explants excerpt)."""
    try:
        import json
        from pathlib import Path

        # Load example data
        example_path = Path(__file__).parent / "example_project.json"
        with open(example_path, 'r') as f:
            example_data = json.load(f)

        # Convert to Manuscript object
        from factory.core.manuscript.structure import Manuscript
        manuscript = Manuscript.from_dict(example_data)

        # Cache as current manuscript
        _manuscript_cache['current'] = manuscript

        return {
            "success": True,
            "message": "Example project loaded successfully",
            "manuscript": example_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**3. Add Load Example Button**

In `BrainstormPage.jsx` (or WelcomeModal), add button:

```jsx
const loadExampleProject = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/example/load', {
      method: 'POST'
    });
    if (response.ok) {
      toast.success('Example project loaded!');
      onProjectCreated(); // Reload app with example
    }
  } catch (error) {
    toast.error('Failed to load example project');
  }
};

<button
  onClick={loadExampleProject}
  className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold"
>
  📖 Load Example Project
</button>
```

**Success Criteria**:
- ✅ Example project JSON created
- ✅ Backend endpoint loads example
- ✅ Load button triggers example load
- ✅ Example project appears in manuscript tree
- ✅ Example scenes are readable and editable
- ✅ Example character analyzable in Character Panel

---

### Task 8-04: Improved Error Messages ⭐ MEDIUM

**Files**:
- `webapp/frontend-v2/src/utils/errorHandler.js` (NEW)
- Various components (MODIFY - use friendly errors)

**Requirements**:

**1. Create Error Handler Utility**

Create `webapp/frontend-v2/src/utils/errorHandler.js`:

```javascript
/**
 * Friendly error message handler for Writers Factory.
 * Converts technical errors into user-friendly messages.
 */

export function getFriendlyErrorMessage(error, context = {}) {
  // Network errors
  if (error.message?.includes('fetch') || error.message?.includes('network')) {
    return {
      title: "Connection Error",
      message: "Couldn't connect to the Writers Factory backend. Make sure it's running at localhost:8000.",
      action: "Check that you started the backend with: python webapp/backend/simple_app.py",
      icon: "🔌"
    };
  }

  // 404 errors
  if (error.status === 404 || error.message?.includes('404')) {
    if (context.type === 'scene') {
      return {
        title: "Scene Not Found",
        message: "The scene you're looking for doesn't exist. It may have been deleted.",
        action: "Try refreshing the page or selecting a different scene.",
        icon: "📄"
      };
    }
    return {
      title: "Not Found",
      message: "The resource you requested couldn't be found.",
      action: "Try refreshing the page or checking your request.",
      icon: "❓"
    };
  }

  // 500 errors
  if (error.status === 500 || error.message?.includes('500')) {
    return {
      title: "Server Error",
      message: "Something went wrong on the server. This is usually temporary.",
      action: "Try refreshing the page. If the problem persists, check the backend logs.",
      icon: "⚠️"
    };
  }

  // API key errors
  if (error.message?.includes('API key') || error.message?.includes('authentication')) {
    return {
      title: "API Key Missing or Invalid",
      message: "Your AI model API key is missing or invalid.",
      action: "Go to Settings > API Keys and add your API key for the model you're using.",
      icon: "🔑"
    };
  }

  // Ollama errors
  if (error.message?.includes('Ollama') || error.message?.includes('11434')) {
    return {
      title: "Ollama Not Running",
      message: "Ollama isn't running or isn't accessible. Local models won't work without it.",
      action: "Start Ollama by running 'ollama serve' in your terminal, or install from ollama.ai",
      icon: "🦙"
    };
  }

  // Model errors
  if (error.message?.includes('model') && context.type === 'generation') {
    return {
      title: "AI Generation Failed",
      message: "The AI model couldn't generate content. This might be due to API limits, invalid keys, or model unavailability.",
      action: "Check your API keys, try a different model, or enable Economy Mode to use local models.",
      icon: "🤖"
    };
  }

  // Generic error
  return {
    title: "Something Went Wrong",
    message: error.message || "An unexpected error occurred.",
    action: "Try refreshing the page. If the problem persists, check the browser console for details.",
    icon: "❌"
  };
}

/**
 * Display friendly error with toast notification
 */
export function showFriendlyError(error, toast, context = {}) {
  const friendly = getFriendlyErrorMessage(error, context);

  toast.error(
    <div>
      <div className="font-semibold flex items-center gap-2">
        <span>{friendly.icon}</span>
        <span>{friendly.title}</span>
      </div>
      <div className="text-sm mt-1">{friendly.message}</div>
      {friendly.action && (
        <div className="text-xs mt-2 text-gray-400">{friendly.action}</div>
      )}
    </div>,
    { duration: 6000 }
  );
}
```

**2. Use in Components**

Example in `SceneEditor.jsx`:

```jsx
import { showFriendlyError } from '../../utils/errorHandler';

// In error handlers:
try {
  const response = await fetch(`/api/scenes/${sceneId}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  // ...
} catch (error) {
  showFriendlyError(error, toast, { type: 'scene' });
}
```

**Success Criteria**:
- ✅ Error handler converts technical errors to friendly messages
- ✅ Errors include title, message, action, and icon
- ✅ Context-aware errors (scene, generation, etc.)
- ✅ Used throughout components
- ✅ Toast notifications show friendly errors

---

### Task 8-05: Quick Start Guide (Sticky Header) ⭐ LOW

**File**: `webapp/frontend-v2/src/features/onboarding/QuickStartBanner.jsx` (NEW)

**Requirements**:

**1. Create Quick Start Banner**

```jsx
import { useState, useEffect } from 'react';
import { X, ChevronRight } from 'lucide-react';

export function QuickStartBanner() {
  const [dismissed, setDismissed] = useState(() => {
    return localStorage.getItem('writers-factory-quickstart-dismissed') === 'true';
  });

  const [step, setStep] = useState(0);

  const steps = [
    {
      icon: "✨",
      text: "New here? Start with the Creation Wizard to build your story foundation.",
      action: "Create Story"
    },
    {
      icon: "🤖",
      text: "Try Economy Mode to use free local models and save 90%+ on costs.",
      action: "Enable Economy Mode"
    },
    {
      icon: "📚",
      text: "Not sure how something works? Click the Help button for detailed guides.",
      action: "Open Help"
    },
    {
      icon: "👥",
      text: "Check the Character Panel to analyze your characters for dimensional depth.",
      action: "Analyze Characters"
    }
  ];

  useEffect(() => {
    // Auto-advance step every 10 seconds
    const timer = setInterval(() => {
      setStep((prev) => (prev + 1) % steps.length);
    }, 10000);
    return () => clearInterval(timer);
  }, []);

  const handleDismiss = () => {
    setDismissed(true);
    localStorage.setItem('writers-factory-quickstart-dismissed', 'true');
  };

  if (dismissed) return null;

  const currentStep = steps[step];

  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 flex items-center justify-between">
      <div className="flex items-center gap-4 flex-1">
        <span className="text-2xl">{currentStep.icon}</span>
        <p className="text-sm font-medium">{currentStep.text}</p>
      </div>

      <div className="flex items-center gap-3">
        <button
          className="px-4 py-1 bg-white/20 hover:bg-white/30 rounded text-sm font-medium transition-colors flex items-center gap-2"
        >
          {currentStep.action}
          <ChevronRight size={16} />
        </button>

        <button
          onClick={handleDismiss}
          className="text-white/70 hover:text-white transition-colors"
          title="Dismiss quick start tips"
        >
          <X size={20} />
        </button>
      </div>
    </div>
  );
}
```

**2. Add to App**

In `App.jsx`:

```jsx
import { QuickStartBanner } from './features/onboarding/QuickStartBanner';

// In render:
<QuickStartBanner />
```

**Success Criteria**:
- ✅ Banner shows at top of app
- ✅ Rotates through 4 tips every 10 seconds
- ✅ Dismiss button hides banner permanently
- ✅ Action buttons are clickable (implement actions)

---

## 🧪 Testing Checklist

### Welcome & Onboarding
1. ✅ Welcome modal shows on first visit
2. ✅ Modal has 3 steps with navigation
3. ✅ Start options trigger correct actions
4. ✅ Modal doesn't show again after dismissal

### Help Documentation
5. ✅ Help button opens help panel
6. ✅ Search filters topics
7. ✅ Topic detail shows Q&A
8. ✅ Back button works
9. ✅ Quick tips display randomly

### Example Project
10. ✅ Example project loads without errors
11. ✅ Example scenes appear in tree
12. ✅ Example scenes are readable
13. ✅ Example character analyzable

### Error Messages
14. ✅ Network errors show friendly message
15. ✅ 404 errors show context-aware message
16. ✅ API key errors guide to settings
17. ✅ Ollama errors explain how to fix

### Quick Start
18. ✅ Quick start banner shows on load
19. ✅ Tips rotate every 10 seconds
20. ✅ Dismiss button hides banner permanently

---

## 📦 Deliverables

### New Files (8):
1. `webapp/frontend-v2/src/features/onboarding/WelcomeModal.jsx` (~300 lines)
2. `webapp/frontend-v2/src/features/help/HelpPanel.jsx` (~150 lines)
3. `webapp/frontend-v2/src/features/help/helpContent.js` (~400 lines)
4. `webapp/backend/example_project.json` (~150 lines JSON)
5. `webapp/frontend-v2/src/utils/errorHandler.js` (~150 lines)
6. `webapp/frontend-v2/src/features/onboarding/QuickStartBanner.jsx` (~100 lines)

### Modified Files (3):
1. `webapp/frontend-v2/src/App.jsx` (+50 lines - modals, help button)
2. `webapp/backend/simple_app.py` (+30 lines - example endpoint)
3. Various components (+error handling)

**Total new code**: ~1,330 lines

---

## 🎯 Success Criteria

Sprint 8 is complete when:

1. ✅ Welcome modal shows on first visit
2. ✅ Help panel accessible with full documentation
3. ✅ Example project loads and works
4. ✅ Error messages are friendly and actionable
5. ✅ Quick start banner guides new users
6. ✅ All testing checklist items pass
7. ✅ Build succeeds without errors
8. ✅ No console warnings

---

## 📝 Notes for January Course

After Sprint 8, Writers Factory will be **student-ready**:

- ✅ **Welcoming**: Clear onboarding for first-time users
- ✅ **Helpful**: Comprehensive help documentation
- ✅ **Demonstrable**: Example project shows features
- ✅ **Forgiving**: Friendly error messages guide recovery
- ✅ **Guiding**: Quick start tips for exploration

Students can:
1. **Start immediately** (Creation Wizard)
2. **Learn by example** (Demo novel)
3. **Get help when stuck** (Help panel)
4. **Understand errors** (Friendly messages)
5. **Explore confidently** (Quick start tips)

This transforms Writers Factory from a **tool** into a **teaching platform**.

---

**Document Created**: November 14, 2025
**Sprint**: 8 of 8 (FINAL!)
**Estimated Effort**: 2-3 days
**Status**: Ready to start
**Priority**: HIGH for January course
