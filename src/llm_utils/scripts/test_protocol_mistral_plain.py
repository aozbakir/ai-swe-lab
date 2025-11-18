# test_protocol_lms_agent.py
from pathlib import Path

from llm_utils.factory_protocol import LLMFactory


# Load LMStudio plain from config.yaml
factory = LLMFactory()
llm = factory.create_from_yaml(Path("configs/config_mistral.yaml"), agentic=False)

# -----------------------------
# Example messages
# -----------------------------
messages = [
    {"role": "user", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello from Paris."}
]

if hasattr(llm, "generate"):
    prompt = messages[-1]["content"]
    reply = llm.generate(prompt)
    print("LLM reply:", reply)
else:
    print("LLM does not support 'generate' method.")
