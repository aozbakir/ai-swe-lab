# domain/time_logic.py
# filepath: d:\Repos2\im2203\src\agentic_chat\domain\time_logic.py
"""Time domain logic for date and time operations."""
from datetime import datetime

def get_current_time() -> str:
    """
    Get the current time in HH:MM format.
    
    Returns:
        Current time as string in HH:MM format
    """
    return datetime.now().strftime("%H:%M")