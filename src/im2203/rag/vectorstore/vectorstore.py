import logging
from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from im2203.rag.embeddings.document_embedder import DocumentEmbedder
from im2203.rag.core.components import BaseComponent
from im2203.rag.schemas.rag_config import RAGConfig

VECTORSTORE_REGISTRY = {
    "faiss": FAISS,
    # add more vector stores here in future
}

def get_vectorstore(strategy: str):
    vs_cls = VECTORSTORE_REGISTRY.get(strategy.lower())
    if not vs_cls:
        available = ", ".join(VECTORSTORE_REGISTRY.keys())
        logging.error(f"Unknown vectorstore strategy requested: {strategy}. Available: {available}")
        raise ValueError(f"Unknown vectorstore strategy '{strategy}'")
    logging.info(f"Using vector store '{strategy}'")
    return vs_cls


class DocumentVectorStore:
    """Handles creation, persistence, and querying of embedded documents."""

    def __init__(self, rag_config: RAGConfig, embedder: DocumentEmbedder):
        super().__init__(rag_config, "vectorstore")
        self.embedder = embedder

        strategy, kwargs = self.get_strategy_config()
        self.strategy = strategy
        self.kwargs = kwargs
        self.index_path = Path(self.kwargs.get("index_path", "faiss_index"))
        self.vs: FAISS | None = None

    def create(self, documents: list[Document], overwrite: bool = False) -> FAISS:
        """Create a new vector store if it doesn't exist or overwrite if specified."""
        if self.index_path.exists() and not overwrite:
            logging.warning(f"Vector store already exists at {self.index_path}. Skipping creation.")
            return self.load()
        
        logging.info(f"Creating {self.strategy} vector store with {len(documents)} documents")
        self.vs = FAISS.from_documents(documents, self.embedder)
        self.save()
        return self.vs

    def save(self):
        if not self.vs:
            raise ValueError("Vector store not initialized. Call 'create' first.")
        logging.info(f"Saving {self.strategy} vector store to {self.index_path}")
        self.vs.save_local(str(self.index_path))

    def load(self, allow_dangerous_deserialization: bool = True) -> FAISS:
        """Load existing vector store from disk."""
        if not self.index_path.exists():
            raise FileNotFoundError(f"Vector store path {self.index_path} does not exist")
        logging.info(f"Loading {self.strategy} vector store from {self.index_path}")
        self.vs = FAISS.load_local(
            str(self.index_path),
            self.embedder,
            allow_dangerous_deserialization=allow_dangerous_deserialization
        )
        return self.vs

    def query(self, text: str, k: int | None = None) -> List[Document]:
        if not self.vs:
            raise ValueError("Vector store not loaded. Call 'create' or 'load' first.")
        k = k or self.kwargs.get("top_k", 5)
        results = self.vs.similarity_search(text, k=k)
        logging.info(f"Query returned {len(results)} documents")
        return results