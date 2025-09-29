"""
Text Cleaning Utilities
"""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    if not text:
        return ''
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove special characters but keep punctuation
    # Keep Amharic characters if present
    text = re.sub(r'[^\w\s\.,!?;:\-\u1200-\u137F]', '', text)
    
    return text


def extract_summary(text: str, max_length: int = 200) -> str:
    """
    Extract a summary from text (first N characters).
    
    Args:
        text: Full text content
        max_length: Maximum length of summary
        
    Returns:
        Summary text
    """
    if not text:
        return ''
    
    if len(text) <= max_length:
        return text
    
    # Find the last sentence boundary before max_length
    summary = text[:max_length]
    last_period = summary.rfind('.')
    
    if last_period > 0:
        summary = summary[:last_period + 1]
    else:
        summary = summary + '...'
    
    return summary


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text with HTML tags
        
    Returns:
        Clean text without HTML
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def normalize_url(url: str, base_url: Optional[str] = None) -> str:
    """
    Normalize and validate URL.
    
    Args:
        url: URL to normalize
        base_url: Base URL for relative URLs
        
    Returns:
        Normalized absolute URL
    """
    if not url:
        return ''
    
    # If URL is relative and we have a base URL
    if url.startswith('/') and base_url:
        return base_url.rstrip('/') + url
    
    return url
