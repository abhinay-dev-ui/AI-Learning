"""
=========================================================
Module: main.py

Purpose:
Application entry point for the PDF Document Ingestion
Pipeline.

Responsibilities:
    - Start the application
    - Execute the PDF ingestion workflow
    - Handle top-level exceptions
    - Display execution status

=========================================================
"""

from pdf_service import process_pdf_document


def main() -> None:
    """Application entry point."""

    try:
        process_pdf_document()

        print("\nDocument ingestion completed successfully.")

    except FileNotFoundError as error:
        print(f"File Error: {error}")

    except PermissionError:
        print("Permission denied while accessing the PDF.")

    except ValueError as error:
        print(f"Validation Error: {error}")

    except Exception as error:
        print(f"Unexpected Error: {error}")


if __name__ == "__main__":
    main()