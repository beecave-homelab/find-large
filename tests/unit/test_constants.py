"""Unit tests for constants module."""

import os
import platform

import pytest

from find_large import constants


def test_default_dir_is_current_directory() -> None:
    """Test DEFAULT_DIR is set to current directory."""
    assert constants.DEFAULT_DIR == "."


def test_default_size_gb_value() -> None:
    """Test DEFAULT_SIZE_GB is 1."""
    assert constants.DEFAULT_SIZE_GB == 1


def test_default_size_mb_value() -> None:
    """Test DEFAULT_SIZE_MB is 100."""
    assert constants.DEFAULT_SIZE_MB == 100


def test_kb_to_bytes_conversion() -> None:
    """Test KB_TO_BYTES conversion constant."""
    assert constants.KB_TO_BYTES == 1024


def test_mb_to_bytes_conversion() -> None:
    """Test MB_TO_BYTES conversion constant."""
    assert constants.MB_TO_BYTES == 1024 * 1024


def test_gb_to_bytes_conversion() -> None:
    """Test GB_TO_BYTES conversion constant."""
    assert constants.GB_TO_BYTES == 1024 * 1024 * 1024


def test_tb_to_bytes_conversion() -> None:
    """Test TB_TO_BYTES conversion constant."""
    assert constants.TB_TO_BYTES == 1024 * 1024 * 1024 * 1024


def test_include_hidden_folders_contains_git() -> None:
    """Test INCLUDE_HIDDEN_FOLDERS contains .git."""
    assert ".git" in constants.INCLUDE_HIDDEN_FOLDERS


def test_include_hidden_folders_contains_config() -> None:
    """Test INCLUDE_HIDDEN_FOLDERS contains .config."""
    assert ".config" in constants.INCLUDE_HIDDEN_FOLDERS


def test_include_hidden_folders_contains_huggingface() -> None:
    """Test INCLUDE_HIDDEN_FOLDERS contains .huggingface."""
    assert ".huggingface" in constants.INCLUDE_HIDDEN_FOLDERS


def test_include_hidden_folders_contains_local() -> None:
    """Test INCLUDE_HIDDEN_FOLDERS contains .local."""
    assert ".local" in constants.INCLUDE_HIDDEN_FOLDERS


def test_exclude_folders_is_list() -> None:
    """Test EXCLUDE_FOLDERS is a list."""
    assert isinstance(constants.EXCLUDE_FOLDERS, list)


def test_exclude_folders_not_empty() -> None:
    """Test EXCLUDE_FOLDERS is not empty."""
    assert len(constants.EXCLUDE_FOLDERS) > 0


@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS-specific paths")
def test_exclude_folders_contains_system_directories() -> None:
    """Test EXCLUDE_FOLDERS contains system directories."""
    assert "/System" in constants.EXCLUDE_FOLDERS
    assert "/private" in constants.EXCLUDE_FOLDERS


@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS-specific paths")
def test_exclude_folders_contains_trash() -> None:
    """Test EXCLUDE_FOLDERS contains Trash."""
    trash_path = os.path.expanduser("~/.Trash")
    assert trash_path in constants.EXCLUDE_FOLDERS


@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS-specific paths")
def test_exclude_folders_contains_photos_library() -> None:
    """Test EXCLUDE_FOLDERS contains Photos Library."""
    photos_path = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
    assert photos_path in constants.EXCLUDE_FOLDERS


def test_size_unit_gb_constant() -> None:
    """Test SIZE_UNIT_GB constant."""
    assert constants.SIZE_UNIT_GB == "GB"


def test_size_unit_mb_constant() -> None:
    """Test SIZE_UNIT_MB constant."""
    assert constants.SIZE_UNIT_MB == "MB"


def test_size_unit_tb_constant() -> None:
    """Test SIZE_UNIT_TB constant."""
    assert constants.SIZE_UNIT_TB == "TB"


def test_exclude_folders_paths_are_absolute() -> None:
    """Test that exclude folder paths are expanded to absolute paths."""
    for folder in constants.EXCLUDE_FOLDERS:
        if folder.startswith("~"):
            assert os.path.isabs(os.path.expanduser(folder))
        else:
            assert os.path.isabs(folder) or folder.startswith("/")
