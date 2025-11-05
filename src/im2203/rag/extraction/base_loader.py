from abc import ABC, abstractmethod
from typing import List
try:
    from langchain.schema import Document
except Exception:
    from langchain.docstore.document import Document

class BaseLoader(ABC):

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load documents from the specified source.
        
        Returns:
            List[Document]: A list of loaded Document objects.
        """
        pass