import { useEffect, useRef } from 'react';
import { quickChips } from '../../utils/mockData.js';

function renderText(text) {
  // Minimal markdown: **bold**, line breaks
  return text
    .split('\n')
    .map((line, i) => {
      const parts = line.split(/\*\*(.*?)\*\*/g);
      return (
        <span key={i}>
          {parts.map((part, j) =>
            j % 2 === 1 ? <strong key={j}>{part}</strong> : part
          )}
          {i < text.split('\n').length - 1 && <br />}
        </span>
      );
    });
}

export function ChatWindow({ messages, input, setInput, isLoading, sendMessage, sendQuick }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col h-[520px]">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100 flex-shrink-0">
        <h2 className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          AI assistant
        </h2>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 border border-blue-200 px-2 py-0.5 text-xs text-blue-700">
            Customer questions
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 border border-gray-200 px-2 py-0.5 text-xs text-gray-500">
            RM knowledge base
          </span>
        </div>
      </div>

      {/* Quick chips */}
      <div className="flex gap-1.5 flex-wrap px-4 py-2 border-b border-gray-100 flex-shrink-0">
        {quickChips.map((chip) => (
          <button
            key={chip.label}
            onClick={() => sendQuick(chip.prompt)}
            className="rounded-full border border-gray-200 bg-gray-50 px-2.5 py-1 text-xs text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
          >
            {chip.label}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
          >
            <p className="text-xs text-gray-400 mb-1">
              {msg.role === 'user' ? 'Sara' : 'Assistant'}
            </p>
            <div
              className={`max-w-[78%] rounded-xl px-3 py-2 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-50 text-blue-900 rounded-br-sm'
                  : 'bg-gray-100 text-gray-800 border border-gray-200 rounded-bl-sm'
              }`}
            >
              {renderText(msg.text)}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex flex-col items-start">
            <p className="text-xs text-gray-400 mb-1">Assistant</p>
            <div className="rounded-xl bg-gray-100 border border-gray-200 px-3 py-2">
              <span className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce"
                    style={{ animationDelay: `${i * 150}ms` }}
                  />
                ))}
              </span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input row */}
      <div className="flex items-center gap-2 px-4 py-3 border-t border-gray-100 flex-shrink-0">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about a customer or bank process…"
          className="flex-1 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-900 outline-none focus:border-blue-300 focus:ring-1 focus:ring-blue-200 placeholder:text-gray-400"
        />
        <button
          onClick={() => sendMessage()}
          disabled={!input.trim() || isLoading}
          className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 hover:bg-blue-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          Send
        </button>
      </div>
    </div>
  );
}