"""
AURA Diagnostics - Data Models

This file contains all the data models and schemas used throughout the application.
We use Pydantic for data validation and serialization - it's fast, type-safe,
and plays nicely with FastAPI.

Why separate models? It gives us a single source of truth for data structures.
If we need to change how patient data looks, we change it here and everywhere
else automatically gets the update.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class StructuredSymptoms(BaseModel):
    """
    Structured representation of patient symptoms.
    
    Instead of just free text, this breaks symptoms down into structured data
    that our AI agents can work with more effectively. Each symptom gets
    qualifiers like severity, duration, triggers, etc.
    """
    symptoms: List[Dict[str, Any]] = Field(description="List of symptoms with their qualifiers")


class EHR_Findings(BaseModel):
    """
    What we extract from the EHR system for a patient.
    
    This is a cleaned-up version of the raw database data, formatted
    specifically for our diagnostic workflow. It's separate from the
    Patient model because this is what gets passed between agents.
    """
    patient_id: int
    name: str
    age: int
    gender: str
    medical_history: str


class LiteratureFindings(BaseModel):
    """
    Results from our literature search.
    
    This wraps the PubMed articles with additional metadata about
    the search process and relevance scoring. Helps us track what
    research was used in each diagnosis.
    """
    articles: List[Dict[str, Any]] = Field(description="List of relevant PubMed articles with summaries")


class DiagnosticState(BaseModel):
    """
    The full state of a single diagnostic session.
    
    This is the "memory" of our LangGraph workflow - it tracks everything that happens
    during a diagnosis from start to finish. Each node in the graph can read from and
    write to this state, making the whole process traceable and debuggable.
    
    Why track state like this? It lets us:
    1. Resume interrupted workflows
    2. Debug what went wrong at each step
    3. Audit our diagnostic process
    4. Cache intermediate results
    5. Show progress to users
    
    LangGraph will pass this state between all the nodes in our diagnostic workflow.
    """
    patient_id: int
    symptoms_text: str
    structured_symptoms: Optional[StructuredSymptoms] = None
    ehr_findings: Optional[EHR_Findings] = None
    lit_search_results: Optional[LiteratureFindings] = None
    final_report: Optional[Dict[str, Any]] = None
    
    # Keep track of errors at each step - LangGraph can use this for error handling
    error_message: Optional[str] = None


class DiagnosisRequest(BaseModel):
    """
    Request model for the diagnosis endpoint.
    
    This is what the frontend sends us when requesting a diagnosis.
    Pydantic will automatically validate the data types and required fields.
    """
    patient_id: int = Field(..., description="Unique identifier for the patient")
    symptoms_text: str = Field(..., min_length=1, description="Free-text description of patient symptoms")


class DiagnosisResponse(BaseModel):
    """
    Response model for the diagnosis endpoint.
    
    This defines the structure of our diagnostic results.
    Having a clear response model makes it easier for frontend devs
    to know exactly what they'll get back from our API.
    """
    diagnosis_id: str = Field(..., description="Unique identifier for this diagnosis session")
    patient_id: int = Field(..., description="Patient identifier")
    symptoms_text: str = Field(..., description="Original symptoms text")
    
    # Results from each agent in our workflow
    structured_symptoms: Optional[Dict[str, Any]] = Field(None, description="Parsed symptoms from Agent 1")
    patient_details: Optional[Dict[str, Any]] = Field(None, description="EHR data from Agent 2")
    literature_evidence: Optional[str] = Field(None, description="Research findings from Agent 3")
    final_report: Optional[str] = Field(None, description="Synthesized report from Agent 4")
    
    # Tracking and error handling
    timestamp: Optional[datetime] = Field(None, description="When this diagnosis was completed")
    error_message: Optional[str] = Field(None, description="Error message if diagnosis failed")
    
    class Config:
        """
        Pydantic config - tells it how to handle our model.
        
        json_encoders helps with datetime serialization.
        schema_extra provides example data for API docs.
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "diagnosis_id": "diag_1703123456_abc12345",
                "patient_id": 123,
                "symptoms_text": "Patient reports chest pain and shortness of breath",
                "structured_symptoms": {"chest_pain": {"severity": "moderate", "duration": "2_days"}},
                "patient_details": {"age": 45, "gender": "M", "medical_history": []},
                "literature_evidence": "Recent studies suggest...",
                "final_report": "Based on the analysis...",
                "timestamp": "2023-12-21T10:30:45.123456",
                "error_message": None
            }
        }