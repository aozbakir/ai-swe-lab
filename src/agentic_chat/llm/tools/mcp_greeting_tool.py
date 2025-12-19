# llm/tools/mcp_greeting_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\mcp_greeting_tool.py
"""MCP greeting tool wrapper."""
import asyncio
from .decorators import tool, trace_tool
from fastmcp import Client
from fastmcp.client.transports import SSETransport

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "greeting",
            "description": "Get a greeting message from the MCP server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet"
                    }
                },
                "required": ["name"]
            }
        }
    },
)
@trace_tool
def greeting(name: str) -> str:
    """Get a greeting message via MCP server."""
    async def _fetch():
        # Connect to your MCP server
        async with Client(SSETransport("http://localhost:8001/sse")) as client:
            return await client.call_tool("greeting", arguments={"name": name})
    
    try:
        # Run the async call and return the result
        result = asyncio.run(_fetch())
        return result[0].text
    except Exception as e:
        return f"Error calling MCP greeting tool: {e}"