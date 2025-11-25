from core.database import db_service
from langchain_core.documents import Document
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingIndexingAgent:
    def __init__(self):
        self.vector_store = db_service.get_vector_store()

    def index_documents(self, documents: List[Document]):
        """
        Embeds and indexes documents into the vector store.
        """
        logger.info(f"Indexing {len(documents)} documents")
        try:
            if not documents:
                return
            
            self.vector_store.add_documents(documents)
            logger.info("Indexing complete")
        except Exception as e:
            logger.error(f"Indexing failed: {e}")

indexing_agent = EmbeddingIndexingAgent()
