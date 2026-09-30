# AI Agents — Notes

These notes follow the 7.1–7.16 concept sequence. The running example is a study research assistant with controlled access to study lookup, evidence search, calculation, and notification capabilities. The CodeLabs come later.

## 7.1 Why AI agents?

A normal model call maps input to output. An agent can choose an intermediate action, observe the result, and continue. Use this flexibility when the required steps depend on information discovered during execution. Keep a fixed path deterministic when the sequence is already known.

```text
Known route: retrieve → rerank → answer
Dynamic route: model chooses an allowed tool → observes → chooses again or finishes
```

## 7.2 Components and execution loop

An agent needs a goal, instructions, a model, tools, state, and a control loop. The application owns the loop and stopping rules.

```text
Goal → context → model decision → action → observation → next decision
```

Every loop needs limits for steps, time, tokens, and cost. A model may propose an action; the application decides whether and how it runs.

## 7.3 Tool and function calling

A Python function becomes a tool when it is exposed with a name, description, and input schema. Type hints and descriptions help the model select it and produce arguments.

```python
from langchain_core.tools import tool

@tool
def get_study(study_id: str) -> dict:
    """Return information for a specific study ID."""
    return {"study_id": study_id, "status": "active"}

model_with_tools = model.bind_tools([get_study])
```

Passing `get_study` registers the callable; writing `get_study()` executes it immediately. A model response may contain zero, one, or several structured tool calls. It does not execute the Python function.

If a study-specific request lacks an ID, instructions should tell the model to ask for it. Schema and application validation must still reject missing or unauthorized arguments. A general question that needs no study lookup should not trigger that clarification.

## 7.4 Observe–Reason–Act / ReAct

The agent observes messages and tool results, decides the next useful action, acts, and observes again. ReAct combines reasoning and action in this iterative pattern. Applications need the observable decisions, tool calls, and results; they do not require hidden chain-of-thought text.

```text
Goal: summarize STUDY-101
Observe: no study data
Act: get_study("STUDY-101")
Observe: treatment A, active
Act: search_evidence("treatment A")
Observe: evidence returned
Act: final grounded answer
```

## 7.5 Basic agent implementation

The core loop appends the model response before any tool result because the response contains the request and its call ID.

```python
messages = [HumanMessage(content=user_question)]

while steps < max_steps:
    response = model_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        return response.content

    for call in response.tool_calls:
        result = tools_by_name[call["name"]].invoke(call["args"])
        messages.append(ToolMessage(
            content=str(result),
            tool_call_id=call["id"],
        ))
```

The history has a valid sequence: user request → AI tool request → matching tool result → next model decision. If multiple independent calls appear in one AI message, append one result for each call. If a later call depends on an earlier result, it belongs to the next loop iteration.

## 7.6 State and memory

**State** is the information available to the current execution. It can include messages, identifiers, results, step count, and errors. **Short-term memory** retains relevant state across turns in one thread. **Long-term memory** stores selected facts across threads and retrieves them only when relevant.

```text
State              current execution data
Short-term memory  persisted thread context
Long-term memory   selected cross-thread knowledge or preferences
```

Do not place every historical fact into each prompt. Store only justified information, retrieve selectively, and enforce data retention and access rules.

## 7.7 Planning and task decomposition

Planning turns a broad goal into executable steps. A static plan is created once; a dynamic plan changes after new observations. A planner may create tasks while an executor completes them.

```text
Goal → plan → execute next step → observe → revise or continue → finish
```

Planning helps with long or uncertain work, dependencies, and progress tracking. It adds model calls and failure modes, so a simple lookup or known business sequence should use direct code or explicit graph edges.

## 7.8 Reflection and self-correction

Reflection evaluates an intermediate or final result and decides whether to accept, revise, retrieve more evidence, or stop.

```text
Generate → evaluate ── pass ─→ finish
              └─ fail → feedback → revise, with a limit
```

Use code for objective requirements, a model evaluator for semantic quality, and a human for high-impact judgments. The evaluator needs clear criteria and supporting evidence. A revision counter prevents endless self-correction.

## 7.9 Structured output

Structured output asks the model to match a schema rather than return prose that application code must parse.

```python
from typing import Literal
from pydantic import BaseModel, Field

class StudyAssessment(BaseModel):
    study_id: str
    status: Literal["active", "completed", "unknown"]
    confidence: float = Field(ge=0, le=1)
    needs_more_evidence: bool

structured_model = model.with_structured_output(StudyAssessment)
```

Schemas are useful for plans, routes, evaluations, tool inputs, and API responses. Type validation proves that the shape is acceptable; it does not prove that the values are factually correct.

## 7.10 Human approval

Pause before a sensitive external action such as updating a record, sending a notification, or publishing a finding. Present the proposed tool, arguments, and effect; allow approve, reject, or edit; validate again before execution.

```text
Agent proposal → policy check → human decision → authorized execution → audit record
```

In LangGraph, `interrupt()` plus a checkpointer and stable `thread_id` supports pause and resume. Place irreversible actions after the approval boundary and make retryable writes idempotent.

## 7.11 Errors, retries, and limits

Classify failures before responding:

| Failure | Typical handling |
|---|---|
| Missing required input | Ask the user |
| Invalid or unauthorized input | Reject or route to correction |
| Temporary timeout or rate limit | Bounded retry with backoff |
| Permanent not-found result | Clear outcome or alternate path |
| Weak evidence | Change the query or strategy in a bounded workflow loop |
| Repeated identical action | Stop and return a controlled failure |

Limit steps, retries, time, tokens, cost, retrieved items, and parallel calls. Retry only safe operations. Use idempotency keys for external writes so a retry does not duplicate a notification or record.

## 7.12 Model Context Protocol (MCP)

MCP is an open protocol through which an AI host connects to servers that expose tools, resources, and prompts.

```text
Agent host → MCP client → MCP server → database, API, or service
```

Tool calling describes how the model selects a capability and supplies arguments. MCP standardizes discovery and communication with external capabilities. The host still decides which servers and tools are trusted, what a user may access, and which actions require approval.

## 7.13 Multi-agent systems

A multi-agent system assigns separate responsibilities to agents with different instructions, tools, context, or permissions. Common patterns include a supervisor delegating to specialists, sequential handoffs, and collaborative review.

```text
Coordinator → research specialist → analysis specialist → report
```

Use a specialist agent only when it needs its own multi-step decisions. A calculation, lookup, or fixed transformation should remain a function, tool, or node. Multiple agents increase cost, latency, context duplication, and debugging difficulty.

## 7.14 Evaluation and observability

Evaluate both the final outcome and the path taken to produce it:

- answer correctness, completeness, and grounding;
- correct tool selection and arguments;
- valid and efficient trajectory;
- authorization and approval compliance;
- latency, tokens, cost, retries, and failures.

Observability records what happened: request and thread IDs, model calls, tool calls and results, graph transitions, timing, usage, errors, and final output. Mask secrets and sensitive data. Use traces to diagnose failures found by offline test datasets and production monitoring.

## 7.15 Security and guardrails

Treat user text, retrieved documents, websites, and tool results as untrusted data. Prompt injection inside those sources must not override system policy. Apply controls in layers:

```text
Input validation
→ authentication and authorization
→ scoped context and tool allowlist
→ argument and policy validation
→ approval for sensitive actions
→ output validation
→ audit and monitoring
```

Use least privilege for every tool. Keep credentials outside prompts and model-visible state. Authorization must happen before protected data reaches retrieval results or model context.

For the clinical research platform, AI may retrieve, summarize, compare, calculate, classify predefined findings, and explain evidence. Humans retain clinical, protocol, and regulatory decisions.

## 7.16 LangChain agents vs LangGraph agents

Current LangChain agent implementations use LangGraph primitives. A LangChain `create_agent` provides a convenient standard tool loop. Direct LangGraph construction provides explicit state, branches, checkpoints, approvals, and custom failure routes.

| Need | Starting point |
|---|---|
| Standard model ↔ tool loop | LangChain agent |
| Learn the mechanics | Manual loop |
| Explicit stateful business process | Custom LangGraph |
| Deterministic calculation or rule | Plain Python/tool/node |
| Agent inside a controlled workflow | LangChain agent within LangGraph boundaries |

For the final platform, LangGraph can own authorization-aware orchestration, monitoring, approval, and recovery; bounded agent nodes can choose among approved research tools; deterministic services enforce rules and permissions.
