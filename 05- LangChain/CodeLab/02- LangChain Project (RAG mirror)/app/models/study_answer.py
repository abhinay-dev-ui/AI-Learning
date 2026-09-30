from pydantic import BaseModel, Field


class StudyAnswer(BaseModel):
    """
    Structured response returned by the research
    question-answering chain.
    """

    study_id: str = Field(
        description=(
            "The study identifier associated "
            "with the answer."
        )
    )

    answer: str = Field(
        description=(
            "A concise factual answer based only "
            "on the provided context."
        )
    )

    evidence_found: bool = Field(
        description=(
            "True when the provided context contains "
            "enough evidence to answer the question. "
            "False otherwise."
        )
    )