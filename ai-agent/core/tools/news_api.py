import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class NewsAPIWrapper:
    def __init__(self, api_key: str = os.getenv("NEWS_API_KEY")):
        """
        Initialize NewsAPI.org wrapper
        
        Args:
            api_key: Get from https://newsapi.org/ (store in .env)
        """
        if not api_key:
            raise ValueError("NEWS_API_KEY environment variable not set")
            
        self.base_url = "https://newsapi.org/v2/"
        self.api_key = api_key
        self.default_params = {
            "pageSize": 10,
            "language": "en",
            "sortBy": "publishedAt"
        }

    def search_news(
        self,
        query: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort_by: str = "relevancy",
        page_size: int = 10
    ) -> List[Dict]:
        """
        Search news articles by keywords

        Returns:
            List of article dictionaries with: 
            title, description, content, url, publishedAt, source
        """
        endpoint = "everything"
        params = {
            "q": query,
            "sortBy": sort_by,
            "pageSize": min(max(page_size, 1), 100),
            "apiKey": self.api_key
        }
        
        # Handle dates
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self._make_request(endpoint, params)

    def get_top_headlines(
        self,
        category: Optional[str] = None,
        country: str = "in",
        page_size: int = 10
    ) -> List[Dict]:
        """
        Get current top headlines
        
        Args:
            category: business, entertainment, general, health, science, sports, technology
            country: 2-letter ISO country code
            page_size: Number of results (1-100)
        """
        endpoint = "top-headlines"
        params = {
            "country": country,
            "pageSize": min(max(page_size, 1), 100),
            "apiKey": self.api_key
        }
        
        if category:
            params["category"] = category
            
        return self._make_request(endpoint, params)

    def _make_request(self, endpoint: str, params: Dict) -> List[Dict]:
        """Handle actual API requests with error handling"""
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                return [{"error": data.get("message", "Unknown API error")}]
                
            return [self._format_article(article) for article in data.get("articles", [])]
            
        except requests.exceptions.RequestException as e:
            return [{"error": f"Request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]

    def _format_article(self, article: Dict) -> Dict:
        """Standardize article format"""
        return {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", ""),
            "author": article.get("author", ""),
            "image_url": article.get("urlToImage", "")
        }

    def get_recent_tech_news(self, days: int = 7) -> List[Dict]:
        """Convenience method for recent tech news"""
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        return self.search_news(
            query="technology",
            from_date=from_date,
            to_date=to_date,
            sort_by="publishedAt",
            page_size=10
        )