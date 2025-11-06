from datetime import datetime
from functools import wraps
import logging
import textwrap

import lmstudio as lms

from agentic_chat.prompts import CHAT_ASSISTANT_PROMPT, SALES_ANALYST_PROMPT
from agentic_chat.tools import Tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
SALES_ANALYST_PROMPT

# ANSI escape codes
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[34m"
GREEN = "\033[32m"
BOLD_BLUE = f"{BOLD}{BLUE}"
BOLD_GREEN = f"{BOLD}{GREEN}"

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

class ChatSession:
    def __init__(self, use_prompt=CHAT_ASSISTANT_PROMPT):
        self.model = lms.llm()
        self.chat = lms.Chat(use_prompt)
        self.tools = Tools.get_tools(trace_tool)
        

    def log_message(self, role: str, content: str) -> None:
        """Log a chat message to the chat history file.
        
        Args:
            role: Either 'user' or 'assistant'
            content: The message content
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wrapped_content = textwrap.fill(content, width=80, subsequent_indent="    ")
        log_entry = f"[{timestamp}] {role.upper()}:\n{wrapped_content}"
        
        with open("chat_history.log", "a", encoding="utf-8") as f:
            f.write(log_entry+ "\n")
            
    def print_fragment(self, fragment, round_index=0):
        # .act() supplies the round index as the second parameter
        # Setting a default value means the callback is also
        # compatible with .complete() and .respond().
        print(fragment.content, end="", flush=True)

    def process_message(self, message: str) -> None:
        """Process a single message in the chat session."""
        # Log user message
        self.log_message("user", message)

        self.chat.add_user_message(message)
        print(f"{BOLD_GREEN}Bot:{RESET} ", end="", flush=True)
        
        # Capture bot's response for logging
        response_chunks = []

        def log_fragment(fragment, round_index=0):
                response_chunks.append(fragment.content)
                print(f"{BOLD_GREEN}{fragment.content}{RESET}", end="", flush=True)

        # Log available tools for debugging
        tool_names = [t.__name__ for t in self.tools]
        logging.info(f"Available tools: {tool_names}")

        # Create tool schemas to help the model understand the format
        tool_schemas = []
        for tool in self.tools:
            schema = {
                "name": tool.__name__,
                "description": tool.__doc__ or f"Tool {tool.__name__}",
                "parameters": {}
            }
            tool_schemas.append(schema)
            
        self.model.act(
            self.chat,
            tools=self.tools,
            on_message=self.chat.append,
            on_prediction_fragment=log_fragment,
            config={
                "maxTokens": 1000,
                "temperature": 0.7,
                "toolSchemas": tool_schemas
            },
        )
        print()

        # Log complete bot response
        self.log_message("assistant", "".join(response_chunks))

    def run(self) -> None:
        """Run an interactive chat session."""
        while True:
            try:
                user_input = input(f"{BOLD_BLUE}You (leave blank to exit): {RESET}")
            except EOFError:
                print()
                break
                
            if not user_input:
                break
                
            self.process_message(user_input)

def main():
    """Run the chat agent."""
    session = ChatSession(CHAT_ASSISTANT_PROMPT) #SALES_ANALYST_PROMPT
    session.run()

if __name__ == "__main__":
    main()
