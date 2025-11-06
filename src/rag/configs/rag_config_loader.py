from pathlib import Path
import yaml

from rag.schemas.rag_config import RAGConfig

class RAGConfigLoader:
    def __init__(self, path: Path):
        self.path = path
        self.config = self._load_config()

    def _load_config(self) -> RAGConfig:
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return RAGConfig(**data)