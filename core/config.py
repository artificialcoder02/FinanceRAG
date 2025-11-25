import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "finance_rag")
    
    # LLM Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
    
    # Embedding Settings
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Search Settings
    SEARCH_RESULTS_LIMIT = int(os.getenv("SEARCH_RESULTS_LIMIT", "10"))
    
    # Reranker Settings
    RERANKER_MODEL_NAME = os.getenv("RERANKER_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")

config = Config()
