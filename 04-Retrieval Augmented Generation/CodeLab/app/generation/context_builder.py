from app.models.document import VectorRecord


class ContextBuilder:

    def build(
        self,
        results: list[tuple[VectorRecord, float]],
    ) -> str:

        context_parts = []

        for record, score in results:

            source = record.metadata.get(
                "filename",
                "unknown",
            )

            context_parts.append(
                f"[Source: {source}]\n"
                f"{record.content}"
            )

        return "\n\n".join(context_parts)