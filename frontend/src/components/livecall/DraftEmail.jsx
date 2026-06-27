import { useState } from 'react';
import { api } from '../../services/api.js';

export function DraftEmail({ draft }) {
  const [text, setText] = useState(draft);
  const [editing, setEditing] = useState(false);
  const [status, setStatus] = useState(null); // null | 'sending' | 'sent'

  async function handleSend() {
    setStatus('sending');
    await api.sendEmail(text);
    setStatus('sent');
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          AI-drafted follow-up
        </h2>
        {status === 'sent' && (
          <span className="text-xs text-green-600 font-medium flex items-center gap-1">
            <i className="ti ti-check" aria-hidden="true" /> Sent & logged
          </span>
        )}
      </div>

      <div className="p-4">
        {editing ? (
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={8}
            className="w-full rounded-lg border border-gray-200 bg-gray-50 p-3 text-sm text-gray-800 leading-relaxed outline-none focus:border-blue-300 focus:ring-1 focus:ring-blue-200 resize-none"
          />
        ) : (
          <div className="rounded-lg border border-blue-100 bg-blue-50 p-3 text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
            {text}
          </div>
        )}
      </div>

      {status !== 'sent' && (
        <div className="flex gap-2 px-4 pb-4">
          <button
            onClick={() => setEditing((e) => !e)}
            className="flex-1 rounded-lg border border-gray-200 bg-white py-2 text-xs font-medium text-gray-600 hover:bg-gray-50 transition-colors"
          >
            {editing ? 'Preview' : 'Edit draft'}
          </button>
          <button
            onClick={handleSend}
            disabled={status === 'sending'}
            className="flex-1 rounded-lg border border-blue-200 bg-blue-50 py-2 text-xs font-medium text-blue-700 hover:bg-blue-100 disabled:opacity-50 transition-colors"
          >
            {status === 'sending' ? 'Sending…' : 'Approve & send'}
          </button>
        </div>
      )}
    </div>
  );
}