import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from core.config import config
import os

class DatabaseService:
    def __init__(self):
        self.embedding_function = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL_NAME
        )
        
        self.vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=self.embedding_function,
            persist_directory=config.CHROMA_DB_DIR
        )

    def get_vector_store(self):
        return self.vector_store
    
    def get_retriever(self, k=10):
        return self.vector_store.as_retriever(search_kwargs={"k": k})

db_service = DatabaseService()
