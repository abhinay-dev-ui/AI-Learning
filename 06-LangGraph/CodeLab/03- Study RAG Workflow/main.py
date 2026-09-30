"""Run one study research request through the complete workflow."""

import argparse

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from app.workflow import build_workflow


def main() -> None:
    """Parse one request, run the graph, and resume it if review pauses it."""
    # Flags let us exercise each control-flow path without editing source code.
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default="What is the duration of STUDY-003?")
    parser.add_argument("--thread-id", default="study-demo-1")
    parser.add_argument("--review", action="store_true")
    parser.add_argument("--decision", choices=("approve", "reject"))
    parser.add_argument("--generator", choices=("extractive", "ollama"), default="extractive")
    parser.add_argument("--simulate-timeout", action="store_true")
    parser.add_argument("--simulate-failure", action="store_true")
    args = parser.parse_args()

    # InMemorySaver is suitable for this one-process lesson. A production
    # service needs a persistent checkpointer such as PostgreSQL.
    graph = build_workflow(checkpointer=InMemorySaver())

    # All invocations and resumes for one workflow instance use the same ID.
    config = {"configurable": {"thread_id": args.thread_id}}

    # Only caller-owned inputs are supplied here. Later nodes add query,
    # documents, scores, draft, approval, and the final answer.
    result = graph.invoke(
        {
            "question": args.question,
            "messages": [HumanMessage(content=args.question)],
            "requires_review": args.review,
            "generator": args.generator,
            "simulate_timeout": args.simulate_timeout,
            "simulate_failure": args.simulate_failure,
            "trace": [],
        },
        config=config,
    )

    # interrupt() returns control to the application instead of continuing to
    # finalize. Resume the saved position under the same thread configuration.
    if "__interrupt__" in result:
        print("Review requested:", result["__interrupt__"][0].value)
        print("Saved next step:", graph.get_state(config).next)
        decision = args.decision
        while decision not in ("approve", "reject"):
            decision = input("Review decision (approve/reject): ").strip().lower()
        result = graph.invoke(Command(resume=decision), config=config)

    # The trace makes the selected path visible while we learn the graph.
    print("Answer:", result["answer"])
    print("Search attempts:", result["attempts"])
    print("Trace:")
    for step in result["trace"]:
        print(" -", step)
    print("Message count:", len(result["messages"]))


if __name__ == "__main__":
    main()
