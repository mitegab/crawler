"""
Wired Scraper
Scrapes tech news articles from Wired.com
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class WiredScraper(BaseScraper):
    """Scraper for Wired website."""
    
    def extract_article_links(self, html: str) -> List[str]:
        """Extract article URLs from Wired homepage."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        # Wired uses summary items for articles
        for item in soup.find_all(['div', 'article'], class_=lambda x: x and 'summary' in str(x).lower()):
            link_tag = item.find('a', href=True)
            if link_tag:
                url = link_tag['href']
                if url.startswith('/'):
                    url = f"https://www.wired.com{url}"
                if 'wired.com/story/' in url:
                    links.append(url)
        
        return list(dict.fromkeys(links))
    
    def extract_article_content(self, url: str, html: str) -> Optional[Dict]:
        """Extract article content from Wired article page."""
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extract title
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else None
            
            if not title:
                return None
            
            # Extract article body
            article_body = soup.find('div', class_='article__body')
            if not article_body:
                article_body = soup.find('article')
            
            content = ''
            if article_body:
                paragraphs = article_body.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            # Extract author
            author = 'Wired Staff'
            author_tag = soup.find('a', {'rel': 'author'})
            if author_tag:
                author = author_tag.get_text(strip=True)
            
            # Extract published date
            time_tag = soup.find('time')
            published_date = time_tag.get('datetime', '') if time_tag else ''
            
            # Extract featured image
            featured_image = None
            picture_tag = soup.find('picture')
            if picture_tag:
                img_tag = picture_tag.find('img')
                if img_tag and img_tag.get('src'):
                    featured_image = img_tag['src']
            
            # Extract all images
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    images.append(src)
            
            return {
                'title': title,
                'content': content,
                'author': author,
                'published_date': published_date,
                'source_url': url,
                'featured_image': featured_image,
                'images': images,
                'category': 'Technology',
                'tags': [],
            }
        
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None
