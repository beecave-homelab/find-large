"""Directory scanner implementation."""

import logging
import os

from find_large.constants import MB_TO_BYTES
from find_large.core import SizeScannerBase


class DirectoryScanner(SizeScannerBase):
    """Scanner for finding large directories."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize the directory scanner."""
        super().__init__(*args, **kwargs)
        self.dir_sizes: dict[str, int] = {}

    def scan(self) -> None:
        """Scan for large directories."""
        try:
            self.dir_sizes = {}
            self.items_list = []
            self.total_bytes = 0

            for root, dirs, files in os.walk(self.search_dir):
                if self.verbose:
                    logging.debug(f"Scanning directory: {root}")

                # Skip excluded directories
                if self.should_skip_path(root):
                    dirs[:] = []
                    continue

                # Filter out hidden directories
                original_dirs_count = len(dirs)
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                if self.verbose and original_dirs_count != len(dirs):
                    logging.debug(
                        "Filtered out %s hidden directories",
                        original_dirs_count - len(dirs),
                    )

                # Calculate directory size for files directly under this directory
                dir_size = 0
                for filename in files:
                    if filename.startswith("."):
                        continue
                    file_path = os.path.join(root, filename)
                    try:
                        size_bytes = os.path.getsize(file_path)
                        dir_size += size_bytes
                    except (OSError, FileNotFoundError) as e:
                        if self.verbose:
                            logging.debug(
                                "Could not access file %s: %s",
                                file_path,
                                str(e),
                            )
                        continue

                # Store direct file size for this directory
                self.dir_sizes[root] = dir_size

            # Aggregate sizes from children to parents for recursive totals
            for path in sorted(
                self.dir_sizes.keys(),
                key=lambda p: p.count(os.sep),
                reverse=True,
            ):
                parent = os.path.dirname(path)
                if parent in self.dir_sizes:
                    self.dir_sizes[parent] += self.dir_sizes[path]

            # Add directories meeting size threshold
            for path, size_bytes in self.dir_sizes.items():
                if size_bytes >= self.size_bytes_threshold:
                    if self.verbose:
                        logging.debug(
                            "Found large directory: %s (%.2f MB)",
                            path,
                            size_bytes / MB_TO_BYTES,
                        )
                    self.items_list.append((path, size_bytes))

            self.total_bytes = self._calculate_total_bytes()

        except Exception as e:
            self.error_exit(f"An error occurred during directory search: {e}")

    def _calculate_total_bytes(self) -> int:
        """Calculate total size without double-counting nested directories.

        Returns:
            int: Total size in bytes for non-overlapping directories.
        """
        total_bytes = 0
        counted_paths: list[str] = []
        for dir_path, size_bytes in sorted(self.items_list, key=lambda item: item[0].count(os.sep)):
            abs_path = os.path.abspath(dir_path)
            if any(
                abs_path == parent or abs_path.startswith(parent + os.sep)
                for parent in counted_paths
            ):
                continue
            total_bytes += size_bytes
            counted_paths.append(abs_path)
        return total_bytes
