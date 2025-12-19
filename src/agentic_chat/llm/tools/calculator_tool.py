"""Calculator tool wrapper for MCP integration."""
from llm.tools.decorators import tool, trace_tool
from domain.calculator_logic import add_numbers

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two integers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "First number to add"
                    },
                    "b": {
                        "type": "integer",
                        "description": "Second number to add"
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
)
@trace_tool
def add(a: int, b: int):
    """Tool wrapper to add two numbers."""
    return add_numbers(a=a, b=b)