# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    # Kaggle configuration
    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
    KAGGLE_KEY = os.getenv("KAGGLE_KEY")
    
    # App settings
    MAX_SEARCH_RESULTS = 3
    MAX_DATASET_RESULTS = 2
    REQUEST_TIMEOUT = 15
    RANDOM_SLEEP_MIN = 2
    RANDOM_SLEEP_MAX = 5
    
    # Output settings
    OUTPUT_DIR = "outputs"
    
    @classmethod
    def validate_keys(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not cls.SERPAPI_API_KEY:
            missing_keys.append("SERPAPI_API_KEY")
            
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True