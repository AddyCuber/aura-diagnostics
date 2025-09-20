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

Note: This implementation supports both JSON database loading and fallback
to in-memory patterns. In production, you'd integrate with comprehensive
drug databases like DrugBank or FDA APIs.
"""

from typing import List, Dict, Any, Optional
import json
import os
import re

class DrugService:
    """
    Handles drug interaction checking and safety warnings.
    
    This service can load drug data from JSON files or fall back to
    built-in interaction patterns. It provides comprehensive drug
    interaction checking and safety recommendations.
    """
    
    def __init__(self):
        """
        Initialize the drug service with drug database and interaction patterns.
        
        First tries to load from JSON database, then falls back to built-in patterns.
        This gives us flexibility - we can use external data when available,
        but still function with basic patterns if the database isn't ready.
        """
        
        # Try to load external drug database first
        self.drug_data = self._load_drug_database()
        
        # Built-in interaction patterns as fallback/supplement
        # These work alongside the JSON database for comprehensive coverage
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
        # These are medical facts that don't change much, so keeping them in-memory is fine
        self.condition_warnings = {
            "kidney": ["kidney disease", "renal", "dialysis"],
            "liver": ["liver disease", "hepatic", "cirrhosis"],
            "heart": ["heart failure", "cardiac", "arrhythmia"]
        }
    
    def _load_drug_database(self) -> Dict[str, Any]:
        """
        Load drug database from JSON file if available.
        
        This allows us to use external drug databases while gracefully
        handling cases where the file doesn't exist or is malformed.
        """
        try:
            # Look for drug database in the backend/data directory
            # Go up from src/services to backend, then into data
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            file_path = os.path.join(backend_dir, 'data', 'drug_database.json')
            
            with open(file_path, 'r') as file:
                drug_data = json.load(file)
                print(f"Loaded drug database with {len(drug_data)} entries")
                return drug_data
                
        except FileNotFoundError:
            print("Info: Drug database file not found. Using built-in patterns only.")
            return {}
        except json.JSONDecodeError:
            print("Warning: Invalid JSON in drug database file. Using built-in patterns only.")
            return {}
        except Exception as e:
            print(f"Warning: Error loading drug database: {e}. Using built-in patterns only.")
            return {}
    
    def check_interactions(self, conditions: List[str], patient_history: str = "") -> Dict[str, Any]:
        """
        Check for drug interactions using both JSON database and built-in patterns.
        
        This combines the flexibility of external databases with the reliability
        of built-in patterns. We get the best of both approaches.
        
        Args:
            conditions: List of medical conditions or potential diagnoses
            patient_history: Patient's medical history as text
            
        Returns:
            Dictionary with warnings, suggestions, and risk assessment
        """
        
        warnings = []
        suggestions = []
        recommendations = []
        
        # Convert to lowercase for case-insensitive matching
        patient_history_lower = patient_history.lower()
        all_text = " ".join(conditions) + " " + patient_history
        all_text_lower = all_text.lower()
        
        # Check JSON database first (if loaded)
        if self.drug_data:
            for condition in conditions:
                if condition in self.drug_data:
                    condition_data = self.drug_data[condition]
                    
                    # Add treatment suggestions from database
                    if "common_treatments" in condition_data:
                        suggestions.extend(condition_data["common_treatments"])
                    
                    # Check contraindications from database
                    if "contraindications" in condition_data:
                        for keyword, warning in condition_data["contraindications"].items():
                            if keyword.lower() in patient_history_lower:
                                warnings.append(f"{condition}: {warning}")
        
        # Check built-in interaction patterns (always run for comprehensive coverage)
        for category, pattern_info in self.interaction_patterns.items():
            for keyword in pattern_info["keywords"]:
                if keyword in all_text_lower:
                    warnings.append(pattern_info["warning"])
                    break  # Only add once per category
        
        # Check for conditions affecting drug metabolism
        for condition, keywords in self.condition_warnings.items():
            for keyword in keywords:
                if keyword in all_text_lower:
                    if condition == "kidney":
                        warnings.append("Kidney function may affect drug dosing - consider renal function tests.")
                    elif condition == "liver":
                        warnings.append("Liver function may affect drug metabolism - monitor liver enzymes.")
                    elif condition == "heart":
                        warnings.append("Heart condition may limit treatment options - cardiology consultation recommended.")
                    break
        
        # Check for polypharmacy risk (multiple medications)
        medication_count = self._count_medication_mentions(all_text_lower)
        if medication_count >= 3:
            warnings.append(f"Patient appears to be on multiple medications ({medication_count} detected) - increased risk of drug interactions.")
        
        # Generate standard recommendations if we found any issues
        if warnings or suggestions:
            recommendations.extend([
                "Review complete medication list with patient",
                "Consider pharmacist consultation for drug interaction screening",
                "Monitor for signs of adverse drug reactions"
            ])
        
        # Determine risk level based on findings
        risk_level = "HIGH" if len(warnings) >= 2 else "MODERATE" if warnings else "LOW"
        
        return {
            "suggestions": list(set(suggestions)),  # Remove duplicates
            "warnings": warnings,
            "recommendations": recommendations,
            "interaction_risk": risk_level
        }
    
    def _count_medication_mentions(self, text: str) -> int:
        """
        Count medication-related terms to assess polypharmacy risk.
        
        More medications = higher chance of interactions.
        This is a simple heuristic but surprisingly effective.
        """
        
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
        Get general safety recommendations based on diagnosis.
        
        These are the "always mention this" safety tips that apply
        to most medical situations. Think of it as the fine print.
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


# Main execution block for testing
if __name__ == "__main__":
    # Create an instance of the DrugService
    drug_service = DrugService()
    
    # Example test case
    conditions = ["Hypertension", "Type 2 Diabetes"]
    patient_history = "Patient has a history of renal failure and asthma. Taking warfarin and metformin daily."
    
    # Check for interactions
    result = drug_service.check_interactions(conditions, patient_history)
    
    # Display the results
    print("Drug Interaction Check Results:")
    print(f"Risk Level: {result['interaction_risk']}")
    
    print("\nSuggested Treatments:")
    for suggestion in result["suggestions"]:
        print(f"- {suggestion}")
    
    print("\nWarnings:")
    if result["warnings"]:
        for warning in result["warnings"]:
            print(f"- {warning}")
    else:
        print("- No warnings found.")
    
    print("\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"- {rec}")