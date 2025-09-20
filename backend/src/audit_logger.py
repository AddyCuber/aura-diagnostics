"""
AURA Diagnostics - Audit Logging Service

This module provides comprehensive logging for each step of the diagnostic workflow.
It creates a detailed audit trail using both file-based logging and SQLite database storage.

This is the core of our "glass box" transparency feature - we log everything
so doctors can see exactly how the AI reached its conclusions.

Why we need this:
- Track every step of the diagnostic process for debugging
- Create audit trails for medical compliance and legal requirements
- Monitor performance and identify bottlenecks
- Provide detailed error context when things go wrong
- Store structured data in database for analysis and reporting
"""

import logging
import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure we can import from the parent directory to get the DB models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from setup_db import AuditLog
    DATABASE_AVAILABLE = True
except ImportError:
    print("Warning: Could not import AuditLog model. Database logging disabled.")
    DATABASE_AVAILABLE = False

# Database setup - use the same central database as the rest of the application
DATABASE_URL = "sqlite:///aura.db"
if DATABASE_AVAILABLE:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the audit logger - this writes to both console and file
# We use a separate logger from the main app so audit logs don't get mixed up
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# Create file handler for persistent audit logs
# These logs are crucial for medical compliance, so we store them permanently
file_handler = logging.FileHandler("audit_trail.log")
file_handler.setLevel(logging.INFO)

# Create console handler for real-time monitoring during development
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format the logs with timestamp, diagnosis_id, and structured data
# This makes it easy to grep logs by diagnosis_id or step_name
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

audit_logger.addHandler(file_handler)
audit_logger.addHandler(console_handler)

def log_step(
    diagnosis_id: str, 
    agent_name: str, 
    action: str, 
    details: str, 
    status: str = "SUCCESS",
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a single step in the diagnostic workflow to both file and database.
    
    This creates a structured log entry that can be easily parsed and analyzed.
    Each log entry includes the diagnosis_id so we can trace the entire workflow.
    We store in both file (for easy reading) and database (for structured queries).
    
    Args:
        diagnosis_id: Unique ID for this diagnostic run
        agent_name: Name of the agent/step (e.g., "SymptomAnalyzer", "EHR_Fetcher")
        action: What's happening (e.g., "START", "END", "ERROR")
        details: Human-readable description of what happened
        status: SUCCESS, FAILURE, or WARNING
        metadata: Optional additional data (performance metrics, etc.)
    
    Example:
        log_step("diag_123_abc", "SymptomAnalyzer", "START", "Processing symptoms for patient 456")
    """
    
    # Create a structured log entry that's both human-readable and machine-parseable
    log_entry = {
        "diagnosis_id": diagnosis_id,
        "agent_name": agent_name,
        "action": action,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    # Format the log message for easy reading
    # The JSON part makes it easy to parse programmatically later
    message = f"[{diagnosis_id}] {agent_name}.{action} | {status} | {details}"
    
    # Log to file and console first (this always works)
    if status == "FAILURE":
        audit_logger.error(f"{message} | DATA: {json.dumps(log_entry)}")
    elif status == "WARNING":
        audit_logger.warning(f"{message} | DATA: {json.dumps(log_entry)}")
    else:
        audit_logger.info(f"{message} | DATA: {json.dumps(log_entry)}")
    
    # Also log to database if available (for structured queries and reporting)
    if DATABASE_AVAILABLE:
        _log_to_database(diagnosis_id, agent_name, action, details, status)

def _log_to_database(diagnosis_id: str, agent_name: str, action: str, details: str, status: str) -> None:
    """
    Internal function to log to the SQLite database.
    
    This is separate so we can gracefully handle database errors without
    breaking the main workflow. File logging will still work even if DB fails.
    """
    session = SessionLocal()
    try:
        # Create a new log entry using our SQLAlchemy model
        # Now we can properly use the diagnosis_id field!
        log_entry = AuditLog(
            diagnosis_id=diagnosis_id,
            patient_id=None,  # We don't have patient_id in our workflow yet
            agent_name=agent_name,
            action_type=action,
            output_data=details,  # Storing details in the more generic output_data field
            success=(status == "SUCCESS"),
            error_message=details if status == "FAILURE" else None
        )
        session.add(log_entry)
        session.commit()
    except Exception as e:
        # If database logging fails, we print an error but don't crash the main workflow
        # File logging will still work, so we don't lose the audit trail completely
        print(f"Warning: Could not write to audit database. Error: {e}")
        audit_logger.warning(f"Database logging failed: {e}")
    finally:
        # Always close the session to release the connection
        session.close()

def log_performance(diagnosis_id: str, agent_name: str, duration_ms: float, details: str = "") -> None:
    """
    Log performance metrics for a workflow step.
    
    This helps us identify slow steps and optimize the workflow.
    Medical AI needs to be fast - patients don't want to wait 5 minutes for a diagnosis.
    
    Args:
        diagnosis_id: Unique ID for this diagnostic run
        agent_name: Name of the step that was timed
        duration_ms: How long the step took in milliseconds
        details: Optional additional context
    """
    metadata = {
        "duration_ms": duration_ms,
        "performance_category": "timing"
    }
    
    # Flag slow steps as warnings so they're easy to spot
    status = "WARNING" if duration_ms > 5000 else "SUCCESS"  # 5 seconds threshold
    
    log_step(
        diagnosis_id=diagnosis_id,
        agent_name=agent_name,
        action="PERFORMANCE",
        details=f"Step completed in {duration_ms:.2f}ms. {details}".strip(),
        status=status,
        metadata=metadata
    )

# Convenience function for backward compatibility with existing code
def log_agent_step(diagnosis_id: str, agent_name: str, action: str, details: str, status: str = "SUCCESS") -> None:
    """
    Backward compatibility wrapper for log_step.
    
    Some existing code might use this function name, so we keep it as an alias.
    """
    log_step(diagnosis_id, agent_name, action, details, status)