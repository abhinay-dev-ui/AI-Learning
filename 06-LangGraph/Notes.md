# LangGraph — Notes

These notes follow the 6.1–6.16 concept sequence. The running example is a research answer that retrieves evidence, checks it, and sometimes needs human approval. Python snippets illustrate the Graph API; the CodeLab comes later.

## 6.1 Why LangGraph?

A LangChain chain works well when the sequence is known: retrieve → prompt → model → parse. Requirements such as “rewrite and search again if evidence is weak” or “pause for approval” introduce control flow and persistent state. LangGraph makes those decisions and transitions explicit. It can call existing LangChain components inside its nodes.

## 6.2 State

**State** is the data carried between steps. A schema names its fields. For the running example:

```python
from typing_extensions import TypedDict

class ResearchState(TypedDict):
    question: str
    documents: list[str]
    answer: str
    retry_count: int
```

Keep fields that later nodes need; avoid storing every temporary local value. A node returns updates to fields instead of mutating a global object. Unless a reducer is declared, a returned value replaces the prior value for that field.

## 6.3 Nodes

A **node** is one named unit of work. It receives the current state and returns a partial update:

```python
def retrieve(state: ResearchState) -> dict:
    documents = search(state["question"])
    return {"documents": documents}
```

`search` represents the retriever already studied in RAG. Nodes can also call models, tools, or ordinary Python code. Give a node one clear responsibility so failures and saved progress are easy to inspect.

## 6.4 Edges, `START`, and `END`

An **edge** connects steps. `START` marks entry; `END` marks completion. A fixed edge says what always follows a node. A conditional edge asks a routing function which destination should follow. A graph must have a reachable path to `END`.

## 6.5 `StateGraph`, compile, and invoke

`StateGraph` collects the state schema, nodes, and edges. `compile()` validates/builds an executable graph. `invoke()` runs it with input state.

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(ResearchState)
builder.add_node("retrieve", retrieve)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", END)
graph = builder.compile()

# Supply all required input fields for this small example.
result = graph.invoke({"question": "Study duration?", "documents": [],
                       "answer": "", "retry_count": 0})
```

The compiled graph runs nodes; the builder describes their connections. Use a smaller input schema when callers should not have to supply internal fields.

## 6.6 Conditional routing

Routing reads state and returns the next path. It should decide, not perform the retrieval itself.

```python
def route_evidence(state: ResearchState) -> str:
    return "generate" if state["documents"] else "rewrite"

builder.add_conditional_edges(
    "check_evidence", route_evidence,
    {"generate": "generate", "rewrite": "rewrite"},
)
```

This assumes `check_evidence`, `generate`, and `rewrite` are registered nodes. For a real RAG system, evidence quality needs a stronger criterion than “nonempty.”

## 6.7 Loops

An edge may point to an earlier node. For weak evidence: retrieve → evaluate → rewrite → retrieve. Put `retry_count` or another clear stop condition in state, then route to a safe outcome or `END` after the limit. Without a bound, a graph may repeat indefinitely; a runtime recursion limit is a secondary guard, not the business rule.

## 6.8 Reducers

A **reducer** defines how updates to one state field combine. The default behavior is replacement. For an accumulating list:

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict

class TraceState(TypedDict):
    steps: Annotated[list[str], operator.add]
```

Returning `{"steps": ["retrieved"]}` appends to `steps` with this reducer. Use replacement for a current answer or retry count. Choose an appropriate reducer when branches can update the same field concurrently.

## 6.9 `MessagesState`

`MessagesState` is a convenient state schema with a `messages` field and the `add_messages` reducer. New messages usually append; a message with an existing ID can replace that message. It is useful for chat and tool-call histories, but ordinary workflow fields still belong in state.

```python
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    retry_count: int
```

## 6.10 Checkpointing

A **checkpointer** stores graph state at execution boundaries so a run can resume and its history can be inspected. Compile with one when persistence is needed:

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
```

`InMemorySaver` is for learning and local development; its data disappears when the process ends. A durable backend is needed across process restarts. Checkpointing saves workflow state; it does not automatically undo external side effects.

## 6.11 Threads

A **thread** identifies one persisted workflow instance. Pass its ID in the configuration on each related call:

```python
config = {"configurable": {"thread_id": "research-123"}}
result = graph.invoke(initial_state, config=config)
```

Use another ID for another request or conversation. A thread ID separates checkpoint histories; it is not authentication or an access-control rule.

## 6.12 Human in the loop: `interrupt()`

An interrupt pauses a node, saves the position through a checkpointer, and exposes a review request. Resume the **same thread** with a decision:

```python
from langgraph.types import Command, interrupt

def review(state: ResearchState) -> dict:
    decision = interrupt({"answer": state["answer"], "question": "Approve?"})
    return {"answer": state["answer"] if decision == "approve" else "Review rejected"}

graph.invoke(Command(resume="approve"), config=config)
```

On resume, the interrupted node starts from its beginning. Avoid irreversible work before `interrupt()` unless it is safe to repeat. The application must collect and validate the human decision.

## 6.13 Tools inside LangGraph

A **tool** exposes a capability such as database lookup or calculation. A **node** is a graph step. A node may call a tool directly when the route is fixed. In an agent loop, a model may request tools; a `ToolNode` executes those calls and returns tool messages, after which the model can continue. Tool access should be scoped and results checked before sensitive actions.

## 6.14 Subgraphs

A **subgraph** is a compiled graph used inside a parent graph. A retrieval subgraph could contain rewrite, retrieve, rerank, and quality check while the parent has a single “find evidence” step. Shared state fields can pass through directly; different state shapes need a wrapper that maps inputs and outputs. Use one when a workflow segment merits its own boundaries, not merely to add another layer.

## 6.15 Retry and error handling

Use a node retry policy for temporary failures such as a network timeout:

```python
from langgraph.types import RetryPolicy

builder.add_node("retrieve", retrieve, retry_policy=RetryPolicy(max_attempts=3))
```

Weak evidence is a **workflow decision**: update the query, increment `retry_count`, and follow a bounded loop. Invalid input usually needs a clear error or human correction. After a service failure, a fallback path may return a safe response; unexpected errors should remain visible for debugging. Review idempotency before retrying nodes that perform external actions.

## 6.16 LangChain vs LangGraph vs agents

| Need | Useful approach |
|---|---|
| Reusable prompts, retrievers, models, and simple composition | LangChain components or plain Python |
| Explicit branching, loops, state, pause/resume | LangGraph |
| Model chooses among next actions or tools | Agent workflow, often built with LangGraph |

An agent describes **who chooses an action**; LangGraph describes **how the workflow is orchestrated**. They can be used together. For a fixed retrieve → rerank → generate path, keep the path deterministic. Introduce model-driven choice only where the next step genuinely depends on interpretation.
