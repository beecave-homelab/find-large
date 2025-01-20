"""Entry point for running the package as a module."""

import click
from .files.cli import main as files_main, scan_files
from .dirs.cli import main as dirs_main, scan_directories
from .videos.cli import main as videos_main, scan_videos
from . import formatting
from .constants import (
    DEFAULT_DIR,
    DEFAULT_SIZE_GB,
    DEFAULT_SIZE_MB,
)

class AsciiArtHelpGroup(click.Group):
    def get_help(self, ctx):
        formatting.print_ascii_art()
        # Get the original help text
        help_text = super().get_help(ctx)
        
        # Style different sections
        help_text = help_text.replace("Usage:", click.style("Usage:", fg="green", bold=True))
        help_text = help_text.replace("Options:", click.style("Options:", fg="green", bold=True))
        help_text = help_text.replace("Commands:", click.style("Commands:", fg="green", bold=True))
        
        return help_text

class AsciiArtHelpCommand(click.Command):
    def get_help(self, ctx):
        formatting.print_ascii_art(self.name)
        # Get the original help text
        help_text = super().get_help(ctx)
        
        # Style different sections
        help_text = help_text.replace("Usage:", click.style("Usage:", fg="green", bold=True))
        help_text = help_text.replace("Options:", click.style("Options:", fg="green", bold=True))
        help_text = help_text.replace("[Examples]", click.style("Examples:", fg="green", bold=True))
        
        # Style command descriptions
        lines = help_text.split('\n')
        styled_lines = []
        for line in lines:
            if line.strip().startswith('$'):
                # Style command examples
                styled_lines.append(click.style(line, fg='yellow'))
            elif (line.strip().startswith('Find ') or line.strip().startswith('List ')) and ':' in line:
                # Style example descriptions
                styled_lines.append(click.style(line, fg='cyan'))
            else:
                styled_lines.append(line)
        
        return '\n'.join(styled_lines)

@click.group(cls=AsciiArtHelpGroup)
def cli():
    """Find Large - A tool to search for large files, dirs or vids on a system.

    A command-line utility to help you identify space-consuming files and directories
    with options for different output formats and filtering.
    """
    pass

@cli.command(cls=AsciiArtHelpCommand)
@click.option('-d', '--directory', 'directory',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
              default=DEFAULT_DIR,
              help='Directory to search (default: current directory)')
@click.option('-S', '--size-in-gb', 'size_gb',
              type=float,
              help=f'Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)')
@click.option('-s', '--size-in-mb', 'size_mb',
              type=float,
              help=f'Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)')
@click.option('-o', '--output', 'output_file',
              type=click.Path(dir_okay=False, writable=True),
              help='Save results to specified file')
@click.option('-n', '--no-size',
              is_flag=True,
              help='Display files without their sizes')
@click.option('-nt', '--no-table',
              is_flag=True,
              help='Output in plain text format (one file per line)')
@click.option('-v', '--verbose',
              is_flag=True,
              help='Enable verbose output showing search progress')
def files(directory, size_gb, size_mb, output_file, no_size, no_table, verbose):
    """Find large files in a directory.

    Search for files larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find files larger than 1GB:
        $ python -m find_large files -d /path/to/search -S 1
        $ find-large files -d /path/to/search -S 1
    
    \b
    Find files larger than 500MB and save results:
        $ python -m find_large files -d /path/to/search -s 500 -o results.txt
        $ find-large files -d /path/to/search -s 500 -o results.txt
    
    \b
    List files without sizes in plain text format:
        $ python -m find_large files -d /path/to/search -s 500 -n -nt
        $ find-large files -d /path/to/search -s 500 -n -nt
    """
    scan_files(directory, size_gb, size_mb, output_file, no_size, no_table, verbose)

@cli.command(cls=AsciiArtHelpCommand)
@click.option('-d', '--directory', 'directory',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
              default=DEFAULT_DIR,
              help='Directory to search (default: current directory)')
@click.option('-S', '--size-in-gb', 'size_gb',
              type=float,
              help=f'Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)')
@click.option('-s', '--size-in-mb', 'size_mb',
              type=float,
              help=f'Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)')
@click.option('-o', '--output', 'output_file',
              type=click.Path(dir_okay=False, writable=True),
              help='Save results to specified file')
@click.option('-n', '--no-size',
              is_flag=True,
              help='Display directories without their sizes')
@click.option('-nt', '--no-table',
              is_flag=True,
              help='Output in plain text format (one directory per line)')
@click.option('-v', '--verbose',
              is_flag=True,
              help='Enable verbose output showing search progress')
def dirs(directory, size_gb, size_mb, output_file, no_size, no_table, verbose):
    """Find large directories.

    Search for directories larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find directories larger than 1GB:
        $ python -m find_large dirs -d /path/to/search -S 1
        $ find-large dirs -d /path/to/search -S 1
    
    \b
    Find directories larger than 500MB and save results:
        $ python -m find_large dirs -d /path/to/search -s 500 -o results.txt
        $ find-large dirs -d /path/to/search -s 500 -o results.txt
    
    \b
    List directories without sizes in plain text format:
        $ python -m find_large dirs -d /path/to/search -s 500 -n -nt
        $ find-large dirs -d /path/to/search -s 500 -n -nt
    """
    scan_directories(directory, size_gb, size_mb, output_file, no_size, no_table, verbose)

@cli.command(name="vids", cls=AsciiArtHelpCommand)
@click.option('-d', '--directory', 'directory',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
              default=DEFAULT_DIR,
              help='Directory to search (default: current directory)')
@click.option('-S', '--size-in-gb', 'size_gb',
              type=float,
              help=f'Size threshold in GB (default: {DEFAULT_SIZE_GB}GB)')
@click.option('-s', '--size-in-mb', 'size_mb',
              type=float,
              help=f'Size threshold in MB (default: {DEFAULT_SIZE_MB}MB)')
@click.option('-o', '--output', 'output_file',
              type=click.Path(dir_okay=False, writable=True),
              help='Save results to specified file')
@click.option('-n', '--no-size',
              is_flag=True,
              help='Display videos without their sizes')
@click.option('-nt', '--no-table',
              is_flag=True,
              help='Output in plain text format (one video per line)')
@click.option('-v', '--verbose',
              is_flag=True,
              help='Enable verbose output showing search progress')
def videos(directory, size_gb, size_mb, output_file, no_size, no_table, verbose):
    """Find large video files.

    Search for video files larger than a specified size in the given directory.
    Results can be displayed in various formats and optionally saved to a file.

    \b
    [Examples]

    \b
    Find videos larger than 1GB:
        $ python -m find_large vids -d /path/to/search -S 1
        $ find-large vids -d /path/to/search -S 1
    
    \b
    Find videos larger than 500MB and save results:
        $ python -m find_large vids -d /path/to/search -s 500 -o results.txt
        $ find-large vids -d /path/to/search -s 500 -o results.txt
    
    \b
    List videos without sizes in plain text format:
        $ python -m find_large vids -d /path/to/search -s 500 -n -nt
        $ find-large vids -d /path/to/search -s 500 -n -nt
    """
    scan_videos(directory, size_gb, size_mb, output_file, no_size, no_table, verbose)

def main():
    """Main entry point when running as a module."""
    cli()

if __name__ == '__main__':
    main() 