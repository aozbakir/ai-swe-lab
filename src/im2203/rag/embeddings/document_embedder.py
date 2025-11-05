from pathlib import Path
from typing import List
import yaml
import logging
from langchain.schema import Document

from .embedder_registry import get_embedder

class DocumentEmbedder:
    """Handles embedding of LangChain Document objects using a configurable embedding model."""

    def __init__(self, config_path: Path):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.embedder = self._init_embedder()

    def _load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _init_embedder(self):
        embeddings_cfg = self.config.get("embeddings", {})
        strategy = embeddings_cfg.get("default", "sentence_transformers")
        kwargs = embeddings_cfg.get("models", {}).get(strategy, {})  # use 'models' as you prefer
        logging.info(f"Initializing embedder '{strategy}' with params: {kwargs}")
        return get_embedder(strategy, **kwargs)

    def embed_documents(self, documents: List[Document]):
        """Return embeddings for a list of LangChain Document objects."""
        texts = [doc.page_content for doc in documents]
        logging.info(f"Embedding {len(texts)} documents")
        return self.embedder.embed_documents(texts)

    def embed_query(self, query: str):
        """Return embedding for a single query string."""
        return self.embedder.embed_query(query)
