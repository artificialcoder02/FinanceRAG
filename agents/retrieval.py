from core.database import db_service
from core.config import config
import logging

logger = logging.getLogger(__name__)

class RetrievalAgent:
    def __init__(self):
        self.retriever = db_service.get_retriever(k=config.SEARCH_RESULTS_LIMIT * 2) # Retrieve more for reranking

    def retrieve(self, query: str):
        """
        Retrieves relevant documents for a query.
        """
        logger.info(f"Retrieving documents for: {query}")
        try:
            docs = self.retriever.invoke(query)
            logger.info(f"Retrieved {len(docs)} documents")
            return docs
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []

retrieval_agent = RetrievalAgent()
