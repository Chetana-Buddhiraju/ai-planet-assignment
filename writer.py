# agents/writer.py
import os
from config import Config

class Writer:
    """Agent responsible for generating reports and saving outputs"""
    
    def __init__(self):
        self.config = Config()
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure the output directory exists"""
        if not os.path.exists(self.config.OUTPUT_DIR):
            os.makedirs(self.config.OUTPUT_DIR)
    
    def save_markdown_report(self, use_cases, filename):
        """
        Formats and saves the prioritized use cases as a markdown report
        
        Args:
            use_cases (list): List of prioritized use cases
            filename (str): Name of the file to save
        """
        markdown_output = "# Prioritized AI/GenAI Use Case Proposal\n\n"

        for i, uc in enumerate(use_cases):
            markdown_output += f"## {i+1}. {uc.get('title', 'Untitled Use Case')}\n\n"
            markdown_output += f"**Description:** {uc.get('description', 'N/A')}\n\n"
            markdown_output += f"**Required Data Sources:** {uc.get('data sources', 'N/A')}\n\n"
            markdown_output += f"**Expected Business Impact:** {uc.get('impact', 'N/A')} | **Estimated Complexity:** {uc.get('complexity', 'N/A')}\n\n"

            if uc.get('datasets'):
                markdown_output += "**Relevant Resources:**\n"
                for dataset in uc['datasets']:
                    title = dataset.get('title', 'Link')
                    url = dataset.get('url', '#')
                    notes = dataset.get('notes', '')
                    markdown_output += f"- [{title}]({url}) ({notes})\n"
                markdown_output += "\n"

            markdown_output += "---\n\n"

        try:
            filepath = os.path.join(self.config.OUTPUT_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
            print(f"Markdown report saved to {filepath}")
            return filepath
        except IOError as e:
            print(f"Error saving markdown report to {filename}: {e}")
            return None