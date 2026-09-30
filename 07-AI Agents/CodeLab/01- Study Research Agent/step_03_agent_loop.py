"""Step 3: run a bounded Observe-Reason-Act loop with two related tools."""

import argparse
import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


# The default question requires information from both tools.
DEFAULT_QUESTION = (
    "What is the status of STUDY-101, and describe its assigned treatment?"
)
MAX_ROUNDS = 5

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


def read_question() -> str:
    """Read an optional question while keeping a useful default."""
    parser = argparse.ArgumentParser(
        description="Run a bounded study research agent loop."
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Question sent to the tool-enabled model.",
    )
    return parser.parse_args().question


def main() -> None:
    """Run tool reasoning rounds until the model answers or reaches the limit."""
    question = read_question()

    # The list exposes tool schemas to the model. The dictionary lets Python
    # safely select the executable tool named in each model response.
    tools = [get_study, get_treatment]
    tools_by_name = {available_tool.name: available_tool for available_tool in tools}

    model = ChatOllama(model="mistral", temperature=0, num_predict=128)

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
        # This step intentionally leaves every action decision to the model.
        # Python limits which tools are currently valid and executes whatever
        # valid request the model returns.
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
        study_loaded_this_round = False
        treatment_loaded_this_round = False
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            if tool_name not in tools_by_name:
                raise ValueError(
                    f"The model requested an unavailable tool: {tool_name}"
                )

            selected_tool = tools_by_name[tool_name]
            requested_code = str(
                tool_call["args"].get("treatment_code", "")
            ).upper()

            if (
                tool_name == "get_treatment"
                and requested_code not in known_treatment_codes
            ):
                tool_result = {
                    "error": (
                        "Treatment details can be requested only with a code "
                        "returned by get_study."
                    )
                }
            else:
                try:
                    tool_result = selected_tool.invoke(tool_call["args"])
                except Exception as error:
                    # An invalid model-generated argument is an observation,
                    # not a reason to crash the agent loop. The next model
                    # round can inspect this error and correct its action.
                    tool_result = {
                        "error": f"Invalid {tool_name} request: {error}"
                    }

            if tool_name == "get_study" and "treatment_code" in tool_result:
                known_treatment_codes.add(tool_result["treatment_code"].upper())
                study_loaded_this_round = True
            if tool_name == "get_treatment" and "error" not in tool_result:
                treatment_details_loaded = True
                treatment_loaded_this_round = True

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

        # Small local models may repeat the previous tool even after seeing a
        # valid observation. This reminder explains the required next action;
        # the model must still create the tool call and its arguments.
        if study_loaded_this_round and not treatment_details_loaded:
            treatment_code = sorted(known_treatment_codes)[0]
            messages.append(
                SystemMessage(
                    content=(
                        "You have completed get_study. The observation returned "
                        f"treatment code '{treatment_code}'. Your next action must "
                        "be get_treatment with that exact treatment_code. Do not "
                        "request get_study again."
                    )
                )
            )
        elif treatment_loaded_this_round:
            messages.append(
                SystemMessage(
                    content=(
                        "All requested evidence is now present. Return the final "
                        "answer without calling another tool."
                    )
                )
            )
    else:
        print(f"Agent stopped after reaching {MAX_ROUNDS} reasoning rounds.")


if __name__ == "__main__":
    main()
