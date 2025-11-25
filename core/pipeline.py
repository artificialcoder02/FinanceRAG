import logging
from agents.web_search import web_search_agent
from agents.web_scraper import web_scraper_agent
from agents.preprocessing import preprocessing_agent
from agents.indexing import indexing_agent
from agents.retrieval import retrieval_agent
from agents.reranker import reranker_agent
from agents.answering import answering_agent
from agents.evaluation import evaluation_agent

logger = logging.getLogger(__name__)

class FinanceRAGPipeline:
    def run(self, query: str):
        logger.info(f"Starting pipeline for query: {query}")
        
        # 1. Web Search
        search_results = web_search_agent.search_web(query)
        logger.info(f"Found {len(search_results)} search results")
        
        # 2. Web Scraping & Preprocessing
        all_docs = []
        for result in search_results:
            url = result.get('link')
            if not url:
                continue
                
            scraped_data = web_scraper_agent.scrape_url(url)
            if scraped_data:
                docs = preprocessing_agent.process_text(scraped_data['text'], scraped_data['metadata'])
                all_docs.extend(docs)
        
        logger.info(f"Scraped and processed {len(all_docs)} chunks")
        
        # 3. Indexing
        indexing_agent.index_documents(all_docs)
        
        # 4. Retrieval
        retrieved_docs = retrieval_agent.retrieve(query)
        
        # 5. Reranking
        reranked_docs = reranker_agent.rerank(query, retrieved_docs)
        
        # 6. Answering
        answer = answering_agent.generate_answer(query, reranked_docs)
        
        # 7. Evaluation
        eval_result = evaluation_agent.evaluate(query, answer, reranked_docs)
        
        return {
            "answer": answer,
            "sources": [doc.metadata for doc in reranked_docs],
            "evaluation": eval_result
        }

pipeline = FinanceRAGPipeline()
