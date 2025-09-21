"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { 
  Heart, 
  Activity, 
  Thermometer, 
  Weight, 
  Calendar, 
  Clock, 
  MapPin, 
  Mail, 
  Phone,
  User,
  FileText,
  AlertTriangle,
  CheckCircle,
  Plus,
  Search,
  Filter,
  BarChart3,
  Stethoscope,
  Pill,
  TestTube,
  MessageCircle,
  ChevronDown
} from "lucide-react"
import { SharedHeader } from "@/components/shared-header"
import { ChatInterface } from "@/components/chat-interface"

interface PatientData {
  id: string
  name: string
  age: number
  bloodType: string
  email: string
  phone: string
  address: string
  emergencyContact: {
    name: string
    relationship: string
    phone: string
  }
  vitals: {
    bloodPressure: string
    heartRate: number
    temperature: number
    height: string
    weight: string
    bmi: number
  }
  allergies: string[]
  currentMedications: string[]
  upcomingAppointments: Array<{
    id: string
    date: string
    time: string
    doctor: string
    department: string
    type: string
  }>
  recentTests: Array<{
    id: string
    name: string
    date: string
    result: string
    status: 'normal' | 'abnormal' | 'pending'
  }>
  medicalHistory: Array<{
    id: string
    condition: string
    diagnosedDate: string
    status: 'active' | 'resolved' | 'chronic'
    notes: string
  }>
}

export default function PatientDashboard() {
  const router = useRouter()
  const [activeSection, setActiveSection] = useState('overview')
  const sectionsRef = useRef<(HTMLElement | null)[]>([])

  // Mock patient data
  const [patientData] = useState<PatientData>({
    id: 'patient-1',
    name: 'Darsh Iyer',
    age: 21,
    bloodType: 'O+',
    email: 'darsh.iyer@email.com',
    phone: '+1 (555) 123-4567',
    address: '456 College Ave, Berkeley, CA 94704',
    emergencyContact: {
      name: 'Priya Iyer',
      relationship: 'Mother',
      phone: '+1 (555) 987-6543'
    },
    vitals: {
      bloodPressure: '115/75',
      heartRate: 68,
      temperature: 98.4,
      height: '5\'10"',
      weight: '165 lbs',
      bmi: 23.7
    },
    allergies: ['None known'],
    currentMedications: ['Multivitamin'],
    upcomingAppointments: [
      {
        id: 'apt-1',
        date: '2024-02-15',
        time: '10:00 AM',
        doctor: 'Dr. Smith',
        department: 'Cardiology',
        type: 'Follow-up'
      },
      {
        id: 'apt-2',
        date: '2024-02-20',
        time: '2:30 PM',
        doctor: 'Dr. Brown',
        department: 'General',
        type: 'Annual Check-up'
      }
    ],
    recentTests: [
      {
        id: 'test-1',
        name: 'Blood Panel',
        date: '2024-01-15',
        result: 'All values within normal range',
        status: 'normal'
      },
      {
        id: 'test-2',
        name: 'Chest X-Ray',
        date: '2024-01-10',
        result: 'Clear lungs, no abnormalities',
        status: 'normal'
      },
      {
        id: 'test-3',
        name: 'ECG',
        date: '2024-01-08',
        result: 'Normal sinus rhythm',
        status: 'normal'
      }
    ],
    medicalHistory: [
      {
        id: 'history-1',
        condition: 'Sports Injury - Sprained Ankle',
        diagnosedDate: '2023-09-15',
        status: 'resolved',
        notes: 'Fully recovered after 6 weeks of physical therapy'
      },
      {
        id: 'history-2',
        condition: 'Wisdom Teeth Extraction',
        diagnosedDate: '2023-06-20',
        status: 'resolved',
        notes: 'All four wisdom teeth removed, healed well'
      },
      {
        id: 'history-3',
        condition: 'Mild Acne',
        diagnosedDate: '2022-01-10',
        status: 'resolved',
        notes: 'Treated with topical medication, cleared up'
      }
    ]
  })

  // Intersection Observer for section detection
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const sectionId = entry.target.id
            setActiveSection(sectionId)
            const section = entry.target as HTMLElement
            section.style.opacity = '1'
            section.style.transform = 'translateY(0)'
          }
        })
      },
      { threshold: 0.5 }
    )

    sectionsRef.current.forEach((section) => {
      if (section) {
        section.style.opacity = '0'
        section.style.transform = 'translateY(20px)'
        section.style.transition = 'opacity 0.8s ease, transform 0.8s ease'
        observer.observe(section)
      }
    })

    return () => observer.disconnect()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal': return 'bg-green-100 text-green-800'
      case 'abnormal': return 'bg-red-100 text-red-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'active': return 'bg-blue-100 text-blue-800'
      case 'resolved': return 'bg-gray-100 text-gray-800'
      case 'chronic': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-black text-foreground relative">
      <SharedHeader 
        showAuth={false} 
        contextText="Your personal health dashboard with AI-powered insights and comprehensive care management"
      />
      
      {/* Left-side Navigation */}
      <nav className="fixed left-8 top-1/2 -translate-y-1/2 z-10 hidden lg:block">
        <div className="flex flex-col gap-4">
          {['overview', 'assistant'].map((section) => (
            <button
              key={section}
              onClick={() => document.getElementById(section)?.scrollIntoView({ behavior: 'smooth' })}
              className={`w-2 h-8 rounded-full transition-all duration-500 ${
                activeSection === section ? 'bg-foreground' : 'bg-muted-foreground/30 hover:bg-muted-foreground/60'
              }`}
              aria-label={`Navigate to ${section}`}
            />
          ))}
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-8 lg:px-16 bg-black">
        {/* Overview Section - Patient Greeting */}
        <header
          id="overview"
          ref={(el) => { sectionsRef.current[0] = el }}
          className="min-h-screen flex items-center opacity-0 bg-black"
        >
          <div className="grid lg:grid-cols-5 gap-16 w-full">
            <div className="lg:col-span-3 space-y-8">
              <div className="space-y-2">
                <div className="text-sm text-white/60 font-mono tracking-wider">PATIENT DASHBOARD / 2025</div>
                <h1 className="text-6xl lg:text-7xl font-light tracking-tight text-white">
                  Welcome,
                  <br />
                  <span className="text-white/60">{patientData.name.split(' ')[0]}</span>
                </h1>
              </div>

              <div className="space-y-6 max-w-md">
                <p className="text-xl text-white/60 leading-relaxed">
                  Your health journey powered by
                  <span className="text-white"> AI insights</span> and
                  <span className="text-white"> personalized care</span> management.
                </p>

                <div className="flex items-center gap-4 text-sm text-white/60">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    All vitals normal
                  </div>
                  <div>{patientData.upcomingAppointments.length} upcoming appointments</div>
                </div>

                <Button 
                   variant="outline" 
                   className="mt-6 border-white/20 text-white hover:bg-white/10"
                   onClick={() => router.push('/patient/medical-history')}
                 >
                   <FileText className="w-4 h-4 mr-2" />
                   View Detailed Medical History
                 </Button>
               </div>

               {/* Scroll Down Arrow */}
               <div className="flex justify-center mt-12">
                 <button
                   onClick={() => document.getElementById('assistant')?.scrollIntoView({ behavior: 'smooth' })}
                   className="flex flex-col items-center gap-2 text-white/60 hover:text-white transition-colors duration-300 group"
                 >
                   <span className="text-sm font-medium">Scroll for AI Assistant</span>
                   <ChevronDown className="w-5 h-5 animate-bounce group-hover:animate-pulse" />
                 </button>
               </div>
            </div>

            <div className="lg:col-span-2 flex flex-col justify-end space-y-8">
              {/* Quick Health Overview Cards */}
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-4 hover:shadow-lg transition-all duration-300 bg-white/5 border-white/10">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-white">{patientData.vitals.heartRate}</div>
                    <div className="text-xs text-white/60 flex items-center gap-1">
                      <Heart className="w-3 h-3" />
                      Heart Rate (BPM)
                    </div>
                  </div>
                </Card>
                
                <Card className="p-4 hover:shadow-lg transition-all duration-300 bg-white/5 border-white/10">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-white">{patientData.vitals.bloodPressure}</div>
                    <div className="text-xs text-white/60 flex items-center gap-1">
                      <Activity className="w-3 h-3" />
                      Blood Pressure
                    </div>
                  </div>
                </Card>

                <Card className="p-4 hover:shadow-lg transition-all duration-300 bg-white/5 border-white/10">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-white">{patientData.vitals.temperature}°F</div>
                    <div className="text-xs text-white/60 flex items-center gap-1">
                      <Thermometer className="w-3 h-3" />
                      Temperature
                    </div>
                  </div>
                </Card>

                <Card className="p-4 hover:shadow-lg transition-all duration-300 bg-white/5 border-white/10">
                  <div className="space-y-2">
                    <div className="text-2xl font-bold text-white">{patientData.vitals.bmi}</div>
                    <div className="text-xs text-white/60 flex items-center gap-1">
                      <Weight className="w-3 h-3" />
                      BMI
                    </div>
                  </div>
                </Card>
              </div>

              {/* Next Appointment Card */}
              {patientData.upcomingAppointments.length > 0 && (
                <Card className="p-6 bg-white/5 border-white/10">
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-blue-400">
                      <Calendar className="w-4 h-4" />
                      <span className="text-sm font-medium">Next Appointment</span>
                    </div>
                    <div className="space-y-1">
                      <div className="font-semibold text-white">
                        {patientData.upcomingAppointments[0].doctor}
                      </div>
                      <div className="text-sm text-white/60">
                        {patientData.upcomingAppointments[0].department} • {patientData.upcomingAppointments[0].type}
                      </div>
                      <div className="text-sm text-white/60">
                        {new Date(patientData.upcomingAppointments[0].date).toLocaleDateString()} at {patientData.upcomingAppointments[0].time}
                      </div>
                    </div>
                  </div>
                </Card>
              )}
            </div>
          </div>
        </header>

        {/* AI Health Assistant Section */}
        <section
          id="assistant"
          ref={(el) => { sectionsRef.current[1] = el }}
          className="min-h-screen flex items-center opacity-0 bg-black"
        >
          <div className="w-full">
            <div className="text-center space-y-8 -mb-48">
              <div className="space-y-2">
                <div className="text-sm text-white/60 font-mono tracking-wider">AI HEALTH ASSISTANT</div>
                <h2 className="text-5xl lg:text-6xl font-light tracking-tight text-white">
                  Your Personal
                  <br />
                  <span className="text-white/60">Health Companion</span>
                </h2>
              </div>
              <p className="text-xl text-white/60 max-w-2xl mx-auto leading-relaxed">
                Get instant answers to your health questions, symptom analysis, and personalized recommendations.
              </p>
            </div>

            {/* Chat Interface */}
            <div className="max-w-4xl mx-auto">
              <ChatInterface />
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}