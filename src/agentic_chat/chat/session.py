from datetime import datetime
import textwrap
import lmstudio as lms

from agentic_chat.prompts.prompts import CHAT_ASSISTANT_PROMPT
from agentic_chat.tools.tools import Tools
from agentic_chat.utils.ansi import BOLD_BLUE, BOLD_GREEN, RESET
from agentic_chat.utils.logging import setup_logging
from agentic_chat.utils.helpers import trace_tool

setup_logging()

class ChatSession:
    def __init__(self, use_prompt=CHAT_ASSISTANT_PROMPT):
        self.model = lms.llm()
        self.chat = lms.Chat(use_prompt)
        self.tools = Tools.get_tools(trace_tool)

    def log_message(self, role: str, content: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wrapped_content = textwrap.fill(content, width=80, subsequent_indent="    ")
        log_entry = f"[{timestamp}] {role.upper()}:\n{wrapped_content}"
        with open("chat_history.log", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def print_fragment(self, fragment, round_index=0):
        print(fragment.content, end="", flush=True)

    def process_message(self, message: str) -> None:
        self.log_message("user", message)
        self.chat.add_user_message(message)
        print(f"{BOLD_GREEN}Bot:{RESET} ", end="", flush=True)
        response_chunks = []

        def log_fragment(fragment, round_index=0):
            response_chunks.append(fragment.content)
            print(f"{BOLD_GREEN}{fragment.content}{RESET}", end="", flush=True)

        tool_names = [t.__name__ for t in self.tools]
        # Logging is now handled by setup_logging and get_logger if needed

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
        self.log_message("assistant", "".join(response_chunks))

    def run(self) -> None:
        while True:
            try:
                user_input = input(f"{BOLD_BLUE}You (leave blank to exit): {RESET}")
            except EOFError:
                print()
                break
            if not user_input:
                break
            self.process_message(user_input)
