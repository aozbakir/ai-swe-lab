from typing import Dict, Literal, Optional, Union
from pydantic import BaseModel, Field


class SentenceTransformersConfig(BaseModel):
    """Configuration for SentenceTransformers models"""
    name: Literal["sentence_transformers"]
    model_name: str = "all-MiniLM-L6-v2"
    device: Literal["cpu", "cuda"] = "cpu"
    normalize_embeddings: bool = True
    cache_dir: Optional[str] = None


class OpenAIEmbeddingConfig(BaseModel):
    """Configuration for OpenAI embedding models"""
    name: Literal["openai"]
    model_name: str = "text-embedding-3-small"
    base_url: Optional[str] = None


class EmbeddingConfig(BaseModel):
    """Configuration for embedding models"""
    default_embedding: str = Field(
        default="sentence_transformers",
        description="Default embedding model to use"
    )
    embeddings: Dict[str, Union[SentenceTransformersConfig, OpenAIEmbeddingConfig]] = Field(
        default_factory=lambda: {
            "sentence_transformers": SentenceTransformersConfig(name="sentence_transformers")
        },
        description="Dictionary of available embedding models"
    )
    
    def get_active_config(self) -> Union[SentenceTransformersConfig, OpenAIEmbeddingConfig]:
        """Get the configuration for the default embedding model"""
        if self.default_embedding not in self.embeddings:
            raise ValueError(f"Default embedding model {self.default_embedding} not found in config")
        return self.embeddings[self.default_embedding]