from pathlib import Path

from im2203.rag.extraction.document_loader import DocumentLoader
from im2203.rag.chunking.document_chunker import DocumentChunker


def main():
    # Load configuration
    ing = DocumentLoader(Path("../configs/config_v2.yaml").resolve())
    chk = DocumentChunker(Path("../configs/config_v2.yaml").resolve())

    # Access input file instead of input_dir
    print(f"Input file: {ing.input_file}")

    # Access model names from config
    print(f"LLM model: {ing.config.llm.openai.model_name}")
    print(f"Embeddings model: {ing.config.embeddings.sentence_transformers.model_name}")

    # Load documents
    documents = ing.load()
    print(f"Loaded {len(documents)} documents")

    # Chunk documents
    chunked_documents = chk.chunk(documents)
    print(f"Chunked {len(chunked_documents)} documents")


if __name__ == "__main__":
    main()