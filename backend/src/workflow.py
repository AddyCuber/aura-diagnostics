# backend/src/workflow.py
"""
AURA Diagnostics - Final Asynchronous Multi-Agent Workflow

This orchestrator runs a sequence of specialized agents to produce an
evidence-backed, safety-checked diagnostic report. This version includes
an enhanced search strategy to prioritize high-value clinical keywords.
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
import json
import os
import traceback
import asyncio
import concurrent.futures
import difflib
from openai import OpenAI

# Python 3.8 compatibility - asyncio.to_thread was added in 3.9
# So we create our own version using run_in_executor with ThreadPoolExecutor
async def to_thread(func, *args, **kwargs):
    """
    Run a function in a thread pool executor - Python 3.8 compatible version.
    This is basically what asyncio.to_thread does in Python 3.9+, but we're
    implementing it ourselves because we're stuck on 3.8 for now.
    """
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))

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

# Load high-value qualifiers once at module level for performance
# This JSON file contains medical terms that are highly specific and clinically significant
# We load it once and normalize all terms to lowercase for consistent matching
try:
    with open(os.path.join(os.path.dirname(__file__), "../config/high_value_qualifiers.json")) as f:
        HIGH_VALUE_QUALIFIERS = {k: [q.lower() for q in v] for k, v in json.load(f).items()}
except FileNotFoundError:
    print("Warning: high_value_qualifiers.json not found. Using fallback qualifiers.")
    HIGH_VALUE_QUALIFIERS = {
        "rash": ["slapped cheek", "bull's-eye", "target lesion"],
        "respiratory": ["whooping cough", "paroxysmal cough"],
        "neurologic": ["nuchal rigidity", "photophobia"]
    }

def match_high_value(qualifier: str) -> Optional[str]:
    """
    Return the best-matching high-value qualifier using fuzzy string matching.
    
    This function takes a symptom qualifier (like "red cheek rash") and tries to find
    the closest match in our high-value qualifiers database. We use difflib's fuzzy
    matching with a cutoff of 0.8 (80% similarity) to catch variations in phrasing.
    
    Args:
        qualifier: The symptom qualifier to match (e.g., "slapped cheek appearance")
    
    Returns:
        The matched high-value term if found, None otherwise
    """
    qualifier_norm = qualifier.lower().strip()
    for category, terms in HIGH_VALUE_QUALIFIERS.items():
        # difflib.get_close_matches returns a list of the best matches
        # We only want the first (best) match if it meets our 80% similarity threshold
        match = difflib.get_close_matches(qualifier_norm, terms, n=1, cutoff=0.8)
        if match:
            return match[0]
    return None

@dataclass
class DiagnosticState:
    """Holds all the data for a single diagnostic workflow run."""
    diagnosis_id: str
    patient_id: int
    symptoms_text: str
    structured_symptoms: Optional[Dict[str, Any]] = None
    patient_details: Optional[Dict[str, Any]] = None
    literature_evidence: List[Dict[str, Any]] = field(default_factory=list)
    case_database_evidence: List[Dict[str, Any]] = field(default_factory=list)
    imaging_findings: Optional[Dict[str, Any]] = None  # Added for imaging analysis results
    critique_notes: Optional[Dict[str, Any]] = None
    final_report: Optional[str] = None
    triage_level: Optional[str] = None
    drug_interaction_warnings: Optional[list] = None
    error_message: Optional[str] = None
    image_data: Optional[bytes] = None  # Added missing field for image data

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class OrchestratorWorkflow:
    """Coordinates the full diagnostic pipeline using an async, state-passing model."""

    def __init__(self):
        """Initialize all necessary clients and services."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pubmed_service = PubMedService()
        self.drug_service = DrugService()
        
        # Initialize ChromaDB only if available
        if CHROMADB_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        else:
            self.chroma_client = None
            
        self.prompts = DiagnosticPrompts()
        print("🤖 OrchestratorWorkflow initialized - ready to diagnose!")

    async def run(self, diagnosis_id: str, patient_id: int, symptoms_text: str, image_data: Optional[bytes] = None) -> Dict[str, Any]:
        """Runs the complete, dynamic, and parallelized diagnostic workflow."""
        state = DiagnosticState(diagnosis_id=diagnosis_id, patient_id=patient_id, symptoms_text=symptoms_text, image_data=image_data)
        log_step(state.diagnosis_id, "Orchestrator", "START", f"Workflow initiated for patient {patient_id}.")

        try:
            state.structured_symptoms = await self._safe_step(state, "SymptomAnalyzer", self._analyze_symptoms)
            state.patient_details = await self._safe_step(state, "EHR_Fetcher", self._fetch_ehr_data)

            # Run evidence-gathering in parallel
            tasks = [
                self._safe_step(state, "LitSearcher", self._search_literature),
                self._safe_step(state, "CaseSearcher", self._search_case_database)
            ]
            if state.image_data:
                tasks.append(self._safe_step(state, "ImagingAnalyzer", self._analyze_image))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Safely process the results
            state.literature_evidence = results[0] if not isinstance(results[0], Exception) else []
            state.case_database_evidence = results[1] if not isinstance(results[1], Exception) else []
            if state.image_data and len(results) > 2:
                 state.imaging_findings = results[2] if not isinstance(results[2], Exception) else None

            state.critique_notes = await self._safe_step(state, "CritiqueAgent", self._critique_evidence)
            state = await self._safe_step(state, "ReportSynthesizer", self._synthesize_report, is_state_modifier=True)
            state = await self._safe_step(state, "DrugChecker", self._check_drug_interactions, is_state_modifier=True)

            log_step(diagnosis_id, "Orchestrator", "END", "Workflow completed successfully.")
            return state.to_dict()

        except Exception as e:
            err_trace = traceback.format_exc()
            log_step(diagnosis_id, "Orchestrator", "FATAL_ERROR", err_trace, status="FAILURE")
            return state.to_dict()

    async def _safe_step(self, state: DiagnosticState, step_name: str, func, is_state_modifier: bool = False):
        """Wrapper for each step to handle logging and exceptions."""
        log_step(state.diagnosis_id, step_name, "START", "Step initiated.")
        try:
            if is_state_modifier:
                result = await func(state)
            else:
                result = await func(state)
            log_step(state.diagnosis_id, step_name, "END", f"Step completed successfully.")
            return result
        except Exception as e:
            err_trace = traceback.format_exc()
            state.error_message = f"Error in step '{step_name}': {str(e)}"
            log_step(state.diagnosis_id, step_name, "ERROR", err_trace, status="FAILURE")
            raise

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

    async def _search_literature(self, state: DiagnosticState) -> list:
        """Agent 3: Finds relevant medical research on PubMed with smarter query strategy."""
        symptoms = state.structured_symptoms.get('symptoms', [])
        if not symptoms:
            return []

        search_term = None

        # Try high-value qualifiers first using our fuzzy matching function
        # This catches specific clinical terms that are highly diagnostic
        for symptom in symptoms:
            for qualifier in symptom.get("qualifiers", []):
                matched = match_high_value(qualifier)
                if matched:
                    # Use "clinical significance" phrasing for better research results
                    # This tends to pull more diagnostic and treatment-focused papers
                    search_term = f"clinical significance of {matched} in pediatrics"
                    break
            if search_term:
                break

        # Fallback to symptom-driven search if no high-value terms found
        # This ensures we still get results even for common/non-specific symptoms
        if not search_term:
            symptom_names = [s.get('name', '') for s in symptoms if s.get('name')]
            if symptom_names:
                symptom_list = ' and '.join(symptom_names)
                search_term = f"differential diagnosis for pediatric {symptom_list}"
            else:
                # Last resort - return empty if we have no usable symptoms
                return []

        print(f"Executing literature search with smart query: '{search_term}'")

        # Query PubMed with our optimized search term
        pmids = await to_thread(self.pubmed_service.search, search_term, max_results=5)
        if not pmids:
            return []

        abstracts_data = await to_thread(self.pubmed_service.fetch_abstracts, pmids[:3])
        if not abstracts_data:
            return []

        return [
            {
                "source_id": f"PMID:{a.get('pmid', 'N/A')}",
                "text": f"Title: {a.get('title', 'N/A')}\nAbstract: {a.get('abstract', 'N/A')}",
                "confidence": a.get('score', 0.0)
            } for a in abstracts_data
        ]

    async def _search_case_database(self, state: DiagnosticState) -> list:
        """Agent 4: Finds similar cases in our local DB."""
        # Return empty list if ChromaDB is not available
        if not CHROMADB_AVAILABLE or not self.chroma_client:
            print("Case database search disabled - ChromaDB not available")
            return []
            
        symptoms = [s.get('name', '') for s in state.structured_symptoms.get('symptoms', []) if s.get('name')]
        if not symptoms: return []
        
        query = f"A case involving a {state.patient_details.get('age')} year old with {' and '.join(symptoms)}"
        
        try:
            collection = self.chroma_client.get_collection(name="medical_cases")
            results = await to_thread(collection.query, query_texts=[query], n_results=2)
            
            if not results or not results['documents'][0]: return []
            
            return [
                {
                    "source_id": f"CaseDB:{meta.get('case_id', f'doc_{i}')}",
                    "text": f"Case Title: {meta.get('title', 'N/A')}\nSummary: {doc}",
                    "confidence": 1 - dist # Convert distance to similarity
                } for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0]))
            ]
        except Exception as e:
            print(f"Case search failed: {e}. This may be expected if the collection is not yet populated.")
            return []


    async def _analyze_image(self, state: DiagnosticState) -> Optional[Dict[str, Any]]:
        """Agent: Analyzes an uploaded medical image using a VLM."""
        if not state.image_data:
            return None
        
        import base64
        base64_image = base64.b64encode(state.image_data).decode('utf-8')
        
        response = await to_thread(
            self.client.chat.completions.create,
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.prompts.IMAGING_ANALYSIS_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": { "url": f"data:image/jpeg;base64,{base64_image}" }
                        }
                    ]
                }
            ]
        )
        return {"analysis": response.choices[0].message.content}

    async def _critique_evidence(self, state: DiagnosticState) -> Dict[str, Any]:
        """Agent 5: Critically reviews all gathered evidence for gaps and inconsistencies."""
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

    async def _synthesize_report(self, state: DiagnosticState) -> DiagnosticState:
        """Agent 6: Generates the main report from all evidence and critique."""
        prompt = self.prompts.synthesis_report_user(state.to_dict())
        response = await to_thread(
            self.client.chat.completions.create,
            model="gpt-4o", temperature=0.2,
            messages=[
                {"role": "system", "content": self.prompts.SYNTHESIS_REPORT_SYSTEM},
                {"role": "user", "content": prompt}
            ]
        )
        full_report_text = response.choices[0].message.content
        
        try:
            last_line = full_report_text.strip().split('\n')[-1]
            if "TRIAGE_LEVEL:" in last_line:
                state.triage_level = last_line.split("TRIAGE_LEVEL:")[1].strip()
        except Exception:
            state.triage_level = "Undetermined"

        state.final_report = full_report_text
        return state

    async def _check_drug_interactions(self, state: DiagnosticState) -> DiagnosticState:
        """Agent 7: A final safety check for drug interactions."""
        potential_conditions = []
        if state.final_report and "Potential Considerations" in state.final_report:
            considerations_section = state.final_report.split("Potential Considerations")[1]
            lines = considerations_section.split('\n')
            for line in lines:
                if line.strip().startswith(('*', '-')):
                    condition = line.strip().lstrip('*- ').strip().split(':')[0]
                    potential_conditions.append(condition)
        
        if potential_conditions:
            interaction_results = self.drug_service.check_interactions(
                conditions=potential_conditions,
                patient_history=state.patient_details.get('medical_history', '')
            )
            if interaction_results and interaction_results.get("warnings"):
                state.drug_interaction_warnings = interaction_results["warnings"]
                state.final_report += "\n\n## 🚨 Safety Warnings\n\n" + "\n".join([f"- {w}" for w in interaction_results["warnings"]])
        return state

