import requests
from abc import ABC, abstractmethod
import google.genai as genai

# 1. PARENT CLASS
class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

# 2. LOCAL CHILD CLASS (unchanged)
class OllamaLLMClient(BaseLLMClient):

    def __init__(self, model, base_url, temperature, timeout: int = 120):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.timeout = timeout

    #Local LLM Call
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,  # llama3:latest
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature
                }
            },
            timeout=self.timeout
        )

        response.raise_for_status()
        data = response.json()
        return data["response"].strip()

# 3. API CHILD CLASS
class GeminiLLMClient(BaseLLMClient):
    def __init__(self, model, api_key, temperature):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature

        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return response.text.strip()