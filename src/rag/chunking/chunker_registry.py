import logging

from .character_splitter import CharacterTextSplitter
from .recursive_splitter import RecursiveTextSplitter

CHUNKER_REGISTRY = {
    "character": CharacterTextSplitter,
    "recursive": RecursiveTextSplitter
}

def get_chunker(strategy: str, **kwargs):
    strategy_key = strategy.lower()
    chunker_cls = CHUNKER_REGISTRY.get(strategy_key)

    if not chunker_cls:
        available = ", ".join(CHUNKER_REGISTRY.keys())
        logging.error(f"Unknown chunking strategy requested: {strategy}. Available: {available}")
        raise ValueError(f"Unknown chunking strategy '{strategy}'. Available: {available}")
    
    logging.info(f"Instantiating chunking for strategy: {strategy}")
    return chunker_cls(**kwargs)