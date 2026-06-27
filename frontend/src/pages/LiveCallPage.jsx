import { useEffect, useState } from 'react';
import { Customer360 } from '../components/livecall/Customer360.jsx';
import { AlertPanel } from '../components/livecall/AlertPanel.jsx';
import { DraftEmail } from '../components/livecall/DraftEmail.jsx';
import { CRMUpdate } from '../components/livecall/CRMUpdate.jsx';
import { api } from '../services/api.js';
import { draftEmail, crmFields } from '../utils/mockData.js';

function useCallTimer(initial = '3:42') {
  const [display] = useState(initial);
  return display;
}

export default function LiveCallPage() {
  const [customer, setCustomer] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const callDuration = useCallTimer();

  useEffect(() => {
    api.getActiveCustomer().then(setCustomer);
    api.getAlerts().then(setAlerts);
  }, []);

  function handleAlertAction(prompt) {
    // In production this would open the assistant with the prompt pre-filled
    console.log('Action triggered:', prompt);
  }

  if (!customer) {
    return (
      <div className="p-6 flex items-center justify-center h-64">
        <p className="text-sm text-gray-400">Loading call view…</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Call header bar */}
      <div className="mb-5 bg-white rounded-xl border border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-blue-50 flex items-center justify-center text-sm font-medium text-blue-700">
            {customer.initials ?? 'KA'}
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-900">{customer.name}</p>
            <p className="text-xs text-gray-500">
              {customer.segment} · {customer.tier} · Joined {customer.joinedYear}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          <span className="text-sm font-medium text-red-600">
            Live · {callDuration}
          </span>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-[1fr_280px] gap-5">
        {/* Left — customer context + draft */}
        <div className="flex flex-col gap-5">
          <Customer360 customer={customer} />
          <DraftEmail draft={draftEmail} />
        </div>

        {/* Right — alerts + CRM */}
        <div className="flex flex-col gap-5">
          <AlertPanel alerts={alerts} onAction={handleAlertAction} />
          <CRMUpdate fields={crmFields} />
        </div>
      </div>
    </div>
  );
}