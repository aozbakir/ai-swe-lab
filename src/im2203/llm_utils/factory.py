from typing import Dict, Any
from pathlib import Path
import yaml
from langchain_core.language_models import BaseChatModel

from .builders.base import LLMBuilder
from .builders.openai_builder import OpenAILLMBuilder
from .builders.lmstudio_builder import LMStudioBuilder
from .builders.huggingface_builder import HuggingFaceBuilder


class LLMFactory:
    """Factory class for creating LLM instances based on configuration.
    
    Uses auto-registration to avoid modifying the factory when adding new builders.
    """
    
    # Class-level registry - builders auto-register themselves
    _builders: Dict[str, LLMBuilder] = {}
    
    @classmethod
    def register_builder(cls, name: str, builder: LLMBuilder) -> None:
        """Register a builder strategy.
        
        Args:
            name: Builder identifier (e.g., "openai", "lmstudio")
            builder: Builder instance
        """
        cls._builders[name] = builder
    
    @classmethod
    def get_builder(cls, name: str) -> LLMBuilder:
        """Get a builder by name.
        
        Args:
            name: Builder identifier
            
        Returns:
            Builder instance
            
        Raises:
            ValueError: If builder not found
        """
        builder = cls._builders.get(name)
        if not builder:
            valid_names = list(cls._builders.keys())
            raise ValueError(
                f"Unknown builder '{name}'. Valid options: {valid_names}"
            )
        return builder
    
    def create_from_yaml_file(self, config_path: Path) -> BaseChatModel:
        """Create an LLM instance from a YAML configuration file.
        
        Args:
            config_path: Path to YAML config file
            
        Returns:
            Configured LLM instance
        """
        config = self._load_config(config_path)
        default_model = config.get('default_model', 'lmstudio')
        model_config = config['models'][default_model]
        
        builder_name = model_config.get('name')
        builder = self.get_builder(builder_name)
        
        return builder.build(**model_config)
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load and validate YAML configuration."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'models' not in config:
            raise ValueError("Config must contain 'models' section")
        
        return config
    
LLMFactory.register_builder("openai", OpenAILLMBuilder())
LLMFactory.register_builder("lmstudio", LMStudioBuilder())
LLMFactory.register_builder("huggingface", HuggingFaceBuilder())