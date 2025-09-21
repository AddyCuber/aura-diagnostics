"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download, FileText, Share } from "lucide-react"

interface DiagnosticData {
  diagnosis_id: string
  patient_id: number
  symptoms_text: string
  medical_analysis?: {
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
  }
  patient_history?: {
    name?: string
    age?: string | number
    gender?: string
    medical_conditions?: string[]
    medications?: string[]
    allergies?: string[]
    family_history?: string[]
  }
  timestamp?: string
}

interface DiagnosticReportProps {
  data: DiagnosticData
  onBack: () => void
  onShowMedicalHistory: () => void
}

const handleDownloadPDF = () => {
  const link = document.createElement('a')
  link.href = '/Patient_Report_Daughter_of_Darsh_Iyer.pdf'
  link.download = 'Patient_Report_Daughter_of_Darsh_Iyer.pdf'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export function DiagnosticReport({ data, onBack, onShowMedicalHistory }: DiagnosticReportProps) {
  return (
    <div className="fixed inset-0 z-50 min-h-screen bg-black text-white overflow-auto">
      {/* Header */}
      <div className="bg-zinc-900 border-b border-zinc-800 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button onClick={onBack} variant="ghost" size="sm" className="text-white hover:bg-zinc-800">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <h1 className="text-xl font-semibold">Medical Diagnostic Report</h1>
          </div>
          <div className="flex items-center space-x-2">
            <Button onClick={handleDownloadPDF} variant="ghost" size="sm" className="text-white hover:bg-zinc-800">
              <Download className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="text-white hover:bg-zinc-800">
              <FileText className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="text-white hover:bg-zinc-800">
              <Share className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto p-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          {/* Patient Header */}
          <div className="bg-zinc-900 rounded-lg p-6 border border-zinc-800">
            <h2 className="text-2xl font-bold mb-4 text-[#BA9465]">Patient Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-zinc-400">Patient Name</p>
                <p className="text-lg font-semibold">{data.patient_history?.name || "Daughter of Darsh Iyer"}</p>
              </div>
              <div>
                <p className="text-sm text-zinc-400">Age</p>
                <p className="text-lg font-semibold">{data.patient_history?.age || "Unknown"}</p>
              </div>
            </div>
          </div>

          {/* Detailed Clinical Analysis */}
          <div className="bg-zinc-900 rounded-lg p-6 border border-zinc-800">
            <h2 className="text-2xl font-bold mb-6 text-[#BA9465] border-b border-zinc-700 pb-2">
              Detailed Clinical Analysis
            </h2>

            {/* Presentation */}
            {data.medical_analysis?.presentation && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Presentation (as described)
                </h3>
                <ul className="space-y-2">
                  {data.medical_analysis.presentation.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Primary Diagnosis */}
            {data.medical_analysis?.primary_diagnosis && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Possible Diagnosis(es) & Differential Diagnoses
                </h3>
                <p className="text-zinc-300 mb-4">
                  Based on the symptoms, a leading possibility is infection with{" "}
                  <span className="font-semibold text-[#BA9465]">{data.medical_analysis.primary_diagnosis}</span>.
                  Key supporting features are:
                </p>
                
                {data.medical_analysis?.supporting_features && (
                  <ul className="space-y-2 mb-6">
                    {data.medical_analysis.supporting_features.map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-[#BA9465] mr-3 mt-1">•</span>
                        <span className="text-zinc-300">{feature}</span>
                      </li>
                    ))}
                  </ul>
                )}

                {data.medical_analysis?.differential_diagnoses && (
                  <div>
                    <p className="text-zinc-300 mb-3">Other differential diagnoses to consider:</p>
                    <ol className="space-y-2">
                      {data.medical_analysis.differential_diagnoses.map((diagnosis, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-[#BA9465] mr-3 mt-1">{index + 1}.</span>
                          <span className="text-zinc-300">{diagnosis}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            )}

            {/* Pathophysiology */}
            {data.medical_analysis?.pathophysiology && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Pathophysiology of Parvovirus B19 (relevant to these symptoms)
                </h3>
                <ul className="space-y-2">
                  {data.medical_analysis.pathophysiology.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Consistency Analysis */}
            {data.medical_analysis?.consistency_analysis && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Consistency Between Case & Parvovirus B19
                </h3>
                <p className="text-zinc-300 mb-4">The symptoms you describe are quite consistent with parvovirus B19 infection:</p>
                <ul className="space-y-2">
                  {data.medical_analysis.consistency_analysis.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommended Tests */}
            {data.medical_analysis?.recommended_tests && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Lab / Tests That Could Help Confirm
                </h3>
                <p className="text-zinc-300 mb-4">To be more certain, following evaluations might be useful:</p>
                <ul className="space-y-2">
                  {data.medical_analysis.recommended_tests.map((test, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{test}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Management */}
            {data.medical_analysis?.management && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Management & Treatment
                </h3>
                <p className="text-zinc-300 mb-4">Assuming parvovirus B19 is the cause, general management is usually supportive:</p>
                <ul className="space-y-2">
                  {data.medical_analysis.management.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Red Flags */}
            {data.medical_analysis?.red_flags && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  When to Seek Medical Care / Red Flags
                </h3>
                <p className="text-zinc-300 mb-4">Some signs that warrant medical attention:</p>
                <ul className="space-y-2">
                  {data.medical_analysis.red_flags.map((flag, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{flag}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Prognosis */}
            {data.medical_analysis?.prognosis && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Prognosis
                </h3>
                <ul className="space-y-2">
                  {data.medical_analysis.prognosis.map((item, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">•</span>
                      <span className="text-zinc-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Next Steps */}
            {data.medical_analysis?.next_steps && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Suggested Next Steps
                </h3>
                <ol className="space-y-2">
                  {data.medical_analysis.next_steps.map((step, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-[#BA9465] mr-3 mt-1">{index + 1}.</span>
                      <span className="text-zinc-300">{step}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {/* Conclusion */}
            {data.medical_analysis?.conclusion && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-zinc-200 border-b border-zinc-700 pb-2">
                  Conclusion
                </h3>
                <p className="text-zinc-300 leading-relaxed">{data.medical_analysis.conclusion}</p>
              </div>
            )}
          </div>

          {/* Disclaimer */}
          <div className="bg-zinc-900 rounded-lg p-6 border border-zinc-800 border-l-4 border-l-yellow-500">
            <p className="text-sm text-zinc-400">
              <strong className="text-yellow-500">Medical Disclaimer:</strong> This analysis is for informational purposes only and should not replace professional medical advice. 
              Please consult with a qualified healthcare provider for proper diagnosis and treatment.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}