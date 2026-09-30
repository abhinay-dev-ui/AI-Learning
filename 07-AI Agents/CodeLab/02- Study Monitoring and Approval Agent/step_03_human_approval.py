"""Application 2, Step 3: pause and resume a monitoring review for approval."""

from typing import Literal, NotRequired, TypedDict

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
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
    approval_decision: NotRequired[str]
    final_decision: NotRequired[str]


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


def route_after_check(
    state: MonitoringState,
) -> Literal["request_approval", "finalize"]:
    """Send only threshold breaches to a human reviewer."""
    if state["finding"] == "Human review required":
        return "request_approval"
    return "finalize"


def request_approval(state: MonitoringState) -> dict:
    """Pause execution and store the human decision supplied on resume."""
    decision = interrupt(
        {
            "question": "Approve, reject, or revise this monitoring finding?",
            "study_id": state["study_id"],
            "deviation_percent": state["deviation_percent"],
            "finding": state["finding"],
        }
    )
    return {"approval_decision": str(decision).lower()}


def finalize(state: MonitoringState) -> dict:
    """Create the final outcome after routing or human review."""
    if state["finding"] == "Human review required":
        decision = state.get("approval_decision", "pending")
        final_decision = f"Human reviewer selected: {decision}"
    else:
        final_decision = "No human approval was required."
    return {"final_decision": final_decision}


def read_human_decision() -> str:
    """Read one of the decisions accepted by the approval workflow."""
    allowed_decisions = {"approve", "reject", "revise"}
    while True:
        decision = input("Decision [approve/reject/revise]: ").strip().lower()
        if decision in allowed_decisions:
            return decision
        print("Enter approve, reject, or revise.")


def build_graph(checkpointer: InMemorySaver):
    """Define the workflow and compile it with checkpoint storage."""
    builder = StateGraph(MonitoringState)
    builder.add_node("create_plan", create_plan)
    builder.add_node("check_enrollment", check_enrollment)
    builder.add_node("request_approval", request_approval)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "create_plan")
    builder.add_edge("create_plan", "check_enrollment")
    builder.add_conditional_edges("check_enrollment", route_after_check)
    builder.add_edge("request_approval", "finalize")
    builder.add_edge("finalize", END)
    return builder.compile(checkpointer=checkpointer)


def main() -> None:
    """Run a review, collect approval if interrupted, and resume its thread."""
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

    if "__interrupt__" in result:
        approval_request = result["__interrupt__"][0].value
        print(f"Approval requested: {approval_request}")
        human_decision = read_human_decision()

        # The same graph and thread ID locate the saved pause point. Command
        # supplies the value returned by interrupt() when the node resumes.
        result = graph.invoke(
            Command(resume=human_decision),
            config=config,
        )

    saved_state = graph.get_state(config).values

    print(f"Thread: {THREAD_ID}")
    print(f"Study: {result['study_id']}")
    print(f"Plan: {result['plan']}")
    print(f"Deviation: {result['deviation_percent']}%")
    print(f"Finding: {result['finding']}")
    print(f"Final decision: {result['final_decision']}")
    print(f"Saved decision: {saved_state['final_decision']}")


if __name__ == "__main__":
    main()
