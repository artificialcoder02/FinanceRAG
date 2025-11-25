from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

class WebSearchAgent:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query: str):
        """
        Performs a web search and returns a list of results.
        """
        logger.info(f"Searching web for: {query}")
        try:
            # DDGS.text() returns a list of dicts: [{'title':..., 'href':..., 'body':...}]
            results = list(self.ddgs.text(query, max_results=10))
            
            # Normalize keys to match what pipeline expects (pipeline expects 'link' or 'href'?)
            # Pipeline uses result.get('link')
            # DDGS returns 'href'. Let's map it.
            normalized_results = []
            for r in results:
                normalized_results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
            
            return normalized_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

web_search_agent = WebSearchAgent()
