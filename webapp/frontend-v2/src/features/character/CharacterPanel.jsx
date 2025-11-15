import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle2, Lightbulb, Users } from 'lucide-react';
import { toast } from 'sonner';

export function CharacterPanel() {
  const [selectedCharacterId, setSelectedCharacterId] = useState(null);

  // Fetch character list
  const { data: charactersData } = useQuery({
    queryKey: ['characters'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/manuscript/explants-v1/characters');
      if (!res.ok) throw new Error('Failed to fetch characters');
      return res.json();
    }
  });

  const characters = charactersData?.characters || [];

  // Analyze character
  const { data: analysis, isLoading: analyzing } = useQuery({
    queryKey: ['character-analysis', selectedCharacterId],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/character/${selectedCharacterId}/analyze`, {
        method: 'POST'
      });
      if (!res.ok) throw new Error('Analysis failed');
      return res.json();
    },
    enabled: !!selectedCharacterId
  });

  const selectedCharacter = characters.find(c => c.id === selectedCharacterId);

  return (
    <div className="h-full flex flex-col bg-gray-800">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold mb-3 flex items-center gap-2">
          <Users size={20} />
          Character Development
        </h3>

        {/* Character Selector */}
        <select
          value={selectedCharacterId || ''}
          onChange={(e) => setSelectedCharacterId(e.target.value)}
          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:border-blue-500"
        >
          <option value="">Select a character...</option>
          {characters.map(char => (
            <option key={char.id} value={char.id}>
              {char.name} ({char.role})
            </option>
          ))}
        </select>
      </div>

      {/* Analysis Results */}
      {selectedCharacter && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Depth Score */}
          <div className="p-4 bg-gray-700 rounded-lg">
            <div className="text-sm text-gray-400 mb-2">Dimensional Depth</div>
            <div className="flex items-end gap-3">
              <div className="text-4xl font-bold">
                {analysis?.depth_score || 0}
              </div>
              <div className="text-gray-400 mb-1">/100</div>
            </div>
            <div className="mt-2 h-2 bg-gray-600 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${
                  (analysis?.depth_score || 0) < 50 ? 'bg-red-500' :
                  (analysis?.depth_score || 0) < 80 ? 'bg-yellow-500' :
                  'bg-green-500'
                }`}
                style={{ width: `${analysis?.depth_score || 0}%` }}
              />
            </div>
            <div className="text-xs text-gray-400 mt-2">
              {(analysis?.depth_score || 0) < 50 ? '⚠️ Flat character - needs contradictions' :
               (analysis?.depth_score || 0) < 80 ? '🔶 Developing - add more complexity' :
               '✅ Dimensional - well-developed'}
            </div>
          </div>

          {/* Flags */}
          {analyzing && (
            <div className="text-center text-gray-400 py-8">
              Analyzing character depth...
            </div>
          )}

          {analysis?.flags && analysis.flags.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-semibold text-sm flex items-center gap-2">
                <AlertTriangle size={16} />
                Issues Detected
              </h4>
              {analysis.flags.map((flag, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg border-l-4 ${
                    flag.severity === 'CRITICAL' ? 'bg-red-900/20 border-red-500' :
                    flag.severity === 'HIGH' ? 'bg-orange-900/20 border-orange-500' :
                    'bg-yellow-900/20 border-yellow-500'
                  }`}
                >
                  <div className="flex items-start gap-2 mb-2">
                    <AlertTriangle size={16} className="mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="font-semibold text-sm mb-1">{flag.message}</div>
                      {flag.example && (
                        <div className="text-xs text-gray-400 mt-2 italic">
                          <strong>Example:</strong> {flag.example}
                        </div>
                      )}
                      {flag.recommendation && (
                        <div className="text-xs text-blue-300 mt-2 flex items-start gap-1">
                          <Lightbulb size={14} className="mt-0.5 flex-shrink-0" />
                          <span>{flag.recommendation}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Recommendations (Strengths) */}
          {analysis?.recommendations && analysis.recommendations.length > 0 && (
            <div className="space-y-2">
              <h4 className="font-semibold text-sm flex items-center gap-2 text-green-400">
                <CheckCircle2 size={16} />
                Strengths
              </h4>
              {analysis.recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-green-900/20 border-l-4 border-green-500 rounded text-sm"
                >
                  <div className="flex items-start gap-2">
                    <CheckCircle2 size={14} className="mt-0.5 flex-shrink-0 text-green-400" />
                    <span className="text-green-200">{rec.message}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {analysis?.flags && analysis.flags.length === 0 && !analyzing && (
            <div className="p-4 bg-green-900/20 border border-green-700/50 rounded-lg flex items-center gap-2">
              <CheckCircle2 size={20} className="text-green-400" />
              <span className="text-green-300">No issues detected - character is well-developed!</span>
            </div>
          )}

          {/* Contradiction Workshop */}
          <div className="p-4 bg-blue-900/20 border border-blue-700/50 rounded-lg">
            <h4 className="font-semibold text-sm mb-2 flex items-center gap-2">
              <Lightbulb size={16} />
              Contradiction Workshop
            </h4>
            <p className="text-xs text-gray-400 mb-3">
              Professional characters are built on contradictions. Add opposing traits to create dimensional depth.
            </p>
            <button
              onClick={() => toast.info('Contradiction generator coming soon!')}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors"
            >
              Generate Contradiction Ideas
            </button>
          </div>

          {/* Character Details (collapsible) */}
          <div className="p-4 bg-gray-700/50 rounded-lg">
            <h4 className="font-semibold text-sm mb-3">Character Details</h4>
            <div className="space-y-2 text-xs">
              {selectedCharacter.core_traits && selectedCharacter.core_traits.length > 0 && (
                <div>
                  <span className="text-gray-400">Core Traits:</span>
                  <span className="ml-2">{selectedCharacter.core_traits.join(', ')}</span>
                </div>
              )}
              {selectedCharacter.observable_traits && selectedCharacter.observable_traits.length > 0 && (
                <div>
                  <span className="text-gray-400">Observable Traits:</span>
                  <span className="ml-2">{selectedCharacter.observable_traits.join(', ')}</span>
                </div>
              )}
              {selectedCharacter.fatal_flaw && (
                <div>
                  <span className="text-gray-400">Fatal Flaw:</span>
                  <span className="ml-2">{selectedCharacter.fatal_flaw}</span>
                </div>
              )}
              {selectedCharacter.mistaken_belief && (
                <div>
                  <span className="text-gray-400">Mistaken Belief:</span>
                  <span className="ml-2">{selectedCharacter.mistaken_belief}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {!selectedCharacter && (
        <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
          Select a character to analyze dimensional depth
        </div>
      )}
    </div>
  );
}
