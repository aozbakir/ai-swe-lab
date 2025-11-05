from pathlib import Path
from typing import List, Union
import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from .base_loader import BaseLoader

class PyPdfLoader(BaseLoader):
    def __init__(self, input_file: Union[str, Path]):
        self.input_file = Path(input_file)

    def load(self) -> List[Document]:
        try:
            logging.info(f"Loading PDF from file: {self.input_file}")
            loader = PyPDFLoader(str(self.input_file))
            documents = loader.load()
            logging.info(f"Loaded {len(documents)} pages from {self.input_file.name}")

            if not documents:
                logging.warning(f"No content found in PDF: {self.input_file}")

            return documents
        except Exception as e:
            logging.error(f"Failed to load documents from {self.input_file}: {e}")
            return []