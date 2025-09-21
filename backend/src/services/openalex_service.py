# backend/src/services/openalex_service.py
import pyalex
from pyalex import Works
import time
from typing import List, Dict
import logging

# Set up logging for debugging - helps us see what's happening when things go wrong
logger = logging.getLogger(__name__)


class OpenAlexService:
    """
    Handles all interactions with the OpenAlex API for academic literature search.
    
    OpenAlex is like PubMed but broader - it covers all academic disciplines, not just medicine.
    It's free, open, and has a really nice API. Perfect complement to PubMed.
    
    Why use this alongside PubMed?
    - OpenAlex has more recent papers (faster indexing)
    - Covers interdisciplinary research that might not be in PubMed
    - Has better metadata (citations, author affiliations, etc.)
    - Free and no rate limits (within reason)
    
    The workflow is simple: search() returns complete paper info in one go.
    No need for separate PMID fetching like PubMed.
    """
    
    def __init__(self):
        # OpenAlex doesn't require API keys or email - it's completely open
        # But we should still be polite with our requests
        self.rate_limit = 10  # requests per second - being conservative
        self.last_request_time = 0
        
        # Configure pyalex - set a polite user agent so they know who's calling
        pyalex.config.email = "aura-diagnostics@example.com"  # Replace with real email in production
        
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Searches OpenAlex and returns complete paper information.
        
        Unlike PubMed, OpenAlex gives us everything in one API call - no need to 
        fetch abstracts separately. This makes it faster and simpler.
        
        Args:
            query: Search terms (e.g., "chest pain diagnosis")
            max_results: How many papers to return (default 10)
            
        Returns:
            List of paper dictionaries with title, abstract, DOI, etc.
            Empty list if search fails or no results found.
        """
        try:
            self._rate_limit()
            
            # Search OpenAlex using their Works API
            # We filter for papers that have abstracts (no point in papers without them)
            # and are in English (for now - could expand this later)
            works = Works().search(query).filter(
                has_abstract=True,
                language="en"
            ).get(per_page=max_results)
            
            papers = []
            for work in works:
                # Extract the info we need for our diagnostic system
                paper_info = self._extract_paper_info(work)
                if paper_info:  # Only add if we successfully extracted info
                    papers.append(paper_info)
                    
            logger.info(f"OpenAlex search for '{query}' returned {len(papers)} papers")
            return papers
            
        except Exception as e:
            # If OpenAlex fails, we don't want to crash the whole system
            # Log the error and return empty list - the system can still work with just PubMed
            logger.error(f"OpenAlex search failed for query '{query}': {str(e)}")
            return []
    
    def _extract_paper_info(self, work) -> Dict:
        """
        Extracts the information we need from an OpenAlex work object.
        
        OpenAlex returns a lot of metadata - we only need the essentials for our diagnostic system.
        This keeps our data structure consistent with what PubMed returns.
        
        Args:
            work: OpenAlex work object
            
        Returns:
            Dictionary with paper info, or None if extraction fails
        """
        try:
            # Get the basic info - title and abstract are essential
            title = work.get('title', 'No title available')
            
            # OpenAlex stores abstracts as inverted indexes, not plain text
            # We need to reconstruct the abstract from the word positions
            abstract = self._reconstruct_abstract(work.get('abstract_inverted_index'))
            
            # Skip papers without meaningful abstracts
            if not abstract or len(abstract.strip()) < 50:
                return None
                
            # Get identifiers - DOI is preferred, but OpenAlex ID works too
            doi = work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else None
            openalex_id = work.get('id', '').replace('https://openalex.org/', '') if work.get('id') else None
            
            # Get publication info
            publication_date = work.get('publication_date', 'Unknown date')
            journal = 'Unknown journal'
            if work.get('primary_location') and work['primary_location'].get('source'):
                journal = work['primary_location']['source'].get('display_name', 'Unknown journal')
            
            # Get authors - format them nicely
            authors = []
            if work.get('authorships'):
                for authorship in work['authorships'][:5]:  # Limit to first 5 authors
                    if authorship.get('author') and authorship['author'].get('display_name'):
                        authors.append(authorship['author']['display_name'])
            
            authors_str = ', '.join(authors) if authors else 'Unknown authors'
            if len(work.get('authorships', [])) > 5:
                authors_str += ' et al.'
            
            return {
                'title': title,
                'abstract': abstract,
                'authors': authors_str,
                'journal': journal,
                'publication_date': publication_date,
                'doi': doi,
                'openalex_id': openalex_id,
                'source': 'OpenAlex',  # Mark the source so we can track where papers came from
                'url': f"https://doi.org/{doi}" if doi else f"https://openalex.org/{openalex_id}"
            }
            
        except Exception as e:
            logger.error(f"Failed to extract paper info from OpenAlex work: {str(e)}")
            return None
    
    def _rate_limit(self):
        """
        Simple rate limiting to be respectful to OpenAlex API.
        
        OpenAlex allows 10 requests per second for the free tier.
        We'll be conservative and wait 0.2 seconds between requests.
        """
        current_time = time.time()
        if hasattr(self, 'last_request_time'):
            time_since_last = current_time - self.last_request_time
            if time_since_last < 0.2:  # 200ms between requests = 5 requests/second
                time.sleep(0.2 - time_since_last)
        
        self.last_request_time = time.time()
    
    def _reconstruct_abstract(self, inverted_index) -> str:
        """
        Reconstructs a readable abstract from OpenAlex's inverted index format.
        
        OpenAlex stores abstracts as {word: [position1, position2, ...]} to save space.
        We need to flip this back to get the original text.
        
        Args:
            inverted_index: Dictionary mapping words to their positions in the abstract
            
        Returns:
            Reconstructed abstract text, or empty string if no index provided
        """
        if not inverted_index:
            return ""
            
        try:
            # Create a list to hold words in their correct positions
            # Find the maximum position to know how long our list should be
            max_position = 0
            for positions in inverted_index.values():
                if positions:  # Some entries might be empty lists
                    max_position = max(max_position, max(positions))
            
            # Initialize list with empty strings
            words = [""] * (max_position + 1)
            
            # Place each word in its correct position(s)
            for word, positions in inverted_index.items():
                for pos in positions:
                    if 0 <= pos <= max_position:  # Safety check
                        words[pos] = word
            
            # Join the words, filtering out any empty positions
            abstract = " ".join(word for word in words if word)
            return abstract
            
        except Exception as e:
            logger.error(f"Failed to reconstruct abstract from inverted index: {str(e)}")
            return ""