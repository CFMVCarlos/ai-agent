"""Test suite for functions.get_file_content."""

from aiagent.functions.get_file_content import get_file_content


def test_get_file_content_reads_existing_file() -> None:
    result = get_file_content("calculator", "lorem.txt")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_file_content_outside_dir_blocked() -> None:
    result = get_file_content("calculator", "/bin/cat")
    assert "outside the permitted working directory" in result


def test_get_file_content_nonexistent_file() -> None:
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    assert "not found" in result.lower()
