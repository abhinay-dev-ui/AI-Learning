"""Application 2, Step 1: store a monitoring plan and evidence in graph state."""

from typing import TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


DEFAULT_STUDY_ID = "STUDY-101"
EXPECTED_ENROLLMENT = 100
CURRENT_ENROLLMENT = 72
REVIEW_THRESHOLD_PERCENT = 20.0


class ReviewPlan(BaseModel):
    """Structured plan created before the monitoring check begins."""

    steps: list[str] = Field(
        min_length=2,
        max_length=4,
        description="Short ordered steps for reviewing the enrollment deviation.",
    )


class MonitoringState(TypedDict):
    """Data shared by every node in one graph execution."""

    study_id: str
    expected_enrollment: int
    current_enrollment: int
    plan: list[str]
    deviation_percent: float
    finding: str


model = ChatOllama(model="mistral", temperature=0)
planner = model.with_structured_output(ReviewPlan)


def create_plan(state: MonitoringState) -> dict:
    """Ask the model for a short plan and return only the state update."""
    plan = planner.invoke(
        "Create a concise monitoring plan for reviewing an enrollment "
        f"deviation in {state['study_id']}. Do not make the final decision."
    )
    return {"plan": plan.steps}


def check_enrollment(state: MonitoringState) -> dict:
    """Calculate deviation deterministically and record the finding."""
    expected = state["expected_enrollment"]
    current = state["current_enrollment"]
    deviation = ((expected - current) / expected) * 100

    finding = (
        "Human review required"
        if deviation >= REVIEW_THRESHOLD_PERCENT
        else "Within the monitoring threshold"
    )
    return {
        "deviation_percent": round(deviation, 1),
        "finding": finding,
    }


def build_graph():
    """Define and compile the first monitoring workflow."""
    builder = StateGraph(MonitoringState)
    builder.add_node("create_plan", create_plan)
    builder.add_node("check_enrollment", check_enrollment)

    builder.add_edge(START, "create_plan")
    builder.add_edge("create_plan", "check_enrollment")
    builder.add_edge("check_enrollment", END)
    return builder.compile()


def main() -> None:
    """Run one monitoring review and print its important state values."""
    graph = build_graph()
    initial_state: MonitoringState = {
        "study_id": DEFAULT_STUDY_ID,
        "expected_enrollment": EXPECTED_ENROLLMENT,
        "current_enrollment": CURRENT_ENROLLMENT,
        "plan": [],
        "deviation_percent": 0.0,
        "finding": "",
    }

    result = graph.invoke(initial_state)

    print(f"Study: {result['study_id']}")
    print(f"Plan: {result['plan']}")
    print(f"Deviation: {result['deviation_percent']}%")
    print(f"Finding: {result['finding']}")


if __name__ == "__main__":
    main()
