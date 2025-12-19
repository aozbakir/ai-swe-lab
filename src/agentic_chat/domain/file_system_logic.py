# domain/file_system_logic.py

from pathlib import Path

def list_files(**kwargs) -> str:
    """List files in the current directory."""
    current_dir = Path.cwd()
    all_items = current_dir.iterdir()
    files_only = [item for item in all_items if item.is_file()]
    file_names = [str(file) for file in files_only]
    return "\n".join(file_names)