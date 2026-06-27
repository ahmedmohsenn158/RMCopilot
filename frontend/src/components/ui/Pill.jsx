const variantClasses = {
  danger:  'bg-red-50   text-red-700   border-red-200',
  warning: 'bg-amber-50 text-amber-700 border-amber-200',
  success: 'bg-green-50 text-green-700 border-green-200',
  accent:  'bg-blue-50  text-blue-700  border-blue-200',
  muted:   'bg-gray-100 text-gray-500  border-gray-200',
  pro:     'bg-purple-50 text-purple-700 border-purple-200',
};

export function Pill({ variant = 'muted', children, className = '' }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${variantClasses[variant] ?? variantClasses.muted} ${className}`}
    >
      {children}
    </span>
  );
}