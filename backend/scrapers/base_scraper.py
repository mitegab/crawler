"""
Base Scraper Class
All site-specific scrapers inherit from this base class.
"""

import os
import time
import random
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from datetime import datetime


class BaseScraper(ABC):
    """
    Abstract base class for all news scrapers.
    Provides common functionality for fetching and parsing web pages.
    """
    
    def __init__(self, source_config: Dict):
        """
        Initialize the scraper with source configuration.
        
        Args:
            source_config: Dictionary containing source name, URL, selectors, etc.
        """
        self.source_config = source_config
        self.source_name = source_config.get('name', 'Unknown')
        self.base_url = source_config.get('url', '')
        self.zyte_api_key = os.getenv('ZYTE_API_KEY')
        self.use_zyte = os.getenv('USE_ZYTE', 'false').lower() == 'true'
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
    
    def get_random_user_agent(self) -> str:
        """Return a random user agent string."""
        return random.choice(self.user_agents)
    
    def fetch_page(self, url: str, use_zyte: bool = None) -> Optional[str]:
        """
        Fetch a web page using either direct requests or Zyte API.
        
        Args:
            url: The URL to fetch
            use_zyte: Override default Zyte usage
            
        Returns:
            HTML content as string or None if failed
        """
        if use_zyte is None:
            use_zyte = self.use_zyte
        
        try:
            if use_zyte and self.zyte_api_key:
                return self._fetch_with_zyte(url)
            else:
                return self._fetch_direct(url)
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def _fetch_direct(self, url: str) -> Optional[str]:
        """Fetch page directly with requests library."""
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Random delay to be polite
        time.sleep(random.uniform(1, 3))
        
        return response.text
    
    def _fetch_with_zyte(self, url: str) -> Optional[str]:
        """Fetch page using Zyte API for anti-bot protection."""
        api_url = "https://api.zyte.com/v1/extract"
        
        payload = {
            "url": url,
            "browserHtml": True,
        }
        
        response = requests.post(
            api_url,
            auth=(self.zyte_api_key, ''),
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        return data.get('browserHtml', '')
    
    @abstractmethod
    def extract_article_links(self, html: str) -> List[str]:
        """
        Extract article URLs from the main page.
        Must be implemented by each scraper.
        
        Args:
            html: HTML content of the main page
            
        Returns:
            List of article URLs
        """
        pass
    
    @abstractmethod
    def extract_article_content(self, url: str, html: str) -> Optional[Dict]:
        """
        Extract article content from an article page.
        Must be implemented by each scraper.
        
        Args:
            url: The article URL
            html: HTML content of the article page
            
        Returns:
            Dictionary containing article data or None if failed
        """
        pass
    
    def run(self, max_articles: int = 10) -> List[Dict]:
        """
        Main scraping logic. Fetches articles from the source.
        
        Args:
            max_articles: Maximum number of articles to scrape
            
        Returns:
            List of article dictionaries
        """
        print(f"Starting scraper for {self.source_name}")
        
        # Fetch main page
        html = self.fetch_page(self.base_url)
        if not html:
            print(f"Failed to fetch main page for {self.source_name}")
            return []
        
        # Extract article links
        article_urls = self.extract_article_links(html)
        print(f"Found {len(article_urls)} article links")
        
        # Limit articles
        article_urls = article_urls[:max_articles]
        
        # Extract content from each article
        articles = []
        for url in article_urls:
            print(f"Scraping: {url}")
            article_html = self.fetch_page(url)
            
            if article_html:
                article_data = self.extract_article_content(url, article_html)
                if article_data:
                    article_data['source'] = self.source_name
                    article_data['scraped_at'] = datetime.utcnow().isoformat()
                    articles.append(article_data)
        
        print(f"Successfully scraped {len(articles)} articles from {self.source_name}")
        return articles
