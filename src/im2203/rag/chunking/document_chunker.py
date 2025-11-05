import logging
from pathlib import Path
from typing import List
import yaml

from langchain.schema import Document

from im2203.rag.schemas.rag_config import RAGConfig
from .chunker_registry import get_chunker

class DocumentChunker:
    def __init__(self, config_path: Path):
        self.config_path = Path(config_path)
        self.config = self._load_config(self.config_path)

    def _load_config(self, config_path: Path) -> RAGConfig:
        """Load and validate YAML configuration into a RAGConfig object."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        try:
            return RAGConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Invalid configuration format: {e}")

    def chunk(self, documents: List[Document]) -> List[Document]:
        """
        Chunk a list of LangChain Document objects based on the configured strategy.
        """
        chunker = self._get_chunker()
        chunks = chunker.chunk(documents)
        logging.info(f"Chunked {len(chunks)} chunks from {len(documents)} documents")
        return chunks

    def _get_chunker(self):
        """Instantiate a chunker based on the extraction config."""
        chunking_cfg = getattr(self.config, "chunking", None)
        if not chunking_cfg:
            raise ValueError("Config missing 'chunking' block")

        chunking_strategy = getattr(chunking_cfg, "default", None)
        if not chunking_strategy:
            raise ValueError("Chunking config missing 'default' strategy")

        chunking_dict = chunking_cfg.dict()
        chunker_kwargs = chunking_dict.get(chunking_strategy, {}) or {}

        logging.info(
            f"Using chunking strategy '{chunking_strategy}' with kwargs: {chunker_kwargs}"
        )
        return get_chunker(chunking_strategy, **chunker_kwargs)
