"""Core functionality for finding large items."""

import logging
import os
import sys
from pathlib import Path

from rich.console import Console

from find_large import formatting
from find_large.constants import (
    EXCLUDE_FOLDERS,
    GB_TO_BYTES,
    INCLUDE_HIDDEN_FOLDERS,
    MB_TO_BYTES,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)


class SizeScannerBase:
    """Base class for scanning items by size."""

    def __init__(
        self,
        search_dir: str | Path,
        size_mb: float,
        output_file: str | None,
        size_unit: str,
        no_size: bool = False,
        no_table: bool = False,
        verbose: bool = False,
    ) -> None:
        """Initialize the scanner."""
        self.search_dir = str(search_dir)
        self.size_mb = size_mb
        self.output_file = output_file
        self.size_unit = size_unit
        self.no_size = no_size
        self.no_table = no_table
        self.verbose = verbose
        self.size_bytes_threshold = int(size_mb * MB_TO_BYTES)
        self.items_list: list[tuple[str, int]] = []
        self.total_bytes: int = 0
        self.exclude_folders_abs = [os.path.abspath(folder) for folder in EXCLUDE_FOLDERS]
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure logging based on verbosity level."""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=log_level, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S")

    def error_exit(self, message: str) -> None:
        """Exit the program with an error message."""
        formatting.print_error(message)
        sys.exit(1)

    def should_skip_path(self, path: str) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check.

        Returns:
            bool: True if path should be skipped, False otherwise.
        """
        basename = os.path.basename(path)
        if basename.startswith(".") and basename not in INCLUDE_HIDDEN_FOLDERS:
            return True

        abs_path = os.path.abspath(path)
        for exclude_path in self.exclude_folders_abs:
            if abs_path.startswith(exclude_path):
                if self.verbose:
                    logging.debug(f"Skipping excluded path: {abs_path}")
                return True
        return False

    def format_size(self, size_bytes: int) -> str:
        """Format size in appropriate units.

        Args:
            size_bytes: Size in bytes.

        Returns:
            str: Formatted size string with unit.
        """
        if self.size_unit == SIZE_UNIT_GB:
            size = size_bytes / GB_TO_BYTES
            size_label = SIZE_UNIT_GB
        else:
            size = size_bytes / MB_TO_BYTES
            size_label = SIZE_UNIT_MB
        return f"{size:.2f} {size_label}"

    def save_results(self, data_lines: list[tuple[str, ...]]) -> None:
        """Save results to file if output file is specified."""
        if self.output_file:
            try:
                file_console: Console = formatting.Console(
                    file=open(self.output_file, "w"), force_terminal=True
                )
                formatting.format_table(
                    data_lines, self.no_size, self.total_bytes, file_console, self.no_table
                )
                file_console.file.close()
                formatting.print_success(f"Results saved to {self.output_file}")
            except Exception as e:
                self.error_exit(f"An error occurred while writing to the output file: {e}")
        else:
            formatting.format_table(
                data_lines, self.no_size, self.total_bytes, no_table=self.no_table
            )

    def format_results(self) -> list[tuple[str, ...]]:
        """Format results for display.

        Returns:
            list[tuple[str, ...]]: Formatted data lines for display.
        """
        if self.no_size:
            data_lines: list[tuple[str, ...]] = [("Location",)]
        else:
            data_lines = [("Location", "Size")]

        for item_path, size_bytes in self.items_list:
            if self.no_size:
                data_lines.append((item_path,))
            else:
                size_formatted = self.format_size(size_bytes)
                data_lines.append((item_path, size_formatted))

        return data_lines

    def scan(self) -> None:
        """Scan for items. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement scan()")

    def run(self) -> None:
        """Run the scanner and display results."""
        if self.verbose:
            logging.debug(f"Starting search in directory: {self.search_dir}")
            logging.debug(f"Size threshold: {self.size_mb} MB ({self.size_bytes_threshold} bytes)")
            logging.debug(f"Excluded folders: {len(EXCLUDE_FOLDERS)}")

        try:
            self.scan()
            if self.verbose:
                logging.debug(
                    f"Search completed. Found {len(self.items_list)} items matching criteria."
                )
            data_lines = self.format_results()
            self.save_results(data_lines)
        except Exception as e:
            self.error_exit(f"An error occurred during search: {e}")
