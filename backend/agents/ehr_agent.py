"""
AURA Diagnostics - EHR Agent

This agent handles all interactions with our patient database.
Think of it as the "medical records clerk" of our AI system.

Why separate this? Because database logic should be isolated from other concerns.
If we need to switch databases or change how we store patient data, 
we only need to update this one file.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional, Dict, Any, List
import sys
import os

# Add the parent directory to the path so we can import from setup_db
# This is a bit hacky but works for our simple setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setup_db import Patient

# Database connection setup
# We're using the same database file that setup_db.py creates
DATABASE_URL = "sqlite:///aura.db"

def get_database_session():
    """
    Create a database session for querying.
    
    We create a new session each time instead of keeping one open
    because SQLite can be finicky with concurrent access.
    """
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_patient_details(patient_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch patient details from the database.
    
    Args:
        patient_id: The ID of the patient to look up
        
    Returns:
        Dictionary with patient data, or None if patient not found
        
    Why return a dict? It's easier to serialize to JSON for our API,
    and it decouples the API from our database models.
    """
    session = get_database_session()
    
    try:
        # Query the patient by ID
        patient = session.query(Patient).filter(Patient.id == patient_id).first()
        
        if not patient:
            return None
            
        # Convert the SQLAlchemy model to a dictionary
        # This makes it easy to return as JSON from our API
        patient_dict = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "medical_history": patient.medical_history,
            "current_symptoms": patient.current_symptoms,
            "created_at": patient.created_at.isoformat() if patient.created_at else None,
            "updated_at": patient.updated_at.isoformat() if patient.updated_at else None
        }
        
        return patient_dict
        
    except Exception as e:
        # In a real system, you'd want proper logging here
        print(f"Error fetching patient {patient_id}: {str(e)}")
        return None
        
    finally:
        # Always close the session to prevent connection leaks
        session.close()

def get_all_patients() -> List[Dict[str, Any]]:
    """
    Fetch all patients from the database.
    
    Useful for testing and for agents that need to see the full patient list.
    In a real system, you'd want pagination here.
    """
    session = get_database_session()
    
    try:
        patients = session.query(Patient).all()
        
        # Convert all patients to dictionaries
        patients_list = []
        for patient in patients:
            patient_dict = {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender,
                "medical_history": patient.medical_history,
                "current_symptoms": patient.current_symptoms,
                "created_at": patient.created_at.isoformat() if patient.created_at else None,
                "updated_at": patient.updated_at.isoformat() if patient.updated_at else None
            }
            patients_list.append(patient_dict)
            
        return patients_list
        
    except Exception as e:
        print(f"Error fetching all patients: {str(e)}")
        return []
        
    finally:
        session.close()