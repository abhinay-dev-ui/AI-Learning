class RAGEvaluator:

    # ---------------------------------------------------------
    # Existing evaluation:
    # Check whether all expected answer facts are present.
    # ---------------------------------------------------------

    def evaluate_answer(
        self,
        answer: str,
        expected_answers: list[str],
    ) -> bool:

        normalized_answer = answer.lower()

        return all(
            expected.lower() in normalized_answer
            for expected in expected_answers
        )

    # ---------------------------------------------------------
    # Existing evaluation:
    # Check whether expected retrieval evidence appears
    # anywhere across retrieved chunks.
    # ---------------------------------------------------------

    def evaluate_retrieval(
        self,
        results,
        expected_terms: list[str],
    ) -> bool:

        retrieved_text = " ".join(
            record.content.lower()
            for record, _ in results
        )

        return all(
            term.lower() in retrieved_text
            for term in expected_terms
        )

    # =========================================================
    # NEW: RETRIEVAL METRICS
    # =========================================================

    # ---------------------------------------------------------
    # Precision@K
    #
    # Of the top K retrieved chunks,
    # how many are relevant?
    #
    # Precision@K =
    # relevant chunks in top K / K
    # ---------------------------------------------------------

    def precision_at_k(
        self,
        results,
        relevant_terms: list[str],
        k: int,
    ) -> float:

        top_k_results = results[:k]

        if not top_k_results:
            return 0.0

        relevant_count = 0

        for record, _ in top_k_results:

            content = record.content.lower()

            if any(
                term.lower() in content
                for term in relevant_terms
            ):
                relevant_count += 1

        return (
            relevant_count
            / len(top_k_results)
        )

    # ---------------------------------------------------------
    # Recall@K
    #
    # For this learning CodeLab we approximate recall by asking:
    #
    # How many expected relevant facts/terms appeared anywhere
    # in the top K retrieved chunks?
    #
    # Recall@K =
    # relevant facts found / total relevant facts expected
    #
    # ---------------------------------------------------------

    def recall_at_k(
        self,
        results,
        relevant_terms: list[str],
        k: int,
    ) -> float:

        if not relevant_terms:
            return 0.0

        top_k_results = results[:k]

        retrieved_text = " ".join(
            record.content.lower()
            for record, _ in top_k_results
        )

        found_count = sum(
            1
            for term in relevant_terms
            if term.lower() in retrieved_text
        )

        return (
            found_count
            / len(relevant_terms)
        )

    # ---------------------------------------------------------
    # Reciprocal Rank
    #
    # Find the rank of the FIRST relevant result.
    #
    # Rank 1 → 1.0
    # Rank 2 → 0.5
    # Rank 3 → 0.333...
    #
    # ---------------------------------------------------------

    def reciprocal_rank(
        self,
        results,
        relevant_terms: list[str],
    ) -> float:

        for rank, (record, _) in enumerate(
            results,
            start=1,
        ):

            content = record.content.lower()

            if any(
                term.lower() in content
                for term in relevant_terms
            ):
                return 1.0 / rank

        return 0.0