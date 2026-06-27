import { useEffect, useState } from 'react';
import { StatsRow } from '../components/dashboard/StatsRow.jsx';
import { MeetingsList } from '../components/dashboard/MeetingsLists.jsx';
import { CustomerSearch } from '../components/dashboard/CustomerSearch.jsx';
import { api } from '../services/api.js';
import { stats } from '../utils/mockData.js';

export default function DashboardPage() {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    api.getMeetings().then(setMeetings);
  }, []);

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Page header */}
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-900">Good morning, Sara</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Saturday, 27 June 2026 · Here's your day at a glance
        </p>
      </div>

      {/* Stats */}
      <div className="mb-6">
        <StatsRow stats={stats} />
      </div>

      {/* Meetings + Search side by side */}
      <div className="grid grid-cols-2 gap-6">
        <MeetingsList meetings={meetings} />
        <CustomerSearch />
      </div>
    </div>
  );
}