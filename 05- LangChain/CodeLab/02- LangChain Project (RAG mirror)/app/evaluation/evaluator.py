from langchain_core.documents import Document

from app.models.evaluation_case import (
    EvaluationCase,
)
from app.models.evaluation_result import (
    EvaluationResult,
)
from app.models.study_answer import (
    StudyAnswer,
)


class EvaluationService:
    def evaluate(
        self,
        case: EvaluationCase,
        documents: list[Document],
        structured_answer: StudyAnswer,
    ) -> EvaluationResult:

        # -------------------------------------------------
        # RETRIEVAL EVALUATION
        # -------------------------------------------------
        #
        # Combine the clean original contents from all
        # final reranked documents into one searchable
        # string.
        retrieved_text = " ".join(
            document.metadata.get(
                "original_content",
                document.page_content,
            )
            for document in documents
        )

        # Normalize case so evaluation isn't affected by:
        #
        # "36 Months"
        # vs
        # "36 months"
        normalized_retrieved_text = (
            retrieved_text.lower()
        )

        # Every expected fact must occur somewhere in
        # the final retrieved evidence.
        retrieval_pass = all(
            expected_fact.lower()
            in normalized_retrieved_text

            for expected_fact
            in case.expected_facts
        )


        # -------------------------------------------------
        # ANSWER EVALUATION
        # -------------------------------------------------

        normalized_answer = (
            structured_answer.answer.lower()
        )

        answer_pass = all(
            expected_fact.lower()
            in normalized_answer

            for expected_fact
            in case.expected_facts
        )


        # -------------------------------------------------
        # BUILD RESULT
        # -------------------------------------------------

        return EvaluationResult(
            case_name=case.name,
            question=case.question,
            expected_facts=(
                case.expected_facts
            ),
            answer=(
                structured_answer.answer
            ),
            evidence_found=(
                structured_answer.evidence_found
            ),
            retrieval_pass=retrieval_pass,
            answer_pass=answer_pass,
        )