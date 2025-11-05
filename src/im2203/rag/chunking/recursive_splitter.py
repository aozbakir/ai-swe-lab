from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter as LCRecursiveSplitter

from .base_chunker import BaseChunker

class RecursiveTextSplitter(BaseChunker):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, separators: list[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def chunk(self, documents: List[Document]) -> List[Document]:
        splitter = LCRecursiveSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators
        )
        return splitter.split_documents(documents)
