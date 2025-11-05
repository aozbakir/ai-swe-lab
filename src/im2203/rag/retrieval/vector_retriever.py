import logging
from typing import List, Optional

from langchain_core.documents import Document

from im2203.rag.retrieval.base import BaseRetriever
from im2203.rag.embeddings.document_vectorstore import DocumentVectorStore

class VectorRetriever(BaseRetriever):
    """Unified vector store retriever supporting different search strategies."""
    
    def __init__(
        self,
        vectorstore: DocumentVectorStore,
        top_k: int,
        search_type: str = "similarity",
        score_threshold: float = 0.0,
        fetch_k: Optional[int] = None,
        lambda_mult: float = 0.5,
    ):
        """
        Initialize retriever.
        
        Args:
            vectorstore: Vector store instance
            top_k: Number of documents to return
            search_type: Search strategy ("similarity" or "mmr")
            score_threshold: Minimum similarity score for documents
            fetch_k: Number of documents to fetch before reranking (for MMR)
            lambda_mult: Balance between relevance (1.0) and diversity (0.0) for MMR
        """
        self.vectorstore = vectorstore
        self.top_k = top_k
        self.search_type = search_type
        self.score_threshold = score_threshold
        self.fetch_k = fetch_k
        self.lambda_mult = lambda_mult

    def retrieve(self, query: str) -> List[Document]:
        """Get documents using configured search strategy."""
        logging.info(
            f"Retrieving top {self.top_k} docs using {self.search_type} search "
            f"(threshold={self.score_threshold})"
        )
        
        return self.vectorstore.query(
            text=query,
            k=self.top_k,
            search_type=self.search_type,
            score_threshold=self.score_threshold,
            fetch_k=self.fetch_k,
            lambda_mult=self.lambda_mult
        )
