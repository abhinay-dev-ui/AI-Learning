from langchain_core.documents import Document


class StructuredContextFormatter:
    def format(
        self,
        documents: list[Document],
    ) -> str:

        context_parts: list[str] = []

        for document in documents:
            original_content = (
                document.metadata.get(
                    "original_content",
                    document.page_content,
                )
            )

            study_id = document.metadata.get(
                "study_id",
                "Unknown",
            )

            treatment = document.metadata.get(
                "treatment",
                "Unknown",
            )

            context_part = (
                f"Study ID: {study_id}\n"
                f"Treatment: {treatment}\n"
                f"Content: {original_content}"
            )

            context_parts.append(
                context_part
            )

        return "\n\n".join(
            context_parts
        )