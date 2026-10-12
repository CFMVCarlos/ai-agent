import os
import subprocess

from openai.types.chat import ChatCompletionToolParam


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """Execute a Python file in a subprocess within the working directory.

    Parameters
    ----------
    working_directory : str
        The base directory path restricting permitted file access.
    file_path : str
        Path to the Python file to run, relative to working directory.
    args : list[str] | None
        Optional arguments passed to the script, by default None.

    Returns
    -------
    str
        Combined standard output and error streams, or an error message.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        output = subprocess.run(
            command,
            cwd=working_dir_abs,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

        strings = []
        if output.returncode:
            strings.append(f"Process exited with code {output.returncode}")
        if not output.stderr and not output.stdout:
            strings.append("No output produced")
        strings.append(f"STDOUT:{output.stdout}")
        strings.append(f"STDERR:{output.stderr}")

        return "".join(strings)
    except Exception as e:  # noqa:BLE001
        return f"Error: executing Python file: {e}"


schema_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory with optional arguments and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of string arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
