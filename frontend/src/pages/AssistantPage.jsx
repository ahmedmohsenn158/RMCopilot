import { ChatWindow } from '../components/assistant/ChatWindow.jsx';
import { useChat } from '../hooks/useChat.js';

export default function AssistantPage() {
  const chat = useChat();

  return (
    <div className="p-6 max-w-3xl mx-auto">
      {/* Page header */}
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-900">AI assistant</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Ask about your customers, bank processes, or product details — I'm here throughout your day.
        </p>
      </div>

      <ChatWindow
        messages={chat.messages}
        input={chat.input}
        setInput={chat.setInput}
        isLoading={chat.isLoading}
        sendMessage={chat.sendMessage}
        sendQuick={chat.sendQuick}
      />

      {/* Onboarding tip for junior RMs */}
      <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 flex gap-3">
        <i className="ti ti-bulb text-amber-600 text-base flex-shrink-0 mt-0.5" aria-hidden="true" />
        <div>
          <p className="text-xs font-medium text-amber-800 mb-0.5">New to RM?</p>
          <p className="text-xs text-amber-700 leading-relaxed">
            Ask me anything — from product eligibility rules to how to handle a difficult call. I know the full policy handbook and every product on offer.
          </p>
        </div>
      </div>
    </div>
  );
}