import { CheckCircle, Circle, Loader2 } from 'lucide-react';

export function ProgressSteps({ steps }) {
  return (
    <div className="space-y-1">
      {steps.map((step, idx) => (
        <ProgressStep
          key={idx}
          name={step.name}
          status={step.status}
          number={idx + 1}
        />
      ))}
    </div>
  );
}

function ProgressStep({ name, status, number }) {
  const getStatusIcon = () => {
    switch (status) {
      case 'complete':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'in_progress':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'pending':
      default:
        return <Circle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'complete':
        return 'text-green-400 bg-green-900/20 border-green-500/50';
      case 'in_progress':
        return 'text-blue-400 bg-blue-900/20 border-blue-500/50';
      case 'pending':
      default:
        return 'text-gray-400 bg-gray-800/50 border-gray-700';
    }
  };

  return (
    <div className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${getStatusColor()}`}>
      {getStatusIcon()}
      <div className="flex-1">
        <div className="text-sm font-medium">{name}</div>
      </div>
      <div className="text-xs text-gray-500">{number}/8</div>
    </div>
  );
}
