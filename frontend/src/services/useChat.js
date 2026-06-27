import { useState, useCallback } from 'react';
import { api } from '../services/api.js';
import { initialMessages } from '../utils/mockData.js';

export function useChat() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(
    async (text) => {
      const messageText = text ?? input;
      if (!messageText.trim() || isLoading) return;

      const userMsg = {
        id: Date.now(),
        role: 'user',
        text: messageText.trim(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setInput('');
      setIsLoading(true);

      try {
        const response = await api.sendChatMessage(messageText, messages);
        const assistantMsg = {
          id: Date.now() + 1,
          role: 'assistant',
          text: response,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } catch (err) {
        const errMsg = {
          id: Date.now() + 1,
          role: 'assistant',
          text: 'Something went wrong. Please try again.',
        };
        setMessages((prev) => [...prev, errMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [input, isLoading, messages]
  );

  const sendQuick = useCallback(
    (prompt) => {
      sendMessage(prompt);
    },
    [sendMessage]
  );

  return { messages, input, setInput, isLoading, sendMessage, sendQuick };
}