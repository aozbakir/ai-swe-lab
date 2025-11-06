from functools import wraps
import logging
from datetime import datetime

from .ansi import GREEN, RESET

def trace_tool(tool_fn):
    @wraps(tool_fn)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"[{timestamp}] TOOL: {tool_fn.__name__} called with args: {args}, kwargs: {kwargs}"

        logging.info(f"{GREEN}[TOOL CALL] {tool_fn.__name__} called with args: {args}, kwargs: {kwargs}{RESET}")

        # Also log to chat history file
        with open("chat_history.log", "a", encoding="utf-8") as f:
            f.write(message + "\n")
        return tool_fn(*args, **kwargs)
    return wrapper