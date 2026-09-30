from app.models.document import VectorRecord
from app.utils.similarity import cosine_similarity


class VectorStore:

    def __init__(self):
        self.records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        self.records.append(record)

    def count(self) -> int:
        return len(self.records)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, str] | None = None, # Added optinal metadata filtering 
    ):

        candidates = self.records

        if filters:
            candidates = [
                record
                for record in candidates
                if all(
                    record.metadata.get(key) == value
                    for key, value in filters.items()
                )
            ]

        scored_results = []

        for record in candidates:

            score = cosine_similarity(
                query_vector,
                record.embedding,
            )

            scored_results.append(
                (record, score)
            )

        scored_results.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scored_results[:top_k] # we need to return all the candidates for reranking purpose