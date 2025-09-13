# agents/search_agent.py
import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import time
import random
from config import Config

class SearchAgent:
    """Agent responsible for web search and content scraping"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
        # Browser headers to avoid bot detection
        self.headers_template = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
            ]),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        }
    
    def search_and_scrape(self, company_or_industry, max_results=None):
        """
        Performs a real-time web search and scrapes content from top results
        
        Args:
            company_or_industry (str): The name of the company or industry to research
            max_results (int): Number of top search results to scrape
            
        Returns:
            list of dict: Each dict contains 'url', 'title', and 'text' fields
        """
        if max_results is None:
            max_results = self.config.MAX_SEARCH_RESULTS
            
        print(f"Running search agent for: {company_or_industry}")
        search_query = f"{company_or_industry} company profile and recent news"
        
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": self.config.SERPAPI_API_KEY
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            # Check for SerpApi error
            if "error" in results:
                print(f"SerpApi Error: {results['error']}")
                return []

            organic_results = results.get("organic_results", [])
            if not organic_results:
                print("No organic results found.")
                return []

            scraped_docs = []

            for i, result in enumerate(organic_results[:max_results]):
                url = result.get("link")
                title = result.get("title")
                if not url or not title:
                    continue

                try:
                    # Add random sleep to avoid bot detection
                    time.sleep(random.uniform(
                        self.config.RANDOM_SLEEP_MIN, 
                        self.config.RANDOM_SLEEP_MAX
                    ))

                    response = self.session.get(
                        url, 
                        headers=self.headers_template, 
                        timeout=self.config.REQUEST_TIMEOUT
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        paragraphs = soup.find_all("p")
                        text = " ".join(p.get_text() for p in paragraphs)
                        clean_text = " ".join(text.split()).strip()

                        if clean_text:
                            scraped_docs.append({
                                "url": url,
                                "title": title,
                                "text": clean_text
                            })
                            print(f"Scraped: {url}")
                    elif response.status_code == 403:
                        print(f"403 Forbidden at {url}. Skipping...")
                    else:
                        print(f"Failed {url} — Status {response.status_code}")

                except requests.exceptions.RequestException as e:
                    print(f"Error scraping {url}: {e}")

            return scraped_docs

        except Exception as e:
            print(f"Unexpected error in search agent: {e}")
            return []