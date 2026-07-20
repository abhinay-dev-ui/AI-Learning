"""
Database Connection

This module simulates a production database connection.
The Context Manager will use this class to manage the
transaction lifecycle.

Author: GenAI Learning Roadmap
"""

from utils.logger import logger


class DatabaseConnection:
    """Represents a database connection."""

    def __init__(self) -> None:
        self.connected = False
        self.transaction_started = False

    def connect(self) -> None:
        """Open database connection."""

        logger.info("Opening database connection...")
        self.connected = True

    def begin_transaction(self) -> None:
        """Start a database transaction."""

        logger.info("Beginning transaction...")
        self.transaction_started = True

    def execute(self, query: str) -> None:
        """Execute SQL statement."""

        if not self.connected:
            raise RuntimeError("Database connection is not open.")

        logger.info(f"Executing SQL -> {query}")

    def commit(self) -> None:
        """Commit current transaction."""

        if self.transaction_started:
            logger.success("Transaction committed.")

    def rollback(self) -> None:
        """Rollback current transaction."""

        if self.transaction_started:
            logger.error("Transaction rolled back.")

    def close(self) -> None:
        """Close database connection."""

        if self.connected:
            logger.info("Closing database connection...")

        self.connected = False
        self.transaction_started = False