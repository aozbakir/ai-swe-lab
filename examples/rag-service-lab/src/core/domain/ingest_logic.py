# core/domain/ingest_logic.py
from pathlib import Path
import logging
from typing import Optional

from rag.configs.rag_config_loader import RAGConfigLoader
from rag.extraction.document_loader import DocumentLoader
from rag.chunking.document_chunker import DocumentChunker
from rag.embeddings.document_embedder import DocumentEmbedder
from rag.embeddings.document_vectorstore import DocumentVectorStore

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def run_ingestion(config_path: Path, input_file: Optional[Path] = None) -> str:
    """
    Run the RAG document ingestion pipeline.

    Args:
        config_path: Path to the YAML configuration file.
        input_file: Optional PDF file to ingest (overrides config).

    Returns:
        str: Path to the created vector store.
    """
    config_path = config_path.resolve()
    logger.debug(f"Using config path: {config_path}")

    # Load configuration
    rag_config_loader = RAGConfigLoader(config_path)
    rag_config = rag_config_loader.config

    # Override input_file if provided
    if input_file is not None:
        rag_config.paths.input_file = str(input_file.resolve())
        logger.debug(f"Overriding input file with uploaded PDF: {rag_config.paths.input_file}")

    logger.debug(f"Loaded RAG config: {rag_config.model_dump()}")

    # Initialize components
    logger.debug("Initializing RAG components...")
    loader = DocumentLoader(rag_config)
    chunker = DocumentChunker(rag_config)
    embedder = DocumentEmbedder(rag_config)

    logger.debug(f"Embedder initialized: {embedder.embedder}")

    # Resolve vector store path (relative to current working dir)
    vs_path_str = rag_config.model_dump().get("paths", {}).get("output_vectorstore_dir", "vector.store")
    vs_path = Path(vs_path_str).resolve()
    vs_path.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    logger.debug(f"Vector store will be at: {vs_path}")

    # Initialize vector store
    vectorstore = DocumentVectorStore(
        embedder=embedder.embedder,
        config={"index_path": str(vs_path / "index.faiss")}
    )

    # Always create a new index when an upload occurs (no override lock)

    # Load documents
    logger.debug("Loading documents...")
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found to ingest.")

    empty_docs = [doc for doc in documents if not doc.page_content.strip()]
    if empty_docs:
        logger.warning(f"Found {len(empty_docs)} empty documents")

    # Chunk documents
    logger.debug("Chunking documents...")
    chunked_documents = chunker.chunk(documents)
    logger.debug(f"Created {len(chunked_documents)} chunks")

    # Create and save vector store
    logger.debug("Creating vector store...")
    vectorstore.create(chunked_documents, overwrite=True)
    logger.debug("Vector store created successfully")

    # Save vector store to disk
    logger.debug("Saving vector store...")
    vectorstore.save()
    logger.debug("Vector store saved successfully")

    return str(vs_path)
