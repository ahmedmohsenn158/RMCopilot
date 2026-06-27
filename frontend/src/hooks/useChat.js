import { useState } from 'react';
import { api } from '../services/api.js';
import { initialMessages } from '../utils/mockData.js';

export function useChat() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage() {
    const text = input.trim();
    if (!text) return;

    const userMessage = { id: Date.now(), role: 'user', text };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const reply = await api.sendChatMessage(text, messages);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, role: 'assistant', text: reply },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  async function sendQuick(prompt) {
    setInput(prompt);
    setMessages((prev) => [...prev, { id: Date.now(), role: 'user', text: prompt }]);
    setIsLoading(true);

    try {
      const reply = await api.sendChatMessage(prompt, messages);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, role: 'assistant', text: reply },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, input, setInput, isLoading, sendMessage, sendQuick };
}
