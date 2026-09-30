# AI Agents CodeLab Roadmap

We will build these applications together after reviewing the documentation. This file defines scope only; implementation will be added one step at a time so each model call, tool request, branch, and state update is understood before moving forward.

## Application 1 — Study Research Agent

```text
Question
→ model chooses an approved study tool
→ application validates and executes it
→ tool result returns as an observation
→ another tool call or structured final answer
```

Covers:

- tool and function calling;
- one tool cycle and a full Observe–Reason–Act loop;
- dependent study and treatment tool calls;
- argument validation, retries, and step limits;
- the difference between model-directed and application-enforced control.

## Application 2 — Study Monitoring and Approval Agent

```text
Monitoring goal
→ create or follow a plan
→ inspect study data
→ run predefined deviation checks
→ explain the finding
→ pause for human review
→ resume and finalize
```

Covers:

- explicit LangGraph state;
- short-term memory, checkpoints, and threads;
- planning where it adds value;
- human approval;
- retry and failure routes;
- observability and safe termination.

The deviation threshold remains deterministic. AI explains the evidence; the human owns the decision.

### Problem statement

A clinical study expects 100 enrolled participants but currently has 72. The
application calculates a 28% enrollment deviation. Because the predefined
review threshold is 20%, the finding requires human review before the
monitoring action can be finalized.

```text
Expected enrollment: 100
Current enrollment:   72
Deviation:            (100 - 72) / 100 * 100 = 28%
Review threshold:     20%
Result:               Human review required
```

### What the example builds

The agent creates a short review plan, calculates the deviation, records the
evidence in graph state, and routes the finding according to the deterministic
threshold. The plan is passed into the evidence explanation so it affects later
work. A high deviation pauses the graph for human approval. The same thread
later resumes with the approval decision and produces the final result.

```text
Monitoring request
→ create a review plan
→ calculate enrollment deviation
→ apply the predefined threshold
→ finalize a low deviation or pause a high deviation
→ receive approve, reject, or revise decision
→ resume the same thread and finalize
```

Responsibility stays explicit:

- the model plans and explains the evidence;
- Python calculates the percentage, applies the threshold, and controls flow;
- the human approves or rejects the proposed monitoring action.

## Application 3 — Multi-Agent Study Review

This final mini app demonstrates bounded collaboration between specialized
agents. A supervisor delegates separate tasks to research and monitoring
specialists. They work in parallel and write separate structured reports. The
coordinator waits for both reports and combines them without changing their
evidence or making a human approval decision.

### Problem statement

A study review needs two different perspectives. A supervisor agent creates
separate assignments. A research agent summarizes recorded study evidence. A
monitoring agent explains a deterministic enrollment calculation and threshold
result. A coordinator agent combines both reports into one clear next step.

```text
Study context
→ supervisor agent creates two bounded assignments
   ├→ research agent → structured research report
   └→ monitoring agent → structured monitoring report
→ wait for both specialists
→ coordinator agent synthesizes one structured report
→ END
```

This teaches model-created delegation, distinct specialist roles, parallel
graph branches, fan-in, structured inter-agent communication, and final
synthesis. Each agent is a separate model invocation with its own prompt and
output contract. The research agent receives authoritative source facts. The
monitoring agent receives a calculation performed by Python. This keeps source
data and arithmetic fixed while the agents analyze, explain, and coordinate.

## Objective audit

| CodeLab | Basic requirement | Where it is satisfied |
|---|---|---|
| 1. Study Research Agent | Tool calling and Observe–Reason–Act | Step 1 exposes a tool schema; Step 2 executes one model-requested call; Step 3 lets the model choose each action in a bounded loop; Step 4 demonstrates a guarded hybrid workflow with validation and retries. |
| 2. Monitoring and Approval Agent | State, planning, memory, human approval, and failure handling | The final graph stores evidence in state, consumes the generated plan during explanation, checkpoints by thread ID, pauses and resumes with `interrupt`, routes model failures safely, and gives approve/reject/revise distinct outcomes. |
| 3. Multi-Agent Study Review | Real delegation and specialist collaboration | A supervisor model delegates work to research and monitoring model agents; both run in parallel and return typed reports; a coordinator model waits for both and synthesizes them. |

The original Phase 7 requirements are all represented:

| Requirement | CodeLab |
|---|---|
| Tool calling | 1 |
| Observe–Reason–Act loop | 1 |
| State and memory | 2 |
| Planning | 2 and 3 |
| Structured output | 2 and 3 |
| Human approval | 2 |
| Retry and failure handling | 1 and 2 |
| Small multi-agent example | 3 |

## CodeLab boundary

The CodeLabs teach agent mechanics. The separate final repository will contain the **AI-Assisted Clinical Research Intelligence & Monitoring Platform**, integrating RAG, LangChain, LangGraph, agents, production controls, and later deployment work.

## Completed CodeLabs and run commands

Run these commands from the `07-AI Agents\CodeLab` folder.

### 1. Study Research Agent

The four files progress from inspecting a tool request to one execution cycle,
a model-directed loop, and a production-style guarded loop. Step 3 is the pure
agent example: the model selects `get_study`, then selects `get_treatment` from
the observation, then answers. Its success depends on the model following the
instructions; an invalid request becomes a tool-error observation and the loop
stops at its round limit if the model does not recover. Step 4 is the reliability comparison: Python enforces the
dependent lookup if the local model stops early, while the model still selects
the first tool and writes the final answer.

```powershell
& "..\..\05- LangChain\.venv\Scripts\python.exe" `
  ".\01- Study Research Agent\step_04_resilient_agent.py"
```

### 2. Study Monitoring and Approval Agent

The four files add explicit state, structured planning, checkpointed threads,
conditional routing, human approval, retries, and safe failure routes. The
final step uses the generated plan while explaining the evidence. Enter
`approve`, `reject`, or `revise` when the final program pauses; each choice now
produces a different operational outcome.

```powershell
& "..\..\05- LangChain\.venv\Scripts\python.exe" `
  ".\02- Study Monitoring and Approval Agent\step_04_safe_monitoring_agent.py"
```

### 3. Multi-Agent Study Review

The final mini app invokes four roles: supervisor, research specialist,
monitoring specialist, and coordinator. The two specialists run as parallel
model calls, return typed reports, and join before coordinator synthesis.

```powershell
& "..\..\05- LangChain\.venv\Scripts\python.exe" `
  ".\03- Multi-Agent Study Review\multi_agent_study_review.py"
```

The examples use the local `mistral` Ollama model. Model-directed behavior can
vary between runs; validation, deterministic calculations, bounded loops, and
explicit graph routes keep that behavior visible and controlled.
