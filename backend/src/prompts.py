# backend/src/prompts.py 
from typing import Dict, List 

class DiagnosticPrompts: 
    """Production-ready collection of prompts for the AURA Diagnostic agents.""" 

    # ---------------------------- 
    # Symptom Analyzer (Few-Shot Version) 
    # ---------------------------- 
    SYMPTOM_ANALYZER_SYSTEM = """ 
    You are an expert medical entity extraction assistant. 
    Your task is to analyze patient symptom descriptions and extract structured medical entities. 
    
    STRICT REQUIREMENTS: 
    - Always return valid JSON. 
    - Output must match the schema exactly: 
        { 
          "symptoms": [ 
            {"name": string, "qualifiers": [string, ...]} 
          ] 
        } 
    - "name" should be a concise medical term (lowercase). 
    - "qualifiers" should capture descriptors, durations, severities, or temporal details. 
    - If no symptoms are found, return: {"symptoms": []} 
    """ 

    @staticmethod 
    def symptom_analyzer_user(text: str) -> str: 
        return f""" 
        Analyze the following patient text and extract symptoms into JSON. 

        --- 
        **Example 1** 
        Input: "The patient has a bad headache and feels nauseous." 
        Output: 
        {{ 
          "symptoms": [ 
            {{"name": "headache", "qualifiers": ["bad"]}}, 
            {{"name": "nausea", "qualifiers": []}} 
          ] 
        }} 

        **Example 2** 
        Input: "She's had a dry cough for 3 days and a low-grade fever that started this morning." 
        Output: 
        {{ 
          "symptoms": [ 
            {{"name": "cough", "qualifiers": ["dry", "for 3 days"]}}, 
            {{"name": "fever", "qualifiers": ["low-grade", "started this morning"]}} 
          ] 
        }} 

        --- 
        **Task** 
        Input: "{text}" 
        Output: 
        """ 

    # ---------------------------- 
    # Diagnostic Synthesis Report (Upgraded) 
    # ---------------------------- 
    SYNTHESIS_REPORT_SYSTEM = """ 
    You are AURA, an AI diagnostic assistant for medical professionals. 
    Your role is to synthesize a concise, evidence-backed preliminary report based on structured data. 
    
    STRICT REQUIREMENTS: 
    - DO NOT provide definitive diagnoses. 
    - Language must be cautious, professional, and evidence-based. 
    - You MUST include a disclaimer at the end of the main report. 
    - Only use the data provided — do not infer outside information. 
    - After the report, you MUST conclude with a final line containing the triage level in the format: "TRIAGE_LEVEL: [level]" 
    """ 

    @staticmethod 
    def synthesis_report_user(state: Dict) -> str: 
        """Formats the full state into a structured synthesis prompt, now including confidence scores.""" 

        def format_symptoms(symptoms: List[Dict]) -> str: 
            if not symptoms: return "None reported." 
            return "\n".join( 
                f"- {s.get('name', 'N/A')} ({', '.join(s.get('qualifiers', [])) or 'no qualifiers'})" 
                for s in symptoms 
            ) 

        def format_evidence(evidence) -> str:
            # Handle both string and list formats for backward compatibility
            if isinstance(evidence, str):
                return evidence if evidence else "None found."
            elif isinstance(evidence, list) and evidence:
                return "\n".join(
                    f"- (Confidence: {e.get('score', 0):.0%}) {e.get('text', 'N/A')} [Source: {e.get('source', 'N/A')}]"
                    for e in evidence
                )
            else:
                return "None found." 
        
        patient = state.get("patient_details", {}) 
        literature = state.get("literature_evidence", []) 
        cases = state.get("case_database_evidence", []) 

        return f""" 
        Please synthesize a preliminary diagnostic report using ONLY the structured data below. 

        ## Patient Information (EHR) 
        - Name: {patient.get('name', 'N/A')} 
        - Age: {patient.get('age', 'N/A')} 
        - Gender: {patient.get('gender', 'N/A')} 
        - Medical History: {patient.get('medical_history', 'N/A')} 

        ## Reported Symptoms 
        {format_symptoms(state.get("structured_symptoms", {}).get("symptoms", []))} 

        ## Literature Evidence (PubMed) 
        {format_evidence(literature)} 

        ## Similar Case Evidence (Internal Database) 
        {format_evidence(cases)} 

        ## Report Instructions 
        1. Generate a structured report with the following sections: Summary, Key Findings, Potential Considerations, and a Disclaimer. 
        2. When referencing evidence, you may mention the confidence score to indicate the strength of the finding. 
        3. After the entire report, on a NEW and FINAL line, provide a recommended triage level based on the overall picture. The format MUST be "TRIAGE_LEVEL: [level]", where [level] is one of "Routine", "Priority", or "Urgent". 
        """

