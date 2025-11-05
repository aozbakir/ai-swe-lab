from typing import List, Optional
import yaml

from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from im2203.llm_utils.schemas.embedding_config import EmbeddingConfig
from im2203.llm_utils.embeddings.custom_embeddings import CustomEmbeddings


class VectorStore:
    """Handles embedding generation and vector database management"""
    def __init__(
        self,
        embedding_config: Optional[EmbeddingConfig] = None,
        store_path: str = "vector_store"
    ):
        if embedding_config is None:
            # Default to sentence transformers if no config provided
            embedding_config = EmbeddingConfig()
        
        self.embeddings = CustomEmbeddings(embedding_config)
        self.store_path = store_path
        self.vectorstore = None
        
    @classmethod
    def from_yaml(cls, config_path: str, store_path: str = "vector_store"):
        """Create VectorStore from YAML config file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        embedding_config = EmbeddingConfig(**config.get('embeddings', {}))
        return cls(embedding_config=embedding_config, store_path=store_path)
    
    def build_from_chunks(self, chunks: List[Document]):
        """Create vector store from document chunks"""
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        print(f"Vector store built with {len(chunks)} embeddings.")
    
    def persist(self):
        """Save vector store to disk"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call build_from_chunks() first.")
        self.vectorstore.save_local(self.store_path)
        print(f"Vector store persisted to {self.store_path}")
    
    def load(self):
        """Load existing vector store from disk"""
        self.vectorstore = FAISS.load_local(
            self.store_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Vector store loaded from {self.store_path}")
        return self.vectorstore
