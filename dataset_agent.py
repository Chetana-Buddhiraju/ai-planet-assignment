# agents/dataset_agent.py
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from huggingface_hub import HfApi
from github import Github, RateLimitExceededException, Auth
from config import Config

class DatasetAgent:
    """Agent responsible for finding relevant datasets and resources"""
    
    def __init__(self):
        self.config = Config()
        self._setup_kaggle()
    
    def _setup_kaggle(self):
        """Setup Kaggle API authentication"""
        try:
            self.kaggle_api = KaggleApi()
            self.kaggle_api.authenticate()
        except Exception as e:
            print(f"Warning: Could not authenticate with Kaggle: {e}")
            self.kaggle_api = None
    
    def search_kaggle(self, keyword, max_results=None):
        """Search for datasets on Kaggle"""
        if max_results is None:
            max_results = self.config.MAX_DATASET_RESULTS
            
        if not self.kaggle_api:
            return []
            
        print(f"Searching Kaggle for datasets related to: {keyword}")
        results = []
        
        try:
            search_results = self.kaggle_api.dataset_list(search=keyword, sort_by="hottest")

            if not search_results:
                print(f"No datasets found on Kaggle for '{keyword}'")
                return []

            for ds in search_results[:max_results]:
                dataset_info = {
                    "url": f"https://www.kaggle.com/{ds.ref}",
                    "title": getattr(ds, "title", "Untitled Dataset"),
                    "notes": f"Kaggle Dataset - Downloads: {getattr(ds, 'downloadCount', 'N/A')}, Views: {getattr(ds, 'viewCount', 'N/A')}"
                }

                try:
                    # Fetch file info for dataset size
                    files_in_dataset = self.kaggle_api.dataset_list_files(ds.ref)
                    if files_in_dataset and hasattr(files_in_dataset, "datasetFiles"):
                        total_size_bytes = sum(
                            getattr(f, "totalBytes", 0) for f in files_in_dataset.datasetFiles
                        )
                        total_size_mb = total_size_bytes / (1024 * 1024)
                        dataset_info["notes"] += f", Total Size: {total_size_mb:.2f} MB"
                    else:
                        dataset_info["notes"] += ", Size info not available"

                except Exception as e:
                    print(f"  - Error getting file list for {ds.ref}: {e}")
                    dataset_info["notes"] += ", Error getting size info"

                results.append(dataset_info)

            return results

        except Exception as e:
            print(f"Error searching Kaggle: {e}")
            return []

    def search_huggingface(self, keyword, max_results=None):
        """Search for datasets on Hugging Face"""
        if max_results is None:
            max_results = self.config.MAX_DATASET_RESULTS
            
        print(f"Searching Hugging Face for datasets related to: {keyword}")
        results = []
        
        try:
            api = HfApi()
            datasets = api.list_datasets(search=keyword, sort="downloads", limit=max_results)

            for ds in datasets:
                results.append({
                    "url": f"https://huggingface.co/datasets/{ds.id}",
                    "title": ds.id.split('/')[-1],
                    "notes": f"HuggingFace Dataset, downloads: {ds.downloads}"
                })
            return results
        except Exception as e:
            print(f"Error searching Hugging Face: {e}")
            return []

    def search_github(self, keyword, max_results=None):
        """Search for repositories on GitHub"""
        if max_results is None:
            max_results = self.config.MAX_DATASET_RESULTS
            
        if not self.config.GITHUB_TOKEN:
            print("GitHub token not found. Skipping GitHub search.")
            return []

        print(f"Searching GitHub for repositories related to: {keyword}")
        results = []
        
        try:
            auth = Auth.Token(self.config.GITHUB_TOKEN)
            g = Github(auth=auth)

            query = f"{keyword} dataset"
            repositories = g.search_repositories(
                query=query, 
                sort="stars", 
                order="desc", 
                per_page=max_results
            )

            for i, repo in enumerate(repositories):
                if i >= max_results:
                    break
                results.append({
                    "url": repo.html_url,
                    "title": repo.full_name,
                    "notes": f"GitHub Repo, stars: {repo.stargazers_count}"
                })
            return results
            
        except RateLimitExceededException:
            print("GitHub API rate limit exceeded. Please wait or use a token with a higher limit.")
            return []
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []

    def find_datasets_for_use_cases(self, use_cases):
        """
        Searches for relevant datasets and resources for proposed use cases
        
        Args:
            use_cases (list): List of use case dictionaries
            
        Returns:
            list: Updated use cases with datasets attached
        """
        updated_use_cases = []
        
        for uc in use_cases:
            keywords = []
            # Extract keywords from title and description
            all_words = []
            if uc.get("title"):
                all_words.extend(uc["title"].lower().replace(':', '').split())
            if uc.get("description"):
                all_words.extend(uc["description"].lower().replace(':', '').split())

            # Filter out short words and basic stopwords
            stop_words = [
                'for', 'and', 'with', 'the', 'from', 'about', 'this', 'that', 
                'which', 'using', 'based', 'improve', 'enhance', 'generate', 
                'automate', 'predict', 'implement', 'utilize', 'leverage'
            ]
            keywords = [
                word for word in all_words 
                if len(word) > 2 and word not in stop_words
            ]

            search_keywords = " ".join(list(set(keywords))[:5])  # Take up to 5 unique keywords

            datasets = []
            # Search across all platforms
            datasets.extend(self.search_kaggle(search_keywords))
            datasets.extend(self.search_huggingface(search_keywords))
            datasets.extend(self.search_github(search_keywords))

            uc['datasets'] = datasets
            updated_use_cases.append(uc)
            
        return updated_use_cases