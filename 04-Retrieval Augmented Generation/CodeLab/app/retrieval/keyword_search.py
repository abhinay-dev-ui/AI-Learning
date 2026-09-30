import re

from app.models.document import VectorRecord


class KeywordSearch:

    def search(
        self,
        query: str,
        records: list[VectorRecord],
    ) -> list[VectorRecord]:

        query_terms = self._tokenize(query)

        results = []

        for record in records:
            document_terms = self._tokenize(record.content)

            if query_terms.intersection(document_terms):
                results.append(record)

        return results

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(
            re.findall(r"\b\w+\b", text.lower())
        )