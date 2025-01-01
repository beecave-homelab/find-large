"""Terminal output formatting and styling for find-large-files."""

from rich.console import Console
from rich.table import Table
from rich.status import Status

# Initialize console
console = Console()

# Color and style definitions
STYLES = {
    'ascii_art': 'bold cyan',
    'command_name': 'bold blue',
    'error': 'bold red',
    'success': 'bold green',
    'warning': 'bold yellow',
    'header': 'bold magenta',
    'total_size': 'bold green',
    'status': 'bold green',
}

# Common ASCII art for all commands
ASCII_ART = """
╔═╗╦╔╗╔╔╦╗  ╦  ╔═╗╦═╗╔═╗╔═╗
╠╣ ║║║║ ║║  ║  ╠═╣╠╦╝║ ╦║╣ 
╚  ╩╝╚╝═╩╝  ╩═╝╩ ╩╩╚═╚═╝╚═╝"""

COMMAND_NAMES = {
    "files": "FILES",
    "dirs": "DIRS",
    "vids": "VIDS"
}

def print_ascii_art(script_type="files"):
    """Print ASCII art banner based on script type."""
    # Print the common ASCII art
    console.print(ASCII_ART, style=STYLES['ascii_art'])
    
    # Get the command name and center it
    command_name = COMMAND_NAMES[script_type]
    # The ASCII art is 32 characters wide
    padding = " " * ((32 - len(command_name)) // 2)
    
    # Print the centered command name
    console.print(f"{padding}[{STYLES['command_name']}]{command_name}[/{STYLES['command_name']}]")

def print_error(message):
    """Print an error message."""
    console.print(f"Error: {message}", style=STYLES['error'])

def print_success(message):
    """Print a success message."""
    console.print(message, style=STYLES['success'])

def print_status(message):
    """Print a status message."""
    console.print(message, style=STYLES['warning'])

def create_results_table(show_size=True):
    """Create and configure the results table."""
    table = Table(show_header=True, header_style=STYLES['header'], show_lines=True)
    table.add_column("File Location", overflow="crop", no_wrap=True)
    if show_size:
        table.add_column("File Size", justify="right", width=12)
    return table

def format_table(data_lines, no_size=False, total_bytes=0, file_console=None, no_table=False):
    """Format and print the results table."""
    output_console = file_console if file_console else console
    
    if no_table:
        # Plain text output
        for line in data_lines[1:]:  # Skip header
            if no_size:
                output_console.print(line[0])
            else:
                output_console.print(f"{line[0]}\t{line[1]}")
        
        if not no_size and total_bytes > 0:
            output_console.print("\nTotal Size Summary")
            output_console.print("─" * 50)
            _print_total_size(output_console, total_bytes, plain=True)
    else:
        table = create_results_table(not no_size)
        
        for line in data_lines[1:]:  # Skip header
            if no_size:
                table.add_row(line[0])
            else:
                table.add_row(line[0], line[1])
        
        output_console.print(table)
        
        if not no_size and total_bytes > 0:
            output_console.print("\n[bold cyan]Total Size Summary[/bold cyan]")
            output_console.print("─" * 50)
            _print_total_size(output_console, total_bytes)

def _print_total_size(console, total_bytes, plain=False):
    """Helper function to print total size with appropriate unit."""
    if total_bytes >= 1024**4:  # TB range
        size = total_bytes / (1024**4)
        unit = "TB"
    elif total_bytes >= 1024**3:  # GB range
        size = total_bytes / (1024**3)
        unit = "GB"
    else:  # MB range
        size = total_bytes / (1024**2)
        unit = "MB"
    
    if plain:
        console.print(f"Total size: {size:.2f} {unit}")
    else:
        console.print(f"Total size: [{STYLES['total_size']}]{size:.2f} {unit}[/{STYLES['total_size']}]")

def get_status_context(message):
    """Get a status context for long-running operations."""
    return console.status(f"[{STYLES['status']}]{message}[/{STYLES['status']}]", spinner="dots") 