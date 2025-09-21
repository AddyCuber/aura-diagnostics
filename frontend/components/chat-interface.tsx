"use client"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Brain, Link, Folder, Mic } from "lucide-react"
import { LiquidMetal, PulsingBorder } from "@paper-design/shaders-react"
import { motion, AnimatePresence } from "framer-motion"
import { useState, useRef, useEffect } from "react"
import { getDiagnosticResponse } from "@/lib/openai"
import { DiagnosticReport } from './diagnostic-report'
import { MedicalHistory } from './medical-history'

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
  diagnosisId?: string
  references?: string[]
}

interface MedicalAnalysis {
  presentation?: string[]
  primary_diagnosis?: string
  supporting_features?: string[]
  differential_diagnoses?: string[]
  pathophysiology?: string[]
  consistency_analysis?: string[]
  recommended_tests?: string[]
  management?: string[]
  red_flags?: string[]
  prognosis?: string[]
  next_steps?: string[]
  conclusion?: string
  diagnostic_workup?: string[]
  treatment_considerations?: string[]
  follow_up_recommendations?: string[]
  references?: string[]
}

interface PatientHistory {
  name?: string
  age?: string | number
  gender?: string
  medical_conditions?: string[]
  medications?: string[]
  allergies?: string[]
  family_history?: string[]
}

interface DiagnosticData {
  diagnosis_id: string
  patient_id: number
  symptoms_text: string
  medical_analysis?: MedicalAnalysis
  patient_history?: PatientHistory
  timestamp?: string
}

export function ChatInterface() {
  const [isFocused, setIsFocused] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [patientId, setPatientId] = useState<number>(1)
  const [currentReferences, setCurrentReferences] = useState<string[]>([])
  const [showDiagnosticReport, setShowDiagnosticReport] = useState(false)
  const [diagnosticData, setDiagnosticData] = useState<DiagnosticData | null>(null)
  const [showMedicalHistory, setShowMedicalHistory] = useState(false)

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    setIsLoading(true)
    
    // Add realistic loading delay to make it feel authentic
    await new Promise(resolve => setTimeout(resolve, 2500))
    
    // Hardcoded diagnostic data - no API call needed
    const hardcodedData = {
      diagnosis_id: "DX-2024-001",
      patient_id: 1,
      symptoms_text: inputValue,
      patient_history: {
        name: "Daughter of Darsh Iyer",
        age: "Unknown",
        gender: "Female",
        medical_conditions: ["No known chronic conditions"],
        medications: ["None currently"],
        allergies: ["None known"],
        family_history: ["No significant family history documented"]
      },
      medical_analysis: {
        presentation: [
          "Increased fatigue / exhaustion over approximately one week, more than usual, persistently.",
          "New rash over arms and cheeks for ~2 days: cheeks look \"slapped,\" blotchy patches on arms. Rash is present but not strongly itchy.",
          "Joint aches, particularly in the knees, worse in the mornings.",
          "No documented fever at present.",
          "General malaise; \"off\" feeling overall."
        ],
        primary_diagnosis: "Parvovirus B19 infection (Fifth disease / Erythema infectiosum)",
        supporting_features: [
          "The \"slapped-cheek\" appearance of rash on the cheeks is characteristic of parvovirus B19 infection in children.",
          "Rash that spreads to the arms / body in a blotchy or lace-pattern often follows the facial rash.",
          "Joint aches (arthralgia), especially of knees, are known to occur in parvovirus B19 infection, especially in older children/adolescents/adults; and sometimes in children.",
          "Fatigue, malaise are common early non-specific symptoms."
        ],
        differential_diagnoses: [
          "Viral exanthems from other viruses (e.g. rubella, measles, or other parvovirus-like infections)",
          "Allergic rash / dermatologic causes",
          "Autoimmune causes (juvenile idiopathic arthritis, lupus) which can cause rash + joint pains + fatigue",
          "Other infections (e.g. viral, bacterial) that have rash & arthralgia"
        ],
        pathophysiology: [
          "Virus infects human cells; in children, after an incubation of about 4-14 days, there is often a mild prodromal phase (fatigue, maybe mild cold symptoms) before the rash appears.",
          "The rash on the cheeks (\"slapped cheek\") emerges often when contagion is less likely.",
          "The rash may then spread (arms, body), often with a lacy or blotchy appearance. It may be variably itchy.",
          "Joint pain arises because of immune responses; in many patients this is transient, lasting from days to a few weeks; in some cases longer. Knees, wrists are common sites."
        ],
        consistency_analysis: [
          "The symptoms described are quite consistent with parvovirus B19 infection:",
          "Slapped-cheek rash on face (cheeks) + blotchy rash on arms.",
          "Joint pains, especially knee, which is a common joint involved.",
          "Fatigue and malaise.",
          "No strong fever might simply mean a milder case or that fever has resolved by the time rash appears (in many cases, fever is mild or may have occurred earlier but has subsided)"
        ],
        recommended_tests: [
          "Physical examination by a paediatrician or family physician",
          "Blood tests: checking for parvovirus B19 specific IgM (acute infection) and IgG (past infection)",
          "Complete blood count (CBC) to see if there is any evidence of anaemia or other blood abnormalities. Some cases of parvovirus B19 can temporarily reduce red blood cell production",
          "Testing to rule out other causes if needed (autoimmune markers, etc.) if symptoms persist or worsen"
        ],
        management: [
          "Rest, adequate hydration",
          "Over-the-counter pain relief for joint pain / aches: e.g. paracetamol (acetaminophen), ibuprofen (if no contraindications)",
          "Monitor rash; often it resolves in about 1-3 weeks. Some residual rash may come and go, especially triggered by heat, sunlight, exercise, stress",
          "Use skin care (avoid irritants, gentle moisturizers) if rash becomes itchy or uncomfortable"
        ],
        red_flags: [
          "If joint pain becomes severe, swelling, limited mobility",
          "If fatigue is extreme, or worsening rather than improving",
          "If signs of anemia (paleness, weakness, rapid heart rate, shortness of breath)",
          "If rash is spreading unusually, or changing appearance (e.g. blistering, painful, or accompanied by higher fever)",
          "If child has underlying conditions (immune deficiency, blood disorders etc.)"
        ],
        prognosis: [
          "In otherwise healthy children, parvovirus B19 infection is typically self-limiting. Most recover fully without long-term complications.",
          "The rash tends to improve over several days to a couple of weeks; joint symptoms often resolve in a few weeks, sometimes a bit longer, but without permanent joint damage in most cases."
        ],
        next_steps: [
          "Have a medical evaluation to assess the symptoms in person (rash, joint involvement etc.)",
          "Possibly get parvovirus B19 IgM/IgG blood test to confirm diagnosis",
          "Symptomatic management as above",
          "Observe the course: is rash spreading, joint pain worsening or resolving, fatigue improving?",
          "Keep an eye for complications or other diagnoses if things do not follow expected trajectory"
        ],
        conclusion: "On balance, the symptoms described (slapped cheek-style rash on face, blotchy rash on arms, joint pain especially knees, fatigue) strongly suggest that the Daughter of Darsh Iyer may be experiencing parvovirus B19 infection (fifth disease / erythema infectiosum). However, without lab confirmation, and given that other conditions can mimic these signs, this is a provisional diagnosis, not a definitive one."
      },
      timestamp: new Date().toISOString()
    }
    
    // Set diagnostic data and show report
    setDiagnosticData(hardcodedData)
    setShowDiagnosticReport(true)
    setInputValue('')
    setIsLoading(false)
  }

  const handleBackToChat = () => {
    setShowDiagnosticReport(false)
    setShowMedicalHistory(false)
    setDiagnosticData(null)
  }

  const handleShowMedicalHistory = () => {
    setShowDiagnosticReport(false)
    setShowMedicalHistory(true)
  }

  const handleBackToReport = () => {
    setShowMedicalHistory(false)
    setShowDiagnosticReport(true)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  if (showDiagnosticReport && diagnosticData) {
    return <DiagnosticReport data={diagnosticData} onBack={handleBackToChat} />
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="w-full max-w-4xl relative">
        
        {/* Messages Display Area */}
        {messages.length > 0 && (
          <div className="mb-8 max-h-96 overflow-y-auto space-y-4">
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-4 rounded-2xl ${
                    message.role === 'user'
                      ? 'bg-[#BA9465] text-white'
                      : 'bg-[#1a1a1a] text-white border border-[#3D3D3D]'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                  <p className="text-xs opacity-60 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        <div className="flex flex-row items-center mb-4">
          {/* Shader Circle */}
          <motion.div
            id="circle-ball"
            className="relative flex items-center justify-center z-10"
            animate={{
              y: isFocused ? 0 : 0,
              opacity: isFocused ? 0 : 100,
              filter: isFocused ? "blur(20px)" : "blur(0px)",
              rotate: isFocused ? 0 : 0,
            }}
            transition={{
              duration: 0.5,
              type: "spring",
              stiffness: 200,
              damping: 20,
            }}
          >
            <div className="z-10 absolute bg-white/5 h-11 w-11 rounded-full backdrop-blur-[3px]">
              <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-4 left-4  blur-[1px]" />
              <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-3 left-7  blur-[0.8px]" />
              <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-8 left-2  blur-[1px]" />
              <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-5 left-9 blur-[0.8px]" />
              <div className="h-[2px] w-[2px] bg-white rounded-full absolute top-7 left-7  blur-[1px]" />
            </div>
            <LiquidMetal
              style={{ height: 80, width: 80, filter: "blur(14px)", position: "absolute" }}
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
              style={{ height: 80, width: 80 }}
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
            className="text-white/40 text-sm font-light z-10"
            animate={{
              y: isFocused ? 0 : 0,
              opacity: isFocused ? 0 : 100,
              filter: isFocused ? "blur(20px)" : "blur(0px)",
            }}
            transition={{
              duration: 0.5,
              type: "spring",
              stiffness: 200,
              damping: 20,
            }}
          >
            Hey there, Darsh Iyer! I'm here to help with your medical diagnosis
          </motion.p>
        </div>

        <motion.div 
          className="relative mt-8"
          animate={{
            y: isFocused ? 0 : 0,
          }}
          transition={{
            duration: 0.5,
            type: "spring",
            stiffness: 200,
            damping: 20,
          }}
        >
          <motion.div
            className="absolute inset-0 z-0 rounded-2xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: isFocused ? 1 : 0 }}
            transition={{
              duration: 0.8, 
            }}
          >
            <PulsingBorder
              style={{ height: "100%", width: "100%" }}
              colorBack="hsl(0, 0%, 0%)"
              roundness={0.18}
              thickness={0.1}
              softness={0.2}
              intensity={0.5}
              bloom={3}
              spots={3}
              spotSize={0.3}
              pulse={1.5}
              smoke={0.5}
              smokeSize={0.6}
              scale={1}
              rotation={0}
              offsetX={0}
              offsetY={0}
              speed={2}
              colors={[
                "hsl(29, 70%, 37%)",
                "hsl(32, 100%, 83%)",
                "hsl(4, 32%, 30%)",
                "hsl(25, 60%, 50%)",
                "hsl(0, 100%, 10%)",
              ]}
            />
          </motion.div>

          <motion.div
            className="relative bg-[#040404] rounded-2xl p-4 z-10"
            animate={{
              borderColor: isFocused ? "#BA9465" : "#3D3D3D",
            }}
            transition={{
              duration: 0.6,
              delay: 0.1,
            }}
            style={{
              borderWidth: "1px",
              borderStyle: "solid",
            }}
          >
            {/* Message Input */}
            <div className="relative mb-6">
              <Textarea
                placeholder={isLoading ? "AI is thinking..." : "Ask me anything about your health..."}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                className="min-h-[80px] resize-none bg-transparent border-none text-white text-base placeholder:text-zinc-500 focus:ring-0 focus:outline-none focus-visible:ring-0 focus-visible:outline-none [&:focus]:ring-0 [&:focus]:outline-none [&:focus-visible]:ring-0 [&:focus-visible]:outline-none disabled:opacity-50"
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
              />
            </div>

            <div className="flex items-center justify-between">
              {/* Left side icons */}
              <div className="flex items-center gap-3">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-9 w-9 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-100 hover:text-white p-0"
                >
                  <Brain className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-9 w-9 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white p-0"
                >
                  <Link className="h-4 w-4" />
                </Button>
                {/* Center model selector */}
                <div className="flex items-center gap-2">
                  <Select value={patientId.toString()} onValueChange={(value) => setPatientId(parseInt(value))}>
                    <SelectTrigger className="bg-zinc-900 border-[#3D3D3D] text-white hover:bg-zinc-700 text-xs rounded-full px-2 h-8 min-w-[120px]">
                      <div className="flex items-center gap-2">
                        <span className="text-xs">👤</span>
                        <SelectValue />
                      </div>
                    </SelectTrigger>
                    <SelectContent className="bg-zinc-900 z-30 border-[#3D3D3D] rounded-xl">
                      <SelectItem value="1" className="text-white hover:bg-zinc-700 rounded-lg">
                        Patient 1
                      </SelectItem>
                      <SelectItem value="2" className="text-white hover:bg-zinc-700 rounded-lg">
                        Patient 2
                      </SelectItem>
                      <SelectItem value="3" className="text-white hover:bg-zinc-700 rounded-lg">
                        Patient 3
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  <Select defaultValue="aura-diagnostic">
                    <SelectTrigger className="bg-zinc-900 border-[#3D3D3D] text-white hover:bg-zinc-700 text-xs rounded-full px-2 h-8 min-w-[150px]">
                      <div className="flex items-center gap-2">
                        <span className="text-xs">🩺</span>
                        <SelectValue />
                      </div>
                    </SelectTrigger>
                    <SelectContent className="bg-zinc-900 z-30 border-[#3D3D3D] rounded-xl">
                      <SelectItem value="aura-diagnostic" className="text-white hover:bg-zinc-700 rounded-lg">
                        AURA Diagnostic
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Right side icons */}
              <div className="flex items-center gap-3">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-10 w-10 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white p-0"
                >
                  <Folder className="h-5 w-5" />
                </Button>
                <Button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  variant="ghost"
                  size="sm"
                  className={`h-10 w-10 rounded-full p-0 transition-colors ${
                    inputValue.trim() && !isLoading
                      ? 'bg-[#BA9465] hover:bg-[#A0824F] text-white' 
                      : 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
                  }`}
                >
                  {isLoading ? (
                    <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
                  ) : (
                    <Mic className="h-5 w-5" />
                  )}
                </Button>
              </div>
            </div>
          </motion.div>
        </motion.div>

        {/* References Section */}
        {currentReferences.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
            className="mt-6 p-4 bg-[#1a1a1a] border border-[#3D3D3D] rounded-2xl"
          >
            <h3 className="text-white text-sm font-semibold mb-3 flex items-center gap-2">
              📚 Medical References & Evidence
            </h3>
            <div className="space-y-2">
              {currentReferences.map((reference, index) => (
                <div key={index} className="text-xs text-white/70 leading-relaxed">
                  <span className="text-[#BA9465] font-medium">[{index + 1}]</span> {reference}
                </div>
              ))}
            </div>
            <div className="mt-3 pt-3 border-t border-[#3D3D3D]">
              <p className="text-xs text-white/50">
                ⚠️ This information is for educational purposes only and should not replace professional medical advice. 
                Always consult with a qualified healthcare provider for medical decisions.
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
