"""Core functionality for finding large directories."""

import os
import sys
import logging
from .. import formatting
from ..constants import (
    MB_TO_BYTES,
    GB_TO_BYTES,
    EXCLUDE_FOLDERS,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)

def get_dir_size(path, verbose=False):
    """Calculate total size of a directory."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except (OSError, FileNotFoundError) as e:
                    if verbose:
                        logging.debug(f"Could not access file {fp}: {str(e)}")
                    continue
    except Exception as e:
        if verbose:
            logging.debug(f"Error accessing directory {path}: {str(e)}")
        return 0
    return total_size

def find_large_dirs(search_dir, size_mb, output_file, size_unit, no_size=False, no_table=False, verbose=False):
    """Main function to find large directories."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    dirs_list = []
    total_bytes = 0
    size_bytes_threshold = size_mb * MB_TO_BYTES

    if verbose:
        logging.debug(f"Starting search in directory: {search_dir}")
        logging.debug(f"Size threshold: {size_mb} MB ({size_bytes_threshold} bytes)")

    exclude_folders_abs = [os.path.abspath(folder) for folder in EXCLUDE_FOLDERS]

    try:
        for root, dirs, _ in os.walk(search_dir):
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
            
            # Calculate directory size
            dir_size = get_dir_size(abs_root, verbose)
            if dir_size >= size_bytes_threshold:
                if verbose:
                    logging.debug(f"Found large directory: {abs_root} ({dir_size / MB_TO_BYTES:.2f} MB)")
                dirs_list.append((abs_root, dir_size))
                
    except Exception as e:
        formatting.print_error(f"An error occurred during directory search: {e}")
        sys.exit(1)

    if verbose:
        logging.debug(f"Search completed. Found {len(dirs_list)} directories matching criteria.")

    if no_size:
        data_lines = [("Directory Location",)]
    else:
        data_lines = [("Directory Location", "Total Size")]

    for dir_path, size_bytes in sorted(dirs_list, key=lambda x: x[1], reverse=True):
        total_bytes += size_bytes
        if no_size:
            data_lines.append((dir_path,))
        else:
            if size_unit == SIZE_UNIT_GB:
                size = size_bytes / GB_TO_BYTES
                size_label = SIZE_UNIT_GB
            else:
                size = size_bytes / MB_TO_BYTES
                size_label = SIZE_UNIT_MB
            size_formatted = f"{size:.2f} {size_label}"
            data_lines.append((dir_path, size_formatted))

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