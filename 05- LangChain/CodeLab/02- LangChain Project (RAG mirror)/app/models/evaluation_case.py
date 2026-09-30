from dataclasses import dataclass


@dataclass
class EvaluationCase:
    """
    Represents one deterministic evaluation case
    for our RAG pipeline.
    """

    name: str

    question: str

    filters: dict[str, str]

    # A case may require multiple facts.
    #
    # Example:
    #
    # ["36 months", "30 percent"]
    expected_facts: list[str]