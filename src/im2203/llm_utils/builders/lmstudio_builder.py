import requests
from langchain_openai import ChatOpenAI

from .base import LLMBuilder

class LMStudioBuilder(LLMBuilder):
    """Strategy for building LM Studio LLMs"""
    
    def build(self, model_name: str, base_url: str, **kwargs) -> ChatOpenAI:
        """Build a LangChain compatible LM Studio instance with error handling"""
        
        # Check if LM Studio is running by testing the connection
        try:
            test_url = base_url + "/models"
            print(f"Testing connection to {test_url}")
            test_response = requests.get(test_url, timeout=5)
            if test_response.status_code != 200:
                raise ConnectionError(f"LM Studio server returned non-200 status: {test_response.status_code}")
                
            # Try to parse the response to see if it's valid JSON
            models = test_response.json()
            print(f"✅ LM Studio connection successful! Available models: {[m.get('id') for m in models.get('data', [])]}")
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Cannot connect to LM Studio at {base_url}: {str(e)}")
        
        # Create the LLM instance if connection was successful
        return ChatOpenAI(
            model_name=model_name,
            openai_api_base=base_url,
            openai_api_key="not-needed",
            **kwargs
        )
    
    