import logging
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Default model for HuggingFace embeddings
DEFAULT_HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

EMBEDDER_REGISTRY = {
    "huggingface": HuggingFaceEmbeddings,
    "sentence_transformers": HuggingFaceEmbeddings,  # alias
    "openai": OpenAIEmbeddings,
}

def get_embedder(strategy: str, **kwargs):
    """Get an embedder instance based on the specified strategy.
    
    Args:
        strategy: The embedding strategy to use (huggingface, sentence_transformers, openai)
        **kwargs: Additional arguments to pass to the embedder constructor
        
    Returns:
        An instance of the requested embedder
        
    Raises:
        ValueError: If the strategy is not recognized
    """
    strategy_key = strategy.lower()
    embedder_cls = EMBEDDER_REGISTRY.get(strategy_key)

    if not embedder_cls:
        available = ", ".join(EMBEDDER_REGISTRY.keys())
        logging.error(f"Unknown embedding strategy requested: {strategy}. Available: {available}")
        raise ValueError(f"Unknown embedding strategy '{strategy}'. Available: {available}")

    # Set default model name for HuggingFace embeddings if not provided
    if embedder_cls == HuggingFaceEmbeddings and "model_name" not in kwargs:
        kwargs["model_name"] = DEFAULT_HF_MODEL
        logging.info(f"Using default model: {DEFAULT_HF_MODEL}")

    logging.info(f"Instantiating embedder for strategy: {strategy} with kwargs: {kwargs}")
    return embedder_cls(**kwargs)
