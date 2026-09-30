import re


class QueryTransformer:

    # ---------------------------------------------------------
    # Previous approach: Single query transformation
    # ---------------------------------------------------------
    #
    # Example:
    #
    # "How long was the study for Treatment C?"
    #
    # becomes:
    #
    # "study duration treatment c"
    #
    # ---------------------------------------------------------

    def transform(self, query: str) -> str:

        query = query.lower().strip()

        query = re.sub(
            r"how long was the study for",
            "study duration",
            query,
        )

        query = re.sub(
            r"how long did",
            "duration",
            query,
        )

        query = query.replace("?", "")

        return query.strip()

    # ---------------------------------------------------------
    # Previous improvement: Multi-query retrieval
    # ---------------------------------------------------------
    #
    # Same user intent expressed using multiple retrieval queries.
    #
    # Example:
    #
    # study duration treatment c
    # study length treatment c
    # trial duration treatment c
    #
    # ---------------------------------------------------------

    def generate_queries(self, query: str) -> list[str]:

        base_query = self.transform(query)

        queries = [
            base_query,
        ]

        if "duration" in base_query:

            queries.append(
                base_query.replace(
                    "duration",
                    "length",
                )
            )

        if "study" in base_query:

            queries.append(
                base_query.replace(
                    "study",
                    "trial",
                )
            )

        # Remove duplicate generated queries.
        return list(dict.fromkeys(queries))

    # ---------------------------------------------------------
    # Current improvement: Query Decomposition
    # ---------------------------------------------------------
    #
    # Multi-query:
    # Same intent → different wording
    #
    # Query decomposition:
    # Multiple intents → separate sub-questions
    #
    # Example:
    #
    # "How long was Treatment C and what was the primary
    # success criterion?"
    #
    # becomes:
    #
    # 1. "How long was the study for Treatment C?"
    # 2. "What was the primary success criterion for Treatment C?"
    #
    # ---------------------------------------------------------

    def decompose(self, query: str) -> list[str]:

        normalized_query = query.strip()

        lower_query = normalized_query.lower()

        # Learning CodeLab implementation:
        #
        # We deliberately use a simple rule-based decomposition
        # before introducing LLM-based decomposition later.

        if (
            "how long" in lower_query
            and "success criterion" in lower_query
        ):

            # In this CodeLab we know the query refers to
            # Treatment C.
            #
            # Later this entity extraction can be improved.
            treatment_match = re.search(
                r"treatment\s+[a-z0-9\-]+",
                lower_query,
            )

            treatment = (
                treatment_match.group(0)
                if treatment_match
                else "treatment"
            )

            return [
                f"How long was the study for {treatment}?",
                (
                    "What was the primary success criterion "
                    f"for {treatment}?"
                ),
            ]

        # No decomposition required.
        return [normalized_query]