from langchain_community.llms import Ollama
from core.config import config

from langchain_google_genai import ChatGoogleGenerativeAI

class LLMService:
    def __init__(self):
        if config.LLM_PROVIDER == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model=config.LLM_MODEL,
                google_api_key=config.GOOGLE_API_KEY,
                temperature=0
            )
        else:
            self.llm = Ollama(
                base_url=config.OLLAMA_BASE_URL,
                model=config.LLM_MODEL
            )

    def get_llm(self):
        return self.llm

llm_service = LLMService()
