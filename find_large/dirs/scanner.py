"""Directory scanner implementation."""

import os
import logging
from typing import Dict

from ..core import SizeScannerBase

class DirectoryScanner(SizeScannerBase):
    """Scanner for finding large directories."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the directory scanner."""
        super().__init__(*args, **kwargs)
        self.dir_sizes: Dict[str, int] = {}

    def scan(self) -> None:
        """Scan for large directories."""
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
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                if self.verbose and original_dirs_count != len(dirs):
                    logging.debug(f"Filtered out {original_dirs_count - len(dirs)} hidden directories")
                
                # Calculate directory size
                dir_size = 0
                for filename in files:
                    if filename.startswith('.'):
                        continue
                    file_path = os.path.join(root, filename)
                    try:
                        size_bytes = os.path.getsize(file_path)
                        dir_size += size_bytes
                    except (OSError, FileNotFoundError) as e:
                        if self.verbose:
                            logging.debug(f"Could not access file {file_path}: {str(e)}")
                        continue

                # Store directory size
                self.dir_sizes[root] = dir_size

                # Add directory to results if it meets size threshold
                if dir_size >= self.size_bytes_threshold:
                    if self.verbose:
                        logging.debug(f"Found large directory: {root} ({dir_size / self.MB_TO_BYTES:.2f} MB)")
                    self.items_list.append((root, dir_size))
                    self.total_bytes += dir_size

        except Exception as e:
            self.error_exit(f"An error occurred during directory search: {e}") 