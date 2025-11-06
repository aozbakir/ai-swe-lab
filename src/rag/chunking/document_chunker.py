import logging

from langchain_core.documents import Document

from rag.schemas.rag_config import RAGConfig
from rag.core.components import BaseComponent
from .chunker_registry import get_chunker

class DocumentChunker(BaseComponent):
    def __init__(self, rag_config: RAGConfig):
        super().__init__(rag_config, "chunking")

    def chunk(self, documents: list[Document]) -> list[Document]:
        strategy, kwargs = self.get_strategy_config()
        logging.info(f"Using chunking strategy '{strategy}' with kwargs: {kwargs}")
        chunker = get_chunker(strategy, **kwargs)
        chunks = chunker.chunk(documents)
        logging.info(f"Chunked {len(chunks)} chunks from {len(documents)} documents")
        return chunks
