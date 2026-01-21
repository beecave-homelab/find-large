"""End-to-end tests for files CLI entry point."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from find_large.files.cli import main, scan_files


class TestFilesCLIEntryPoints:
    """Test cases for files CLI entry point."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner for testing.

        Returns:
            CliRunner: Click test runner instance.
        """
        return CliRunner()

    def test_main_help_displays_help(self, runner: CliRunner) -> None:
        """Test main command displays help text."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output

    def test_main_runs_successfully(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command runs successfully."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-s", "1"])
        assert result.exit_code == 0

    def test_main_with_gb_size(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command with GB size option."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-S", "1"])
        assert result.exit_code == 0

    def test_main_with_output_file(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command saves results to file."""
        output_file = tmp_path / "output.txt"
        result = runner.invoke(main, ["-d", str(tmp_path), "-s", "1", "-o", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_main_no_size_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command with no-size flag."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-s", "1", "-n"])
        assert result.exit_code == 0

    def test_main_no_table_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command with no-table flag."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-s", "1", "-nt"])
        assert result.exit_code == 0

    def test_main_verbose_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command with verbose flag."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-s", "1", "-v"])
        assert result.exit_code == 0

    def test_main_rejects_invalid_directory(self, runner: CliRunner) -> None:
        """Test main command rejects invalid directory."""
        result = runner.invoke(main, ["-d", "/nonexistent", "-s", "1"])
        assert result.exit_code != 0

    def test_main_rejects_both_size_options(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test main command rejects both size options."""
        result = runner.invoke(main, ["-d", str(tmp_path), "-S", "1", "-s", "500"])
        assert result.exit_code != 0


class TestScanFilesFunction:
    """Test cases for scan_files function."""

    def test_scan_files_with_gb_size(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files with GB size option."""
        scan_files(str(tmp_path), 1.0, None, None, False, False, False)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out

    def test_scan_files_with_mb_size(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files with MB size option."""
        scan_files(str(tmp_path), None, 500, None, False, False, False)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out

    def test_scan_files_defaults_to_gb(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files defaults to GB when no size specified."""
        scan_files(str(tmp_path), None, None, None, False, False, False)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out

    def test_scan_files_raises_on_both_size_options(self, tmp_path: Path) -> None:
        """Test scan_files raises error when both size options provided."""
        with pytest.raises(Exception):
            scan_files(str(tmp_path), 1.0, 500, None, False, False, False)

    def test_scan_files_raises_on_invalid_directory(self, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files raises error on invalid directory."""
        with pytest.raises(Exception):
            scan_files("/nonexistent", None, None, None, False, False, False)

    def test_scan_files_with_output_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test scan_files with output file."""
        output_file = tmp_path / "output.txt"
        scan_files(str(tmp_path), None, 1, str(output_file), False, False, False)
        assert output_file.exists()

    def test_scan_files_no_size_flag(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files with no-size flag."""
        scan_files(str(tmp_path), None, 1, None, True, False, False)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out

    def test_scan_files_no_table_flag(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files with no-table flag."""
        scan_files(str(tmp_path), None, 1, None, False, True, False)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out

    def test_scan_files_verbose_flag(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test scan_files with verbose flag."""
        scan_files(str(tmp_path), None, 1, None, False, False, True)
        captured = capsys.readouterr()
        assert "Searching for files larger than" in captured.out
