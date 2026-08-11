from app.embeddings.embedding_service import EmbeddingService
from app.models.document import VectorRecord
from app.vectorstore.vector_store import VectorStore


class Retriever:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        similarity_threshold: float = 0.5,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        filters: dict[str, str] | None = None,
    ) -> list[tuple[VectorRecord, float]]:

        query_vector = self.embedding_service.embed(query)

        # ---------------------------------------------------------
        # Previous approach: Top-K only
        # ---------------------------------------------------------
        # We returned the top K results regardless of their
        # relevance.
        #
        # Example:
        #   STUDY-003 → 0.6285  relevant
        #   STUDY-003 → 0.5281  relevant
        #   STUDY-001 → 0.5234  irrelevant
        #
        # Problem:
        # top_k=3 guarantees that 3 results are returned even
        # when some results have weak similarity.
        #
        # results = self.vector_store.search(
        #     query_vector,
        #     top_k=top_k,
        # )

        # ---------------------------------------------------------
        # Improved approach: Top-K + Similarity Threshold
        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # Step 1: Retrieve Top-K candidates
        # ---------------------------------------------------------

        candidate_results = self.vector_store.search(
            query_vector,
            top_k=top_k,
            filters=filters,
        )

        print("\nRetrieval filters:")
    
        if filters:
            for key, value in filters.items():
                print(f"{key}: {value}")
        else:
            print("None")

        print("\nTop-K candidates:")

        for record, score in candidate_results:
            print(f"Score: {score:.4f}")
            print(f"Source: {record.metadata.get('filename', 'unknown')}")
            print(record.content)
            print("-" * 50)


        # ---------------------------------------------------------
        # Step 2: Apply similarity threshold
        # ---------------------------------------------------------

        filtered_results = [
            (record, score)
            for record, score in candidate_results
            if score >= self.similarity_threshold
        ]

        print("\nAfter similarity threshold:")

        for record, score in filtered_results:
            print(f"Score: {score:.4f}")
            print(f"Source: {record.metadata.get('filename', 'unknown')}")
            print(record.content)
            print("-" * 50)

        return filtered_results