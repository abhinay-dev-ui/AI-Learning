"""Application 3: coordinate two specialist agents and combine their reports."""

import json
from typing import NotRequired, TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


DEFAULT_STUDY_ID = "STUDY-101"
DEFAULT_STUDY_CONTEXT = {
    "status": "Active",
    "treatment": "Investigational tablet once daily",
    "expected_enrollment": 100,
    "current_enrollment": 72,
    "review_threshold_percent": 20,
}


class DelegationPlan(BaseModel):
    """Bounded assignments created by the supervisor agent."""

    research_task: str
    monitoring_task: str


class ResearchAnalysis(BaseModel):
    """Model-generated analysis kept separate from authoritative facts."""

    study_summary: str
    evidence: list[str] = Field(min_length=1, max_length=3)


class MonitoringAnalysis(BaseModel):
    """Model explanation of deterministic monitoring evidence."""

    explanation: str
    recommended_check: str


class ResearchReport(BaseModel):
    """Research assignment, source facts, and specialist analysis."""

    task: str
    facts: dict
    analysis: ResearchAnalysis


class MonitoringReport(BaseModel):
    """Monitoring assignment, calculated facts, and specialist analysis."""

    task: str
    deviation_percent: float
    threshold_crossed: bool
    monitoring_summary: str
    analysis: MonitoringAnalysis


class CoordinatedReport(BaseModel):
    """Combined output produced after both specialists finish."""

    combined_summary: str
    recommended_next_step: str


class MultiAgentState(TypedDict):
    """Shared state used to exchange tasks and specialist results."""

    study_id: str
    study_context: dict
    research_task: NotRequired[str]
    monitoring_task: NotRequired[str]
    research_report: NotRequired[dict]
    monitoring_report: NotRequired[dict]
    final_report: NotRequired[dict]


model = ChatOllama(model="mistral", temperature=0, num_predict=256)
delegation_planner = model.with_structured_output(DelegationPlan).with_retry(
    stop_after_attempt=2
)
research_agent = model.with_structured_output(ResearchAnalysis).with_retry(
    stop_after_attempt=2
)
monitoring_agent = model.with_structured_output(MonitoringAnalysis).with_retry(
    stop_after_attempt=2
)
coordinator = model.with_structured_output(CoordinatedReport)


def delegate_work(state: MultiAgentState) -> dict:
    """Let the supervisor agent create two bounded specialist assignments."""
    plan = delegation_planner.invoke(
        "Create exactly two short assignments for a study review. The research "
        "specialist may examine only study status, treatment, current enrollment, "
        "and expected enrollment. Do not request participant-level fields or any "
        "field outside that list. The monitoring specialist must explain a "
        "deterministic enrollment calculation and threshold result. Neither may "
        "approve or reject. "
        f"Study ID: {state['study_id']}."
    )
    return {
        "research_task": plan.research_task,
        "monitoring_task": plan.monitoring_task,
    }


def run_research_specialist(state: MultiAgentState) -> dict:
    """Run an LLM specialist over source-grounded research facts."""
    context = state["study_context"]
    facts = {
        "study_id": state["study_id"],
        "status": context["status"],
        "treatment": context["treatment"],
        "current_enrollment": context["current_enrollment"],
        "expected_enrollment": context["expected_enrollment"],
    }
    analysis = research_agent.invoke(
        f"Assignment: {state['research_task']}\n"
        "Use only the following authoritative facts. Do not infer efficacy, "
        "safety, recruitment status, or study results.\n"
        f"Facts: {json.dumps(facts)}"
    )
    report = ResearchReport(
        task=state["research_task"],
        facts=facts,
        analysis=analysis,
    )
    return {"research_report": report.model_dump()}


def run_monitoring_specialist(state: MultiAgentState) -> dict:
    """Run an LLM specialist over deterministic monitoring evidence."""
    context = state["study_context"]
    expected = context["expected_enrollment"]
    current = context["current_enrollment"]
    threshold = context["review_threshold_percent"]

    if expected <= 0:
        raise ValueError("Expected enrollment must be greater than zero.")

    deviation = round(((expected - current) / expected) * 100, 1)
    threshold_crossed = deviation >= threshold
    comparison = "crosses" if threshold_crossed else "does not cross"
    monitoring_summary = (
        f"Enrollment is {deviation}% below the target of {expected}; "
        f"this {comparison} the {threshold}% review threshold."
    )
    analysis = monitoring_agent.invoke(
        f"Assignment: {state['monitoring_task']}\n"
        "Explain these authoritative calculated values without recalculating "
        "or changing them, then recommend one monitoring check. Do not approve "
        "or reject.\n"
        f"Deviation percent: {deviation}\n"
        f"Threshold crossed: {threshold_crossed}\n"
        f"Monitoring summary: {monitoring_summary}"
    )

    report = MonitoringReport(
        task=state["monitoring_task"],
        deviation_percent=deviation,
        threshold_crossed=threshold_crossed,
        monitoring_summary=monitoring_summary,
        analysis=analysis,
    )
    return {"monitoring_report": report.model_dump()}


def combine_reports(state: MultiAgentState) -> dict:
    """Synthesize both specialist reports without changing their evidence."""
    report = coordinator.invoke(
        "Combine the two specialist reports into one concise study review. "
        "Treat all structured values, especially threshold_crossed, as "
        "authoritative. Correct any narrative conflict, preserve the evidence, "
        "and recommend the next review step without making a human approval "
        "decision.\n"
        f"Research report: {json.dumps(state['research_report'])}\n"
        f"Monitoring report: {json.dumps(state['monitoring_report'])}"
    )
    return {"final_report": report.model_dump()}


def build_graph():
    """Build parallel specialist branches followed by one coordinator."""
    builder = StateGraph(MultiAgentState)
    builder.add_node("delegate_work", delegate_work)
    builder.add_node("research_specialist", run_research_specialist)
    builder.add_node("monitoring_specialist", run_monitoring_specialist)
    builder.add_node("coordinator", combine_reports)

    builder.add_edge(START, "delegate_work")
    builder.add_edge("delegate_work", "research_specialist")
    builder.add_edge("delegate_work", "monitoring_specialist")

    # A list creates a fan-in barrier: the coordinator waits for both branches.
    builder.add_edge(
        ["research_specialist", "monitoring_specialist"],
        "coordinator",
    )
    builder.add_edge("coordinator", END)
    return builder.compile()


def main() -> None:
    """Run the coordinated review and print each specialist contribution."""
    graph = build_graph()
    result = graph.invoke(
        {
            "study_id": DEFAULT_STUDY_ID,
            "study_context": DEFAULT_STUDY_CONTEXT,
        }
    )

    print("Research specialist:")
    print(json.dumps(result["research_report"], indent=2))
    print("\nMonitoring specialist:")
    print(json.dumps(result["monitoring_report"], indent=2))
    print("\nCoordinator:")
    print(json.dumps(result["final_report"], indent=2))


if __name__ == "__main__":
    main()
