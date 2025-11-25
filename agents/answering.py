from core.llm import llm_service
from langchain_core.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

class AnsweringAgent:
    def __init__(self):
        self.llm = llm_service.get_llm()
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are FinanceRAG, an expert financial assistant.
            Answer the user's question using ONLY the provided context.
            
            Context:
            {context}
            
            Question:
            {question}
            
            Rules:
            1. If information is present, answer clearly.
            2. If not present, say "Data not found in retrieved context".
            3. Use citations in the format [Source Title].
            4. Do not hallucinate.
            
            Answer:"""
        )

    def generate_answer(self, query: str, context_docs: list):
        """
        Generates an answer based on the query and context documents.
        """
        logger.info(f"Generating answer for: {query}")
        try:
            # Format context
            context_text = "\n\n".join([f"Source: {doc.metadata.get('title', 'Unknown')}\nContent: {doc.page_content}" for doc in context_docs])
            
            prompt = self.prompt_template.format(context=context_text, question=query)
            response = self.llm.invoke(prompt)
            
            return response
        except Exception as e:
            logger.error(f"Answer generation failed: {e}")
            return "Sorry, I encountered an error while generating the answer."

answering_agent = AnsweringAgent()
