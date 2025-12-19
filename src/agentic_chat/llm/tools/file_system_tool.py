# llm/tools/file_writer_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\file_writer_tool.py
"""File writer tool wrapper."""
from .decorators import tool, trace_tool
from domain.file_system_logic import list_files

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the current directory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
)
@trace_tool
def list_files_tool(**kwargs) -> str:
    """Tool wrapper to list files in the current directory."""
    return list_files(**kwargs)