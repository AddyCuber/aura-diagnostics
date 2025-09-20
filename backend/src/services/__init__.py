"""
AURA Diagnostics - Services Package

This package contains all the external service integrations.
Each service gets its own file to keep things organized and testable.

Current services:
- pubmed_service: Handles research article retrieval from PubMed
- More services will be added as we integrate with other APIs

Why separate services? External APIs change, have different authentication,
and different error handling needs. Keeping them separate makes the system
more maintainable and easier to mock for testing.
"""

# Import all services for easy access
from . import pubmed_service

__all__ = ["pubmed_service"]