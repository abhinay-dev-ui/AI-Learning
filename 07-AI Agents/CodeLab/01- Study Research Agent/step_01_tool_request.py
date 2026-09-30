"""Step 1: let the model request a study lookup without executing it."""

import argparse

from langchain_core.tools import tool
from langchain_ollama import ChatOllama


# A complete default question keeps the first run reproducible.
DEFAULT_QUESTION = "What is the status of STUDY-101?"

# Local data stands in for a database during the learning exercise.
STUDIES = {
    "STUDY-101": {
        "status": "Active",
        "treatment": "A",
    },
    "STUDY-102": {
        "status": "Completed",
        "treatment": "B",
    },
}


@tool
def get_study(study_id: str) -> dict:
    """Return the status and treatment for a specific study ID."""
    return STUDIES.get(
        study_id.upper(),
        {"error": f"Study {study_id} was not found."},
    )


def read_question() -> str:
    """Read an optional question while keeping a useful default."""
    parser = argparse.ArgumentParser(
        description="Inspect the tool call requested by a local model."
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Question sent to the tool-enabled model.",
    )
    return parser.parse_args().question


def main() -> None:
    """Bind the study tool, invoke the model, and print its requested action."""
    question = read_question()

    # Creating and binding the model exposes the tool schema; it does not run
    # get_study. The model can only return a request to use that capability.
    model = ChatOllama(model="mistral", temperature=0)
    model_with_tools = model.bind_tools([get_study])

    response = model_with_tools.invoke(question)

    print(f"Question: {question}")
    print(f"Response content: {response.content!r}")

    if not response.tool_calls:
        print("The model did not request a tool.")
        return

    for tool_call in response.tool_calls:
        print(f"Requested tool: {tool_call['name']}")
        print(f"Arguments: {tool_call['args']}")
        print(f"Tool call ID: {tool_call['id']}")


if __name__ == "__main__":
    main()
