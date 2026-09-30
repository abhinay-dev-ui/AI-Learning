from langchain_core.documents import Document


class SearchContextEnricher:
    def enrich(
        self,
        documents: list[Document],
    ) -> list[Document]:

        enriched_documents: list[Document] = []

        for document in documents:

            # Keep the real source chunk.
            original_content = (
                document.page_content
            )

            # Read useful semantic context from metadata.
            study_id = document.metadata.get(
                "study_id",
                "Unknown",
            )

            treatment = document.metadata.get(
                "treatment",
                "Unknown",
            )

            # Build a richer textual representation
            # specifically for semantic embedding/search.
            #
            # The embedding model WILL see this text because
            # it becomes page_content of the indexed Document.
            searchable_content = (
                f"Study ID: {study_id}\n"
                f"Treatment: {treatment}\n\n"
                f"Content:\n"
                f"{original_content}"
            )

            # Copy metadata rather than modifying the original
            # dictionary directly.
            enriched_metadata = {
                **document.metadata,

                # Preserve the clean source chunk so later
                # generation can use it instead of the
                # enrichment text.
                "original_content": (
                    original_content
                ),
            }

            enriched_document = Document(
                page_content=searchable_content,
                metadata=enriched_metadata,
            )

            enriched_documents.append(
                enriched_document
            )

        return enriched_documents