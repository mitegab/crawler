"""
Translation Service
Handles translation of articles from English to Amharic
"""

import os
from typing import Optional, Dict
from googletrans import Translator as GoogleTranslator


class Translator:
    """
    Translation service for converting English content to Amharic.
    Supports multiple translation backends (Google, Azure, OpenAI).
    """
    
    def __init__(self, service: str = 'google'):
        """
        Initialize translator with specified service.
        
        Args:
            service: Translation service to use ('google', 'azure', 'openai')
        """
        self.service = service
        self.source_lang = 'en'
        self.target_lang = 'am'  # Amharic
        
        if service == 'google':
            self.translator = GoogleTranslator()
        elif service == 'azure':
            # Azure Translator setup (requires azure-ai-translation-text package)
            self.azure_key = os.getenv('AZURE_TRANSLATOR_KEY')
            self.azure_endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
            self.azure_region = os.getenv('AZURE_TRANSLATOR_REGION')
        elif service == 'openai':
            # OpenAI setup (requires openai package)
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    def translate_text(self, text: str) -> Optional[str]:
        """
        Translate text from English to Amharic.
        
        Args:
            text: English text to translate
            
        Returns:
            Translated Amharic text or None if failed
        """
        if not text or not text.strip():
            return text
        
        try:
            if self.service == 'google':
                return self._translate_google(text)
            elif self.service == 'azure':
                return self._translate_azure(text)
            elif self.service == 'openai':
                return self._translate_openai(text)
            else:
                raise ValueError(f"Unsupported translation service: {self.service}")
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None
    
    def _translate_google(self, text: str) -> Optional[str]:
        """Translate using Google Translate API."""
        # Split long text into chunks (Google has character limits)
        max_length = 5000
        if len(text) > max_length:
            chunks = self._split_text(text, max_length)
            translated_chunks = []
            
            for chunk in chunks:
                result = self.translator.translate(chunk, src=self.source_lang, dest=self.target_lang)
                translated_chunks.append(result.text)
            
            return '\n\n'.join(translated_chunks)
        else:
            result = self.translator.translate(text, src=self.source_lang, dest=self.target_lang)
            return result.text
    
    def _translate_azure(self, text: str) -> Optional[str]:
        """Translate using Azure Translator API."""
        # TODO: Implement Azure Translator
        # Requires azure-ai-translation-text package
        raise NotImplementedError("Azure Translator not yet implemented")
    
    def _translate_openai(self, text: str) -> Optional[str]:
        """Translate using OpenAI GPT API."""
        # TODO: Implement OpenAI translation
        # Can provide better context and technical term handling
        raise NotImplementedError("OpenAI Translator not yet implemented")
    
    def _split_text(self, text: str, max_length: int) -> list:
        """
        Split text into chunks at sentence boundaries.
        
        Args:
            text: Text to split
            max_length: Maximum length of each chunk
            
        Returns:
            List of text chunks
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = ''
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:
                current_chunk += sentence + '. '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_article(self, article: Dict) -> Dict:
        """
        Translate an entire article (title and content).
        
        Args:
            article: Dictionary containing article data
            
        Returns:
            Article dictionary with translated fields added
        """
        print(f"Translating article: {article.get('title', 'Unknown')}")
        
        # Translate title
        translated_title = self.translate_text(article.get('title', ''))
        
        # Translate content
        translated_content = self.translate_text(article.get('content', ''))
        
        # Add translated fields to article
        article['title_am'] = translated_title
        article['content_am'] = translated_content
        article['translation_service'] = self.service
        
        return article
