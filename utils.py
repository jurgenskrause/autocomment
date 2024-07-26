# utils.py

import os

def read_file(file_path):
    """
    Reads the content of a text file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def extract_commented_code(response_text):
    """
    Extracts the code between specified anchors from the response text.

    Args:
        response_text (str): The text containing the commented code.

    Returns:
        str: The extracted code between the anchors if found, otherwise None.
    """
    start_anchor = "###START OF COMMENTED CODE###"
    end_anchor = "###END OF COMMENTED CODE###"
    start_index = response_text.find(start_anchor) + len(start_anchor)
    end_index = response_text.find(end_anchor)
    
    if start_index != -1 and end_index != -1:
        return response_text[start_index:end_index].strip()
    else:
        return None

def write_to_file(file_path, content):
    """
    Writes the extracted code to a new file.

    Args:
        file_path (str): The path to the file where the content will be written.
        content (str): The content to be written to the file.
    """
    with open(file_path, 'w') as file:
        file.write(content)
