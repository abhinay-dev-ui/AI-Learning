"""Step 1: follow state through two deterministic LangGraph nodes."""

from typing import NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


class StudyState(TypedDict):
    study_id: str
    duration_months: NotRequired[int]
    answer: NotRequired[str]


# This small table stands in for the data source we will connect later.
STUDIES = {"STUDY-002": 24, "STUDY-003": 36}


def lookup_study(state: StudyState) -> dict[str, int]:
    """Read the ID and return only the new duration field."""
    duration = STUDIES[state["study_id"]]
    return {"duration_months": duration}


def format_answer(state: StudyState) -> dict[str, str]:
    """Use state from the previous node to build the answer."""
    answer = f'{state["study_id"]} lasted {state["duration_months"]} months.'
    return {"answer": answer}


def build_graph():
    builder = StateGraph(StudyState)
    builder.add_node("lookup_study", lookup_study)
    builder.add_node("format_answer", format_answer)

    builder.add_edge(START, "lookup_study")
    builder.add_edge("lookup_study", "format_answer")
    builder.add_edge("format_answer", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"study_id": "STUDY-003"})

    print("Final state:", result)
    print("Answer:", result["answer"])
