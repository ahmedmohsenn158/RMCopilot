import { useState, useEffect } from 'react';
import { Pill } from '../ui/Pill.jsx';
import { api } from '../../services/api.js';

const avatarColor = {
  accent:  'bg-blue-50  text-blue-700',
  success: 'bg-green-50 text-green-700',
  warning: 'bg-amber-50 text-amber-700',
  muted:   'bg-gray-100 text-gray-500',
};

const statusVariant = {
  alert:    'danger',
  active:   'success',
  review:   'warning',
  inactive: 'muted',
};

export function CustomerSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    let cancelled = false;
    api.getCustomers(query).then((data) => {
      if (!cancelled) setResults(data);
    });
    return () => { cancelled = true; };
  }, [query]);

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Customer search
        </h2>
      </div>

      {/* Search input */}
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-gray-100">
        <i className="ti ti-search text-gray-400 text-base flex-shrink-0" aria-hidden="true" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, segment, or account…"
          className="flex-1 text-sm text-gray-900 bg-transparent outline-none placeholder:text-gray-400"
        />
        {query && (
          <button
            onClick={() => setQuery('')}
            className="text-gray-400 hover:text-gray-600"
            aria-label="Clear search"
          >
            <i className="ti ti-x text-sm" aria-hidden="true" />
          </button>
        )}
      </div>

      {/* Results */}
      <ul>
        {results.length === 0 && (
          <li className="px-4 py-6 text-center text-sm text-gray-400">
            No customers match "{query}"
          </li>
        )}
        {results.map((c, idx) => (
          <li
            key={c.id}
            className={`flex items-center gap-3 px-4 py-2.5 cursor-pointer hover:bg-gray-50 transition-colors ${
              idx < results.length - 1 ? 'border-b border-gray-100' : ''
            }`}
          >
            <div
              className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium flex-shrink-0 ${
                avatarColor[c.color] ?? avatarColor.muted
              }`}
            >
              {c.initials}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{c.name}</p>
              <p className="text-xs text-gray-400 truncate">
                {c.segment} · {c.accountNo}
              </p>
            </div>
            <Pill variant={statusVariant[c.status] ?? 'muted'}>
              {c.statusLabel}
            </Pill>
          </li>
        ))}
      </ul>
    </div>
  );
}