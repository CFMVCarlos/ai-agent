import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
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
