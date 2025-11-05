"""RAG Pipeline implementation."""

from typing import Tuple
import time

from langchain_core.language_models import BaseChatModel

from im2203.rag.embeddings.document_vectorstore import DocumentVectorStore
from im2203.rag.prompts.prompt import PromptTemplate


def rag_query(query: str,
            vectorstore: DocumentVectorStore,
            llm: BaseChatModel,
            prompt_template: PromptTemplate,
            k: int = 2,
            verbose: bool = False) -> Tuple[str, float]:
    """Query the RAG system with a question.
    
    Args:
        query: The question to ask
        vectorstore: Vector store for document retrieval
        llm: Language model for generation
        prompt_template: Template for formatting prompt
        k: Number of documents to retrieve
        verbose: If True, print debug information
        
    Returns:
        tuple[str, float]: Generated response and time taken
    """
    # Start timing the entire operation
    start_time = time.time()
    
    # Debug header
    if verbose:
        print("\nDEBUG INFO:")
        print("-" * 20)
        print(f"Processing: {query!r}")
    
    # Retrieve relevant documents
    results = vectorstore.query(query, k=k)
    
    # Create context from retrieved documents
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    if verbose:
        print(f"Documents: {len(results)}")
        print(f"Context length: {len(context)} chars")
    
    # Format prompt
    formatted_prompt = prompt_template.format(query=query, context=context)
    if verbose:
        print(f"Prompt length: {len(formatted_prompt)} chars")
        print("Generating...")
    
    # Generate response
    response = llm.invoke(formatted_prompt)
    total_time = time.time() - start_time
    
    # Extract message content from response
    if hasattr(response, 'content'):
        response_text = response.content
    else:
        response_text = str(response)
        
    if verbose:
        print(f"Done in {total_time:.2f}s")
        print("-" * 20)
    
    return response_text.strip(), total_time