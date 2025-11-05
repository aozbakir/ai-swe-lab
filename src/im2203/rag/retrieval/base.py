from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseRetriever(ABC):
    """Abstract retriever interface."""
    
    @abstractmethod
    def retrieve(self, query: str) -> List[Document]:
        """Retrieve relevant documents for a query."""
        pass
