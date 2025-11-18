# test_protocol_lms_agent.py
from datetime import datetime
from pathlib import Path
import sys
from typing import List, Callable, Optional

from llm_utils.factory_protocol import LLMFactory
from llm_utils.tools.tools_manager import ToolManager


# -----------------------------
# Define tools
# -----------------------------
def get_current_time():
    """Return the current time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load LMStudio plain from config.yaml
factory = LLMFactory()
llm = factory.create_from_yaml(Path("configs/config_lms.yaml"), agentic=True)

tool_manager = ToolManager(tools=[get_current_time])
llm.tool_manager = tool_manager

print(f"Using backend: {llm.backend_name}")


# -----------------------------
# Example messages
# -----------------------------
messages = [
    {"role": "system", "content": "You are a helpful assistant that can use tools."},
    {"role": "user", "content": "Hello! Can you tell me the current time?"}
]

# -----------------------------
# Run agentic chat with tool support
# -----------------------------
if hasattr(llm, "invoke"):
    reply = llm.invoke(messages, tools=tool_manager.tools)
    print("Final reply:", reply)
else:
    print("LLM does not support 'invoke' method.")
