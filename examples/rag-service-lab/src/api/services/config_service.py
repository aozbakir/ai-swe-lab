import yaml
from core.configs.settings import Settings

settings = Settings()

class ConfigService:
    """API-facing wrapper for config parameters."""

    def __init__(self, config_path=None):
        self.config_path = config_path or settings.LLM_CONFIG_PATH
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.yaml_config = yaml.safe_load(f)

    def get_config_params(self):
        """
        Return relevant config parameters for UI, mirroring YAML structure.
        """
        config = self.yaml_config

        # Extraction
        extraction_default = config.get("extraction", {}).get("default", "")
        extraction_params = config.get("extraction", {}).get(extraction_default, {})

        # Chunking
        chunking_default = config.get("chunking", {}).get("default", "")
        chunking_params = config.get("chunking", {}).get("chunkers", {}).get(chunking_default, {})

        # LLM
        llm_default = config.get("llm", {}).get("default", "")
        llm_info = config.get("llm", {}).get(llm_default, {})
        llm_name = llm_info.get("name", llm_default)
        llm_model = llm_info.get("model_name", "")

        # Embeddings
        embedding_default = config.get("embeddings", {}).get("default", "")
        embedding_info = config.get("embeddings", {}).get(embedding_default, {})
        embedding_model = embedding_info.get("model_name", "")

        # Retrieval
        retrieval_default = config.get("retrieval", {}).get("default", "")
        retrieval_info = config.get("retrieval", {}).get(retrieval_default, {})
        retrieval_type = retrieval_info.get("type", "")
        similarity_metric = retrieval_info.get("similarity_metric", "")
        top_k = retrieval_info.get("top_k", "")
        search_kwargs = retrieval_info.get("search_kwargs", {})

        return {
            "extraction": {
                "default": extraction_default,
                extraction_default: extraction_params
            },
            "chunking": {
                "default": chunking_default,
                chunking_default: chunking_params
            },
            "llm": {
                "default": llm_default,
                llm_default: {
                    "name": llm_name,
                    "model_name": llm_model
                }
            },
            "embeddings": {
                "default": embedding_default,
                embedding_default: {
                    "model_name": embedding_model
                }
            },
            "retrieval": {
                "default": retrieval_default,
                retrieval_default: {
                    "type": retrieval_type,
                    "similarity_metric": similarity_metric,
                    "top_k": top_k,
                    "search_kwargs": search_kwargs
                }
            }
        }