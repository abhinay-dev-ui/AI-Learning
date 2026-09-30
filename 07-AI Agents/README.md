# AI Agents

## Overview

An AI agent receives a goal, observes its current context, chooses an action, and repeats until it can finish or must stop. The model can request tools, but trusted application code validates and executes them.

```text
Goal → Observe → Reason → Act → Observe again
                         │
                         ├── call a tool
                         ├── ask for missing input
                         └── return the answer
```

This phase builds on LangChain components and LangGraph orchestration. It focuses on where model-selected actions are useful and where deterministic workflows, rules, and human decisions should remain in control.

## Learning Objectives

By the end of this phase, you should be able to explain an agent loop, expose safe tools, distinguish state from memory, design bounded planning and reflection, use structured output, add human approval, evaluate an agent's result and trajectory, and choose between a prebuilt LangChain agent and a custom LangGraph workflow.

## Topics Covered

| Section | Concept | Main question |
|---|---|---|
| 7.1 | Why agents? | When does model-selected action add value? |
| 7.2 | Components and loop | What turns a model call into an agent? |
| 7.3 | Tool and function calling | How does a model request external work? |
| 7.4 | Observe–Reason–Act / ReAct | How does the agent use observations to choose the next action? |
| 7.5 | Basic agent | What happens inside the tool execution loop? |
| 7.6 | State and memory | What is retained during and across runs? |
| 7.7 | Planning | How is a broad goal decomposed into steps? |
| 7.8 | Reflection | How can a result be checked and revised? |
| 7.9 | Structured output | How does the application receive validated fields? |
| 7.10 | Human approval | Where should execution pause for a person? |
| 7.11 | Errors, retries, limits | How does the agent stop and fail safely? |
| 7.12 | MCP | How are external tools and context exposed through a standard protocol? |
| 7.13 | Multi-agent systems | When should work be delegated to specialists? |
| 7.14 | Evaluation and observability | Was the result and execution path good? |
| 7.15 | Security and guardrails | Which controls must surround the model? |
| 7.16 | LangChain vs LangGraph agents | Which abstraction fits the workflow? |

## Learning Path

Read [Notes.md](Notes.md) for the concept sequence, [Diagrams](Diagrams) for the execution and control boundaries, [Quick-Reference.md](Quick-Reference.md) for revision, and [Interview.md](Interview.md) to test understanding. [Story Telling.md](Story%20Telling.md) gives the intuition; [Resource.md](Resource.md) links to current official material.

The [CodeLab roadmap](CodeLab/README.md) separates the phase into two required small applications and one optional integration exercise. We will implement them together later.

## Prerequisites

- [LangChain](../05-%20LangChain/README.md) for models, tools, structured output, and composition.
- [LangGraph](../06-LangGraph/README.md) for state, routing, loops, persistence, and human review.
- RAG concepts for the study research examples.

## Connection to the Final Project

The future **AI-Assisted Clinical Research Intelligence & Monitoring Platform** will use bounded agent behavior for research tasks while keeping authorization, predefined monitoring rules, clinical boundaries, and approval decisions deterministic.

```text
Research question → authorized tools → grounded answer
Study data → deterministic checks → explanation → human decision
```

## Learning Outcome

You should be able to design an agent that selects only approved tools, preserves the correct state, asks for missing input, stops within defined limits, records its execution, and leaves high-impact decisions to trusted code or a human reviewer.
