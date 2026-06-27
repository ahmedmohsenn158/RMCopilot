import { Pill } from '../ui/Pill.jsx';

const alertStyle = {
  danger:  {
    border: 'border-l-red-400',
    title:  'text-red-700',
    body:   'text-red-600',
    pill:   'danger',
    icon:   'ti-alert-triangle',
  },
  warning: {
    border: 'border-l-amber-400',
    title:  'text-amber-700',
    body:   'text-amber-600',
    pill:   'warning',
    icon:   'ti-clock',
  },
  info:    {
    border: 'border-l-blue-400',
    title:  'text-blue-700',
    body:   'text-blue-600',
    pill:   'accent',
    icon:   'ti-trending-up',
  },
};

export function AlertPanel({ alerts, onAction }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Live alerts
        </h2>
        <Pill variant="danger">{alerts.length} active</Pill>
      </div>

      <ul className="divide-y divide-gray-100">
        {alerts.map((alert) => {
          const s = alertStyle[alert.type] ?? alertStyle.info;
          return (
            <li
              key={alert.id}
              className={`border-l-[3px] ${s.border} px-4 py-3`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-xs font-medium flex items-center gap-1 ${s.title}`}>
                  <i className={`ti ${s.icon} text-sm`} aria-hidden="true" />
                  {alert.title}
                </span>
                <span className="text-xs text-gray-400">{alert.time}</span>
              </div>
              <p className={`text-xs leading-relaxed mb-2 ${s.body}`}>
                {alert.body}
              </p>
              {alert.actionLabel && (
                <button
                  onClick={() => onAction?.(alert.actionPrompt)}
                  className="w-full rounded-lg border border-blue-200 bg-blue-50 py-1.5 text-xs font-medium text-blue-700 hover:bg-blue-100 transition-colors"
                >
                  {alert.actionLabel}
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}