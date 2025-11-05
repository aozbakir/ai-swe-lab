from typing import List

from .base_embedder import BaseEmbedder
import openai

class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "text-embedding-3-small", **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name

    def embed(self, texts: List[str]) -> List[list[float]]:
        responses = openai.Embedding.create(
            model=self.model_name,
            input=texts
        )
        return [r["embedding"] for r in responses["data"]]
