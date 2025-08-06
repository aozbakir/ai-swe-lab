from datetime import datetime
from functools import wraps
import logging

import lmstudio as lms

from im2203.agentic_chat.prompts import CHAT_ASSISTANT_PROMPT
from im2203.agentic_chat.tools import Tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def trace_tool(tool_fn):
    @wraps(tool_fn)
    def wrapper(*args, **kwargs):
        GREEN = "\033[1;32m"
        RESET = "\033[0m"
        logging.info(f"{GREEN}[TOOL CALL] {tool_fn.__name__} called with args: {args}, kwargs: {kwargs}{RESET}")
        return tool_fn(*args, **kwargs)
    return wrapper

class ChatSession:
    def __init__(self):
        self.model = lms.llm()
        self.chat = lms.Chat(CHAT_ASSISTANT_PROMPT)
        self.tools = Tools.get_tools(trace_tool)

    def log_message(self, role: str, content: str) -> None:
        """Log a chat message to the chat history file.
        
        Args:
            role: Either 'user' or 'assistant'
            content: The message content
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {role}: {content}\n"
        
        with open("chat_history.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
            
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
        print("Bot: ", end="", flush=True)
        
        # Capture bot's response for logging
        response_chunks = []

        def log_fragment(fragment, round_index=0):
                response_chunks.append(fragment.content)
                print(fragment.content, end="", flush=True)

        self.model.act(
            self.chat,
            tools=self.tools,
            on_message=self.chat.append,
            on_prediction_fragment=log_fragment,
            config={
                "maxTokens": 1000,
                "temperature": 0.7
            },
        )
        print()

        # Log complete bot response
        self.log_message("assistant", "".join(response_chunks))

    def run(self) -> None:
        """Run an interactive chat session."""
        while True:
            try:
                user_input = input("You (leave blank to exit): ")
            except EOFError:
                print()
                break
                
            if not user_input:
                break
                
            self.process_message(user_input)



def main():
    """Run the chat agent."""
    session = ChatSession()
    session.run()

if __name__ == "__main__":
    main()
