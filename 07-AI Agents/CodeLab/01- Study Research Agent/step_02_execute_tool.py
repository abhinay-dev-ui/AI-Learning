"""Step 2: execute one requested tool and return its result to the model."""

import argparse
import json

from langchain_core.messages import HumanMessage, ToolMessage
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
        description="Execute one model-requested study tool."
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Question sent to the tool-enabled model.",
    )
    return parser.parse_args().question


def main() -> None:
    """Complete one model → tool → model cycle."""
    question = read_question()

    # The list is registered with the model; the dictionary lets application
    # code safely find the requested executable tool by its returned name.
    tools = [get_study]
    tools_by_name = {available_tool.name: available_tool for available_tool in tools}

    model = ChatOllama(model="mistral", temperature=0)
    model_with_tools = model.bind_tools(tools)

    # Messages preserve the model's tool request and the matching result.
    messages = [HumanMessage(content=question)]
    response = model_with_tools.invoke(messages)
    messages.append(response)

    print(f"Question: {question}")

    if not response.tool_calls:
        print(f"Direct model answer: {response.content}")
        return

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        if tool_name not in tools_by_name:
            raise ValueError(f"The model requested an unavailable tool: {tool_name}")

        selected_tool = tools_by_name[tool_name]
        tool_result = selected_tool.invoke(tool_call["args"])

        print(f"Requested tool: {tool_name}")
        print(f"Arguments: {tool_call['args']}")
        print(f"Tool result: {tool_result}")

        # tool_call_id connects this observation to the model's request.
        messages.append(
            ToolMessage(
                content=json.dumps(tool_result),
                tool_call_id=tool_call["id"],
            )
        )

    # The second invocation can see the original question, tool request, and
    # tool result, so it can now produce a grounded natural-language answer.
    final_response = model_with_tools.invoke(messages)
    print(f"Final answer: {final_response.content}")


if __name__ == "__main__":
    main()
