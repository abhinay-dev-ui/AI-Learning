"""
=========================================================
Module: main.py

Purpose:
Application entry point for the Employee Report Generator.

Responsibilities:
    - Start the application.
    - Execute the employee report workflow.
    - Handle top-level exceptions.
    - Display execution status.

=========================================================
"""

from employee_service import process_employee_report


def main() -> None:
    """Application entry point."""

    try:
        process_employee_report()
        print("Employee report generated successfully.")

    except FileNotFoundError:
        print("Error: Input file was not found.")

    except PermissionError:
        print("Error: Permission denied while accessing a file.")

    except UnicodeDecodeError:
        print("Error: Unable to decode the input file.")

    except Exception as error:
        # Catch any unexpected errors that were not explicitly handled.
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()