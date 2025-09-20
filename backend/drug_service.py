"""
Drug Service Module

This module provides functionality to check drug interactions and contraindications
based on patient conditions and medical history.
"""

import json
import os
import re

class DrugService:
    """
    Service for checking drug interactions and providing treatment suggestions
    based on patient conditions and medical history.
    """
    
    def __init__(self):
        """
        Initialize the DrugService by loading the drug database from JSON.
        Handles FileNotFoundError if the database file doesn't exist.
        """
        try:
            # Construct the path to the drug database JSON file
            file_path = os.path.join(os.path.dirname(__file__), 'data', 'drug_database.json')
            
            # Load and parse the JSON file
            with open(file_path, 'r') as file:
                self.drug_data = json.load(file)
                
        except FileNotFoundError:
            print("Warning: Drug database file not found. Service will operate with empty data.")
            self.drug_data = {}
        except json.JSONDecodeError:
            print("Warning: Invalid JSON in drug database file. Service will operate with empty data.")
            self.drug_data = {}
    
    def check_interactions(self, conditions, patient_history):
        """
        Check for drug interactions based on patient conditions and medical history.
        
        Args:
            conditions (list): List of medical conditions as strings
            patient_history (str): Patient's medical history as a single string
            
        Returns:
            dict: Dictionary with 'suggestions' and 'warnings' lists
        """
        suggestions = []
        warnings = []
        
        # Convert patient_history to lowercase for case-insensitive matching
        patient_history_lower = patient_history.lower()
        
        # Iterate through each condition
        for condition in conditions:
            # Skip if condition is not in our database
            if condition not in self.drug_data:
                continue
                
            # Get data for this condition
            condition_data = self.drug_data[condition]
            
            # Add common treatments to suggestions
            if "common_treatments" in condition_data:
                suggestions.extend(condition_data["common_treatments"])
            
            # Check for contraindications
            if "contraindications" in condition_data:
                for keyword, warning in condition_data["contraindications"].items():
                    # Case-insensitive check for keyword in patient history
                    if keyword.lower() in patient_history_lower:
                        # Add the condition and warning to the warnings list
                        warnings.append(f"{condition}: {warning}")
        
        # Return results as a dictionary
        return {
            "suggestions": suggestions,
            "warnings": warnings
        }


# Main execution block for testing
if __name__ == "__main__":
    # Create an instance of the DrugService
    drug_service = DrugService()
    
    # Example test case
    conditions = ["Hypertension", "Type 2 Diabetes"]
    patient_history = "Patient has a history of renal failure and asthma. No known drug allergies."
    
    # Check for interactions
    result = drug_service.check_interactions(conditions, patient_history)
    
    # Display the results
    print("Drug Interaction Check Results:")
    print("\nSuggested Treatments:")
    for suggestion in result["suggestions"]:
        print(f"- {suggestion}")
    
    print("\nWarnings:")
    if result["warnings"]:
        for warning in result["warnings"]:
            print(f"- {warning}")
    else:
        print("- No warnings found.")