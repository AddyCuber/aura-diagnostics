"use client"
import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { X, MessageCircle } from "lucide-react"

export function ChatbotHint() {
  const [isVisible, setIsVisible] = useState(false)
  const [isDismissed, setIsDismissed] = useState(false)

  useEffect(() => {
    // Check if user has already dismissed the hint
    const dismissed = localStorage.getItem('chatbot-hint-dismissed')
    if (dismissed) {
      setIsDismissed(true)
      return
    }

    // Show hint after 3 seconds
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, 3000)

    return () => clearTimeout(timer)
  }, [])

  const handleDismiss = () => {
    setIsVisible(false)
    setIsDismissed(true)
    localStorage.setItem('chatbot-hint-dismissed', 'true')
  }

  if (isDismissed) return null

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.8 }}
          transition={{ duration: 0.4, type: "spring", stiffness: 300, damping: 30 }}
          className="fixed bottom-6 left-6 z-40"
        >
          <div className="bg-gradient-to-r from-[#e78a53] to-[#d17a43] p-4 rounded-lg shadow-lg max-w-sm">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <div className="bg-white/20 p-2 rounded-full">
                  <MessageCircle className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h3 className="text-white font-medium text-sm mb-1">
                    AI Assistant Available!
                  </h3>
                  <p className="text-white/90 text-xs leading-relaxed">
                    Press <kbd className="bg-white/20 px-1.5 py-0.5 rounded text-xs font-mono">Ctrl + Z</kbd> anywhere to open your AI assistant
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleDismiss}
                className="h-6 w-6 p-0 text-white/70 hover:text-white hover:bg-white/20 ml-2"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}