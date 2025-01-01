"""Command-line interface for finding large video files."""

import os
import sys
import argparse
from .. import formatting
from ..constants import (
    DEFAULT_DIR,
    DEFAULT_SIZE_GB,
    DEFAULT_SIZE_MB,
    SIZE_UNIT_GB,
    SIZE_UNIT_MB,
)
from .core import find_large_videos, VIDEO_EXTENSIONS

def get_program_name():
    """Get the program name to display in help."""
    if sys.argv[0].endswith('__main__.py'):
        return 'find-large vids'
    return 'find-large-vids'

def show_help(prog_name):
    """Display help message."""
    # Show ASCII art banner first
    formatting.print_ascii_art("vids")
    
    help_message = f"""
Usage: {prog_name} [OPTIONS]

Options:
  File Search Options:
    -d,  --directory DIRECTORY    Directory to search (default: current directory)
    -S,  --size-in-gb SIZE        Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)
    -s,  --size-in-mb SIZE        Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)

  Output Options:
    -o,  --output FILE            Save results to specified file
    -n,  --no-size                Display videos without their sizes
    -nt, --no-table               Output in plain text format (one video per line)
    -v,  --verbose                Enable verbose output showing search progress

  Help:
    -h,  --help                   Show this help message

Supported Video Formats:
    {', '.join(sorted(ext[1:] for ext in VIDEO_EXTENSIONS))}

Examples:
  Search for videos larger than 5GB and save results:
    {prog_name} -d /path/to/search -S 5 -o results.txt

  Search for videos larger than 300MB:
    {prog_name} --directory /path/to/search --size-in-mb 300

  List videos larger than 500MB without sizes:
    {prog_name} -d /path/to/search -s 500 -n

  Output as plain text with verbose logging:
    {prog_name} -d /path/to/search -s 500 -nt -v
"""
    formatting.console.print(help_message)

def main():
    """Main entry point for the command-line interface."""
    try:
        prog_name = get_program_name()
        parser = argparse.ArgumentParser(
            prog=prog_name,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter,
        )

        # File Search Options
        search_group = parser.add_argument_group('File Search Options')
        search_group.add_argument('-d', '--directory', metavar='DIRECTORY',
                          help='Directory to search (default: current directory)',
                          default=DEFAULT_DIR)
        search_group.add_argument('-S', '--size-in-gb', metavar='SIZE', type=float,
                          help=f'Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)')
        search_group.add_argument('-s', '--size-in-mb', metavar='SIZE', type=float,
                          help=f'Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)')

        # Output Options
        output_group = parser.add_argument_group('Output Options')
        output_group.add_argument('-o', '--output', metavar='FILE',
                          help='Save results to specified file')
        output_group.add_argument('-n', '--no-size', action='store_true',
                          help='Display videos without their sizes')
        output_group.add_argument('-nt', '--no-table', action='store_true',
                          help='Output in plain text format (one video per line)')
        output_group.add_argument('-v', '--verbose', action='store_true',
                          help='Enable verbose output')

        # Help Option
        parser.add_argument('-h', '--help', action='store_true', help=argparse.SUPPRESS)

        args, unknown = parser.parse_known_args()

        if args.help:
            show_help(prog_name)
            sys.exit(0)

        search_dir = args.directory
        size_gb = args.size_in_gb
        size_mb = args.size_in_mb
        output_file = args.output

        if size_gb is not None and size_mb is not None:
            formatting.print_error("You cannot use both --size-in-gb and --size-in-mb at the same time.")
            sys.exit(1)

        if size_gb is not None:
            size_mb = size_gb * 1024
            size_unit = SIZE_UNIT_GB
        elif size_mb is not None:
            size_mb = size_mb
            size_unit = SIZE_UNIT_MB
        else:
            size_mb = DEFAULT_SIZE_GB * 1024
            size_unit = SIZE_UNIT_GB

        if not os.path.isdir(search_dir):
            formatting.print_error(f"Directory '{search_dir}' does not exist or is not accessible.")
            sys.exit(1)

        # Show ASCII art banner
        formatting.print_ascii_art()
        
        if size_unit == SIZE_UNIT_GB:
            size_display = f"{size_mb/1024:.1f} {SIZE_UNIT_GB}"
        else:
            size_display = f"{size_mb:.0f} {SIZE_UNIT_MB}"
            
        formatting.print_status(f"Searching for videos larger than {size_display} in {search_dir}...\n")

        with formatting.get_status_context("Searching..."):
            find_large_videos(search_dir, size_mb, output_file, size_unit,
                            args.no_size, args.no_table, args.verbose)

    except KeyboardInterrupt:
        formatting.print_error("\nSearch interrupted by user.")
        sys.exit(0)

if __name__ == '__main__':
    main() 