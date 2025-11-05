from pathlib import Path
import logging

from im2203.rag.schemas.rag_config import RAGConfig
from im2203.rag.components import BaseComponent
from .loader_registry import get_loader

class DocumentLoader(BaseComponent):
    def __init__(self, rag_config: RAGConfig):
        super().__init__(rag_config, "extraction")
        self.input_file = Path(rag_config.paths.input_file)

    def load(self):
        strategy, kwargs = self.get_strategy_config()
        kwargs["input_file"] = self.input_file

        logging.info(f"Using loader strategy '{strategy}' with kwargs: {kwargs}")
        loader = get_loader(strategy, **kwargs)
        documents = loader.load()
        logging.info(f"Ingested {len(documents)} documents from {self.input_file}")
        return documents
