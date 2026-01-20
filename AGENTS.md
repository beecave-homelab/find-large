# AGENTS.md

## Setup & Commands

### Install

**Package manager:** PDM (use `pdm install` and `pdm run` for local development)

**Recommended installation (via pipx):**

```bash
pipx install "git+https://github.com/beecave-homelab/find-large.git"
```

**From source (PDM):**

```bash
git clone https://github.com/beecave-homelab/find-large.git
cd find-large
pdm install
```

### Run / Dev

The tool provides three console scripts (unified CLI entry points). When developing locally, run them through `pdm run`:

```bash
# Find large files
pdm run find-large-files [OPTIONS]

# Find large directories
pdm run find-large-dirs [OPTIONS]

# Find large video files
pdm run find-large-vids [OPTIONS]
```

**Common options across all commands:**

- `-d, --directory PATH`: Target directory (default: current directory)
- `-S, --size-in-gb FLOAT`: Size threshold in GB (default: 1.0)
- `-s, --size-in-mb FLOAT`: Size threshold in MB
- `-o, --output PATH`: Save results to file
- `-n, --no-size`: Hide size column from output
- `-nt, --no-table`: Use plain text output instead of table
- `-v, --verbose`: Enable debug logging

**Example usage:**

```bash
# Find files larger than 500MB
pdm run find-large-files -s 500 -v

# Find directories larger than 2GB, save to file
pdm run find-large-dirs -S 2 -o results.txt

# Find video files in /Users/movies with table output
pdm run find-large-vids -d /Users/movies
```

### Tests

**Current status:** Not yet implemented (tests/ directory is a placeholder)

**Recommended setup for future testing:**

```bash
# Install test dependencies
pdm install -G test

# Run tests (once implemented)
pdm run pytest

# Run with coverage
pdm run pytest --cov=find_large
```

Test files should be placed in `tests/` directory following pytest conventions.

### Lint / Format / Typecheck

**Configured scripts (via PDM):**

```bash
# Install lint dependencies
pdm install -G lint

# Format code
pdm run format

# Lint code
pdm run lint

# Auto-fix lint issues
pdm run fix
```

Type checking is not currently configured; add a PDM script if needed.

### Build

```bash
# Build distributions
pdm build
```

## Project Structure

```dir
find-large/
├── find_large/              # Main package directory
│   ├── __init__.py          # Package initialization, exports main()
│   ├── __main__.py          # Entry point for `python -m find_large`
│   ├── cli.py               # UNIFIED CLI - Click group with all commands
│   ├── core.py              # SizeScannerBase abstract base class
│   ├── constants.py         # Configuration constants (size thresholds, exclusions)
│   ├── formatting.py        # Output formatting utilities (tables, colors)
│   ├── files/               # File scanning module
│   │   ├── __init__.py
│   │   ├── cli.py           # [LEGACY] Individual CLI for files command
│   │   ├── core.py          # [LEGACY] Procedural implementation
│   │   └── scanner.py       # [MODERN] FileScanner class (OOP)
│   ├── dirs/                # Directory scanning module
│   │   ├── __init__.py
│   │   ├── cli.py           # [LEGACY] Individual CLI for dirs command
│   │   ├── core.py          # [LEGACY] Procedural implementation
│   │   └── scanner.py       # [MODERN] DirectoryScanner class (OOP)
│   └── videos/              # Video scanning module
│       ├── __init__.py
│       ├── cli.py           # [LEGACY] Individual CLI for vids command
│       ├── core.py          # [LEGACY] Procedural implementation
│       └── scanner.py       # [MODERN] VideoScanner class (OOP)
├── tests/                   # Test directory (placeholder - not implemented)
├── docs/                    # Documentation directory (placeholder)
├── requirements.txt         # Dependencies (click 8.1.8, rich >=10.0.0)
├── README.md                # User documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore patterns
```

**Key architectural notes:**

- **Modern code**: `scanner.py` files use OOP with SizeScannerBase inheritance
- **Legacy code**: `core.py` files use procedural implementation (duplicated logic)
- **Unified CLI**: Primary interface in `find_large/cli.py` (280 lines)
- **Legacy CLIs**: Individual CLIs in submodules (`cli.py`) are outdated

**Entry points** (defined in pyproject.toml under `[project.scripts]`):

- `find-large-files` → `find_large.files.cli:main`
- `find-large-dirs` → `find_large.dirs.cli:main`
- `find-large-vids` → `find_large.videos.cli:main`

## Tech Stack

### Core

- **Python**: >=3.12
- **PDM / pdm-backend**: Package management and distribution

### CLI & Output

- **click**: Command-line interface framework for argument parsing and command structure
- **rich**: Terminal formatting, colored output, tables, progress spinners, and ASCII art

### Standard Library Modules

- `os`: File system operations and path handling
- `sys`: System operations and exit handling
- `logging`: Verbose output debugging
- `pathlib`: Modern path handling
- `typing`: Type hints (Optional, List, Tuple, Union, Set, Dict, Final)

### Development (Not Yet Configured)

- Recommended: pytest (testing), black (formatting), ruff (linting), mypy (type checking)

## Architecture & Patterns

### Modern vs Legacy Code

**IMPORTANT**: The codebase contains both modern and legacy implementations. New code should follow modern patterns.

**Modern Code** (use this pattern for new features):

- **Location**: `scanner.py` files in each submodule
- **Pattern**: Object-oriented with class inheritance
- **Base**: `SizeScannerBase` (find_large/core.py:138 lines)
- **Implementation**: `FileScanner`, `DirectoryScanner`, `VideoScanner`
- **Benefits**: Code reuse, consistent interface, easier testing

**Legacy Code** (avoid extending this pattern):

- **Location**: `core.py` files in submodules
- **Pattern**: Procedural implementation
- **Status**: Duplicated logic across three modules
- **Migration**: Eventually replace with scanner.py implementations

### Class Hierarchy

```text
SizeScannerBase (find_large/core.py)
    ├── FileScanner (files/scanner.py)
    ├── DirectoryScanner (dirs/scanner.py)
    └── VideoScanner (videos/scanner.py)
```

**SizeScannerBase** provides:

- Abstract interface for scanning operations
- Shared utility methods for size calculation and filtering
- Common validation logic

**Concrete scanners** implement:

- Specific scanning logic for files/directories/videos
- File type filtering (VideoScanner supports 20+ formats)
- Size threshold comparison

### Unified CLI Architecture

**Primary CLI**: `find_large/cli.py` (280 lines)

- Uses Click group pattern with three commands: `files`, `dirs`, `vids`
- Features ASCII art help display
- Centralized option definitions and validation
- Invokes scanner classes for actual work

**Legacy CLIs** (in submodules):

- `files/cli.py`, `dirs/cli.py`, `videos/cli.py`
- Standalone implementations that duplicate functionality
- Only maintained for backward compatibility

### Constants Configuration

**Location**: `find_large/constants.py` (155 lines)

**Contains**:

- Size conversion constants (KB, MB, GB, TB to bytes)
- Default search parameters (current directory, 1GB threshold)
- Hidden folders to include: `.git`, `.config`, `.huggingface`, `.local`
- 150+ macOS-specific system folders to exclude (Library, Containers, Caches, etc.)
- Video file extensions (20+ formats: .mp4, .mkv, .avi, .mov, etc.)

**Usage**: Import constants rather than hardcoding values throughout code.

### Formatting System

**Location**: `find_large/formatting.py` (127 lines)

**Features**:

- ASCII art banner display with command highlighting
- Color-coded output using Rich library
- Table formatting with automatic sizing
- Plain text output option (`--no-table`)
- Status spinner for long operations
- Total size summary with auto unit selection (TB/GB/MB)

### Data Flow

1. User invokes CLI command (e.g., `find-large-files`)
2. Click parses arguments and validates options
3. CLI creates appropriate scanner instance (FileScanner, DirectoryScanner, etc.)
4. Scanner recursively walks directory tree
5. Each item checked against size threshold
6. Exclusions (hidden folders, system paths) filtered out
7. Results formatted via formatting module
8. Output displayed or saved to file

## Code Style & Patterns

### Python Code Style

**Type Hints**:

- **Modern code** (scanner.py, cli.py, core.py): Full type hints with typing module
- **Legacy code** (submodule core.py files): No type hints
- **New code**: Always include type hints using `Optional`, `List`, `Tuple`, `Union`, `Set`, `Dict`, `Final`
- Example: `def scan_directory(directory: str, min_size: int) -> List[Tuple[str, int]]:`

**Naming Conventions**:

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Clear, descriptive names throughout

**Docstrings**:

- Google-style multi-line docstrings
- Module-level docstrings in all files
- Function docstrings describe purpose, parameters, and return values
- Click command docstrings include usage examples

**Import Ordering**:

Imports must be ordered as follows:

1. **Standard library** imports (os, sys, logging, pathlib, typing)
2. **Third-party** imports (rich, click)
3. **First-party/local** imports - use absolute imports for internal package modules (e.g., `from find_large import formatting` or `from find_large.files.scanner import FileScanner`)
4. Sorted alphabetically within each group
5. One blank line between groups

**Import Style for Internal Modules**:

- Never use relative imports for internal modules (e.g., avoid `from .. import formatting`)
- Structure: Use full package paths starting with `find_large`
- Prefer one import per line for clarity
- Keep all imports at top of file (module scope)
- Don't alias unless it adds clarity (e.g., `import numpy as np`)

**Canonical example**:

```python
from __future__ import annotations

import dataclasses
import pathlib

import httpx
import pydantic

from find_large import formatting
from find_large.files.scanner import FileScanner
```

**Error Handling**:

- Graceful handling of permission errors (continue scanning)
- Exit with error message for directory access failures
- Use `click.Abort` for user validation errors

### Commit Message Format

Use **Conventional Commits** with emoji prefixes:

```txt
feat ✨: [description]
fix 🐛: [description]
style 💎: [description]
chore 📦: [description]
docs 📝: [description]
```

**Examples**:

```txt
feat ✨: Initial implementation of the find-large package
fix 🐛: Refactor core functionality in find-large package
style 💎: Enhance find_large package with Click command-line interface
chore 📦: Add hidden folder inclusion to search
docs 📝: Update README.md with detailed project description
```

### Testing Patterns

**Not yet implemented** - When adding tests:

- Use pytest framework (recommended)
- Place test files in `tests/` directory
- Name test files as `test_<module>.py`
- Use descriptive test names following pattern: `test_<function>_<scenario>`
- Mock file system operations for unit tests
- Test edge cases: empty directories, permission errors, size thresholds

## Git / PR Workflow

### Branching Strategy

- **Main branch**: `main` (production-ready code)
- **Development branch**: `dev` (development work)
- **Feature branches**: Create from `dev` for specific features
- **Pull requests**: Merge to `main` via PRs with review

### Commit Workflow

1. Create feature branch from `dev`: `git checkout -b feature/my-feature`
2. Make commits using Conventional Commits format with emojis
3. Push to remote: `git push origin feature/my-feature`
4. Create pull request to `main`
5. Request review and address feedback
6. Merge with squash or merge commit (maintains linear history)

### Pull Request Checklist

Before creating a PR:

- [ ] Code follows style conventions
- [ ] Type hints included in new code (prefer modern pattern)
- [ ] Docstrings added/updated
- [ ] Commit messages follow emoji prefix format
- [ ] Entry points not broken (verify `find-large-files`, etc. work)
- [ ] Tests added (if applicable, though not yet implemented)

## Boundaries

### ✅ Always

- **Use Click for CLI features**: All new command-line functionality should use Click framework
- **Maintain type hints in new code**: Modern Python code (scanner.py, new features) must include type hints
- **Use Rich for output formatting**: Terminal output should use Rich library for colors, tables, and formatting
- **Follow SizeScannerBase pattern**: Create new scanner types by inheriting from SizeScannerBase
- **Use constants module**: Reference configuration values from constants.py, don't hardcode
- **Use formatting utilities**: Format output via formatting.py, not inline string manipulation
- **Handle errors gracefully**: Catch and handle permission/access errors without crashing
- **Write Google-style docstrings**: All functions and classes should have descriptive docstrings
- **Use emoji prefix in commits**: Follow Conventional Commits format with emoji prefixes
- **Test entry points**: Verify all three entry points work after changes

### ⚠️ Ask First

- **Modifying SizeScannerBase**: Changes to base class affect all scanners - discuss impact first
- **Adding new entry points**: Adding new console scripts requires pyproject.toml changes - coordinate with maintainer
- **Changing constants.py**: Modifications to size thresholds or exclusions affect all commands - verify implications
- **Removing legacy code**: While core.py files are legacy, they're currently active - plan migration before removal
- **Adding new dependencies**: External libraries increase package size - evaluate necessity
- **Breaking changes to CLI**: Changes to command structure or options affect user workflow - consider backward compatibility
- **Modifying video format list**: Adding/removing video extensions affects users - confirm with stakeholder

### 🚫 Never

- **Modify individual CLI implementations without considering unified CLI**: Changes to files/cli.py, dirs/cli.py, or videos/cli.py should be considered alongside find_large/cli.py
- **Break existing entry points**: All three console scripts must continue working after changes
- **Hardcode magic numbers**: Use constants from constants.py, not inline numeric literals
- **Use print() for user output**: Use Rich formatting library, not print statements
- **Ignore type hints in modern code**: New code following scanner.py pattern must include type hints
- **Crash on permission errors**: Handle file/directory access errors gracefully, continue scanning
- **Remove SizeScannerBase inheritance**: Scanner classes must inherit from base class
- **Commit secrets or sensitive data**: Never commit .env, credentials, or sensitive configuration files
- **Skip docstrings for public functions**: All exported functions and classes must have documentation

## Common Tasks

### Adding a New File Extension Filter

**Goal**: Add support for a new file type (e.g., images)

**Steps**:

1. Add extension to constants.py: Create new constant list (e.g., `IMAGE_EXTENSIONS`)
2. Create new scanner module: `find_large/images/` with `__init__.py`, `cli.py`, `core.py`, `scanner.py`
3. Implement ImageScanner class in `images/scanner.py` inheriting from SizeScannerBase
4. Add `images` command to unified CLI in `find_large/cli.py`
5. Add entry point to pyproject.toml: `find-large-images → find_large.images.cli:main`
6. Test new command with various file sizes and directories

**Reference**: See `videos/scanner.py` for pattern to follow

### Modifying Exclusion Lists

**Goal**: Add or remove directories from exclusion list

**Steps**:

1. Edit `find_large/constants.py`
2. Locate appropriate exclusion list (e.g., `MACOS_SYSTEM_FOLDERS`, `EXCLUDED_FOLDERS`)
3. Add/remove entries following existing pattern
4. Save file and test with `-v` flag to see which directories are being skipped

**Note**: Changes affect all commands (files, dirs, vids)

### Creating a New Scanner Type

**Goal**: Create scanner for a new category (e.g., audio files)

**Steps**:

1. Create new submodule: `find_large/audio/`
2. Implement `AudioScanner` class inheriting from `SizeScannerBase`
3. Override key methods:
   - `should_include_file()`: Filter by audio extensions
   - `get_item_size()`: Calculate file or directory size
4. Add command to unified CLI in `find_large/cli.py`
5. Add entry point to `pyproject.toml`
6. Test with various directories and file sizes

**Reference**: `videos/scanner.py:57` lines shows minimal scanner implementation

### Updating CLI Options

**Goal**: Add new option to existing command (e.g., --sort-by option)

**Steps**:

1. Edit `find_large/cli.py`

2. Add new Click option to command decorator:

   ```python
   @main.command('files')
   @click.option('--sort-by', type=click.Choice(['size', 'name', 'date']), default='size')
   ```

3. Pass option to scanner initialization

4. Modify scanner to handle sorting logic

5. Update help text and docstrings

6. Test with all command combinations

**Reference**: `find_large/cli.py:280` lines for current option patterns

### Working with Constants Module

**Goal**: Add new configuration constant

**Steps**:

1. Edit `find_large/constants.py`
2. Add constant at appropriate section (size thresholds, file extensions, exclusions)
3. Follow naming convention: `UPPER_CASE` for constants
4. Add descriptive comment explaining purpose
5. Import constant in modules where needed
6. Update docstrings if constant affects user-facing behavior

**Note**: Constants are used across all three scanner types

## Troubleshooting

### Permission Denied Errors

**Symptom**: Tool crashes with `PermissionError` when scanning directories

**Cause**: File system permissions prevent access to certain directories

**Solution**:

- Tool handles permission errors gracefully and continues scanning
- Use `-v` flag to see which directories are being skipped
- Run with elevated permissions if needed: `sudo find-large-files` (use cautiously)
- Check that excluded directories list in constants.py includes system folders
- Current implementation logs error and continues, doesn't crash

### Path Issues on Different Operating Systems

**Symptom**: Paths don't work correctly on Windows vs macOS/Linux

**Cause**: Path separators and path handling differences

**Solution**:

- Use `pathlib.Path` for all path operations (not `os.path`)
- Code uses `pathlib` which handles cross-platform paths
- Avoid hardcoded path separators (`/` or `\`)
- Test on target OS before deployment
- Exclusion lists are currently macOS-specific - add OS-specific lists as needed

### Large Directory Scanning Performance

**Symptom**: Tool takes very long to scan directories with many files

**Cause**: Recursive directory walking is I/O intensive

**Solution**:

- Use `-v` flag to see progress and identify slow operations
- Add more exclusions to constants.py to skip large system directories
- Consider adding `--max-depth` option to limit recursion depth
- Current implementation is single-threaded - could be parallelized for performance
- For very large scans, consider saving results to file with `-o` option

### Entry Points Not Found

**Symptom**: `find-large-files: command not found`

**Cause**: Package not installed correctly or entry points not set up

**Solution**:

- Verify installation: `pip list | grep find-large`
- Reinstall: `pip install --force-reinstall "git+https://github.com/beecave-homelab/find-large.git"`
- Check pyproject.toml entry points are correctly defined
- Use direct invocation as fallback: `python -m find_large files`
- Ensure Python scripts directory is in PATH

### Size Threshold Not Working

**Symptom**: Files/directories smaller than threshold appear in results

**Cause**: Size unit confusion (MB vs GB) or conversion error

**Solution**:

- Verify correct unit flag: `-S` for GB, `-s` for MB
- Use decimal numbers: `-S 1.5` for 1.5 GB, not `-S 1500`
- Check constants.py for size conversion constants
- Use `-v` flag to see size comparisons being made
- Verify file/directory sizes manually with `ls -lh` or `du -sh`

### Output Formatting Issues

**Symptom**: Tables don't display correctly or colors are missing

**Cause**: Terminal doesn't support Rich output or configuration issue

**Solution**:

- Use `-nt` flag for plain text output if tables don't render
- Ensure terminal supports ANSI colors and UTF-8
- Check that rich library is installed: `pip list | grep rich`
- Try different terminal emulators
- Save output to file with `-o` option for non-interactive use

### Hidden Folders Being Excluded

**Symptom**: `.git` or `.config` folders not scanned

**Cause**: Default behavior excludes hidden folders

**Solution**:

- Hidden folders are excluded by default in scanning logic
- To include specific hidden folders, add them to `INCLUDE_HIDDEN_FOLDERS` in constants.py
- Currently included: `.git`, `.config`, `.huggingface`, `.local`
- Modify exclusion logic if you want all hidden folders scanned
- Note: System hidden folders are always excluded for safety

### Video Files Not Detected

**Symptom**: Video files don't appear in `find-large-vids` results

**Cause**: File extension not in supported video formats list

**Solution**:

- Check supported formats in constants.py: `VIDEO_EXTENSIONS`
- Currently supports 20+ formats: .mp4, .mkv, .avi, .mov, .wmv, etc.
- Add new extensions to `VIDEO_EXTENSIONS` constant if needed
- Verify file has correct extension (case-sensitive matching)
- Use `-v` flag to see which files are being filtered

### Test Infrastructure Missing

**Symptom**: No tests run or `pytest: command not found`

**Cause**: Testing not yet implemented (tests/ directory is placeholder)

**Solution**:

- Install pytest: `pip install pytest pytest-cov`
- Test directory is currently empty (only .gitkeep)
- When adding tests, place them in `tests/` directory following pytest conventions
- Run tests with: `pytest`
- Run with coverage: `pytest --cov=find_large`

### Linting Tools Not Configured

**Symptom**: No automated code quality checks

**Cause**: Linting/formatting tools not set up yet

**Solution**:

- Install recommended tools: `pip install black ruff mypy`
- Format code: `black find_large/`
- Lint code: `ruff check find_large/`
- Type check: `mypy find_large/`
- Consider adding pre-commit hooks to enforce these automatically
- Currently no CI/CD pipeline to run these checks automatically
