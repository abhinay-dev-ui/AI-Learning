from collections import defaultdict

from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


class DocumentSplitter:
    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        documents: list[Document],
    ) -> list[Document]:

        chunks = self.splitter.split_documents(
            documents
        )

        source_indexes: dict[str, int] = defaultdict(int)

        for chunk in chunks:
            source = chunk.metadata.get(
                "source",
                "unknown",
            )

            chunk.metadata["chunk_index"] = (
                source_indexes[source]
            )

            source_indexes[source] += 1

        return chunks