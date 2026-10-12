"""Test suite for functions.write_file."""

from aiagent.functions.write_file import write_file


def test_write_file_outside_dir_blocked() -> None:
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    assert "outside the permitted working directory" in result


def test_write_file_within_dir() -> None:
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    assert "Successfully wrote" in result
