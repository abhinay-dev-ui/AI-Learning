"""Application 2, Step 2: checkpoint monitoring state under a thread ID."""

from typing import NotRequired, TypedDict

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


DEFAULT_STUDY_ID = "STUDY-101"
EXPECTED_ENROLLMENT = 100
CURRENT_ENROLLMENT = 72
REVIEW_THRESHOLD_PERCENT = 20.0
THREAD_ID = "study-101-monitoring-review"


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
    # Nodes generate these fields, so callers do not need to provide them.
    plan: NotRequired[list[str]]
    deviation_percent: NotRequired[float]
    finding: NotRequired[str]


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


def build_graph(checkpointer: InMemorySaver):
    """Define the workflow and compile it with checkpoint storage."""
    builder = StateGraph(MonitoringState)
    builder.add_node("create_plan", create_plan)
    builder.add_node("check_enrollment", check_enrollment)

    builder.add_edge(START, "create_plan")
    builder.add_edge("create_plan", "check_enrollment")
    builder.add_edge("check_enrollment", END)
    return builder.compile(checkpointer=checkpointer)


def main() -> None:
    """Run a review and retrieve its saved state from the same thread."""
    checkpointer = InMemorySaver()
    graph = build_graph(checkpointer)

    # Reusing this ID continues the same saved execution. A different ID gets
    # an isolated state history.
    config = {"configurable": {"thread_id": THREAD_ID}}

    initial_state: MonitoringState = {
        "study_id": DEFAULT_STUDY_ID,
        "expected_enrollment": EXPECTED_ENROLLMENT,
        "current_enrollment": CURRENT_ENROLLMENT,
    }

    result = graph.invoke(initial_state, config=config)
    saved_state = graph.get_state(config).values

    print(f"Thread: {THREAD_ID}")
    print(f"Study: {result['study_id']}")
    print(f"Plan: {result['plan']}")
    print(f"Deviation: {result['deviation_percent']}%")
    print(f"Finding: {result['finding']}")
    print(f"Saved finding: {saved_state['finding']}")


if __name__ == "__main__":
    main()
