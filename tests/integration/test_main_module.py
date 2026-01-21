"""Integration tests for __main__ module."""

import subprocess


def test_main_module_runs_as_script() -> None:
    """Test __main__ module can be run as a script."""
    result = subprocess.run(
        ["python", "-m", "find_large", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout
