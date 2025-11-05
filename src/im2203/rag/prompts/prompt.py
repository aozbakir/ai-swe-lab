from typing import List, Optional
import yaml
from pathlib import Path
from langchain_core.documents import Document


class PromptTemplate:
    """A flexible prompt template system for RAG applications"""
    
    DEFAULT_TEMPLATE = """
You are a helpful AI assistant. Use the provided context to answer questions accurately.

IMPORTANT INSTRUCTIONS:
1. Base your answers solely on the provided context
2. If the necessary information is not in the context, say "I don't find this information in the provided context"
3. Do not make assumptions or use external knowledge
4. Be precise and concise in your answers
5. When relevant, cite specific parts of the context to support your answer

Remember to stay focused on the information present in the context.

Context:
{context}

Question: {query}

Answer:"""

    def __init__(self, template: Optional[str] = None):
        """Initialize with optional custom template"""
        self.template = template if template is not None else self.DEFAULT_TEMPLATE

    @classmethod
    def from_config(cls, config_path: str) -> "PromptTemplate":
        """Load prompt template from main config file"""
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            prompts_config = config.get("prompts", {})
            default_prompt = prompts_config.get("default", "qa")
            template = prompts_config.get(default_prompt, {}).get("template")
            return cls(template=template)
    
    def format(self, query: str, context: str) -> str:
        """Format the prompt template with query and context"""
        return self.template.format(context=context, query=query)
