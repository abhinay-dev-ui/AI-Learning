# AI Agents — Quick Reference

## Core mental model

```text
Agent = model + instructions + tools + state + controlled loop
Loop  = observe → decide → act → observe again
```

The model requests an action. Application code validates permissions and arguments, executes the tool, and returns the observation.

## Tool-call sequence

```text
HumanMessage
→ AIMessage(tool call + call ID)
→ ToolMessage(result + matching call ID)
→ AIMessage(next call or final answer)
```

Append the AI message before its tool results. One AI message can contain several independent calls. Dependent calls require another model iteration.

## Register versus execute

```python
model.bind_tools([get_study])  # Pass the callable.
get_study.invoke({"study_id": "STUDY-101"})  # Execute the tool.
```

## Choose the mechanism

| Requirement | Mechanism |
|---|---|
| Fixed sequence | Plain code, LCEL, or fixed graph |
| Model selects an allowed capability | Agent tool call |
| Missing required information | Ask user; do not invent an argument |
| Validated fields | Structured output schema |
| Current execution data | State |
| Same conversation continuity | Checkpoint + thread ID |
| Cross-thread facts | Separate long-term store |
| Sensitive action | Policy check + human approval |
| Temporary technical failure | Bounded retry with backoff |
| Weak result | Change strategy in a bounded loop |
| Standard tool loop | LangChain `create_agent` |
| Custom control flow | LangGraph |

## Agent limits

```text
max steps
max retries per tool
model and tool timeout
token and cost budget
parallel-call limit
retrieval limit
```

## Evaluation checklist

- Correct final answer and evidence.
- Correct tool and arguments.
- Valid, efficient action trajectory.
- Authorization and approval rules followed.
- Acceptable latency, cost, and retry count.
- No sensitive data in logs or output.

## Design reminders

- A function performs code; a tool exposes a described and typed capability to a model.
- Structured output validates shape and types, not truth.
- Reflection needs criteria and a revision limit.
- Planning is useful when steps are not known in advance.
- Use an agent as a specialist only when it needs independent decisions.
- MCP standardizes connection and discovery; it does not grant trust or permission.
- Keep authorization, critical rules, and high-impact decisions outside model discretion.
