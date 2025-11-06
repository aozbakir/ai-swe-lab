from agentic_chat.chat.session import ChatSession
from agentic_chat.prompts.prompts import CHAT_ASSISTANT_PROMPT

def main():
    session = ChatSession(CHAT_ASSISTANT_PROMPT)
    session.run()

if __name__ == "__main__":
    main()
