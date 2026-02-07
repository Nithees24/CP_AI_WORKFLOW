import requests
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OllamaLLMClient(BaseLLMClient):
    """
    Ollama LLM client using OpenAI-compatible API.
    Works with Llama 3 / Llama 3.x models.
    """

    def __init__(self,model,base_url,temperature,timeout: int = 120):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout


#this portion process the page chunk with the prompt and give back the solution
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
