#!/usr/bin/env python3
"""
Script to load medical case studies from JSON into ChromaDB collection.

This script reads case studies from a JSON file and loads them into a ChromaDB
collection for vector search capabilities. It maps the case_id, full_text, title,
keywords, and outcome fields from the JSON to the appropriate ChromaDB fields.
"""
import json
import os
import sys
import chromadb
from chromadb.utils import embedding_functions

def load_cases():
    """
    Load medical case studies from JSON file into ChromaDB collection.
    
    Returns:
        bool: True if loading was successful, False otherwise
    """
    try:
        # Define the path to the data file
        data_path = os.path.join(os.path.dirname(__file__), "data", "case_studies.json")
        
        # Check if the data file exists
        if not os.path.exists(data_path):
            print(f"Error: Data file not found at {data_path}")
            return False
        
        # Create chroma_db directory if it doesn't exist
        chroma_db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        os.makedirs(chroma_db_path, exist_ok=True)
        
        # Initialize a persistent ChromaDB client
        client = chromadb.PersistentClient(chroma_db_path)
        
        # Get or create a collection with default embedding function
        embedding_function = embedding_functions.DefaultEmbeddingFunction()
        collection = client.get_or_create_collection(
            name="medical_cases",
            embedding_function=embedding_function
        )
        
        # Read and parse the JSON data
        with open(data_path, 'r') as file:
            try:
                cases = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON format in {data_path}: {e}")
                return False
        
        # Validate that cases is a list
        if not isinstance(cases, list):
            print(f"Error: Expected a JSON array in {data_path}, got {type(cases).__name__}")
            return False
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for i, case in enumerate(cases):
            try:
                # Validate required fields
                required_fields = ["case_id", "full_text", "title", "keywords", "outcome"]
                for field in required_fields:
                    if field not in case:
                        print(f"Error: Missing required field '{field}' in case at index {i}")
                        continue
                
                # Map case_id to ids list
                ids.append(case["case_id"])
                
                # Map full_text to documents list
                documents.append(case["full_text"])
                
                # Map title, keywords, and outcome to metadatas list
                # Join keywords list into a comma-separated string
                metadata = {
                    "title": case["title"],
                    "keywords": ", ".join(case["keywords"]) if isinstance(case["keywords"], list) else case["keywords"],
                    "outcome": case["outcome"]
                }
                metadatas.append(metadata)
            except Exception as e:
                print(f"Error processing case at index {i}: {e}")
        
        # Add the prepared data to the collection
        if ids:
            try:
                collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                
                # Get the total count in the collection
                total_count = len(collection.get()["ids"])
                
                # Print confirmation message
                print(f"Successfully loaded {len(ids)} cases. Total cases in collection: {total_count}")
                return True
            except Exception as e:
                print(f"Error adding data to collection: {e}")
                return False
        else:
            print("No valid cases found to load.")
            return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = load_cases()
    sys.exit(0 if success else 1)