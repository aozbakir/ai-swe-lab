import argparse
import textwrap
from pathlib import Path
from time import time

from llm_utils.factory import LLMFactory
from rag.configs.rag_config_loader import RAGConfigLoader
from rag.embeddings.document_vectorstore import DocumentVectorStore
from rag.embeddings.document_embedder import DocumentEmbedder
from rag.prompts.prompt import PromptTemplate
from rag.retrieval.qa_retriever import QARetriever
from rag.retrieval.vector_retriever import VectorRetriever

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Interactive RAG system for querying documents'
    )
    parser.add_argument(
        '--config', 
        type=Path,
        required=True,
        help='Path to configuration YAML file'
    )
    parser.add_argument(
        '--search-type',
        choices=['similarity', 'mmr'],
        default='mmr',
        help='Search strategy (default: mmr)'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        help='Number of documents to retrieve (default: 5)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=120,
        help='Timeout in seconds for LLM calls (default: 120)'
    )
    return parser.parse_args()

def print_separator(char="=", length=80):
    """Print a separator line."""
    print(f"\n{char * length}")

def initialize_rag_system(config_path, search_type, top_k):
    """Initialize RAG components."""
    print(f"Loading configuration from: {config_path}")
    rag_config_loader = RAGConfigLoader(config_path)
    rag_config = rag_config_loader.config

    # Initialize components
    embedder = DocumentEmbedder(rag_config).embedder
    vectorstore = DocumentVectorStore(
        embedder=embedder,
        config=rag_config.model_dump()
    )
    vs = vectorstore.load()  # Load existing vector store
    prompt_template = PromptTemplate(rag_config)

    # Initialize LLM
    llm_factory = LLMFactory()
    llm = llm_factory.create_from_yaml_file(config_path)

    # Initialize retriever with specified search type
    retriever_kwargs = {
        'vectorstore': vectorstore,
        'top_k': top_k,
        'search_type': search_type,
    }
    
    if search_type == 'mmr':
        retriever_kwargs.update({
            'fetch_k': 20,
            'lambda_mult': 0.7
        })

    retriever = VectorRetriever(**retriever_kwargs)

    return QARetriever(
        retriever=retriever,
        llm=llm,
        prompt_template=prompt_template
    )

def interactive_loop(qa_pipeline, timeout):
    """Run interactive query loop."""
    print("\nWelcome to the Interactive RAG System!")
    print("Type 'exit' or 'quit' to end the session")
    print("Type 'help' for command list")
    print_separator()

    while True:
        try:
            # Get user input
            query = input("\nEnter your question: ").strip()
            
            # Handle special commands
            if query.lower() in ['exit', 'quit']:
                print("\nThank you for using the RAG system!")
                break
            elif query.lower() == 'help':
                print("\nAvailable commands:")
                print("- exit/quit: End the session")
                print("- help: Show this help message")
                continue
            elif not query:
                print("Please enter a question!")
                continue

            # Process query
            print_separator("-")
            print(f"Processing query: {query}")
            print_separator("-")

            start_time = time()
            try:
                response_text, _ = qa_pipeline.run(query=query, verbose=True)
                total_time = time() - start_time

                print("\nRESPONSE:")
                print("-" * 40)
                wrapped_response = textwrap.fill(response_text.strip(), width=70)
                print(wrapped_response)
                print(f"\nTime taken: {total_time:.2f} seconds")
                print_separator()

            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                continue
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please try a different question")
                continue

        except KeyboardInterrupt:
            print("\nExiting...")
            break

def main():
    args = parse_args()
    
    try:
        # Initialize RAG system
        qa_pipeline = initialize_rag_system(
            args.config.resolve(),
            args.search_type,
            args.top_k
        )
        
        # Run interactive loop
        interactive_loop(qa_pipeline, args.timeout)

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())