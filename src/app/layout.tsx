import './globals.css'
import { Header } from "@/components/header"
import { ChatOverlay } from '../components/ChatOverlay';
import { ChatToggleButton } from '@/components/ChatToggleButton';
import Script from "next/script";



export default function RootLayout({
    children,
  }: {
    children: React.ReactNode
    }) {
      return (
        <html lang="en">
          <body className='dark:bg-white'>
          <Script src="https://cdn.lordicon.com/lordicon.js"></Script>
            <div>
            <Header/>
            <ChatOverlay />
            <ChatToggleButton />
            {children}
            </div>
          </body>
        </html>
      )
    }
