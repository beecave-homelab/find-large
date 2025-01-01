"""Core functionality for finding large video files."""

import os
import sys
import logging
from .. import formatting
from ..constants import (
    DEFAULT_DIR,
    MB_TO_BYTES,
    GB_TO_BYTES,
    EXCLUDE_FOLDERS,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)

# Common video file extensions
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
    '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.m2ts', '.mts',
    '.ts', '.vob', '.ogv', '.rm', '.rmvb', '.asf', '.divx'
}

def is_video_file(filename):
    """Check if a file is a video file based on its extension."""
    return os.path.splitext(filename)[1].lower() in VIDEO_EXTENSIONS

def find_large_videos(search_dir, size_mb, output_file, size_unit, no_size=False, no_table=False, verbose=False):
    """Main function to find large video files."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    videos_list = []
    total_bytes = 0
    size_bytes_threshold = size_mb * MB_TO_BYTES

    if verbose:
        logging.debug(f"Starting search in directory: {search_dir}")
        logging.debug(f"Size threshold: {size_mb} MB ({size_bytes_threshold} bytes)")
        logging.debug(f"Searching for video extensions: {', '.join(sorted(VIDEO_EXTENSIONS))}")

    exclude_folders_abs = [os.path.abspath(folder) for folder in EXCLUDE_FOLDERS]

    try:
        for root, dirs, files in os.walk(search_dir):
            if verbose:
                logging.debug(f"Scanning directory: {root}")
            
            abs_root = os.path.abspath(root)
            skip_dir = False
            for exclude_path in exclude_folders_abs:
                if abs_root.startswith(exclude_path):
                    if verbose:
                        logging.debug(f"Skipping excluded directory: {abs_root}")
                    skip_dir = True
                    break
            if skip_dir:
                dirs[:] = []
                continue

            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                    
                if not is_video_file(filename):
                    continue
                    
                file_path = os.path.join(root, filename)
                try:
                    size_bytes = os.path.getsize(file_path)
                    if size_bytes >= size_bytes_threshold:
                        if verbose:
                            logging.debug(f"Found large video: {file_path} ({size_bytes / MB_TO_BYTES:.2f} MB)")
                        videos_list.append((file_path, size_bytes))
                except (OSError, FileNotFoundError) as e:
                    if verbose:
                        logging.debug(f"Could not access file {file_path}: {str(e)}")
                    continue
    except Exception as e:
        formatting.print_error(f"An error occurred during video search: {e}")
        sys.exit(1)

    if verbose:
        logging.debug(f"Search completed. Found {len(videos_list)} videos matching criteria.")

    if no_size:
        data_lines = [("Video Location",)]
    else:
        data_lines = [("Video Location", "File Size")]

    for video_path, size_bytes in sorted(videos_list, key=lambda x: x[1], reverse=True):
        total_bytes += size_bytes
        if no_size:
            data_lines.append((video_path,))
        else:
            if size_unit == SIZE_UNIT_GB:
                size = size_bytes / GB_TO_BYTES
                size_label = SIZE_UNIT_GB
            else:
                size = size_bytes / MB_TO_BYTES
                size_label = SIZE_UNIT_MB
            size_formatted = f"{size:.2f} {size_label}"
            data_lines.append((video_path, size_formatted))

    if output_file:
        try:
            file_console = formatting.Console(file=open(output_file, "w"), force_terminal=True)
            formatting.format_table(data_lines, no_size, total_bytes, file_console, no_table)
            file_console.file.close()
            formatting.print_success(f"Results saved to {output_file}")
        except Exception as e:
            formatting.print_error(f"An error occurred while writing to the output file: {e}")
            sys.exit(1)
    else:
        formatting.format_table(data_lines, no_size, total_bytes, no_table=no_table) 