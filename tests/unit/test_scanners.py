"""Unit tests for scanner modules."""

import shutil
from pathlib import Path

import pytest

from find_large import constants
from find_large.core import SizeScannerBase
from find_large.dirs.scanner import DirectoryScanner
from find_large.files.scanner import FileScanner
from find_large.videos.scanner import VideoScanner

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "files"
VIDEO_FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "videos"


@pytest.fixture
def sample_file_tree(tmp_path: Path) -> Path:
    """Create a sample file tree for testing.

    Returns:
        Path: Path to the temporary directory with sample files.
    """
    # Create directories
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / ".hidden_dir").mkdir()

    # Create files
    shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "small.txt")
    shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
    shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / ".hidden_file")
    shutil.copyfile(FIXTURES_DIR / "large_3k.bin", tmp_path / "dir1" / "file1.txt")
    shutil.copyfile(FIXTURES_DIR / "small_100.txt", tmp_path / "dir1" / "file2.txt")
    shutil.copyfile(FIXTURES_DIR / "large_4k.bin", tmp_path / "dir2" / "file3.txt")

    return tmp_path


@pytest.fixture
def sample_video_tree(tmp_path: Path) -> Path:
    """Create a sample video file tree for testing.

    Returns:
        Path: Path to the temporary directory with sample video files.
    """
    # Create directories
    (tmp_path / "videos").mkdir()
    (tmp_path / "other").mkdir()

    # Create video files
    shutil.copyfile(VIDEO_FIXTURES_DIR / "large_2k.mp4", tmp_path / "videos" / "large.mp4")
    shutil.copyfile(VIDEO_FIXTURES_DIR / "small_100.mkv", tmp_path / "videos" / "small.mkv")
    shutil.copyfile(VIDEO_FIXTURES_DIR / "large_3k.avi", tmp_path / "other" / "movie.avi")
    shutil.copyfile(VIDEO_FIXTURES_DIR / "large_2k.mp4", tmp_path / "other" / "not_video.txt")

    return tmp_path


class TestFileScanner:
    """Test cases for FileScanner."""

    def test_scanner_is_subclass_of_base(self) -> None:
        """Test FileScanner is a subclass of SizeScannerBase."""
        assert issubclass(FileScanner, SizeScannerBase)

    def test_scan__finds_large_files(self, sample_file_tree: Path) -> None:
        """Test scanner finds files above size threshold."""
        # Mock exclude folders to avoid excluding tmp_path on macOS
        scanner = FileScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        # Clear exclude folders to allow scanning
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert len(scanner.items_list) == 3
        assert any("large.bin" in path for path, _ in scanner.items_list)
        assert any("file1.txt" in path for path, _ in scanner.items_list)
        assert any("file3.txt" in path for path, _ in scanner.items_list)

    def test_scan__skips_small_files(self, sample_file_tree: Path) -> None:
        """Test scanner skips files below size threshold."""
        scanner = FileScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.size_bytes_threshold = 5120
        scanner.scan()
        assert len(scanner.items_list) == 0

    def test_scan__skips_hidden_files(self, sample_file_tree: Path) -> None:
        """Test scanner skips hidden files."""
        scanner = FileScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert not any(".hidden_file" in path for path, _ in scanner.items_list)

    def test_scan__calculates_total_bytes(self, sample_file_tree: Path) -> None:
        """Test scanner calculates total bytes correctly."""
        scanner = FileScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        expected_total = 2048 + 3072 + 4096
        assert scanner.total_bytes == expected_total

    def test_scan__handles_permission_errors(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors gracefully."""
        scanner = FileScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        # Create a file that we'll make unreadable
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        # Make file unreadable (may not work on all systems)
        try:
            (tmp_path / "large.bin").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_scan__handles_permission_errors_verbose(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors with verbose logging."""
        scanner = FileScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        # Create a file that we'll make unreadable
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        # Make file unreadable
        try:
            (tmp_path / "large.bin").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_scan__handles_oserror(self, tmp_path: Path) -> None:
        """Test scanner handles OSError gracefully."""
        scanner = FileScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        # Create a file that we'll make unreadable
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        # Make file unreadable
        try:
            (tmp_path / "large.bin").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_scan__with_verbose_logging(self, sample_file_tree: Path) -> None:
        """Test scanner with verbose logging enabled."""
        scanner = FileScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert len(scanner.items_list) > 0


class TestDirectoryScanner:
    """Test cases for DirectoryScanner."""

    def test_scanner_is_subclass_of_base(self) -> None:
        """Test DirectoryScanner is a subclass of SizeScannerBase."""
        assert issubclass(DirectoryScanner, SizeScannerBase)

    def test_scan__finds_large_directories(self, sample_file_tree: Path) -> None:
        """Test scanner finds directories above size threshold."""
        scanner = DirectoryScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        # Should find dir1, dir2, and root directory
        assert len(scanner.items_list) >= 2

    def test_scan__calculates_recursive_sizes(self, sample_file_tree: Path) -> None:
        """Test scanner calculates recursive directory sizes."""
        scanner = DirectoryScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        # dir1 should have 3072 + 100 bytes
        dir1_size = next((size for path, size in scanner.items_list if "dir1" in path), 0)
        assert dir1_size >= 3072

    def test_scan__skips_small_directories(self, sample_file_tree: Path) -> None:
        """Test scanner skips directories below size threshold."""
        scanner = DirectoryScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.size_bytes_threshold = 10240
        scanner.scan()
        # No directory should be >= 10KB
        assert len(scanner.items_list) == 0

    def test_scan__calculates_total_without_double_counting(self, sample_file_tree: Path) -> None:
        """Test scanner calculates total without double-counting nested directories."""
        scanner = DirectoryScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        # Total should be sum of non-overlapping directories
        assert scanner.total_bytes > 0

    def test_scan__initializes_dir_sizes_dict(self, sample_file_tree: Path) -> None:
        """Test scanner initializes dir_sizes dictionary."""
        scanner = DirectoryScanner(
            search_dir=str(sample_file_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        assert hasattr(scanner, "dir_sizes")
        assert isinstance(scanner.dir_sizes, dict)

    def test_scan__handles_permission_errors(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors gracefully."""
        scanner = DirectoryScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        # Create a file that we'll make unreadable
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        # Make file unreadable
        try:
            (tmp_path / "large.bin").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass

    def test_scan__handles_permission_errors_verbose(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors with verbose logging."""
        scanner = DirectoryScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        # Create a file that we'll make unreadable
        shutil.copyfile(FIXTURES_DIR / "large_2k.bin", tmp_path / "large.bin")
        # Make file unreadable
        try:
            (tmp_path / "large.bin").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.bin").chmod(0o644)
            except Exception:
                pass


class TestVideoScanner:
    """Test cases for VideoScanner."""

    def test_scanner_is_subclass_of_base(self) -> None:
        """Test VideoScanner is a subclass of SizeScannerBase."""
        assert issubclass(VideoScanner, SizeScannerBase)

    def test_video_extensions__contains_common_formats(self) -> None:
        """Test VIDEO_EXTENSIONS contains common video formats."""
        assert ".mp4" in VideoScanner.VIDEO_EXTENSIONS
        assert ".mkv" in VideoScanner.VIDEO_EXTENSIONS
        assert ".avi" in VideoScanner.VIDEO_EXTENSIONS
        assert ".mov" in VideoScanner.VIDEO_EXTENSIONS

    def test_is_video_file__recognizes_mp4(self) -> None:
        """Test is_video_file recognizes .mp4 files."""
        scanner = VideoScanner(
            search_dir="/tmp",
            size_mb=1,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        assert scanner.is_video_file("video.mp4") is True

    def test_is_video_file__recognizes_mkvs(self) -> None:
        """Test is_video_file recognizes .mkv files."""
        scanner = VideoScanner(
            search_dir="/tmp",
            size_mb=1,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        assert scanner.is_video_file("movie.mkv") is True

    def test_is_video_file__case_insensitive(self) -> None:
        """Test is_video_file is case insensitive."""
        scanner = VideoScanner(
            search_dir="/tmp",
            size_mb=1,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        assert scanner.is_video_file("video.MP4") is True
        assert scanner.is_video_file("video.Mp4") is True

    def test_is_video_file__rejects_non_video_files(self) -> None:
        """Test is_video_file rejects non-video files."""
        scanner = VideoScanner(
            search_dir="/tmp",
            size_mb=1,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        assert scanner.is_video_file("document.txt") is False
        assert scanner.is_video_file("image.jpg") is False
        assert scanner.is_video_file("archive.zip") is False

    def test_scan__finds_large_video_files(self, sample_video_tree: Path) -> None:
        """Test scanner finds large video files."""
        scanner = VideoScanner(
            search_dir=str(sample_video_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert len(scanner.items_list) == 2
        assert any("large.mp4" in path for path, _ in scanner.items_list)
        assert any("movie.avi" in path for path, _ in scanner.items_list)

    def test_scan__skips_non_video_files(self, sample_video_tree: Path) -> None:
        """Test scanner skips non-video files even if large."""
        scanner = VideoScanner(
            search_dir=str(sample_video_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert not any("not_video.txt" in path for path, _ in scanner.items_list)

    def test_scan__skips_small_video_files(self, sample_video_tree: Path) -> None:
        """Test scanner skips small video files."""
        scanner = VideoScanner(
            search_dir=str(sample_video_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        assert not any("small.mkv" in path for path, _ in scanner.items_list)

    def test_scan__calculates_total_bytes(self, sample_video_tree: Path) -> None:
        """Test scanner calculates total bytes correctly."""
        scanner = VideoScanner(
            search_dir=str(sample_video_tree),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        scanner.scan()
        expected_total = 2048 + 3072
        assert scanner.total_bytes == expected_total

    def test_scan__handles_permission_errors(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors gracefully."""
        scanner = VideoScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=False,
        )
        scanner.exclude_folders_abs = []
        # Create a video file that we'll make unreadable
        shutil.copyfile(VIDEO_FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        # Make file unreadable
        try:
            (tmp_path / "large.mp4").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass

    def test_scan__handles_permission_errors_verbose(self, tmp_path: Path) -> None:
        """Test scanner handles permission errors with verbose logging."""
        scanner = VideoScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        # Create a video file that we'll make unreadable
        shutil.copyfile(VIDEO_FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        # Make file unreadable
        try:
            (tmp_path / "large.mp4").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass

    def test_scan__handles_oserror(self, tmp_path: Path) -> None:
        """Test scanner handles OSError gracefully."""
        scanner = VideoScanner(
            search_dir=str(tmp_path),
            size_mb=0.001,
            output_file=None,
            size_unit=constants.SIZE_UNIT_MB,
            no_size=False,
            no_table=False,
            verbose=True,
        )
        scanner.exclude_folders_abs = []
        # Create a video file that we'll make unreadable
        shutil.copyfile(VIDEO_FIXTURES_DIR / "large_2k.mp4", tmp_path / "large.mp4")
        # Make file unreadable
        try:
            (tmp_path / "large.mp4").chmod(0o000)
            scanner.scan()
        except Exception:
            pass
        finally:
            # Restore permissions for cleanup
            try:
                (tmp_path / "large.mp4").chmod(0o644)
            except Exception:
                pass
