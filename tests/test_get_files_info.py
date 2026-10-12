"""Test suite for functions.get_files_info."""

from aiagent.functions.get_files_info import get_files_info


def test_get_files_info_current_directory() -> None:
    result = get_files_info("calculator", ".")
    assert isinstance(result, str)
    assert "pkg" in result
    assert "main.py" in result


def test_get_files_info_subdirectory() -> None:
    result = get_files_info("calculator", "pkg")
    assert isinstance(result, str)
    assert "calculator.py" in result


def test_get_files_info_outside_dir_blocked() -> None:
    result = get_files_info("calculator", "/bin")
    assert "outside the permitted working directory" in result

    parent_result = get_files_info("calculator", "../")
    assert "outside the permitted working directory" in parent_result
