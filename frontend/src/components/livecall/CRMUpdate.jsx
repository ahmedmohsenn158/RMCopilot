import { useState } from 'react';
import { api } from '../../services/api.js';

const fieldColor = {
  success: 'text-green-600',
  default: 'text-gray-800',
};

export function CRMUpdate({ fields }) {
  const [status, setStatus] = useState(null); // null | 'pushing' | 'pushed'

  async function handlePush() {
    setStatus('pushing');
    await api.pushToCRM(fields);
    setStatus('pushed');
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Post-call CRM
        </h2>
        {status === 'pushed' && (
          <span className="text-xs text-green-600 font-medium flex items-center gap-1">
            <i className="ti ti-check" aria-hidden="true" /> Pushed
          </span>
        )}
      </div>

      <ul className="divide-y divide-gray-100">
        {fields.map((f) => (
          <li key={f.label} className="flex items-center justify-between px-4 py-2.5 text-xs">
            <span className="text-gray-400">{f.label}</span>
            <span className={fieldColor[f.color] ?? fieldColor.default}>
              {f.value}
            </span>
          </li>
        ))}
      </ul>

      {status !== 'pushed' && (
        <div className="px-4 pb-4 pt-2">
          <button
            onClick={handlePush}
            disabled={status === 'pushing'}
            className="w-full rounded-lg border border-blue-200 bg-blue-50 py-2 text-xs font-medium text-blue-700 hover:bg-blue-100 disabled:opacity-50 transition-colors flex items-center justify-center gap-1.5"
          >
            <i className="ti ti-check text-sm" aria-hidden="true" />
            {status === 'pushing' ? 'Pushing…' : 'Push to CRM'}
          </button>
        </div>
      )}
    </div>
  );
}