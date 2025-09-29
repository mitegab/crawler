"""
Appwrite Manager
Handles all interactions with Appwrite backend services
"""

import os
from typing import Dict, List, Optional
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.exception import AppwriteException


class AppwriteManager:
    """
    Manager for Appwrite backend operations including:
    - Database operations (CRUD for articles)
    - File storage (images)
    - Authentication
    """
    
    def __init__(self):
        """Initialize Appwrite client and services."""
        # Initialize client
        self.client = Client()
        
        endpoint = os.getenv('APPWRITE_ENDPOINT', 'https://cloud.appwrite.io/v1')
        project_id = os.getenv('APPWRITE_PROJECT_ID')
        api_key = os.getenv('APPWRITE_API_KEY')
        
        if not project_id or not api_key:
            raise ValueError("APPWRITE_PROJECT_ID and APPWRITE_API_KEY must be set in environment")
        
        self.client.set_endpoint(endpoint)
        self.client.set_project(project_id)
        self.client.set_key(api_key)
        
        # Initialize services
        self.databases = Databases(self.client)
        self.storage = Storage(self.client)
        
        # Configuration
        self.database_id = os.getenv('APPWRITE_DATABASE_ID', 'tech-news-db')
        self.articles_collection_id = os.getenv('APPWRITE_ARTICLES_COLLECTION_ID', 'articles')
        self.storage_bucket_id = os.getenv('APPWRITE_STORAGE_BUCKET_ID', 'article-images')
    
    def save_article(self, article: Dict) -> Optional[Dict]:
        """
        Save an article to the database.
        
        Args:
            article: Article dictionary with all fields
            
        Returns:
            Document dict if successful, None otherwise
        """
        try:
            # Prepare document data matching the database schema
            # Schema: title, title_am, url, summary, summary_am, source, image_url, published_date, category
            document_data = {
                'title': article.get('title', ''),
                'title_am': article.get('title_am', ''),
                'url': article.get('url', article.get('source_url', '')),
                'summary': article.get('summary', article.get('content', '')[:500] if article.get('content') else ''),
                'summary_am': article.get('summary_am', ''),
                'source': article.get('source', ''),
                'image_url': article.get('image_url', article.get('featured_image', '')),
                'published_date': article.get('published_date', ''),
                'category': article.get('category', 'Technology'),
            }
            
            # Create document
            result = self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.articles_collection_id,
                document_id=ID.unique(),
                data=document_data
            )
            
            return result
        
        except AppwriteException as e:
            print(f"Appwrite error saving article: {e.message}")
            return None
        except Exception as e:
            print(f"Error saving article: {str(e)}")
            return None
    
    def get_article(self, document_id: str) -> Optional[Dict]:
        """
        Retrieve an article by ID.
        
        Args:
            document_id: The document ID
            
        Returns:
            Article document or None
        """
        try:
            result = self.databases.get_document(
                database_id=self.database_id,
                collection_id=self.articles_collection_id,
                document_id=document_id
            )
            return result
        except AppwriteException as e:
            print(f"Appwrite error getting article: {e.message}")
            return None
    
    def list_articles(self, limit: int = 25, offset: int = 0) -> List[Dict]:
        """
        List articles with pagination.
        
        Args:
            limit: Number of articles to return
            offset: Number of articles to skip
            
        Returns:
            List of article documents
        """
        try:
            result = self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.articles_collection_id,
                queries=[
                    f'limit({limit})',
                    f'offset({offset})',
                    'orderDesc("scraped_at")'
                ]
            )
            return result['documents']
        except AppwriteException as e:
            print(f"Appwrite error listing articles: {e.message}")
            return []
    
    def update_article(self, document_id: str, data: Dict) -> bool:
        """
        Update an article document.
        
        Args:
            document_id: The document ID
            data: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.databases.update_document(
                database_id=self.database_id,
                collection_id=self.articles_collection_id,
                document_id=document_id,
                data=data
            )
            return True
        except AppwriteException as e:
            print(f"Appwrite error updating article: {e.message}")
            return False
    
    def delete_article(self, document_id: str) -> bool:
        """
        Delete an article.
        
        Args:
            document_id: The document ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.databases.delete_document(
                database_id=self.database_id,
                collection_id=self.articles_collection_id,
                document_id=document_id
            )
            return True
        except AppwriteException as e:
            print(f"Appwrite error deleting article: {e.message}")
            return False
    
    def upload_image(self, file_path: str, file_name: str) -> Optional[str]:
        """
        Upload an image to Appwrite Storage.
        
        Args:
            file_path: Local path to the file
            file_name: Name for the uploaded file
            
        Returns:
            File ID if successful, None otherwise
        """
        try:
            with open(file_path, 'rb') as file:
                result = self.storage.create_file(
                    bucket_id=self.storage_bucket_id,
                    file_id=ID.unique(),
                    file=file
                )
                return result['$id']
        except AppwriteException as e:
            print(f"Appwrite error uploading image: {e.message}")
            return None
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return None
