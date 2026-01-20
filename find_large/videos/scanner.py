"""Video scanner implementation."""

import logging
import os

from find_large.core import SizeScannerBase


class VideoScanner(SizeScannerBase):
    """Scanner for finding large video files."""

    VIDEO_EXTENSIONS: set[str] = {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".mpg",
        ".mpeg",
        ".3gp",
        ".3g2",
        ".m2ts",
        ".mts",
        ".ts",
        ".vob",
        ".ogv",
        ".rm",
        ".rmvb",
        ".asf",
        ".divx",
    }

    def is_video_file(self, filename: str) -> bool:
        """Check if a file is a video file based on its extension.

        Args:
            filename: Name of the file to check.

        Returns:
            bool: True if the file has a video extension, False otherwise.
        """
        return os.path.splitext(filename)[1].lower() in self.VIDEO_EXTENSIONS

    def scan(self) -> None:
        """Scan for large video files."""
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

                # Process video files
                for filename in files:
                    if filename.startswith(".") or not self.is_video_file(filename):
                        continue
                    file_path = os.path.join(root, filename)
                    try:
                        size_bytes = os.path.getsize(file_path)
                        if size_bytes >= self.size_bytes_threshold:
                            if self.verbose:
                                logging.debug(
                                    f"Found large video: {file_path} "
                                    f"({size_bytes / self.MB_TO_BYTES:.2f} MB)"
                                )
                            self.items_list.append((file_path, size_bytes))
                            self.total_bytes += size_bytes
                    except (OSError, FileNotFoundError) as e:
                        if self.verbose:
                            logging.debug(f"Could not access file {file_path}: {str(e)}")
                        continue
        except Exception as e:
            self.error_exit(f"An error occurred during video search: {e}")
