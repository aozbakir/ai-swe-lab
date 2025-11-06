import logging

def setup_logging(level=logging.INFO, fmt='%(asctime)s - %(levelname)s - %(message)s'):
    """Configure global logging settings."""
    logging.basicConfig(level=level, format=fmt)

def get_logger(name=None):
    """Get a logger instance with the given name."""
    return logging.getLogger(name)