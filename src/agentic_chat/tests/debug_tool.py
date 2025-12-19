# debug_tool.py
# filepath: d:\Repos2\im2203\src\agentic_chat\debug_tool.py
"""Debug the tool execution issue."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm.tools.registry import tool_registry
from llm import tools

print("=== TOOL REGISTRY DEBUG ===")
print(f"tool_registry.tools type: {type(tool_registry.tools)}")
print(f"tool_registry.tools: {tool_registry.tools}")

print(f"\ntool_registry.schemas type: {type(tool_registry.schemas)}")
print(f"Number of schemas: {len(tool_registry.schemas) if hasattr(tool_registry.schemas, '__len__') else 'N/A'}")

# Try to access tools differently
if hasattr(tool_registry, 'tools'):
    if isinstance(tool_registry.tools, dict):
        print(f"Tools (dict): {list(tool_registry.tools.keys())}")
    elif isinstance(tool_registry.tools, list):
        print(f"Tools (list): {tool_registry.tools}")
        # Try to find function names in the list
        for i, tool in enumerate(tool_registry.tools):
            print(f"Tool {i}: {tool} (type: {type(tool)})")
            if hasattr(tool, '__name__'):
                print(f"  Function name: {tool.__name__}")

print("\n=== SCHEMA CHECK ===")
if hasattr(tool_registry, 'schemas'):
    for i, schema in enumerate(tool_registry.schemas):
        print(f"Schema {i}: {schema}")

print("\n=== REGISTRY METHODS ===")
print(f"Registry methods: {dir(tool_registry)}")