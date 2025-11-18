# test_chat_logic.py
from pathlib import Path
from chat_logic import ChatLogic

def test_chat():
    config_path = Path("src/core/configs/config.yaml")

    try:
        chat = ChatLogic(config_path=config_path)

        result = chat.answer("What is MetaGPT?")

        print("\nChat succeeded!")
        print("Response:", result.get("response"))



    except Exception as e:
        print("Chat failed:", e)

if __name__ == "__main__":
    test_chat()
