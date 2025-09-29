"""
Ars Technica Scraper
Scrapes tech news articles from ArsTechnica.com
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class ArsTechnicaScraper(BaseScraper):
    """Scraper for Ars Technica website."""
    
    def extract_article_links(self, html: str) -> List[str]:
        """Extract article URLs from Ars Technica homepage."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        # Find article links
        for article in soup.find_all('article'):
            link_tag = article.find('a', href=True)
            if link_tag:
                url = link_tag['href']
                if url.startswith('/'):
                    url = f"https://arstechnica.com{url}"
                if 'arstechnica.com' in url:
                    links.append(url)
        
        return list(dict.fromkeys(links))
    
    def extract_article_content(self, url: str, html: str) -> Optional[Dict]:
        """Extract article content from Ars Technica article page."""
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extract title
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else None
            
            if not title:
                return None
            
            # Extract article content
            article_content = soup.find('div', class_='article-content')
            if not article_content:
                article_content = soup.find('article')
            
            content = ''
            if article_content:
                paragraphs = article_content.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            # Extract author
            author = 'Ars Technica Staff'
            author_tag = soup.find('span', class_='author')
            if author_tag:
                author = author_tag.get_text(strip=True)
            
            # Extract published date
            time_tag = soup.find('time')
            published_date = time_tag.get('datetime', '') if time_tag else ''
            
            # Extract featured image
            featured_image = None
            img_tag = soup.find('img', class_='featured-image')
            if not img_tag:
                img_tag = soup.find('figure', class_='featured-image')
                if img_tag:
                    img_tag = img_tag.find('img')
            
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
