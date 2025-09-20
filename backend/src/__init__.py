"""
AURA Diagnostics - Source Package

This is the core of our diagnostic system. It contains:
- models.py: Data models and schemas for our application
- prompts.py: All the AI prompts used throughout the system
- workflow.py: The main diagnostic workflow orchestration
- services/: External service integrations (PubMed, etc.)

Why a src folder? It's a common Python pattern that separates
application code from configuration, tests, and other project files.
Makes imports cleaner and the project structure more professional.
"""

# Import core modules for easy access
from . import models
from . import prompts
from . import workflow

__all__ = ["models", "prompts", "workflow"]