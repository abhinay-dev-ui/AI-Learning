"""
RAG Session Context Manager

Author: GenAI Learning Roadmap
"""

from ai.embedding_model import EmbeddingModel
from ai.vector_database import VectorDatabase


class RagSession:
    """
    Context Manager responsible for coordinating
    AI infrastructure resources.
    """

    def __init__(self) -> None:

        self.embedding_model = EmbeddingModel()
        self.vector_database = VectorDatabase()

    def __enter__(self) -> "RagSession":

        self.embedding_model.load()
        self.vector_database.connect()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:

        self.vector_database.disconnect()
        self.embedding_model.unload()

        return False