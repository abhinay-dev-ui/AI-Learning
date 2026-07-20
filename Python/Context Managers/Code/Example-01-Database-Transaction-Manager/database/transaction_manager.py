"""
Database Transaction Manager

Implements a Context Manager responsible for managing
the complete lifecycle of a database transaction.

Author: GenAI Learning Roadmap
"""

from database.connection import DatabaseConnection


class TransactionManager:
    """Context Manager for database transactions."""

    def __init__(self) -> None:
        self.connection = DatabaseConnection()

    def __enter__(self) -> DatabaseConnection:
        """
        Acquire the database connection and begin a transaction.
        """

        self.connection.connect()
        self.connection.begin_transaction()

        return self.connection

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ) -> bool:
        """
        Commit the transaction if no exception occurred.
        Otherwise, rollback the transaction.

        Always close the database connection.
        """

        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()

        finally:
            self.connection.close()

        # Propagate exceptions to the caller.
        return False