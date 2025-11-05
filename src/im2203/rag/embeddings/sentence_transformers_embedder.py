from typing import List

from .base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", **kwargs):
        super().__init__(**kwargs)
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[list[float]]:
        return self.model.encode(texts, show_progress_bar=True).tolist()
