#!/usr/bin/env python3
"""
AURA Diagnostics - OpenAI Powered Backend
Generates realistic medical diagnostic responses using OpenAI API
"""

import json
import uuid
import time
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_openai_response(prompt: str, patient_history: dict = None, max_tokens: int = 1500) -> dict:
    """Get structured medical response from OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Enhanced system prompt for structured medical responses
        system_prompt = """You are AURA, an advanced medical AI diagnostic assistant. Provide comprehensive, structured medical analysis in JSON format with the following structure:

{
  "diagnosis": {
    "primary": "Primary diagnosis with confidence level",
    "differential": ["List of differential diagnoses"],
    "confidence": "High/Medium/Low"
  },
  "assessment": {
    "symptoms_analysis": "Detailed symptom analysis",
    "risk_factors": ["Identified risk factors"],
    "severity": "Mild/Moderate/Severe"
  },
  "recommendations": {
    "immediate": ["Immediate actions needed"],
    "diagnostic_tests": ["Recommended tests"],
    "treatment": ["Treatment recommendations"],
    "follow_up": "Follow-up timeline"
  },
  "patient_context": {
    "relevant_history": "How patient history relates to current symptoms",
    "contraindications": ["Any contraindications based on history"]
  },
  "references": [
    {
      "title": "Relevant medical literature or guideline",
      "source": "Journal/Organization name",
      "year": "2023",
      "relevance": "How this reference supports the diagnosis"
    }
  ],
  "disclaimer": "Professional medical disclaimer"
}

Always provide realistic, evidence-based medical information. Include relevant references from medical literature."""
        
        # Include patient history in the prompt if available
        user_prompt = f"Patient Symptoms: {prompt}"
        if patient_history:
            user_prompt += f"\n\nPatient Medical History: {json.dumps(patient_history, indent=2)}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        # Try to parse JSON response
        try:
            return json.loads(response.choices[0].message.content.strip())
        except json.JSONDecodeError:
            # Fallback to structured text if JSON parsing fails
            return {
                "diagnosis": {
                    "primary": "Clinical assessment required",
                    "differential": ["Multiple conditions possible"],
                    "confidence": "Medium"
                },
                "assessment": {
                    "symptoms_analysis": response.choices[0].message.content.strip(),
                    "risk_factors": ["Patient history factors"],
                    "severity": "Moderate"
                },
                "recommendations": {
                    "immediate": ["Consult healthcare provider"],
                    "diagnostic_tests": ["Comprehensive evaluation"],
                    "treatment": ["Professional medical care"],
                    "follow_up": "As directed by physician"
                },
                "patient_context": {
                    "relevant_history": "Consider patient's medical background",
                    "contraindications": []
                },
                "references": [
                    {
                        "title": "Clinical Practice Guidelines",
                        "source": "Medical Association",
                        "year": "2023",
                        "relevance": "Evidence-based diagnostic approach"
                    }
                ],
                "disclaimer": "This analysis is for informational purposes only. Always consult qualified healthcare professionals for medical advice."
            }
            
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        # Return structured fallback
        return {
            "diagnosis": {
                "primary": "Professional evaluation needed",
                "differential": ["Multiple conditions possible"],
                "confidence": "Low"
            },
            "assessment": {
                "symptoms_analysis": "Comprehensive clinical assessment required for accurate diagnosis",
                "risk_factors": ["Individual patient factors"],
                "severity": "Unknown"
            },
            "recommendations": {
                "immediate": ["Schedule medical consultation"],
                "diagnostic_tests": ["Complete medical evaluation"],
                "treatment": ["Professional medical guidance"],
                "follow_up": "Regular monitoring as advised"
            },
            "patient_context": {
                "relevant_history": "Patient history review recommended",
                "contraindications": []
            },
            "references": [
                {
                    "title": "Standard Clinical Practice Guidelines",
                    "source": "Healthcare Standards Organization",
                    "year": "2023",
                    "relevance": "Evidence-based medical practice"
                }
            ],
            "disclaimer": "This is a fallback response. Please consult healthcare professionals for proper medical evaluation."
        }

class DiagnosticHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "AURA Diagnostics API - OpenAI Powered", "status": "healthy"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/diagnose':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                patient_id = request_data.get('patient_id')
                symptoms_text = request_data.get('symptoms_text')
                
                if not patient_id or not symptoms_text:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_response = {"error": "Missing patient_id or symptoms_text"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return
                
                diagnosis_id = f"diag_{int(time.time())}_{uuid.uuid4().hex[:8]}"
                print(f"Processing diagnosis {diagnosis_id} for patient {patient_id}")
                
                # Mock patient history data (in real system, this would come from database)
                patient_history = {
                    "age": 34,
                    "gender": "Female",
                    "medical_history": ["Hypertension", "Type 2 Diabetes"],
                    "current_medications": ["Lisinopril 10mg", "Metformin 500mg"],
                    "allergies": ["Penicillin", "Shellfish"],
                    "family_history": ["Heart disease (father)", "Diabetes (mother)"],
                    "social_history": "Non-smoker, occasional alcohol use",
                    "recent_vitals": {
                        "blood_pressure": "130/85",
                        "heart_rate": 78,
                        "temperature": 98.6,
                        "weight": "140 lbs",
                        "height": "5'6\""
                    }
                }
                
                # Get structured medical analysis from OpenAI
                medical_analysis = get_openai_response(symptoms_text, patient_history)
                
                # Structure the response with enhanced medical data
                response = {
                    "diagnosis_id": diagnosis_id,
                    "patient_id": patient_id,
                    "symptoms_text": symptoms_text,
                    "medical_analysis": medical_analysis,
                    "patient_history": patient_history,
                    "timestamp": datetime.now().isoformat(),
                    "error_message": None
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, indent=2).encode())
                
                print(f"Completed diagnosis {diagnosis_id} for patient {patient_id}")
                
            except Exception as e:
                print(f"Error processing diagnosis: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {
                    "error_message": f"Diagnostic processing error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, DiagnosticHandler)
    print(f"AURA Diagnostics OpenAI Backend running on http://localhost:8001")
    print(f"OpenAI API Key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    httpd.serve_forever()