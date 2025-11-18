# src/api/endpoints/chat_endpoint.py
from fastapi import APIRouter, Depends, Request
from pathlib import Path

from ..models.chat import ChatRequest, ChatResponse
from ..services.chat_service import ChatService

router = APIRouter(tags=["chat"])

def get_chat_service(request: Request) -> ChatService:
    # Initialize ChatService with default config and optional LLM
    return ChatService(
        llm=getattr(request.app.state, "llm", None),
        config_path=Path("src/core/configs/config.yaml")
    )

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask a question to the RAG chat assistant",
    description="Processes a natural-language question and returns an LLM-generated answer using document retrieval."
)
def chat(
    req: ChatRequest,
    service: ChatService = Depends(get_chat_service)
):
    # Directly pass the message; no session_id
    reply = service.process_message(req.message)
    return ChatResponse(**reply)
