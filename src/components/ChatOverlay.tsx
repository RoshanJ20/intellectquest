// components/ChatOverlay.tsx
'use client'
import { useChatStore } from '../stores/chatStore'; // Adjust the path as necessary

export const ChatOverlay = () => {
  const { showOverlay, toggleOverlay, currentMessage, setCurrentMessage, messageHistory, sendMessage } = useChatStore();

  if (!showOverlay) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-lg font-bold mb-2">Chat with Us!</h2>
        <div className="overflow-auto h-64 mb-4">
          {messageHistory.map((msg, index) => (
            <div key={index} className={`p-2 ${msg.sender === 'ai' ? 'text-left' : 'text-right'}`}>
              <span className="inline-block bg-gray-200 rounded p-2">{msg.message}</span>
            </div>
          ))}
        </div>
        <div className="flex">
          <input
            type="text"
            className="border p-2 w-full rounded-l"
            placeholder="Type your message..."
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-r">
            Send
          </button>
        </div>
        <button onClick={toggleOverlay} className="mt-4 bg-red-500 text-white p-2 rounded">
          Close Chat
        </button>
      </div>
    </div>
  );
};
