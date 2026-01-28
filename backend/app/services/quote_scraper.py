"""
Quote scraper service for fetching quotes from various online sources.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
import time

logger = logging.getLogger(__name__)


class QuoteScraper:
    """Service for scraping quotes from various online sources."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_quotes_from_brainyquote(self, topic: str, max_quotes: int = 5) -> List[Dict[str, str]]:
        """
        Fetch quotes from BrainyQuote based on a topic.
        
        Args:
            topic: The topic to search for
            max_quotes: Maximum number of quotes to fetch
            
        Returns:
            List of quote dictionaries with 'text', 'author', and 'source' keys
        """
        quotes = []
        try:
            # Clean topic for URL
            topic_clean = topic.lower().replace(' ', '_')
            url = f"https://www.brainyquote.com/topics/{topic_clean}-quotes"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quote_elements = soup.find_all('div', class_='grid-item', limit=max_quotes)
            
            for element in quote_elements:
                try:
                    text_elem = element.find('a', class_='b-qt')
                    author_elem = element.find('a', class_='bq-aut')
                    
                    if text_elem and author_elem:
                        quotes.append({
                            'text': text_elem.get_text(strip=True),
                            'author': author_elem.get_text(strip=True),
                            'source': url
                        })
                except Exception as e:
                    logger.warning(f"Error parsing quote element: {e}")
                    continue
            
            logger.info(f"Fetched {len(quotes)} quotes from BrainyQuote for topic: {topic}")
            
        except requests.RequestException as e:
            logger.error(f"Error fetching quotes from BrainyQuote: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in fetch_quotes_from_brainyquote: {e}")
        
        return quotes
    
    def fetch_quotes_from_goodreads(self, topic: str, max_quotes: int = 5) -> List[Dict[str, str]]:
        """
        Fetch quotes from Goodreads based on a topic.
        
        Args:
            topic: The topic to search for
            max_quotes: Maximum number of quotes to fetch
            
        Returns:
            List of quote dictionaries with 'text', 'author', and 'source' keys
        """
        quotes = []
        try:
            # Clean topic for URL
            topic_clean = topic.lower().replace(' ', '+')
            url = f"https://www.goodreads.com/quotes/search?q={topic_clean}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quote_elements = soup.find_all('div', class_='quote', limit=max_quotes)
            
            for element in quote_elements:
                try:
                    text_elem = element.find('div', class_='quoteText')
                    
                    if text_elem:
                        # Extract quote text (before the author tag)
                        quote_text = text_elem.get_text(strip=True)
                        # Remove the author part if it exists
                        if '―' in quote_text:
                            text, author = quote_text.split('―', 1)
                            text = text.strip().strip('"').strip('"').strip('"')
                            author = author.strip().split(',')[0].strip()
                        else:
                            text = quote_text.strip('"').strip('"').strip('"')
                            author = "Unknown"
                        
                        quotes.append({
                            'text': text,
                            'author': author,
                            'source': url
                        })
                except Exception as e:
                    logger.warning(f"Error parsing quote element: {e}")
                    continue
            
            logger.info(f"Fetched {len(quotes)} quotes from Goodreads for topic: {topic}")
            
        except requests.RequestException as e:
            logger.error(f"Error fetching quotes from Goodreads: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in fetch_quotes_from_goodreads: {e}")
        
        return quotes
    
    def fetch_quotes_by_topic(self, topic: str, max_quotes: int = 5) -> List[Dict[str, str]]:
        """
        Fetch quotes from multiple sources based on a topic.
        
        Args:
            topic: The topic to search for
            max_quotes: Maximum number of quotes to fetch per source
            
        Returns:
            Combined list of quote dictionaries from all sources
        """
        all_quotes = []
        
        # Try BrainyQuote first
        brainy_quotes = self.fetch_quotes_from_brainyquote(topic, max_quotes)
        all_quotes.extend(brainy_quotes)
        
        # Add a small delay to be respectful to servers
        time.sleep(1)
        
        # Try Goodreads if we need more quotes
        if len(all_quotes) < max_quotes:
            goodreads_quotes = self.fetch_quotes_from_goodreads(topic, max_quotes - len(all_quotes))
            all_quotes.extend(goodreads_quotes)
        
        return all_quotes[:max_quotes]


# Singleton instance
quote_scraper = QuoteScraper()

# Made with Bob