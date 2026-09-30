"""Step 2: choose one of two answer paths from the updated state."""

from typing import Literal, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


class StudyState(TypedDict):
    study_id: str
    duration_months: NotRequired[int | None]
    answer: NotRequired[str]


STUDIES = {"STUDY-002": 24, "STUDY-003": 36}


def lookup_study(state: StudyState) -> dict[str, int | None]:
    return {"duration_months": STUDIES.get(state["study_id"])}


def route_study(state: StudyState) -> Literal["format_answer", "study_not_found"]:
    if state["duration_months"] is None:
        return "study_not_found"
    return "format_answer"


def format_answer(state: StudyState) -> dict[str, str]:
    duration = state["duration_months"]
    assert duration is not None  # This node runs only on the found path.
    return {"answer": f'{state["study_id"]} lasted {duration} months.'}


def study_not_found(state: StudyState) -> dict[str, str]:
    return {"answer": f'No duration found for {state["study_id"]}.'}


def build_graph():
    builder = StateGraph(StudyState)
    builder.add_node("lookup_study", lookup_study)
    builder.add_node("format_answer", format_answer)
    builder.add_node("study_not_found", study_not_found)

    builder.add_edge(START, "lookup_study")
    builder.add_conditional_edges("lookup_study", route_study)
    builder.add_edge("format_answer", END)
    builder.add_edge("study_not_found", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    for study_id in ("STUDY-003", "STUDY-999"):
        result = graph.invoke({"study_id": study_id})
        print(f"{study_id}: {result}")
