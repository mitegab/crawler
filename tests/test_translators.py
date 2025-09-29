"""
Tests for Translators
"""

import pytest
from backend.translators.translator import Translator


def test_translator_initialization():
    """Test translator initialization."""
    translator = Translator(service='google')
    assert translator.service == 'google'
    assert translator.source_lang == 'en'
    assert translator.target_lang == 'am'


def test_text_splitting():
    """Test text splitting for long content."""
    translator = Translator()
    
    # Create a long text
    long_text = "This is a sentence. " * 500
    
    # Split text
    chunks = translator._split_text(long_text, max_length=1000)
    
    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)


# Add more tests as needed
