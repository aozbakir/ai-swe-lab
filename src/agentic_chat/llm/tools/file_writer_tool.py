# llm/tools/file_writer_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\file_writer_tool.py
"""File writer tool wrapper."""
from .decorators import tool, trace_tool
from domain.file_writer_logic import print_out

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file. Creates the file if it doesn't exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to write to the file"
                    },
                    "filename": {
                        "type": "string", 
                        "description": "The name of the file to write to"
                    }
                },
                "required": ["text", "filename"]
            }
        }
    },
)
@trace_tool
def write_file(text: str, filename: str, **kwargs) -> str:
    """Write text to a file."""
    return print_out(text, filename)