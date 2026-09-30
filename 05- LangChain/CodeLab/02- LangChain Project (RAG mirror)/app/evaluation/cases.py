from app.models.evaluation_case import (
    EvaluationCase,
)


EVALUATION_CASES = [
    EvaluationCase(
        name="Treatment C Duration",
        question=(
            "How long was the study "
            "for Treatment C?"
        ),
        filters={
            "study_id": "STUDY-003"
        },
        expected_facts=[
            "36 months"
        ],
    ),

    EvaluationCase(
        name="Treatment C Success Criterion",
        question=(
            "What was the primary success "
            "criterion for Treatment C?"
        ),
        filters={
            "study_id": "STUDY-003"
        },
        expected_facts=[
            "30 percent"
        ],
    ),

    EvaluationCase(
        name=(
            "Treatment C Duration "
            "and Success Criterion"
        ),
        question=(
            "How long was the study for "
            "Treatment C and what was its "
            "primary success criterion?"
        ),
        filters={
            "study_id": "STUDY-003"
        },
        expected_facts=[
            "36 months",
            "30 percent",
        ],
    ),
]