# LangGraph

## Overview

LangGraph organizes a workflow as shared **state**, processing **nodes**, and connecting **edges**. It is useful when the path can branch, loop, pause for a person, or resume later. The RAG and LangChain phases supplied the components; this phase explains how to coordinate them.

```text
Question → Retrieve → Check evidence ── enough ─→ Generate → Review → END
                         │
                         └─ weak → Rewrite → Retrieve
```

## Learning Objectives

By the end of this phase, you should be able to explain a graph's state and execution path, design a bounded loop, choose state reducers, persist a thread, pause for human review, and distinguish a defined workflow from an agent.

## Topics Covered

| Section | Concept | Main question |
|---|---|---|
| 6.1 | Why LangGraph? | When does a linear chain become awkward? |
| 6.2 | State | What information travels through the workflow? |
| 6.3 | Nodes | What does each step read and update? |
| 6.4 | Edges, `START`, `END` | How are steps connected? |
| 6.5 | `StateGraph`, compile, invoke | How is a graph built and run? |
| 6.6 | Conditional routing | How is the next step chosen? |
| 6.7 | Loops | How can work repeat safely? |
| 6.8 | Reducers | How are multiple updates combined? |
| 6.9 | `MessagesState` | How is message history updated? |
| 6.10 | Checkpointing | How is progress saved? |
| 6.11 | Threads | How are workflow instances separated? |
| 6.12 | Human in the loop | How does `interrupt()` pause for review? |
| 6.13 | Tools | How do graph steps call external capabilities? |
| 6.14 | Subgraphs | How is a complex step composed? |
| 6.15 | Retry and errors | Which failures deserve retry or fallback? |
| 6.16 | LangChain, LangGraph, agents | Which level of control fits the task? |

## Learning Path

Read [Notes.md](Notes.md) for the explanations, [Diagrams](Diagrams) for the execution picture, [Quick-Reference.md](Quick-Reference.md) for revision, and [Interview.md](Interview.md) to check understanding. [Story Telling.md](Story%20Telling.md) provides the intuition; [Resource.md](Resource.md) links to further reading.

The [CodeLab](CodeLab/README.md) starts with a small graph before connecting the earlier RAG components.

## Prerequisites

The earlier [RAG](../04-Retrieval%20Augmented%20Generation/README.md) and [LangChain](../05-%20LangChain/README.md) phases explain retrieval and reusable LLM components. LangGraph can orchestrate those components; it does not change how retrieval or a model works internally.

## Learning Outcome

You should be able to sketch a research workflow that retrieves evidence, routes on its quality, limits retries, requests approval when needed, and keeps each request's progress under its own thread ID.
