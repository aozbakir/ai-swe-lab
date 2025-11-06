from abc import ABC, abstractmethod
from typing import List, Any

class BaseEmbedder(ABC):
    """Abstract base class for embedding models."""

    def __init__(self, **kwargs):
        self.params = kwargs

    @abstractmethod
    def embed(self, texts: List[str]) -> List[Any]:
        """Embed a list of texts into vector representations."""
        pass