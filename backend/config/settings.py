"""
Configuration Settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Appwrite Configuration
APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT', 'https://cloud.appwrite.io/v1')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID', '')
APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY', '')
APPWRITE_DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID', 'tech-news-db')
APPWRITE_ARTICLES_COLLECTION_ID = os.getenv('APPWRITE_ARTICLES_COLLECTION_ID', 'articles')
APPWRITE_STORAGE_BUCKET_ID = os.getenv('APPWRITE_STORAGE_BUCKET_ID', 'article-images')

# Zyte Configuration
ZYTE_API_KEY = os.getenv('ZYTE_API_KEY', '')
USE_ZYTE = os.getenv('USE_ZYTE', 'false').lower() == 'true'

# Translation Configuration
TRANSLATION_SERVICE = os.getenv('TRANSLATION_SERVICE', 'google')  # google, azure, openai

# Google Translate (uses free library by default)

# Azure Translator
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY', '')
AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT', '')
AZURE_TRANSLATOR_REGION = os.getenv('AZURE_TRANSLATOR_REGION', '')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Scraping Configuration
MAX_ARTICLES_PER_SOURCE = int(os.getenv('MAX_ARTICLES_PER_SOURCE', '10'))
SCRAPE_INTERVAL_HOURS = int(os.getenv('SCRAPE_INTERVAL_HOURS', '6'))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
