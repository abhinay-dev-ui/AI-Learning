"""
PDF Processing Service

Simulates processing a large PDF document.

Author: GenAI Learning Roadmap
"""

import time

from utils.logger import logger


class PdfProcessingService:
    """Business logic for PDF processing."""

    def process_document(self) -> None:
        self._extract_text()
        self._generate_embeddings()
        self._store_embeddings()

    def _extract_text(self) -> None:
        logger.info("Extracting text from PDF...")
        time.sleep(1)

    def _generate_embeddings(self) -> None:
        logger.info("Generating embeddings...")
        time.sleep(2)

    def _store_embeddings(self) -> None:
        logger.info("Storing embeddings...")
        time.sleep(1)