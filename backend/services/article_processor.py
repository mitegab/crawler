"""
Article Processor Service
Orchestrates scraping, translation, and storage of articles
"""

from typing import List, Dict
from scrapers.techcrunch import TechCrunchScraper
from scrapers.theverge import TheVergeScraper
from scrapers.arstechnica import ArsTechnicaScraper
from scrapers.wired import WiredScraper
from translators.translator import Translator


class ArticleProcessor:
    """
    Main service for processing articles through the pipeline:
    scrape -> translate -> store
    """
    
    def __init__(self, appwrite_manager=None):
        """
        Initialize the article processor.
        
        Args:
            appwrite_manager: Instance of AppwriteManager for database operations
        """
        self.appwrite_manager = appwrite_manager
        self.translator = Translator(service='google')
        
        # Initialize scrapers
        self.scrapers = {
            'techcrunch': TechCrunchScraper({
                'name': 'TechCrunch',
                'url': 'https://techcrunch.com/'
            }),
            'theverge': TheVergeScraper({
                'name': 'The Verge',
                'url': 'https://www.theverge.com/'
            }),
            'arstechnica': ArsTechnicaScraper({
                'name': 'Ars Technica',
                'url': 'https://arstechnica.com/'
            }),
            'wired': WiredScraper({
                'name': 'Wired',
                'url': 'https://www.wired.com/'
            })
        }
    
    def scrape_all_sources(self, max_articles_per_source: int = 5) -> List[Dict]:
        """
        Scrape articles from all configured sources.
        
        Args:
            max_articles_per_source: Maximum articles to scrape from each source
            
        Returns:
            List of scraped articles
        """
        all_articles = []
        
        for source_name, scraper in self.scrapers.items():
            print(f"\n{'='*60}")
            print(f"Scraping {source_name}...")
            print(f"{'='*60}")
            
            try:
                articles = scraper.run(max_articles=max_articles_per_source)
                all_articles.extend(articles)
                print(f"✓ Scraped {len(articles)} articles from {source_name}")
            except Exception as e:
                print(f"✗ Error scraping {source_name}: {str(e)}")
        
        return all_articles
    
    def translate_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Translate a list of articles to Amharic.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles with translations added
        """
        translated_articles = []
        
        for i, article in enumerate(articles, 1):
            print(f"\nTranslating article {i}/{len(articles)}: {article.get('title', 'Unknown')[:50]}...")
            
            try:
                translated_article = self.translator.translate_article(article)
                translated_articles.append(translated_article)
                print(f"✓ Translation successful")
            except Exception as e:
                print(f"✗ Translation failed: {str(e)}")
                # Still include the article without translation
                translated_articles.append(article)
        
        return translated_articles
    
    def save_articles(self, articles: List[Dict]) -> int:
        """
        Save articles to Appwrite database.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Number of successfully saved articles
        """
        if not self.appwrite_manager:
            print("Warning: No Appwrite manager configured. Articles not saved.")
            return 0
        
        saved_count = 0
        
        for article in articles:
            try:
                self.appwrite_manager.save_article(article)
                saved_count += 1
                print(f"✓ Saved: {article.get('title', 'Unknown')[:50]}...")
            except Exception as e:
                print(f"✗ Failed to save article: {str(e)}")
        
        return saved_count
    
    def process_pipeline(self, max_articles_per_source: int = 5, translate: bool = True, save: bool = True):
        """
        Run the complete article processing pipeline.
        
        Args:
            max_articles_per_source: Maximum articles per source
            translate: Whether to translate articles
            save: Whether to save to database
        """
        print("\n" + "="*60)
        print("STARTING ARTICLE PROCESSING PIPELINE")
        print("="*60)
        
        # Step 1: Scrape
        print("\n[1/3] Scraping articles...")
        articles = self.scrape_all_sources(max_articles_per_source)
        print(f"\nTotal articles scraped: {len(articles)}")
        
        if not articles:
            print("No articles scraped. Exiting.")
            return
        
        # Step 2: Translate
        if translate:
            print("\n[2/3] Translating articles...")
            articles = self.translate_articles(articles)
        
        # Step 3: Save
        if save:
            print("\n[3/3] Saving articles to database...")
            saved_count = self.save_articles(articles)
            print(f"\nSaved {saved_count}/{len(articles)} articles")
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETED")
        print("="*60)
        
        return articles
