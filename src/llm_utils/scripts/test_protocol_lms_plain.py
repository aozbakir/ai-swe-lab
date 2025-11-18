from pathlib import Path
from llm_utils.factory_protocol import LLMFactory

factory = LLMFactory()

# Load LMStudio plain from config.yaml
llm = factory.create_from_yaml(Path("configs/config_lms.yaml"), agentic=False)

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
