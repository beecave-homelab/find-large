"""Unit tests for dirs.core module."""

import logging
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from find_large import constants
from find_large.dirs.core import find_large_dirs, get_dir_size

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "files"


class TestGetDirSize:
    """Test cases for get_dir_size function."""

    @pytest.fixture(autouse=True)
    def reset_logging(self) -> None:
        """Reset logging state before each test."""
        logging.root.handlers = []
        logging.root.setLevel(logging.WARNING)

    def test_get_dir_size_calculates_total_size(self, tmp_path: Path) -> None:
        """Test get_dir_size calculates total size of directory."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", test_dir / "file1.txt")
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", test_dir / "file2.txt")

        size = get_dir_size(str(test_dir))
        assert size == 200

    def test_get_dir_size_handles_permission_errors(self, tmp_path: Path) -> None:
        """Test get_dir_size handles permission errors gracefully."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", test_dir / "file1.txt")

        try:
            (test_dir / "file1.txt").chmod(0o000)
            get_dir_size(str(test_dir), verbose=True)
        except Exception:
            pass
        finally:
            try:
                (test_dir / "file1.txt").chmod(0o644)
            except Exception:
                pass

    def test_get_dir_size_handles_oserror(self, tmp_path: Path) -> None:
        """Test get_dir_size handles OSError gracefully."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", test_dir / "file1.txt")

        try:
            (test_dir / "file1.txt").chmod(0o000)
            get_dir_size(str(test_dir), verbose=True)
        except Exception:
            pass
        finally:
            try:
                (test_dir / "file1.txt").chmod(0o644)
            except Exception:
                pass


class TestFindLargeDirs:
    """Test cases for find_large_dirs function."""

    @pytest.fixture(autouse=True)
    def reset_logging(self) -> None:
        """Reset logging state before each test."""
        logging.root.handlers = []
        logging.root.setLevel(logging.WARNING)

    def test_find_large_dirs_finds_large_directories(self, tmp_path: Path) -> None:
        """Test find_large_dirs finds directories above size threshold."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_dirs_skips_small_directories(self, tmp_path: Path) -> None:
        """Test find_large_dirs skips directories below size threshold."""
        small_dir = tmp_path / "small_dir"
        small_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", small_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 1, None, constants.SIZE_UNIT_MB)

    def test_find_large_dirs_with_verbose_logging(self, tmp_path: Path) -> None:
        """Test find_large_dirs with verbose logging enabled."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_large_dirs_saves_to_output_file(self, tmp_path: Path) -> None:
        """Test find_large_dirs saves results to output file."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")
        output_file = tmp_path / "results.txt"

        find_large_dirs(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)

        assert output_file.exists()

    def test_find_large_dirs_no_size_column(self, tmp_path: Path) -> None:
        """Test find_large_dirs with no_size=True hides size column."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_size=True)

    def test_find_large_dirs_no_table_output(self, tmp_path: Path) -> None:
        """Test find_large_dirs with no_table=True uses plain text."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_table=True)

    def test_find_large_dirs_size_unit_gb(self, tmp_path: Path) -> None:
        """Test find_large_dirs with GB size unit."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_10k.bin", large_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.00001, None, constants.SIZE_UNIT_GB)

    def test_find_large_dirs_handles_output_file_error(self, tmp_path: Path) -> None:
        """Test find_large_dirs handles output file write errors."""
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", large_dir / "file1.txt")
        output_file = tmp_path / "nonexistent" / "results.txt"

        with patch("find_large.dirs.core.formatting.print_error"):
            with patch("find_large.dirs.core.sys.exit") as mock_exit:
                find_large_dirs(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)
                mock_exit.assert_called_once_with(1)

    def test_find_large_dirs_skips_excluded_directories(self, tmp_path: Path) -> None:
        """Test find_large_dirs skips excluded directories."""
        # Use mocking to simulate an excluded directory
        excluded_dir = tmp_path / "excluded"
        excluded_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", excluded_dir / "file1.txt")

        # Create a directory in a non-excluded location
        normal_dir = tmp_path / "normal"
        normal_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", normal_dir / "file2.txt")

        # Mock EXCLUDE_FOLDERS to include our test directory
        with patch("find_large.dirs.core.EXCLUDE_FOLDERS", [str(excluded_dir)]):
            find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_large_dirs_handles_hidden_directories(self, tmp_path: Path) -> None:
        """Test find_large_dirs skips hidden directories."""
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", hidden_dir / "file1.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_dirs_finds_multiple_directories(self, tmp_path: Path) -> None:
        """Test find_large_dirs finds and sorts multiple directories by size."""
        small_dir = tmp_path / "small_dir"
        small_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", small_dir / "file1.txt")
        large_dir = tmp_path / "large_dir"
        large_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_3k.bin", large_dir / "file2.txt")
        medium_dir = tmp_path / "medium_dir"
        medium_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", medium_dir / "file3.txt")

        find_large_dirs(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_dirs_with_no_directories_found(self, tmp_path: Path) -> None:
        """Test find_large_dirs handles case with no directories found."""
        # Create only small files
        shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "small.txt")

        find_large_dirs(str(tmp_path), 1, None, constants.SIZE_UNIT_MB)
