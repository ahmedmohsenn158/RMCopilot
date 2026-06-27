import { useState } from 'react';
import { Pill } from '../ui/Pill.jsx';
import { api } from '../../services/api.js';

const avatarColor = {
  accent:  'bg-blue-50  text-blue-700',
  success: 'bg-green-50 text-green-700',
  warning: 'bg-amber-50 text-amber-700',
};

export function MeetingsList({ meetings }) {
  const [loading, setLoading] = useState(null);
  const [briefed, setBriefed] = useState(new Set());

  async function handlePrepBrief(meeting) {
    setLoading(meeting.id);
    await api.prepareMeetingBrief(meeting.name, meeting.topic);
    setBriefed((prev) => new Set([...prev, meeting.id]));
    setLoading(null);
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          Upcoming meetings
        </h2>
        <Pill variant="accent">3 today</Pill>
      </div>

      <ul>
        {meetings.map((meeting, idx) => (
          <li
            key={meeting.id}
            className={`flex items-center gap-3 px-4 py-3 ${
              idx < meetings.length - 1 ? 'border-b border-gray-100' : ''
            }`}
          >
            {/* Time */}
            <div className="w-10 flex-shrink-0 text-center">
              <span className="text-sm font-medium text-gray-900 leading-none block">
                {meeting.time.split(' ')[0]}
              </span>
              <span className="text-xs text-gray-400">
                {meeting.time.split(' ')[1]}
              </span>
            </div>

            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium flex-shrink-0 ${
                avatarColor[meeting.color] ?? avatarColor.accent
              }`}
            >
              {meeting.initials}
            </div>

            {/* Info */}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {meeting.name}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {meeting.topic} · {meeting.segment}
              </p>
            </div>

            {/* Action */}
            <button
              onClick={() => handlePrepBrief(meeting)}
              disabled={loading === meeting.id}
              className={`flex-shrink-0 rounded-full border px-2.5 py-1 text-xs font-medium transition-colors ${
                briefed.has(meeting.id)
                  ? 'border-green-200 bg-green-50 text-green-700'
                  : 'border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100'
              }`}
            >
              {loading === meeting.id
                ? 'Loading…'
                : briefed.has(meeting.id)
                ? '✓ Ready'
                : 'Prep brief'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}