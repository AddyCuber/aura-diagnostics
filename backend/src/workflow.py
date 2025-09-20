# backend/src/workflow.py
"""
AURA Diagnostics - Asynchronous Multi-Agent Workflow (Dev Mode)

This version is adjusted to work with mock services, allowing for
independent development while other components are being built.
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json
import os
import traceback
import asyncio
import concurrent.futures

# Compatibility function for Python 3.8
def to_thread(func, *args, **kwargs):
    """Compatibility wrapper for asyncio.to_thread (Python 3.9+)"""
    loop = asyncio.get_event_loop()
    # Use partial to handle keyword arguments properly
    from functools import partial
    if kwargs:
        func = partial(func, **kwargs)
    return loop.run_in_executor(None, func, *args)
from openai import OpenAI
# ChromaDB import with fallback for compatibility
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except (ImportError, RuntimeError) as e:
    print(f"ChromaDB not available: {e}")
    CHROMADB_AVAILABLE = False
    chromadb = None

# Ensure we can import from parent directories
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import ehr_agent
from src.services.pubmed_service import PubMedService
from src.services.drug_service import DrugService
from src.prompts import DiagnosticPrompts
from src.audit_logger import log_step

@dataclass
class DiagnosticState:
    """State container that flows through our workflow."""
    diagnosis_id: str
    patient_id: int
    symptoms_text: str
    structured_symptoms: Optional[Dict[str, Any]] = None
    patient_details: Optional[Dict[str, Any]] = None
    literature_evidence: str = "No relevant literature found."
    case_database_evidence: str = "No similar cases found."
    critique_notes: Optional[Dict[str, Any]] = None  # NEW: Critique Agent results
    final_report: Optional[str] = None
    drug_interaction_warnings: Optional[list] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class OrchestratorWorkflow:
    """Coordinates the full diagnostic pipeline using an async, state-passing model."""

    def __init__(self):
        """Initialize all necessary clients and services."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
        self.pubmed_service = PubMedService()
        self.drug_service = DrugService()
        
        # Initialize ChromaDB only if available
        if CHROMADB_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        else:
            self.chroma_client = None
            print("⚠️  ChromaDB unavailable - case database search will be disabled")
            
        self.prompts = DiagnosticPrompts()
        print("🤖 OrchestratorWorkflow initialized - ready to diagnose!")
        print("⚠️  Orchestrator is running in DEV mode with some services mocked.")

    async def run(self, diagnosis_id: str, patient_id: int, symptoms_text: str) -> Dict[str, Any]:
        """Runs the complete, sequential diagnostic workflow."""
        state = DiagnosticState(diagnosis_id=diagnosis_id, patient_id=patient_id, symptoms_text=symptoms_text)
        log_step(state.diagnosis_id, "Orchestrator", "START", f"Workflow initiated for patient {patient_id}.")

        try:
            # The main sequence of agent steps
            state.structured_symptoms = await self._safe_step(state, "SymptomAnalyzer", self._analyze_symptoms)
            state.patient_details = await self._safe_step(state, "EHR_Fetcher", self._fetch_ehr_data)
            state.literature_evidence = await self._safe_step(state, "LitSearcher", self._search_literature)
            
            # --- TEMPORARILY DISABLED ---
            # The CaseSearcher is disabled until the ChromaDB collection is ready.
            log_step(state.diagnosis_id, "CaseSearcher", "SKIPPED", "Case database not yet available.")
            state.case_database_evidence = "No similar cases found - case database temporarily disabled."
            # ----------------------------
            
            # --- NEW SUPERVISOR STEP ---
            state.critique_notes = await self._safe_step(state, "CritiqueAgent", self._critique_evidence)
            # ---------------------------
            
            state.final_report = await self._safe_step(state, "ReportSynthesizer", self._synthesize_report)
            state = await self._safe_step(state, "DrugChecker", self._check_drug_interactions, is_state_modifier=True)

            log_step(diagnosis_id, "Orchestrator", "END", "Workflow completed successfully.")
            return state.to_dict()

        except Exception as e:
            # This top-level catch handles failures raised by _safe_step
            err_trace = traceback.format_exc()
            log_step(diagnosis_id, "Orchestrator", "FATAL_ERROR", err_trace, status="FAILURE")
            # The error message is already set in the state by _safe_step
            return state.to_dict()

    async def _safe_step(self, state: DiagnosticState, step_name: str, func, is_state_modifier: bool = False):
        """Wrapper for each step to handle logging and exceptions."""
        try_details = f"Input state for {step_name} received."
        log_step(state.diagnosis_id, step_name, "START", try_details)
        try:
            result = await func(state)
            log_step(state.diagnosis_id, step_name, "END", f"Step completed successfully.")
            return result
        except Exception as e:
            err_trace = traceback.format_exc()
            state.error_message = f"Error in step '{step_name}': {str(e)}"
            log_step(state.diagnosis_id, step_name, "ERROR", err_trace, status="FAILURE")
            raise  # Re-raise the exception to be caught by the main run method

    # --- Agent Implementations ---

    async def _analyze_symptoms(self, state: DiagnosticState) -> Dict[str, Any]:
        """Agent 1: Extracts structured symptoms from raw text."""
        response = await to_thread(
            self.client.chat.completions.create,
            model="gpt-4o-mini", temperature=0.1,
            messages=[
                {"role": "system", "content": self.prompts.SYMPTOM_ANALYZER_SYSTEM},
                {"role": "user", "content": self.prompts.symptom_analyzer_user(state.symptoms_text)}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    async def _fetch_ehr_data(self, state: DiagnosticState) -> Dict[str, Any]:
        """Agent 2: Gets patient details from the database."""
        details = await to_thread(ehr_agent.get_patient_details, state.patient_id)
        if details is None:
            raise ValueError(f"Patient with ID {state.patient_id} not found.")
        return details

    async def _search_literature(self, state: DiagnosticState) -> str:
        """Agent 3: Finds relevant medical research on PubMed."""
        symptoms = [s.get('name', '') for s in state.structured_symptoms.get('symptoms', []) if s.get('name')]
        if not symptoms: return "No structured symptoms to search."
        
        # Build a differential diagnosis query - this tells PubMed we want articles 
        # that discuss how to tell the difference between various conditions
        symptom_list = ' and '.join(symptoms)
        query = f"differential diagnosis for pediatric {symptom_list}"
        pmids = await to_thread(self.pubmed_service.search, query, max_results=5)
        if not pmids: return "No relevant articles found on PubMed."
        
        abstracts_data = await to_thread(self.pubmed_service.fetch_abstracts, pmids[:3])
        if not abstracts_data: return "Could not fetch abstracts for found articles."
        
        abstract_texts = [f"Title: {a.get('title', 'N/A')}\nAbstract: {a.get('abstract', 'N/A')}" for a in abstracts_data]
        return "\n\n---\n\n".join(abstract_texts)

    async def _search_case_database(self, state: DiagnosticState) -> str:
        """Agent 4: Finds similar cases in our local DB."""
        # Check if ChromaDB is available
        if not CHROMADB_AVAILABLE or self.chroma_client is None:
            return "Case database search unavailable - ChromaDB not installed or compatible."
            
        symptoms = [s.get('name', '') for s in state.structured_symptoms.get('symptoms', []) if s.get('name')]
        if not symptoms: return "No structured symptoms to search."
        
        try:
            query = f"A case involving a {state.patient_details.get('age')} year old with {' and '.join(symptoms)}"
            collection = self.chroma_client.get_collection(name="medical_cases")
            results = await to_thread(collection.query, query_texts=[query], n_results=2)
            
            if not results or not results['documents'][0]: return "No similar cases found in the database."
            
            case_texts = [f"Case Title: {meta.get('title', 'N/A')}\nSummary: {doc}" for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
            return "\n\n---\n\n".join(case_texts)
        except Exception as e:
            return f"Case database search failed: {str(e)}"

    async def _synthesize_report(self, state: DiagnosticState) -> str:
        """Agent 5: Generates the main report from all evidence."""
        prompt = self.prompts.synthesis_report_user(state.to_dict())
        response = await to_thread(
            self.client.chat.completions.create,
            model="gpt-4o", temperature=0.2,
            messages=[
                {"role": "system", "content": self.prompts.SYNTHESIS_REPORT_SYSTEM},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    async def _check_drug_interactions(self, state: DiagnosticState) -> DiagnosticState:
        """Agent 6: A final safety check for drug interactions."""
        # This is a synchronous function, so we don't need to wrap it in to_thread
        potential_conditions = []
        if "Potential Considerations" in state.final_report:
            considerations_section = state.final_report.split("Potential Considerations")[1]
            lines = considerations_section.split('\n')
            for line in lines:
                if line.strip().startswith('*'):
                    potential_conditions.append(line.strip().lstrip('* ').strip())
        
        if potential_conditions:
            interaction_results = self.drug_service.check_interactions(
                potential_conditions=potential_conditions,
                patient_history=state.patient_details.get('medical_history', '')
            )
            if interaction_results.get("warnings"):
                state.drug_interaction_warnings = interaction_results["warnings"]
                state.final_report += "\n\n## 🚨 Safety Warnings\n\n" + "\n".join([f"- {w}" for w in interaction_results["warnings"]])
        return state

    async def _critique_evidence(self, state: DiagnosticState) -> Dict[str, Any]:
        """Agent 5: Critically reviews all gathered evidence for gaps and inconsistencies."""
        # Hey future dev - this is where we get skeptical about our evidence quality!
        # The AI acts like a senior clinician double-checking our work before we write the final report.
        # If this breaks, check that the prompts.py has the CRITIQUE_AGENT_SYSTEM prompt defined.
        prompt = self.prompts.critique_agent_user(state.to_dict())
        response = await to_thread(
            self.client.chat.completions.create,
            model="gpt-4o-mini", temperature=0.1,
            messages=[
                {"role": "system", "content": self.prompts.CRITIQUE_AGENT_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
