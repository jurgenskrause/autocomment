import os
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from ai import AutoComment
from utils import read_file, extract_commented_code, write_to_file

def load_config():
    """
    Load configuration from config.json.

    Returns:
        dict: The configuration dictionary.
    """
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def initialize_client():
    """
    Initialize the OpenAI client with the API key from environment variables.

    First, it tries to load the API key from the system environment variables.
    If the API key is not found, it attempts to load it from a .env file.

    Returns:
        OpenAI: The initialized OpenAI client.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        load_dotenv(find_dotenv())
        api_key = os.getenv("OPENAI_API_KEY")
        
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables or .env file.")
    
    return OpenAI(api_key=api_key)

def process_file(client, input_file_path, output_file_path, prompt_text):
    """
    Process a single file for code commenting.

    Args:
        client (OpenAI): The initialized OpenAI client.
        input_file_path (str): The path to the input file to be processed.
        output_file_path (str): The path to the output file where commented code will be written.
        prompt_text (str): The prompt text for configuring the AI model.
    """
    # Read the content of the input file
    text_content = read_file(input_file_path)

    # Create instances with a specific model parameter
    autocommenter = AutoComment(client=client, model="gpt-4o-mini", color="\033[32m", name="AutoCommenter")

    # Configure the AI model for code commenting
    autocommenter.configure(prompt_text)

    # Run initial completion
    autocommenter.says('Please submit the file to be analyzed.')
    autocommenter.display_last_message()
    print(f"Processing file: {input_file_path}")
    autocommenter.hears(text_content)
    response = autocommenter.getCompletion()

    commented_code = extract_commented_code(response)

    if commented_code:
        write_to_file(output_file_path, commented_code)
        print(f"Commented code has been written to {output_file_path}")
    else:
        print(f"No commented code found between the specified anchors in {input_file_path}.")

def main():
    """
    Main function to execute the script. It processes either a single file specified by the user or iterates over multiple files as defined in the configuration.
    """
    # Load configuration from config.json
    config = load_config()

    root_dir = config["root_dir"]
    sub_dirs = config["sub_dirs"]
    dst_root_dir = config["dst_root_dir"]
    extensions = config["extensions"]
    default_prompt_file = config["prompt"]

    # Ensure the destination root directory exists
    os.makedirs(dst_root_dir, exist_ok=True)

    # Argument parser setup
    parser = argparse.ArgumentParser(description="AutoCommenter Script")
    parser.add_argument('-f', '--file', type=str, help="Single file to process")
    parser.add_argument('-l', '--language', type=str, help="Language to determine which prompt file to use")

    args = parser.parse_args()

    # Validate arguments
    if args.file and not args.language:
        parser.error("--language is required when --file is specified")

    # Read the prompt text from the configured prompt file
    if args.language:
        prompt_file = f'prompt-{args.language}.txt'
    else:
        prompt_file = default_prompt_file

    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file '{prompt_file}' not found.")

    prompt_text = read_file(prompt_file)

    # Initialize the OpenAI client
    client = initialize_client()

    if args.file:
        # Process a single file specified on the command line
        input_file_path = args.file
        output_file_path = args.file
        process_file(client, input_file_path, output_file_path, prompt_text)
    else:
        # Iterate over each directory and process files with the specified extensions
        for sub_dir in [''] + sub_dirs:  # Include the root directory and subdirectories
            current_dir = os.path.join(root_dir, sub_dir)
            for file_name in os.listdir(current_dir):
                if any(file_name.endswith(ext) for ext in extensions):  # Only process files with specified extensions
                    print(f"Processing file: {file_name}")
                    input_file_path = os.path.join(current_dir, file_name)
                    output_file_path = os.path.join(dst_root_dir, sub_dir, file_name)
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    process_file(client, input_file_path, output_file_path, prompt_text)

if __name__ == "__main__":
    main()
