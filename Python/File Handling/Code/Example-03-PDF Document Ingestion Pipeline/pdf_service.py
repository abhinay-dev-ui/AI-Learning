"""
=========================================================
Module: pdf_service.py

Purpose:
Handles the business logic for validating and ingesting
PDF documents.

Responsibilities:
    - Validate file existence
    - Validate file extension
    - Verify PDF signature (Magic Bytes)
    - Read PDF as binary data
    - Record execution log

Used By:
    - main.py

Depends On:
    - file_utils.py
=========================================================
"""

from datetime import datetime
from pathlib import Path

from file_utils import (
    append_text_file,
    read_binary_file,
    read_file_header,
)

# ------------------------------------------------------------------
# Application Paths
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "input" / "Income_Tax_Rules.pdf"
LOG_FILE = BASE_DIR / "logs" / "execution.log"

# PDF files always begin with these bytes.
PDF_SIGNATURE = b"%PDF"


def validate_pdf_file(file_path: Path) -> None:
    """
    Validate that the supplied file is a valid PDF.

    Args:
        file_path:
            Path of the PDF document.

    Raises:
        FileNotFoundError:
            If the file does not exist.

        ValueError:
            If the file extension or signature is invalid.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path.name}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Invalid file type. Expected a PDF document.")

    signature = read_file_header(file_path, 4)

    if signature != PDF_SIGNATURE:
        raise ValueError(
            "Invalid PDF signature. The file may be corrupted or is not a valid PDF."
        )


def ingest_pdf(file_path: Path) -> bytes:
    """
    Read the PDF as raw bytes after successful validation.

    Args:
        file_path:
            Path of the PDF document.

    Returns:
        Raw bytes of the PDF document.
    """

    validate_pdf_file(file_path)

    return read_binary_file(file_path)


def process_pdf_document() -> None:
    """
    Execute the complete PDF document ingestion workflow.
    """

    pdf_bytes = ingest_pdf(INPUT_FILE)

    print(f"Successfully read {len(pdf_bytes):,} bytes.\n")

    print("✓ File Found")
    print("✓ Extension Verified")
    print("✓ PDF Signature Verified")
    print("✓ Binary Data Read Successfully")
    print("✓ Ready for PDF Parser")

    append_text_file(
        LOG_FILE,
        (
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n"
            "PDF Document Validated Successfully\n"
            f"{'-' * 40}\n"
        ),
    )