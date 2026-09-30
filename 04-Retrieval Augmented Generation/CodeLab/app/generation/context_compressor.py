import re

from app.models.document import VectorRecord


class ContextCompressor:

    def compress(
        self,
        query: str,
        results: list[tuple[VectorRecord, float]],
    ) -> list[tuple[VectorRecord, float]]:

        query_terms = self._tokenize(query)

        compressed_results = []

        for record, score in results:

            sentences = self._split_sentences(
                record.content
            )

            relevant_sentences = []

            for sentence in sentences:

                sentence_terms = self._tokenize(
                    sentence
                )

                if query_terms.intersection(
                    sentence_terms
                ):
                    relevant_sentences.append(
                        sentence.strip()
                    )

            # If compression removed everything,
            # keep the original chunk.
            #
            # This prevents useful information from
            # disappearing because of a weak rule.
            compressed_content = (
                " ".join(relevant_sentences)
                if relevant_sentences
                else record.content
            )

            compressed_record = VectorRecord(
                content=compressed_content,
                embedding=record.embedding,
                metadata=record.metadata,
            )

            compressed_results.append(
                (
                    compressed_record,
                    score,
                )
            )

        return compressed_results

    @staticmethod
    def _tokenize(text: str) -> set[str]:

        return set(
            re.findall(
                r"\b\w+\b",
                text.lower(),
            )
        )

    @staticmethod
    def _split_sentences(
        text: str,
    ) -> list[str]:

        return re.split(
            r"(?<=[.!?])\s+",
            text.strip(),
        )