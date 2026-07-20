"""
Performance Timer

Measures execution time using a Context Manager.

Author: GenAI Learning Roadmap
"""

import time

from reports.metrics_reporter import MetricsReporter


class PerformanceTimer:
    """Context Manager for measuring execution time."""

    def __init__(self, operation: str) -> None:
        self.operation = operation
        self.start_time = 0.0
        self.end_time = 0.0
        self.duration = 0.0

        self.reporter = MetricsReporter()

    def __enter__(self) -> "PerformanceTimer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

        self.reporter.report(
            self.operation,
            self.duration,
        )

        return False