"""
AURA Diagnostics - Database Setup Script

This script creates our SQLite database with the core tables we need:
- patients: Store patient information and medical history
- audit_log: Track every action our AI agents take for full transparency

Why SQLite? It's perfect for development and small deployments. No server needed,
just a file on disk. Easy to backup, version control, and debug.

Run this script once to set up your database: python setup_db.py
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create the base class for our database models
Base = declarative_base()

class Patient(Base):
    """
    Patient information table.
    
    Stores basic patient data and medical history.
    In a real system, this would be much more complex with proper medical record standards.
    """
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    
    # Medical history as JSON-like text for simplicity
    # In production, you'd want proper normalized tables for conditions, medications, etc.
    medical_history = Column(Text, nullable=True)
    current_symptoms = Column(Text, nullable=True)
    
    # Timestamps for tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    """
    Audit trail for AI agent actions.
    
    Every time an AI agent does something, we log it here.
    This gives doctors full transparency into how the AI reached its conclusions.
    """
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # --- THIS IS THE NEW, CRITICAL FIELD ---
    # Each diagnostic session gets a unique ID like "diag_1758379433_a84753ed"
    # This lets us track all the steps that happened during one diagnosis
    diagnosis_id = Column(String(50), nullable=False, index=True)
    # ------------------------------------
    
    patient_id = Column(Integer, nullable=True)  # Which patient this relates to
    agent_name = Column(String(50), nullable=False)  # Which AI agent performed the action
    action_type = Column(String(50), nullable=False)  # What type of action (analyze, search, etc.)
    
    # The actual content of what the agent did
    input_data = Column(Text, nullable=True)  # What the agent received
    output_data = Column(Text, nullable=True)  # What the agent produced
    
    # Metadata
    confidence_score = Column(Float, nullable=True)  # How confident the agent was
    processing_time = Column(Float, nullable=True)  # How long it took
    success = Column(Boolean, default=True)  # Did the action succeed?
    error_message = Column(Text, nullable=True)  # If it failed, why?
    
    timestamp = Column(DateTime, default=datetime.utcnow)

def create_database():
    """
    Create the database file and all tables.
    
    This will create aura.db in the current directory.
    If the file already exists, it won't overwrite existing data.
    """
    # Create SQLite database file
    database_url = "sqlite:///aura.db"
    engine = create_engine(database_url, echo=True)  # echo=True shows SQL queries
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    return engine

def add_sample_patients(engine):
    """
    Add some fake patients for testing.
    
    In a real system, patient data would come from hospital systems.
    These are just for development and testing our AI agents.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    # Sample patients with different medical scenarios
    sample_patients = [
        Patient(
            name="Alice Johnson",
            age=8,
            gender="Female",
            medical_history="No significant past medical history. Up to date on vaccinations.",
            current_symptoms="Fever (101.5°F), cough for 3 days, runny nose, decreased appetite. Mother reports child seems tired and fussy."
        ),
        Patient(
            name="Bobby Chen",
            age=12,
            gender="Male",
            medical_history="Mild asthma, uses albuterol inhaler as needed. No recent hospitalizations.",
            current_symptoms="Wheezing, shortness of breath after playing soccer. Used inhaler twice today with minimal relief."
        ),
        Patient(
            name="Maria Rodriguez",
            age=5,
            gender="Female",
            medical_history="Born at 36 weeks, no complications. Normal development milestones.",
            current_symptoms="Ear pain, pulling at right ear, low-grade fever (100.2°F), irritability especially when lying down."
        )
    ]
    
    # Add patients to database
    for patient in sample_patients:
        session.add(patient)
    
    # Commit the changes
    session.commit()
    session.close()
    
    print(f"Added {len(sample_patients)} sample patients to the database.")

def main():
    """
    Main function to set up the database.
    
    Creates tables and adds sample data.
    """
    print("Setting up AURA Diagnostics database...")
    
    # Create database and tables
    engine = create_database()
    print("✅ Database tables created successfully!")
    
    # Add sample patients
    add_sample_patients(engine)
    print("✅ Sample patients added successfully!")
    
    print("\nDatabase setup complete! 🗃️")
    print("Database file: aura.db")
    print("You can now run the FastAPI server with: uvicorn main:app --reload")

if __name__ == "__main__":
    main()