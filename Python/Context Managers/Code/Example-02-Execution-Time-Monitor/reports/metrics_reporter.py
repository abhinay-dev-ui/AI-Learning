"""
Metrics Reporter

Responsible for reporting execution metrics.

Author: GenAI Learning Roadmap
"""

from utils.logger import logger


class MetricsReporter:
    """Reports execution metrics."""

    def report(self, operation: str, duration: float) -> None:
        logger.success(
            f"{operation} completed in {duration:.4f} seconds."
        )