// stores/chatStore.ts
import {create} from 'zustand';

interface ChatMessage {
  sender: string;
  message: string;
}

interface ChatState {
  showOverlay: boolean;
  currentMessage: string;
  messageHistory: ChatMessage[];
  toggleOverlay: () => void;
  setCurrentMessage: (message: string) => void;
  sendMessage: () => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  showOverlay: false,
  currentMessage: '',
  messageHistory: [],
  toggleOverlay: () => set(state => ({ showOverlay: !state.showOverlay })),
  setCurrentMessage: (message: string) => set({ currentMessage: message }),
  sendMessage: async () => {
    const { currentMessage, messageHistory } = get();
    if (!currentMessage.trim()) return;

    const userMessage: ChatMessage = { sender: 'user', message: currentMessage };
    const updatedHistory = [...messageHistory, userMessage];
    set({ messageHistory: updatedHistory });

    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userInput: currentMessage }),
      });

      if (response.ok) {
        const { message } = await response.json();
        const aiMessage: ChatMessage = { sender: 'ai', message };
        set({ messageHistory: [...updatedHistory, aiMessage] });
      } else {
        console.error('Failed to fetch response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }

    set({ currentMessage: '' });
  },
}));
