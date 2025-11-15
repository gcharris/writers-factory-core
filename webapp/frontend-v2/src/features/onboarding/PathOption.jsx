import { Check } from 'lucide-react';

export function PathOption({
  icon,
  title,
  description,
  details,
  badge,
  recommended = false,
  selected = false,
  onClick
}) {
  return (
    <button
      onClick={onClick}
      className={`
        w-full p-6 rounded-lg text-left transition-all transform
        ${selected
          ? 'bg-blue-600/20 border-2 border-blue-500 scale-[1.02]'
          : 'bg-gray-700/50 border-2 border-gray-600 hover:border-blue-500/50 hover:bg-gray-700'
        }
      `}
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className={`
          flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center
          ${selected ? 'bg-blue-600' : 'bg-gray-600'}
        `}>
          {icon}
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h4 className="font-semibold text-lg">{title}</h4>

            {/* Badge */}
            {badge && (
              <span className="px-2 py-1 text-xs font-semibold bg-blue-600 text-white rounded">
                {badge}
              </span>
            )}

            {/* Selected Checkmark */}
            {selected && (
              <Check className="w-5 h-5 text-blue-400 ml-auto" />
            )}
          </div>

          <p className="text-gray-400 text-sm mb-3">{description}</p>

          {/* Details List */}
          {details && details.length > 0 && (
            <ul className="space-y-1">
              {details.map((detail, idx) => (
                <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span>{detail}</span>
                </li>
              ))}
            </ul>
          )}

          {/* Recommended Star */}
          {recommended && (
            <div className="mt-3 text-yellow-400 text-sm font-medium">
              ⭐ Recommended for best results
            </div>
          )}
        </div>
      </div>
    </button>
  );
}
