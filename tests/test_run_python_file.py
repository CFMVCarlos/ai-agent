"""Test suite for functions.run_python_file."""

from functions.run_python_file import run_python_file


def test_run_python_file_main() -> None:
    result = run_python_file("calculator", "main.py")
    assert "Calculator App" in result or "Usage:" in result


def test_run_python_file_with_args() -> None:
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    assert "8" in result


def test_run_python_file_outside_dir_blocked() -> None:
    result = run_python_file("calculator", "../main.py")
    assert "outside the permitted working directory" in result


def test_run_python_file_nonexistent() -> None:
    result = run_python_file("calculator", "nonexistent.py")
    assert "does not exist" in result.lower()
