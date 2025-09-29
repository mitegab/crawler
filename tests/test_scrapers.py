"""
Tests for Scrapers
"""

import pytest
from backend.scrapers.base_scraper import BaseScraper
from backend.scrapers.techcrunch import TechCrunchScraper


def test_base_scraper_initialization():
    """Test base scraper initialization."""
    config = {
        'name': 'Test Source',
        'url': 'https://example.com'
    }
    
    class TestScraper(BaseScraper):
        def extract_article_links(self, html):
            return []
        
        def extract_article_content(self, url, html):
            return {}
    
    scraper = TestScraper(config)
    assert scraper.source_name == 'Test Source'
    assert scraper.base_url == 'https://example.com'


def test_techcrunch_scraper_initialization():
    """Test TechCrunch scraper initialization."""
    config = {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/'
    }
    
    scraper = TechCrunchScraper(config)
    assert scraper.source_name == 'TechCrunch'
    assert 'techcrunch.com' in scraper.base_url


# Add more tests as needed
