
from sentence_transformers import CrossEncoder

from app.models.document import VectorRecord


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: list[tuple[VectorRecord, float]],
        top_k: int = 3,
    ) -> list[tuple[VectorRecord, float]]:

        pairs = [
            [query, record.content]
            for record, _ in candidates
        ]

        scores = self.model.predict(pairs)

        reranked = [
            (record, float(score))
            for (record, _), score in zip(candidates, scores)
        ]

        reranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return reranked[:top_k]



# Below code for bi-coding Reranker and will replace the same with Cross Reranker
# import re

# from app.models.document import VectorRecord


# class Reranker:

#     def rerank(
#         self,
#         query: str,
#         candidates: list[tuple[VectorRecord, float]],
#         top_k: int = 3,
#     ) -> list[tuple[VectorRecord, float]]:

#         query_terms = self._tokenize(query)

#         reranked = []

#         for record, similarity_score in candidates:

#             document_terms = self._tokenize(record.content)

#             matched_terms = query_terms.intersection(document_terms)

#             relevance_score = (
#                 len(matched_terms) / len(query_terms)
#                 if query_terms
#                 else 0.0
#             )

#             reranked.append(
#                 (record, relevance_score)
#             )

#         reranked.sort(
#             key=lambda item: item[1],
#             reverse=True,
#         )

#         return reranked[:top_k]

#     @staticmethod
#     def _tokenize(text: str) -> set[str]:
#         return set(
#             re.findall(
#                 r"\b\w+\b",
#                 text.lower(),
#             )
#         )