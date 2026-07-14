"""
=========================================================
Module: file_utils.py

Purpose:
Provides reusable helper functions for reading,
writing, and appending text files.

This module abstracts all low-level file operations so
the business layer does not interact directly with
Python's file APIs.

Used By:
    - employee_service.py

Concepts Demonstrated:
    - pathlib
    - Context Managers (with)
    - File Objects
    - Reading Text Files
    - Writing Text Files
    - Append Mode
    - Exception Propagation
    - Separation of Concerns

=========================================================
"""

from pathlib import Path


def read_text_file(file_path: Path) -> list[str]:
    """
    Reads a text file and returns its contents as a list of lines.

    Args:
        file_path:
            Path of the input file.

    Returns:
        List[str]:
            A list containing each line from the file.

    Raises:
        FileNotFoundError
        PermissionError
        UnicodeDecodeError
    """

    employees = []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                employees.append(line.strip())

        return employees

    except (
        FileNotFoundError,
        PermissionError,
        UnicodeDecodeError,
    ):
        raise


def write_text_file(file_path: Path, content: str) -> None:
    """
    Creates or overwrites a text file.

    Args:
        file_path:
            Output file location.

        content:
            Text to write.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        file.write(content)


def append_text_file(file_path: Path, content: str) -> None:
    """
    Appends text to an existing file.

    Creates the file if it does not already exist.

    Args:
        file_path:
            File to append.

        content:
            Text to append.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("a", encoding="utf-8") as file:
        file.write(content)

def read_binary_file(file_path: Path) -> bytes:
    """
    Reads an entire binary file.

    Args:
        file_path:
            Path to the binary file.

    Returns:
        Raw bytes.

    Raises:
        FileNotFoundError
        PermissionError
    """

    with file_path.open("rb") as file:
        return file.read()
    
def read_file_header(file_path: Path, size: int) -> bytes:
    """
    Reads only the first few bytes of a file.

    Useful for validating file signatures
    (Magic Bytes).

    Args:
        file_path:
            File path.

        size:
            Number of bytes to read.

    Returns:
        Raw bytes.
    """

    with file_path.open("rb") as file:
        return file.read(size)