# test_mcp_sse_client.py
# filepath: d:\Repos2\im2203\src\agentic_chat\tests\test_mcp_sse_client.py
"""Test MCP server using SSE transport like in the notebook."""
import asyncio
from fastmcp import Client
from fastmcp.client.transports import SSETransport

def test_greeting(name: str) -> str:
    """Test the greeting tool via MCP server."""
    async def _fetch():
        # Connect over HTTP/SSE and call the tool
        async with Client(SSETransport("http://localhost:8001/sse")) as client:
            return await client.call_tool("greeting", arguments={"name": name})
    
    # Run the coroutine to completion and return its result
    result = asyncio.run(_fetch())
    return result[0].text

if __name__ == "__main__":
    try:
        print("🔍 Testing MCP SSE client...")
        result = test_greeting("Arthur")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()