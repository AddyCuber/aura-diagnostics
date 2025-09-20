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
    # --- NEW: CRITIQUE AGENT --- 
    # ---------------------------- 
    CRITIQUE_AGENT_SYSTEM = """ 
    You are a senior clinical reviewer AI. Your role is to critically evaluate a collection of evidence 
    for a patient case. You are a skeptic. Your goal is to identify potential issues before a final 
    report is generated. Do not offer a diagnosis. Focus ONLY on the quality and coherence of the data provided.
    
    CRITICAL: When providing critique, you must reference specific sources from the evidence provided.
    - Reference specific PubMed articles: "The study PMID:12345 suggests..."
    - Reference specific case studies: "Case CaseDB:CASE_001 shows..."  
    - Reference patient documents: "Patient's medical history [Patient: Medical History] indicates..."
    - NEVER make generic statements without source attribution
    - Your critique must be evidence-based, not opinion-based
    """ 

    @staticmethod 
    def critique_agent_user(state: Dict) -> str: 
        # (Helper functions can be defined here or globally in the file if needed) 
        def format_symptoms(symptoms: List[Dict]) -> str: 
            if not symptoms: return "None reported." 
            return ", ".join([s.get('name', 'N/A') for s in symptoms]) 

        def format_evidence(evidence: list, source_prefix: str) -> str: 
            if not evidence: return f"No {source_prefix.lower()} found." 
            # Handle the new structured format with source_id, text, and confidence
            if isinstance(evidence[0], dict) and 'source_id' in evidence[0]: 
                 return "\n- ".join([f"[{item.get('source_id', 'N/A')}] {item.get('text', 'N/A')[:100]}..." for item in evidence]) 
            # Fallback for old format or simple dicts
            elif isinstance(evidence[0], dict): 
                 return "\n- ".join([f"[{source_prefix}] {item.get('title', 'N/A')}" for item in evidence]) 
            return "\n- ".join([f"[{source_prefix}] {item}" for item in evidence]) 

        patient = state.get("patient_details", {}) 
        symptoms = state.get("structured_symptoms", {}).get("symptoms", []) 
        literature = state.get("literature_evidence", []) 
        cases = state.get("case_database_evidence", []) 

        return f""" 
        Critically review the following evidence bundle. 

        ## Patient Information 
        - Age: {patient.get('age', 'N/A')} 
        - Gender: {patient.get('gender', 'N/A')} 
        - Medical History: {patient.get('medical_history', 'N/A')} 

        ## Evidence 
        - Symptoms Reported: {format_symptoms(symptoms)} 
        - Literature Found: {format_evidence(literature, 'PubMed')} 
        - Similar Cases Found: {format_evidence(cases, 'CaseDB')} 

        ## Your Task 
        Based ONLY on the data above, provide a critique in a valid JSON format. 
        Identify: 
        1. "inconsistencies": Are there any contradictions between the patient's history and the evidence? (e.g., literature suggests a condition common in adults, but the patient is a child). 
        2. "gaps": Is there any missing information that weakens the evidence? (e.g., "The literature search returned very few results, suggesting the initial query may be too narrow.") 
        3. "red_flags": Are there any high-risk factors that need to be highlighted? (e.g., "The symptom 'neck stiffness' combined with fever is a significant red flag for meningitis and should be prioritized.") 

        Respond ONLY with a JSON object in this format: 
        {{ 
          "inconsistencies": ["...", "..."], 
          "gaps": ["...", "..."], 
          "red_flags": ["...", "..."] 
        }} 
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
    
    CRITICAL SOURCE CITATION REQUIREMENT:
    - When you use ANY piece of evidence in your report, you MUST include the full [Source:...] tag provided with it.
    - This is NON-NEGOTIABLE. Every statement based on evidence MUST be followed by its source citation.
    - Example: "Patient presents with chest pain [Source: PMID:12345]" or "Similar case showed improvement [Source: CaseDB:CASE_001]"
    - Do NOT paraphrase or modify the source tags - use them EXACTLY as provided in the evidence.
    - If evidence lacks a proper external source, reference patient documents using [Patient: Document Type] format
    - NEVER use generic "Internal Analysis" - always trace back to specific literature, cases, or patient documents
    
    PATIENT DOCUMENT REFERENCING:
    - When referencing patient-specific information from their medical records, use the format [Patient: Document Type]
    - Examples: "Patient has history of asthma [Patient: Medical History]" or "Lab results show elevated eosinophils [Patient: Lab Results]"
    - This allows medical professionals to quickly access the source documents for verification
    - Use these document types: Medical History, Lab Results, Chest X-Ray, Previous Visits, Medications, Allergies
    """ 

    @staticmethod
    def _format_evidence_for_prompt(evidence: list) -> str:
        """
        Formats evidence list into a clean, readable string for the synthesis prompt.
        Each piece of evidence gets its own section with clear source attribution.
        This makes it easier for the AI to reference specific sources in the report.
        """
        if not evidence: 
            return "No relevant evidence found."
        
        # Create clean sections separated by dividers - makes it super clear where each piece starts/ends
        return "\n\n---\n\n".join(
            f"{item['text']}\n[Source: {item['source_id']}]"
            for item in evidence
        )

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
                    f"- (Confidence: {e.get('confidence', 0):.0%}) {e.get('text', 'N/A')} [Source: {e.get('source_id', 'N/A')}]"
                    for e in evidence
                )
            else:
                return "None found." 
        
        # NEW: Add critique formatting
        critique = state.get("critique_notes", {}) 

        def format_critique(critique_data: dict) -> str: 
            if not critique_data or not any(critique_data.values()): return "No critique notes provided." 
            notes = [] 
            if critique_data.get("inconsistencies"): 
                notes.append(f"Inconsistencies Identified: {' | '.join(critique_data['inconsistencies'])}") 
            if critique_data.get("gaps"): 
                notes.append(f"Gaps Identified: {' | '.join(critique_data['gaps'])}") 
            if critique_data.get("red_flags"): 
                notes.append(f"Red Flags Identified: {' | '.join(critique_data['red_flags'])}") 
            return "\n".join(f"- {note}" for note in notes) 
        
        patient = state.get("patient_details", {}) 
        # NEW: Use the cleaner formatting method for evidence - gives better source attribution
        literature = DiagnosticPrompts._format_evidence_for_prompt(state.get("literature_evidence", []))
        cases = DiagnosticPrompts._format_evidence_for_prompt(state.get("case_database_evidence", [])) 
        
        # Format imaging findings if available
        imaging_section = ""
        if state.get("imaging_findings"):
            imaging_analysis = state["imaging_findings"].get("analysis", "No imaging analysis available.")
            imaging_section = f"""
        ## Imaging Analysis
        {imaging_analysis} [Patient: Imaging Report]
        """

        return f""" 
        Please synthesize a preliminary diagnostic report using ONLY the structured data and the supervisory critique below. 

        ## Supervisory Critique 
        {format_critique(critique)} 

        ## Patient Information (EHR) 
        - Name: {patient.get('name', 'N/A')} 
        - Age: {patient.get('age', 'N/A')} 
        - Gender: {patient.get('gender', 'N/A')} 
        - Medical History: {patient.get('medical_history', 'N/A')} 

        ## Reported Symptoms 
        {format_symptoms(state.get("structured_symptoms", {}).get("symptoms", []))} 

        ## Literature Evidence (PubMed) 
        {literature} 

        ## Similar Case Evidence (Internal Database) 
        {cases} 
        {imaging_section}
        ## Report Instructions 
        1. Generate a structured report with the following sections: Summary, Key Findings, Potential Considerations, and a Disclaimer. 
        2. **Use the Supervisory Critique to guide your summary and to highlight any identified gaps or red flags in the 'Potential Considerations' section.** 
        3. When referencing evidence, you may mention the confidence score to indicate the strength of the finding. 
        4. After the entire report, on a NEW and FINAL line, provide a recommended triage level based on the overall picture. The format MUST be "TRIAGE_LEVEL: [level]", where [level] is one of "Routine", "Priority", or "Urgent". 
        """

    # ----------------------------
    # Imaging Analysis Agent
    # ----------------------------
    IMAGING_ANALYSIS_PROMPT = """
    You are a medical imaging analysis AI assistant. Your role is to analyze medical images and provide structured observations that can support diagnostic workflows.

    CRITICAL INSTRUCTIONS:
    - You are NOT providing a diagnosis - only describing what you observe in the image
    - Focus on objective, measurable findings
    - Use precise medical terminology when describing anatomical structures
    - Note any abnormalities, asymmetries, or concerning features
    - Indicate areas that may require further clinical correlation
    - Always include confidence levels for your observations

    RESPONSE FORMAT:
    Provide your analysis in this structure:
    
    ## Image Quality Assessment
    [Comment on image quality, clarity, positioning]
    
    ## Anatomical Observations  
    [Describe normal anatomical structures visible]
    
    ## Notable Findings
    [List any abnormalities, asymmetries, or areas of concern]
    
    ## Clinical Correlation Needed
    [Areas that require additional clinical context or further imaging]
    
    ## Confidence Assessment
    [Rate your confidence in the observations and explain any limitations]

    Remember: This analysis supports clinical decision-making but does not replace professional medical interpretation.
    """

