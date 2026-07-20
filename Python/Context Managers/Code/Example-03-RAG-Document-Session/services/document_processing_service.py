"""
Document Processing Service

Author: GenAI Learning Roadmap
"""

from ai.rag_session import RagSession
from models.document import Document
from utils.logger import logger


class DocumentProcessingService:
    """Processes documents using a RAG session."""

    def process_document(
        self,
        session: RagSession,
        document: Document,
    ) -> None:

        logger.info(
            f"Reading '{document.file_name}'..."
        )

        text = (
            "Income Tax Rules extracted from PDF."
        )

        embeddings = (
            session.embedding_model.generate_embeddings(
                text
            )
        )

        session.vector_database.store_embeddings(
            document.file_name,
            embeddings,
        )