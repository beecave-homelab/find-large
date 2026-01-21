"""Unit tests for videos.core module."""

import logging
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from find_large import constants
from find_large.videos.core import find_large_videos, is_video_file

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "videos"


class TestIsVideoFile:
    """Test cases for is_video_file function."""

    def test_is_video_file_recognizes_mp4(self) -> None:
        """Test is_video_file recognizes .mp4 files."""
        assert is_video_file("video.mp4") is True

    def test_is_video_file_recognizes_mkvs(self) -> None:
        """Test is_video_file recognizes .mkv files."""
        assert is_video_file("movie.mkv") is True

    def test_is_video_file_case_insensitive(self) -> None:
        """Test is_video_file is case insensitive."""
        assert is_video_file("video.MP4") is True
        assert is_video_file("video.Mp4") is True

    def test_is_video_file_rejects_non_video_files(self) -> None:
        """Test is_video_file rejects non-video files."""
        assert is_video_file("document.txt") is False
        assert is_video_file("image.jpg") is False
        assert is_video_file("archive.zip") is False


class TestFindLargeVideos:
    """Test cases for find_large_videos function."""

    @pytest.fixture(autouse=True)
    def reset_logging(self) -> None:
        """Reset logging state before each test."""
        logging.root.handlers = []
        logging.root.setLevel(logging.WARNING)

    def test_find_large_videos_finds_large_videos(self, tmp_path: Path) -> None:
        """Test find_large_videos finds large video files."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_skips_small_videos(self, tmp_path: Path) -> None:
        """Test find_large_videos skips small video files."""
        shutil.copyfile(FIXTURES_DIR / "small_100.mkv", tmp_path / "small.mkv")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_skips_non_video_files(self, tmp_path: Path) -> None:
        """Test find_large_videos skips non-video files even if large."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "not_video.txt")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_with_verbose_logging(self, tmp_path: Path) -> None:
        """Test find_large_videos with verbose logging enabled."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_large_videos_saves_to_output_file(self, tmp_path: Path) -> None:
        """Test find_large_videos saves results to output file."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        output_file = tmp_path / "results.txt"

        find_large_videos(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)

        assert output_file.exists()

    def test_find_large_videos_no_size_column(self, tmp_path: Path) -> None:
        """Test find_large_videos with no_size=True hides size column."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_size=True)

    def test_find_large_videos_no_table_output(self, tmp_path: Path) -> None:
        """Test find_large_videos with no_table=True uses plain text."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, no_table=True)

    def test_find_large_videos_size_unit_gb(self, tmp_path: Path) -> None:
        """Test find_large_videos with GB size unit."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        find_large_videos(str(tmp_path), 0.00001, None, constants.SIZE_UNIT_GB)

    def test_find_large_videos_handles_permission_errors(self, tmp_path: Path) -> None:
        """Test find_large_videos handles permission errors gracefully."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        try:
            (tmp_path / "large.mp4").chmod(0o000)
            find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)
        except Exception:
            pass
        finally:
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass

    def test_find_large_videos_handles_oserror(self, tmp_path: Path) -> None:
        """Test find_large_videos handles OSError gracefully."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        try:
            (tmp_path / "large.mp4").chmod(0o000)
            find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)
        except Exception:
            pass
        finally:
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass

    def test_find_large_videos_handles_output_file_error(self, tmp_path: Path) -> None:
        """Test find_large_videos handles output file write errors."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        output_file = tmp_path / "nonexistent" / "results.txt"

        with patch("find_large.videos.core.sys.exit") as mock_exit:
            find_large_videos(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)
            mock_exit.assert_called_once_with(1)

    def test_find_large_videos_skips_excluded_directories(self, tmp_path: Path) -> None:
        """Test find_large_videos skips excluded directories."""
        # Use mocking to simulate an excluded directory
        excluded_dir = tmp_path / "excluded"
        excluded_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", excluded_dir / "large.mp4")

        # Create a video in a non-excluded directory
        normal_dir = tmp_path / "normal"
        normal_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", normal_dir / "large.mp4")

        # Mock EXCLUDE_FOLDERS to include our test directory
        with patch("find_large.videos.core.EXCLUDE_FOLDERS", [str(excluded_dir)]):
            find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)

    def test_find_large_videos_skips_hidden_files(self, tmp_path: Path) -> None:
        """Test find_large_videos skips hidden files."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / ".hidden.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_finds_multiple_videos(self, tmp_path: Path) -> None:
        """Test find_large_videos finds and sorts multiple videos by size."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "small.mp4")
        shutil.copyfile(FIXTURES_DIR / "large_3k.avi", tmp_path / "large.mp4")
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "medium.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_with_no_videos_found(self, tmp_path: Path) -> None:
        """Test find_large_videos handles case with no videos found."""
        # Create only non-video files
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "document.txt")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_filters_by_size_threshold(self, tmp_path: Path) -> None:
        """Test find_large_videos filters videos by size threshold."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "small.mp4")
        shutil.copyfile(FIXTURES_DIR / "large_5k.mp4", tmp_path / "large.mp4")

        # Only large video should be found
        find_large_videos(str(tmp_path), 0.002, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_with_output_file(self, tmp_path: Path) -> None:
        """Test find_large_videos writes to output file."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        output_file = tmp_path / "results.txt"

        find_large_videos(str(tmp_path), 0.001, str(output_file), constants.SIZE_UNIT_MB)

        assert output_file.exists()

    def test_find_large_videos_handles_hidden_directories(self, tmp_path: Path) -> None:
        """Test find_large_videos skips hidden directories."""
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", hidden_dir / "large.mp4")

        find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB)

    def test_find_large_videos_handles_file_access_errors(self, tmp_path: Path) -> None:
        """Test find_large_videos handles file access errors gracefully."""
        shutil.copyfile(FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")

        try:
            (tmp_path / "large.mp4").chmod(0o000)
            find_large_videos(str(tmp_path), 0.001, None, constants.SIZE_UNIT_MB, verbose=True)
        except Exception:
            pass
        finally:
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass
