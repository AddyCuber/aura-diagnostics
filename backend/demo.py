#!/usr/bin/env python3
"""
AURA Diagnostic System - Comprehensive Demo Script

This demo showcases the complete AURA diagnostic workflow with multiple test cases.
It demonstrates how the system processes patient symptoms, searches medical literature,
analyzes evidence, and generates comprehensive diagnostic reports.

Run this script to see AURA in action!
"""

import sys
import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.workflow import OrchestratorWorkflow

class AURADemo:
    """
    Demo orchestrator that runs multiple test cases to showcase AURA's capabilities.
    
    This class handles the demo flow, formatting output, and presenting results
    in a user-friendly way. Think of it as the "presenter" for our AI diagnostic system.
    """
    
    def __init__(self):
        """Initialize the demo with our workflow and test cases."""
        self.workflow = OrchestratorWorkflow()
        
        # Define our test cases - these represent different types of medical scenarios
        # Each case tests different aspects of the diagnostic system
        self.test_cases = [
            {
                "name": "Pediatric Autoimmune Case",
                "description": "Young patient with systemic symptoms suggesting autoimmune condition",
                "patient_id": 3,  # Maria Rodriguez from our test data
                "symptoms": "Patient presents with fatigue, joint pain, and skin rash that worsens in sunlight. Reports morning stiffness lasting over an hour and butterfly-shaped facial rash.",
                "expected_focus": "Autoimmune conditions, particularly lupus"
            },
            {
                "name": "Respiratory Infection Case", 
                "description": "Adult patient with respiratory symptoms",
                "patient_id": 1,  # John Smith from our test data
                "symptoms": "Patient has persistent cough for 3 weeks, fever up to 101.5°F, chest pain when breathing deeply, and shortness of breath with mild exertion.",
                "expected_focus": "Respiratory infections, pneumonia, tuberculosis"
            },
            {
                "name": "Neurological Symptoms Case",
                "description": "Patient with concerning neurological presentation",
                "patient_id": 2,  # Sarah Johnson from our test data  
                "symptoms": "Patient reports severe headaches with neck stiffness, sensitivity to light, nausea, and mild confusion. Symptoms developed over 2 days.",
                "expected_focus": "Meningitis, intracranial pressure, neurological infections"
            }
        ]
    
    async def run_demo(self):
        """
        Run the complete AURA demo with all test cases.
        
        This is the main demo flow - it runs each test case and presents
        the results in a clear, organized way that shows off what AURA can do.
        """
        print("🚀 AURA Diagnostic System - Live Demo")
        print("=" * 60)
        print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("🤖 About AURA:")
        print("AURA is an AI-powered diagnostic assistant that:")
        print("• Analyzes patient symptoms using advanced NLP")
        print("• Searches medical literature for relevant research")
        print("• Reviews evidence for diagnostic insights")
        print("• Generates comprehensive diagnostic reports")
        print("• Provides triage recommendations")
        print()
        
        # Run each test case
        for i, case in enumerate(self.test_cases, 1):
            print(f"📋 Test Case {i}: {case['name']}")
            print("-" * 40)
            print(f"Description: {case['description']}")
            print(f"Expected Focus: {case['expected_focus']}")
            print()
            
            try:
                # Run the diagnostic workflow
                result = await self.workflow.run(
                    diagnosis_id=f"demo-{i:03d}",
                    patient_id=case["patient_id"],
                    symptoms_text=case["symptoms"]
                )
                
                # Present the results
                await self._present_results(case, result)
                
            except Exception as e:
                print(f"❌ Error in test case {i}: {str(e)}")
                print()
            
            # Add spacing between test cases
            if i < len(self.test_cases):
                print("\n" + "="*60 + "\n")
        
        print("🎯 Demo Complete!")
        print("AURA has successfully demonstrated its diagnostic capabilities.")
        print("The system is ready for clinical evaluation and testing.")
    
    async def _present_results(self, case: Dict[str, Any], result: Dict[str, Any]):
        """
        Present the results of a diagnostic workflow in a clear, organized format.
        
        This method takes the raw workflow output and formats it for human consumption.
        It highlights the key insights and shows the diagnostic reasoning process.
        """
        print("📊 DIAGNOSTIC RESULTS:")
        print()
        
        # Patient Information
        patient = result.get("patient_details", {})
        if patient:
            print(f"👤 Patient: {patient.get('name', 'Unknown')}")
            print(f"   Age: {patient.get('age', 'Unknown')} years")
            print(f"   Gender: {patient.get('gender', 'Unknown')}")
            print()
        
        # Symptom Analysis
        symptoms = result.get("structured_symptoms", {})
        if symptoms and symptoms.get("symptoms"):
            print("🔍 SYMPTOM ANALYSIS:")
            for symptom in symptoms["symptoms"][:3]:  # Show top 3 symptoms
                name = symptom.get("name", "Unknown")
                severity = symptom.get("severity", "Unknown")
                print(f"   • {name} (Severity: {severity})")
            print()
        
        # Literature Evidence
        literature = result.get("literature_evidence", [])
        if literature:
            print(f"📚 LITERATURE EVIDENCE ({len(literature)} articles found):")
            for i, article in enumerate(literature[:2], 1):  # Show top 2 articles
                source_id = article.get("source_id", "Unknown")
                # Extract title from the text field
                text = article.get("text", "")
                title = text.split("Title: ")[1].split("\nAbstract:")[0] if "Title: " in text else "Unknown Title"
                print(f"   {i}. {source_id}")
                print(f"      {title[:80]}{'...' if len(title) > 80 else ''}")
            print()
        
        # Clinical Critique
        critique = result.get("critique_notes", {})
        if critique:
            print("🔬 CLINICAL REVIEW:")
            gaps = critique.get("evidence_gaps", [])
            if gaps:
                print("   Evidence Gaps Identified:")
                for gap in gaps[:2]:  # Show top 2 gaps
                    print(f"   • {gap}")
            
            recommendations = critique.get("recommendations", [])
            if recommendations:
                print("   Clinical Recommendations:")
                for rec in recommendations[:2]:  # Show top 2 recommendations
                    print(f"   • {rec}")
            print()
        
        # Final Assessment
        triage = result.get("triage_level", "Not determined")
        print(f"🚨 TRIAGE LEVEL: {triage}")
        
        # Report Summary
        report = result.get("final_report", "")
        if report:
            print("📋 DIAGNOSTIC SUMMARY:")
            # Show first few lines of the report
            report_lines = report.split('\n')[:4]
            for line in report_lines:
                if line.strip():
                    print(f"   {line.strip()}")
            if len(report.split('\n')) > 4:
                print("   [... full report available in system ...]")
        
        print()
        print("✅ Case completed successfully!")
        print()

async def main():
    """
    Main entry point for the AURA demo.
    
    This function sets up and runs the complete demonstration.
    It's designed to be run from the command line to showcase AURA's capabilities.
    """
    try:
        demo = AURADemo()
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the demo
    print("Starting AURA Diagnostic System Demo...")
    print("Press Ctrl+C to stop at any time")
    print()
    
    asyncio.run(main())