import logging
from pathlib import Path
from typing import Any, Dict
import yaml

from im2203.rag.schemas.rag_config import RAGConfig
from .loader_registry import get_loader

class DocumentLoader:
    def __init__(self, config_path: Path):
        self.config_path = Path(config_path)
        self.config = self._load_config(self.config_path)

        self.input_file = Path(self.config.paths.input_file)
        self.output_vectorstore_dir = Path(self.config.paths.output_vectorstore_dir) # does not need this

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

    def load(self):
        """Run the configured document loader and return LangChain Document objects."""
        loader = self._get_loader()
        documents = loader.load()
        logging.info(f"Ingested {len(documents)} documents from {self.input_file}")
        return documents

    def _get_loader(self):
        """Instantiate a loader based on the extraction config."""
        extraction_cfg = getattr(self.config, "extraction", None)
        if not extraction_cfg:
            raise ValueError("Config missing 'extraction' block")

        loader_strategy = getattr(extraction_cfg, "default", None)
        if not loader_strategy:
            raise ValueError("Extraction config missing 'default' loader strategy")

        loader_kwargs = extraction_cfg.loaders.get(loader_strategy, {})  # e.g., {"mode": "single"}
        loader_kwargs["input_file"] = self.input_file

        logging.info(f"Using loader strategy '{loader_strategy}' for {self.input_file.resolve()} with kwargs: {loader_kwargs}")

        return get_loader(loader_strategy, **loader_kwargs)
