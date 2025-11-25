from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class PreprocessingAgent:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )

    def process_text(self, text: str, metadata: dict):
        """
        Splits text into chunks and returns Document objects.
        """
        logger.info(f"Processing text from: {metadata.get('source', 'unknown')}")
        try:
            docs = self.text_splitter.create_documents([text], metadatas=[metadata])
            return docs
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return []

preprocessing_agent = PreprocessingAgent()
