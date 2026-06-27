import { Pill } from '../ui/Pill.jsx';

export function Customer360({ customer }) {
  if (!customer) return null;

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Customer 360
        </h2>
      </div>

      <div className="p-4 space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-50 text-sm font-medium text-blue-700">
            {customer.initials}
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">{customer.name}</p>
            <p className="text-xs text-gray-500">{customer.segment} · {customer.tier}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {customer.stats?.map((stat) => (
            <div key={stat.label} className="rounded-lg border border-gray-200 bg-gray-50 p-3">
              <p className="text-[11px] uppercase tracking-wide text-gray-400">{stat.label}</p>
              <p className="mt-1 text-sm font-medium text-gray-900">{stat.value}</p>
            </div>
          ))}
        </div>

        <div>
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Tags</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {customer.tags?.map((tag) => (
              <Pill key={tag.label} variant={tag.color ?? 'muted'}>
                {tag.label}
              </Pill>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}