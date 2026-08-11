from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.embeddings.embedding_service import EmbeddingService
from app.models.document import VectorRecord
from app.vectorstore.vector_store import VectorStore
from app.retrieval.retriever import Retriever
from app.generation.context_builder import ContextBuilder
from app.generation.prompt import PromptBuilder
from app.generation.llm_service import LLMService


def main():

    loader = DocumentLoader()

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    documents = loader.load("data/documents")

    for document in documents:

        chunks = chunker.split(document)

        for chunk in chunks:

            embedding = embedding_service.embed(
                chunk.content
            )

            record = VectorRecord(
                content=chunk.content,
                embedding=embedding,
                metadata=chunk.metadata,
            )

            vector_store.add(record)

    print("Total vectors:", vector_store.count())

    # Retrieval
        # ---------------------------------------------------------
    # Previous approach: Top-K only
    # ---------------------------------------------------------
    # Problem:
    # Top-K may return weak or irrelevant chunks.
    #
    # ---------------------------------------------------------
    # Experiment: Similarity threshold
    # ---------------------------------------------------------
    # A threshold can remove weak results, but a threshold
    # that is too high can remove useful supporting chunks.
    #
    # Example:
    #
    # 0.6285 → Treatment C / STUDY-003
    # 0.5281 → Study duration = 36 months
    #
    # With threshold = 0.55:
    #
    # 0.6285 → KEEP
    # 0.5281 → REMOVED
    #
    # This causes the LLM to lose the actual answer.
    #
    # Therefore:
    # Similarity threshold must be tuned based on retrieval
    # quality and should not be treated as a universal value.

    retriever = Retriever(
    embedding_service=embedding_service,
    vector_store=vector_store,
    similarity_threshold=0.5,
)

    query = "How long was the study for Treatment C?"

    results = retriever.retrieve(
        query=query,
        top_k=3,
        filters={
            "study_id": "STUDY-003",
        },
    )
    print("\nRetrieved chunks:\n")

    for record, score in results:
        print(f"Score: {score:.4f}")
        print(record.content)
        print("Source:", record.metadata.get("filename"))
        print("-" * 50)


    context_builder = ContextBuilder()

    context = context_builder.build(results)

    prompt_builder = PromptBuilder()

    prompt = prompt_builder.build(
        question=query,
        context=context,
    )

    llm = LLMService()

    answer = llm.generate(prompt)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()