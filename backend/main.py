"""
AURA Diagnostics - Main FastAPI Application

This is the entry point for our multi-agent AI diagnostic system.
Now powered by LangGraph for orchestrating our AI agents in a clean workflow.

Why FastAPI? It's async by default, has automatic API docs, and plays nice with Pydantic.
Perfect for our AI agents that'll be making lots of concurrent API calls.

The main magic happens in /api/diagnose - that's where our LangGraph workflow
takes patient symptoms and runs them through our four specialized agents.
"""

import uuid
import time
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agents import ehr_agent
from src.workflow import OrchestratorWorkflow  # Our new LangGraph workflow
from src.models import DiagnosisRequest, DiagnosisResponse  # Pydantic models
from dotenv import load_dotenv

# Load environment variables from .env file
# This gets our OpenAI API key and other secrets
load_dotenv()

# Configure logging for production-ready audit trails
logger = logging.getLogger("diagnosis")
logger.setLevel(logging.INFO)

app = FastAPI(
    title="AURA Diagnostics API",
    description="Multi-agent AI workflow for transparent and auditable patient diagnostics",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow after environment variables are loaded
workflow = OrchestratorWorkflow()

# Remove the old DiagnosisRequest model since we now import it from models.py

@app.get("/")
async def root():
    """
    Basic health check endpoint.
    
    Returns a simple message to confirm the API is running.
    This will be our first test to make sure FastAPI is working properly.
    """
    return {"message": "AURA Diagnostics API is running 🩺"}

# New main endpoint to run the diagnostic workflow
# This is where the magic happens - our LangGraph workflow orchestrates everything
@app.post("/api/diagnose", response_model=DiagnosisResponse)
async def run_diagnosis(request: DiagnosisRequest) -> JSONResponse:
    """
    Run the full diagnostic workflow given patient symptoms.
    
    Generates a traceable diagnosis_id for monitoring.
    Returns structured results or a clear error response.
    """
    diagnosis_id = f"diag_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    logger.info(f"[{diagnosis_id}] Starting diagnosis for patient_id={request.patient_id}")

    try:
        # OrchestratorWorkflow.run should be async-safe
        result = await workflow.run(
            diagnosis_id=diagnosis_id,
            patient_id=request.patient_id,
            symptoms_text=request.symptoms_text
        )

        if not result:
            logger.error(f"[{diagnosis_id}] Empty result from workflow")
            raise HTTPException(status_code=502, detail="Workflow returned no result.")

        if result.get("error_message"):
            logger.warning(f"[{diagnosis_id}] Workflow error: {result['error_message']}")
            raise HTTPException(status_code=400, detail=result["error_message"])

        # Add diagnosis_id and timestamp to the result
        result["diagnosis_id"] = diagnosis_id
        result["timestamp"] = datetime.now().isoformat()

        logger.info(f"[{diagnosis_id}] Diagnosis completed successfully")
        return JSONResponse(content=result)

    except HTTPException:
        raise  # re-raise FastAPI handled exceptions

    except Exception as e:
        logger.exception(f"[{diagnosis_id}] Unexpected error during diagnosis")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """
    More detailed health check for monitoring.
    
    Later we can add database connectivity checks, AI model status, etc.
    For now, just confirming the service is up and our workflow is ready.
    """
    return {
        "status": "healthy",
        "service": "AURA Diagnostics API",
        "components": {
            "api": "operational",
            "workflow": "ready",      # Our LangGraph workflow is initialized
            "database": "operational", # EHR agent can connect to SQLite
            "ai_agents": "ready"      # All four agents are ready to go
        }
    }

# Existing endpoints for direct EHR access
# These are useful for testing and for the frontend to browse patients
@app.get("/api/patients/{patient_id}")
async def read_patient(patient_id: int):
    """
    Get details for a specific patient.
    
    This endpoint connects to our EHR agent to fetch patient data from the database.
    Returns 404 if the patient doesn't exist.
    
    Args:
        patient_id: The ID of the patient to retrieve
        
    Returns:
        Patient data including medical history and current symptoms
    """
    patient_details = ehr_agent.get_patient_details(patient_id)
    
    if patient_details is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Patient with ID {patient_id} not found"
        )
    
    return patient_details

@app.get("/api/patients")
async def list_patients():
    """
    Get a list of all patients.
    
    Useful for testing and for the frontend to show available patients.
    In a real system, this would have pagination and filtering.
    """
    patients = ehr_agent.get_all_patients()
    return {
        "patients": patients,
        "count": len(patients)
    }

# This runs when you start the server with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    # Run the server on localhost:8000
    # --reload makes it restart when you change code (great for development)
    uvicorn.run(app, host="0.0.0.0", port=8000)