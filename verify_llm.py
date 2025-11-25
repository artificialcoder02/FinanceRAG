from core.llm import llm_service
import os
from dotenv import load_dotenv

load_dotenv()

print(f"Testing LLM Provider: {os.getenv('LLM_PROVIDER', 'gemini')}")
print(f"API Key present: {bool(os.getenv('GOOGLE_API_KEY'))}")

try:
    response = llm_service.get_llm().invoke("Hello, are you Gemini?")
    print("Success:", response.content)
except Exception as e:
    print("Error:", e)
