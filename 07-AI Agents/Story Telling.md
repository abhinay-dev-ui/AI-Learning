# Why AI Agents? — Storytelling

## A useful assistant reaches a boundary

Our RAG application can answer a question from retrieved evidence, and LangGraph can route, retry, pause, and resume a defined workflow. Then a researcher asks:

> Compare the last three authorized studies, calculate the change in recovery results, check for recorded incidents, and summarize the evidence.

The required capabilities are known, but every request may need a different subset and order.

## Give the model controlled choices

We expose a small set of tools:

```text
get_study_details
retrieve_authorized_evidence
calculate_percentage
get_recorded_incidents
```

The model observes the goal and chooses `get_study_details`. Application code checks authorization, validates the arguments, and executes it. The result returns as an observation. The model now has enough information to choose the calculation and evidence tools.

```text
Goal → Observe → choose allowed tool → validate and execute
  ↑                                      │
  └──────────── observe result ──────────┘
```

When no more tools are required, it produces a structured, evidence-backed answer.

## Control remains around the loop

The agent cannot use arbitrary functions. It receives only approved tools. Each call has a step limit, timeout, argument checks, and an audit trace. Study access is enforced before data reaches the model.

If the agent proposes a notification or record update, the workflow pauses. A human sees the action and its arguments, then approves, rejects, or edits it. The action occurs only after validation.

## One-minute mental story

LangChain supplies models, tools, schemas, and a convenient agent loop. LangGraph supplies explicit state and control when the process needs branches, persistence, approval, or recovery. MCP can connect external capabilities through a shared protocol.

The agent chooses moves inside boundaries designed by the application. In the clinical research platform, AI gathers and explains evidence; deterministic policy and qualified people control access and high-impact decisions.
