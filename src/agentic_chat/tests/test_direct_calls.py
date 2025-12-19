# test_direct_calls.py
# filepath: d:\Repos2\im2203\src\agentic_chat\test_direct_calls.py
"""Test direct tool calls."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm.tools.registry import tool_registry
from llm import tools

print("=== DIRECT TOOL CALLS ===")

# Get the tools
tools_list = tool_registry.tools

# Test each tool
for tool_func in tools_list:
    tool_name = tool_func.__name__
    print(f"\n--- Testing {tool_name} ---")
    
    try:
        if tool_name == 'add':
            result = tool_func(a=5, b=3)
            print(f"✅ {tool_name}(a=5, b=3) = {result}")
            
        elif tool_name == 'wiki_search':
            result = tool_func(query="test")
            print(f"✅ {tool_name}(query='test') = {result[:50]}...")
            
        elif tool_name in ['time_now', 'echo_test']:
            result = tool_func()
            print(f"✅ {tool_name}() = '{result}'")
            
    except Exception as e:
        print(f"❌ {tool_name} error: {e}")
        import traceback
        traceback.print_exc()