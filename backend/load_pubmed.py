"""
AURA Diagnostics - PubMed Data Loader

This script downloads medical abstracts from PubMed and loads them into ChromaDB.
Our AI agents will use this knowledge base to find relevant medical literature
to support their diagnostic suggestions.

Why PubMed? It's the gold standard for medical literature. Free access to abstracts,
and the content is peer-reviewed and reliable.

Why ChromaDB? It's designed for AI applications. Handles embeddings automatically,
fast similarity search, and easy to use with LangChain.

Run this script to populate your knowledge base: python load_pubmed.py
"""

import requests
import time
import json
from typing import List, Dict
import chromadb
from chromadb.config import Settings
import xml.etree.ElementTree as ET
from datetime import datetime

class PubMedLoader:
    """
    Handles downloading and processing PubMed abstracts.
    
    Uses the free PubMed E-utilities API to search and download abstracts.
    No API key required for basic usage, but be respectful with rate limits.
    """
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = "your-email@example.com"  # PubMed asks for this for tracking
        
    def search_pubmed(self, query: str, max_results: int = 1000) -> List[str]:
        """
        Search PubMed for articles matching the query.
        
        Returns a list of PubMed IDs (PMIDs) that we can use to fetch full abstracts.
        
        Args:
            query: Search terms (e.g., "pediatric respiratory infections")
            max_results: Maximum number of articles to return
        """
        print(f"Searching PubMed for: '{query}'")
        
        # Build the search URL
        search_url = f"{self.base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email,
            "tool": "aura_diagnostics"
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            pmids = data["esearchresult"]["idlist"]
            
            print(f"Found {len(pmids)} articles")
            return pmids
            
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def fetch_abstracts(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch full abstracts for a list of PubMed IDs.
        
        Returns a list of dictionaries with article metadata and abstracts.
        We'll process these in batches to be nice to PubMed's servers.
        """
        print(f"Fetching abstracts for {len(pmids)} articles...")
        
        articles = []
        batch_size = 50  # Process 50 articles at a time
        
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(pmids)-1)//batch_size + 1}")
            
            # Fetch this batch
            fetch_url = f"{self.base_url}efetch.fcgi"
            params = {
                "db": "pubmed",
                "id": ",".join(batch),
                "retmode": "xml",
                "email": self.email,
                "tool": "aura_diagnostics"
            }
            
            try:
                response = requests.get(fetch_url, params=params)
                response.raise_for_status()
                
                # Parse the XML response
                root = ET.fromstring(response.content)
                batch_articles = self._parse_pubmed_xml(root)
                articles.extend(batch_articles)
                
                # Be nice to PubMed's servers - wait between requests
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching batch: {e}")
                continue
        
        print(f"Successfully fetched {len(articles)} articles with abstracts")
        return articles
    
    def _parse_pubmed_xml(self, root) -> List[Dict]:
        """
        Parse PubMed XML response into structured data.
        
        Extracts title, abstract, authors, journal, and publication date.
        Only includes articles that have abstracts (some don't).
        """
        articles = []
        
        for article in root.findall(".//PubmedArticle"):
            try:
                # Extract basic info
                pmid_elem = article.find(".//PMID")
                pmid = pmid_elem.text if pmid_elem is not None else "unknown"
                
                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else "No title"
                
                # Extract abstract (skip if no abstract)
                abstract_elem = article.find(".//Abstract/AbstractText")
                if abstract_elem is None:
                    continue  # Skip articles without abstracts
                
                abstract = abstract_elem.text if abstract_elem.text else ""
                if len(abstract.strip()) < 50:  # Skip very short abstracts
                    continue
                
                # Extract journal info
                journal_elem = article.find(".//Journal/Title")
                journal = journal_elem.text if journal_elem is not None else "Unknown journal"
                
                # Extract publication year
                year_elem = article.find(".//PubDate/Year")
                year = year_elem.text if year_elem is not None else "Unknown"
                
                # Extract authors (first few)
                authors = []
                for author in article.findall(".//Author")[:3]:  # Just first 3 authors
                    lastname = author.find("LastName")
                    firstname = author.find("ForeName")
                    if lastname is not None:
                        name = lastname.text
                        if firstname is not None:
                            name = f"{firstname.text} {name}"
                        authors.append(name)
                
                articles.append({
                    "pmid": pmid,
                    "title": title,
                    "abstract": abstract,
                    "journal": journal,
                    "year": year,
                    "authors": authors,
                    "full_text": f"{title}\n\n{abstract}"  # Combined text for embedding
                })
                
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        
        return articles

def setup_chromadb():
    """
    Initialize ChromaDB for storing medical literature.
    
    Creates a persistent database that will store our PubMed abstracts
    with their embeddings for fast similarity search.
    """
    print("Setting up ChromaDB...")
    
    # Create ChromaDB client with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get collection for PubMed articles
    # ChromaDB will automatically generate embeddings for our text
    collection = client.get_or_create_collection(
        name="pubmed_articles",
        metadata={"description": "Medical literature abstracts from PubMed"}
    )
    
    print("✅ ChromaDB initialized successfully!")
    return collection

def load_articles_to_chromadb(articles: List[Dict], collection):
    """
    Load processed articles into ChromaDB.
    
    ChromaDB will automatically create embeddings for the text,
    so our AI agents can do semantic search later.
    """
    print(f"Loading {len(articles)} articles into ChromaDB...")
    
    # Prepare data for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for article in articles:
        documents.append(article["full_text"])
        metadatas.append({
            "pmid": article["pmid"],
            "title": article["title"],
            "journal": article["journal"],
            "year": article["year"],
            "authors": ", ".join(article["authors"]),
            "loaded_at": datetime.now().isoformat()
        })
        ids.append(f"pmid_{article['pmid']}")
    
    # Add to ChromaDB in batches (ChromaDB has limits on batch size)
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        end_idx = min(i + batch_size, len(documents))
        
        collection.add(
            documents=documents[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]
        )
        
        print(f"Loaded batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
    
    print("✅ All articles loaded into ChromaDB!")

def main():
    """
    Main function to download PubMed data and load into ChromaDB.
    
    Downloads abstracts about pediatric respiratory infections and stores them
    for our AI agents to use as a knowledge base.
    """
    print("AURA Diagnostics - PubMed Data Loader")
    print("=====================================")
    
    # Initialize PubMed loader
    loader = PubMedLoader()
    
    # Search for relevant medical literature
    # You can change this query to focus on different medical topics
    query = "pediatric respiratory infections OR childhood pneumonia OR pediatric bronchitis"
    pmids = loader.search_pubmed(query, max_results=1000)
    
    if not pmids:
        print("No articles found. Exiting.")
        return
    
    # Fetch abstracts
    articles = loader.fetch_abstracts(pmids)
    
    if not articles:
        print("No abstracts retrieved. Exiting.")
        return
    
    # Set up ChromaDB
    collection = setup_chromadb()
    
    # Load articles into ChromaDB
    load_articles_to_chromadb(articles, collection)
    
    print(f"\n🎉 Successfully loaded {len(articles)} medical articles!")
    print("Your AI agents now have access to relevant medical literature.")
    print("\nNext steps:")
    print("1. Run the database setup: python setup_db.py")
    print("2. Start the FastAPI server: uvicorn main:app --reload")

if __name__ == "__main__":
    main()