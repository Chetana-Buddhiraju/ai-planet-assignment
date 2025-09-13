# agents/research_agent.py
from .search_agent import SearchAgent

class ResearchAgent:
    """Agent responsible for coordinating research activities"""
    
    def __init__(self):
        self.search_agent = SearchAgent()
    
    def conduct_research(self, company_or_industry, max_results=None):
        """
        Conducts comprehensive research on a company or industry
        
        Args:
            company_or_industry (str): The name of the company or industry to research
            max_results (int): Number of search results to process
            
        Returns:
            list of dict: Research findings with url, title, and text
        """
        print(f"Conducting research for: {company_or_industry}")
        
        # Perform web search and scraping
        research_findings = self.search_agent.search_and_scrape(
            company_or_industry, 
            max_results
        )
        
        if not research_findings:
            print("No research findings obtained.")
            return []
        
        print(f"Research completed. Found {len(research_findings)} documents.")
        return research_findings