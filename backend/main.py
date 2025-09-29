"""
Main Entry Point for the Crawler Application
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.article_processor import ArticleProcessor
from services.appwrite_manager import AppwriteManager
from config.settings import MAX_ARTICLES_PER_SOURCE
from utils.logger import setup_logger


def main():
    """Main function to run the crawler."""
    # Setup logger
    logger = setup_logger(name='crawler', log_file='logs/crawler.log')
    
    logger.info("Starting Tech News Crawler")
    
    try:
        # Initialize Appwrite manager (optional - will skip if not configured)
        appwrite_manager = None
        try:
            appwrite_manager = AppwriteManager()
            logger.info("Appwrite manager initialized")
        except Exception as e:
            logger.warning(f"Appwrite not configured: {str(e)}")
            logger.warning("Articles will be scraped but not saved to database")
        
        # Initialize processor
        processor = ArticleProcessor(appwrite_manager=appwrite_manager)
        
        # Run the pipeline
        articles = processor.process_pipeline(
            max_articles_per_source=MAX_ARTICLES_PER_SOURCE,
            translate=True,
            save=appwrite_manager is not None
        )
        
        # Print summary
        logger.info(f"\n{'='*60}")
        logger.info(f"SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total articles processed: {len(articles)}")
        
        if articles:
            translated_count = sum(1 for a in articles if a.get('title_am'))
            logger.info(f"Articles translated: {translated_count}")
            
            # Save articles to JSON for review
            import json
            output_file = 'output/articles.json'
            Path('output').mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Articles saved to: {output_file}")
        
        logger.info("Crawler completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Crawler interrupted by user")
    except Exception as e:
        logger.error(f"Error running crawler: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
