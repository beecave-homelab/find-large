# VERSIONS.md

## ToC

- [v0.2.1](#v021-current---21-01-2026)
- [v0.2.0](#v020---18-01-2026)
- [v0.1.0](#v010---01-01-2026)

## **v0.2.1** (Current) - *21-01-2026*

### 🐛 **Bug Fix Release**

### 🧪 **Testing Improvements in v0.2.1**

- **Added**: Expanded end-to-end and unit test coverage for CLI workflows.
- **Enhanced**: Added fixtures and return type checks to ensure consistent outputs.

### 🐛 **Bug Fixes in v0.2.1**

- **Fixed**: Updated video scanner to use consistent MB-to-bytes conversion.
  - **Issue**: Video thresholds were computed with mismatched constants.
  - **Root Cause**: The scanner used a legacy conversion value.
  - **Solution**: Standardized on the MB_TO_BYTES constant.

### 🔧 **Improvements in v0.2.1**

- **Improved**: Added MB_TO_BYTES constant to the formatting utilities.
- **Updated**: Maintenance updates for CodeQL schedule and workflow configuration.

### 📝 **Key Commits in v0.2.1**

`5af2038`, `54db851`, `d4e584c`, `9187b21`, `163e90f`

______________________________________________________________________

## **v0.2.0** - *18-01-2026*

### ✨ **Feature Release**

### ✨ **New Features in v0.2.0**

- **Added**: Migration to PDM/pyproject.toml backend for packaging.
- **Enhanced**: Refactored scanning logic across files, dirs, and vids.

### 🔧 **Improvements in v0.2.0**

- **Improved**: Internal refactors to modernize scanner implementations.
- **Updated**: Documentation updates for AI agent/contributor guidance.

### 🐛 **Fixes in v0.2.0**

- **Fixed**: Added validation for positive size values in the CLI.
- **Fixed**: Added validation for output file paths in local CI automation.
- **Fixed**: Updated video formats in CLI documentation.
- **Fixed**: Corrected output file handling in legacy core implementation.
- **Fixed**: Resolved case sensitivity issues in ASCII art rendering.

### 📝 **Key Commits in v0.2.0**

`0623ede`, `256beb9`, `680ab22`, `9c0eccc`, `0071c3b`, `05eec97`

______________________________________________________________________

## **v0.1.0** - *01-01-2026*

### 🎉 **Initial Release**

- **Added**: Initial CLI for finding large files, directories, and videos.

______________________________________________________________________
