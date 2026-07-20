"""
Application Entry Point

Author: GenAI Learning Roadmap
"""

from ai.rag_session import RagSession
from models.document import Document
from services.document_processing_service import (
    DocumentProcessingService,
)


def main() -> None:

    document = Document(
        file_name="Income_Tax_Rules.pdf",
    )

    service = DocumentProcessingService()

    with RagSession() as session:

        service.process_document(
            session,
            document,
        )


if __name__ == "__main__":
    main()