"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Calendar, Heart, Pill, AlertTriangle, Users, Activity } from "lucide-react"

interface MedicalHistoryProps {
  patientName: string
  patientAge: number
  onBack: () => void
}

export function MedicalHistory({ patientName, patientAge, onBack }: MedicalHistoryProps) {
  // Realistic medical history for a 21-year-old
  const medicalHistory = {
    personalHistory: {
      birthDate: "March 15, 2003",
      bloodType: "O+",
      height: "5'10\" (178 cm)",
      weight: "165 lbs (75 kg)",
      bmi: "23.7 (Normal)",
      emergencyContact: "Priya Iyer (Mother) - (555) 123-4567"
    },
    chronicConditions: [
      {
        condition: "Seasonal Allergic Rhinitis",
        diagnosedDate: "2018",
        status: "Active - Well Controlled",
        description: "Mild seasonal allergies primarily affecting spring and fall seasons. Responds well to antihistamines."
      }
    ],
    pastMedicalHistory: [
      {
        condition: "Childhood Asthma",
        diagnosedDate: "2008",
        resolvedDate: "2016",
        status: "Resolved",
        description: "Mild intermittent asthma during childhood. No episodes since age 13. No longer requires medication."
      },
      {
        condition: "Appendectomy",
        date: "July 2019",
        status: "Resolved",
        description: "Laparoscopic appendectomy performed at age 16. Uncomplicated recovery, no residual issues."
      },
      {
        condition: "Concussion",
        date: "September 2020",
        status: "Resolved",
        description: "Mild concussion from sports injury (soccer). Full recovery within 3 weeks, cleared for all activities."
      }
    ],
    currentMedications: [
      {
        medication: "Loratadine (Claritin)",
        dosage: "10mg daily",
        frequency: "As needed during allergy season",
        prescribedDate: "2020",
        indication: "Seasonal allergies"
      },
      {
        medication: "Multivitamin",
        dosage: "1 tablet daily",
        frequency: "Daily with breakfast",
        prescribedDate: "2021",
        indication: "General health maintenance"
      }
    ],
    allergies: [
      {
        allergen: "Tree Pollen",
        reaction: "Rhinitis, watery eyes, sneezing",
        severity: "Mild to Moderate",
        firstOccurrence: "2015"
      },
      {
        allergen: "Dust Mites",
        reaction: "Nasal congestion, mild wheezing",
        severity: "Mild",
        firstOccurrence: "2016"
      }
    ],
    familyHistory: [
      {
        relation: "Paternal Grandfather",
        condition: "Hypertension",
        ageOfOnset: "55",
        status: "Managed with medication"
      },
      {
        relation: "Maternal Grandmother",
        condition: "Type 2 Diabetes",
        ageOfOnset: "62",
        status: "Well controlled with diet and medication"
      },
      {
        relation: "Father",
        condition: "High Cholesterol",
        ageOfOnset: "45",
        status: "Managed with lifestyle changes"
      },
      {
        relation: "Mother",
        condition: "Migraine Headaches",
        ageOfOnset: "30",
        status: "Occasional episodes, managed with medication"
      }
    ],
    socialHistory: {
      occupation: "College Student - Computer Science Major",
      education: "Currently pursuing Bachelor's degree",
      smokingStatus: "Never smoker",
      alcoholUse: "Social drinking - 1-2 drinks per week",
      drugUse: "None",
      exercise: "Regular - Soccer 3x/week, gym 2x/week",
      diet: "Generally healthy, occasional fast food"
    },
    immunizations: [
      { vaccine: "COVID-19 (Pfizer)", date: "2021-2022", status: "Up to date" },
      { vaccine: "Influenza", date: "Annual", status: "Current" },
      { vaccine: "Tdap", date: "2018", status: "Current" },
      { vaccine: "MMR", date: "Childhood series", status: "Complete" },
      { vaccine: "Varicella", date: "Childhood series", status: "Complete" },
      { vaccine: "HPV", date: "2017-2018", status: "Complete series" }
    ],
    recentVisits: [
      {
        date: "2024-01-15",
        type: "Annual Physical",
        provider: "Dr. Sarah Chen, MD",
        findings: "Normal physical exam, all vital signs within normal limits",
        followUp: "Routine annual exam in 2025"
      },
      {
        date: "2023-09-20",
        type: "Sports Physical",
        provider: "Dr. Michael Rodriguez, MD",
        findings: "Cleared for all athletic activities",
        followUp: "None needed"
      },
      {
        date: "2023-04-10",
        type: "Allergy Consultation",
        provider: "Dr. Jennifer Park, MD",
        findings: "Seasonal allergies well controlled with current regimen",
        followUp: "As needed basis"
      }
    ]
  }

  return (
    <div className="fixed inset-0 z-50 min-h-screen bg-black text-white overflow-auto">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <Button onClick={onBack} variant="ghost" size="sm" className="text-white hover:bg-zinc-800">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Report
            </Button>
            <div>
              <h1 className="text-2xl font-bold">Detailed Medical History</h1>
              <p className="text-zinc-400">Complete medical record for {patientName}</p>
            </div>
          </div>
        </div>

        {/* Patient Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Activity className="h-5 w-5 text-blue-400" />
            <h2 className="text-xl font-semibold">Patient Information</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="text-zinc-400 text-sm">Full Name</p>
              <p className="font-medium">{patientName}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Age</p>
              <p className="font-medium">{patientAge} years old</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Date of Birth</p>
              <p className="font-medium">{medicalHistory.personalHistory.birthDate}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Blood Type</p>
              <p className="font-medium">{medicalHistory.personalHistory.bloodType}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Height / Weight</p>
              <p className="font-medium">{medicalHistory.personalHistory.height} / {medicalHistory.personalHistory.weight}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">BMI</p>
              <p className="font-medium">{medicalHistory.personalHistory.bmi}</p>
            </div>
          </div>
        </motion.div>

        {/* Current Conditions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Heart className="h-5 w-5 text-red-400" />
            <h2 className="text-xl font-semibold">Current Medical Conditions</h2>
          </div>
          {medicalHistory.chronicConditions.map((condition, index) => (
            <div key={index} className="border-l-4 border-yellow-500 pl-4 mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-yellow-400">{condition.condition}</h3>
                  <p className="text-sm text-zinc-400">Diagnosed: {condition.diagnosedDate}</p>
                  <p className="text-sm mt-1">{condition.description}</p>
                </div>
                <span className="bg-green-900 text-green-300 px-2 py-1 rounded text-xs">
                  {condition.status}
                </span>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Past Medical History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Calendar className="h-5 w-5 text-blue-400" />
            <h2 className="text-xl font-semibold">Past Medical History</h2>
          </div>
          {medicalHistory.pastMedicalHistory.map((item, index) => (
            <div key={index} className="border-l-4 border-blue-500 pl-4 mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-blue-400">{item.condition}</h3>
                  <p className="text-sm text-zinc-400">
                    {item.date || `${item.diagnosedDate} - ${item.resolvedDate}`}
                  </p>
                  <p className="text-sm mt-1">{item.description}</p>
                </div>
                <span className="bg-zinc-700 text-zinc-300 px-2 py-1 rounded text-xs">
                  {item.status}
                </span>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Current Medications */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Pill className="h-5 w-5 text-green-400" />
            <h2 className="text-xl font-semibold">Current Medications</h2>
          </div>
          {medicalHistory.currentMedications.map((med, index) => (
            <div key={index} className="border-l-4 border-green-500 pl-4 mb-4">
              <h3 className="font-semibold text-green-400">{med.medication}</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mt-2 text-sm">
                <div>
                  <span className="text-zinc-400">Dosage: </span>
                  <span>{med.dosage}</span>
                </div>
                <div>
                  <span className="text-zinc-400">Frequency: </span>
                  <span>{med.frequency}</span>
                </div>
                <div>
                  <span className="text-zinc-400">For: </span>
                  <span>{med.indication}</span>
                </div>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Allergies */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <AlertTriangle className="h-5 w-5 text-orange-400" />
            <h2 className="text-xl font-semibold">Allergies & Reactions</h2>
          </div>
          {medicalHistory.allergies.map((allergy, index) => (
            <div key={index} className="border-l-4 border-orange-500 pl-4 mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-orange-400">{allergy.allergen}</h3>
                  <p className="text-sm text-zinc-400">First occurred: {allergy.firstOccurrence}</p>
                  <p className="text-sm mt-1">{allergy.reaction}</p>
                </div>
                <span className="bg-orange-900 text-orange-300 px-2 py-1 rounded text-xs">
                  {allergy.severity}
                </span>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Family History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <Users className="h-5 w-5 text-purple-400" />
            <h2 className="text-xl font-semibold">Family Medical History</h2>
          </div>
          {medicalHistory.familyHistory.map((family, index) => (
            <div key={index} className="border-l-4 border-purple-500 pl-4 mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-purple-400">{family.relation}</h3>
                  <p className="text-sm text-zinc-400">Condition: {family.condition}</p>
                  <p className="text-sm text-zinc-400">Age of onset: {family.ageOfOnset} years</p>
                </div>
                <span className="bg-purple-900 text-purple-300 px-2 py-1 rounded text-xs">
                  {family.status}
                </span>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Social History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <h2 className="text-xl font-semibold mb-4">Social History</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-zinc-400 text-sm">Occupation</p>
              <p className="font-medium">{medicalHistory.socialHistory.occupation}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Education</p>
              <p className="font-medium">{medicalHistory.socialHistory.education}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Smoking Status</p>
              <p className="font-medium">{medicalHistory.socialHistory.smokingStatus}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Alcohol Use</p>
              <p className="font-medium">{medicalHistory.socialHistory.alcoholUse}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Exercise</p>
              <p className="font-medium">{medicalHistory.socialHistory.exercise}</p>
            </div>
            <div>
              <p className="text-zinc-400 text-sm">Diet</p>
              <p className="font-medium">{medicalHistory.socialHistory.diet}</p>
            </div>
          </div>
        </motion.div>

        {/* Recent Visits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-zinc-900 rounded-lg p-6 mb-6"
        >
          <h2 className="text-xl font-semibold mb-4">Recent Medical Visits</h2>
          {medicalHistory.recentVisits.map((visit, index) => (
            <div key={index} className="border-l-4 border-cyan-500 pl-4 mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-cyan-400">{visit.type}</h3>
                  <p className="text-sm text-zinc-400">Date: {visit.date}</p>
                  <p className="text-sm text-zinc-400">Provider: {visit.provider}</p>
                  <p className="text-sm mt-1">{visit.findings}</p>
                  <p className="text-sm text-zinc-500">Follow-up: {visit.followUp}</p>
                </div>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Emergency Contact */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-red-900/20 border border-red-800 rounded-lg p-6"
        >
          <h2 className="text-xl font-semibold mb-2 text-red-400">Emergency Contact</h2>
          <p className="text-lg">{medicalHistory.personalHistory.emergencyContact}</p>
        </motion.div>
      </div>
    </div>
  )
}