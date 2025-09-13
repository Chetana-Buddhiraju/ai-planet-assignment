# agents/usecase_agent.py
import openai
from config import Config

class UseCaseAgent:
    """Agent responsible for generating AI/GenAI use cases"""
    
    def __init__(self):
        self.config = Config()
        self.client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
    
    def generate_use_cases(self, company_name, research_findings):
        """
        Analyzes research findings and proposes relevant AI/GenAI use cases
        
        Args:
            company_name (str): The name of the company
            research_findings (list): A list of dictionaries containing research data
            
        Returns:
            list of dict: Proposed use cases with structured information
        """
        company_context = "\n".join([
            d.get('text', '') for d in research_findings if d.get('text')
        ])

        if not company_context:
            print("Warning: No research context available to generate use cases.")
            return []

        prompt = f"""
You are an AI strategy consultant. Given these facts about {company_name} (context below), propose exactly 5 distinct GenAI/AI use cases for the company focusing on operations, customer experience, and monetization.

For each use case, provide the following information in a structured format:
TITLE: [Short Title]
DESCRIPTION: [One-sentence description]
DATA SOURCES: [List of required data sources, e.g., customer data, sales data, website logs]
BUSINESS IMPACT: [Expected business impact: Low, Medium, or High]
COMPLEXITY: [Estimated complexity: Low, Medium, or High]

Context:
{company_context}

Ensure each use case is clearly separated by a horizontal rule "---" and follows the exact 'FIELD_NAME: [Value]' format. Do not include any introductory or concluding text outside of the use case blocks.
"""

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            llm_output = resp.choices[0].message.content

            use_cases = []
            use_case_blocks = llm_output.strip().split('---')

            for block in use_case_blocks:
                block = block.strip()
                if not block:
                    continue

                current_use_case = {}
                lines = block.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith("TITLE:"):
                        current_use_case["title"] = line.replace("TITLE:", "").strip()
                    elif line.startswith("DESCRIPTION:"):
                        current_use_case["description"] = line.replace("DESCRIPTION:", "").strip()
                    elif line.startswith("DATA SOURCES:"):
                        current_use_case["data sources"] = line.replace("DATA SOURCES:", "").strip()
                    elif line.startswith("BUSINESS IMPACT:"):
                        current_use_case["impact"] = line.replace("BUSINESS IMPACT:", "").strip()
                    elif line.startswith("COMPLEXITY:"):
                        current_use_case["complexity"] = line.replace("COMPLEXITY:", "").strip()

                if current_use_case and current_use_case.get("title"):
                    use_cases.append(current_use_case)

            if not use_cases or len(use_cases) < 3:
                print("Warning: Parsing failed or fewer than 3 valid use cases found.")
                print("LLM Output:\n", llm_output)

            return use_cases

        except Exception as e:
            print(f"Error generating use cases: {e}")
            return []