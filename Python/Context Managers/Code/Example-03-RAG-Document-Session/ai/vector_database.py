"""
Vector Database

Author: GenAI Learning Roadmap
"""

from utils.logger import logger


class VectorDatabase:
    """Simulates a vector database."""

    def connect(self) -> None:
        logger.info("Connecting to vector database...")

    def store_embeddings(
        self,
        document_name: str,
        embeddings: list[float],
    ) -> None:

        logger.info(
            f"Saving embeddings for '{document_name}'..."
        )

    def disconnect(self) -> None:
        logger.info("Disconnecting vector database...")