from app.models.document import Document


class DocumentChunker:

    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 40):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, document: Document) -> list[Document]:
        content = document.content

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(content):
            end = start + self.chunk_size
            chunk_content = content[start:end]

            metadata = {
                **document.metadata,
                "chunk_index": chunk_index,
            }

            chunks.append(
                Document(
                    content=chunk_content,
                    metadata=metadata,
                )
            )

            chunk_index += 1

            start += self.chunk_size - self.chunk_overlap

        return chunks