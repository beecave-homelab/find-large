"""Command-line interface for finding large files."""

import os
from pathlib import Path

import click

from find_large import formatting
from find_large.constants import (
    DEFAULT_DIR,
    DEFAULT_SIZE_GB,
    DEFAULT_SIZE_MB,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)
from find_large.files.core import find_files


def scan_files(
    directory: str | Path,
    size_gb: float | None,
    size_mb: float | None,
    output_file: str | None,
    no_size: bool,
    no_table: bool,
    verbose: bool,
) -> None:
    """Core function to handle file scanning logic.

    Args:
        directory: Directory to scan.
        size_gb: Size threshold in GB.
        size_mb: Size threshold in MB.
        output_file: Output file path.
        no_size: Hide size column.
        no_table: Use plain text output.
        verbose: Enable verbose output.

    Raises:
        click.Abort: If validation fails.
    """
    if size_gb is not None and size_mb is not None:
        formatting.print_error(
            "You cannot use both --size-in-gb and --size-in-mb at the same time."
        )
        raise click.Abort()

    if size_gb is not None:
        size_mb = size_gb * 1024
        size_unit = SIZE_UNIT_GB
    elif size_mb is not None:
        size_unit = SIZE_UNIT_MB
    else:
        size_mb = DEFAULT_SIZE_GB * 1024
        size_unit = SIZE_UNIT_GB

    if not os.path.isdir(directory):
        formatting.print_error(f"Directory '{directory}' does not exist or is not accessible.")
        raise click.Abort()

    if size_unit == SIZE_UNIT_GB:
        size_display: str = f"{size_mb / 1024:.1f} {SIZE_UNIT_GB}"
    else:
        size_display: str = f"{size_mb:.0f} {SIZE_UNIT_MB}"

    formatting.print_status(f"Searching for files larger than {size_display} in {directory}...\n")

    with formatting.get_status_context("Searching..."):
        find_files(directory, size_mb, output_file, size_unit, no_size, no_table, verbose)


@click.command()
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
def main(
    directory: str | Path,
    size_gb: float | None,
    size_mb: float | None,
    output_file: str | None,
    no_size: bool,
    no_table: bool,
    verbose: bool,
) -> None:
    r"""Find large files in a directory.

    Examples:
    \b
        find-large files -d /path/to/search -S 1
        find-large files -d /path/to/search -s 500 -o results.txt
        find-large files -d /path/to/search -s 500 -n -nt -v
    """
    scan_files(directory, size_gb, size_mb, output_file, no_size, no_table, verbose)


if __name__ == "__main__":
    main()
