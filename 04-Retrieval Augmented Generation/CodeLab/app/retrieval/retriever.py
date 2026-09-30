from app.embeddings.embedding_service import EmbeddingService
from app.models.document import VectorRecord
from app.vectorstore.vector_store import VectorStore
from app.retrieval.reranker import Reranker
from app.retrieval.keyword_search import KeywordSearch
from app.retrieval.query_transformer import QueryTransformer


class Retriever:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        similarity_threshold: float = 0.5,
        reranker: Reranker | None = None,
        keyword_search: KeywordSearch | None = None,
        query_transformer: QueryTransformer | None = None,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold
        self.reranker = reranker
        self.keyword_search = keyword_search
        self.query_transformer = query_transformer

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        candidate_k: int = 10,
        filters: dict[str, str] | None = None,
    ) -> list[tuple[VectorRecord, float]]:

        print("\nOriginal query:")
        print(query)

        # ---------------------------------------------------------
        # Previous approach: Single transformed query
        # ---------------------------------------------------------
        #
        # retrieval_query = (
        #     self.query_transformer.transform(query)
        # )
        #
        # One query was used for vector + keyword retrieval.
        #
        # ---------------------------------------------------------
        # Previous improvement: Multi-query retrieval
        # ---------------------------------------------------------
        #
        # retrieval_queries = (
        #     self.query_transformer.generate_queries(query)
        # )
        #
        # for retrieval_query in retrieval_queries:
        #     vector search
        #     keyword search
        #
        # merge + dedupe
        # rerank
        #
        # ---------------------------------------------------------
        # Current improvement: Query Decomposition
        # ---------------------------------------------------------
        #
        # Complex user question
        #        ↓
        # Sub-query 1
        # Sub-query 2
        #        ↓
        # Generate multiple retrieval queries for EACH sub-query
        #        ↓
        # Hybrid retrieval
        #        ↓
        # Merge all candidates
        #        ↓
        # Rerank against ORIGINAL question
        #
        # ---------------------------------------------------------

        if self.query_transformer:

            sub_queries = (
                self.query_transformer.decompose(query)
            )

        else:

            sub_queries = [query]

        print("\nDecomposed queries:")

        for index, sub_query in enumerate(
            sub_queries,
            start=1,
        ):
            print(f"{index}. {sub_query}")

        # ---------------------------------------------------------
        # Build authorized scope
        # ---------------------------------------------------------

        authorized_records = self.vector_store.records

        if filters:

            authorized_records = [
                record
                for record in authorized_records
                if all(
                    record.metadata.get(key) == value
                    for key, value in filters.items()
                )
            ]

        print("\nRetrieval filters:")

        if filters:
            for key, value in filters.items():
                print(f"{key}: {value}")
        else:
            print("None")

        # ---------------------------------------------------------
        # Collect candidates across every sub-query
        # ---------------------------------------------------------

        combined_results: dict[
            int,
            tuple[VectorRecord, float]
        ] = {}

        for sub_query in sub_queries:

            print("\n" + "#" * 60)
            print(f"Processing sub-query: {sub_query}")
            print("#" * 60)

            # -----------------------------------------------------
            # Multi-query generation for this sub-query
            # -----------------------------------------------------

            if self.query_transformer:

                retrieval_queries = (
                    self.query_transformer.generate_queries(
                        sub_query
                    )
                )

            else:

                retrieval_queries = [sub_query]

            print("\nGenerated retrieval queries:")

            for index, retrieval_query in enumerate(
                retrieval_queries,
                start=1,
            ):
                print(f"{index}. {retrieval_query}")

            # -----------------------------------------------------
            # Hybrid retrieval for every generated query
            # -----------------------------------------------------

            for retrieval_query in retrieval_queries:

                print("\n" + "=" * 60)
                print(
                    f"Retrieving for: {retrieval_query}"
                )
                print("=" * 60)

                # -------------------------------------------------
                # Vector search
                # -------------------------------------------------

                query_vector = (
                    self.embedding_service.embed(
                        retrieval_query
                    )
                )

                vector_results = (
                    self.vector_store.search(
                        query_vector,
                        top_k=candidate_k,
                        filters=filters,
                    )
                )

                print("\nVector search candidates:")

                for record, score in vector_results:

                    print(
                        f"Vector score: {score:.4f}"
                    )

                    print(
                        "Source:",
                        record.metadata.get(
                            "filename",
                            "unknown",
                        ),
                    )

                    print(record.content)
                    print("-" * 50)

                    record_id = id(record)

                    if record_id not in combined_results:

                        combined_results[record_id] = (
                            record,
                            score,
                        )

                    else:

                        (
                            existing_record,
                            existing_score,
                        ) = combined_results[record_id]

                        # Keep the highest vector score when
                        # the same chunk is found by different
                        # generated queries.
                        if score > existing_score:

                            combined_results[
                                record_id
                            ] = (
                                existing_record,
                                score,
                            )

                # -------------------------------------------------
                # Keyword search
                # -------------------------------------------------

                keyword_results: list[
                    VectorRecord
                ] = []

                if self.keyword_search:

                    keyword_results = (
                        self.keyword_search.search(
                            query=retrieval_query,
                            records=authorized_records,
                        )
                    )

                print(
                    "\nKeyword search candidates:"
                )

                if keyword_results:

                    for record in keyword_results:

                        print(
                            "Source:",
                            record.metadata.get(
                                "filename",
                                "unknown",
                            ),
                        )

                        print(record.content)
                        print("-" * 50)

                        record_id = id(record)

                        if (
                            record_id
                            not in combined_results
                        ):

                            # 0.0 means this candidate entered
                            # through keyword retrieval and has
                            # no vector similarity score yet.
                            combined_results[
                                record_id
                            ] = (
                                record,
                                0.0,
                            )

                else:

                    print("None")

        # ---------------------------------------------------------
        # Merge + dedupe complete
        # ---------------------------------------------------------

        combined_candidates = list(
            combined_results.values()
        )

        print("\n" + "=" * 60)
        print(
            "Combined decomposition + multi-query "
            "hybrid candidates:"
        )
        print("=" * 60)

        for record, score in combined_candidates:

            print(
                f"Initial score: {score:.4f}"
            )

            print(
                "Source:",
                record.metadata.get(
                    "filename",
                    "unknown",
                ),
            )

            print(record.content)
            print("-" * 50)

        # ---------------------------------------------------------
        # Cross-encoder reranking
        # ---------------------------------------------------------
        #
        # IMPORTANT:
        #
        # We still use the ORIGINAL user question.
        #
        # Sub-queries and generated queries exist only to improve
        # candidate retrieval.
        # ---------------------------------------------------------

        if self.reranker:

            reranked_results = (
                self.reranker.rerank(
                    query=query,
                    candidates=combined_candidates,
                    top_k=top_k,
                )
            )

        else:

            reranked_results = (
                combined_candidates[:top_k]
            )

        print("\nAfter reranking:")

        for record, score in reranked_results:

            print(
                f"Rerank score: {score:.4f}"
            )

            print(
                "Source:",
                record.metadata.get(
                    "filename",
                    "unknown",
                ),
            )

            print(record.content)
            print("-" * 50)

        return reranked_results