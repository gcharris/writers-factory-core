import { useState } from 'react';
import {
  BookOpen,
  Users,
  Globe,
  BookText,
  PenTool,
  Search,
  CheckCircle,
  Download,
  ArrowLeft,
  ExternalLink
} from 'lucide-react';

export function NotebookLMGuide({ onBack, onReadyNow, onContinueWithout }) {
  const [completedSteps, setCompletedSteps] = useState([]);

  const toggleStep = (stepNum) => {
    if (completedSteps.includes(stepNum)) {
      setCompletedSteps(completedSteps.filter(s => s !== stepNum));
    } else {
      setCompletedSteps([...completedSteps, stepNum]);
    }
  };

  const downloadGuide = () => {
    const guideText = `
# NotebookLM Setup Guide for Writers Factory

## Step 1: Create Your Free NotebookLM Account
1. Go to https://notebooklm.google.com
2. Sign in with your Google account (it's free!)
3. No credit card required

## Step 2: Create a New Notebook for Your Novel
1. Click "Create new notebook"
2. Name it after your novel (e.g., "My Sci-Fi Novel Ideas")
3. This will be your central collection point

## Step 3: Start Adding Content

### Suggested Categories:

**📝 Character Ideas**
- Character profiles and traits
- Backstories and motivations
- Character arcs and development
- Internal conflicts

**🌍 World & Setting Notes**
- Location descriptions
- Time period details
- World-building rules
- Historical/cultural research

**📖 Story Ideas & Plot Threads**
- Main conflict and stakes
- Key scenes you envision
- Plot twists and revelations
- Thematic elements

**✍️ Writing Samples**
- Your own writing samples (for voice analysis)
- Narrative style examples
- Dialogue snippets

**🔍 Research & Inspiration**
- Articles related to your theme
- Character inspirations
- Genre examples
- Visual mood boards

## Step 4: Let It Grow Naturally
Don't rush! Spend 2-7 days collecting:
- Random thoughts
- Shower ideas
- Character revelations
- Plot connections
- Research findings

NotebookLM helps you:
- Ask questions about your ideas
- Find connections you missed
- Organize thoughts naturally

## Step 5: Return to Writers Factory When Ready
Once you have 10+ notes in your NotebookLM:
1. Open Writers Factory
2. Choose "Prepared Writer" path
3. Paste your NotebookLM URL
4. Let AI extract and organize everything!

---

**Bookmark this guide and return when ready!**
    `;

    const blob = new Blob([guideText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'notebooklm-setup-guide.md';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleReadyNow = () => {
    if (onReadyNow) onReadyNow();
  };

  const handleContinueWithout = () => {
    if (onContinueWithout) onContinueWithout();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-400 hover:text-gray-200 mb-4"
          >
            <ArrowLeft size={20} />
            <span>Back</span>
          </button>

          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
              <BookOpen className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">NotebookLM Setup Guide</h1>
              <p className="text-gray-400">Prepare your ideas for the AI Wizard</p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-12 space-y-8">
        {/* Introduction */}
        <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg p-6 border border-blue-500/50">
          <h2 className="text-2xl font-bold mb-4">Why NotebookLM?</h2>
          <p className="text-gray-300 leading-relaxed">
            NotebookLM is a free tool from Google that helps you collect and organize your story ideas
            before you start writing. When you're ready, the Writers Factory AI Wizard will automatically
            extract and structure everything from your notebook, saving you hours of manual work!
          </p>
        </div>

        {/* Step 1 */}
        <StepCard
          number={1}
          title="Create Your Free NotebookLM Account"
          icon={<BookOpen />}
          completed={completedSteps.includes(1)}
          onToggle={() => toggleStep(1)}
        >
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>Go to <a href="https://notebooklm.google.com" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline inline-flex items-center gap-1">
              notebooklm.google.com <ExternalLink size={14} />
            </a></li>
            <li>Sign in with your Google account (it's free!)</li>
            <li>No credit card required</li>
          </ol>
        </StepCard>

        {/* Step 2 */}
        <StepCard
          number={2}
          title="Create a New Notebook for Your Novel"
          icon={<BookText />}
          completed={completedSteps.includes(2)}
          onToggle={() => toggleStep(2)}
        >
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>Click "Create new notebook"</li>
            <li>Name it after your novel (e.g., "My Sci-Fi Novel Ideas")</li>
            <li>This will be your central collection point for all story-related thoughts</li>
          </ol>
        </StepCard>

        {/* Step 3 */}
        <StepCard
          number={3}
          title="Start Adding Content"
          icon={<PenTool />}
          completed={completedSteps.includes(3)}
          onToggle={() => toggleStep(3)}
        >
          <p className="text-gray-300 mb-4">
            Add notes in these suggested categories (NotebookLM is flexible - organize however feels natural):
          </p>

          <div className="space-y-4">
            <CategoryCard
              icon={<Users size={20} />}
              title="📝 Character Ideas"
              examples={[
                "Character profiles and traits",
                "Backstories and motivations",
                "Character arcs and development",
                "Internal conflicts and fears"
              ]}
            />

            <CategoryCard
              icon={<Globe size={20} />}
              title="🌍 World & Setting Notes"
              examples={[
                "Location descriptions",
                "Time period details",
                "World-building rules and logic",
                "Historical or cultural research"
              ]}
            />

            <CategoryCard
              icon={<BookText size={20} />}
              title="📖 Story Ideas & Plot Threads"
              examples={[
                "Main conflict and stakes",
                "Key scenes you envision",
                "Plot twists and revelations",
                "Thematic elements and symbolism"
              ]}
            />

            <CategoryCard
              icon={<PenTool size={20} />}
              title="✍️ Writing Samples"
              examples={[
                "Your own writing samples (for voice analysis)",
                "Narrative style examples",
                "Dialogue snippets",
                "Scene experiments"
              ]}
            />

            <CategoryCard
              icon={<Search size={20} />}
              title="🔍 Research & Inspiration"
              examples={[
                "Articles related to your theme",
                "Character inspirations",
                "Genre examples and comparisons",
                "Visual mood boards or descriptions"
              ]}
            />
          </div>
        </StepCard>

        {/* Step 4 */}
        <StepCard
          number={4}
          title="Let It Grow Naturally (2-7 Days)"
          icon={<Search />}
          completed={completedSteps.includes(4)}
          onToggle={() => toggleStep(4)}
        >
          <div className="space-y-4">
            <p className="text-gray-300">
              <strong className="text-white">Don't rush!</strong> The best results come from spending
              a few days collecting your thoughts naturally:
            </p>

            <ul className="space-y-2 text-gray-300">
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>Random thoughts that pop up during the day</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>Shower ideas and late-night revelations</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>Character discoveries and "what if" moments</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>Plot connections you didn't see before</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>Research findings and inspirations</span>
              </li>
            </ul>

            <div className="bg-gray-700/30 rounded-lg p-4 border border-gray-600">
              <p className="text-gray-300 text-sm">
                <strong className="text-white">NotebookLM helps you:</strong> Ask questions about
                your ideas, find connections you missed, and organize thoughts naturally through conversation
                with AI.
              </p>
            </div>
          </div>
        </StepCard>

        {/* Step 5 */}
        <StepCard
          number={5}
          title="Return to Writers Factory When Ready"
          icon={<CheckCircle />}
          completed={completedSteps.includes(5)}
          onToggle={() => toggleStep(5)}
        >
          <div className="space-y-4">
            <p className="text-gray-300">
              <strong className="text-white">Once you have 10+ notes</strong> in your NotebookLM
              (usually after 2-7 days of collecting), you're ready!
            </p>

            <ol className="list-decimal list-inside space-y-2 text-gray-300">
              <li>Open Writers Factory</li>
              <li>Choose "Prepared Writer" path</li>
              <li>Paste your NotebookLM URL</li>
              <li>Let the AI Wizard extract and organize everything automatically!</li>
            </ol>

            <div className="bg-green-900/30 rounded-lg p-4 border border-green-500/50">
              <p className="text-green-200 text-sm">
                <strong className="text-green-100">The AI Wizard will:</strong> Intelligently extract
                characters, locations, plot threads, themes, and more from your notebook. It validates
                findings with you and creates a structured reference library automatically!
              </p>
            </div>
          </div>
        </StepCard>

        {/* Action Buttons */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 space-y-4">
          <h3 className="text-xl font-bold mb-4">What's Next?</h3>

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={downloadGuide}
              className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-all flex items-center justify-center gap-2"
            >
              <Download size={20} />
              Save This Guide
            </button>

            <button
              onClick={handleReadyNow}
              className="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition-all"
            >
              I'm Ready Now
            </button>
          </div>

          <button
            onClick={handleContinueWithout}
            className="w-full px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all text-sm"
          >
            Continue Without NotebookLM
          </button>

          <p className="text-gray-400 text-sm text-center">
            You can bookmark this page and return when your notebook is ready!
          </p>
        </div>
      </div>
    </div>
  );
}

function StepCard({ number, title, icon, completed, onToggle, children }) {
  return (
    <div className={`
      bg-gray-800 rounded-lg border transition-all
      ${completed ? 'border-green-500' : 'border-gray-700'}
    `}>
      <div
        className="p-6 flex items-start gap-4 cursor-pointer hover:bg-gray-700/50"
        onClick={onToggle}
      >
        <div className={`
          flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl
          ${completed ? 'bg-green-600' : 'bg-blue-600'}
        `}>
          {completed ? <CheckCircle className="w-6 h-6" /> : number}
        </div>

        <div className="flex-1">
          <h3 className="text-xl font-bold mb-2">{title}</h3>
          <div className="text-gray-300">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

function CategoryCard({ icon, title, examples }) {
  return (
    <div className="bg-gray-700/30 rounded-lg p-4 border border-gray-600">
      <div className="flex items-center gap-2 mb-2">
        <div className="text-blue-400">
          {icon}
        </div>
        <h4 className="font-semibold text-white">{title}</h4>
      </div>
      <ul className="space-y-1 ml-7">
        {examples.map((example, idx) => (
          <li key={idx} className="text-sm text-gray-400">
            • {example}
          </li>
        ))}
      </ul>
    </div>
  );
}
