"""Unit tests for formatting module."""

from io import StringIO

import pytest
from rich.console import Console

from find_large import formatting


def test_print_ascii_art__files_command() -> None:
    """Test ASCII art prints for files command."""
    formatting.print_ascii_art("files")


def test_print_ascii_art__dirs_command() -> None:
    """Test ASCII art prints for dirs command."""
    formatting.print_ascii_art("dirs")


def test_print_ascii_art__vids_command() -> None:
    """Test ASCII art prints for vids command."""
    formatting.print_ascii_art("vids")


def test_print_error__displays_message() -> None:
    """Test error message is printed correctly."""
    formatting.print_error("Test error message")


def test_print_success__displays_message() -> None:
    """Test success message is printed correctly."""
    formatting.print_success("Test success message")


def test_print_status__displays_message() -> None:
    """Test status message is printed correctly."""
    formatting.print_status("Test status message")


def test_create_results_table__with_size_column() -> None:
    """Test table creation includes size column."""
    table = formatting.create_results_table(show_size=True)
    assert table is not None


def test_create_results_table__without_size_column() -> None:
    """Test table creation excludes size column."""
    table = formatting.create_results_table(show_size=False)
    assert table is not None


def test_format_table__with_size_column() -> None:
    """Test table formatting with size column."""
    data_lines = [
        ("Location", "Size"),
        ("/path/to/file1.txt", "1.00 GB"),
        ("/path/to/file2.txt", "500.00 MB"),
    ]
    formatting.format_table(data_lines, no_size=False, total_bytes=1536 * 1024 * 1024)


def test_format_table__without_size_column() -> None:
    """Test table formatting without size column."""
    data_lines = [
        ("Location",),
        ("/path/to/file1.txt",),
        ("/path/to/file2.txt",),
    ]
    formatting.format_table(data_lines, no_size=True, total_bytes=0)


def test_format_table__plain_text_with_size() -> None:
    """Test plain text output with size column."""
    data_lines = [
        ("Location", "Size"),
        ("/path/to/file1.txt", "1.00 GB"),
    ]
    formatting.format_table(
        data_lines, no_size=False, total_bytes=1024 * 1024 * 1024, no_table=True
    )


def test_format_table__plain_text_without_size() -> None:
    """Test plain text output without size column."""
    data_lines = [
        ("Location",),
        ("/path/to/file1.txt",),
    ]
    formatting.format_table(data_lines, no_size=True, total_bytes=0, no_table=True)


def test_format_table__to_file_console() -> None:
    """Test table formatting to file console."""
    data_lines = [
        ("Location", "Size"),
        ("/path/to/file1.txt", "1.00 GB"),
    ]
    file_console = Console(file=StringIO(), force_terminal=True)
    formatting.format_table(
        data_lines,
        no_size=False,
        total_bytes=1024 * 1024 * 1024,
        file_console=file_console,
    )


def test_get_status_context__returns_status() -> None:
    """Test status context creation."""
    status = formatting.get_status_context("Processing...")
    assert status is not None


@pytest.mark.parametrize(
    "total_bytes,expected_unit",
    [
        (1024**4, "TB"),  # 1 TB
        (1024**3, "GB"),  # 1 GB
        (1024**2, "MB"),  # 1 MB
        (500 * 1024**2, "MB"),  # 500 MB
        (2 * 1024**3, "GB"),  # 2 GB
    ],
)
def test_format_table__total_size_units(total_bytes: int, expected_unit: str) -> None:
    """Test total size displays correct units."""
    data_lines = [("Location", "Size"), ("/path/to/file.txt", "1.00 GB")]
    formatting.format_table(data_lines, no_size=False, total_bytes=total_bytes, no_table=True)
