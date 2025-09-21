"use client"

import type React from "react"

import { useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SharedHeader } from "@/components/shared-header"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [userType, setUserType] = useState<"patient" | "recruiter">("patient")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    // Simulate login process
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setIsLoading(false)
    console.log("[Recruitment Platform] Login attempt:", { email, password, userType })
    
    // Redirect based on user type
    if (userType === "patient") {
      window.location.href = "/patient/dashboard"
    } else {
      window.location.href = "/recruiter/dashboard"
    }
  }

  return (
    <div className="min-h-screen bg-black relative">
      {/* Header */}
      <div className="relative z-50 p-4">
        <SharedHeader showAuth={false} showSignup={true} />
      </div>

      {/* Main content */}
      <div className="flex items-center justify-center p-4 min-h-[calc(100vh-100px)]">
        {/* Enhanced background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-zinc-900 via-black to-zinc-900" />
        <div className="absolute inset-0 bg-gradient-to-tr from-[#e78a53]/5 via-transparent to-purple-900/10" />

      {/* Enhanced decorative elements */}
      <div className="absolute top-10 left-10 w-72 h-72 bg-gradient-to-r from-[#e78a53]/20 to-purple-600/20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-gradient-to-r from-blue-600/15 to-[#e78a53]/15 rounded-full blur-3xl animate-pulse delay-1000" />
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-[#e78a53]/5 to-purple-600/5 rounded-full blur-3xl" />
      
      {/* Additional floating elements for enhanced aesthetics */}
      <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-gradient-to-br from-[#e78a53]/10 to-transparent rounded-full blur-2xl animate-bounce" style={{animationDuration: '3s'}} />
      <div className="absolute bottom-1/4 left-1/4 w-24 h-24 bg-gradient-to-tl from-purple-500/10 to-transparent rounded-full blur-xl animate-bounce" style={{animationDuration: '4s', animationDelay: '1s'}} />
      
      {/* Floating particles */}
      <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-[#e78a53]/30 rounded-full animate-bounce" style={{animationDelay: '0s', animationDuration: '3s'}} />
      <div className="absolute top-3/4 right-1/4 w-1 h-1 bg-white/20 rounded-full animate-bounce" style={{animationDelay: '1s', animationDuration: '4s'}} />
      <div className="absolute top-1/2 right-1/3 w-1.5 h-1.5 bg-[#e78a53]/40 rounded-full animate-bounce" style={{animationDelay: '2s', animationDuration: '5s'}} />

      <motion.div
        initial={{ opacity: 0, y: 30, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 w-full max-w-md mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2 bg-gradient-to-r from-white to-zinc-300 bg-clip-text text-transparent">Welcome Back</h1>
          <p className="text-zinc-400">Sign in to continue your journey</p>
        </div>

        {/* Enhanced Login Form */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="relative backdrop-blur-2xl bg-white/[0.08] border border-white/20 rounded-3xl p-10 shadow-2xl overflow-hidden"
          whileHover={{ scale: 1.02, y: -5 }}
        >
          {/* Inner glow effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#e78a53]/10 via-transparent to-purple-500/10 rounded-3xl" />
          <div className="absolute inset-[1px] bg-gradient-to-br from-white/5 to-transparent rounded-3xl" />
          <div className="relative z-10">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* User Type Selection */}
              <div className="space-y-3">
                <Label className="text-white text-sm font-medium">
                  I am a:
                </Label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setUserType("patient")}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                      userType === "patient"
                        ? "border-[#e78a53] bg-[#e78a53]/10 text-white"
                        : "border-zinc-700 bg-zinc-800/30 text-zinc-400 hover:border-zinc-600"
                    }`}
                  >
                    <div className="text-center">
                      <div className="text-2xl mb-2">🏥</div>
                      <div className="font-medium">Patient</div>
                      <div className="text-xs mt-1 opacity-80">Health management</div>
                    </div>
                  </button>
                  <button
                    type="button"
                    onClick={() => setUserType("recruiter")}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                      userType === "recruiter"
                        ? "border-[#e78a53] bg-[#e78a53]/10 text-white"
                        : "border-zinc-700 bg-zinc-800/30 text-zinc-400 hover:border-zinc-600"
                    }`}
                  >
                    <div className="text-center">
                      <div className="text-2xl mb-2">🏢</div>
                      <div className="font-medium">Recruiter</div>
                      <div className="text-xs mt-1 opacity-80">Hiring talent</div>
                    </div>
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                <Label htmlFor="email" className="text-white/90 font-medium text-sm">
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-white/10 border-white/30 text-white placeholder:text-white/60 focus:border-[#e78a53] focus:ring-2 focus:ring-[#e78a53]/30 rounded-xl h-12 backdrop-blur-sm transition-all duration-200 hover:bg-white/15"
                  required
                />
              </div>

              <div className="space-y-3">
                <Label htmlFor="password" className="text-white/90 font-medium text-sm">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-white/10 border-white/30 text-white placeholder:text-white/60 focus:border-[#e78a53] focus:ring-2 focus:ring-[#e78a53]/30 rounded-xl h-12 backdrop-blur-sm transition-all duration-200 hover:bg-white/15"
                  required
                />
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center space-x-2 text-sm">
                  <input
                    type="checkbox"
                    className="rounded border-zinc-700 bg-zinc-800 text-[#e78a53] focus:ring-[#e78a53]/20"
                  />
                  <span className="text-zinc-300">Remember me</span>
                </label>
                <Link href="#" className="text-sm text-[#e78a53] hover:text-[#e78a53]/80">
                  Forgot password?
                </Link>
              </div>

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-[#e78a53] to-[#d4763f] hover:from-[#d4763f] hover:to-[#c26b35] text-white font-semibold py-3 rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-[#e78a53]/25 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none h-12 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <span className="relative z-10">
                  {isLoading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      <span>Signing in...</span>
                    </div>
                  ) : (
                    "Sign In"
                  )}
                </span>
              </Button>
            </form>

            <div className="mt-6 text-center relative z-10">
              <p className="text-zinc-400">
                Don't have an account?{" "}
                <Link href="/signup" className="text-[#e78a53] hover:text-[#e78a53]/80 font-medium transition-colors duration-200 hover:underline">
                  Create account
                </Link>
              </p>
            </div>
          </div>
        </motion.div>

        {/* Enhanced Social Login */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8"
        >
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-zinc-700/50" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-black text-zinc-500 font-medium">Or continue with</span>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-4">
            <Button
              variant="outline"
              className="relative bg-zinc-900/60 border-zinc-700/50 text-zinc-300 hover:bg-zinc-800/80 hover:text-white hover:border-zinc-600 transition-all duration-300 group backdrop-blur-sm py-3 rounded-xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-red-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <svg
                className="w-5 h-5 mr-2 text-zinc-300 group-hover:text-white transition-colors duration-300 relative z-10"
                viewBox="0 0 24 24"
              >
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              <span className="relative z-10 font-medium">Google</span>
            </Button>
            <Button
              variant="outline"
              className="relative bg-zinc-900/60 border-zinc-700/50 text-zinc-300 hover:bg-zinc-800/80 hover:text-white hover:border-zinc-600 transition-all duration-300 group backdrop-blur-sm py-3 rounded-xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <svg
                className="w-5 h-5 mr-2 text-zinc-300 group-hover:text-white transition-colors duration-300 relative z-10"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              <span className="relative z-10 font-medium">GitHub</span>
            </Button>
          </div>
        </motion.div>
      </motion.div>
      </div>
    </div>
  )
}
