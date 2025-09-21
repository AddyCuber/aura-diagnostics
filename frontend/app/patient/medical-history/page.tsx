"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { 
  ArrowLeft, 
  User, 
  Calendar, 
  Heart, 
  Pill, 
  AlertTriangle, 
  Shield, 
  Stethoscope,
  FileText,
  Phone,
  MapPin,
  Clock,
  Activity,
  TestTube,
  Thermometer,
  Weight,
  Eye,
  Ear,
  Brain,
  Bone,
  Zap
} from "lucide-react"
import { SharedHeader } from "@/components/shared-header"
import { useRouter } from "next/navigation"

export default function MedicalHistory() {
  const router = useRouter()

  const medicalHistoryData = {
    personalInfo: {
      name: "Darsh Iyer",
      age: 21,
      gender: "Male",
      dateOfBirth: "March 15, 2003",
      bloodType: "O+",
      height: "5'10\"",
      weight: "165 lbs",
      bmi: 23.7,
      emergencyContact: {
        name: "Priya Iyer",
        relationship: "Mother",
        phone: "+1 (555) 987-6543"
      }
    },
    chronicConditions: [
      {
        condition: "None currently diagnosed",
        status: "N/A",
        notes: "Patient maintains good overall health with no chronic conditions"
      }
    ],
    pastMedicalHistory: [
      {
        condition: "Sports Injury - Sprained Right Ankle",
        date: "September 15, 2023",
        status: "Resolved",
        treatment: "Physical therapy, RICE protocol",
        duration: "6 weeks",
        notes: "Occurred during intramural soccer. Complete recovery achieved through consistent PT."
      },
      {
        condition: "Wisdom Teeth Extraction (All Four)",
        date: "June 20, 2023",
        status: "Resolved",
        treatment: "Surgical extraction under local anesthesia",
        duration: "2 weeks recovery",
        notes: "Prophylactic removal. No complications. Healed well with proper oral hygiene."
      },
      {
        condition: "Mild Acne Vulgaris",
        date: "January 10, 2022 - August 2022",
        status: "Resolved",
        treatment: "Topical benzoyl peroxide, salicylic acid cleanser",
        duration: "8 months",
        notes: "Hormonal acne during late teens. Responded well to OTC treatments."
      },
      {
        condition: "Seasonal Allergic Rhinitis",
        date: "Spring 2021, 2022, 2023",
        status: "Managed",
        treatment: "Antihistamines (Claritin) during pollen season",
        duration: "Seasonal (March-May)",
        notes: "Mild symptoms including sneezing, runny nose. Well-controlled with medication."
      }
    ],
    familyHistory: [
      {
        relation: "Father (Raj Iyer, 52)",
        conditions: ["Type 2 Diabetes (diagnosed age 45)", "Hypertension (diagnosed age 48)"],
        notes: "Well-controlled with medication and lifestyle changes"
      },
      {
        relation: "Mother (Priya Iyer, 49)",
        conditions: ["Hypothyroidism (diagnosed age 42)", "Osteoporosis (diagnosed age 47)"],
        notes: "Takes levothyroxine and calcium supplements"
      },
      {
        relation: "Paternal Grandfather (deceased age 78)",
        conditions: ["Coronary Artery Disease", "Stroke"],
        notes: "Passed away from complications of stroke"
      },
      {
        relation: "Maternal Grandmother (85, living)",
        conditions: ["Arthritis", "Cataracts"],
        notes: "Active lifestyle, manages conditions well"
      }
    ],
    socialHistory: {
      smoking: "Never smoked",
      alcohol: "Occasional social drinking (1-2 drinks per week)",
      drugs: "No recreational drug use",
      exercise: "Regular - plays soccer 2x/week, gym 3x/week",
      diet: "Balanced diet, occasional fast food",
      occupation: "College student (Computer Science major)",
      livingArrangement: "Lives in college dormitory",
      stressLevel: "Moderate (academic stress during exams)"
    },
    currentMedications: [
      {
        medication: "Multivitamin (One-A-Day Men's)",
        dosage: "1 tablet daily",
        frequency: "Daily with breakfast",
        startDate: "January 2023",
        reason: "General health maintenance"
      },
      {
        medication: "Protein Powder (Whey)",
        dosage: "1 scoop (30g)",
        frequency: "Post-workout",
        startDate: "September 2022",
        reason: "Athletic performance and muscle recovery"
      }
    ],
    allergies: [
      {
        allergen: "No Known Drug Allergies (NKDA)",
        reaction: "N/A",
        severity: "N/A"
      },
      {
        allergen: "Tree Pollen (mild)",
        reaction: "Sneezing, runny nose, watery eyes",
        severity: "Mild",
        management: "Antihistamines during spring season"
      }
    ],
    immunizations: [
      { vaccine: "COVID-19 (Pfizer)", date: "March 2021, April 2021, October 2021, September 2023", status: "Up to date" },
      { vaccine: "Influenza", date: "October 2023", status: "Annual" },
      { vaccine: "Tdap (Tetanus, Diphtheria, Pertussis)", date: "August 2021", status: "Up to date" },
      { vaccine: "MMR (Measles, Mumps, Rubella)", date: "Childhood series complete", status: "Up to date" },
      { vaccine: "Hepatitis B", date: "Childhood series complete", status: "Up to date" },
      { vaccine: "Varicella (Chickenpox)", date: "Childhood series complete", status: "Up to date" }
    ],
    recentVisits: [
      {
        date: "January 15, 2024",
        provider: "Dr. Sarah Chen, MD",
        department: "Family Medicine",
        reason: "Annual physical exam",
        findings: "Excellent health, all vitals normal",
        followUp: "Next annual exam January 2025"
      },
      {
        date: "September 20, 2023",
        provider: "Dr. Michael Rodriguez, DPT",
        department: "Physical Therapy",
        reason: "Final PT session for ankle injury",
        findings: "Full range of motion restored, strength at 100%",
        followUp: "Return to full activities, injury prevention exercises"
      },
      {
        date: "June 25, 2023",
        provider: "Dr. Jennifer Park, DDS",
        department: "Oral Surgery",
        reason: "Post-operative check (wisdom teeth)",
        findings: "Healing well, no complications",
        followUp: "Regular dental cleanings every 6 months"
      }
    ],
    vitalSigns: {
      bloodPressure: "115/75 mmHg",
      heartRate: "68 bpm",
      temperature: "98.4°F",
      respiratoryRate: "16 breaths/min",
      oxygenSaturation: "99%",
      lastUpdated: "January 15, 2024"
    },
    labResults: [
      {
        test: "Complete Blood Count (CBC)",
        date: "January 15, 2024",
        results: "All values within normal limits",
        status: "Normal"
      },
      {
        test: "Basic Metabolic Panel",
        date: "January 15, 2024",
        results: "Glucose: 88 mg/dL, Creatinine: 0.9 mg/dL",
        status: "Normal"
      },
      {
        test: "Lipid Panel",
        date: "January 15, 2024",
        results: "Total cholesterol: 165 mg/dL, HDL: 55 mg/dL, LDL: 95 mg/dL",
        status: "Excellent"
      }
    ]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <SharedHeader />
      
      <div className="container mx-auto px-4 py-8 pt-24">
        {/* Header with Back Button */}
        <div className="flex items-center gap-4 mb-8">
          <Button
            variant="outline"
            onClick={() => router.back()}
            className="border-white/20 text-white hover:bg-white/10"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
          <div>
            <h1 className="text-4xl font-bold text-white">Medical History</h1>
            <p className="text-white/60 mt-2">Comprehensive medical record for {medicalHistoryData.personalInfo.name}</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Personal Information */}
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <User className="w-5 h-5" />
                Personal Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-white/60">Full Name</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.name}</p>
                </div>
                <div>
                  <p className="text-white/60">Age</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.age} years</p>
                </div>
                <div>
                  <p className="text-white/60">Date of Birth</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.dateOfBirth}</p>
                </div>
                <div>
                  <p className="text-white/60">Blood Type</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.bloodType}</p>
                </div>
                <div>
                  <p className="text-white/60">Height</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.height}</p>
                </div>
                <div>
                  <p className="text-white/60">Weight</p>
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.weight}</p>
                </div>
              </div>
              
              <div className="border-t border-white/10 pt-4">
                <p className="text-white/60 text-sm mb-2">Emergency Contact</p>
                <div className="space-y-1">
                  <p className="text-white font-medium">{medicalHistoryData.personalInfo.emergencyContact.name}</p>
                  <p className="text-white/80 text-sm">{medicalHistoryData.personalInfo.emergencyContact.relationship}</p>
                  <p className="text-white/80 text-sm">{medicalHistoryData.personalInfo.emergencyContact.phone}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Current Vital Signs */}
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Current Vital Signs
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <Heart className="w-4 h-4 text-red-400" />
                  <div>
                    <p className="text-white/60">Blood Pressure</p>
                    <p className="text-white font-medium">{medicalHistoryData.vitalSigns.bloodPressure}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  <div>
                    <p className="text-white/60">Heart Rate</p>
                    <p className="text-white font-medium">{medicalHistoryData.vitalSigns.heartRate}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Thermometer className="w-4 h-4 text-blue-400" />
                  <div>
                    <p className="text-white/60">Temperature</p>
                    <p className="text-white font-medium">{medicalHistoryData.vitalSigns.temperature}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-green-400" />
                  <div>
                    <p className="text-white/60">O2 Saturation</p>
                    <p className="text-white font-medium">{medicalHistoryData.vitalSigns.oxygenSaturation}</p>
                  </div>
                </div>
              </div>
              <p className="text-white/60 text-xs">Last updated: {medicalHistoryData.vitalSigns.lastUpdated}</p>
            </CardContent>
          </Card>

          {/* Current Medications */}
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Pill className="w-5 h-5" />
                Current Medications
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {medicalHistoryData.currentMedications.map((med, index) => (
                <div key={index} className="border-b border-white/10 pb-3 last:border-b-0">
                  <p className="text-white font-medium">{med.medication}</p>
                  <p className="text-white/80 text-sm">{med.dosage} - {med.frequency}</p>
                  <p className="text-white/60 text-xs">Started: {med.startDate}</p>
                  <p className="text-white/60 text-xs">{med.reason}</p>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Past Medical History */}
        <Card className="bg-white/5 border-white/10 backdrop-blur-sm mt-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Past Medical History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              {medicalHistoryData.pastMedicalHistory.map((history, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border border-white/10 rounded-lg p-4 bg-white/5"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-white font-medium">{history.condition}</h3>
                    <Badge variant={history.status === 'Resolved' ? 'default' : 'secondary'} className="text-xs">
                      {history.status}
                    </Badge>
                  </div>
                  <p className="text-white/80 text-sm mb-2">{history.date}</p>
                  <p className="text-white/60 text-sm mb-2"><strong>Treatment:</strong> {history.treatment}</p>
                  <p className="text-white/60 text-sm mb-2"><strong>Duration:</strong> {history.duration}</p>
                  <p className="text-white/60 text-sm">{history.notes}</p>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Family History */}
        <Card className="bg-white/5 border-white/10 backdrop-blur-sm mt-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Heart className="w-5 h-5" />
              Family History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              {medicalHistoryData.familyHistory.map((family, index) => (
                <div key={index} className="border border-white/10 rounded-lg p-4 bg-white/5">
                  <h3 className="text-white font-medium mb-2">{family.relation}</h3>
                  <ul className="space-y-1 mb-2">
                    {family.conditions.map((condition, condIndex) => (
                      <li key={condIndex} className="text-white/80 text-sm">• {condition}</li>
                    ))}
                  </ul>
                  <p className="text-white/60 text-sm">{family.notes}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Social History */}
        <Card className="bg-white/5 border-white/10 backdrop-blur-sm mt-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <User className="w-5 h-5" />
              Social History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <h4 className="text-white font-medium mb-2">Lifestyle</h4>
                <div className="space-y-2 text-sm">
                  <p className="text-white/80"><strong>Smoking:</strong> {medicalHistoryData.socialHistory.smoking}</p>
                  <p className="text-white/80"><strong>Alcohol:</strong> {medicalHistoryData.socialHistory.alcohol}</p>
                  <p className="text-white/80"><strong>Drugs:</strong> {medicalHistoryData.socialHistory.drugs}</p>
                </div>
              </div>
              <div>
                <h4 className="text-white font-medium mb-2">Health & Fitness</h4>
                <div className="space-y-2 text-sm">
                  <p className="text-white/80"><strong>Exercise:</strong> {medicalHistoryData.socialHistory.exercise}</p>
                  <p className="text-white/80"><strong>Diet:</strong> {medicalHistoryData.socialHistory.diet}</p>
                  <p className="text-white/80"><strong>Stress Level:</strong> {medicalHistoryData.socialHistory.stressLevel}</p>
                </div>
              </div>
              <div>
                <h4 className="text-white font-medium mb-2">Living Situation</h4>
                <div className="space-y-2 text-sm">
                  <p className="text-white/80"><strong>Occupation:</strong> {medicalHistoryData.socialHistory.occupation}</p>
                  <p className="text-white/80"><strong>Living:</strong> {medicalHistoryData.socialHistory.livingArrangement}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Allergies & Immunizations */}
        <div className="grid md:grid-cols-2 gap-8 mt-8">
          <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Allergies
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {medicalHistoryData.allergies.map((allergy, index) => (
                <div key={index} className="border-b border-white/10 pb-3 last:border-b-0">
                  <p className="text-white font-medium">{allergy.allergen}</p>
                  {allergy.reaction !== 'N/A' && (
                    <>
                      <p className="text-white/80 text-sm">Reaction: {allergy.reaction}</p>
                      <p className="text-white/60 text-sm">Severity: {allergy.severity}</p>
                      {allergy.management && (
                        <p className="text-white/60 text-sm">Management: {allergy.management}</p>
                      )}
                    </>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Shield className="w-5 h-5" />
                Immunizations
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {medicalHistoryData.immunizations.map((vaccine, index) => (
                <div key={index} className="flex justify-between items-center border-b border-white/10 pb-2 last:border-b-0">
                  <div>
                    <p className="text-white font-medium text-sm">{vaccine.vaccine}</p>
                    <p className="text-white/60 text-xs">{vaccine.date}</p>
                  </div>
                  <Badge variant="default" className="text-xs">
                    {vaccine.status}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Recent Lab Results */}
        <Card className="bg-white/5 border-white/10 backdrop-blur-sm mt-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <TestTube className="w-5 h-5" />
              Recent Laboratory Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              {medicalHistoryData.labResults.map((lab, index) => (
                <div key={index} className="border border-white/10 rounded-lg p-4 bg-white/5">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-white font-medium">{lab.test}</h3>
                    <Badge variant={lab.status === 'Normal' || lab.status === 'Excellent' ? 'default' : 'destructive'} className="text-xs">
                      {lab.status}
                    </Badge>
                  </div>
                  <p className="text-white/80 text-sm mb-2">{lab.date}</p>
                  <p className="text-white/60 text-sm">{lab.results}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Healthcare Visits */}
        <Card className="bg-white/5 border-white/10 backdrop-blur-sm mt-8 mb-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Stethoscope className="w-5 h-5" />
              Recent Healthcare Visits
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {medicalHistoryData.recentVisits.map((visit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border border-white/10 rounded-lg p-4 bg-white/5"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-white font-medium">{visit.reason}</h3>
                      <p className="text-white/80 text-sm">{visit.provider} - {visit.department}</p>
                    </div>
                    <p className="text-white/60 text-sm">{visit.date}</p>
                  </div>
                  <p className="text-white/80 text-sm mb-2"><strong>Findings:</strong> {visit.findings}</p>
                  <p className="text-white/60 text-sm"><strong>Follow-up:</strong> {visit.followUp}</p>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}