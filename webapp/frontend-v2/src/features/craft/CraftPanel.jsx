import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Wand2, Loader2, CheckCircle, AlertCircle, Copy, Download } from 'lucide-react';
import { toast } from 'sonner';

export function CraftPanel({ projectId = "explants-v1" }) {
  const [selectedSkill, setSelectedSkill] = useState('scene-analyzer');
  const [sceneContent, setSceneContent] = useState('');
  const [mode, setMode] = useState('detailed');
  const [phase, setPhase] = useState('phase2');

  // Get available skills
  const { data: skillsData, isLoading: loadingSkills } = useQuery({
    queryKey: ['skills'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/skills/list');
      return res.json();
    }
  });

  // Execute skill mutation
  const executeMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch('http://localhost:8000/api/skills/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skill_name: selectedSkill,
          input_data: buildInputData(),
          context: { project_id: projectId },
          allow_fallback: true
        })
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Skill execution failed');
      }
      return res.json();
    },
    onSuccess: (data) => {
      toast.success(`${selectedSkill} executed successfully`);
    },
    onError: (error) => {
      toast.error(`Execution failed: ${error.message}`);
    }
  });

  const buildInputData = () => {
    const baseInput = {
      scene_content: sceneContent
    };

    if (selectedSkill === 'scene-analyzer') {
      return {
        ...baseInput,
        mode,
        phase
      };
    }

    if (selectedSkill === 'scene-enhancer') {
      return {
        ...baseInput,
        enhancement_level: 'standard',
        preserve_structure: true
      };
    }

    return baseInput;
  };

  const handleExecute = () => {
    if (!sceneContent.trim()) {
      toast.error('Please enter scene content');
      return;
    }
    executeMutation.mutate();
  };

  const copyResults = () => {
    if (executeMutation.data?.data) {
      const text = JSON.stringify(executeMutation.data.data, null, 2);
      navigator.clipboard.writeText(text);
      toast.success('Results copied to clipboard');
    }
  };

  const downloadResults = () => {
    if (executeMutation.data?.data) {
      const text = JSON.stringify(executeMutation.data, null, 2);
      const blob = new Blob([text], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedSkill}-results.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success('Results downloaded');
    }
  };

  const skills = skillsData?.skills || [];

  return (
    <div className="h-full flex flex-col bg-gray-900">
      {/* Header */}
      <div className="p-4 border-b border-gray-700 bg-gray-800">
        <h2 className="font-semibold text-gray-100 flex items-center">
          <Wand2 size={18} className="mr-2" />
          Craft Tools
        </h2>
        <p className="text-xs text-gray-400 mt-1">
          Explants writing craft analysis and enhancement
        </p>
      </div>

      {/* Skill Selector */}
      <div className="p-4 border-b border-gray-700 bg-gray-800">
        <label className="block text-sm font-medium mb-2 text-gray-300">
          Select Skill:
        </label>
        {loadingSkills ? (
          <div className="text-sm text-gray-400">Loading skills...</div>
        ) : (
          <select
            value={selectedSkill}
            onChange={(e) => setSelectedSkill(e.target.value)}
            className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {skills.map(skill => (
              <option key={skill.skill_id} value={skill.skill_id}>
                {skill.name} ({skill.available ? 'Available' : 'Unavailable'})
              </option>
            ))}
          </select>
        )}

        {/* Skill description */}
        {skills.length > 0 && (
          <div className="mt-2 text-xs text-gray-400">
            {skills.find(s => s.skill_id === selectedSkill)?.description}
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {/* Scene Content Input */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">
              Scene Content:
            </label>
            <textarea
              value={sceneContent}
              onChange={(e) => setSceneContent(e.target.value)}
              placeholder="Paste scene content here..."
              className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-500 font-mono text-sm"
              rows={12}
            />
            <div className="text-xs text-gray-500 mt-1">
              {sceneContent.split(/\s+/).filter(Boolean).length} words
            </div>
          </div>

          {/* Skill-specific options */}
          {selectedSkill === 'scene-analyzer' && (
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Analysis Mode:
                </label>
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="detailed">Detailed Analysis</option>
                  <option value="quick">Quick Audit</option>
                  <option value="variant_comparison">Compare Variants</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Phase:
                </label>
                <select
                  value={phase}
                  onChange={(e) => setPhase(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-100 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="phase1">Phase 1 (Simple Voice)</option>
                  <option value="phase2">Phase 2 (Complex Voice)</option>
                  <option value="phase3">Phase 3 (Advanced)</option>
                </select>
              </div>
            </div>
          )}

          {/* Execute Button */}
          <button
            onClick={handleExecute}
            disabled={executeMutation.isPending || !sceneContent.trim()}
            className="w-full px-4 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium"
          >
            {executeMutation.isPending ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Wand2 size={18} />
                Execute Skill
              </>
            )}
          </button>

          {/* Results Display */}
          {executeMutation.data && (
            <div className="mt-6 space-y-4">
              {/* Metadata */}
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-semibold text-gray-300">Execution Info</h3>
                  <div className="flex gap-2">
                    <button
                      onClick={copyResults}
                      className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded hover:bg-gray-600 flex items-center gap-1"
                    >
                      <Copy size={12} />
                      Copy
                    </button>
                    <button
                      onClick={downloadResults}
                      className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded hover:bg-gray-600 flex items-center gap-1"
                    >
                      <Download size={12} />
                      Download
                    </button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="text-gray-400">
                    Status: <span className="text-gray-200">{executeMutation.data.status}</span>
                  </div>
                  <div className="text-gray-400">
                    Provider: <span className="text-gray-200">{executeMutation.data.metadata?.provider}</span>
                  </div>
                  <div className="text-gray-400">
                    Execution Time: <span className="text-gray-200">{executeMutation.data.metadata?.execution_time_ms}ms</span>
                  </div>
                  {executeMutation.data.metadata?.cost_estimate > 0 && (
                    <div className="text-gray-400">
                      Cost: <span className="text-gray-200">${executeMutation.data.metadata.cost_estimate.toFixed(4)}</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Skill-specific results */}
              {selectedSkill === 'scene-analyzer' && executeMutation.data.data && (
                <AnalyzerResults data={executeMutation.data.data} />
              )}

              {selectedSkill === 'scene-enhancer' && executeMutation.data.data && (
                <EnhancerResults data={executeMutation.data.data} />
              )}

              {/* Generic results for other skills */}
              {!['scene-analyzer', 'scene-enhancer'].includes(selectedSkill) && (
                <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                  <h3 className="text-sm font-semibold text-gray-300 mb-3">Results</h3>
                  <pre className="text-xs text-gray-300 overflow-auto">
                    {JSON.stringify(executeMutation.data.data, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* Error Display */}
          {executeMutation.isError && (
            <div className="bg-red-900/20 border border-red-700 rounded-lg p-4 flex items-start gap-2">
              <AlertCircle size={18} className="text-red-500 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-red-300">
                {executeMutation.error?.message || 'An error occurred'}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Scene Analyzer Results Component
function AnalyzerResults({ data }) {
  const getQualityColor = (tier) => {
    if (tier?.includes('Gold')) return 'text-yellow-400';
    if (tier?.includes('A+')) return 'text-green-400';
    if (tier?.includes('A')) return 'text-green-500';
    if (tier?.includes('B')) return 'text-blue-400';
    return 'text-gray-400';
  };

  const getPriorityColor = (priority) => {
    if (priority === 'critical') return 'text-red-400';
    if (priority === 'high') return 'text-orange-400';
    if (priority === 'medium') return 'text-yellow-400';
    return 'text-gray-400';
  };

  return (
    <div className="space-y-4">
      {/* Score Summary */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-bold text-gray-100">
              {data.total_score}/100
            </h3>
            <div className={`text-sm font-semibold ${getQualityColor(data.quality_tier)}`}>
              {data.quality_tier}
            </div>
          </div>
          <CheckCircle size={32} className="text-green-500" />
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
        <h3 className="text-sm font-semibold text-gray-300 mb-3">Category Breakdown</h3>
        <div className="space-y-3">
          {data.category_scores && Object.entries(data.category_scores).map(([category, score]) => {
            const maxScores = {
              voice_authenticity: 30,
              character_consistency: 20,
              metaphor_discipline: 20,
              anti_pattern_compliance: 15,
              phase_appropriateness: 15
            };
            const max = maxScores[category] || 100;
            const percentage = (score / max) * 100;

            return (
              <div key={category}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400 capitalize">
                    {category.replace(/_/g, ' ')}
                  </span>
                  <span className="text-gray-300">{score}/{max}</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      percentage >= 90 ? 'bg-green-500' :
                      percentage >= 75 ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Fixes */}
      {data.fixes && data.fixes.length > 0 && (
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">
            Recommended Fixes ({data.fixes.length})
          </h3>
          <div className="space-y-3">
            {data.fixes.map((fix, i) => (
              <div key={i} className="border-l-2 border-blue-500 pl-3 py-1">
                <div className="flex items-start gap-2">
                  <span className={`text-xs font-semibold ${getPriorityColor(fix.priority)}`}>
                    [{fix.priority?.toUpperCase() || 'INFO'}]
                  </span>
                  <div className="flex-1">
                    <div className="text-xs font-medium text-gray-300 mb-1">
                      {fix.pattern || fix.issue}
                    </div>
                    {fix.old_string && (
                      <div className="text-xs text-gray-500 mb-1">
                        Found: "{fix.old_string.substring(0, 60)}..."
                      </div>
                    )}
                    <div className="text-xs text-gray-400">
                      {fix.suggested_fix || fix.suggestion}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Scene Enhancer Results Component
function EnhancerResults({ data }) {
  return (
    <div className="space-y-4">
      {/* Enhanced Scene */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
        <h3 className="text-sm font-semibold text-gray-300 mb-3">Enhanced Scene</h3>
        <div className="text-sm text-gray-200 whitespace-pre-wrap font-mono bg-gray-900 p-3 rounded border border-gray-600 max-h-96 overflow-y-auto">
          {data.enhanced_scene || data.message}
        </div>
      </div>

      {/* Changes Made */}
      {data.changes_made && data.changes_made.length > 0 && (
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">
            Changes Made ({data.changes_made.length})
          </h3>
          <ul className="space-y-2">
            {data.changes_made.map((change, i) => (
              <li key={i} className="text-xs text-gray-400 flex items-start gap-2">
                <span className="text-green-500">•</span>
                {change}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvement Score */}
      {data.improvement_score !== undefined && (
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">Quality Improvement:</span>
            <span className="text-lg font-bold text-green-400">
              +{data.improvement_score} points
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
