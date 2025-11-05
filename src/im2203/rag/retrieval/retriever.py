

class Retriever:
    """Handles semantic search and context retrieval"""
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
    
    def retrieve_similar(self, query: str, k: int = 3):
        """
        Retrieve top-k similar documents and their metadata IDs.
        Returns:
            docs: List[Document]
            ids: List (from doc.metadata['id'])
        """
        # Access the underlying FAISS vectorstore
        if not hasattr(self.vectorstore, 'vectorstore'):
            raise ValueError("Vectorstore not properly initialized or loaded")
        
        retrieved_docs = self.vectorstore.vectorstore.similarity_search(query, k=k)
        doc_ids = [doc.metadata.get('id', '') for doc in retrieved_docs]  # Safely get ID from metadata
        return retrieved_docs, doc_ids