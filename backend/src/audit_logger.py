"""
AURA Diagnostics - Audit Logger

This module provides comprehensive logging for each step of the diagnostic workflow.
It creates a detailed audit trail that helps with debugging, monitoring, and compliance.

Why we need this:
- Track every step of the diagnostic process for debugging
- Create audit trails for medical compliance
- Monitor performance and identify bottlenecks
- Provide detailed error context when things go wrong
"""

import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any

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
    step_name: str, 
    action: str, 
    details: str, 
    status: str = "SUCCESS",
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a single step in the diagnostic workflow.
    
    This creates a structured log entry that can be easily parsed and analyzed.
    Each log entry includes the diagnosis_id so we can trace the entire workflow.
    
    Args:
        diagnosis_id: Unique ID for this diagnostic run
        step_name: Name of the agent/step (e.g., "SymptomAnalyzer", "EHR_Fetcher")
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
        "step_name": step_name,
        "action": action,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    # Format the log message for easy reading
    # The JSON part makes it easy to parse programmatically later
    message = f"[{diagnosis_id}] {step_name}.{action} | {status} | {details}"
    
    if status == "FAILURE":
        audit_logger.error(f"{message} | DATA: {json.dumps(log_entry)}")
    elif status == "WARNING":
        audit_logger.warning(f"{message} | DATA: {json.dumps(log_entry)}")
    else:
        audit_logger.info(f"{message} | DATA: {json.dumps(log_entry)}")

def log_performance(diagnosis_id: str, step_name: str, duration_ms: float, details: str = "") -> None:
    """
    Log performance metrics for a workflow step.
    
    This helps us identify slow steps and optimize the workflow.
    Medical AI needs to be fast - patients don't want to wait 5 minutes for a diagnosis.
    
    Args:
        diagnosis_id: Unique ID for this diagnostic run
        step_name: Name of the step that was timed
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
        step_name=step_name,
        action="PERFORMANCE",
        details=f"Step completed in {duration_ms:.2f}ms. {details}".strip(),
        status=status,
        metadata=metadata
    )