const colorMap = {
  default: 'text-gray-900',
  warning: 'text-amber-600',
  success: 'text-green-600',
  danger:  'text-red-600',
};

export function StatsRow({ stats }) {
  return (
    <div className="grid grid-cols-4 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="bg-white rounded-xl border border-gray-200 p-4"
        >
          <p className="text-xs text-gray-500 mb-1">{stat.label}</p>
          <p className={`text-2xl font-medium ${colorMap[stat.color] ?? colorMap.default}`}>
            {stat.value}
          </p>
        </div>
      ))}
    </div>
  );
}