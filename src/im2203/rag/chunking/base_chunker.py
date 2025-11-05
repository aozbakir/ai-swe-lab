from abc import ABC, abstractmethod
from typing import List
from langchain.docstore.document import Document
import logging


class BaseChunker(ABC):
    """Abstract base class for document chunkers."""
    def __init__(self, **kwargs):
        self.params = kwargs
        logging.debug(f"{self.__class__.__name__} initialized with params: {kwargs}")

    @abstractmethod
    def chunk(self, documents: List[Document]) -> List[Document]:
        """Split input documents into chunks."""
        pass
