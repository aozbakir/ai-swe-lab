import argparse
from pathlib import Path

from im2203.rag.configs.rag_config_loader import RAGConfigLoader
from im2203.rag.extraction.document_loader import DocumentLoader
from im2203.rag.chunking.document_chunker import DocumentChunker
from im2203.rag.embeddings.document_embedder import DocumentEmbedder
from im2203.rag.embeddings.document_vectorstore import DocumentVectorStore

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Document ingestion pipeline for RAG system'
    )
    parser.add_argument(
        '--config', 
        type=Path,
        required=True,
        help='Path to configuration YAML file'
    )
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    config_path = args.config.resolve()
    
    # Load configuration
    print(f"Loading configuration from: {config_path}")
    rag_config_loader = RAGConfigLoader(config_path)
    rag_config = rag_config_loader.config

    # Initialize components
    print("\nInitializing RAG components...")
    ing = DocumentLoader(rag_config)
    chk = DocumentChunker(rag_config)
    emb = DocumentEmbedder(rag_config)
    vectorstore = DocumentVectorStore(
        embedder=emb.embedder, 
        config=rag_config.model_dump()
    )

    # Load documents
    print("\nLoading documents...")
    documents = ing.load()
    print(f"Loaded {len(documents)} documents")

    # Check for empty documents
    empty_docs = [doc for doc in documents if not doc.page_content.strip()]
    if empty_docs:
        print(f"Warning: Found {len(empty_docs)} empty documents")

    # Chunk documents
    print("\nChunking documents...")
    chunked_documents = chk.chunk(documents)
    print(f"Created {len(chunked_documents)} chunks")

    # Create and save vector store
    print("\nCreating vector store...")
    vectorstore.create(chunked_documents)
    print("Vector store created successfully")

    # Load vector store to verify
    print("\nVerifying vector store...")
    vs = vectorstore.load()
    print("Vector store loaded and verified successfully")

    print("\nIngestion pipeline completed successfully!")

if __name__ == "__main__":
    main()