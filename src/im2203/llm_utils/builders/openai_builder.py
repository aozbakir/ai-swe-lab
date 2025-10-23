import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .base import LLMBuilder

class OpenAILLMBuilder(LLMBuilder):
    """Strategy for building OpenAI LLMs"""
    
    def build(self, model_name: str, api_key: str = None, **kwargs) -> ChatOpenAI:
        """Build a LangChain OpenAI ChatModel instance"""
        # If no API key provided as argument, try to get from environment
        if api_key is None:
            # Force reload from .env file to ensure we have the latest
            api_key = self._get_api_key_from_env(force_reload=True)
            
            # If still no API key, raise error
            if not api_key:
                raise ValueError("OpenAI API key must be provided via argument or OPENAI_API_KEY env variable.")
            
            # Only show part of the key for security
            print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
        
        return ChatOpenAI(model=model_name, openai_api_key=api_key, **kwargs)
    
    def _get_api_key_from_env(self, force_reload=False):
        """Get the API key from environment variables, with option to force reload from .env"""
        # If forcing reload or no key exists, try loading from .env
        if force_reload or not os.environ.get("OPENAI_API_KEY"):
            # Use absolute path
            ROOT_DIR = Path("D:\Repos2")  # Using forward slashes for Path compatibility
            dotenv_path = ROOT_DIR / '.env'
            print(dotenv_path)
            
            if dotenv_path.exists():
                print(f"Loading API key from: {dotenv_path.absolute()}")
                # Load and update the environment
                load_dotenv(dotenv_path=dotenv_path, override=True)
                
                # Directly access os.environ after reload to get fresh value
                if "OPENAI_API_KEY" in os.environ:
                    return os.environ["OPENAI_API_KEY"]
        
        # Return from environment (either pre-existing or newly loaded)
        return os.environ.get("OPENAI_API_KEY")
