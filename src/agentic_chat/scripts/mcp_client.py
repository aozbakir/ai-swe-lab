import asyncio
from fastmcp import Client
from fastmcp.client.transports import SSETransport

MCP_URL = "http://127.0.0.1:8000/mcp/"

def get_client():
    return Client(MCP_URL)

async def call_tool(tool_name: str, arguments: dict):
    async with get_client() as client:
        return await client.call_tool(tool_name, arguments=arguments)

async def read_resource(uri: str):
    async with get_client() as client:
        return await client.read_resource(uri)
