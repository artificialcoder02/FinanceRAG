import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

class WebScraperAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_url(self, url: str):
        """
        Scrapes text from a URL.
        """
        logger.info(f"Scraping URL: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()

            text = soup.get_text(separator='\n')
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            metadata = {
                "source": url,
                "title": soup.title.string if soup.title else "No Title"
            }
            
            return {"text": clean_text, "metadata": metadata}
            
        except Exception as e:
            logger.error(f"Scraping failed for {url}: {e}")
            return None

web_scraper_agent = WebScraperAgent()
