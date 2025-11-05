from im2203.rag.core.components import BaseComponent
from im2203.rag.schemas.rag_config import RAGConfig

class PromptTemplate(BaseComponent):
    DEFAULT_TEMPLATE = """
You are a helpful AI assistant. Use the provided context to answer questions accurately.

IMPORTANT INSTRUCTIONS:
1. Base your answers solely on the provided context
2. If the necessary information is not in the context, say "I don't find this information in the provided context"
3. Do not make assumptions or use external knowledge
4. Be precise and concise in your answers
5. When relevant, cite specific parts of the context to support your answer

Context:
{context}

Question: {query}

Answer:"""

    def __init__(self, rag_config: RAGConfig):
        super().__init__(rag_config, "prompts")
        cfg_dict = self.config.model_dump() if hasattr(self.config, "model_dump") else self.config

        default_prompt_name = cfg_dict.get("default", "qa")
        self.template: str = cfg_dict.get(default_prompt_name, {}).get("template", self.DEFAULT_TEMPLATE)

    def format(self, query: str, context: str) -> str:
        return self.template.format(context=context, query=query)
