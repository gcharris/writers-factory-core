import { useQuery } from '@tanstack/react-query';
import { X } from 'lucide-react';

export function CostDashboard({ onClose }) {
  const { data, isLoading } = useQuery({
    queryKey: ['session-cost'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/session/cost');
      return res.json();
    },
    refetchInterval: 5000 // Refresh every 5 seconds
  });

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4">
          <div className="text-center text-gray-400">Loading cost data...</div>
        </div>
      </div>
    );
  }

  const totalCost = data?.total_cost || 0;
  const savings = data?.savings || 0;
  const localGens = data?.local_generations || 0;
  const cloudGens = data?.cloud_generations || 0;
  const modelBreakdown = data?.by_model || [];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold">Cost Dashboard</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-700 rounded"
          >
            <X size={20} />
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-700 rounded p-4">
            <div className="text-sm text-gray-400 mb-1">Total Spent</div>
            <div className="text-2xl font-bold text-red-400">
              ${totalCost.toFixed(2)}
            </div>
          </div>

          <div className="bg-gray-700 rounded p-4">
            <div className="text-sm text-gray-400 mb-1">Savings (Local)</div>
            <div className="text-2xl font-bold text-green-400">
              ${savings.toFixed(2)}
            </div>
          </div>

          <div className="bg-gray-700 rounded p-4">
            <div className="text-sm text-gray-400 mb-1">Generations</div>
            <div className="text-2xl font-bold text-blue-400">
              {localGens + cloudGens}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {localGens} local / {cloudGens} cloud
            </div>
          </div>
        </div>

        {/* Model Breakdown */}
        {modelBreakdown.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-400 mb-3">Breakdown by Model</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {modelBreakdown.map((item, idx) => (
                <div
                  key={idx}
                  className="bg-gray-700 rounded p-3 flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium">
                      {item.is_local ? '🦙' : '☁️'} {item.model}
                    </span>
                    {item.is_local && (
                      <span className="text-xs bg-green-900/50 text-green-300 px-2 py-0.5 rounded">
                        FREE
                      </span>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold">
                      ${(item.cost || 0).toFixed(4)}
                    </div>
                    <div className="text-xs text-gray-400">
                      {item.count || 1} {item.count === 1 ? 'generation' : 'generations'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {modelBreakdown.length === 0 && (
          <div className="text-center text-gray-400 py-8">
            No generations yet. Start using AI tools to see cost tracking!
          </div>
        )}

        {/* Tips */}
        <div className="mt-6 p-4 bg-blue-900/20 border border-blue-700/50 rounded">
          <div className="text-sm text-blue-200">
            💡 <strong>Tip:</strong> Enable Economy Mode to prefer local models and maximize savings!
          </div>
        </div>
      </div>
    </div>
  );
}
