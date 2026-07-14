"""
=========================================================
Module: log_service.py

Purpose:
Processes large application log files and generates
a summary report.

Responsibilities:
    - Read log file efficiently
    - Count log levels
    - Generate summary report
    - Save report
    - Record execution log

Used By:
    - main.py

Depends On:
    - file_utils.py
=========================================================
"""

from datetime import datetime
from pathlib import Path

from file_utils import append_text_file, write_text_file

# ------------------------------------------------------------------
# Application Paths
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "input" / "application.log"
REPORT_FILE = BASE_DIR / "output" / "log_summary.txt"
LOG_FILE = BASE_DIR / "logs" / "execution.log"


def analyze_log_file() -> dict[str, int]:
    """
    Analyze the log file without loading the entire file into memory.
    """

    statistics = {
        "TOTAL": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }

    with INPUT_FILE.open("r", encoding="utf-8") as file:

        # Read one line at a time.
        # Python internally buffers the file, making this
        # memory-efficient even for very large log files.
        for line in file:

            statistics["TOTAL"] += 1

            if " INFO " in line:
                statistics["INFO"] += 1

            elif " WARNING " in line:
                statistics["WARNING"] += 1

            elif " ERROR " in line:
                statistics["ERROR"] += 1

            elif " CRITICAL " in line:
                statistics["CRITICAL"] += 1

    return statistics


def generate_report(statistics: dict[str, int]) -> str:
    """
    Generate the log summary report.
    """

    report = [
        "Log Analysis Report",
        "=" * 40,
        "",
        f"Total Entries : {statistics['TOTAL']}",
        "",
        f"INFO      : {statistics['INFO']}",
        f"WARNING   : {statistics['WARNING']}",
        f"ERROR     : {statistics['ERROR']}",
        f"CRITICAL  : {statistics['CRITICAL']}",
        "",
        "Report Generated Successfully",
    ]

    return "\n".join(report)


def process_log_file() -> None:
    """
    Execute the complete log analysis workflow.
    """

    statistics = analyze_log_file()

    report = generate_report(statistics)

    write_text_file(REPORT_FILE, report)

    append_text_file(
        LOG_FILE,
        (
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n"
            "Log Analysis Completed Successfully\n"
            f"{'-' * 40}\n"
        ),
    )