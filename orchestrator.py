# orchestrator.py
import os
from agents.research_agent import ResearchAgent
from agents.usecase_agent import UseCaseAgent
from agents.dataset_agent import DatasetAgent
from agents.prioritizer import Prioritizer
from agents.writer import Writer
from config import Config

class Orchestrator:
    """Main orchestrator for the multi-agent system workflow"""
    
    def __init__(self):
        self.config = Config()
        self.research_agent = ResearchAgent()
        self.usecase_agent = UseCaseAgent()
        self.dataset_agent = DatasetAgent()
        self.prioritizer = Prioritizer()
        self.writer = Writer()
    
    def run_analysis(self, company_or_industry):
        """
        Orchestrates the complete analysis workflow
        
        Args:
            company_or_industry (str): The name of the company or industry to research
            
        Returns:
            list: Prioritized use cases with associated data and resources
        """
        print(f"Starting orchestration for: {company_or_industry}")

        # 1. Research Phase
        print("Running research agent...")
        research_docs = self.research_agent.conduct_research(company_or_industry)
        if not research_docs:
            print("Research phase failed or returned no documents.")
            return []

        # 2. Use Case Generation Phase
        print("Running use case generation agent...")
        generated_use_cases = self.usecase_agent.generate_use_cases(
            company_or_industry, 
            research_docs
        )
        if not generated_use_cases:
            print("Use case generation phase failed or returned no use cases.")
            return []

        # 3. Resource Collection Phase
        print("Running dataset agent...")
        use_cases_with_datasets = self.dataset_agent.find_datasets_for_use_cases(
            generated_use_cases
        )
        if not use_cases_with_datasets:
            print("Dataset agent failed or returned no datasets.")
            # Continue with use cases without datasets if the agent fails
            use_cases_with_datasets = generated_use_cases

        # 4. Prioritization Phase
        print("Running prioritization agent...")
        prioritized_usecases = self.prioritizer.rank_use_cases(use_cases_with_datasets)
        if not prioritized_usecases:
            print("Prioritization agent failed.")
            # Continue with the list from the previous step if prioritization fails
            prioritized_usecases = use_cases_with_datasets

        # 5. Report Writing Phase
        print("Saving markdown report...")
        output_filename = f"{company_or_industry.replace(' ', '_').lower()}_usecases.md"
        self.writer.save_markdown_report(prioritized_usecases, output_filename)

        print(f"Orchestration complete. Report saved to {output_filename}")

        return prioritized_usecases

def run_analysis(company_or_industry):
    """
    Convenience function to run the complete analysis
    
    Args:
        company_or_industry (str): The name of the company or industry to research
        
    Returns:
        list: Prioritized use cases with associated data and resources
    """
    orchestrator = Orchestrator()
    return orchestrator.run_analysis(company_or_industry)