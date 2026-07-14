"""
=========================================================
Module: main.py

Purpose:
Application entry point for the Large Log File Analyzer.
=========================================================
"""

from log_service import process_log_file


def main() -> None:
    """Application entry point."""

    try:
        process_log_file()
        print("Log analysis completed successfully.")

    except FileNotFoundError:
        print("Error: Log file not found.")

    except PermissionError:
        print("Error: Permission denied.")

    except UnicodeDecodeError:
        print("Error: Unable to decode log file.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()