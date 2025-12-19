import logging

def print_out(text: str, filename: str) -> str:
    """Write text to a file. Creates the file if it doesn't exist.
    Args:
        text: The text to write to the file
        filename: The name of the file to write to
    Returns:
        A message indicating success or failure
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Successfully wrote text to {filename}"
    except Exception as e:
        error_msg = f"Error writing to file: {str(e)}"
        logging.error(error_msg)
        return error_msg