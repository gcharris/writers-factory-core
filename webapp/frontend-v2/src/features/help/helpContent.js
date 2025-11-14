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
        answer: "Click the 'Cost' button in the top toolbar to open the Cost Dashboard. It shows total spent, savings from local models, generation counts, and a breakdown by model."
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
