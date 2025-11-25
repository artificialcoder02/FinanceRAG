from sentence_transformers import CrossEncoder
from core.config import config
import logging

logger = logging.getLogger(__name__)

class RerankerAgent:
    def __init__(self):
        # Load model only when needed or at startup? Startup is better.
        # Using a small model for speed.
        try:
            self.model = CrossEncoder(config.RERANKER_MODEL_NAME)
        except Exception as e:
            logger.warning(f"Could not load reranker model: {e}. Reranking will be skipped.")
            self.model = None

    def rerank(self, query: str, docs: list, top_k: int = 5):
        """
        Reranks documents based on relevance to the query.
        """
        if not self.model or not docs:
            return docs[:top_k]
        
        logger.info(f"Reranking {len(docs)} documents")
        try:
            # Prepare pairs [query, doc_text]
            pairs = [[query, doc.page_content] for doc in docs]
            scores = self.model.predict(pairs)
            
            # Combine docs with scores
            doc_score_pairs = list(zip(docs, scores))
            
            # Sort by score descending
            doc_score_pairs.sort(key=lambda x: x[1], reverse=True)
            
            # Return top_k docs
            reranked_docs = [doc for doc, score in doc_score_pairs[:top_k]]
            return reranked_docs
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return docs[:top_k]

reranker_agent = RerankerAgent()
