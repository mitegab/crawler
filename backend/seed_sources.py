#!/usr/bin/env python3
"""
Seed script to populate the 'sources' collection in Appwrite.
Run this after setting up your Appwrite database to add initial news sources.
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    APPWRITE_ENDPOINT,
    APPWRITE_PROJECT_ID,
    APPWRITE_API_KEY,
    APPWRITE_DATABASE_ID,
    APPWRITE_SOURCES_COLLECTION_ID
)


# News sources configuration
SOURCES = [
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com",
        "enabled": True,
        "scraper_class": "TechCrunchScraper",
        "selector_config": json.dumps({
            "article_links": ".post-block__title__link",
            "title": ".article__title",
            "content": ".article-content",
            "author": ".article__byline a",
            "date": ".article__byline time",
            "image": ".article__featured-image img"
        }),
        "crawl_frequency": 3600,  # 1 hour
        "max_articles": 10,
        "category": "Technology",
        "language": "en",
        "priority": 10,
        "error_count": 0,
        "status": "active"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/tech",
        "enabled": True,
        "scraper_class": "TheVergeScraper",
        "selector_config": json.dumps({
            "article_links": "h2 a",
            "title": ".duet--article--article-title",
            "content": ".duet--article--article-body",
            "author": ".duet--article--article-author-name",
            "date": ".duet--article--article-date",
            "image": ".duet--article--article-featured-image img"
        }),
        "crawl_frequency": 3600,
        "max_articles": 10,
        "category": "Technology",
        "language": "en",
        "priority": 9,
        "error_count": 0,
        "status": "active"
    },
    {
        "name": "Ars Technica",
        "url": "https://arstechnica.com",
        "enabled": True,
        "scraper_class": "ArsTechnicaScraper",
        "selector_config": json.dumps({
            "article_links": ".article-title a",
            "title": "h1.heading",
            "content": ".article-content",
            "author": ".author-name",
            "date": "time.date",
            "image": ".article-featured-image img"
        }),
        "crawl_frequency": 3600,
        "max_articles": 10,
        "category": "Technology",
        "language": "en",
        "priority": 8,
        "error_count": 0,
        "status": "active"
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com",
        "enabled": True,
        "scraper_class": "WiredScraper",
        "selector_config": json.dumps({
            "article_links": ".summary-item__hed-link",
            "title": ".content-header__row h1",
            "content": ".article__body",
            "author": ".byline__name",
            "date": "time.content-header__publish-date",
            "image": ".main-image img"
        }),
        "crawl_frequency": 3600,
        "max_articles": 10,
        "category": "Technology",
        "language": "en",
        "priority": 7,
        "error_count": 0,
        "status": "active"
    },
    {
        "name": "TechRadar",
        "url": "https://www.techradar.com",
        "enabled": False,  # Disabled by default, can enable later
        "scraper_class": "TechRadarScraper",
        "selector_config": json.dumps({
            "article_links": ".article-link",
            "title": ".article-headline",
            "content": ".article-body",
            "author": ".author-name",
            "date": ".publish-date",
            "image": ".hero-image img"
        }),
        "crawl_frequency": 7200,  # 2 hours
        "max_articles": 8,
        "category": "Technology",
        "language": "en",
        "priority": 6,
        "error_count": 0,
        "status": "paused"
    },
    {
        "name": "Engadget",
        "url": "https://www.engadget.com",
        "enabled": False,
        "scraper_class": "EngadgetScraper",
        "selector_config": json.dumps({
            "article_links": ".article-link",
            "title": ".article-title",
            "content": ".article-text",
            "author": ".author",
            "date": ".timestamp",
            "image": ".article-image img"
        }),
        "crawl_frequency": 7200,
        "max_articles": 8,
        "category": "Technology",
        "language": "en",
        "priority": 5,
        "error_count": 0,
        "status": "paused"
    }
]


def seed_sources():
    """Seed the sources collection with initial data"""
    print("\n" + "="*60)
    print("🌱 SEEDING NEWS SOURCES")
    print("="*60)
    
    try:
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        print(f"\n✅ Connected to Appwrite")
        print(f"   Project: {APPWRITE_PROJECT_ID}")
        print(f"   Database: {APPWRITE_DATABASE_ID}")
        print(f"   Collection: {APPWRITE_SOURCES_COLLECTION_ID}")
        
        # Check if sources already exist
        existing = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        if existing['total'] > 0:
            print(f"\n⚠️  Found {existing['total']} existing sources")
            response = input("Do you want to add more sources? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        # Add sources
        print(f"\n📝 Adding {len(SOURCES)} news sources...")
        added = 0
        skipped = 0
        
        for source in SOURCES:
            try:
                # Check if source already exists by name
                existing_source = databases.list_documents(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=APPWRITE_SOURCES_COLLECTION_ID
                )
                
                exists = False
                for doc in existing_source['documents']:
                    if doc['name'] == source['name']:
                        exists = True
                        break
                
                if exists:
                    print(f"   ⏭️  Skipped '{source['name']}' (already exists)")
                    skipped += 1
                    continue
                
                # Create source
                document = databases.create_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=APPWRITE_SOURCES_COLLECTION_ID,
                    document_id=ID.unique(),
                    data=source
                )
                
                status_icon = "🟢" if source['enabled'] else "🔴"
                print(f"   {status_icon} Added '{source['name']}' (Priority: {source['priority']})")
                added += 1
                
            except Exception as e:
                print(f"   ❌ Error adding '{source['name']}': {e}")
        
        # Summary
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        print(f"✅ Added: {added}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"📚 Total sources: {added + existing['total']}")
        
        # List all sources
        all_sources = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        print(f"\n🌐 All News Sources:")
        for source in all_sources['documents']:
            status_icon = "🟢" if source['enabled'] else "🔴"
            print(f"   {status_icon} {source['name']} - Priority: {source['priority']} ({source['status']})")
        
        print("\n✅ Seeding complete!")
        print("\nYou can now run the crawler:")
        print("  python main.py")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📋 Please check:")
        print("   1. .env file is configured")
        print("   2. Appwrite connection details are correct")
        print("   3. 'sources' collection exists")
        print("   4. API key has write permissions")
        sys.exit(1)


def list_sources():
    """List all sources in the database"""
    try:
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        sources = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        print("\n" + "="*60)
        print(f"🌐 NEWS SOURCES ({sources['total']} total)")
        print("="*60)
        
        if sources['total'] == 0:
            print("\nNo sources found. Run with '--seed' to add sources.")
        else:
            for source in sources['documents']:
                status_icon = "🟢" if source['enabled'] else "🔴"
                print(f"\n{status_icon} {source['name']}")
                print(f"   URL: {source['url']}")
                print(f"   Scraper: {source['scraper_class']}")
                print(f"   Priority: {source['priority']}")
                print(f"   Status: {source['status']}")
                print(f"   Max Articles: {source['max_articles']}")
                print(f"   Frequency: {source['crawl_frequency']}s")
                if source.get('last_crawled'):
                    print(f"   Last Crawled: {source['last_crawled']}")
        
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def enable_source(source_name):
    """Enable a source by name"""
    try:
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        # Find source
        sources = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        found = False
        for source in sources['documents']:
            if source['name'].lower() == source_name.lower():
                # Enable source
                databases.update_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=APPWRITE_SOURCES_COLLECTION_ID,
                    document_id=source['$id'],
                    data={'enabled': True, 'status': 'active'}
                )
                print(f"✅ Enabled '{source['name']}'")
                found = True
                break
        
        if not found:
            print(f"❌ Source '{source_name}' not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def disable_source(source_name):
    """Disable a source by name"""
    try:
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        # Find source
        sources = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        found = False
        for source in sources['documents']:
            if source['name'].lower() == source_name.lower():
                # Disable source
                databases.update_document(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=APPWRITE_SOURCES_COLLECTION_ID,
                    document_id=source['$id'],
                    data={'enabled': False, 'status': 'paused'}
                )
                print(f"🔴 Disabled '{source['name']}'")
                found = True
                break
        
        if not found:
            print(f"❌ Source '{source_name}' not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage news sources in Appwrite')
    parser.add_argument('--seed', action='store_true', help='Seed sources to database')
    parser.add_argument('--list', action='store_true', help='List all sources')
    parser.add_argument('--enable', type=str, help='Enable a source by name')
    parser.add_argument('--disable', type=str, help='Disable a source by name')
    
    args = parser.parse_args()
    
    if args.seed:
        seed_sources()
    elif args.list:
        list_sources()
    elif args.enable:
        enable_source(args.enable)
    elif args.disable:
        disable_source(args.disable)
    else:
        # Default: seed
        seed_sources()
