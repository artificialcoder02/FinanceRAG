from langchain_community.llms import Ollama
from core.config import config

class LLMService:
    def __init__(self):
        self.llm = Ollama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.LLM_MODEL
        )

    def get_llm(self):
        return self.llm

llm_service = LLMService()
