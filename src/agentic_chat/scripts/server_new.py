"""
New MCP server using domain logic and tool decorators
"""
import sys
import os
from fastmcp import FastMCP

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.tools.decorators import trace_tool

mcp = FastMCP(name="MyAssistantServer")

@mcp.tool
@trace_tool
def greeting(name: str) -> str:
    """Return a greeting message."""
    return f"We are the knights who say 'Ni!' to {name}!"


if __name__ == "__main__":
    # Start MCP server with SSE transport on port 8000
    mcp.run(
        transport="sse", 
        host="127.0.0.1",
        port=8001
    )