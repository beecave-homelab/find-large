"""Setup configuration for find-large package."""

from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="find-large",
    version="0.1.0",
    author="elvee",
    description="A tool to search for large files in a system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beecave-homelab/find-large",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        "rich>=10.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "find-large-files=find_large.files.cli:main",
            "find-large-dirs=find_large.dirs.cli:main",
            "find-large-vids=find_large.videos.cli:main",
        ],
    },
) 