"""Entry point for running the package as a module."""

import sys
from .files.cli import main as files_main
from .dirs.cli import main as dirs_main
from .videos.cli import main as videos_main
from . import formatting

def show_usage():
    """Show usage information."""
    formatting.print_ascii_art("files")
    help_message = """
Usage: python -m find_large <command> [options]

Commands:
    files   Find large files in a directory
    dirs    Find large directories
    vids    Find large video files

Run 'python -m find_large <command> --help' for command-specific options.

Examples:
    python -m find_large files -d /path/to/search -S 1
    python -m find_large dirs -d /path/to/search -s 500
    python -m find_large vids -d /path/to/search -S 2
"""
    formatting.console.print(help_message)
    sys.exit(1)

def main():
    """Main entry point when running as a module."""
    if len(sys.argv) < 2:
        show_usage()
        return

    command = sys.argv[1]
    # Remove the command from argv so the individual CLI handlers work correctly
    sys.argv.pop(1)

    if command == "files":
        files_main()
    elif command == "dirs":
        dirs_main()
    elif command == "vids":
        videos_main()
    else:
        show_usage()

if __name__ == '__main__':
    main() 