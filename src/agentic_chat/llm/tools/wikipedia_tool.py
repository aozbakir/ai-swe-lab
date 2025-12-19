"""Wikipedia tool wrapper for MCP integration."""
from llm.tools.decorators import tool, trace_tool
from domain.wikipedia_logic import WikipediaLogic

wikipedia_logic = WikipediaLogic()

@tool(
    schema={
        "type": "function",
        "function": {
            "name": "wiki_search",
            "description": "Search Wikipedia for information about a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The topic to search for on Wikipedia"
                    }
                },
                "required": ["query"]
            }
        }
    },
)
@trace_tool
def wiki_search(query: str):
    """Tool wrapper to search Wikipedia content."""
    return wikipedia_logic.search_content(query=query)