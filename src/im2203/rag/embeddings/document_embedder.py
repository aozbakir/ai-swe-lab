import logging

from langchain_core.documents import Document

from im2203.rag.schemas.rag_config import RAGConfig
from im2203.rag.components import BaseComponent
from .embedder_registry import get_embedder

class DocumentEmbedder(BaseComponent):
    def __init__(self, rag_config: RAGConfig):
        super().__init__(rag_config, "embeddings")
        strategy, kwargs = self.get_strategy_config()
        logging.info(f"Initializing embedder '{strategy}' with params: {kwargs}")
        self.embedder = get_embedder(strategy, **kwargs)

    def embed_documents(self, documents: list[Document]):
        texts = [doc.page_content for doc in documents]
        logging.info(f"Embedding {len(texts)} documents")
        return self.embedder.embed_documents(texts)

    def embed_query(self, query: str):
        return self.embedder.embed_query(query)
