# llm/tools/echo_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\echo_tool.py
"""Echo tool wrapper for testing."""
from .decorators import tool, trace_tool
from domain.echo_logic import echo_hello

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "echo_test",
            "description": "Returns a hello message exactly as provided by the tool.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
)
@trace_tool
def echo_test(**kwargs):
    """Tool wrapper to echo a test message."""
    result = echo_hello(**kwargs)
    print(f"🔍 DEBUG: echo_test returning to LLM: '{result}'")
    return result