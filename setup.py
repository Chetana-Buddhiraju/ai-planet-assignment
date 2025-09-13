# setup.py
import os
import shutil
from pathlib import Path

def setup_project():
    """Setup the AI Planet Project"""
    
    print(" Setting up AI Planet Project...")
    
    # Create necessary directories
    directories = [
        "agents",
        "outputs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("Created .env file from template")
            print("Please edit .env file with your API keys")
        else:
            print(".env.example not found. Please create .env file manually")
    
    # Create __init__.py for agents package
    init_file = Path("agents/__init__.py")
    if not init_file.exists():
        init_content = '''# agents/__init__.py
from .search_agent import SearchAgent
from .research_agent import ResearchAgent
from .usecase_agent import UseCaseAgent
from .dataset_agent import DatasetAgent
from .prioritizer import Prioritizer
from .writer import Writer

__all__ = [
    'SearchAgent',
    'ResearchAgent', 
    'UseCaseAgent',
    'DatasetAgent',
    'Prioritizer',
    'Writer'
]
'''
        init_file.write_text(init_content)
        print("Created agents/__init__.py")
    
    print("\n Setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Edit .env file with your API keys")
    print("3. Run the app: streamlit run app.py")

if __name__ == "__main__":
    setup_project()