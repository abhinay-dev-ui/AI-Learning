"""
Document Model

Author: GenAI Learning Roadmap
"""


class Document:
    """Represents a document to be processed."""

    def __init__(
        self,
        file_name: str,
    ) -> None:
        self.file_name = file_name