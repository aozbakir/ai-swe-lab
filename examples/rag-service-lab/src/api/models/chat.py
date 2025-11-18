"""Chat-related data models and schemas."""

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    """Chat request model containing user message."""
    message: str

class RetrievedDoc(BaseModel):
    page_content: str
    page: Optional[int]
    file_path: Optional[str]

class ChatResponse(BaseModel):
    response: str
    retrieved_docs: List[RetrievedDoc]