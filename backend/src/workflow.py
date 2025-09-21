# backend/src/workflow.py
"""
AURA Diagnostics - Final "Epic" Asynchronous Multi-Agent Workflow

This orchestrator is the brain of the AURA system. This final version includes
a highly refined, direct search strategy for PubMed and fixes a critical
data-passing bug to ensure patient data integrity in the final report.

Key fixes in this version:
- Smart PubMed query mapping for laser-focused clinical results
- Patient data bug SQUASHED - correct patient info flows to final report
- Robust error handling and async execution
- Full integration of all research sources (PubMed, OpenAlex, Case DB)
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
import json
import os
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import difflib

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
from src.services.openalex_service import OpenAlexService
from src.services.drug_service import DrugService
from src.prompts import DiagnosticPrompts
from src.audit_logger import log_step

# Load high-value qualifiers for smart search
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
    Fuzzy matching function to find high-value clinical qualifiers.
    This catches specific diagnostic terms that are clinically significant.
    """
    qualifier_lower = qualifier.lower()
    for category, qualifiers in HIGH_VALUE_QUALIFIERS.items():
        for q in qualifiers:
            # Use difflib for fuzzy matching - catches typos and variations
            if difflib.SequenceMatcher(None, qualifier_lower, q).ratio() > 0.8:
                return q
    return None

@dataclass
class DiagnosticState:
    """
    State container that flows through our workflow.
    This holds all the data as it gets enriched by each agent.
    """
    diagnosis_id: str
    patient_id: int
    symptoms_text: str
    image_data: Optional[bytes] = None
    structured_symptoms: Optional[Dict[str, Any]] = None
    patient_details: Optional[Dict[str, Any]] = None
    literature_evidence: List[Dict[str, Any]] = field(default_factory=list)
    case_database_evidence: List[Dict[str, Any]] = field(default_factory=list)
    imaging_findings: Optional[Dict[str, Any]] = None
    critique_notes: Optional[Dict[str, Any]] = None
    final_report: Optional[str] = None
    triage_level: Optional[str] = None
    drug_interaction_warnings: Optional[list] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for prompt generation and API responses."""
        return asdict(self)

class OrchestratorWorkflow:
    """
    Coordinates the full diagnostic pipeline using a dynamic, async, state-passing model.
    This is where all the magic happens - each agent enriches the state sequentially.
    """

    def __init__(self):
        """Initialize all necessary clients, services, and load the Clinical Lexicon."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pubmed_service = PubMedService()
        self.openalex_service = OpenAlexService()  # Keep the working OpenAlex service
        self.drug_service = DrugService()
        
        # ChromaDB setup with error handling
        if CHROMADB_AVAILABLE:
            try:
                self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            except Exception as e:
                print(f"ChromaDB initialization failed: {e}")
                self.chroma_client = None
        else:
            self.chroma_client = None
            
        self.prompts = DiagnosticPrompts()
        self.executor = ThreadPoolExecutor(max_workers=5)
        print("🤖 Final Epic OrchestratorWorkflow initialized!")

    async def _run_in_executor(self, func, *args, **kwargs):
        """
        Compatibility wrapper to run synchronous functions asynchronously.
        This lets us use async/await with the OpenAI client and other sync libraries.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, partial(func, *args, **kwargs))

    async def run(self, diagnosis_id: str, patient_id: int, symptoms_text: str, image_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Runs the complete, dynamic, and parallelized diagnostic workflow.
        This is the main entry point that orchestrates all the agents.
        """
        state = DiagnosticState(diagnosis_id=diagnosis_id, patient_id=patient_id, symptoms_text=symptoms_text, image_data=image_data)
        log_step(state.diagnosis_id, "Orchestrator", "START", f"Workflow initiated for patient {patient_id}.")

        try:
            # --- PHASE 1: SEQUENTIAL FOUNDATION ---
            # These need to run in order because later steps depend on them
            state.structured_symptoms = await self._safe_step(state, "SymptomAnalyzer", self._analyze_symptoms)
            state.patient_details = await self._safe_step(state, "EHR_Fetcher", self._fetch_ehr_data)

            # --- PHASE 2: PARALLEL META-RESEARCH ---
            # These can all run at the same time to speed things up
            evidence_tasks = [
                self._safe_step(state, "PubMedSearcher", self._search_pubmed),
                self._safe_step(state, "OpenAlexSearcher", self._search_openalex),
                self._safe_step(state, "CaseSearcher", self._search_case_database)
            ]
            if state.image_data:
                evidence_tasks.append(self._safe_step(state, "ImagingAnalyzer", self._analyze_image))
            
            results = await asyncio.gather(*evidence_tasks, return_exceptions=True)

            # Combine PubMed and OpenAlex results into literature_evidence
            pubmed_results = results[0] if not isinstance(results[0], Exception) else []
            openalex_results = results[1] if not isinstance(results[1], Exception) else []
            state.literature_evidence = pubmed_results + openalex_results
            
            state.case_database_evidence = results[2] if not isinstance(results[2], Exception) else []
            if state.image_data and len(results) > 3:
                 state.imaging_findings = results[3] if not isinstance(results[3], Exception) else None

            # --- PHASE 3: SYNTHESIS & SAFETY CHECKS ---
            # These run sequentially because they build on each other
            state.critique_notes = await self._safe_step(state, "CritiqueAgent", self._critique_evidence)
            state = await self._safe_step(state, "ReportSynthesizer", self._synthesize_report, is_state_modifier=True)
            state = await self._safe_step(state, "DrugChecker", self._check_drug_interactions, is_state_modifier=True)

            log_step(diagnosis_id, "Orchestrator", "END", "Workflow completed successfully.")
            return state.to_dict()

        except Exception as e:
            err_trace = traceback.format_exc()
            log_step(diagnosis_id, "Orchestrator", "FATAL_ERROR", err_trace, status="FAILURE")
            state.error_message = f"Workflow failed: {str(e)}"
            return state.to_dict()

    async def _safe_step(self, state: DiagnosticState, step_name: str, func, is_state_modifier: bool = False):
        """
        Wrapper for each step to handle logging and exceptions robustly.
        This ensures that if one agent fails, the whole workflow doesn't crash.
        """
        log_step(state.diagnosis_id, step_name, "START", "Step initiated.")
        try:
            result = await func(state)
            log_step(state.diagnosis_id, step_name, "END", "Step completed successfully.")
            return result
        except Exception as e:
            err_trace = traceback.format_exc()
            state.error_message = f"Error in step '{step_name}': {str(e)}"
            log_step(state.diagnosis_id, step_name, "ERROR", err_trace, status="FAILURE")
            # Return empty result instead of crashing
            if is_state_modifier:
                return state
            else:
                return [] if "search" in step_name.lower() else {}

    # --- Agent Implementations ---

    async def _analyze_symptoms(self, state: DiagnosticState) -> Dict[str, Any]:
        """
        Agent 1: Extracts structured symptoms from raw text.
        This turns messy human language into structured data the other agents can use.
        """
        response = await self._run_in_executor(
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
        """
        Agent 2: Gets patient details from the database.
        This is critical - we need the right patient data for the final report.
        """
        patient_data = await self._run_in_executor(ehr_agent.get_patient_details, state.patient_id)
        if patient_data is None:
            raise ValueError(f"Patient with ID {state.patient_id} not found or data malformed.")
        return patient_data

    def _get_smart_search_query(self, state: DiagnosticState) -> str:
        """
        THE BIG FIX: Smart query generation for PubMed.
        Instead of complex clinical lexicon queries, we map high-value keywords
        directly to powerful medical search terms that PubMed understands.
        """
        symptoms = state.structured_symptoms.get('symptoms', [])
        if not symptoms: 
            return ""

        # --- REFINED QUERY LOGIC ---
        # Tier 1: Check for high-value keywords and map them to direct medical terms.
        # This is the secret sauce - direct mapping to known diagnostic terms.
        high_value_map = {
            "strawberry tongue": '"Kawasaki Disease" OR "Scarlet Fever"',
            "slapped cheek": '"Parvovirus B19" OR "Erythema Infectiosum"',
            "bull's-eye rash": '"Lyme Disease" OR "Erythema Migrans"',
            "target lesion": '"Stevens-Johnson Syndrome" OR "Erythema Multiforme"',
            "nuchal rigidity": '"meningitis" OR "nuchal rigidity"',
            "whooping cough": '"Pertussis" OR "Bordetella pertussis"',
            "paroxysmal cough": '"Pertussis" OR "whooping cough"'
        }
        
        search_query = ""
        # Check qualifiers first - these are the most specific
        for symptom in symptoms:
            for qualifier in symptom.get("qualifiers", []):
                qualifier_lower = qualifier.lower()
                for keyword, medical_term in high_value_map.items():
                    if keyword in qualifier_lower:
                        search_query = medical_term
                        print(f"🎯 High-value match found: '{qualifier}' -> '{medical_term}'")
                        break
                if search_query: 
                    break
            # Check the symptom name itself too
            if not search_query:
                symptom_name = symptom.get('name', '').lower()
                if symptom_name in high_value_map:
                    search_query = high_value_map[symptom_name]
                    print(f"🎯 High-value symptom match: '{symptom_name}' -> '{search_query}'")
                    break
        
        # Tier 2: Fallback to a focused differential diagnosis query
        if not search_query:
            symptom_names = [s.get('name', '') for s in symptoms[:2] if s.get('name')]  # Limit to top 2
            if symptom_names:
                # Build a simple, focused query that PubMed can handle
                patient_age = state.patient_details.get('age', 0) if state.patient_details else 0
                age_term = "pediatric" if patient_age < 18 else "adult"
                search_query = f'{age_term} differential diagnosis {" ".join(symptom_names)}'
                print(f"📋 Fallback query: '{search_query}'")
        
        return search_query

    async def _search_pubmed(self, state: DiagnosticState) -> list:
        """
        Agent: Finds specialized clinical research on PubMed.
        Now uses the smart query system for laser-focused results.
        """
        query = self._get_smart_search_query(state)
        if not query: 
            return []
            
        print(f"🔍 Executing PubMed search with smart query: '{query}'")
        
        pmids = await self._run_in_executor(self.pubmed_service.search, query, max_results=3)
        if not pmids: 
            return []
        
        abstracts_data = await self._run_in_executor(self.pubmed_service.fetch_abstracts, pmids)
        if not abstracts_data: 
            return []
        
        return [
            {
                "source_id": f"PMID:{a.get('pmid', 'N/A')}", 
                "text": f"Title: {a.get('title', 'N/A')}\nAbstract: {a.get('abstract', 'N/A')}", 
                "confidence": 0.95
            } 
            for a in abstracts_data
        ]

    async def _search_openalex(self, state: DiagnosticState) -> list:
        """
        Agent: Finds broad, interdisciplinary research on OpenAlex.
        Uses the same smart query system but casts a wider net.
        """
        query = self._get_smart_search_query(state)
        if not query: 
            return []
            
        print(f"🌐 Executing OpenAlex search with smart query: '{query}'")

        try:
            results = await self._run_in_executor(self.openalex_service.search, query, max_results=2)
            return results if results else []
        except Exception as e:
            print(f"OpenAlex search failed: {e}")
            return []

    async def _search_case_database(self, state: DiagnosticState) -> list:
        """
        Agent: Finds similar cases in our local ChromaDB.
        This provides institutional knowledge and similar case patterns.
        """
        if not self.chroma_client: 
            return []
            
        symptoms = [s.get('name', '') for s in state.structured_symptoms.get('symptoms', []) if s.get('name')]
        if not symptoms: 
            return []
            
        # Build a natural language query for semantic search
        patient_age = state.patient_details.get('age', 'unknown age') if state.patient_details else 'unknown age'
        query = f"A case involving a {patient_age} year old with {' and '.join(symptoms)}"
        
        try:
            collection = self.chroma_client.get_collection(name="medical_cases")
            results = await self._run_in_executor(collection.query, query_texts=[query], n_results=2)
            
            if not results or not results['documents'][0]: 
                return []
                
            return [
                {
                    "source_id": f"CaseDB:{meta.get('case_id', f'doc_{i}')}", 
                    "text": f"Case Title: {meta.get('title', 'N/A')}\nSummary: {doc}", 
                    "confidence": 1 - dist
                } 
                for i, (doc, meta, dist) in enumerate(zip(
                    results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]
                ))
            ]
        except Exception as e:
            print(f"Case search failed: {e}. This is expected if the collection is not populated.")
            return []

    async def _analyze_image(self, state: DiagnosticState) -> Optional[Dict[str, Any]]:
        """
        Agent: Analyzes an uploaded medical image using GPT-4V.
        This adds visual diagnostic information to the evidence mix.
        """
        if not state.image_data: 
            return None
            
        import base64
        base64_image = base64.b64encode(state.image_data).decode('utf-8')
        
        response = await self._run_in_executor(
            self.client.chat.completions.create,
            model="gpt-4o",
            messages=[{
                "role": "user", 
                "content": [
                    {"type": "text", "text": self.prompts.IMAGING_ANALYSIS_PROMPT}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]
        )
        return {"analysis": response.choices[0].message.content}

    async def _critique_evidence(self, state: DiagnosticState) -> Dict[str, Any]:
        """
        Agent: Critically reviews all gathered evidence.
        This is our quality control - it identifies weak evidence and gaps.
        """
        prompt = self.prompts.critique_agent_user(state.to_dict())
        response = await self._run_in_executor(
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
        """
        Agent: Generates the main report from all evidence and critique.
        
        🚨 CRITICAL BUG FIX: We now pass the entire current state.to_dict() 
        to the prompt function. This ensures the prompt gets the LATEST 
        patient_details for this specific diagnostic run, not some cached 
        or default patient data.
        """
        # --- THIS IS THE BUG FIX ---
        # We pass the complete, current state to ensure correct patient data flows through
        prompt = self.prompts.synthesis_report_user(state.to_dict())
        # --- END OF BUG FIX ---
        
        response = await self._run_in_executor(
            self.client.chat.completions.create,
            model="gpt-4o", temperature=0.2,
            messages=[
                {"role": "system", "content": self.prompts.SYNTHESIS_REPORT_SYSTEM}, 
                {"role": "user", "content": prompt}
            ]
        )
        
        full_report_text = response.choices[0].message.content
        
        # Extract triage level from the report
        try:
            last_line = full_report_text.strip().split('\n')[-1]
            if "TRIAGE_LEVEL:" in last_line:
                state.triage_level = last_line.split("TRIAGE_LEVEL:")[1].strip()
        except Exception:
            state.triage_level = "Undetermined"
            
        state.final_report = full_report_text
        return state

    async def _check_drug_interactions(self, state: DiagnosticState) -> DiagnosticState:
        """
        Agent: A final safety check for drug interactions.
        This scans the diagnostic considerations for potential medication conflicts.
        """
        potential_conditions = []
        
        # Extract potential conditions from the report
        if state.final_report and "Potential Considerations" in state.final_report:
            section = state.final_report.split("Potential Considerations")[1]
            lines = section.split('\n')
            for line in lines:
                if line.strip().startswith(('*', '-')):
                    condition = line.strip().lstrip('*- ').strip().split(':')[0]
                    potential_conditions.append(condition)
        
        # Check for interactions if we found potential conditions
        if potential_conditions:
            interaction_results = self.drug_service.check_interactions(
                conditions=potential_conditions,
                patient_history=state.patient_details.get('medical_history', '') if state.patient_details else ''
            )
            
            if interaction_results and interaction_results.get("warnings"):
                state.drug_interaction_warnings = interaction_results["warnings"]
                # Append warnings to the report
                state.final_report += "\n\n## 🚨 Safety Warnings\n\n" + "\n".join([
                    f"- {w}" for w in interaction_results["warnings"]
                ])
                
        return state

