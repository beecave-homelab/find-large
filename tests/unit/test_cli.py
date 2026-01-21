"""Unit tests for CLI module."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from find_large import constants
from find_large.cli import cli, validate_directory, validate_size_options


class TestValidateSizeOptions:
    """Test cases for validate_size_options function."""

    def test_validate_size_options__with_gb(self) -> None:
        """Test validation with GB size option."""
        size_mb, size_unit = validate_size_options(size_gb=2.0, size_mb=None)
        assert size_mb == 2048.0
        assert size_unit == constants.SIZE_UNIT_GB

    def test_validate_size_options__with_mb(self) -> None:
        """Test validation with MB size option."""
        size_mb, size_unit = validate_size_options(size_gb=None, size_mb=500)
        assert size_mb == 500
        assert size_unit == constants.SIZE_UNIT_MB

    def test_validate_size_options__defaults_to_gb(self) -> None:
        """Test validation defaults to GB when no size specified."""
        size_mb, size_unit = validate_size_options(size_gb=None, size_mb=None)
        assert size_mb == constants.DEFAULT_SIZE_GB * 1024
        assert size_unit == constants.SIZE_UNIT_GB

    def test_validate_size_options__raises_on_both_options(self) -> None:
        """Test validation raises error when both options provided."""
        with pytest.raises(Exception):
            validate_size_options(size_gb=1.0, size_mb=500)

    def test_validate_size_options__raises_on_negative_gb(self) -> None:
        """Test validation raises error on negative GB."""
        with pytest.raises(Exception):
            validate_size_options(size_gb=-1.0, size_mb=None)

    def test_validate_size_options__raises_on_zero_gb(self) -> None:
        """Test validation raises error on zero GB."""
        with pytest.raises(Exception):
            validate_size_options(size_gb=0.0, size_mb=None)

    def test_validate_size_options__raises_on_negative_mb(self) -> None:
        """Test validation raises error on negative MB."""
        with pytest.raises(Exception):
            validate_size_options(size_gb=None, size_mb=-100)


class TestValidateDirectory:
    """Test cases for validate_directory function."""

    def test_validate_directory__accepts_existing_directory(self, tmp_path: Path) -> None:
        """Test validation accepts existing directory."""
        validate_directory(str(tmp_path))

    def test_validate_directory__raises_on_missing_directory(self) -> None:
        """Test validation raises error on missing directory."""
        with pytest.raises(Exception):
            validate_directory("/nonexistent/directory")

    def test_validate_directory__raises_on_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Test validation raises error when path is a file."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")
        with pytest.raises(Exception):
            validate_directory(str(file_path))


class TestCLICommands:
    """Test cases for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner for testing.

        Returns:
            CliRunner: Click CLI runner instance.
        """
        return CliRunner()

    def test_cli_help__displays_help(self, runner: CliRunner) -> None:
        """Test CLI help displays help text."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Commands:" in result.output

    def test_cli_files_help__displays_help(self, runner: CliRunner) -> None:
        """Test files command help displays help text."""
        result = runner.invoke(cli, ["files", "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output

    def test_cli_dirs_help__displays_help(self, runner: CliRunner) -> None:
        """Test dirs command help displays help text."""
        result = runner.invoke(cli, ["dirs", "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output

    def test_cli_vids_help__displays_help(self, runner: CliRunner) -> None:
        """Test vids command help displays help text."""
        result = runner.invoke(cli, ["vids", "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output

    def test_cli_files__runs_successfully(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command runs successfully."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-s", "1"])
        assert result.exit_code == 0

    def test_cli_files__with_gb_size(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command with GB size option."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-S", "1"])
        assert result.exit_code == 0

    def test_cli_files__with_output_file(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command saves results to file."""
        output_file = tmp_path / "output.txt"
        result = runner.invoke(
            cli, ["files", "-d", str(tmp_path), "-s", "1", "-o", str(output_file)]
        )
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_files__no_size_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command with no-size flag."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-s", "1", "-n"])
        assert result.exit_code == 0

    def test_cli_files__no_table_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command with no-table flag."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-s", "1", "-nt"])
        assert result.exit_code == 0

    def test_cli_files__verbose_flag(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command with verbose flag."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-s", "1", "-v"])
        assert result.exit_code == 0

    def test_cli_dirs__runs_successfully(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test dirs command runs successfully."""
        result = runner.invoke(cli, ["dirs", "-d", str(tmp_path), "-s", "1"])
        assert result.exit_code == 0

    def test_cli_dirs__with_output_file(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test dirs command saves results to file."""
        output_file = tmp_path / "output.txt"
        result = runner.invoke(
            cli, ["dirs", "-d", str(tmp_path), "-s", "1", "-o", str(output_file)]
        )
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_vids__runs_successfully(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test vids command runs successfully."""
        result = runner.invoke(cli, ["vids", "-d", str(tmp_path), "-s", "1"])
        assert result.exit_code == 0

    def test_cli_vids__with_output_file(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test vids command saves results to file."""
        output_file = tmp_path / "output.txt"
        result = runner.invoke(
            cli, ["vids", "-d", str(tmp_path), "-s", "1", "-o", str(output_file)]
        )
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_files__rejects_invalid_directory(self, runner: CliRunner) -> None:
        """Test files command rejects invalid directory."""
        result = runner.invoke(cli, ["files", "-d", "/nonexistent", "-s", "1"])
        assert result.exit_code != 0

    def test_cli_files__rejects_both_size_options(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command rejects both size options."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-S", "1", "-s", "500"])
        assert result.exit_code != 0

    def test_cli_files__rejects_negative_size(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test files command rejects negative size."""
        result = runner.invoke(cli, ["files", "-d", str(tmp_path), "-s", "-100"])
        assert result.exit_code != 0


class TestAsciiArtHelp:
    """Test cases for ASCII art help classes."""

    def test_cli_help__contains_ascii_art(self) -> None:
        """Test CLI help contains ASCII art."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert "╔═╗╦╔╗╔╔╦╗" in result.output

    def test_files_help__contains_ascii_art(self) -> None:
        """Test files help contains ASCII art."""
        runner = CliRunner()
        result = runner.invoke(cli, ["files", "--help"])
        assert "╔═╗╦╔╗╔╔╦╗" in result.output

    def test_dirs_help__contains_ascii_art(self) -> None:
        """Test dirs help contains ASCII art."""
        runner = CliRunner()
        result = runner.invoke(cli, ["dirs", "--help"])
        assert "╔═╗╦╔╗╔╔╦╗" in result.output

    def test_vids_help__contains_ascii_art(self) -> None:
        """Test vids help contains ASCII art."""
        runner = CliRunner()
        result = runner.invoke(cli, ["vids", "--help"])
        assert "╔═╗╦╔╗╔╔╦╗" in result.output
