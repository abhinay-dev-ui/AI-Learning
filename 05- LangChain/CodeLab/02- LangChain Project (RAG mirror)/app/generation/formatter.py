from langchain_core.documents import Document


class ContextFormatter:
    def format(
        self,
        documents: list[Document],
    ) -> str:

        context_parts: list[str] = []

        for document in documents:

            # We deliberately use original_content.
            #
            # page_content contains our enriched SEARCH text:
            #
            # Study ID: ...
            # Treatment: ...
            # Content: ...
            #
            # But the LLM should receive the clean source chunk.
            original_content = (
                document.metadata.get(
                    "original_content",
                    document.page_content,
                )
            )

            context_parts.append(
                original_content
            )

        # Combine all retrieved evidence into one context string.
        #
        # "\n\n" places a blank line between chunks.
        return "\n\n".join(
            context_parts
        )