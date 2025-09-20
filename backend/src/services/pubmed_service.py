# backend/src/services/pubmed_service.py
import requests
import time
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
        self.email = "aura-hackathon@example.com"  # PubMed requires this for rate limiting
        
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
        print(f"PubMedService: Searching for '{query}'...")
        params = {
            "db": "pubmed", "term": query, "retmax": max_results,
            "retmode": "json", "email": self.email, "tool": "aura_diagnostics"
        }
        try:
            response = requests.get(f"{self.base_url}esearch.fcgi", params=params)
            response.raise_for_status()
            pmids = response.json()["esearchresult"]["idlist"]
            print(f"PubMedService: Found {len(pmids)} PMIDs.")
            return pmids
        except Exception as e:
            print(f"PubMedService Error searching: {e}")
            return []

    def fetch_abstracts(self, pmids: List[str]) -> List[Dict]:
        """
        Fetches and parses abstracts for a list of PMIDs.
        
        This is step 2 of the PubMed workflow. We take the PMIDs from search()
        and fetch the actual article content (title, abstract, etc.).
        
        We batch the requests because PubMed gets angry if you ask for too many
        articles at once. The 0.3 second sleep is to be nice to their servers.
        
        Args:
            pmids: List of PMID strings from search()
            
        Returns:
            List of article dictionaries with pmid, title, abstract
        """
        if not pmids:
            return []
        print(f"PubMedService: Fetching abstracts for {len(pmids)} PMIDs...")
        articles = []
        batch_size = 20  # PubMed's recommended batch size
        
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i + batch_size]
            params = {
                "db": "pubmed", "id": ",".join(batch), "retmode": "xml",
                "email": self.email, "tool": "aura_diagnostics"
            }
            try:
                response = requests.get(f"{self.base_url}efetch.fcgi", params=params)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                articles.extend(self._parse_xml(root))
                time.sleep(0.3)  # Be nice to PubMed's servers
            except Exception as e:
                print(f"PubMedService Error fetching batch: {e}")
        return articles

    def _parse_xml(self, root) -> List[Dict]:
        """
        Helper to parse the XML from PubMed.
        
        PubMed returns XML that's... not the most friendly to work with.
        This method digs through the XML structure to extract what we need:
        PMID, title, and abstract.
        
        If any article is missing required fields, we skip it rather than
        crash the whole batch. Better to get some articles than none.
        
        Args:
            root: XML root element from PubMed response
            
        Returns:
            List of parsed article dictionaries
        """
        parsed_articles = []
        for article in root.findall(".//PubmedArticle"):
            try:
                pmid_elem = article.find(".//PMID")
                title_elem = article.find(".//ArticleTitle")
                abstract_elem = article.find(".//Abstract/AbstractText")

                if pmid_elem is not None and title_elem is not None and abstract_elem is not None:
                    parsed_articles.append({
                        "pmid": pmid_elem.text,
                        "title": title_elem.text,
                        "abstract": abstract_elem.text,
                    })
            except Exception:
                # Skip malformed articles rather than crash the whole batch
                continue
        return parsed_articles