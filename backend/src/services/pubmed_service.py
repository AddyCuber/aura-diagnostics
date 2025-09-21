# backend/src/services/pubmed_service.py
import requests
import time
import os
from typing import List, Dict
import xml.etree.ElementTree as ET


class PubMedService:
    """
    Handles all interactions with the PubMed E-utilities API.
    
    This service encapsulates all the messy details of talking to PubMed's API.
    Why separate this? Because PubMed's API is quirky and changes sometimes.
    Having it in one place makes it easier to maintain and test.
    
    The workflow is always: search() to get PMIDs, then fetch_abstracts() to get content.
    """
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # Load configuration from environment variables
        # PubMed requires an email for API access - it's how they track usage and contact you if needed
        # If no email is set in .env, we'll fall back to a default (but you should set your real email!)
        self.email = os.getenv("PUBMED_EMAIL", "aura-hackathon@example.com")
        
        # API key is optional but recommended for production
        # With an API key, you get higher rate limits (10 requests/second vs 3)
        # Get one free from: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
        self.api_key = os.getenv("PUBMED_API_KEY")
        
        # Rate limiting - how many requests per second we can make
        # 3/sec without API key, 10/sec with API key
        self.rate_limit = float(os.getenv("PUBMED_RATE_LIMIT", "3"))
        self.last_request_time = 0
        
    def search(self, query: str, max_results: int = 10) -> List[str]:
        """
        Searches PubMed and returns a list of article IDs (PMIDs).
        
        This is step 1 of the PubMed workflow. We send a search query and get back
        a list of PMIDs (PubMed IDs) that match. No actual article content yet.
        
        Args:
            query: Search terms (e.g., "chest pain diagnosis")
            max_results: How many PMIDs to return (default 10)
            
        Returns:
            List of PMID strings, or empty list if search fails
        """
        # Respect rate limiting - don't hammer PubMed's servers
        self._rate_limit()
        
        print(f"--> PubMed DEBUG: Executing search with query: '{query}'")
        
        # Build the request parameters
        # The 'tool' and 'email' params are required by PubMed for tracking
        params = {
            "db": "pubmed", 
            "term": query, 
            "retmax": max_results,
            "retmode": "json", 
            "email": self.email, 
            "tool": "aura_diagnostics"
        }
        
        # Add API key if we have one - this gets us higher rate limits
        if self.api_key:
            params["api_key"] = self.api_key
            
        print(f"--> PubMed DEBUG: Request params: {params}")
            
        try:
            response = requests.get(f"{self.base_url}esearch.fcgi", params=params)
            print(f"--> PubMed DEBUG: Received status code {response.status_code}")
            
            # Add this to see the raw response if it fails
            if response.status_code != 200:
                print(f"--> PubMed DEBUG: Error response text: {response.text}")
                
            response.raise_for_status()
            
            # Parse the JSON response and extract PMIDs
            json_response = response.json()
            print(f"--> PubMed DEBUG: Full JSON response: {json_response}")
            
            pmids = json_response["esearchresult"]["idlist"]
            print(f"--> PubMed DEBUG: Found {len(pmids)} PMIDs: {pmids}")
            return pmids
        except Exception as e:
            print(f"--> PubMed DEBUG: Exception occurred: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []

    def fetch_abstracts(self, pmids: List[str]) -> List[Dict]:
        """
        Fetches full abstracts for a list of PMIDs.
        
        This is step 2 of the PubMed workflow. We take the PMIDs from search()
        and get the actual article titles, abstracts, and metadata.
        
        Args:
            pmids: List of PMID strings from search()
            
        Returns:
            List of dicts with keys: pmid, title, abstract, authors, journal
        """
        if not pmids:
            return []
            
        # Respect rate limiting
        self._rate_limit()
        
        print(f"PubMedService: Fetching abstracts for {len(pmids)} PMIDs...")
        
        # Build request parameters
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "email": self.email,
            "tool": "aura_diagnostics"
        }
        
        # Add API key if available
        if self.api_key:
            params["api_key"] = self.api_key
            
        try:
            response = requests.get(f"{self.base_url}efetch.fcgi", params=params)
            response.raise_for_status()
            
            # Parse the XML response
            root = ET.fromstring(response.content)
            articles = self._parse_xml(root)
            print(f"PubMedService: Successfully parsed {len(articles)} articles.")
            return articles
            
        except Exception as e:
            print(f"PubMedService Error fetching abstracts: {e}")
            return []

    def _parse_xml(self, root) -> List[Dict]:
        """
        Helper to parse the XML from PubMed.
        
        PubMed returns XML that's... not the most friendly to work with.
        This method digs through the XML structure to extract what we need:
        PMID, title, and abstract.
        
        Now returns structured evidence format with proper source_id for traceability.
        Each article gets formatted as evidence with confidence score and source citation.
        
        FIXED: Now handles articles with missing abstracts gracefully by including
        them with a placeholder abstract instead of skipping them entirely.
        
        Args:
            root: XML root element from PubMed response
            
        Returns:
            List of parsed article dictionaries with source_id format
        """
        parsed_articles = []
        for article in root.findall(".//PubmedArticle"):
            try:
                pmid_elem = article.find(".//PMID")
                title_elem = article.find(".//ArticleTitle")
                abstract_elem = article.find(".//Abstract/AbstractText")

                # Only require PMID and title - handle missing abstracts gracefully
                if pmid_elem is not None and title_elem is not None:
                    pmid = pmid_elem.text
                    title = title_elem.text
                    
                    # Handle missing abstracts properly - check if element exists AND has text
                    if abstract_elem is not None and abstract_elem.text:
                        abstract = abstract_elem.text
                        confidence = 0.8  # Full confidence for complete articles
                    else:
                        abstract = "Abstract not available"
                        confidence = 0.6  # Lower confidence for missing abstracts
                    
                    # Format as structured evidence with proper source_id for traceability
                    parsed_articles.append({
                        "pmid": pmid,
                        "title": title,
                        "abstract": abstract,
                        "source_id": f"PMID:{pmid}",  # Critical: proper source_id format
                        "text": f"Title: {title}\nAbstract: {abstract}",
                        "confidence": confidence
                    })
            except Exception:
                # Skip malformed articles rather than crash the whole batch
                continue
        return parsed_articles
    
    def _rate_limit(self):
        """
        Simple rate limiting to be respectful to PubMed's servers.
        
        PubMed allows 3 requests per second without an API key,
        10 requests per second with an API key. We use the rate_limit
        from environment variables to control this.
        
        The sleep time is calculated as 1/rate_limit seconds.
        """
        sleep_time = 1.0 / self.rate_limit
        time.sleep(sleep_time)