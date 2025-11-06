from typing import Dict, List, Optional, Union
from pathlib import Path
from uuid import uuid4
import yaml

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.utils import trim_messages
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.memory import MemorySaver


class ConversationManager:
    """Lightweight wrapper for LangGraph conversation with memory management"""
    
    def __init__(
        self,
        llm: BaseChatModel,
        config_path: Optional[Union[str, Path]] = None,
        verbose: bool = False,
        thread_id: str = "default"
    ):
        self.llm = llm
        self.verbose = verbose
        self.thread_id = thread_id
        
        # Default config
        self.config = {
            "max_tokens": 4,
            "strategy": "last",
            "start_on": "human",
            "end_on": ("human", "tool")
        }
        
        # Load from YAML if provided
        if config_path:
            self._load_config(config_path)
        
        # Build graph
        self.graph = self._build_graph()
        self.config_dict = {"configurable": {"thread_id": self.thread_id}}
    
    def _load_config(self, config_path: Union[str, Path]) -> None:
        """Load memory config from YAML"""
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
            memory_config = data.get('conversation', {}).get('memory', {})
            self.config.update(memory_config)
    
    def _build_graph(self):
        """Build the LangGraph conversation graph"""
        def call_model(state: MessagesState):
            messages = trim_messages(
                state["messages"],
                strategy=self.config["strategy"],
                token_counter=len,
                max_tokens=self.config["max_tokens"],
                start_on=self.config["start_on"],
                end_on=self.config["end_on"]
            )
            
            if self.verbose:
                print(f"🔍 Trimmed to {len(messages)} messages")
                for msg in messages:
                    print(f"  - {type(msg).__name__}: {msg.content}")
            
            response = self.llm.invoke(messages)
            return {"messages": [response]}
        
        builder = StateGraph(MessagesState)
        builder.add_node("call_model", call_model)
        builder.add_edge(START, "call_model")
        return builder.compile(checkpointer=MemorySaver())
    
    def chat(self, message: str) -> str:
        """Send message and get response"""
        response = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            self.config_dict
        )
        return response["messages"][-1].content
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        state = self.graph.get_state(self.config_dict)
        messages = []
        
        for msg in state.values.get("messages", []):
            if isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})
        
        return messages
    
    def reset(self) -> None:
        """Reset conversation by creating new thread"""
        self.thread_id = str(uuid4())
        self.config_dict = {"configurable": {"thread_id": self.thread_id}}
    
    @classmethod
    def from_yaml(cls, llm: BaseChatModel, config_path: Union[str, Path], 
                  verbose: bool = False, thread_id: str = "default"):
        """Create manager from YAML config"""
        return cls(llm, config_path, verbose, thread_id)
    
class RAGChat:
    def __init__(self, llm, retriever=None, prompt_constructor=None, k=3):
        """
        Chat interface for standard and RAG-augmented chat.
        Args:
            llm (LLM): Language model instance.
            retriever (Retriever): Retriever instance for RAG.
            prompt_constructor (PromptConstructor): PromptConstructor for RAG.
            k (int): Number of docs to retrieve for RAG.
            use_rag (bool): If True, use RAG; else, standard chat.
        """
        self.llm = llm
        self.retriever = retriever
        self.prompt_constructor = prompt_constructor
        self.k = k

    def chat(self, query):
            retrieved_docs, faiss_ids = self.retriever.retrieve_similar(query, k=self.k)
            rag_prompt = self.prompt_constructor.build_prompt(query, retrieved_docs)
            response = self.llm.chat(rag_prompt)
            return response, faiss_ids