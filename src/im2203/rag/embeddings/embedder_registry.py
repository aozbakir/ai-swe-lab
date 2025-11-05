import logging
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings


EMBEDDER_REGISTRY = {
    "huggingface": HuggingFaceEmbeddings,
    "sentence_transformers": HuggingFaceEmbeddings,  # alias
    "openai": OpenAIEmbeddings,
}

def get_embedder(strategy: str, **kwargs):
    strategy_key = strategy.lower()
    embedder_cls = EMBEDDER_REGISTRY.get(strategy_key)

    if not embedder_cls:
        available = ", ".join(EMBEDDER_REGISTRY.keys())
        logging.error(f"Unknown embedding strategy requested: {strategy}. Available: {available}")
        raise ValueError(f"Unknown embedding strategy '{strategy}'. Available: {available}")

    logging.info(f"Instantiating embedder for strategy: {strategy} with kwargs: {kwargs}")
    return embedder_cls(**kwargs)
