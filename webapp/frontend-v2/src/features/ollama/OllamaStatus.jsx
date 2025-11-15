import { useQuery } from '@tanstack/react-query';

export function OllamaStatus() {
  const { data } = useQuery({
    queryKey: ['ollama-status'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/ollama/status');
      return res.json();
    },
    refetchInterval: 30000, // Check every 30 seconds
    retry: false
  });

  if (!data) {
    return null; // Loading...
  }

  if (!data.available) {
    return (
      <div className="px-4 py-2 bg-yellow-900/20 border-b border-yellow-700/50 text-yellow-200 text-sm">
        ⚠️ Ollama not running - only cloud models available
        {data.message && <span className="ml-2 text-yellow-300/60">({data.message})</span>}
      </div>
    );
  }

  return (
    <div className="px-4 py-2 bg-green-900/20 border-b border-green-700/50 text-green-200 text-sm flex items-center justify-between">
      <span>
        ✅ Ollama running - {data.models?.length || 0} local models available (FREE!)
      </span>
      <span className="text-green-300/60 text-xs">
        {data.models?.map(m => m.name || m).join(', ')}
      </span>
    </div>
  );
}
