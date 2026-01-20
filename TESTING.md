# Testing Guide

This document describes the testing strategy and best practices for the `find_large` package. The project does not yet ship with a full test suite, so this guide defines the intended structure, tooling, and conventions to follow as tests are added.

**Updated**: January 19, 2026 - Guide created to mirror the current codebase state.

## Quick Start

```bash
# Install test dependencies (dev group in PDM)
pdm install -G test

# Run all tests (once tests are added)
pdm run pytest

# Run unit tests only (recommended default)
pdm run pytest tests/unit/

# Run unit tests with coverage
pdm run pytest tests/unit/ --cov=find_large --cov-report=term-missing:skip-covered

# Run specific test files or functions
pdm run pytest tests/unit/test_formatting.py
pdm run pytest tests/unit/test_formatting.py::test_render_table__formats_sizes

# Verbose output
pdm run pytest -v

# Stop after first failure
pdm run pytest --maxfail=1
```

> Note: Test dependencies are already declared in the optional PDM dev group (`[tool.pdm.dev-dependencies].test`).

## Test Organization

### Directory Structure (Target)

```txt
tests/
├── unit/                # Fast, hermetic unit tests
│   ├── test_cli_unit.py
│   ├── test_core.py
│   ├── test_formatting.py
│   └── test_scanners.py
├── integration/         # Cross-boundary tests (filesystem, CLI, subprocess)
│   ├── test_cli.py
│   └── test_walkers.py
├── e2e/                 # End-to-end workflows (CLI commands)
│   └── test_find_large_cli.py
├── slow/                # Resource-intensive tests (reserved)
└── __init__.py
```

### Current State

- `tests/` is a placeholder with no test files yet.
- New tests should follow the structure above to keep unit and integration coverage organized.

### Test Markers

Use pytest markers to categorize tests by resource requirements:

- **`@pytest.mark.integration`** - Crosses filesystem or subprocess boundaries
- **`@pytest.mark.slow`** - Long-running tests (>5 seconds)
- **`@pytest.mark.e2e`** - Full CLI workflow smoke tests

## Test Types

**Unit Tests** (default, fast)

- Pure logic testing
- No external I/O beyond `tmp_path`
- Deterministic and hermetic
- Run by default with `pytest tests/unit/`

**Integration Tests** (`@pytest.mark.integration`)

- Cross filesystem or subprocess boundaries
- Validate CLI wiring and file walking
- Opt-in via `-m integration`

**End-to-End Tests** (`@pytest.mark.e2e`)

- Full workflow validation
- CLI integration tests for the entry points
- Black-box user-level scenarios

## Writing Tests

### Test Naming Convention

Follow the pattern: `test_<unit_under_test>__<expected_behavior>`

```python
from pathlib import Path

def test_format_size__converts_bytes_to_gb() -> None:
    """Verify size formatting converts bytes to GB."""
    result = format_size(1024 ** 3)
    assert "GB" in result
```

### Arrange-Act-Assert Pattern

All tests should follow the AAA pattern for clarity:

```python
def test_scan_directory__filters_below_threshold(tmp_path: Path) -> None:
    """Ensure scanner filters files below the threshold."""
    # Arrange
    target = tmp_path / "sample.txt"
    target.write_text("data")

    # Act
    results = scanner.scan(tmp_path)

    # Assert
    assert results == []
```

### Using Fixtures

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_tree(tmp_path: Path) -> Path:
    """Create a small directory tree for testing."""
    (tmp_path / "a.txt").write_text("alpha")
    (tmp_path / "b.txt").write_text("beta")
    return tmp_path
```

### Parametrized Tests

Use `@pytest.mark.parametrize` to test multiple inputs:

```python
import pytest

@pytest.mark.parametrize(
    "size_bytes,expected_unit",
    [
        (1024, "KB"),
        (1024 ** 2, "MB"),
        (1024 ** 3, "GB"),
    ],
)
def test_format_size__uses_expected_unit(size_bytes: int, expected_unit: str) -> None:
    """Test size formatter units."""
    assert expected_unit in format_size(size_bytes)
```

### Type Annotations

All test functions must have type annotations:

```python
from pathlib import Path

def test_example(tmp_path: Path) -> None:
    """Example test with proper type hints."""
    pass
```

## Test Isolation & Determinism

### Filesystem Isolation

Use `tmp_path` fixture for file operations:

```python
def test_save_output__writes_file(tmp_path: Path) -> None:
    """Test file saving to temporary directory."""
    output_file = tmp_path / "output.txt"
    save_output(output_file, "content")
    assert output_file.exists()
    assert output_file.read_text() == "content"
```

### Mocking External Dependencies

Mock external boundaries, not internal logic:

```python
from unittest.mock import patch

def test_cli__exits_on_invalid_directory() -> None:
    """Ensure CLI exits on invalid directories."""
    with patch("pathlib.Path.exists", return_value=False):
        result = runner.invoke(app, ["files", "-d", "/missing"])
        assert result.exit_code != 0
```

### Deterministic Data

- Use fixed seeds for random data
- Normalize timestamps and unordered collections
- Create minimal test fixtures programmatically

## Coverage Goals

- **Target**: >=85% line coverage for core logic
- **Focus**: scanners, formatting utilities, CLI validation
- **Exclude**: system-specific paths and OS-dependent directory scanning

Run coverage reports:

```bash
# Terminal report
python -m pytest tests/unit/ --cov=find_large --cov-report=term-missing:skip-covered

# HTML report (detailed)
python -m pytest tests/unit/ --cov=find_large --cov-report=html
open htmlcov/index.html
```

## Common Patterns

### Testing CLI Commands

```python
from click.testing import CliRunner

from find_large.cli import cli


def test_cli_help() -> None:
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
```

### Testing with Temporary Files

```python
from pathlib import Path


def test_scanner__finds_large_file(tmp_path: Path) -> None:
    """Test file scanner finds a large file."""
    target = tmp_path / "large.bin"
    target.write_bytes(b"0" * 1024 * 1024)

    results = scanner.scan(tmp_path)
    assert any(path == target for path, _ in results)
```

### Testing Error Handling

```python
import pytest

def test_validate_directory__raises_on_missing() -> None:
    """Test error handling for missing directories."""
    with pytest.raises(ValueError, match="does not exist"):
        validate_directory("/missing")
```

## CI Integration

In CI environments:

- Only fast unit tests should run by default
- Integration/E2E tests are opt-in via markers
- Coverage reports should be generated for unit tests

## Best Practices Summary

✅ **DO:**

- Write fast, deterministic, hermetic unit tests by default
- Use proper test markers for integration/slow/e2e tests
- Follow AAA pattern and one assertion per test concept
- Use `tmp_path` for filesystem isolation
- Mock external boundaries (I/O, subprocesses)
- Include type annotations on all test functions
- Use parametrized tests for multiple input scenarios

❌ **DON'T:**

- Download assets or use real network calls in unit tests
- Rely on system-specific paths during default runs
- Use absolute paths or hardcoded file locations
- Leave tests non-deterministic (random without seeds)
- Mock internal business logic
- Skip writing docstrings for test functions

## Running Specific Test Suites

```bash
# Fast unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# E2E tests only
python -m pytest tests/e2e/

# Run all tests
python -m pytest

# Exclude specific markers
python -m pytest -m "not (e2e or slow)"

# Collect and show tests without running
python -m pytest --collect-only
```

## Debugging Tests

```bash
# Run with detailed output
python -m pytest -vv

# Show print statements
python -m pytest -s

# Drop into debugger on failure
python -m pytest --pdb

# Detailed traceback
python -m pytest --tb=long
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- Project coding standards: `AGENTS.md`
