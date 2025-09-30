#!/usr/bin/env python3
"""
Test Zyte API integration with the scrapers
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import config to load .env
from backend.config import settings

from backend.scrapers.techcrunch import TechCrunchScraper
from backend.scrapers.theverge import TheVergeScraper

def test_zyte_integration():
    """Test Zyte API with scrapers."""
    
    print("=" * 60)
    print("TESTING ZYTE API INTEGRATION")
    print("=" * 60)
    print(f"\nZyte API Key: {'***' + settings.ZYTE_API_KEY[-8:] if settings.ZYTE_API_KEY else 'NOT SET'}")
    print(f"Use Zyte: {settings.USE_ZYTE}")
    print()
    
    # Test TechCrunch scraper
    print("Testing TechCrunch scraper with Zyte API...")
    print("-" * 60)
    
    tc_scraper = TechCrunchScraper({
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/'
    })
    
    try:
        # Fetch homepage with Zyte
        html = tc_scraper.fetch_page('https://techcrunch.com/', use_zyte=True)
        
        if html:
            print(f"✓ Successfully fetched page (HTML length: {len(html)} chars)")
            
            # Try to extract article links
            links = tc_scraper.extract_article_links(html)
            print(f"✓ Found {len(links)} article links")
            
            if links:
                print("\nSample article links:")
                for link in links[:3]:
                    print(f"  - {link}")
            else:
                print("\n⚠ No article links found (selectors may need updating)")
        else:
            print("✗ Failed to fetch page")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print()
    
    # Test The Verge scraper
    print("Testing The Verge scraper with Zyte API...")
    print("-" * 60)
    
    tv_scraper = TheVergeScraper({
        'name': 'The Verge',
        'url': 'https://www.theverge.com/'
    })
    
    try:
        # Fetch homepage with Zyte
        html = tv_scraper.fetch_page('https://www.theverge.com/', use_zyte=True)
        
        if html:
            print(f"✓ Successfully fetched page (HTML length: {len(html)} chars)")
            
            # Try to extract article links
            links = tv_scraper.extract_article_links(html)
            print(f"✓ Found {len(links)} article links")
            
            if links:
                print("\nSample article links:")
                for link in links[:3]:
                    print(f"  - {link}")
            else:
                print("\n⚠ No article links found (selectors may need updating)")
        else:
            print("✗ Failed to fetch page")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Zyte API integration test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_zyte_integration()
