# Study RAG Workflow — LangGraph CodeLab

This is the main example for the LangGraph phase. It reads the **same three study text files** used by the preceding LangChain RAG CodeLab. The earlier files remain unchanged. The default answer is deterministic and extractive, so we can see the graph's decisions without needing an LLM server. `--generator ollama` replaces only the drafting step with the familiar LangChain prompt → Ollama model → parser chain.

## The problem

A simple RAG chain can retrieve and answer in a fixed order. This workflow must also retry a temporary search failure, rewrite a weak query once, stop when evidence remains weak, and optionally pause for a person's approval. Those are control-flow concerns that LangGraph makes explicit.

```text
START → prepare → retrieval subgraph → enough evidence?
                     │                    ├─ no → safe fallback → finalize → END
                     │                    └─ yes → draft → review needed?
                     │                                       ├─ no → finalize → END
                     │                                       └─ yes → interrupt → resume → finalize → END
                     └─ retrieve → assess ── weak → rewrite → retrieve
```

The rewrite loop is limited to two searches. A node retry policy handles a **temporary execution failure** separately from that workflow loop.

## What each file teaches

| File | Purpose |
|---|---|
| [state.py](app/state.py) | Parent and child state; `MessagesState`; a list reducer in the retrieval subgraph. |
| [study_data.py](app/study_data.py) | Read earlier study files as LangChain `Document` objects and expose `search_studies` as a tool. |
| [workflow.py](app/workflow.py) | Nodes, conditional edges, bounded loop, subgraph, retry policy, drafting, and `interrupt()`. |
| [main.py](main.py) | Invoke one run, supply `thread_id`, inspect the pause, and resume it with `Command`. |
| [thread_demo.py](thread_demo.py) | Run two requests under separate thread IDs and read their saved answers. |

`search_studies` is a **tool**: a callable search capability. `retrieve` is a **node**: a scheduled graph step that invokes the tool and writes its result to state. In this workflow the developer decides when to search. An agent would allow a model to decide whether or which tool to call.

The search uses word overlap and study or treatment identity. It is a transparent stand-in for the vector retriever and cross-encoder reranker in the LangChain CodeLab. It refuses to pick an arbitrary study when the question names neither an ID nor a treatment. The extractive drafting function handles duration and success-criterion questions; it is not a general language model.

## Run the examples

Use the Python environment with [requirements.txt](../requirements.txt). From this folder:

```powershell
python main.py
python main.py --question "How long did Treatment C trial last?"
python main.py --question "What is the duration of STUDY-999?"
python main.py --review
python main.py --simulate-timeout
python main.py --simulate-failure
python thread_demo.py
```

The first query needs one search. “Treatment C trial” needs a rewrite and a second search. The unknown ID takes the safe fallback after two attempts. `--review` pauses and asks you to type `approve` or `reject`; for a scripted run, use `--review --decision approve`. `--simulate-timeout` fails the first execution attempt of the search node, then succeeds under its retry policy; the trace shows `node attempt 2` while the workflow search count remains `1`. `--simulate-failure` exhausts node retries and uses an error handler to return a different fallback. `thread_demo.py` shows two saved states in one process.

To try the earlier Ollama/Mistral setup, run `python main.py --generator ollama` with Ollama and the `mistral` model available locally. This path was also checked with the local Mistral model.

## Follow one run through the code

1. `prepare` extracts a study ID when present, sets the query, and starts the workflow search count at zero.
2. The retrieval **subgraph** runs `retrieve` and `assess_evidence`. If evidence is weak and an attempt remains, `rewrite_query` changes the query and loops back.
3. The parent graph routes to `draft_answer` or `no_evidence`. A retrieved LangChain `Document` includes source metadata, which the answer cites.
4. If review was requested, `interrupt()` returns a review payload. `main.py` reads the saved state for that thread and resumes with `Command(resume=...)` using the **same** `thread_id`.
5. `finalize` adds an AI message to `MessagesState` and returns the answer.

`RetrievalState.trace` uses `operator.add` to append events inside the child graph. The parent receives that completed trace once and then extends it explicitly. This avoids counting the child's earlier events twice. `MessagesState` supplies its own message-aware reducer.

## Persistence and scope

The example uses `InMemorySaver`. It keeps each `thread_id` separate while this Python process is running, but checkpoints disappear when the process exits. A persistent checkpointer is needed for a real service or approvals that may arrive after a restart. The script asks for approval in the same process to make pause/resume easy to observe; a real application would show the interrupt payload to a reviewer and resume later. Keep actions before an interrupt repeatable, because the interrupted node starts again on resume.

## Check your understanding

- Why does `--simulate-timeout` show **node attempt 2** but **search attempt 1**?
- Why does `route_search` return a destination instead of a state update?
- What would you replace to use the previous vector retriever and reranker while keeping the graph structure?
- Why must resume use the same thread ID?
