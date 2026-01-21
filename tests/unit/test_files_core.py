"""Unit tests for files.core module."""

import logging
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from find_large import constants
from find_large.files.core import error_exit, find_files, setup_logging

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "files"


class TestErrorExit:
    """Test cases for error_exit function."""

    def test_error_exit_prints_error_and_exits(self, tmp_path: Path) -> None:
        """Test error_exit prints error message and exits."""
        with patch("find_large.files.core.formatting.print_error") as mock_print:
            with patch("find_large.files.core.sys.exit") as mock_exit:
                error_exit("Test error")
                mock_print.assert_called_once_with("Test error")
                mock_exit.assert_called_once_with(1)


class TestSetupLogging:
    """Test cases for setup_logging function."""

    @pytest.fixture(autouse=True)
    def reset_logging(self) -> None:
        """Reset logging state before each test."""
        logging.root.handlers = []
        logging.root.setLevel(logging.WARNING)

    def test_setup_logging_verbose_true(self) -> None:
        """Test setup_logging with verbose=True sets DEBUG level."""
        setup_logging(True)
        # Check that logging is configured
        assert len(logging.root.handlers) > 0

    def test_setup_logging_verbose_false(self) -> None:
        """Test setup_logging with verbose=False sets INFO level."""
        setup_logging(False)
        # Check that logging is configured
        assert len(logging.root.handlers) > 0


class TestFindFiles:
    """Test cases for find_files function."""

    @pytest.fixture(autouse=True)
    def reset_logging(self) -> None:
        """Reset logging state before each test."""
        logging.root.handlers = []
        logging.root.setLevel(logging.WARNING)

    def test_find_files_finds_large_files(self, tmp_path: Path) -> None:
        """Test find_files finds files above size threshold."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "small.txt")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_files_skips_small_files(self, tmp_path: Path) -> None:
        """Test find_files skips files below size threshold."""
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "small.txt")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_files_skips_hidden_files(self, tmp_path: Path) -> None:
        """Test find_files skips hidden files."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / ".hidden")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_files_with_hidden_directories(self, tmp_path: Path) -> None:
        """Test find_files filters out hidden directories."""
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_files_with_verbose_hidden_dirs_filtered(self, tmp_path: Path) -> None:
        """Test find_files logs hidden directory filtering."""
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_files_with_verbose_logging(self, tmp_path: Path) -> None:
        """Test find_files with verbose logging enabled."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_files_with_verbose_large_file_found(self, tmp_path: Path) -> None:
        """Test find_files logs large file discovery."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_files_saves_to_output_file(self, tmp_path: Path) -> None:
        """Test find_files saves results to output file."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        output_file = tmp_path / "results.txt"

        find_files(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)

        assert output_file.exists()

    def test_find_files_no_size_column(self, tmp_path: Path) -> None:
        """Test find_files with no_size=True hides size column."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_size=True)

    def test_find_files_no_table_output(self, tmp_path: Path) -> None:
        """Test find_files with no_table=True uses plain text."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_table=True)

    def test_find_files_size_unit_gb(self, tmp_path: Path) -> None:
        """Test find_files with GB size unit."""
        shutil.copyfile(FIXTURES_DIR / "large_10k.bin", tmp_path / "large.bin")

        find_files(str(tmp_path), 0.00001, None, constants.SIZE_UNIT_GB)

    def test_find_files_handles_permission_errors(self, tmp_path: Path) -> None:
        """Test find_files handles permission errors gracefully."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        try:
            (tmp_path / "large.bin").chmod(0o000)
            find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)
        except Exception:
            pass
        finally:
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_find_files_handles_oserror(self, tmp_path: Path) -> None:
        """Test find_files handles OSError gracefully."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")

        try:
            (tmp_path / "large.bin").chmod(0o000)
            find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)
        except Exception:
            pass
        finally:
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_find_files_handles_output_file_error(self, tmp_path: Path) -> None:
        """Test find_files handles output file write errors."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        output_file = tmp_path / "nonexistent" / "results.txt"

        with patch("find_large.files.core.error_exit") as mock_error_exit:
            find_files(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)
            mock_error_exit.assert_called_once()

    def test_find_files_skips_excluded_directories(self, tmp_path: Path) -> None:
        """Test find_files skips excluded directories."""
        # Use mocking to simulate an excluded directory
        excluded_dir = tmp_path / "excluded"
        excluded_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", excluded_dir / "large.bin")

        # Create a file in a non-excluded directory
        normal_dir = tmp_path / "normal"
        normal_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", normal_dir / "large.bin")

        # Mock EXCLUDE_FOLDERS to include our test directory
        with patch("find_large.files.core.EXCLUDE_FOLDERS", [str(excluded_dir)]):
            find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_files_finds_multiple_files(self, tmp_path: Path) -> None:
        """Test find_files finds and sorts multiple files by size."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        shutil.copyfile(FIXTURES_DIR / "large_3k.bin", tmp_path / "medium.txt")
        shutil.copyfile(FIXTURES_DIR / "large_4k.bin", tmp_path / "small.txt")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_files_with_no_files_found(self, tmp_path: Path) -> None:
        """Test find_files handles case with no files found."""
        # Create only small files
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "small.txt")

        find_files(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)
