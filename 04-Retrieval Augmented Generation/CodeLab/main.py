from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.embeddings.embedding_service import EmbeddingService
from app.models.document import VectorRecord
from app.vectorstore.vector_store import VectorStore

from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker
from app.retrieval.keyword_search import KeywordSearch
from app.retrieval.query_transformer import QueryTransformer

from app.generation.context_builder import ContextBuilder
from app.generation.context_compressor import ContextCompressor
from app.generation.prompt import PromptBuilder
from app.generation.llm_service import LLMService

from app.evaluation.evaluation import RAGEvaluator


def main():

    # =========================================================
    # INGESTION PIPELINE
    # =========================================================

    loader = DocumentLoader()

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    documents = loader.load(
        "data/documents"
    )

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

    print(
        "Total vectors:",
        vector_store.count(),
    )

    # =========================================================
    # RETRIEVAL COMPONENTS
    # =========================================================

    reranker = Reranker()

    keyword_search = KeywordSearch()

    query_transformer = QueryTransformer()

    retriever = Retriever(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.5,
        reranker=reranker,
        keyword_search=keyword_search,
        query_transformer=query_transformer,
    )

    # =========================================================
    # GENERATION COMPONENTS
    # =========================================================

    context_compressor = ContextCompressor()

    context_builder = ContextBuilder()

    prompt_builder = PromptBuilder()

    llm = LLMService()

    # =========================================================
    # PREVIOUS APPROACH:
    # MANUAL SINGLE-QUERY RAG TEST
    # =========================================================
    #
    # This was our previous end-to-end test.
    #
    # It demonstrated:
    #
    # - Query decomposition
    # - Multi-query retrieval
    # - Hybrid search
    # - Merge + dedupe
    # - Cross-encoder reranking
    # - Context compression
    # - Context building
    # - Prompt building
    # - LLM generation
    #
    # ---------------------------------------------------------
    #
    # query = (
    #     "How long was the study for Treatment C "
    #     "and what was the primary success criterion?"
    # )
    #
    # results = retriever.retrieve(
    #     query=query,
    #     top_k=4,
    #     candidate_k=10,
    #     filters={
    #         "study_id": "STUDY-003",
    #     },
    # )
    #
    # print("\nRetrieved chunks:\n")
    #
    # for record, score in results:
    #
    #     print(
    #         f"Score: {score:.4f}"
    #     )
    #
    #     print(record.content)
    #
    #     print(
    #         "Source:",
    #         record.metadata.get(
    #             "filename",
    #         ),
    #     )
    #
    #     print("-" * 50)
    #
    # ---------------------------------------------------------
    # Previous approach before context compression:
    # ---------------------------------------------------------
    #
    # context = context_builder.build(
    #     results
    # )
    #
    # This sent entire retrieved chunks directly
    # to the LLM.
    #
    # ---------------------------------------------------------
    # Improved approach: Context Compression
    # ---------------------------------------------------------
    #
    # compressed_results = context_compressor.compress(
    #     query=query,
    #     results=results,
    # )
    #
    # print("\nCompressed chunks:\n")
    #
    # for record, score in compressed_results:
    #
    #     print(
    #         f"Score: {score:.4f}"
    #     )
    #
    #     print(record.content)
    #
    #     print(
    #         "Source:",
    #         record.metadata.get(
    #             "filename",
    #         ),
    #     )
    #
    #     print("-" * 50)
    #
    # context = context_builder.build(
    #     compressed_results
    # )
    #
    # prompt = prompt_builder.build(
    #     question=query,
    #     context=context,
    # )
    #
    # answer = llm.generate(
    #     prompt
    # )
    #
    # print("\nAnswer:")
    # print(answer)
    #
    # =========================================================
    # Limitation of manual testing
    # =========================================================
    #
    # We were visually inspecting one answer and deciding:
    #
    # "The answer looks correct."
    #
    # This does not scale and does not allow us to compare
    # retrieval strategies systematically.
    #
    # =========================================================


    # =========================================================
    # CURRENT APPROACH:
    # RAG EVALUATION DATASET
    # =========================================================
    #
    # Each evaluation case contains:
    #
    # question
    #     → user question
    #
    # expected_answers
    #     → facts expected in final LLM answer
    #
    # expected_terms
    #     → evidence terms expected in retrieval
    #
    # study_id
    #     → authorized metadata scope
    #
    # =========================================================

    evaluation_cases = [
        {
            "question": (
                "How long was the study "
                "for Treatment C?"
            ),
            "expected_answers": [
                "36 months",
            ],
            "expected_terms": [
                "study duration",
                "36 months",
            ],
            "study_id": "STUDY-003",
        },
        {
            "question": (
                "What was the primary success criterion "
                "for Treatment C?"
            ),
            "expected_answers": [
                "30 percent",
            ],
            "expected_terms": [
                "improvement",
                "recovery time",
                "30 percent",
            ],
            "study_id": "STUDY-003",
        },
        {
            "question": (
                "How long was the study for Treatment C "
                "and what was the primary success criterion?"
            ),
            "expected_answers": [
                "36 months",
                "30 percent",
            ],
            "expected_terms": [
                "36 months",
                "improvement",
                "recovery time",
                "30 percent",
            ],
            "study_id": "STUDY-003",
        },
    ]

    # =========================================================
    # RAG EVALUATOR
    # =========================================================

    evaluator = RAGEvaluator()

    print("\n")
    print("=" * 70)
    print("RAG EVALUATION")
    print("=" * 70)

    passed = 0

    total_cases = len(
        evaluation_cases
    )

    # ---------------------------------------------------------
    # Used later to calculate Mean Reciprocal Rank (MRR)
    # across all evaluation cases.
    # ---------------------------------------------------------

    reciprocal_ranks = []

    # =========================================================
    # RUN EACH EVALUATION CASE
    # =========================================================

    for index, case in enumerate(
        evaluation_cases,
        start=1,
    ):

        question = case["question"]

        print("\n")
        print("=" * 70)
        print(
            f"Evaluation Case {index}"
        )
        print("=" * 70)

        print(
            "\nQuestion:"
        )

        print(
            question
        )

        # -----------------------------------------------------
        # Step 1: Retrieval
        # -----------------------------------------------------

        results = retriever.retrieve(
            query=question,
            top_k=4,
            candidate_k=10,
            filters={
                "study_id": case[
                    "study_id"
                ],
            },
        )

        # -----------------------------------------------------
        # Step 2: Context Compression
        # -----------------------------------------------------

        compressed_results = (
            context_compressor.compress(
                query=question,
                results=results,
            )
        )

        # -----------------------------------------------------
        # Step 3: Context Building
        # -----------------------------------------------------

        context = context_builder.build(
            compressed_results
        )

        # -----------------------------------------------------
        # Step 4: Prompt Building
        # -----------------------------------------------------

        prompt = prompt_builder.build(
            question=question,
            context=context,
        )

        # -----------------------------------------------------
        # Step 5: Generation
        # -----------------------------------------------------

        answer = llm.generate(
            prompt
        )

        # =====================================================
        # BASIC EVALUATION
        # =====================================================

        # -----------------------------------------------------
        # Step 6: Retrieval Evaluation
        #
        # Did the retrieved chunks contain all expected
        # evidence terms?
        # -----------------------------------------------------

        retrieval_passed = (
            evaluator.evaluate_retrieval(
                results=results,
                expected_terms=case[
                    "expected_terms"
                ],
            )
        )

        # -----------------------------------------------------
        # Step 7: Answer Evaluation
        #
        # Did the generated answer contain all expected facts?
        # -----------------------------------------------------

        answer_passed = (
            evaluator.evaluate_answer(
                answer=answer,
                expected_answers=case[
                    "expected_answers"
                ],
            )
        )

        # =====================================================
        # RETRIEVAL METRICS
        # =====================================================

        # -----------------------------------------------------
        # Precision@3
        #
        # Of the top 3 retrieved chunks,
        # how many appear relevant?
        # -----------------------------------------------------

        precision_at_3 = (
            evaluator.precision_at_k(
                results=results,
                relevant_terms=case[
                    "expected_terms"
                ],
                k=3,
            )
        )

        # -----------------------------------------------------
        # Recall@3
        #
        # Of the expected retrieval evidence,
        # how much appeared in the top 3?
        # -----------------------------------------------------

        recall_at_3 = (
            evaluator.recall_at_k(
                results=results,
                relevant_terms=case[
                    "expected_terms"
                ],
                k=3,
            )
        )

        # -----------------------------------------------------
        # Reciprocal Rank
        #
        # Measures how high the first relevant chunk appears.
        #
        # Rank 1 → 1.0
        # Rank 2 → 0.5
        # Rank 3 → 0.333...
        # -----------------------------------------------------

        reciprocal_rank = (
            evaluator.reciprocal_rank(
                results=results,
                relevant_terms=case[
                    "expected_terms"
                ],
            )
        )

        reciprocal_ranks.append(
            reciprocal_rank
        )

        # =====================================================
        # PRINT CASE RESULTS
        # =====================================================

        print(
            "\nGenerated Answer:"
        )

        print(
            answer
        )

        print(
            "\nExpected Answers:"
        )

        for expected in case[
            "expected_answers"
        ]:
            print(
                f"- {expected}"
            )

        print(
            "\nExpected Retrieval Terms:"
        )

        for term in case[
            "expected_terms"
        ]:
            print(
                f"- {term}"
            )

        print(
            "\nRetrieval passed:",
            retrieval_passed,
        )

        print(
            "Answer passed:",
            answer_passed,
        )

        print(
            f"Precision@3: "
            f"{precision_at_3:.4f}"
        )

        print(
            f"Recall@3: "
            f"{recall_at_3:.4f}"
        )

        print(
            f"Reciprocal Rank: "
            f"{reciprocal_rank:.4f}"
        )

        # -----------------------------------------------------
        # Case passes only when BOTH retrieval and generation
        # checks pass.
        # -----------------------------------------------------

        if (
            retrieval_passed
            and answer_passed
        ):

            passed += 1

            print(
                "\nCase Result: PASS"
            )

        else:

            print(
                "\nCase Result: FAIL"
            )

    # =========================================================
    # FINAL EVALUATION SUMMARY
    # =========================================================

    print("\n")
    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Passed: "
        f"{passed}/{total_cases}"
    )

    success_rate = (
        passed / total_cases
        if total_cases
        else 0
    )

    print(
        f"Success Rate: "
        f"{success_rate:.2%}"
    )

    # ---------------------------------------------------------
    # Mean Reciprocal Rank
    #
    # MRR = average reciprocal rank across all queries.
    # ---------------------------------------------------------

    mrr = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
        if reciprocal_ranks
        else 0.0
    )

    print(
        f"MRR: {mrr:.4f}"
    )

    # =========================================================
    # CURRENT EVALUATION CAPABILITIES
    # =========================================================
    #
    # We now measure:
    #
    # ✅ Expected retrieval evidence
    # ✅ Expected answer facts
    # ✅ Precision@K
    # ✅ Recall@K
    # ✅ Reciprocal Rank
    # ✅ Mean Reciprocal Rank (MRR)
    #
    # ---------------------------------------------------------
    # Still remaining:
    # ---------------------------------------------------------
    #
    # - Faithfulness / groundedness
    # - Semantic answer correctness
    # - Hallucination detection
    #
    # IMPORTANT:
    #
    # Precision@K and Recall@K in this CodeLab currently use
    # expected textual evidence terms as an approximation.
    #
    # A production evaluation dataset would normally define
    # ground-truth relevant document/chunk IDs.
    #
    # =========================================================


if __name__ == "__main__":
    main()  