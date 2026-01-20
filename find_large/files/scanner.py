"""File scanner implementation."""

import logging
import os

from find_large.core import SizeScannerBase


class FileScanner(SizeScannerBase):
    """Scanner for finding large files."""

    def scan(self) -> None:
        """Scan for large files."""
        try:
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
                if self.verbose:
                    logging.debug(
                        f"Filtered out {original_dirs_count - len(dirs)} hidden directories"
                    )

                # Process files
                for filename in files:
                    if filename.startswith("."):
                        continue
                    file_path = os.path.join(root, filename)
                    try:
                        size_bytes = os.path.getsize(file_path)
                        if size_bytes >= self.size_bytes_threshold:
                            if self.verbose:
                                logging.debug(
                                    f"Found large file: {file_path} "
                                    f"({size_bytes / self.MB_TO_BYTES:.2f} MB)"
                                )
                            self.items_list.append((file_path, size_bytes))
                            self.total_bytes += size_bytes
                    except (OSError, FileNotFoundError) as e:
                        if self.verbose:
                            logging.debug(f"Could not access file {file_path}: {str(e)}")
                        continue
        except Exception as e:
            self.error_exit(f"An error occurred during file search: {e}")
