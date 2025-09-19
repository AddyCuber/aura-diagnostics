# aura-diagnostics
A multi-agent AI workflow for transparent and auditable patient diagnostics

# AURA Diagnostics 🩺

AURA (Agent-Unified Response & Analysis) is a multi-agent AI ecosystem designed to assist medical professionals by providing fast, evidence-backed, and fully traceable diagnostic suggestions.

---
## ✨ Core Features

* **Multi-Agent Collaboration:** A central Orchestrator agent manages a team of specialized agents for symptom analysis, literature review, and case history lookup.
* **Evidence Packet:** The final output isn't just a suggestion, but a full report detailing the evidence found by each agent.
* **Audit Trail:** A fully traceable log of the AI's entire workflow, ensuring complete transparency for doctors.
* **Dual Portals:** Separate, user-friendly interfaces for both doctors and patients.

---
## 🛠️ Tech Stack

* **Frontend:** React (Vite)
* **Backend:** FastAPI (Python)
* **AI Core:** LangGraph
* **Database:** SQLite & ChromaDB

---
## 🚀 Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
