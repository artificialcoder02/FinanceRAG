from duckduckgo_search import DDGS
import logging
from core.config import config

logger = logging.getLogger(__name__)

class WebSearchAgent:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query: str):
        """
        Performs a web search using DuckDuckGo and returns a list of results.
        """
        logger.info(f"Searching web for: {query}")
        try:
            max_results = config.SEARCH_RESULTS_LIMIT
            results = list(self.ddgs.text(query, max_results=max_results))
            
            # Normalize keys to match what pipeline expects
            normalized_results = []
            for r in results:
                normalized_results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
            
            logger.info(f"DuckDuckGo search succeeded: {len(normalized_results)} results")
            return normalized_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

web_search_agent = WebSearchAgent()

