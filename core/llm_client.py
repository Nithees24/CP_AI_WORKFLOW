from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM  # LangChain's Ollama wrapper
import google.genai as genai
from google.genai import types


# 1. PARENT CLASS
class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


# 2. LOCAL CHILD CLASS — now using LangChain wrapper
class OllamaLLMClient(BaseLLMClient):

    def __init__(self, model, base_url, temperature, timeout: int = 120):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.timeout = timeout

        # LangChain OllamaLLM replaces the manual requests.post call
        self._llm = OllamaLLM(
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature,
        )

    def generate(self, prompt: str) -> str:
        response = self._llm.invoke(prompt)
        return response.strip()


# 3. API CHILD CLASS (unchanged)
class GeminiLLMClient(BaseLLMClient):
    def __init__(self, model, api_key, temperature):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=self.temperature)
        )
        return response.text.strip()