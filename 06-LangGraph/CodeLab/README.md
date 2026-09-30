# LangGraph CodeLab

We will build this CodeLab one step at a time. The first exercise is deliberately small: an in-memory study lookup with no LLM. It isolates LangGraph's execution model before we introduce routing, loops, checkpoints, human review, or the existing RAG components.

## Step 1 — A two-node graph

Open [simple_graph.py](01-%20LangGraph%20Basics/simple_graph.py). The graph answers: “How long did STUDY-003 last?”

```text
START → lookup_study → format_answer → END
```

| Code | Why it exists |
|---|---|
| `StudyState` | Names the data shared between steps. |
| `lookup_study` | Reads `study_id` and returns one state update: `duration_months`. |
| `format_answer` | Reads the updated state and returns `answer`. |
| `StateGraph` and edges | Define the order explicitly. |
| `compile()` | Turns the definition into an executable graph. |
| `invoke()` | Starts one run with input state and returns the final state. |

The lookup table stands in for a database or retriever. Each node returns only the field it changes. LangGraph combines that update with the existing state, so `format_answer` can read both `study_id` and `duration_months`.

## Run it

From the `01- LangGraph Basics` folder:

```powershell
python simple_graph.py
```

Use a Python environment with the version in [requirements.txt](requirements.txt). The expected answer is `STUDY-003 lasted 36 months.` The printed final state also shows that fields from earlier steps remain available.

## Check your understanding

Before changing the code, predict the result of calling `graph.invoke({"study_id": "STUDY-002"})`. Then try it. Which node would need to change if the sentence format changed? Which node would need to change if the study data came from a database?

An unknown study ID currently raises `KeyError`. We will handle alternate paths in the routing step rather than hiding the failure in this first exercise.

## Step 2 — Conditional routing

Open [conditional_routing.py](02-%20Conditional%20Routing/conditional_routing.py). The lookup now uses `.get()`, so an unknown ID produces `None` instead of stopping the run with `KeyError`.

```text
START → lookup_study → route_study ── found ─→ format_answer → END
                              └── missing → study_not_found → END
```

`route_study` reads the state **after** `lookup_study` returns. It chooses a node name; it does not update the state. `add_conditional_edges` connects that choice to the corresponding node. Each answer node writes the same `answer` field, but only one runs for a given input.

Run `python conditional_routing.py` from the `02- Conditional Routing` folder. The script tries a known and an unknown study ID. Before running it, predict which answer node each input reaches and what the final state contains. The next step will use a conditional edge to make a bounded loop.

## Step 3 — The study RAG workflow

The [main example](03-%20Study%20RAG%20Workflow/README.md) applies these ideas to the study documents from the LangChain CodeLab. It adds a retrieval subgraph, evidence-based routing, a bounded query-rewrite loop, reducers, messages, node retries, checkpoints, threads, optional human review, and an optional LangChain/Ollama drafting chain. Work through its five-run sequence and inspect the trace after each run.
