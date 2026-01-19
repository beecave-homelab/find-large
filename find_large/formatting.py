"""Terminal output formatting and styling for find-large-files."""

from rich.console import Console
from rich.status import Status
from rich.table import Table

# Initialize console
console: Console = Console()

# Color and style definitions
STYLES: dict[str, str] = {
    "ascii_art": "bold cyan",
    "active_command": "bold blue",
    "inactive_command": "dim",
    "error": "bold red",
    "success": "bold green",
    "warning": "bold yellow",
    "header": "bold magenta",
    "total_size": "bold green",
    "status": "bold green",
}

# Common ASCII art for all commands
ASCII_ART: str = """
╔═╗╦╔╗╔╔╦╗  ╦  ╔═╗╦═╗╔═╗╔═╗
╠╣ ║║║║ ║║  ║  ╠═╣╠╦╝║ ╦║╣
╚  ╩╝╚╝═╩╝  ╩═╝╩ ╩╩╚═╚═╝╚═╝"""


def print_ascii_art(script_type: str = "files") -> None:
    """Print ASCII art banner based on script type."""
    # Print the common ASCII art
    console.print(ASCII_ART, style=STYLES["ascii_art"])

    # Format each command based on whether it's the current one
    commands: list[str] = ["FILES", "DIRS", "VIDS"]
    formatted_commands: list[str] = []

    for cmd in commands:
        if cmd.lower() == script_type.upper():
            formatted_commands.append(
                f"[{STYLES['active_command']}]{cmd}[/{STYLES['active_command']}]"
            )
        else:
            formatted_commands.append(
                f"[{STYLES['inactive_command']}]{cmd}[/{STYLES['inactive_command']}]"
            )

    # Join with separator and print
    command_line: str = " | ".join(formatted_commands)
    console.print(f"    {command_line}\n")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"Error: {message}", style=STYLES["error"])


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(message, style=STYLES["success"])


def print_status(message: str) -> None:
    """Print a status message."""
    console.print(message, style=STYLES["warning"])


def create_results_table(show_size: bool = True) -> Table:
    """Create and configure the results table.

    Args:
        show_size: Whether to include the size column.

    Returns:
        Table: Configured results table.
    """
    table = Table(show_header=True, header_style=STYLES["header"], show_lines=True)
    table.add_column("File Location", overflow="crop", no_wrap=True)
    if show_size:
        table.add_column("File Size", justify="right", width=12)
    return table


def format_table(
    data_lines: list[tuple[str, str]],
    no_size: bool = False,
    total_bytes: int = 0,
    file_console: Console | None = None,
    no_table: bool = False,
) -> None:
    """Format and print the results table."""
    output_console: Console = file_console if file_console else console

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
        table: Table = create_results_table(not no_size)

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


def _print_total_size(console: Console, total_bytes: int, plain: bool = False) -> None:
    """Helper function to print total size with appropriate unit."""
    if total_bytes >= 1024**4:  # TB range
        size: float = total_bytes / (1024**4)
        unit: str = "TB"
    elif total_bytes >= 1024**3:  # GB range
        size: float = total_bytes / (1024**3)
        unit: str = "GB"
    else:  # MB range
        size: float = total_bytes / (1024**2)
        unit: str = "MB"

    if plain:
        console.print(f"Total size: {size:.2f} {unit}")
    else:
        console.print(
            f"Total size: [{STYLES['total_size']}]{size:.2f} {unit}[/{STYLES['total_size']}]"
        )


def get_status_context(message: str) -> Status:
    """Get a status context for long-running operations.

    Args:
        message: Status message to display.

    Returns:
        Status: Rich status context object.
    """
    return console.status(f"[{STYLES['status']}]{message}[/{STYLES['status']}]", spinner="dots")
