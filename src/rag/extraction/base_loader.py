from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load documents from the specified source.
        
        Returns:
            List[Document]: A list of loaded Document objects.
        """
        pass