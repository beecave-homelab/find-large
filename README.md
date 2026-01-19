# Find Large Files

A command-line tool to search for and list large files in a directory. This utility helps you identify space-consuming files and directories with options for different output formats and filtering.

## Versions

**Current version**: 0.2.0 - Initial release with support for finding large files, directories, and video files.

## Table of Contents

- [Versions](#versions)
- [Badges](#badges)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Badges

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Version](https://img.shields.io/badge/version-0.2.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Installation

You can install find-large directly using `pipx`:

```bash
pipx install "git+https://github.com/beecave-homelab/find-large.git"
```

### Install in a Virtual Environment

If you prefer to use a virtual environment:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the package
pip install "git+https://github.com/beecave-homelab/find-large.git"
```

### Install from Source

Clone and install from source:

```bash
git clone https://github.com/beecave-homelab/find-large.git
cd find-large
pip install .
```

## Usage

Find Large Files provides three main commands:

- `files`: Find large files in a directory
- `dirs`: Find large directories
- `vids`: Find large video files

### Basic Usage

Run as a module:

```bash
python -m find_large <command> [options]
```

Examples:

```bash
# Find files larger than 1GB in current directory
python -m find_large files -S 1

# Find files larger than 500MB in a specific directory
python -m find_large files -d /path/to/search -s 500

# Find large directories
python -m find_large dirs -d /path/to/search -s 500

# Find large video files
python -m find_large vids -d /path/to/search -S 2
```

For help with any command:

```bash
python -m find_large --help
python -m find_large <command> --help
```

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for more information.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
