from agentic_chat.chat.session import ChatSession
from agentic_chat.prompts.prompts import CHAT_ASSISTANT_PROMPT
from agentic_chat.utils.logging import setup_logging
from agentic_chat.utils.chat_logger import ChatLogger

def main():
    setup_logging()
    logger = ChatLogger()
    session = ChatSession(use_prompt=CHAT_ASSISTANT_PROMPT, logger=logger)
    session.run()

if __name__ == "__main__":
    main()
