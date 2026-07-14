"""
=========================================================
Module: employee_service.py

Purpose:
Contains the business logic for processing employee
records and generating a summary report.

This module is responsible for:
    - Loading employee records
    - Validating employee data
    - Generating a report
    - Saving the report
    - Recording execution logs

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
    read_text_file,
    write_text_file,
)

# ------------------------------------------------------------------
# Application Paths
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "input" / "employees.txt"
REPORT_FILE = BASE_DIR / "output" / "employee_report.txt"
LOG_FILE = BASE_DIR / "logs" / "execution.log"


def validate_employee_record(record: str) -> bool:
    """
    Validates an employee record.

    Expected format:

        Name,Department

    Returns:
        True if valid, otherwise False.
    """

    if "," not in record:
        return False

    name, department = record.split(",", maxsplit=1)

    return bool(name.strip()) and bool(department.strip())


def generate_report(employee_records: list[str]) -> str:
    """
    Generates the employee summary report.
    """

    report = []
    departments = []

    report.append("Employee Report")
    report.append("=" * 40)
    report.append("")

    report.append(f"Total Employees : {len(employee_records)}")
    report.append("")

    report.append("Departments")
    report.append("-" * 20)

    for record in employee_records:
        _, department = record.split(",", maxsplit=1)
        departments.append(department.strip())

    for department in departments:
        report.append(f"- {department}")

    report.append("")
    report.append("Report Generated Successfully")

    return "\n".join(report)


def process_employee_report() -> None:
    """
    Executes the complete employee report workflow.
    """

    employee_records = read_text_file(INPUT_FILE)

    valid_records = []

    for record in employee_records:

        if validate_employee_record(record):
            valid_records.append(record)

    report = generate_report(valid_records)

    write_text_file(REPORT_FILE, report)

    append_text_file(
        LOG_FILE,
        (
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n"
            "Employee Report Generated Successfully\n"
            f"{'-' * 40}\n"
        ),
    )