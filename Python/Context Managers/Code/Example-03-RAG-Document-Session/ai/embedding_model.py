"""
Embedding Model

Author: GenAI Learning Roadmap
"""

from utils.logger import logger


class EmbeddingModel:
    """Simulates an embedding model."""

    def load(self) -> None:
        logger.info("Loading embedding model...")

    def generate_embeddings(
        self,
        text: str,
    ) -> list[float]:
        logger.info("Generating embeddings...")

        # Simulated embedding vector
        return [0.21, 0.53, 0.76, 0.44]

    def unload(self) -> None:
        logger.info("Unloading embedding model...")