"""
Translation Function for Appwrite

This function translates articles from English to Amharic.
Can be triggered manually or automatically for new articles.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from translators.translator import Translator
from services.appwrite_manager import AppwriteManager


def main(req, res):
    """
    Appwrite Function entry point for translation.
    
    Args:
        req: Request object with article_id
        res: Response object
    """
    try:
        # Get article ID from request
        payload = json.loads(req.payload or '{}')
        article_id = payload.get('article_id')
        
        if not article_id:
            return res.json({
                'success': False,
                'error': 'article_id is required'
            }, 400)
        
        # Initialize services
        appwrite_manager = AppwriteManager()
        translator = Translator(service='google')
        
        # Get article from database
        article = appwrite_manager.get_article(article_id)
        
        if not article:
            return res.json({
                'success': False,
                'error': f'Article {article_id} not found'
            }, 404)
        
        # Translate article
        translated_article = translator.translate_article(article)
        
        # Update database with translation
        update_data = {
            'title_am': translated_article.get('title_am'),
            'content_am': translated_article.get('content_am'),
            'status': 'translated'
        }
        
        success = appwrite_manager.update_article(article_id, update_data)
        
        if success:
            result = {
                'success': True,
                'article_id': article_id,
                'message': 'Article translated successfully'
            }
            return res.json(result)
        else:
            return res.json({
                'success': False,
                'error': 'Failed to update article with translation'
            }, 500)
    
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        return res.json(error_result, 500)
