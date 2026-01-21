"""Unit tests for __main__ module."""

from unittest.mock import patch

from find_large import __main__


def test_main_imports_cli_main() -> None:
    """Test __main__ imports main from cli module."""
    assert hasattr(__main__, "main")
    assert callable(__main__.main)


def test_main_callable_with_mock() -> None:
    """Test main is callable and invokes CLI."""
    with patch("find_large.cli.cli") as mock_cli:
        __main__.main()
        mock_cli.assert_called_once()
