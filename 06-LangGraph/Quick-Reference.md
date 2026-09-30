# LangGraph — Quick Reference

## Core mental model

```text
State = data carried forward
Node = work that returns state updates
Edge = next step
START / END = entry / completion
```

## Choose the mechanism

| Requirement | Mechanism |
|---|---|
| Always run B after A | `add_edge("a", "b")` |
| Choose B or C from state | `add_conditional_edges(...)` |
| Repeat after a quality check | Edge back + explicit stop condition |
| Accumulate one field | `Annotated[..., reducer]` |
| Keep messages | `MessagesState` |
| Resume saved progress | Checkpointer + `thread_id` |
| Request human decision | `interrupt()` + `Command(resume=...)` |
| Retry a temporary node failure | `RetryPolicy` |
| Group a workflow segment | Subgraph |

## Minimal graph

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str

def normalize(state: State) -> dict:
    return {"text": state["text"].strip()}

builder = StateGraph(State)
builder.add_node("normalize", normalize)
builder.add_edge(START, "normalize")
builder.add_edge("normalize", END)
graph = builder.compile()
result = graph.invoke({"text": "  hello  "})
```

## Persistence and review

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, interrupt

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "case-123"}}

# In a node: decision = interrupt({"question": "Approve?"})
# Later, with the same config:
# graph.invoke(Command(resume="approve"), config=config)
```

The example shows the API shape; the minimal graph above has no interrupt node. In-memory checkpoints do not survive a process restart.

## Decision reminders

- A retry policy handles a transient execution failure; a graph loop handles a meaningful change in the work, such as query rewrite.
- A tool supplies a capability; a node owns a step in the graph.
- Checkpointing stores progress; an external action may still need idempotency.
- A defined graph need not give control to an LLM. An agent lets a model select some actions.
