"""
AURA Diagnostics - Agents Package

This package contains all the AI agents that make up our diagnostic system.
Each agent has a specific role and responsibility in the workflow.

Current agents:
- ehr_agent: Handles patient data retrieval from the database
- More agents will be added as we build out the multi-agent system

Why separate agents? It follows the single responsibility principle.
Each agent does one thing well, making the system easier to test and maintain.
"""

# Import all agents so they can be accessed as agents.ehr_agent, etc.
from . import ehr_agent

__all__ = ["ehr_agent"]