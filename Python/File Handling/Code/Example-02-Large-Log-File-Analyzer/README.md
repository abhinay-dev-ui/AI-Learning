# Example 02 - Large Log File Analyzer

## Overview

The **Large Log File Analyzer** demonstrates how production applications process **large text files efficiently** without loading the entire file into memory.

Unlike Example 01, which focused on basic file operations, this example introduces **streaming file processing**, where log entries are read one line at a time. This approach keeps memory usage low and allows the application to process files ranging from a few megabytes to several gigabytes using the same implementation.

The application analyzes an application log file, counts the occurrences of different log levels, generates a summary report, and records the execution in a log file.

---

# Business Use Case

Production applications generate log files continuously.

Operations teams often need a quick summary of the logs to answer questions such as:

- How many log entries were generated?
- How many INFO messages were recorded?
- How many WARNING messages occurred?
- How many ERROR or CRITICAL failures happened?

Instead of manually reviewing large log files, this application automates the analysis and generates a concise summary report.

---

# Application Workflow

```text
                application.log
                        │
                        ▼
             Open File (Read Mode)
                        │
                        ▼
         Read One Line at a Time (Streaming)
                        │
                        ▼
          Count Log Levels (INFO/WARNING/...)
                        │
                        ▼
             Generate Summary Report
                 │              │
                 ▼              ▼
       log_summary.txt    execution.log
```

---

# Folder Structure

```text
Example-02-Large-Log-File-Analyzer/

│
├── README.md
├── main.py
├── log_service.py
├── file_utils.py
│
├── input/
│   └── application.log
│
├── output/
│   └── log_summary.txt
│
└── logs/
    └── execution.log
```

---

# Concepts Covered

## File Handling

- Reading large files
- File iteration
- Internal buffering
- Memory-efficient processing
- Writing reports
- Append mode

---

## Python

- Dictionaries
- String processing
- Functions
- Exception handling
- pathlib

---

## Production Engineering

- Streaming data processing
- Log analysis
- Performance optimization
- Scalability
- Separation of concerns
- Code reuse

---

# Learning Objectives

After completing this example, you should be able to:

- Explain why `read()` is not suitable for large files.
- Understand why iterating over a file object is memory efficient.
- Process files of virtually any size using constant memory.
- Generate reports from streaming data.
- Reuse utility modules across multiple applications.

---

# Production Perspective

Large file processing is a common requirement in enterprise systems.

Similar techniques are used in:

- Log Analysis Systems
- ETL Pipelines
- SIEM Platforms
- Cloud Monitoring
- Data Processing Pipelines
- Financial Transaction Processing
- AI Dataset Preparation

The same streaming approach is also used to process large CSV files, datasets, and AI training data.

---

# Files in this Example

| File | Responsibility |
|------|----------------|
| `main.py` | Application entry point |
| `log_service.py` | Business logic for log analysis |
| `file_utils.py` | Reusable file operations |
| `application.log` | Input log file |
| `log_summary.txt` | Generated summary report |
| `execution.log` | Application execution log |

---

# Expected Output

## Log Summary

```text
Log Analysis Report
========================================

Total Entries : 10

INFO      : 5
WARNING   : 2
ERROR     : 2
CRITICAL  : 1

Report Generated Successfully
```

---

# Key Takeaway

The most important lesson from this example is choosing the **right reading strategy**.

| Method | Best Used For |
|---------|---------------|
| `read()` | Small files |
| `read(size)` | Chunk-based processing |
| `for line in file` | Large text files |

Although all three methods read data from a file, they differ significantly in terms of memory usage and scalability.

---

# Things to Try

- Generate a log file with thousands of entries and verify that memory usage remains stable.
- Replace the `for` loop with `read()` and compare the memory footprint.
- Process the file using `read(size)` with different chunk sizes.
- Count unique error messages.
- Generate separate reports for each log level.
- Export the report to CSV format.
- Filter logs by date or severity.
- Add support for additional log levels such as DEBUG or TRACE.