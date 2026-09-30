# Why LangGraph? — Storytelling

## A familiar starting point

Our RAG application has a clear route: retrieve documents, rerank them, put context in a prompt, and generate an answer. LangChain helps connect those pieces. For a fixed route, that is enough.

## A new requirement

One day the retrieved evidence is weak. The application should rewrite the query and search once more. Another answer has high impact and needs a researcher's approval before it is shared.

```text
Retrieve → Check evidence ── good ─→ Draft → Human review → Finish
              │
              └─ weak → Rewrite → Retrieve
```

The application now needs to remember the current question, documents, retry count, and draft. It also needs to know where to go next and how to wait for a person without leaving a process running.

## The LangGraph idea

Write that shared information as **state**. Give each action a **node**. Draw **edges** for the possible next steps. Let a routing function inspect the evidence. Stop the rewrite loop after a defined number of attempts. Save progress with a checkpointer and identify this research request with a thread ID.

At the review step, `interrupt()` pauses. The researcher sees the draft and provides a decision. The same thread resumes, and the workflow follows the approved route.

## One-minute mental story

LangChain gives us reusable building blocks. LangGraph gives the workflow a map, a working memory, and a place to pause. The map can be entirely developer defined. If the model chooses some actions or tools, that part is an agent workflow.
