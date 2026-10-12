"""Tool function for inspecting files and directory hierarchies."""

import os

from openai.types.chat import ChatCompletionToolParam


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """List file and directory information within a bounded working directory.

    Parameters
    ----------
    working_directory : str
        The base directory path restricting permitted file access.
    directory : str, default="."
        Target directory to inspect, relative to the working directory.

    Returns
    -------
    str
        Formatted string listing file sizes and directory flags, or an
        error message if access fails.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        strings = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            strings.append(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(strings)
    except Exception as e:  # noqa:BLE001
        return f"Error: {e}"


schema_get_files_info: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
