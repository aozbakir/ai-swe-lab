import os

from fastmcp import FastMCP
import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='im2203-wiki-tool/1.0 (educational-project)'
)

mcp = FastMCP(name="MyAssistantServer")

@mcp.tool
def wiki_search(query: str) -> str:
    """Search Wikipedia for information about a topic.
    Args:
        query: The topic to search for
    Returns:
        String containing the summary of the Wikipedia page
    """
    try:
        page = wiki.page(query)
        if page.exists():
            return page.summary or "No summary available"
        return f"Page '{query}' not found on Wikipedia"
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def greeting(name: str) -> str:
    """Return a greeting message."""
    return f"We are the knights who say 'Ni!' to {name}!"

@mcp.tool
def foo(a: int, b: int) -> float:
    """Return the ratio of the difference to the sum of two integers (i.e., (a - b) / (a + b)) using the MCP server."""
    if a + b == 0:
        return 0.0
    return (a - b) / (a + b)

@mcp.resource("quote://{id}")
def quote(id: str) -> str:
    """Return a quote based on ID."""
    quotes = {
        "1": "Always look on the bright side of life.",
        "2": "This parrot is no more!",
    }
    return quotes.get(id, "Ni! Ni! Ni!")


if __name__ == "__main__":
    # Start MCP server with SSE transport on port 8000
    mcp.run(
        transport="http", 
        host="127.0.0.1",
        port=8000
    )
