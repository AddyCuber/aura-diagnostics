"use client"
import { useState, useEffect } from "react"
import Hero from "@/components/home/hero"
import Features from "@/components/features"
import { TestimonialsSection } from "@/components/testimonials"
import { NewReleasePromo } from "@/components/new-release-promo"
import { FAQSection } from "@/components/faq-section"
import { PricingSection } from "@/components/pricing-section"
import { StickyFooter } from "@/components/sticky-footer"
import { ShimmerButton } from "@/components/shimmer-button"
import { LineShadowText } from "@/components/line-shadow-text"
import { Button } from "@/components/ui/button"
import { ArrowRight, Menu } from "lucide-react"
import { SharedHeader } from "@/components/shared-header"

export default function Home() {
  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove("light", "system")
    root.classList.add("dark")
  }, [])

  return (
    <div className="min-h-screen w-full relative bg-black">
      {/* Animated Background */}
      <div className="absolute inset-0 z-0">
        {/* Base gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black" />
        
        {/* Animated SVG Background with Wire Effects - Hero Section Only */}
         <svg
           className="absolute top-0 left-0 w-full h-screen opacity-40"
           viewBox="0 0 1200 800"
           fill="none"
           xmlns="http://www.w3.org/2000/svg"
           preserveAspectRatio="xMidYMid slice"
           style={{ maxHeight: '100vh' }}
         >
           <defs>
             {/* Neon pulse gradients */}
             <radialGradient id="neonPulse1" cx="50%" cy="50%" r="50%">
               <stop offset="0%" stopColor="rgba(255,255,255,1)" />
               <stop offset="30%" stopColor="rgba(251,146,60,1)" />
               <stop offset="70%" stopColor="rgba(249,115,22,0.8)" />
               <stop offset="100%" stopColor="rgba(249,115,22,0)" />
             </radialGradient>
             <radialGradient id="neonPulse2" cx="50%" cy="50%" r="50%">
               <stop offset="0%" stopColor="rgba(255,255,255,0.9)" />
               <stop offset="25%" stopColor="rgba(251,146,60,0.9)" />
               <stop offset="60%" stopColor="rgba(234,88,12,0.7)" />
               <stop offset="100%" stopColor="rgba(234,88,12,0)" />
             </radialGradient>
             <radialGradient id="neonPulse3" cx="50%" cy="50%" r="50%">
               <stop offset="0%" stopColor="rgba(255,255,255,1)" />
               <stop offset="35%" stopColor="rgba(251,146,60,1)" />
               <stop offset="75%" stopColor="rgba(234,88,12,0.6)" />
               <stop offset="100%" stopColor="rgba(234,88,12,0)" />
             </radialGradient>
             
             {/* Thread fade gradients */}
             <linearGradient id="threadFade1" x1="0%" y1="0%" x2="100%" y2="0%">
               <stop offset="0%" stopColor="rgba(0,0,0,1)" />
               <stop offset="15%" stopColor="rgba(249,115,22,0.8)" />
               <stop offset="85%" stopColor="rgba(249,115,22,0.8)" />
               <stop offset="100%" stopColor="rgba(0,0,0,1)" />
             </linearGradient>
             <linearGradient id="threadFade2" x1="0%" y1="0%" x2="100%" y2="0%">
               <stop offset="0%" stopColor="rgba(0,0,0,1)" />
               <stop offset="12%" stopColor="rgba(251,146,60,0.7)" />
               <stop offset="88%" stopColor="rgba(251,146,60,0.7)" />
               <stop offset="100%" stopColor="rgba(0,0,0,1)" />
             </linearGradient>
             <linearGradient id="threadFade3" x1="0%" y1="0%" x2="100%" y2="0%">
               <stop offset="0%" stopColor="rgba(0,0,0,1)" />
               <stop offset="18%" stopColor="rgba(234,88,12,0.8)" />
               <stop offset="82%" stopColor="rgba(234,88,12,0.8)" />
               <stop offset="100%" stopColor="rgba(0,0,0,1)" />
             </linearGradient>
             
             {/* Neon glow filter */}
             <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
               <feGaussianBlur stdDeviation="2" result="coloredBlur" />
               <feMerge>
                 <feMergeNode in="coloredBlur" />
                 <feMergeNode in="SourceGraphic" />
               </feMerge>
             </filter>
           </defs>
           
           <g>
             {/* Wire Thread Animations */}
             
             {/* Thread 1 - Top area */}
             <path
               id="thread1"
               d="M100 200 Q300 180 500 220 Q700 260 900 240 Q1100 220 1200 210"
               stroke="url(#threadFade1)"
               strokeWidth="0.6"
               fill="none"
               opacity="0.4"
             />
             <circle r="1.5" fill="url(#neonPulse1)" opacity="0.6" filter="url(#neonGlow)">
               <animateMotion dur="8s" repeatCount="indefinite">
                 <mpath href="#thread1" />
               </animateMotion>
             </circle>
             
             {/* Thread 2 - Middle area */}
             <path
               id="thread2"
               d="M50 350 Q250 320 450 360 Q650 400 850 380 Q1050 360 1150 350"
               stroke="url(#threadFade2)"
               strokeWidth="0.8"
               fill="none"
               opacity="0.3"
             />
             <circle r="2" fill="url(#neonPulse2)" opacity="0.5" filter="url(#neonGlow)">
               <animateMotion dur="10s" repeatCount="indefinite">
                 <mpath href="#thread2" />
               </animateMotion>
             </circle>
             
             {/* Thread 3 - Lower area */}
             <path
               id="thread3"
               d="M150 500 Q350 480 550 520 Q750 560 950 540 Q1150 520 1200 510"
               stroke="url(#threadFade3)"
               strokeWidth="0.5"
               fill="none"
               opacity="0.4"
             />
             <circle r="1.8" fill="url(#neonPulse1)" opacity="0.4" filter="url(#neonGlow)">
               <animateMotion dur="9s" repeatCount="indefinite">
                 <mpath href="#thread3" />
               </animateMotion>
             </circle>

           </g>
         </svg>
      </div>
      
      <style jsx>{`
        @keyframes pulse1 {
          0%, 100% { opacity: 0.4; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.2); }
        }
        @keyframes pulse2 {
          0%, 100% { opacity: 0.3; transform: scale(0.9); }
          50% { opacity: 1; transform: scale(1.1); }
        }
        @keyframes pulse3 {
          0%, 100% { opacity: 0.5; transform: scale(0.7); }
          50% { opacity: 1; transform: scale(1.3); }
        }
      `}</style>

      <SharedHeader showAuth={true} />



      {/* Hero Section */}
      <Hero />

      {/* Features Section */}
      <div id="features">
        <Features />
      </div>

      {/* Pricing Section */}
      <div id="pricing">
        <PricingSection />
      </div>

      {/* Testimonials Section */}
      <div id="testimonials">
        <TestimonialsSection />
      </div>

      <NewReleasePromo />

      {/* FAQ Section */}
      <div id="faq">
        <FAQSection />
      </div>

      {/* Sticky Footer */}
      <StickyFooter />
    </div>
  )
}
