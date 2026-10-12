import os

from openai.types.chat import ChatCompletionToolParam


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write text content to a target file within the working directory.

    Parameters
    ----------
    working_directory : str
        The base directory path restricting permitted file access.
    file_path : str
        Path to the destination file, relative to working directory.
    content : str
        Text content to write into the file.

    Returns
    -------
    str
        Confirmation message with character count, or an error message.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"


schema_write_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
