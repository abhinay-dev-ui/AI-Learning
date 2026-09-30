# from collections.abc import Callable

# from langchain_core.documents import Document
# from langchain_core.vectorstores import (
#     InMemoryVectorStore,
#     VectorStoreRetriever,
# )


# class RetrieverService:
#     def __init__(
#         self,
#         vector_store: InMemoryVectorStore,
#         top_k: int,
#     ):
#         # Keep the vector store because retrieval filters
#         # may change for every request.
#         #
#         # Example:
#         # Request 1 -> STUDY-001
#         # Request 2 -> STUDY-003
#         self.vector_store = vector_store
#         self.top_k = top_k

#     def retrieve(
#         self,
#         query: str,
#         filters: dict[str, str] | None = None,
#     ) -> list[Document]:

#         # Convert our application's simple metadata dictionary:
#         #
#         # {"study_id": "STUDY-003"}
#         #
#         # into the callable filter expected by
#         # InMemoryVectorStore.
#         metadata_filter = self._build_filter(
#             filters
#         )

#         # Create a Retriever configured for THIS request.
#         #
#         # search_kwargs are forwarded to the underlying
#         # vector-store similarity search.
#         search_kwargs = {
#             "k": self.top_k,
#         }

#         # Only add the filter when one was supplied.
#         if metadata_filter is not None:
#             search_kwargs["filter"] = metadata_filter

#         retriever: VectorStoreRetriever = (
#             self.vector_store.as_retriever(
#                 search_type="similarity",
#                 search_kwargs=search_kwargs,
#             )
#         )

#         # Retriever is a Runnable.
#         #
#         # Input:
#         #   query: str
#         #
#         # Output:
#         #   list[Document]
#         return retriever.invoke(query)

#     def _build_filter(
#         self,
#         filters: dict[str, str] | None,
#     ) -> Callable[[Document], bool] | None:

#         if not filters:
#             return None

#         def metadata_filter(
#             document: Document,
#         ) -> bool:

#             # all(...) returns True only when EVERY requested
#             # metadata condition matches.
#             #
#             # Example:
#             #
#             # filters =
#             # {"study_id": "STUDY-003"}
#             #
#             # STUDY-003 chunk -> True
#             # STUDY-002 chunk -> False
#             return all(
#                 document.metadata.get(key) == value
#                 for key, value in filters.items()
#             )

#         return metadata_filter

from collections.abc import Callable

from langchain_core.documents import Document
from langchain_core.vectorstores import (
    InMemoryVectorStore,
    VectorStoreRetriever,
)


class RetrieverService:
    def __init__(
        self,
        vector_store: InMemoryVectorStore,
        candidate_k: int,
    ):
        # Vector retrieval returns a larger candidate set.
        #
        # These candidates will later be sent to the
        # cross-encoder reranker.
        self.vector_store = vector_store
        self.candidate_k = candidate_k


    def retrieve(
        self,
        query: str,
        filters: dict[str, str] | None = None,
    ) -> list[Document]:

        metadata_filter = self._build_filter(
            filters
        )

        search_kwargs = {
            "k": self.candidate_k,
        }

        if metadata_filter is not None:
            search_kwargs["filter"] = (
                metadata_filter
            )

        retriever: VectorStoreRetriever = (
            self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs=search_kwargs,
            )
        )

        return retriever.invoke(query)


    def _build_filter(
        self,
        filters: dict[str, str] | None,
    ) -> Callable[[Document], bool] | None:

        if not filters:
            return None

        def metadata_filter(
            document: Document,
        ) -> bool:

            return all(
                document.metadata.get(key)
                == value

                for key, value
                in filters.items()
            )

        return metadata_filter