"use client"
import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Brain, Link, Folder, Mic, X } from "lucide-react"
import { LiquidMetal, PulsingBorder } from "@paper-design/shaders-react"

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
}

interface FloatingChatbotProps {
  isOpen: boolean
  onClose: () => void
  currentPage?: string
}

export function FloatingChatbot({ isOpen, onClose, currentPage = "general" }: FloatingChatbotProps) {
  const [isFocused, setIsFocused] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")

  // Reset chat when chatbot is closed
  useEffect(() => {
    if (!isOpen) {
      setMessages([])
      setInputValue("")
    }
  }, [isOpen])

  // Add keyboard shortcut Ctrl+Z to focus chatbot input
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.ctrlKey && event.key === 'z') {
        event.preventDefault()
        if (!isOpen) {
          onClose() // This toggles the chatbot open
        }
        // Small delay to ensure chatbot is open before focusing
        setTimeout(() => {
          if (inputRef.current) {
            inputRef.current.focus()
          }
        }, 100)
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen, onClose])

  const toggleChatbot = () => {
    if (isOpen) {
      // Reset messages when closing
      setMessages([])
      setInputValue("")
    }
    onClose()
  }

  const getContextualGreeting = () => {
    switch (currentPage) {
      case "candidate":
        return "Hi! I'm here to help with your resume, job matching, and career questions."
      case "candidate-onboarding":
        return "Welcome to Pause! I'm here to help you get started and set up your profile."
      case "recruiter":
        return "Hello! I can assist with job descriptions, candidate evaluation, and recruitment."
      case "login":
        return "Need help with login or account issues? I'm here to assist!"
      case "signup":
        return "Welcome! I can help you create your account and get started on Pause."
      case "homepage":
        return "Welcome to Pause! I'm here to answer questions about our platform and features."
      default:
        return "Hey there! I'm your AI assistant. How can I help you today?"
    }
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return
    
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: "user",
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    const messageToSend = inputValue
    setInputValue("")
    
    try {
      // Call the chat API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          context: currentPage,
          conversationHistory: messages
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to get response')
      }
      
      const data = await response.json()
      
      if (data.success && data.message) {
        setMessages(prev => [...prev, {
          id: data.message.id,
          content: data.message.content,
          role: "assistant",
          timestamp: new Date(data.message.timestamp)
        }])
      }
    } catch (error) {
      console.error('Chat error:', error)
      // Fallback response
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm sorry, I'm having trouble responding right now. Please try again in a moment.",
        role: "assistant",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorResponse])
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>

          
          {/* Bottom Chat Input Bar */}
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            transition={{ duration: 0.3, type: "spring", stiffness: 300, damping: 30 }}
            className="fixed bottom-20 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6 z-50"
          >


            {/* Globe and Greeting Section */}
            <div className="flex flex-row items-center mb-2">
              {/* Globe Animation */}
              <motion.div
                className="relative flex items-center justify-center z-10 mr-3"
                animate={{
                  y: isFocused ? 50 : 0,
                  opacity: isFocused ? 0 : 1,
                  filter: isFocused ? "blur(4px)" : "blur(0px)",
                  rotation: isFocused ? 180 : 0,
                }}
                transition={{
                  duration: 0.5,
                  type: "spring",
                  stiffness: 200,
                  damping: 20,
                }}
              >
                <div className="z-10 absolute bg-white/5 h-10 w-10 rounded-full backdrop-blur-[3px]">
                  <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-3 left-3 blur-[1px]" />
                  <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-2 left-6 blur-[0.8px]" />
                  <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-7 left-2 blur-[1px]" />
                  <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-4 left-8 blur-[0.8px]" />
                  <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-6 left-6 blur-[1px]" />
                </div>
                <LiquidMetal
                  style={{ height: 70, width: 70, filter: "blur(14px)", position: "absolute" }}
                  colorBack="hsl(0, 0%, 0%, 0)"
                  colorTint="hsl(29, 77%, 49%)"
                  repetition={4}
                  softness={0.5}
                  shiftRed={0.3}
                  shiftBlue={0.3}
                  distortion={0.1}
                  contour={1}
                  shape="circle"
                  offsetX={0}
                  offsetY={0}
                  scale={0.58}
                  rotation={50}
                  speed={5}
                />
                <LiquidMetal
                  style={{ height: 70, width: 70 }}
                  colorBack="hsl(0, 0%, 0%, 0)"
                  colorTint="hsl(29, 77%, 49%)"
                  repetition={4}
                  softness={0.5}
                  shiftRed={0.3}
                  shiftBlue={0.3}
                  distortion={0.1}
                  contour={1}
                  shape="circle"
                  offsetX={0}
                  offsetY={0}
                  scale={0.58}
                  rotation={50}
                  speed={5}
                />
              </motion.div>

              {/* Greeting Text */}
               <motion.p
                 className="text-white/50 text-sm font-light z-10"
                 animate={{
                   y: isFocused ? 50 : 0,
                   opacity: isFocused ? 0 : 100,
                   filter: isFocused ? "blur(4px)" : "blur(0px)",
                 }}
                 transition={{
                   duration: 0.5,
                   type: "spring",
                   stiffness: 200,
                   damping: 20,
                 }}
               >
                 {getContextualGreeting()}
               </motion.p>
             </div>

             {/* Messages */}
             {messages.length > 0 && (
               <div className="max-h-48 overflow-y-auto space-y-3 mb-4 px-2 scrollbar-hide">
                 {messages.map((message) => (
                   <motion.div
                     key={message.id}
                     initial={{ opacity: 0, y: 10 }}
                     animate={{ opacity: 1, y: 0 }}
                     className={`flex ${
                       message.role === "user" ? "justify-end" : "justify-start"
                     }`}
                   >
                     <div
                       className={`max-w-[75%] p-3 rounded-xl backdrop-blur-md border ${
                         message.role === "user"
                           ? "bg-orange-500/20 border-orange-400/30 text-orange-100"
                           : "bg-white/10 border-white/20 text-gray-200"
                       } shadow-lg`}
                     >
                       <p className="text-sm leading-relaxed">{message.content}</p>
                       <span className="text-xs opacity-60 mt-1 block">
                         {message.timestamp.toLocaleTimeString([], {
                           hour: "2-digit",
                           minute: "2-digit",
                         })}
                       </span>
                     </div>
                   </motion.div>
                 ))}
               </div>
             )}

            {/* Input area */}
            <div className="relative mt-4">

              <div className="relative bg-zinc-900/90 backdrop-blur-md border border-zinc-700/50 rounded-2xl shadow-2xl p-4 z-10 flex items-center gap-3">
                <Textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything..."
                  className="flex-1 min-h-[40px] max-h-[120px] resize-none bg-transparent border-none text-white text-sm placeholder:text-zinc-500 focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none [&:focus]:ring-0 [&:focus]:outline-none [&:focus-visible]:ring-0 [&:focus-visible]:outline-none"
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                />
                
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-8 w-8 rounded-full bg-zinc-700 hover:bg-zinc-600 text-zinc-300 hover:text-white p-0"
                  >
                    <Brain className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-8 w-8 rounded-full bg-zinc-700 hover:bg-zinc-600 text-zinc-300 hover:text-white p-0"
                  >
                    <Mic className="h-4 w-4" />
                  </Button>
                  
                  <Button
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim()}
                    className="bg-[#e78a53] hover:bg-[#d17a43] text-white px-4 py-2 h-8 text-sm"
                  >
                    Send
                  </Button>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}