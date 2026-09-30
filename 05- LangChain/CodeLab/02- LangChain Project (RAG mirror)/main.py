from langchain_core.documents import Document

from app.chains.structured_rag_chain import (
    StructuredRAGChain,
)
from app.generation.structured_prompt import (
    StructuredPromptService,
)
from app.generation.structured_formatter import (
    StructuredContextFormatter,
)

from app.evaluation.cases import (
    EVALUATION_CASES,
)
from app.evaluation.evaluator import (
    EvaluationService,
)

from app.config import (
    CANDIDATE_K,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATA_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    RERANKER_MODEL,
    TOP_K,
)
from app.chains.rag_chain import RAGChain

from app.generation.formatter import (
    ContextFormatter,
)
from app.generation.model import (
    ModelService,
)
from app.generation.output_parser import (
    OutputParserService,
)
from app.generation.prompt import (
    PromptService,
)
from app.retrieval.reranker import (
    RerankerService,
)
from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.context_enricher import SearchContextEnricher
from app.ingestion.loader import DocumentLoader
from app.ingestion.splitter import DocumentSplitter
from app.retrieval.retriever import RetrieverService
from app.retrieval.vector_store import VectorStoreService


def main():
    # ---------------------------------------------------------
    # 1. LOAD DOCUMENTS
    # ---------------------------------------------------------

    loader = DocumentLoader()

    documents = loader.load_directory(
        DATA_DIR
    )

    print(
        f"Loaded documents: {len(documents)}"
    )

    for document in documents:
        print(
            document.metadata
        )


    # ---------------------------------------------------------
    # 2. SPLIT DOCUMENTS
    # ---------------------------------------------------------

    splitter = DocumentSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split(
        documents
    )

    print(
        f"\nTotal chunks: {len(chunks)}"
    )


    # ---------------------------------------------------------
    # 3. ENRICH CHUNKS FOR SEMANTIC SEARCH
    # ---------------------------------------------------------

    # The original chunks do not always contain enough context.
    #
    # Example:
    #
    # Original chunk:
    # "The target study duration is 36 months."
    #
    # This chunk does not explicitly mention:
    # "Treatment C"
    #
    # So we create a richer searchable representation:
    #
    # Study ID: STUDY-003
    # Treatment: Treatment C
    #
    # Content:
    # The target study duration is 36 months.
    #
    # This enriched text will be embedded and stored
    # in the vector store.
    context_enricher = SearchContextEnricher()

    search_documents = context_enricher.enrich(
        chunks
    )

    print(
        f"Search documents: {len(search_documents)}"
    )


    # ---------------------------------------------------------
    # 4. INSPECT ONE ENRICHED DOCUMENT
    # ---------------------------------------------------------

   # =========================================================
    # DIAGNOSTIC — SEARCH CONTEXT ENRICHMENT
    # =========================================================
    #
    # Added during Milestone 3 to verify that metadata such as
    # study_id and treatment was copied into the searchable
    # page_content before embedding.
    #
    # Example expected search document:
    #
    # Study ID: STUDY-003
    # Treatment: Treatment C
    #
    # Content:
    # The target study duration is 36 months.
    #
    # Re-enable this block if semantic retrieval quality changes
    # or if metadata/context enrichment needs debugging.
    #
    # example_document = next(
    #     document
    #     for document in search_documents
    #     if (
    #         document.metadata.get("study_id")
    #         == "STUDY-003"
    #         and "36 months"
    #         in document.metadata.get(
    #             "original_content",
    #             "",
    #         )
    #     )
    # )
    #
    # print(
    #     "\nExample enriched search document:"
    # )
    #
    # print(
    #     example_document.page_content
    # )
    #
    # print(
    #     f"Metadata: {example_document.metadata}"
    # )

    # ---------------------------------------------------------
    # 5. CREATE EMBEDDING MODEL
    # ---------------------------------------------------------

    embedding_service = EmbeddingService(
        model_name=EMBEDDING_MODEL
    )

    embeddings = (
        embedding_service.get_embeddings()
    )

    # Embed one small query only to verify the vector size.
    #
    # all-MiniLM-L6-v2 should produce a 384-dimensional
    # embedding vector.
    # =========================================================
    # DIAGNOSTIC — EMBEDDING DIMENSION CHECK
    # =========================================================
    #
    # Added during Milestone 2 to verify that
    # sentence-transformers/all-MiniLM-L6-v2 generates
    # 384-dimensional embeddings.
    #
    # Re-enable if the embedding model changes or if vector
    # dimension issues occur.
    #
    # test_vector = embeddings.embed_query(
    #     "study duration treatment c"
    # )
    #
    # print(
    #     f"\nEmbedding dimensions: "
    #     f"{len(test_vector)}"
    # )


    # ---------------------------------------------------------
    # 6. CREATE VECTOR STORE
    # ---------------------------------------------------------

    vector_store_service = VectorStoreService(
        embeddings=embeddings
    )


    # ---------------------------------------------------------
    # 7. INDEX ENRICHED SEARCH DOCUMENTS
    # ---------------------------------------------------------

    # Important:
    #
    # We index search_documents, NOT the original chunks.
    #
    # search_documents contain:
    #
    # page_content
    # → enriched semantic search text
    #
    # metadata["original_content"]
    # → clean original chunk
    document_ids = (
        vector_store_service.add_documents(
            search_documents
        )
    )

    print(
        f"Indexed documents: {len(document_ids)}"
    )


    # # ---------------------------------------------------------
    # # 8. CREATE RETRIEVER SERVICE
    # # ---------------------------------------------------------

    # retriever_service = RetrieverService(
    #     vector_store=(
    #         vector_store_service.get_store()
    #     ),
    #     top_k=TOP_K,
    # )


    # # ---------------------------------------------------------
    # # 9. DEFINE QUERY + METADATA FILTER
    # # ---------------------------------------------------------

    # query = (
    #     "How long was the study for Treatment C?"
    # )

    # # For this CodeLab example, we already know the search scope.
    # #
    # # RetrieverService converts this dictionary into
    # # a callable metadata filter.
    # filters = {
    #     "study_id": "STUDY-003"
    # }


    # # ---------------------------------------------------------
    # # 10. RETRIEVE DOCUMENTS
    # # ---------------------------------------------------------

    # retrieved_documents = (
    #     retriever_service.retrieve(
    #         query=query,
    #         filters=filters,
    #     )
    # )

    # print(
    #     f"\nQuery: {query}"
    # )

    # print(
    #     f"Retrieval filters: {filters}"
    # )

    # print(
    #     f"Retrieved documents: "
    #     f"{len(retrieved_documents)}"
    # )

    # for index, document in enumerate(
    #     retrieved_documents,
    #     start=1,
    # ):
    #     print("\n---")

    #     print(
    #         f"Rank: {index}"
    #     )

    #     print(
    #         f"Metadata: {document.metadata}"
    #     )

    #     print(
    #         "Search Content:"
    #     )

    #     print(
    #         document.page_content
    #     )

    #     print(
    #         "Original Content:"
    #     )

    #     print(
    #         document.metadata.get(
    #             "original_content"
    #         )
    #     )


    # # ---------------------------------------------------------
    # # 11. FILTERED SIMILARITY SEARCH WITH SCORES
    # # ---------------------------------------------------------

    # # Retriever.invoke() returns Documents but does not expose
    # # similarity scores.
    # #
    # # For debugging/learning, call the vector store directly
    # # so we can inspect how enrichment changed the ranking.
    # print(
    #     "\nFiltered similarity search with scores:"
    # )


    # def study_filter(
    #     document: Document,
    # ) -> bool:
    #     # Return True only for STUDY-003 chunks.
    #     return (
    #         document.metadata.get("study_id")
    #         == "STUDY-003"
    #     )


    # results_with_scores = (
    #     vector_store_service
    #     .get_store()
    #     .similarity_search_with_score(
    #         query,
    #         k=4,
    #         filter=study_filter,
    #     )
    # )

    # for index, (
    #     document,
    #     score,
    # ) in enumerate(
    #     results_with_scores,
    #     start=1,
    # ):
    #     print("\n---")

    #     print(
    #         f"Rank: {index}"
    #     )

    #     print(
    #         f"Score: {score:.4f}"
    #     )

    #     print(
    #         f"Metadata: {document.metadata}"
    #     )

    #     print(
    #         "Search Content:"
    #     )

    #     print(
    #         document.page_content
    #     )

    #     print(
    #         "Original Content:"
    #     )

    #     print(
    #         document.metadata.get(
    #             "original_content"
    #         )
    #     )


# ---------------------------------------------------------
# 8. CREATE RETRIEVER SERVICE
# ---------------------------------------------------------

    retriever_service = RetrieverService(
        vector_store=(
            vector_store_service.get_store()
        ),
        candidate_k=CANDIDATE_K,
    )


    # ---------------------------------------------------------
    # 9. DEFINE QUERY + METADATA FILTER
    # ---------------------------------------------------------

    query = (
        "How long was the study for Treatment C?"
    )

    # query = (
    #     "What was the average age of participants "
    #     "in Treatment C?"
    #     )

    filters = {
        "study_id": "STUDY-003"
    }


    # ---------------------------------------------------------
    # 10. RETRIEVE CANDIDATE DOCUMENTS
    # ---------------------------------------------------------
    # =========================================================
    # DIAGNOSTIC — VECTOR RETRIEVAL CANDIDATES
    # =========================================================
    #
    # Added during Milestones 3 and 4 to inspect the documents
    # returned by vector similarity BEFORE cross-encoder
    # reranking.
    #
    # Useful when debugging:
    #
    # - metadata filtering
    # - candidate_k
    # - unexpected retrieved studies
    # - semantic ranking
    # - context enrichment
    #
    # Re-enable after:
    #
    # candidate_documents = retriever_service.retrieve(...)
    #
    # for index, document in enumerate(
    #     candidate_documents,
    #     start=1,
    # ):
    #     print("\n---")
    #
    #     print(
    #         f"Vector Rank: {index}"
    #     )
    #
    #     print(
    #         f"Metadata: {document.metadata}"
    #     )
    #
    #     print(
    #         "Original Content:"
    #     )
    #
    #     print(
    #         document.metadata.get(
    #             "original_content"
    #         )
    #     )

    # ---------------------------------------------------------
    # 11. CREATE CROSS-ENCODER RERANKER
    # ---------------------------------------------------------

    reranker_service = RerankerService(
        model_name=RERANKER_MODEL,
        top_n=TOP_K,
    )


    # ---------------------------------------------------------
    # 12. INSPECT CROSS-ENCODER SCORES
    # ---------------------------------------------------------

    # =========================================================
    # DIAGNOSTIC — RAW CROSS-ENCODER SCORES
    # =========================================================
    #
    # Added during Milestone 4 to compare vector ranking with
    # cross-encoder relevance ranking.
    #
    # This calls the cross-encoder separately from rerank(),
    # meaning that enabling this diagnostic causes candidates
    # to be scored TWICE:
    #
    # score_documents()
    #       +
    # rerank()
    #
    # Therefore keep this disabled during normal execution.
    #
    # Useful for debugging:
    #
    # - poor reranking
    # - relevance thresholds
    # - no-evidence queries
    # - candidate ordering
    #
    # scored_documents = (
    #     reranker_service.score_documents(
    #         query=query,
    #         documents=candidate_documents,
    #     )
    # )
    #
    # print(
    #     "\nCross-encoder scores:"
    # )
    #
    # for index, (
    #     document,
    #     score,
    # ) in enumerate(
    #     scored_documents,
    #     start=1,
    # ):
    #     print("\n---")
    #
    #     print(
    #         f"Rerank Position: {index}"
    #     )
    #
    #     print(
    #         f"Reranker Score: {score:.4f}"
    #     )
    #
    #     print(
    #         f"Metadata: {document.metadata}"
    #     )
    #
    #     print(
    #         "Original Content:"
    #     )
    #
    #     print(
    #         document.metadata.get(
    #             "original_content"
    #         )
    #     )

    # ---------------------------------------------------------
    # 13. FINAL RERANKED DOCUMENTS
    # ---------------------------------------------------------

    # reranked_documents = (
    #     reranker_service.rerank(
    #         query=query,
    #         documents=candidate_documents,
    #     )
    # )

    # print(
    #     f"\nFinal documents: "
    #     f"{len(reranked_documents)}"
    # )


    # for index, document in enumerate(
    #     reranked_documents,
    #     start=1,
    # ):
    #     print("\n---")

    #     print(
    #         f"Final Rank: {index}"
    #     )

    #     print(
    #         f"Metadata: {document.metadata}"
    #     )

    #     print(
    #         "Original Content:"
    #     )

    #     print(
    #         document.metadata.get(
    #             "original_content"
    #         )
    #     )
    # ---------------------------------------------------------
    # 14. FORMAT RERANKED DOCUMENTS INTO LLM CONTEXT (WITHOUT LCEL)
    # ---------------------------------------------------------

    # context_formatter = ContextFormatter()

    # context = context_formatter.format(
    #     reranked_documents
    # )

    # print(
    #     "\nFormatted LLM Context:"
    # )

    # print(
    #     context
    # )


    # # ---------------------------------------------------------
    # # 15. BUILD CHAT PROMPT
    # # ---------------------------------------------------------

    # prompt_service = PromptService()

    # prompt_value = prompt_service.format_prompt(
    #     context=context,
    #     question=query,
    # )

    # print(
    #     "\nFormatted Prompt Messages:"
    # )

    # # ChatPromptValue.to_messages() returns the actual
    # # SystemMessage / HumanMessage objects.
    # for message in prompt_value.to_messages():

    #     print(
    #         f"\n{message.__class__.__name__}:"
    #     )

    #     print(
    #         message.content
    #     )


    # # ---------------------------------------------------------
    # # 16. CALL OLLAMA / MISTRAL
    # # ---------------------------------------------------------

    # model_service = ModelService(
    #     model_name=LLM_MODEL,
    #     temperature=LLM_TEMPERATURE,
    # )

    # model_response = model_service.generate(
    #     prompt_value
    # )

    # print(
    #     "\nRaw Model Response:"
    # )

    # print(
    #     model_response
    # )


    # # ---------------------------------------------------------
    # # 17. PARSE MODEL RESPONSE
    # # ---------------------------------------------------------

    # output_parser_service = (
    #     OutputParserService()
    # )

    # answer = output_parser_service.parse(
    #     model_response
    # )

    # print(
    #     "\nFinal Answer:"
    # )

    # print(
    #     answer
    # )
    # =========================================================
    # MILESTONE 6 — LCEL + RUNNABLE FREE-TEXT GENERATION
    # =========================================================
    #
    # This code was our first LCEL-based generation pipeline.
    #
    # Flow:
    #
    # reranked_documents
    #       ↓
    # RunnableLambda
    #       ↓
    # ContextFormatter
    #       ↓
    # ChatPromptTemplate
    #       ↓
    # ChatOllama
    #       ↓
    # AIMessage
    #       ↓
    # StrOutputParser
    #       ↓
    # Python str
    #
    # It is intentionally kept here for comparison with
    # Milestone 7 structured output.
    #

    # ---------------------------------------------------------
    # 14. CREATE GENERATION COMPONENTS USING LCEL
    # Commmenting due to structured Output changes
    # ---------------------------------------------------------

    # context_formatter = ContextFormatter()

    # prompt_service = PromptService()

    # model_service = ModelService(
    #     model_name=LLM_MODEL,
    #     temperature=LLM_TEMPERATURE,
    # )

    # output_parser_service = (
    #     OutputParserService()
    # )


    # # ---------------------------------------------------------
    # # 15. CREATE LCEL RAG CHAIN
    # # ---------------------------------------------------------

    # rag_chain = RAGChain(
    #     context_formatter=context_formatter,
    #     prompt_service=prompt_service,
    #     model_service=model_service,
    #     output_parser_service=(
    #         output_parser_service
    #     ),
    # )


    # # ---------------------------------------------------------
    # # 16. INVOKE LCEL CHAIN
    # # ---------------------------------------------------------

    # answer = rag_chain.invoke(
    #     documents=reranked_documents,
    #     question=query,
    # )

    # print(
    #     "\nLCEL Final Answer:"
    # )

    # print(
    #     answer
    # )


    # =========================================================
    # MILESTONE 7 — STRUCTURED OUTPUT
    # =========================================================
    #
    # Instead of returning an arbitrary string, this version
    # asks the LLM to return a result matching our StudyAnswer
    # Pydantic schema.
    #
    # Expected result:
    #
    # StudyAnswer(
    #     study_id="STUDY-003",
    #     answer="36 months",
    #     evidence_found=True,
    # )
    # =========================================================


    # ---------------------------------------------------------
    # 17. CREATE STRUCTURED GENERATION COMPONENTS
    # ---------------------------------------------------------

    context_formatter = ContextFormatter()

    structured_context_formatter = (
        StructuredContextFormatter()
    )


    structured_prompt_service = (
        StructuredPromptService()
    )

    model_service = ModelService(
        model_name=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
    )


    # ---------------------------------------------------------
    # 18. CREATE STRUCTURED LCEL RAG CHAIN
    # ---------------------------------------------------------

    structured_rag_chain = (
        StructuredRAGChain(
            context_formatter=structured_context_formatter,
            prompt_service=(
                structured_prompt_service
            ),
            model_service=model_service,
        )
    )


    # ---------------------------------------------------------
    # 19. INVOKE STRUCTURED CHAIN
    # ---------------------------------------------------------

    # structured_answer = (
    #     structured_rag_chain.invoke(
    #         documents=reranked_documents,
    #         question=query,
    #     )
    # )


    # ---------------------------------------------------------
    # 20. INSPECT STRUCTURED RESULT
    # ---------------------------------------------------------

    # =========================================================
    # MILESTONE 7 — SINGLE QUERY STRUCTURED OUTPUT
    # =========================================================
    #
    # The code below validated:
    #
    # query
    #   ↓
    # retrieval
    #   ↓
    # reranking
    #   ↓
    # structured LCEL chain
    #   ↓
    # StudyAnswer
    #
    # Positive test:
    #   duration = 36 months
    #   evidence_found = True
    #
    # Negative test:
    #   participant age
    #   evidence_found = False
    #
    # Retained for milestone history.
    #


    # print(
    #     "\nStructured Answer:"
    # )

    # print(
    #     structured_answer
    # )


    # print(
    #     "\nStructured Answer Type:"
    # )

    # print(
    #     type(structured_answer)
    # )


    # print(
    #     "\nIndividual Fields:"
    # )

    # print(
    #     f"Study ID: "
    #     f"{structured_answer.study_id}"
    # )

    # print(
    #     f"Answer: "
    #     f"{structured_answer.answer}"
    # )

    # print(
    #     f"Evidence Found: "
    #     f"{structured_answer.evidence_found}"
    # )


    # =========================================================
    # MILESTONE 8 — RAG EVALUATION HARNESS
    # =========================================================
    #
    # Instead of manually changing one query at a time,
    # execute multiple predefined evaluation cases through
    # exactly the same retrieval + reranking + generation
    # pipeline.
    #
    # For every case:
    #
    # question
    #     ↓
    # RetrieverService
    #     ↓
    # candidate documents
    #     ↓
    # RerankerService
    #     ↓
    # final documents
    #     ↓
    # StructuredRAGChain
    #     ↓
    # StudyAnswer
    #     ↓
    # EvaluationService
    #
    # We evaluate:
    #
    # 1. Did retrieval contain the expected facts?
    # 2. Did the generated answer contain them?
    # =========================================================


    evaluation_service = EvaluationService()

    evaluation_results = []


    for case in EVALUATION_CASES:

        print(
            "\n"
            "=================================================="
        )

        print(
            f"Evaluation Case: {case.name}"
        )

        print(
            f"Question: {case.question}"
        )

        print(
            f"Expected Facts: "
            f"{case.expected_facts}"
        )


        # -----------------------------------------------------
        # 1. RETRIEVE CANDIDATES
        # -----------------------------------------------------

        candidate_documents = (
            retriever_service.retrieve(
                query=case.question,
                filters=case.filters,
            )
        )


        # -----------------------------------------------------
        # 2. RERANK CANDIDATES
        # -----------------------------------------------------
        # =========================================================
        # DIAGNOSTIC — FINAL RERANKED DOCUMENTS
        # =========================================================
        #
        # Added during Milestone 4 to inspect which documents
        # survived CrossEncoderReranker top_n selection.
        #
        # Useful when:
        #
        # - the final answer is incorrect
        # - retrieval passes but generation fails
        # - expected evidence disappears during reranking
        #
        # for index, document in enumerate(
        #     final_documents,
        #     start=1,
        # ):
        #     print("\n---")
        #
        #     print(
        #         f"Final Rank: {index}"
        #     )
        #
        #     print(
        #         f"Metadata: {document.metadata}"
        #     )
        #
        #     print(
        #         "Original Content:"
        #     )
        #
        #     print(
        #         document.metadata.get(
        #             "original_content"
        #         )
        #     )

        # -----------------------------------------------------
        # RERANKING
        # -----------------------------------------------------

        final_documents = (
            reranker_service.rerank(
                query=case.question,
                documents=candidate_documents,
            )
        )

        # -----------------------------------------------------
        # 3. GENERATE STRUCTURED ANSWER
        # -----------------------------------------------------

        structured_answer = (
            structured_rag_chain.invoke(
                documents=final_documents,
                question=case.question,
            )
        )


        # -----------------------------------------------------
        # 4. EVALUATE RETRIEVAL + ANSWER
        # -----------------------------------------------------

        result = evaluation_service.evaluate(
            case=case,
            documents=final_documents,
            structured_answer=structured_answer,
        )

        evaluation_results.append(
            result
        )


        # -----------------------------------------------------
        # 5. PRINT CASE RESULT
        # -----------------------------------------------------

        print(
            f"\nAnswer: {result.answer}"
        )

        print(
            f"Evidence Found: "
            f"{result.evidence_found}"
        )

        print(
            f"Retrieval: "
            f"{'PASS' if result.retrieval_pass else 'FAIL'}"
        )

        print(
            f"Answer: "
            f"{'PASS' if result.answer_pass else 'FAIL'}"
        )

    # ---------------------------------------------------------
    # EVALUATION SUMMARY
    # ---------------------------------------------------------

    print(
        "\n"
        "=================================================="
    )

    print(
        "EVALUATION SUMMARY"
    )

    print(
        "=================================================="
    )


    total_cases = len(
        evaluation_results
    )

    retrieval_passes = sum(
        result.retrieval_pass
        for result in evaluation_results
    )

    answer_passes = sum(
        result.answer_pass
        for result in evaluation_results
    )


    print(
        f"Total Cases: {total_cases}"
    )

    print(
        f"Retrieval Passed: "
        f"{retrieval_passes}/{total_cases}"
    )

    print(
        f"Answers Passed: "
        f"{answer_passes}/{total_cases}"
    )


    for result in evaluation_results:

        print(
            "\n---"
        )

        print(
            f"Case: {result.case_name}"
        )

        print(
            f"Retrieval: "
            f"{'PASS' if result.retrieval_pass else 'FAIL'}"
        )

        print(
            f"Answer: "
            f"{'PASS' if result.answer_pass else 'FAIL'}"
        )


if __name__ == "__main__":
    main()