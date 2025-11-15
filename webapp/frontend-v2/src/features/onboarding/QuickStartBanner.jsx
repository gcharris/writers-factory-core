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
