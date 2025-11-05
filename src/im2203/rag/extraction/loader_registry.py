import os
from .pypdf_loader import PyPdfLoader
from .pdfplumber_loader import PdfPlumberLoader
import logging

LOADER_REGISTRY = {
    "pypdf": PyPdfLoader,
    "pdfplumber": PdfPlumberLoader
}

def get_loader(strategy: str, **kwargs):
    loader_cls = LOADER_REGISTRY.get(strategy.lower())

    if not loader_cls:
        available = ", ".join(LOADER_REGISTRY.keys())
        logging.error(f"Unknown loader strategy requested: {strategy}. Available: {available}")
        raise ValueError(f"Unknown loader strategy '{strategy}'. Available: {available}")
    
    logging.info(f"Instantiating loader for strategy: {strategy}")
    return loader_cls(**kwargs)