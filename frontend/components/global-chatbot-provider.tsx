"use client"
import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { usePathname } from "next/navigation"
import { FloatingChatbot } from "@/components/floating-chatbot"
import { ChatbotHint } from "@/components/chatbot-hint"

interface ChatbotContextType {
  isOpen: boolean
  openChatbot: () => void
  closeChatbot: () => void
  toggleChatbot: () => void
}

const ChatbotContext = createContext<ChatbotContextType | undefined>(undefined)

export function useChatbot() {
  const context = useContext(ChatbotContext)
  if (!context) {
    throw new Error('useChatbot must be used within a ChatbotProvider')
  }
  return context
}

interface ChatbotProviderProps {
  children: ReactNode
}

export function GlobalChatbotProvider({ children }: ChatbotProviderProps) {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  const openChatbot = () => setIsOpen(true)
  const closeChatbot = () => setIsOpen(false)
  const toggleChatbot = () => setIsOpen(prev => !prev)

  // Get current page context for the chatbot with enhanced awareness
  const getCurrentPageContext = () => {
    // More specific page detection
    if (pathname === '/patient/dashboard') return 'patient'
    if (pathname === '/patient/onboarding') return 'patient-onboarding'
    if (pathname === '/recruiter/dashboard') return 'recruiter'
    if (pathname === '/login') return 'login'
    if (pathname === '/signup') return 'signup'
    if (pathname === '/') return 'homepage'
    
    // Fallback for general candidate/recruiter areas
    if (pathname.includes('/patient')) return 'patient'
    if (pathname.includes('/recruiter')) return 'recruiter'
    
    return 'general'
  }

  // Global keyboard listener for Alt + Space
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Check for Ctrl + Z combination
      if (event.ctrlKey && event.code === 'KeyZ') {
        event.preventDefault()
        toggleChatbot()
      }
      
      // Close chatbot on Escape key
      if (event.key === 'Escape' && isOpen) {
        closeChatbot()
      }
    }

    // Add event listener to document
    document.addEventListener('keydown', handleKeyDown)

    // Cleanup
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen])

  // Close chatbot when navigating to a new page
  useEffect(() => {
    setIsOpen(false)
  }, [pathname])

  const contextValue: ChatbotContextType = {
    isOpen,
    openChatbot,
    closeChatbot,
    toggleChatbot
  }

  return (
    <ChatbotContext.Provider value={contextValue}>
      {children}
      <FloatingChatbot
        isOpen={isOpen}
        onClose={closeChatbot}
        currentPage={getCurrentPageContext()}
      />
      <ChatbotHint />
    </ChatbotContext.Provider>
  )
}