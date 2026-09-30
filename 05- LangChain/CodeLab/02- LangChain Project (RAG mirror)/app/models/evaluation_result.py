from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """
    Stores the result of one evaluation case.
    """

    case_name: str

    question: str

    expected_facts: list[str]

    answer: str

    evidence_found: bool

    retrieval_pass: bool

    answer_pass: bool