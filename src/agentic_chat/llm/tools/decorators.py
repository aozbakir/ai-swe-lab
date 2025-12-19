# llm/tools/decorators.py
# filepath: d:\Repos2\im2203\src\agentic_chat\llm\tools\decorators.py
from datetime import datetime
from functools import wraps
from inspect import signature
from typing import Callable

from llm.tools.registry import tool_registry  # singleton instance


def trace_tool(tool_fn):
    """Decorator to trace tool calls."""
    @wraps(tool_fn)  # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Console logging
        print(f"[{timestamp}] TOOL {tool_fn.__name__} called with args={args}, kwargs={kwargs}")
        
        # File logging
        try:
            from utils.chat_logger import ChatLogger
            logger = ChatLogger()
            logger.log_tool_call(tool_fn.__name__, args, kwargs)
        except ImportError:
            pass  # Logger not available
        
        result = tool_fn(*args, **kwargs)
        return result
    
    #wrapper.__signature__ = signature(tool_fn)
    return wrapper


def tool(schema: dict):
    """Decorator to register a tool with its schema."""
    def wrapper(fn: Callable):
        tool_registry.register_tool(fn, schema)
        return fn
    return wrapper

def mcp_tool(fn: Callable):
    """Decorator to automatically register with MCP server."""
    # Import here to avoid circular imports
    from scripts.server import mcp
    
    # Apply @mcp.tool decorator
    return mcp.tool(fn)

def mcp_resource(uri_template: str):
    """Decorator to automatically register with MCP server as resource."""
    def wrapper(fn: Callable):
        # Import here to avoid circular imports  
        from scripts.server import mcp
        
        # Apply @mcp.resource decorator
        return mcp.resource(uri_template)(fn)
    return wrapper