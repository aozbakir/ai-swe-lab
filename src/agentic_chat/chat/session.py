# chat/session_new.py
# filepath: d:\Repos2\im2203\src\agentic_chat\chat\session_new.py
"""Chat UI using domain layer directly."""
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.chat_session import ChatSession as DomainChatSession
from llm.factory import LLMFactory
from llm.prompts.prompts import CHAT_ASSISTANT_PROMPT
from utils.ansi import BOLD_BLUE, BOLD_GREEN, RESET
from utils.chat_logger import ChatLogger
from llm.tools.registry import tool_registry

# Import tools to register them
from llm import tools

class ChatSession:
    def __init__(self, config_path: str = None, system_prompt: str = None, logger=None):
        """Initialize chat session with domain logic."""
        # Create LLM instance
        factory = LLMFactory()
        llm = factory.get("lmstudio-agent")()
        
        # Use provided prompt or default
        prompt = system_prompt or CHAT_ASSISTANT_PROMPT
        
        # Create domain session (handles conversation state + LLM calls)
        self.domain_session = DomainChatSession(llm, prompt)
        self.llm = llm
        
        # Initialize logger for chat history - IMPORTANT!
        self.logger = logger or ChatLogger()
        
        print(f"🤖 Using backend: {llm.backend_name}")
        
        # Get tool count from registry
        tools_count = len(tool_registry.tools)
        print(f"🔧 Available tools: {tools_count} tools loaded")
        
        if tools_count > 0:
            tool_names = [schema['function']['name'] for schema in tool_registry.schemas]
            print(f"🛠️  Tools: {', '.join(tool_names)}")

    def process_message(self, message: str) -> str:
        """Process user message via domain layer."""
        # Log user message FIRST
        self.logger.log_message("user", message)
        
        print(f"{BOLD_GREEN}Bot:{RESET} ", end="", flush=True)
        
        # Delegate directly to domain
        response = self.domain_session.process_message(message)
        
        print()  # New line after streaming
        
        # Log assistant response AFTER
        self.logger.log_message("assistant", response)
        
        return response

    def run(self):
        """Run interactive chat session."""
        print(f"\n{BOLD_BLUE}=== Agentic Chat Session ==={RESET}")
        print("Type your message and press Enter. Leave blank to exit.\n")
        
        while True:
            try:
                user_input = input(f"{BOLD_BLUE}You: {RESET}")
            except EOFError:
                print()
                break
                
            if not user_input.strip():
                print("Goodbye! 👋")
                break
                
            self.process_message(user_input)
            print()

    def clear_history(self):
        """Clear conversation history."""
        # Reset domain session messages but keep system prompt
        self.domain_session.messages = [{"role": "system", "content": self.domain_session.prompt}]
        print("🗑️  Conversation history cleared!")

if __name__ == "__main__":
    session = ChatSession()
    session.run()