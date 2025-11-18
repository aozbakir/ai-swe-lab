from openai import OpenAI
from llm_utils.interfaces.base import BaseLLM

class OpenAIChat(BaseLLM):
    """Simple OpenAI LLM wrapper (plain, no tools)."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model_name = model_name

    def name(self) -> str:
        return f"openai-plain:{self.model_name}"

    def metadata(self) -> dict:
        return {"backend": "openai", "capabilities": ["chat"]}

    def generate(self, prompt: str) -> str:
        """Send a single prompt to OpenAI and return the response content."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def invoke(self, messages: list) -> str:
        """Send a list of messages to OpenAI and return the response content."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return response.choices[0].message.content
