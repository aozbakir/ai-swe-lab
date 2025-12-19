# llm/tools/time_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\time_tool.py
"""Time tool wrapper for MCP integration."""
from .decorators import tool, trace_tool
from domain.time_logic import get_current_time

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "time_now",
            "description": "Get the current time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
)
@trace_tool
def time_now(**kwargs):
    """Return the current time as a string."""
    result = get_current_time(**kwargs)
    print(f"🔍 DEBUG: time_now returning to LLM: '{result}'")
    return result


