from typing import Any
from openai import OpenAI  # type: ignore


class AIAssistant:
    def __init__(self, api_host: str, api_key: str, model: str, temperature: float) -> None:
        self.client = OpenAI(base_url=api_host, api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate_streaming_response(self, messages: list[dict[str, str]]) -> Any:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        )
        return response
