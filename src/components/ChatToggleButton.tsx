// components/ChatToggleButton.tsx
'use client'
import { useChatStore } from '../stores/chatStore'; // Adjust the path as necessary
import Button from './ui/button';
// import { ReactComponent as TextIcon } from '../assets/textIcon.svg'; // Adjust the path and method of importing the icon as necessary


function TextIcon() {
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M17 6.1H3" />
        <path d="M21 12.1H3" />
        <path d="M15.1 18H3" />
      </svg>
    );
  }

  
export const ChatToggleButton = () => {
  const { toggleOverlay } = useChatStore();

  return (
    <div className="absolute bottom-5 right-5" onClick={toggleOverlay}>
    <script src="https://cdn.lordicon.com/lordicon.js"></script>
      <Button>
      <lord-icon
            src="https://cdn.lordicon.com/lbjtvqiv.json"
            trigger="hover">
        </lord-icon>
      </Button>
    </div>
  );
};
