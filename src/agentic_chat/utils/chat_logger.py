from datetime import datetime
import textwrap


class ChatLogger:
    def __init__(self, log_file="chat_history.log"):
        self.log_file = log_file

    def log_message(self, role: str, content: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wrapped_content = textwrap.fill(content, width=80, subsequent_indent="    ")
        log_entry = f"[{timestamp}] {role.upper()}:\n{wrapped_content}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def log_tool_call(self, tool_name: str, args, kwargs):
        """Log tool calls to match the existing format."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] TOOL: {tool_name} called with args: {args}, kwargs: {kwargs}\n")