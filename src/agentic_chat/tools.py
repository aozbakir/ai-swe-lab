"""Tools available to the chat agent."""

import asyncio
from datetime import datetime
import logging
from pathlib import Path

from agentic_chat.mcp_client import call_tool

class Tools:
    """Collection of tools available to the chat agent."""
    
    @staticmethod
    def ls() -> str:
        """List files in the current directory."""
        return "\n".join(str(p) for p in Path.cwd().iterdir() if p.is_file())

    @staticmethod
    def date_now() -> str:
        """Return current date."""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def time_now() -> str:
        """Return current time."""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def greeting(name: str) -> str:
        """Wrapper for MCP 'greeting' tool."""
        async def _run():
            result = await call_tool("greeting", {"name": name})
            return result[0].text
        return asyncio.run(_run())

    @staticmethod
    def wiki_search(query: str) -> str:
        """Wrapper for MCP 'wiki_search' tool."""
        async def _run():
            try:
                result = await call_tool("wiki_search", {"query": query})
                response = result[0].text
                logging.info(f"Wikipedia response: {response[:100]}...")
                return response
            except Exception as e:
                error_msg = f"Error calling wiki_search: {str(e)}"
                logging.error(error_msg)
                return error_msg
        return asyncio.run(_run())

    @staticmethod
    def print_out(text: str, filename: str) -> str:
        """Write text to a file. Creates the file if it doesn't exist.
        Args:
            text: The text to write to the file
            filename: The name of the file to write to
        Returns:
            A message indicating success or failure
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            return f"Successfully wrote text to {filename}"
        except Exception as e:
            error_msg = f"Error writing to file: {str(e)}"
            logging.error(error_msg)
            return error_msg

    @staticmethod
    def read_file_context(filename: str) -> str:
        """Read up to `max_lines` from the given file."""
        max_lines = 50  # Number of lines to read from the file
        try:
            file_path = Path(filename).resolve()
            if not file_path.is_file():
                return f"File not found: {file_path}"
            
            with file_path.open('r', encoding='utf-8') as f:
                lines = []
                for _ in range(max_lines):
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line.rstrip('\n'))
                content = "\n".join(lines)
                # Add ellipsis if more content exists
                if f.readline():
                    content += "\n..."
                return content
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            return f"Error reading file: {e}"

    @classmethod
    def get_tools(cls, trace_tool):
        """Get all available tools wrapped with tracing."""
        return [
            trace_tool(cls.time_now),
            trace_tool(cls.date_now),
            trace_tool(cls.ls),
            trace_tool(cls.read_file_context),
            #trace_tool(cls.greeting),
            trace_tool(cls.wiki_search),
            trace_tool(cls.print_out),
        ]
