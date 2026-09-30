"""Application 2, Step 4: explain evidence and terminate safely on failures."""

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


class EvidenceExplanation(BaseModel):
    """Structured explanation that supports, but does not make, the decision."""

    summary: str = Field(description="Concise explanation of the measured evidence.")
    recommended_next_step: str = Field(
        description="A review action that does not approve or reject the finding."
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
    explanation: NotRequired[str]
    recommended_next_step: NotRequired[str]
    error: NotRequired[str]
    approval_decision: NotRequired[str]
    final_decision: NotRequired[str]


model = ChatOllama(model="mistral", temperature=0, num_predict=256)
planner = model.with_structured_output(ReviewPlan)
explainer = model.with_structured_output(EvidenceExplanation).with_retry(
    stop_after_attempt=2
)


def create_plan(state: MonitoringState) -> dict:
    """Create a validated plan or return a routable failure."""
    try:
        plan = planner.invoke(
            "Create a concise monitoring plan for reviewing an enrollment "
            f"deviation in {state['study_id']}. Include evidence checks and "
            "the next review action. Do not make the final decision."
        )
        return {"plan": plan.steps, "error": ""}
    except Exception as error:
        return {"plan": [], "error": f"Planning failed: {error}"}


def route_after_plan(
    state: MonitoringState,
) -> Literal["check_enrollment", "handle_failure"]:
    """Continue only when a validated plan was created."""
    return "handle_failure" if state.get("error") else "check_enrollment"


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


def explain_finding(state: MonitoringState) -> dict:
    """Explain deterministic evidence with structured output and retries."""
    try:
        plan_text = " -> ".join(state.get("plan", []))
        explanation = explainer.invoke(
            f"Follow this review plan: {plan_text}. "
            f"Study {state['study_id']} expected "
            f"{state['expected_enrollment']} participants and currently has "
            f"{state['current_enrollment']}. Its calculated deviation is "
            f"{state['deviation_percent']}% and the finding is "
            f"'{state['finding']}'. Explain the evidence and recommend only "
            "the next review step. Do not approve or reject the finding."
        )
        return {
            "explanation": explanation.summary,
            "recommended_next_step": explanation.recommended_next_step,
            "error": "",
        }
    except Exception as error:
        return {"error": f"Evidence explanation failed: {error}"}


def route_after_explanation(
    state: MonitoringState,
) -> Literal["request_approval", "finalize", "handle_failure"]:
    """Route failures safely and send threshold breaches for approval."""
    if state.get("error"):
        return "handle_failure"
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
            "explanation": state["explanation"],
            "recommended_next_step": state["recommended_next_step"],
        }
    )
    return {"approval_decision": str(decision).lower()}


def finalize(state: MonitoringState) -> dict:
    """Create the final outcome after routing or human review."""
    if state["finding"] == "Human review required":
        decision = state.get("approval_decision", "pending")
        outcomes = {
            "approve": "Approved: continue with the recommended monitoring action.",
            "reject": "Rejected: do not proceed; escalate for manual reassessment.",
            "revise": "Revision requested: update the evidence explanation before approval.",
        }
        final_decision = outcomes.get(
            decision,
            "Approval is still pending.",
        )
    else:
        final_decision = "No human approval was required."
    return {"final_decision": final_decision}


def handle_failure(state: MonitoringState) -> dict:
    """Convert an exhausted model failure into an explicit terminal result."""
    return {
        "final_decision": (
            "Monitoring review stopped safely. "
            f"Manual follow-up is required. {state['error']}"
        )
    }


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
    builder.add_node("explain_finding", explain_finding)
    builder.add_node("request_approval", request_approval)
    builder.add_node("finalize", finalize)
    builder.add_node("handle_failure", handle_failure)

    builder.add_edge(START, "create_plan")
    builder.add_conditional_edges("create_plan", route_after_plan)
    builder.add_edge("check_enrollment", "explain_finding")
    builder.add_conditional_edges("explain_finding", route_after_explanation)
    builder.add_edge("request_approval", "finalize")
    builder.add_edge("finalize", END)
    builder.add_edge("handle_failure", END)
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
    if result.get("explanation"):
        print(f"Explanation: {result['explanation']}")
        print(f"Recommended next step: {result['recommended_next_step']}")
    print(f"Final decision: {result['final_decision']}")
    print(f"Saved decision: {saved_state['final_decision']}")


if __name__ == "__main__":
    main()
