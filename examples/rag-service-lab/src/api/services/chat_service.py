# src/api/services/chat_service.py
from pathlib import Path
from typing import List, Dict, Union
from core.domain.chat_logic import ChatLogic

class ChatService:
    """
    API-facing wrapper for RAG QA sessions.
    Keeps optional conversation history.
    """

    def __init__(
        self,
        config_path: Path = Path("src/core/configs/config.yaml"),
        llm=None,
        prompt: Union[str, None] = None,
        search_type: str = "mmr",
        top_k: int = None
    ):
        # Initialize ChatLogic
        self.logic = ChatLogic(
            config_path=config_path,
            llm=llm,
            prompt=prompt,
            search_type=search_type,
            top_k=top_k
        )

        # Optional conversation history
        self.history: List[Dict[str, str]] = []

    def process_message(self, message: str, return_docs: bool = False) -> Dict[str, Union[str, list]]:
        """
        Process a user message, optionally returning retrieved documents.
        """
        result = self.logic.answer(message)

        # Save chat history
        self.history.append({
            "user": message,
            "assistant": result["response"]
        })

        return {
            "response": result["response"],
            "retrieved_docs": [
                {
                    "page_content": doc.page_content,
                    "page": doc.metadata.get("page"),
                    "file_path": doc.metadata.get("file_path") or doc.metadata.get("source")
                }
                for doc in result["retrieved_docs"]
                if hasattr(doc, "page_content") and hasattr(doc, "metadata")
            ]
        }
