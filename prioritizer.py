# agents/prioritizer.py
from config import Config

class Prioritizer:
    """Agent responsible for prioritizing use cases based on impact and complexity"""
    
    def __init__(self):
        self.config = Config()
    
    def rank_use_cases(self, use_cases):
        """
        Ranks use cases based on impact and complexity
        
        Args:
            use_cases (list): List of use case dictionaries
            
        Returns:
            list: Ranked use cases with core scores
        """
        ranked_use_cases = []
        
        for uc in use_cases:
            # Assign numerical scores for impact
            impact_score = 0
            if 'impact' in uc:
                impact_lower = uc['impact'].lower()
                if 'high' in impact_lower:
                    impact_score = 3
                elif 'med' in impact_lower:
                    impact_score = 2
                elif 'low' in impact_lower:
                    impact_score = 1

            # Assign numerical scores for complexity (inverse scoring)
            complexity_score = 0
            if 'complexity' in uc:
                complexity_lower = uc['complexity'].lower()
                if 'high' in complexity_lower:
                    complexity_score = 1  # Inverse score for complexity
                elif 'med' in complexity_lower:
                    complexity_score = 2
                elif 'low' in complexity_lower:
                    complexity_score = 3

            # Assuming data availability is medium (score 2) if not explicitly provided
            data_avail_score = 2

            # Calculate core score using the provided formula structure
            # core = 0.5 * impact_score + 0.4 * data_avail_score - 0.3 * complexity_score
            # Simplified formula using only impact and complexity as data_avail_score is assumed constant
            core_score = 0.5 * impact_score - 0.3 * complexity_score

            uc['core_score'] = core_score
            ranked_use_cases.append(uc)

        # Sort by core score in descending order
        ranked_use_cases = sorted(
            ranked_use_cases, 
            key=lambda x: x.get('core_score', 0), 
            reverse=True
        )

        return ranked_use_cases