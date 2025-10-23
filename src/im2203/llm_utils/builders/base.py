from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel

class LLMBuilder(ABC):
    """Abstract base class for LLM builders using the Strategy Pattern"""
    
    @abstractmethod
    def build(self, **kwargs) -> BaseChatModel:
        """Build and return a LangChain LLM instance"""
        pass