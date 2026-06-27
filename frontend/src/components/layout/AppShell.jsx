import { NavLink } from 'react-router-dom';
import { currentRM } from '../../utils/mockData.js';

const navItems = [
  { to: '/',          icon: 'ti-layout-dashboard', label: 'Dashboard' },
  { to: '/assistant', icon: 'ti-message-chatbot',  label: 'Assistant'  },
  { to: '/live-call', icon: 'ti-phone-call',        label: 'Live call'  },
];

export function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top bar */}
      <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center">
            <i className="ti ti-building-bank text-white text-sm" aria-hidden="true" />
          </div>
          <span className="font-semibold text-gray-900 text-sm tracking-tight">
            Finaira Copilot
          </span>
        </div>

        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-gray-200 bg-gray-50 px-2.5 py-1 text-xs text-gray-600">
            <i className="ti ti-user text-xs" aria-hidden="true" />
            {currentRM.name} · {currentRM.role}
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-green-50 border border-green-200 px-2.5 py-1 text-xs font-medium text-green-700">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
            Online
          </span>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-52 bg-white border-r border-gray-200 flex flex-col pt-4 flex-shrink-0">
          <nav className="flex flex-col gap-1 px-3">
            {navItems.map(({ to, icon, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 font-medium'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                <i className={`ti ${icon} text-base`} aria-hidden="true" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-auto px-3 pb-4">
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-3">
              <p className="text-xs font-medium text-gray-700 mb-0.5">Today</p>
              <p className="text-xs text-gray-500">3 meetings · 2 alerts</p>
            </div>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}