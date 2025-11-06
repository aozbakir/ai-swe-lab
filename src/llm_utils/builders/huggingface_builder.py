from typing import Any, Dict, Optional
from pathlib import Path
from langchain_core.language_models import BaseChatModel
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch

from .base import LLMBuilder


class HuggingFaceBuilder(LLMBuilder):
    """Builder for HuggingFace transformer models with LangChain integration"""
    
    def build(
        self,
        model_name: str,
        temperature: float = 0.7,
        quantize_4bit: bool = False,
        max_new_tokens: int = 500,
        top_k: int = 50,
        top_p: float = 0.95,
        **kwargs
    ) -> HuggingFacePipeline:
        """Build a HuggingFace LLM instance.
        
        Args:
            model_name: HuggingFace model identifier (e.g., "mistralai/Mistral-7B-Instruct-v0.3")
            temperature: Sampling temperature
            quantize_4bit: Whether to use 4-bit quantization
            max_new_tokens: Maximum tokens to generate
            top_k: Top-k sampling parameter
            top_p: Top-p (nucleus) sampling parameter
            **kwargs: Additional arguments
            
        Returns:
            HuggingFacePipeline instance wrapped for LangChain
        """
        # Try to find model in local cache first
        cache_base = Path("D:/huggingface_cache/hub")
        model_cache_name = model_name.replace("/", "--")
        local_model_path = cache_base / f"models--{model_cache_name}"
        
        # Check if we have snapshots folder
        snapshots_path = local_model_path / "snapshots"
        if snapshots_path.exists():
            # Get the latest snapshot (first subdirectory)
            snapshot_dirs = list(snapshots_path.iterdir())
            if snapshot_dirs:
                model_path = str(snapshot_dirs[0])
                print(f"Loading from local cache: {model_path}")
                use_local = True
            else:
                model_path = model_name
                use_local = False
        else:
            model_path = model_name
            use_local = False

        # Setup quantization config if needed
        if quantize_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=bnb_config,
                local_files_only=use_local
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                local_files_only=use_local
            )
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=use_local
        )
        
        # Create transformers pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,
        )
        
        # Wrap in LangChain's HuggingFacePipeline
        return HuggingFacePipeline(pipeline=pipe)