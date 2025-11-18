# src/app/chat/chat_logic.py
from pathlib import Path
from typing import Union

from llm_utils.factory import LLMFactory
from rag.configs.rag_config_loader import RAGConfigLoader
from rag.embeddings.document_vectorstore import DocumentVectorStore
from rag.embeddings.document_embedder import DocumentEmbedder
from rag.prompts.prompt import PromptTemplate
from rag.retrieval.vector_retriever import VectorRetriever
from rag.retrieval.qa_retriever import QARetriever


class ChatLogic:
    """
    RAG-based chat logic for document Q&A.

    Can accept an optional LLM instance and a prompt template.
    """

    def __init__(
        self,
        config_path: Path,
        llm=None,
        prompt=None,
        search_type="mmr",
        top_k=None
    ):

        # Load RAG configuration
        rag_config_loader = RAGConfigLoader(config_path)
        self.rag_config = rag_config_loader.config

        # Initialize embeddings and vector store
        embedder = DocumentEmbedder(self.rag_config).embedder
        self.vectorstore = DocumentVectorStore(
            embedder=embedder,
            config=self.rag_config.model_dump()
        )
        self.vectorstore.index = self.vectorstore.load()


        # Initialize prompt template
        self.prompt_template = PromptTemplate(self.rag_config)

        # Initialize LLM
        llm_factory = LLMFactory()
        llm = llm_factory.create_from_yaml_file(config_path)

        # Initialize QA retriever pipeline
        retrieval_config = self.rag_config.retrieval.vectorstore

        retriever_kwargs = {
            'vectorstore': self.vectorstore,
            'top_k': top_k or retrieval_config.top_k,
            'search_type': search_type,
        }
        if search_type == "mmr":
            retriever_kwargs.update({"fetch_k": 20, "lambda_mult": 0.7})

        retriever = VectorRetriever(**retriever_kwargs)

        self.pipeline = QARetriever(
            retriever=retriever,
            llm=llm,
            prompt_template=self.prompt_template
        )
        

    def answer(self, query: str) -> dict:
        response, retrieved_docs = self.pipeline.run(query=query, verbose=False)

        # Ensure retrieved_docs is always a list of Document-like objects
        retrieved_docs = [doc for doc in retrieved_docs if hasattr(doc, "page_content")]


        ChatLogic.print_doc_fragments(retrieved_docs)

        return {
            "response": response,
            "retrieved_docs": retrieved_docs
        }

    @staticmethod
    def print_doc_fragments(docs, fragment_len=200):
        print("Retrieved document fragments:")
        for i, doc in enumerate(docs):
            fragment = getattr(doc, "page_content", str(doc))[:fragment_len]
            print(f"Doc {i+1}: {fragment!r}")
