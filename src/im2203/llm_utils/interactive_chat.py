#!/usr/bin/env python
"""Interactive chat interface for ConversationManager - run from terminal"""

from pathlib import Path
from im2203.llm_utils.factory import LLMFactory
from im2203.llm_utils.chat import ConversationManager


def main():
    """Run an interactive chat session in the terminal"""
    print("=" * 60)
    print("Interactive Chat Session")
    print("=" * 60)
    
    # Load configurations
    config_dir = Path(__file__).parent / "configs"
    llm_config = config_dir / "config.yaml"
    chat_config = config_dir / "conversation.yaml"
    
    print("\nInitializing LLM...")
    llm_factory = LLMFactory()
    llm = llm_factory.create_from_yaml_file(llm_config)
    
    print("Creating conversation manager...")
    chat = ConversationManager(llm=llm, config_path=chat_config, verbose=False)
    
    print("\n" + "=" * 60)
    print("Chat ready! Type 'exit', 'quit', or 'q' to end.")
    print("Type 'history' to see conversation history.")
    print("Type 'reset' to start a new conversation.")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'history':
                print("\n📜 Conversation History:")
                print("-" * 60)
                for msg in chat.get_history():
                    role_emoji = "🧑" if msg['role'] == 'user' else "🤖"
                    print(f"{role_emoji} {msg['role'].capitalize()}: {msg['content']}")
                print("-" * 60)
                continue
            
            if user_input.lower() == 'reset':
                chat.reset()
                print("\n🔄 Conversation reset. Starting fresh!")
                continue
            
            # Get response from chat
            response = chat.chat(user_input)
            print(f"\n🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
