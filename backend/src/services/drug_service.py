"""
AURA Diagnostics - Drug Interaction Service

This service provides drug interaction checking and safety warnings.
It's the final safety net in our diagnostic workflow - we want to catch
any potential drug interactions before they become a problem.

Why this matters:
- Drug interactions can be life-threatening
- Patients often don't tell doctors about all their medications
- AI can help catch interactions that humans might miss
- This is a critical safety feature for medical AI

Note: This is a simplified implementation. In production, you'd want to
integrate with a comprehensive drug database like DrugBank or FDA APIs.
"""

from typing import List, Dict, Any, Optional
import re

class DrugService:
    """
    Handles drug interaction checking and safety warnings.
    
    This is a basic implementation that looks for common drug interaction patterns.
    In a real medical system, you'd integrate with professional drug databases.
    """
    
    def __init__(self):
        """
        Initialize the drug service with common interaction patterns.
        
        These are simplified examples - real drug interaction checking
        requires comprehensive pharmaceutical databases and complex logic.
        """
        
        # Common drug interaction patterns to watch for
        # In production, this would be a proper database with thousands of interactions
        self.interaction_patterns = {
            "blood_thinners": {
                "keywords": ["warfarin", "heparin", "aspirin", "clopidogrel", "anticoagulant"],
                "warning": "Blood thinning medications require careful monitoring when combined with other treatments."
            },
            "diabetes_meds": {
                "keywords": ["insulin", "metformin", "diabetes", "diabetic", "blood sugar"],
                "warning": "Diabetes medications may need adjustment based on new treatments or conditions."
            },
            "heart_meds": {
                "keywords": ["beta blocker", "ace inhibitor", "cardiac", "heart medication", "hypertension"],
                "warning": "Heart medications can interact with many other drugs and may affect treatment options."
            },
            "antibiotics": {
                "keywords": ["antibiotic", "penicillin", "amoxicillin", "infection treatment"],
                "warning": "Antibiotics can affect the absorption and effectiveness of other medications."
            }
        }
        
        # Common conditions that affect drug metabolism
        self.condition_warnings = {
            "kidney": ["kidney disease", "renal", "dialysis"],
            "liver": ["liver disease", "hepatic", "cirrhosis"],
            "heart": ["heart failure", "cardiac", "arrhythmia"]
        }
    
    def check_interactions(self, potential_conditions: List[str], patient_history: str = "") -> Dict[str, Any]:
        """
        Check for potential drug interactions based on conditions and patient history.
        
        This analyzes the diagnostic results and patient history to identify
        potential drug interaction risks that doctors should be aware of.
        
        Args:
            potential_conditions: List of potential diagnoses from the AI
            patient_history: Patient's medical history text
            
        Returns:
            Dictionary with warnings and recommendations
        """
        
        warnings = []
        recommendations = []
        
        # Combine all text to search for drug-related keywords
        all_text = " ".join(potential_conditions) + " " + patient_history
        all_text = all_text.lower()
        
        # Check for drug interaction patterns
        for category, pattern_info in self.interaction_patterns.items():
            for keyword in pattern_info["keywords"]:
                if keyword in all_text:
                    warnings.append(pattern_info["warning"])
                    break  # Only add the warning once per category
        
        # Check for conditions that affect drug metabolism
        for condition, keywords in self.condition_warnings.items():
            for keyword in keywords:
                if keyword in all_text:
                    if condition == "kidney":
                        warnings.append("Kidney function may affect drug dosing - consider renal function tests.")
                    elif condition == "liver":
                        warnings.append("Liver function may affect drug metabolism - monitor liver enzymes.")
                    elif condition == "heart":
                        warnings.append("Heart condition may limit treatment options - cardiology consultation recommended.")
                    break
        
        # Look for multiple medication mentions (polypharmacy risk)
        medication_count = self._count_medication_mentions(all_text)
        if medication_count >= 3:
            warnings.append(f"Patient appears to be on multiple medications ({medication_count} detected) - increased risk of drug interactions.")
        
        # Generate recommendations based on warnings
        if warnings:
            recommendations.extend([
                "Review complete medication list with patient",
                "Consider pharmacist consultation for drug interaction screening",
                "Monitor for signs of adverse drug reactions"
            ])
        
        return {
            "warnings": warnings,
            "recommendations": recommendations,
            "interaction_risk": "HIGH" if len(warnings) >= 2 else "MODERATE" if warnings else "LOW"
        }
    
    def _count_medication_mentions(self, text: str) -> int:
        """
        Count how many medication-related terms appear in the text.
        
        This gives us a rough estimate of polypharmacy risk.
        More medications = higher chance of interactions.
        """
        
        # Common medication-related terms
        med_terms = [
            "medication", "medicine", "drug", "pill", "tablet", "capsule",
            "prescription", "dose", "dosage", "mg", "ml", "treatment",
            "therapy", "taking", "prescribed"
        ]
        
        count = 0
        for term in med_terms:
            count += len(re.findall(r'\b' + term + r'\b', text, re.IGNORECASE))
        
        return count
    
    def get_safety_recommendations(self, diagnosis_text: str) -> List[str]:
        """
        Get general safety recommendations based on the diagnosis.
        
        This provides standard safety advice that applies to most medical treatments.
        Think of it as the "fine print" that should always be mentioned.
        """
        
        recommendations = [
            "Inform all healthcare providers about current medications and supplements",
            "Report any unusual symptoms or side effects immediately",
            "Do not stop or change medications without consulting your doctor"
        ]
        
        # Add specific recommendations based on diagnosis content
        diagnosis_lower = diagnosis_text.lower()
        
        if any(term in diagnosis_lower for term in ["pain", "analgesic", "nsaid"]):
            recommendations.append("Be cautious with over-the-counter pain medications - they can interact with prescriptions")
        
        if any(term in diagnosis_lower for term in ["infection", "antibiotic"]):
            recommendations.append("Complete the full course of any prescribed antibiotics, even if feeling better")
        
        if any(term in diagnosis_lower for term in ["chronic", "long-term", "ongoing"]):
            recommendations.append("Regular follow-up appointments are essential for chronic conditions")
        
        return recommendations