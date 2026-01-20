"""Command-line interface for find-large."""

from pathlib import Path

import click
from click import Context

from find_large import formatting
from find_large.constants import (
    DEFAULT_DIR,
    DEFAULT_SIZE_GB,
    DEFAULT_SIZE_MB,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)
from find_large.dirs.scanner import DirectoryScanner
from find_large.files.scanner import FileScanner
from find_large.videos.scanner import VideoScanner


class AsciiArtHelpGroup(click.Group):
    """Click group with ASCII art help."""

    def get_help(self, ctx: Context) -> str:
        """Get help text with ASCII art.

        Args:
            ctx: Click context.

        Returns:
            Formatted help text with ASCII art.
        """
        formatting.print_ascii_art()
        # Get the original help text
        help_text: str = super().get_help(ctx)

        # Style different sections
        help_text = help_text.replace("Usage:", click.style("Usage:", fg="green", bold=True))
        help_text = help_text.replace("Options:", click.style("Options:", fg="green", bold=True))
        help_text = help_text.replace("Commands:", click.style("Commands:", fg="green", bold=True))

        return help_text


class AsciiArtHelpCommand(click.Command):
    """Click command with ASCII art help."""

    def get_help(self, ctx: Context) -> str:
        """Get help text with ASCII art.

        Args:
            ctx: Click context.

        Returns:
            Formatted help text with ASCII art.
        """
        formatting.print_ascii_art(self.name)
        # Get the original help text
        help_text: str = super().get_help(ctx)

        # Style different sections
        help_text = help_text.replace("Usage:", click.style("Usage:", fg="green", bold=True))
        help_text = help_text.replace("Options:", click.style("Options:", fg="green", bold=True))
        help_text = help_text.replace("[Examples]", click.style("Examples:", fg="green", bold=True))

        # Style command descriptions
        lines: list[str] = help_text.split("\n")
        styled_lines: list[str] = []
        for line in lines:
            if line.strip().startswith("$"):
                # Style command examples
                styled_lines.append(click.style(line, fg="yellow"))
            elif (
                line.strip().startswith("Find ") or line.strip().startswith("List ")
            ) and ":" in line:
                # Style example descriptions
                styled_lines.append(click.style(line, fg="cyan"))
            else:
                styled_lines.append(line)

        return "\n".join(styled_lines)


def validate_size_options(size_gb: float | None, size_mb: float | None) -> tuple[float, str]:
    """Validate and process size options.

    Args:
        size_gb: Size threshold in GB.
        size_mb: Size threshold in MB.

    Returns:
        Tuple of (size_mb, size_unit).

    Raises:
        click.Abort: If both size options are provided.
    """
    if size_gb is not None and size_mb is not None:
        formatting.print_error(
            "You cannot use both --size-in-gb and --size-in-mb at the same time."
        )
        raise click.Abort()

    if size_gb is not None and size_gb <= 0:
        formatting.print_error("Size in GB must be greater than 0.")
        raise click.Abort()
    if size_mb is not None and size_mb <= 0:
        formatting.print_error("Size in MB must be greater than 0.")
        raise click.Abort()

    if size_gb is not None:
        size_mb = size_gb * 1024
        size_unit = SIZE_UNIT_GB
    elif size_mb is not None:
        size_unit = SIZE_UNIT_MB
    else:
        size_mb = DEFAULT_SIZE_GB * 1024
        size_unit = SIZE_UNIT_GB

    return size_mb, size_unit


def validate_directory(directory: str) -> None:
    """Validate directory exists and is accessible.

    Args:
        directory: Directory path to validate.

    Raises:
        click.Abort: If directory does not exist or is not accessible.
    """
    if not Path(directory).is_dir():
        formatting.print_error(f"Directory '{directory}' does not exist or is not accessible.")
        raise click.Abort()


@click.group(cls=AsciiArtHelpGroup)
def cli() -> None:
    """Find Large - A tool to search for large files, dirs or vids on a system.

    A command-line utility to help you identify space-consuming files and directories
    with options for different output formats and filtering.
    """
    pass


@cli.command(cls=AsciiArtHelpCommand)
@click.option(
    "-d",
    "--directory",
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default=DEFAULT_DIR,
    help="Directory to search (default: current directory)",
)
@click.option(
    "-S",
    "--size-in-gb",
    "size_gb",
    type=float,
    help=f"Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)",
)
@click.option(
    "-s",
    "--size-in-mb",
    "size_mb",
    type=float,
    help=f"Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)",
)
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(dir_okay=False, writable=True),
    help="Save results to specified file",
)
@click.option("-n", "--no-size", is_flag=True, help="Display files without their sizes")
@click.option(
    "-nt", "--no-table", is_flag=True, help="Output in plain text format (one file per line)"
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output showing search progress")
def files(
    directory: str,
    size_gb: float | None,
    size_mb: float | None,
    output_file: str | None,
    no_size: bool,
    no_table: bool,
    verbose: bool,
) -> None:
    r"""Find large files in a directory.

    Search for files larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find files larger than 1GB:
        $ python -m find_large files -d /path/to/search -S 1
        $ find-large files -d /path/to/search -S 1

    \b
    Find files larger than 500MB and save results:
        $ python -m find_large files -d /path/to/search -s 500 -o results.txt
        $ find-large files -d /path/to/search -s 500 -o results.txt

    \b
    List files without sizes in plain text format:
        $ python -m find_large files -d /path/to/search -s 500 -n -nt
        $ find-large files -d /path/to/search -s 500 -n -nt
    """
    validate_directory(directory)
    size_mb, size_unit = validate_size_options(size_gb, size_mb)
    scanner = FileScanner(directory, size_mb, output_file, size_unit, no_size, no_table, verbose)
    scanner.run()


@cli.command(cls=AsciiArtHelpCommand)
@click.option(
    "-d",
    "--directory",
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default=DEFAULT_DIR,
    help="Directory to search (default: current directory)",
)
@click.option(
    "-S",
    "--size-in-gb",
    "size_gb",
    type=float,
    help=f"Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)",
)
@click.option(
    "-s",
    "--size-in-mb",
    "size_mb",
    type=float,
    help=f"Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)",
)
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(dir_okay=False, writable=True),
    help="Save results to specified file",
)
@click.option("-n", "--no-size", is_flag=True, help="Display directories without their sizes")
@click.option(
    "-nt", "--no-table", is_flag=True, help="Output in plain text format (one directory per line)"
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output showing search progress")
def dirs(
    directory: str,
    size_gb: float | None,
    size_mb: float | None,
    output_file: str | None,
    no_size: bool,
    no_table: bool,
    verbose: bool,
) -> None:
    r"""Find large directories.

    Search for directories larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find directories larger than 1GB:
        $ python -m find_large dirs -d /path/to/search -S 1
        $ find-large dirs -d /path/to/search -S 1

    \b
    Find directories larger than 500MB and save results:
        $ python -m find_large dirs -d /path/to/search -s 500 -o results.txt
        $ find-large dirs -d /path/to/search -s 500 -o results.txt

    \b
    List directories without sizes in plain text format:
        $ python -m find_large dirs -d /path/to/search -s 500 -n -nt
        $ find-large dirs -d /path/to/search -s 500 -n -nt
    """
    validate_directory(directory)
    size_mb, size_unit = validate_size_options(size_gb, size_mb)
    scanner = DirectoryScanner(
        directory, size_mb, output_file, size_unit, no_size, no_table, verbose
    )
    scanner.run()


@cli.command(name="vids", cls=AsciiArtHelpCommand)
@click.option(
    "-d",
    "--directory",
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default=DEFAULT_DIR,
    help="Directory to search (default: current directory)",
)
@click.option(
    "-S",
    "--size-in-gb",
    "size_gb",
    type=float,
    help=f"Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)",
)
@click.option(
    "-s",
    "--size-in-mb",
    "size_mb",
    type=float,
    help=f"Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)",
)
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(dir_okay=False, writable=True),
    help="Save results to specified file",
)
@click.option("-n", "--no-size", is_flag=True, help="Display videos without their sizes")
@click.option(
    "-nt", "--no-table", is_flag=True, help="Output in plain text format (one video per line)"
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output showing search progress")
def videos(
    directory: str,
    size_gb: float | None,
    size_mb: float | None,
    output_file: str | None,
    no_size: bool,
    no_table: bool,
    verbose: bool,
) -> None:
    r"""Find large video files.

    Search for video files larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find videos larger than 1GB:
        $ python -m find_large vids -d /path/to/search -S 1
        $ find-large vids -d /path/to/search -S 1

    \b
    Find videos larger than 500MB and save results:
        $ python -m find_large vids -d /path/to/search -s 500 -o results.txt
        $ find-large vids -d /path/to/search -s 500 -o results.txt

    \b
    List videos without sizes in plain text format:
        $ python -m find_large vids -d /path/to/search -s 500 -n -nt
        $ find-large vids -d /path/to/search -s 500 -n -nt
    """
    validate_directory(directory)
    size_mb, size_unit = validate_size_options(size_gb, size_mb)
    scanner = VideoScanner(directory, size_mb, output_file, size_unit, no_size, no_table, verbose)
    scanner.run()


def main() -> None:
    """Main entry point when running as a module."""
    cli()
