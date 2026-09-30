from langchain_community.cross_encoders import (
    HuggingFaceCrossEncoder,
)
from langchain_classic.retrievers.document_compressors import (
    CrossEncoderReranker,
)
from langchain_core.documents import Document


class RerankerService:
    def __init__(
        self,
        model_name: str,
        top_n: int,
    ):
        # Create the actual Hugging Face cross-encoder model.
        #
        # Unlike our embedding model, this model receives
        # query + document together.
        self.model = HuggingFaceCrossEncoder(
            model_name=model_name,
        )

        # LangChain wrapper responsible for:
        #
        # 1. scoring each candidate against the query
        # 2. sorting candidates by relevance
        # 3. returning only top_n documents
        self.reranker = CrossEncoderReranker(
            model=self.model,
            top_n=top_n,
        )


    def rerank(
        self,
        query: str,
        documents: list[Document],
    ) -> list[Document]:

        # compress_documents() is slightly confusingly named.
        #
        # In this case it does NOT summarize the documents.
        #
        # It:
        #   query + documents
        #       ↓
        #   cross-encoder scores
        #       ↓
        #   reorder
        #       ↓
        #   top_n documents
        reranked_documents = (
            self.reranker.compress_documents(
                documents=documents,
                query=query,
            )
        )

        return list(reranked_documents)


    def score_documents(
        self,
        query: str,
        documents: list[Document],
    ) -> list[tuple[Document, float]]:

        # Diagnostic method for learning/debugging.
        #
        # A cross encoder expects pairs:
        #
        # [
        #   (query, document1),
        #   (query, document2),
        #   ...
        # ]
        pairs = [
            (
                query,
                document.page_content,
            )
            for document in documents
        ]

        scores = self.model.score(
            pairs
        )

        scored_documents = list(
            zip(
                documents,
                scores,
            )
        )

        # Highest cross-encoder relevance score first.
        scored_documents.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scored_documents