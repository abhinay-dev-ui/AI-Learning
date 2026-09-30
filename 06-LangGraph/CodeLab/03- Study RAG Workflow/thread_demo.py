"""Show that one checkpointer keeps two workflow threads separate."""

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from app.workflow import build_workflow


def request(question: str) -> dict:
    """Build the caller-owned initial state for one independent request."""
    return {
        "question": question,
        "messages": [HumanMessage(content=question)],
        "requires_review": False,
        "generator": "extractive",
        "simulate_timeout": False,
        "simulate_failure": False,
        "trace": [],
    }


if __name__ == "__main__":
    # Both runs share one checkpointer but use distinct thread IDs.
    graph = build_workflow(checkpointer=InMemorySaver())
    first = {"configurable": {"thread_id": "study-002-request"}}
    second = {"configurable": {"thread_id": "study-003-request"}}

    graph.invoke(request("What is the duration of STUDY-002?"), config=first)
    graph.invoke(request("What is the duration of STUDY-003?"), config=second)

    # get_state(config) selects the latest checkpoint for that specific thread.
    first_answer = graph.get_state(first).values["answer"]
    second_answer = graph.get_state(second).values["answer"]
    print("Thread study-002-request:", first_answer)
    print("Thread study-003-request:", second_answer)
