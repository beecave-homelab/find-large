"""Core functionality for finding large files."""

import logging
import os
import sys
from pathlib import Path

from rich.console import Console

from find_large import formatting
from find_large.constants import (
    EXCLUDE_FOLDERS,
    GB_TO_BYTES,
    MB_TO_BYTES,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)


def error_exit(message: str) -> None:
    """Exit the program with an error message."""
    formatting.print_error(message)
    sys.exit(1)


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S")


def find_files(
    search_dir: str | Path,
    size_mb: float,
    output_file: str | None,
    size_unit: str,
    no_size: bool = False,
    no_table: bool = False,
    verbose: bool = False,
) -> None:
    """Main function to find large files in a directory."""
    setup_logging(verbose)

    files_list: list[tuple[str, int]] = []
    total_bytes: int = 0
    size_bytes_threshold: int = int(size_mb * MB_TO_BYTES)

    if verbose:
        logging.debug(f"Starting search in directory: {search_dir}")
        logging.debug(f"Size threshold: {size_mb} MB ({size_bytes_threshold} bytes)")
        logging.debug(f"Excluded folders: {len(EXCLUDE_FOLDERS)}")

    exclude_folders_abs: list[str] = [os.path.abspath(folder) for folder in EXCLUDE_FOLDERS]

    try:
        for root, dirs, files in os.walk(str(search_dir)):
            if verbose:
                logging.debug(f"Scanning directory: {root}")

            abs_root: str = os.path.abspath(root)
            skip_dir: bool = False
            for exclude_path in exclude_folders_abs:
                if abs_root.startswith(exclude_path):
                    if verbose:
                        logging.debug(f"Skipping excluded directory: {abs_root}")
                    skip_dir = True
                    break
            if skip_dir:
                dirs[:] = []
                continue

            original_dirs_count: int = len(dirs)
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if verbose and original_dirs_count != len(dirs):
                logging.debug(f"Filtered out {original_dirs_count - len(dirs)} hidden directories")

            for filename in files:
                if filename.startswith("."):
                    continue
                file_path: str = os.path.join(root, filename)
                try:
                    size_bytes: int = os.path.getsize(file_path)
                    if size_bytes >= size_bytes_threshold:
                        if verbose:
                            logging.debug(
                                f"Found large file: {file_path} ({size_bytes / MB_TO_BYTES:.2f} MB)"
                            )
                        files_list.append((file_path, size_bytes))
                except (OSError, FileNotFoundError) as e:
                    if verbose:
                        logging.debug(f"Could not access file {file_path}: {str(e)}")
                    continue
    except Exception as e:
        error_exit(f"An error occurred during file search: {e}")

    if verbose:
        logging.debug(f"Search completed. Found {len(files_list)} files matching criteria.")

    if no_size:
        data_lines: list[tuple[str, ...]] = [("File Location",)]
    else:
        data_lines: list[tuple[str, str]] = [("File Location", "File Size")]

    for file_path, size_bytes in files_list:
        total_bytes += size_bytes
        if no_size:
            data_lines.append((file_path,))
        else:
            if size_unit == SIZE_UNIT_GB:
                size: float = size_bytes / GB_TO_BYTES
                size_label: str = SIZE_UNIT_GB
            else:
                size = size_bytes / MB_TO_BYTES
                size_label = SIZE_UNIT_MB
            size_formatted: str = f"{size:.2f} {size_label}"
            data_lines.append((file_path, size_formatted))

    if output_file:
        try:
            file_console: Console = formatting.Console(
                file=open(output_file, "w"), force_terminal=True
            )
            formatting.format_table(data_lines, no_size, total_bytes, file_console, no_table)
            file_console.file.close()
            formatting.print_success(f"Results saved to {output_file}")
        except Exception as e:
            error_exit(f"An error occurred while writing to the output file: {e}")
    else:
        formatting.format_table(data_lines, no_size, total_bytes, no_table=no_table)
