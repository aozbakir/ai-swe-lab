from pathlib import Path
from llm_utils.factory_protocol import LLMFactory

factory = LLMFactory()

import sys
sys.path.append(r"D:/Repos2/mas4te/fastapi_app/backup/fastapi_app/dependencies")

# Import OpenAIAuthenticator from auth.py
from auth import OpenAIAuthenticator

# Load OpenAI API key
auth = OpenAIAuthenticator()
api_key = auth.api_key

# Load LMStudio plain from config.yaml
llm = factory.create_from_yaml(Path("configs/config_openai.yaml"), agentic=False)

print(f"Using backend: {llm.name()}")

# Example message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello from Paris."}
]


# For plain backend, use the standard generate method
if hasattr(llm, "generate"):
    prompt = messages[-1]["content"]  # Use only the user's message
    reply = llm.generate(prompt)
    print("LLM reply:", reply)
else:
    print("LLM does not support 'generate' method.")
