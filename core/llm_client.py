import requests
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class CloudLLMClient(BaseLLMClient):
    """
    Cloud LLM client using OpenAI-compatible chat completions API.
    """

    def __init__(self, model: str, base_url: str, api_key: str, temperature: float, timeout: int = 120):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError(
                "LLM_API_KEY is not set. Please export LLM_API_KEY before running the pipeline."
            )

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a strict JSON extraction engine."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": self.temperature,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()
        data = response.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not content:
            raise ValueError("Cloud LLM returned empty content")

        return content
