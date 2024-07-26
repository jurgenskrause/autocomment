# AutoCommenter

AutoCommenter is a Python script designed to automatically generate comments for code files in various programming languages. It leverages OpenAI's GPT model to analyze code files, generate meaningful comments, and insert them into the code. Commenting guidelines are specified through a GPT prompt, and can be customized to suit your needs.

## Features

- Analyzes code files to understand functionality and logic.
- Generates comments that provide context, explain purposes, and avoid redundancy.
- Uses XML documentation for public classes, methods, and properties.
- Processes multiple directories and files automatically.
- Allows processing of a single file via command-line argument.
- Supports multiple programming languages by specifying file extensions and prompt files.

## Requirements

- Python 3.7 or higher
- `openai` library
- `python-dotenv` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AutoCommenter.git
    cd AutoCommenter
    ```

2. Install the required Python packages:
    ```bash
    pip install openai python-dotenv
    ```

3. Set your OpenAI API key:
    - **Preferred**: Set the `OPENAI_API_KEY` as a system environment variable.
    - **Fallback**: Create a `.env` file in the root directory and add your OpenAI API key:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

4. Create a `config.json` file in the root directory and add your configuration:
    ```json
    {
        "root_dir": "/path/to/your/root/dir",
        "sub_dirs": ["Services", "Ui", "Models", "Pages", "ViewModels"],
        "dst_root_dir": "/path/to/your/destination/dir",
        "extensions": [".cs", ".py", ".js"],
        "prompt": "prompt-netmaui.txt"
    }
    ```

5. Create the default prompt file (e.g., `prompt-netmaui.txt`) and any other language-specific prompt files (e.g., `prompt-python.txt`) in the root directory and add your prompt text.

## Usage

### Process All Files

1. **Prepare the script for execution:**

    - Ensure your directory structure is set up as expected. The script will process files in the `root_dir` directory by default, including subdirectories `Services`, `Ui`, `Models`, `Pages`, and `ViewModels`.

    - Modify the `config.json` file if your directory structure or desired file extensions are different.

2. **Run the script:**

    ```bash
    python autocomment.py
    ```

### Process a Single File

1. **Specify the file and language on the command line:**

    ```bash
    python autocomment.py -f /path/to/your/file.cs -l python
    ```

3. **Script Behavior:**

    - The script reads each specified file in the configured directories, or the single file specified via the command line.
    - It sends the file content to the OpenAI model configured with guidelines for commenting.
    - It extracts the commented code and writes it back to the corresponding file.

## Configuration

### Adjusting Commenting Guidelines

You can modify the commenting guidelines in the prompt file specified in the `config.json` file. The `autocommenter.configure` method sets the rules and examples that the AI model will follow when generating comments.

### Customizing Directories and Files

To process specific files or additional directories, adjust the `root_dir`, `sub_dirs`, `extensions`, and `dst_root_dir` in the `config.json` file.

## Example

Here’s a quick example of how you can set up and run the script:

```bash
# Clone the repository
git clone https://github.com/jurgenskrause/AutoCommenter.git
cd AutoCommenter

# Install dependencies
pip install openai python-dotenv

# Set your OpenAI API key in the environment
export OPENAI_API_KEY=your_openai_api_key

# Alternatively, add your OpenAI API key in the .env file
echo "OPENAI_API_KEY=your_openai_api_key" > .env

# Create config.json file
echo '{
    "root_dir": "/path/to/your/root/dir",
    "sub_dirs": ["Services", "Ui", "Models", "Pages", "ViewModels"],
    "dst_root_dir": "/path/to/your/destination/dir",
    "extensions": [".cs", ".py", ".js"],
    "prompt": "prompt-netmaui.txt"
}' > config.json

# Create the specified prompt file and add your prompt text

# Run the script to process all files
python autocomment.py

# Run the script to process a single file
python autocomment.py -f /path/to/your/file.cs -l python
