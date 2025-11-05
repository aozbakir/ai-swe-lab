from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import yaml

# --------------------------------------------------
# PATHS
# --------------------------------------------------
class PathsConfig(BaseModel):
    input_file: str
    output_vectorstore_dir: str


# --------------------------------------------------
# EXTRACTION
# --------------------------------------------------

class ExtractionConfig(BaseModel):
    default: str = "TextLoader"
    loaders: Optional[Dict[str, Dict[str, Any]]] = Field(default_factory=dict)


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

class ChunkingConfig(BaseModel):
    default: str = "character"
    chunkers: Dict[str, Dict[str, Any]] = {}


# --------------------------------------------------
# LLMs
# --------------------------------------------------
class OpenAIConfig(BaseModel):
    name: str = "openai"
    model_name: str
    base_url: Optional[str] = None
    temperature: float = 0.0

class LMStudioConfig(BaseModel):
    name: str = "lmstudio"
    model_name: str
    base_url: str
    temperature: float = 0.0
    max_tokens: int = 512
    top_p: float = 0.1
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    request_timeout: int = 120

class HuggingFaceConfig(BaseModel):
    name: str = "huggingface"
    model_name: str
    temperature: float = 0.3
    quantize_4bit: bool = False
    max_new_tokens: int = 500
    top_k: int = 50
    top_p: float = 0.95

class LLMConfig(BaseModel):
    default: str = "openai"
    openai: OpenAIConfig
    lmstudio: Optional[LMStudioConfig] = None
    huggingface: Optional[HuggingFaceConfig] = None


# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------
class SentenceTransformersConfig(BaseModel):
    name: str = "sentence_transformers"
    model_name: str
    device: str = "cpu"
    normalize_embeddings: bool = True
    cache_dir: Optional[str] = None

class OpenAIEmbeddingConfig(BaseModel):
    name: str = "openai"
    model_name: str
    base_url: Optional[str] = None

class EmbeddingsConfig(BaseModel):
    default: str = "sentence_transformers"
    sentence_transformers: SentenceTransformersConfig
    openai: Optional[OpenAIEmbeddingConfig] = None


# --------------------------------------------------
# VECTORSTORE & RETRIEVAL
# --------------------------------------------------
class FAISSConfig(BaseModel):
    index_path: str

class VectorstoreConfig(BaseModel):
    default: str = "faiss"
    faiss: FAISSConfig

class RetrievalConfig(BaseModel):
    default: str = "vectorstore"
    type: str = "FAISS"
    similarity_metric: str = "cosine"
    top_k: int = 5
    search_kwargs: Optional[Dict[str, Optional[Union[str, float]]]] = None


# --------------------------------------------------
# GENERATION
# --------------------------------------------------
class GenerationBackendConfig(BaseModel):
    model_ref: str
    prompt_template: str = "default"
    max_tokens: int = 500
    temperature: float = 0.2

class GenerationConfig(BaseModel):
    default: str = "openai"
    openai: GenerationBackendConfig


# --------------------------------------------------
# PROMPTS
# --------------------------------------------------
class PromptTemplateConfig(BaseModel):
    template: str

class PromptsConfig(BaseModel):
    default: str = "qa"
    qa: PromptTemplateConfig



# --------------------------------------------------
# ROOT CONFIG
# --------------------------------------------------
class RAGConfig(BaseModel):
    paths: PathsConfig
    extraction: ExtractionConfig
    chunking: ChunkingConfig
    llm: LLMConfig
    embeddings: EmbeddingsConfig
    vectorstore: VectorstoreConfig
    retrieval: RetrievalConfig
    generation: GenerationConfig
    prompts: PromptsConfig

    @classmethod
    def from_yaml(cls, path: str) -> "RAGConfig":
        """Load RAGConfig from a YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
