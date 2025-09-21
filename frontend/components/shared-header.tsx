"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"

interface SharedHeaderProps {
  showAuth?: boolean
  contextText?: string
  onLogout?: () => void
  showSignup?: boolean
}

export function SharedHeader({ showAuth = true, contextText, onLogout, showSignup = false }: SharedHeaderProps) {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleLogout = () => {
    if (onLogout) {
      onLogout()
    }
    // Clear any stored auth data
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userType')
    router.push('/')
  }

  const handleSignup = () => {
    router.push('/signup')
  }

  const defaultContextText = "Build your perfect resume with AI assistance"

  return (
    <>
      {/* Desktop Header */}
      <header
        className={`sticky top-4 z-[9999] mx-auto hidden w-full flex-row items-center justify-between self-start rounded-full bg-background/80 md:flex backdrop-blur-sm border border-border/50 shadow-lg transition-all duration-300 ${
          isScrolled ? "max-w-3xl px-2" : "max-w-5xl px-4"
        } py-2`}
        style={{
          willChange: "transform",
          transform: "translateZ(0)",
          backfaceVisibility: "hidden",
          perspective: "1000px",
        }}
      >
        <a
          className={`z-50 flex items-center justify-center gap-2 transition-all duration-300 ${
            isScrolled ? "ml-4" : ""
          }`}
          href="/"
        >
          <div className="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="text-foreground size-6 w-6"
            >
              <rect x="6" y="4" width="4" height="16" rx="1"/>
              <rect x="14" y="4" width="4" height="16" rx="1"/>
            </svg>
            <span className={`text-xl font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/80 bg-clip-text text-transparent transition-all duration-300 ${
              isScrolled ? "opacity-0 w-0 overflow-hidden" : "opacity-100"
            }`}>
              Pause
            </span>
          </div>
        </a>

        <div className="flex items-center gap-6">
          {!isScrolled && (
            <span className="text-sm text-muted-foreground font-medium">
              {contextText || defaultContextText}
            </span>
          )}
        </div>

        <div className="flex items-center gap-4">
          {showAuth ? (
            <>
              <a
                href="/login"
                className="font-medium transition-colors hover:text-foreground text-muted-foreground text-sm cursor-pointer"
              >
                Log In
              </a>
              <a
                href="/signup"
                className="font-medium transition-colors hover:text-foreground text-muted-foreground text-sm cursor-pointer"
              >
                Sign Up
              </a>
            </>
          ) : (
            <Button
              onClick={showSignup ? handleSignup : handleLogout}
              variant="outline"
              className="text-sm font-medium"
            >
              {showSignup ? "Sign Up" : "Logout"}
            </Button>
          )}
        </div>
      </header>

      {/* Mobile Header */}
      <header className={`sticky top-4 z-[9999] mx-4 flex w-auto flex-row items-center justify-between rounded-full bg-background/80 backdrop-blur-sm border border-border/50 shadow-lg md:hidden transition-all duration-300 ${
        isScrolled ? "px-2 py-2" : "px-4 py-3"
      }`}>
        <a
          className="flex items-center justify-center gap-2"
          href="/"
        >
          <div className="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="text-foreground size-5 w-5"
            >
              <rect x="6" y="4" width="4" height="16" rx="1"/>
              <rect x="14" y="4" width="4" height="16" rx="1"/>
            </svg>
            <span className={`text-lg font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/80 bg-clip-text text-transparent transition-all duration-300 ${
              isScrolled ? "opacity-0 w-0 overflow-hidden" : "opacity-100"
            }`}>
              Pause
            </span>
          </div>
        </a>

        <div className="flex items-center gap-2">
          {showAuth ? (
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="flex items-center justify-center w-10 h-10 rounded-full bg-background/50 border border-border/50 transition-colors hover:bg-background/80"
              aria-label="Toggle menu"
            >
              <div className="flex flex-col items-center justify-center w-5 h-5 space-y-1">
                <span
                  className={`block w-4 h-0.5 bg-foreground transition-all duration-300 ${isMobileMenuOpen ? "rotate-45 translate-y-1.5" : ""}`}
                ></span>
                <span
                  className={`block w-4 h-0.5 bg-foreground transition-all duration-300 ${isMobileMenuOpen ? "opacity-0" : ""}`}
                ></span>
                <span
                  className={`block w-4 h-0.5 bg-foreground transition-all duration-300 ${isMobileMenuOpen ? "-rotate-45 -translate-y-1.5" : ""}`}
                ></span>
              </div>
            </button>
          ) : (
            <Button
              onClick={showSignup ? handleSignup : handleLogout}
              variant="outline"
              size="sm"
              className="text-xs"
            >
              {showSignup ? "Sign Up" : "Logout"}
            </Button>
          )}
        </div>
      </header>

      {/* Mobile Menu */}
      {isMobileMenuOpen && showAuth && (
        <div className="fixed inset-0 z-[9998] bg-background/95 backdrop-blur-sm md:hidden">
          <div className="flex flex-col items-center justify-center h-full space-y-8">
            <a
              href="/login"
              className="text-lg font-medium transition-colors hover:text-foreground text-muted-foreground"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Log In
            </a>
            <a
              href="/signup"
              className="text-lg font-medium transition-colors hover:text-foreground text-muted-foreground"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Sign Up
            </a>
          </div>
        </div>
      )}
    </>
  )
}