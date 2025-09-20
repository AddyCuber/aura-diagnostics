"""
AURA Diagnostics - PubMed API Health Check

This is a simple, standalone script to verify that we can connect to the
NCBI PubMed E-utilities API and get a valid response.

Run this from your terminal to quickly debug connection issues:
$ python check_pubmed.py
"""
import requests
import json

def check_pubmed_api():
    """
    Performs a quick health check of the PubMed API.
    
    1. Makes a simple search request for a common term ("aspirin").
    2. Checks for a successful HTTP status code (200).
    3. Validates that the response is valid JSON and contains search results.
    
    Prints a clear success or failure message.
    """
    print("🩺 Running PubMed API Health Check...")

    # --- Configuration ---
    # We use the esearch utility, which is the simplest way to test connectivity.
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Parameters for a simple, low-impact query
    params = {
        "db": "pubmed",
        "term": "aspirin",  # A common term guaranteed to have results
        "retmax": 1,        # We only need one result to confirm it works
        "retmode": "json",
        "tool": "aura_diagnostics_healthcheck",
        "email": "your-email@example.com"  # Be a good internet citizen
    }

    try:
        # --- 1. Attempt to connect to the API ---
        print("    - Step 1: Connecting to PubMed server...")
        response = requests.get(search_url, params=params, timeout=10)  # 10-second timeout
        print(f"    - ... Connection successful with Status Code: {response.status_code}")

        # --- 2. Check the HTTP Status Code ---
        print("    - Step 2: Verifying HTTP response...")
        response.raise_for_status()  # This will raise an exception for non-2xx status codes
        print("    - ... HTTP status OK (200).")

        # --- 3. Validate the JSON Response ---
        print("    - Step 3: Parsing and validating JSON data...")
        data = response.json()
        
        # A valid response will have this structure
        if "esearchresult" in data and "idlist" in data["esearchresult"] and len(data["esearchresult"]["idlist"]) > 0:
            pmid = data["esearchresult"]["idlist"][0]
            print(f"    - ... JSON is valid. Found at least one article (PMID: {pmid}).")
        else:
            raise ValueError("Response JSON is not in the expected format or contains no results.")

        # --- Success ---
        print("\n✅ SUCCESS: The PubMed API is online and responding correctly.")

    except requests.exceptions.RequestException as e:
        print("\n❌ FAILURE: Could not connect to the PubMed API.")
        print(f"    - Error Type: Connection Error")
        print(f"    - Details: {e}")
        print("    - Check your internet connection and firewall settings.")

    except ValueError as e:
        print("\n❌ FAILURE: The API responded, but the data was not in the expected format.")
        print(f"    - Error Type: Data Validation Error")
        print(f"    - Details: {e}")
        print("    - PubMed may have changed its API format, or the service may be having issues.")
        
    except Exception as e:
        print("\n❌ FAILURE: An unexpected error occurred.")
        print(f"    - Error Type: General Error")
        print(f"    - Details: {e}")

if __name__ == "__main__":
    check_pubmed_api()