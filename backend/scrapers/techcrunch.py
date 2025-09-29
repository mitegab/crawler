"""
TechCrunch Scraper
Scrapes tech news articles from TechCrunch.com
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class TechCrunchScraper(BaseScraper):
    """Scraper for TechCrunch website."""
    
    def extract_article_links(self, html: str) -> List[str]:
        """Extract article URLs from TechCrunch homepage."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        # TechCrunch article links
        for article in soup.find_all('article', class_='post-block'):
            link_tag = article.find('a', href=True)
            if link_tag:
                url = link_tag['href']
                if url.startswith('http') and 'techcrunch.com' in url:
                    links.append(url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def extract_article_content(self, url: str, html: str) -> Optional[Dict]:
        """Extract article content from TechCrunch article page."""
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extract title
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else None
            
            if not title:
                return None
            
            # Extract article content
            content_div = soup.find('div', class_='article-content')
            if not content_div:
                content_div = soup.find('article')
            
            content = ''
            if content_div:
                paragraphs = content_div.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            # Extract author
            author_tag = soup.find('a', {'rel': 'author'})
            author = author_tag.get_text(strip=True) if author_tag else 'TechCrunch Staff'
            
            # Extract published date
            time_tag = soup.find('time')
            published_date = time_tag.get('datetime', '') if time_tag else ''
            
            # Extract featured image
            featured_image = None
            img_tag = soup.find('img', class_='wp-post-image')
            if img_tag and img_tag.get('src'):
                featured_image = img_tag['src']
            
            # Extract all images
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    images.append(src)
            
            # Extract category/tags
            category = 'Technology'
            tags = []
            tag_links = soup.find_all('a', {'rel': 'tag'})
            for tag_link in tag_links:
                tags.append(tag_link.get_text(strip=True))
            
            return {
                'title': title,
                'content': content,
                'author': author,
                'published_date': published_date,
                'source_url': url,
                'featured_image': featured_image,
                'images': images,
                'category': category,
                'tags': tags,
            }
        
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None
