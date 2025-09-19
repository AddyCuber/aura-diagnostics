"""
AURA Diagnostics - Main FastAPI Application

This is the entry point for our multi-agent AI diagnostic system.
Starting simple with a hello world to make sure everything's wired up correctly.

Why FastAPI? It's async by default, has automatic API docs, and plays nice with Pydantic.
Perfect for our AI agents that'll be making lots of concurrent API calls.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app instance
# We'll add more config here as we build out the system
app = FastAPI(
    title="AURA Diagnostics API",
    description="Multi-agent AI workflow for transparent and auditable patient diagnostics",
    version="1.0.0"
)

# Add CORS middleware so our React frontend can talk to us
# In production, you'd want to be more restrictive with origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    """
    Basic health check endpoint.
    
    Returns a simple message to confirm the API is running.
    This will be our first test to make sure FastAPI is working properly.
    """
    return {
        "message": "Hello from AURA Diagnostics! 🩺",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """
    More detailed health check for monitoring.
    
    Later we can add database connectivity checks, AI model status, etc.
    For now, just confirming the service is up.
    """
    return {
        "status": "healthy",
        "service": "AURA Diagnostics API",
        "components": {
            "api": "operational",
            "database": "pending",  # We'll update this once we set up SQLite
            "vector_db": "pending",  # We'll update this once ChromaDB is ready
            "ai_agents": "pending"   # We'll update this once agents are implemented
        }
    }

# This runs when you start the server with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    # Run the server on localhost:8000
    # --reload makes it restart when you change code (great for development)
    uvicorn.run(app, host="0.0.0.0", port=8000)