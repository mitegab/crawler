#!/usr/bin/env python3
"""
Test script to verify Appwrite Cloud setup.
Tests database connection, collections, storage, and basic operations.
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    APPWRITE_ENDPOINT,
    APPWRITE_PROJECT_ID,
    APPWRITE_API_KEY,
    APPWRITE_DATABASE_ID,
    APPWRITE_ARTICLES_COLLECTION_ID,
    APPWRITE_SOURCES_COLLECTION_ID,
    APPWRITE_QUEUE_COLLECTION_ID,
    APPWRITE_STORAGE_BUCKET_ID
)


def test_connection():
    """Test basic Appwrite connection"""
    print("\n" + "="*60)
    print("🔌 Testing Appwrite Connection")
    print("="*60)
    
    try:
        client = Client()
        client.set_endpoint(APPWRITE_ENDPOINT)
        client.set_project(APPWRITE_PROJECT_ID)
        client.set_key(APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        # Try to get database info
        database = databases.get(APPWRITE_DATABASE_ID)
        
        print(f"✅ Connected successfully!")
        print(f"   Endpoint: {APPWRITE_ENDPOINT}")
        print(f"   Project ID: {APPWRITE_PROJECT_ID}")
        print(f"   Database: {database['name']} ({database['$id']})")
        
        return client, databases
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n📋 Please verify:")
        print("   1. APPWRITE_PROJECT_ID is correct")
        print("   2. APPWRITE_API_KEY is valid")
        print("   3. API key has necessary permissions")
        return None, None


def test_collections(databases):
    """Test database collections"""
    print("\n" + "="*60)
    print("📚 Testing Collections")
    print("="*60)
    
    collections_to_check = {
        'articles': APPWRITE_ARTICLES_COLLECTION_ID,
        'sources': APPWRITE_SOURCES_COLLECTION_ID,
        'translations_queue': APPWRITE_QUEUE_COLLECTION_ID
    }
    
    all_good = True
    
    for name, collection_id in collections_to_check.items():
        try:
            collection = databases.get_collection(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=collection_id
            )
            
            print(f"✅ Collection '{name}': {collection['name']}")
            print(f"   ID: {collection['$id']}")
            print(f"   Attributes: {len(collection['attributes'])}")
            
            # List some attributes
            if collection['attributes']:
                print(f"   Sample attributes:")
                for attr in collection['attributes'][:5]:
                    print(f"     - {attr['key']} ({attr['type']})")
                    
        except Exception as e:
            print(f"❌ Collection '{name}' not found: {e}")
            all_good = False
    
    return all_good


def test_article_creation(databases):
    """Test creating a test article"""
    print("\n" + "="*60)
    print("📝 Testing Article Creation")
    print("="*60)
    
    try:
        # Create test article
        article_data = {
            'title_en': 'Test Article - Appwrite Setup Verification',
            'content_en': 'This is a test article created to verify the Appwrite setup is working correctly.',
            'source': 'Test',
            'source_url': 'https://example.com/test-article',
            'scraped_at': datetime.now().isoformat(),
            'status': 'pending',
            'category': 'Testing'
        }
        
        article = databases.create_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_ARTICLES_COLLECTION_ID,
            document_id=ID.unique(),
            data=article_data
        )
        
        print(f"✅ Test article created successfully!")
        print(f"   Article ID: {article['$id']}")
        print(f"   Title: {article['title_en']}")
        print(f"   Status: {article['status']}")
        
        # Try to read it back
        retrieved = databases.get_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_ARTICLES_COLLECTION_ID,
            document_id=article['$id']
        )
        
        print(f"✅ Article retrieved successfully!")
        
        # Clean up - delete test article
        databases.delete_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_ARTICLES_COLLECTION_ID,
            document_id=article['$id']
        )
        
        print(f"✅ Test article deleted (cleanup)")
        
        return True
    except Exception as e:
        print(f"❌ Article creation failed: {e}")
        print("\n📋 Please check:")
        print("   1. Collection 'articles' exists")
        print("   2. All required attributes are defined")
        print("   3. API key has write permissions")
        return False


def test_storage(client):
    """Test storage bucket access"""
    print("\n" + "="*60)
    print("📦 Testing Storage")
    print("="*60)
    
    try:
        storage = Storage(client)
        
        # Try to get bucket info
        bucket = storage.get_bucket(APPWRITE_STORAGE_BUCKET_ID)
        
        print(f"✅ Storage bucket accessible!")
        print(f"   Bucket: {bucket['name']} ({bucket['$id']})")
        print(f"   Max file size: {bucket['maximumFileSize']} bytes")
        print(f"   Enabled: {bucket['enabled']}")
        
        # List files
        files = storage.list_files(APPWRITE_STORAGE_BUCKET_ID)
        print(f"   Current files: {files['total']}")
        
        return True
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
        print("\n📋 Please check:")
        print("   1. Storage bucket exists")
        print("   2. Bucket ID is correct")
        print("   3. API key has storage permissions")
        return False


def test_sources_data(databases):
    """Test if sources collection has data"""
    print("\n" + "="*60)
    print("🌐 Checking News Sources")
    print("="*60)
    
    try:
        sources = databases.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=APPWRITE_SOURCES_COLLECTION_ID
        )
        
        if sources['total'] == 0:
            print(f"⚠️  No news sources found")
            print(f"   You should add sources to the 'sources' collection")
            print(f"   Refer to APPWRITE_SETUP.md for seed data")
            return False
        else:
            print(f"✅ Found {sources['total']} news sources:")
            for source in sources['documents']:
                enabled = "🟢" if source.get('enabled', False) else "🔴"
                print(f"   {enabled} {source['name']} - Priority: {source.get('priority', 0)}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking sources: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 APPWRITE SETUP VERIFICATION")
    print("="*60)
    print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'connection': False,
        'collections': False,
        'article_creation': False,
        'storage': False,
        'sources': False
    }
    
    # Test connection
    client, databases = test_connection()
    if client and databases:
        results['connection'] = True
        
        # Test collections
        results['collections'] = test_collections(databases)
        
        # Test article creation
        results['article_creation'] = test_article_creation(databases)
        
        # Test storage
        results['storage'] = test_storage(client)
        
        # Check sources
        results['sources'] = test_sources_data(databases)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nYour Appwrite setup is fully functional!")
        print("You can now run the crawler:")
        print("  python main.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\nPlease review the errors above and:")
        print("1. Check your .env file configuration")
        print("2. Verify Appwrite console setup")
        print("3. Refer to docs/APPWRITE_SETUP.md")
    print("\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
