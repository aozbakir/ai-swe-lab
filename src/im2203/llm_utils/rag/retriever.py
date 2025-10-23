

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
        retrieved_docs = self.vectorstore.similarity_search(query, k=k)
        doc_ids = [doc.id for doc in retrieved_docs]
        return retrieved_docs, doc_ids