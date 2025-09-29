"""
Scheduled Crawler Function for Appwrite

This function runs on a CRON schedule (e.g., every 6 hours)
to scrape articles from all configured sources.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.article_processor import ArticleProcessor
from services.appwrite_manager import AppwriteManager


def main(req, res):
    """
    Appwrite Function entry point.
    
    Args:
        req: Request object
        res: Response object
    """
    try:
        # Initialize services
        appwrite_manager = AppwriteManager()
        processor = ArticleProcessor(appwrite_manager=appwrite_manager)
        
        # Get max articles from environment or use default
        max_articles = int(os.getenv('MAX_ARTICLES_PER_SOURCE', '5'))
        
        # Run scraping pipeline
        articles = processor.scrape_all_sources(max_articles_per_source=max_articles)
        
        # Save to database
        saved_count = processor.save_articles(articles)
        
        result = {
            'success': True,
            'articles_scraped': len(articles),
            'articles_saved': saved_count,
            'message': f'Successfully scraped and saved {saved_count} articles'
        }
        
        return res.json(result)
    
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        return res.json(error_result, 500)
