from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter as LCCharacterTextSplitter

from .base_chunker import BaseChunker

class CharacterTextSplitter(BaseChunker):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, separator: str = ""):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

    def chunk(self, documents: List[Document]) -> List[Document]:
        splitter = LCCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separator=self.separator
        )
        return splitter.split_documents(documents)
