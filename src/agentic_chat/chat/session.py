import lmstudio as lms

from agentic_chat.prompts.prompts import CHAT_ASSISTANT_PROMPT
from agentic_chat.tools.tools import Tools
from agentic_chat.utils.ansi import BOLD_BLUE, BOLD_GREEN, RESET
from agentic_chat.utils.helpers import trace_tool
from agentic_chat.utils.chat_logger import ChatLogger

class ChatSession:
    def __init__(self, use_prompt=CHAT_ASSISTANT_PROMPT, logger=None):
        self.model = lms.llm()
        self.chat = lms.Chat(use_prompt)
        self.tools = Tools.get_tools(trace_tool)
        self.response_chunks = []
        self.logger = logger or ChatLogger()

    def _build_tool_schemas(self):
        return [
            {
                "name": tool.__name__,
                "description": tool.__doc__ or f"Tool {tool.__name__}",
                "parameters": {}
            }
            for tool in self.tools
        ]

    def _print_bot_response(self, content):
        print(f"{BOLD_GREEN}{content}{RESET}", end="", flush=True)

    def _log_fragment(self, fragment, round_index=0):
        self.response_chunks.append(fragment.content)
        self._print_bot_response(fragment.content)

    def process_message(self, message: str) -> None:
        self.logger.log_message("user", message)
        self.chat.add_user_message(message)
        print(f"{BOLD_GREEN}Bot:{RESET} ", end="", flush=True)
        self.response_chunks = []

        tool_schemas = self._build_tool_schemas() # This should be a singleton.
        self.model.act(
            self.chat,
            tools=self.tools,
            on_message=self.chat.append,
            on_prediction_fragment=self._log_fragment,
            config={
                "maxTokens": 1000,
                "temperature": 0.7,
                "toolSchemas": tool_schemas
            },
        )
        print()
        self.logger.log_message("assistant", "".join(self.response_chunks))

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