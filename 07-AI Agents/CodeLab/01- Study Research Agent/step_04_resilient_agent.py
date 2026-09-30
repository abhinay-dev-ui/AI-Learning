"""Step 4: add retry and recoverable failures to the agent loop."""

import argparse
import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


# The default question requires information from both tools.
DEFAULT_QUESTION = (
    "What is the status of STUDY-101, and describe its assigned treatment?"
)
MAX_ROUNDS = 5
MAX_TOOL_ATTEMPTS = 2

# Local data stands in for databases during this learning exercise.
STUDIES = {
    "STUDY-101": {
        "status": "Active",
        "treatment_code": "A",
    },
    "STUDY-102": {
        "status": "Completed",
        "treatment_code": "B",
    },
}

TREATMENTS = {
    "A": {
        "name": "Investigational tablet",
        "schedule": "Once daily",
    },
    "B": {
        "name": "Standard comparator",
        "schedule": "Twice daily",
    },
}


@tool
def get_study(study_id: str) -> dict:
    """Return the status and treatment code for a specific study ID."""
    return STUDIES.get(
        study_id.upper(),
        {"error": f"Study {study_id} was not found."},
    )


@tool
def get_treatment(treatment_code: str) -> dict:
    """Return details for a treatment code found in a study record."""
    normalized_code = treatment_code.upper()
    return TREATMENTS.get(
        normalized_code,
        {"error": f"Treatment {treatment_code} was not found."},
    )


def execute_tool(
    tool_call: dict,
    tools_by_name: dict,
    known_treatment_codes: set[str],
) -> dict:
    """Execute a requested tool, retry exceptions, and return failures as data."""
    tool_name = tool_call["name"]
    selected_tool = tools_by_name.get(tool_name)

    # Returning an observation lets the model explain or recover from the
    # problem instead of terminating the entire application.
    if selected_tool is None:
        return {"error": f"Tool {tool_name} is not available."}

    if tool_name == "get_treatment":
        requested_code = str(
            tool_call["args"].get("treatment_code", "")
        ).upper()
        if requested_code not in known_treatment_codes:
            return {
                "error": (
                    "Treatment details can be requested only with a code "
                    "returned by get_study."
                )
            }

    for attempt in range(1, MAX_TOOL_ATTEMPTS + 1):
        try:
            return selected_tool.invoke(tool_call["args"])
        except Exception as error:
            print(
                f"Tool {tool_name} failed on attempt "
                f"{attempt}/{MAX_TOOL_ATTEMPTS}: {error}"
            )

    return {
        "error": (
            f"Tool {tool_name} failed after "
            f"{MAX_TOOL_ATTEMPTS} attempts."
        )
    }


def read_question() -> str:
    """Read an optional question while keeping a useful default."""
    parser = argparse.ArgumentParser(
        description="Run a resilient study research agent loop."
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Question sent to the tool-enabled model.",
    )
    return parser.parse_args().question


def main() -> None:
    """Run bounded reasoning rounds with recoverable tool failures."""
    question = read_question()

    # The list exposes tool schemas to the model. The dictionary lets Python
    # safely select the executable tool named in each model response.
    tools = [get_study, get_treatment]
    tools_by_name = {available_tool.name: available_tool for available_tool in tools}

    model = ChatOllama(model="mistral", temperature=0)

    # The instruction prevents the model from guessing data that tools provide.
    messages = [
        SystemMessage(
            content=(
                "Use the available tools for study and treatment facts. "
                "First retrieve the study record. If the user asks to "
                "describe or explain its treatment, you must then call "
                "get_treatment with the exact code returned by get_study. "
                "Do not answer a treatment-description question until the "
                "get_treatment result is present."
            )
        ),
        HumanMessage(content=question),
    ]
    treatment_details_required = "treatment" in question.lower()
    known_treatment_codes: set[str] = set()
    treatment_details_loaded = False

    print(f"Question: {question}")

    # Each iteration is one Observe-Reason-Act round. A limit prevents the
    # application from continuing forever if the model never finishes.
    for round_number in range(1, MAX_ROUNDS + 1):
        # Enforce the data dependency in application code. This remains reliable
        # even when a local model ignores forced tool-selection instructions.
        if (
            treatment_details_required
            and known_treatment_codes
            and not treatment_details_loaded
        ):
            treatment_code = sorted(known_treatment_codes)[0]
            tool_call = {
                "name": "get_treatment",
                "args": {"treatment_code": treatment_code},
                "id": f"required-treatment-{round_number}",
                "type": "tool_call",
            }
            messages.append(AIMessage(content="", tool_calls=[tool_call]))
            tool_result = execute_tool(
                tool_call,
                tools_by_name,
                known_treatment_codes,
            )
            messages.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )
            treatment_details_loaded = "error" not in tool_result

            print(f"\nReasoning round {round_number}")
            print("Required tool: get_treatment")
            print(f"Arguments: {tool_call['args']}")
            print(f"Tool result: {tool_result}")
            continue

        # Python exposes the dependent treatment tool only after get_study has
        # returned a real treatment code.
        if not known_treatment_codes:
            available_tools = [get_study]
        else:
            available_tools = tools
        model_with_tools = model.bind_tools(available_tools)
        response = model_with_tools.invoke(messages)
        messages.append(response)

        # No tool calls means the model has produced its final response.
        if not response.tool_calls:
            if treatment_details_required and not known_treatment_codes:
                messages.append(
                    SystemMessage(
                        content=(
                            "The required study evidence is still missing. "
                            "Call get_study before answering."
                        )
                    )
                )
                continue
            if treatment_details_required and not treatment_details_loaded:
                treatment_code = sorted(known_treatment_codes)[0]
                messages.append(
                    SystemMessage(
                        content=(
                            "The treatment description is still missing. "
                            "Call get_treatment now with treatment_code "
                            f"'{treatment_code}' before answering."
                        )
                    )
                )
                continue
            print(f"Final answer: {response.content}")
            break

        print(f"\nReasoning round {round_number}")

        # A single model response can request several tools. Python executes
        # every request and records every result before the next model round.
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_result = execute_tool(
                tool_call,
                tools_by_name,
                known_treatment_codes,
            )

            if tool_name == "get_study" and "treatment_code" in tool_result:
                known_treatment_codes.add(tool_result["treatment_code"].upper())
            if tool_name == "get_treatment" and "error" not in tool_result:
                treatment_details_loaded = True

            print(f"Requested tool: {tool_name}")
            print(f"Arguments: {tool_call['args']}")
            print(f"Tool result: {tool_result}")

            # The call ID connects this observation to the matching request.
            messages.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )
    else:
        print(f"Agent stopped after reaching {MAX_ROUNDS} reasoning rounds.")


if __name__ == "__main__":
    main()
