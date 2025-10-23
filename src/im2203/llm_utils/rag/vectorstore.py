from typing import List

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

class VectorStore:
    """Handles embedding generation and vector database management"""
    def __init__(self, embeddings=None, store_path="vector_store"):
        self.embeddings = embeddings or OpenAIEmbeddings()
        self.store_path = store_path
        self.vectorstore = None
    
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
