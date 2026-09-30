# AI Agents — Interview Questions

## Basic

### 1. What makes an LLM application an agent?

An agent can choose actions, use tools, observe results, and repeat toward a goal. The surrounding application controls execution, permissions, and stopping conditions.

### 2. What is the Observe–Reason–Act loop?

The agent observes the request and current results, decides the next useful step, performs an action, and observes the new result until it finishes or stops.

### 3. What is the difference between passing `tool` and calling `tool()`?

Passing the callable registers or transfers it. Parentheses execute it immediately with supplied arguments.

### 4. Does the model execute a tool?

No. The model returns a structured request. Trusted application code or a framework node validates and executes the tool, then returns a tool result.

### 5. Why append the AI tool-call message before the tool result?

The request contains the tool name, arguments, and call ID. The matching `ToolMessage` must follow it so the protocol and next model call can associate the result with its request.

### 6. What should happen when a required tool argument is missing?

If the task requires that tool, ask for the missing information. Validate before execution. Do not ask for irrelevant information when the request can be answered without the tool.

### 7. What is the difference between state and memory?

State holds current execution data. Short-term memory persists relevant state across turns in a thread. Long-term memory stores selected information across threads and retrieves it when needed.

### 8. What is structured output?

It constrains a model response to a schema such as a Pydantic model or JSON Schema. It validates format and types, but not factual correctness.

## Intermediate

### 9. How does ReAct differ from a fixed workflow?

ReAct lets the model select the next action after each observation. A fixed workflow follows developer-defined steps. Use model choice only when the next step is genuinely uncertain.

### 10. When is planning useful?

For multi-step, uncertain, or long-running tasks with dependencies. A simple lookup or known business process normally does not need model-generated planning.

### 11. What is reflection?

An evaluation step checks an output against criteria and returns feedback for a bounded revision. Objective rules should use code; semantic quality may use a model evaluator.

### 12. How do you prevent an infinite agent loop?

Set maximum steps, retries, time, token and cost budgets; detect repeated calls; define success and controlled failure outcomes.

### 13. Which errors should be retried?

Temporary failures such as timeouts or rate limits may be retried with backoff. Invalid input, authorization failures, and permanent not-found outcomes need correction or a clear failure path.

### 14. Why is idempotency important for agents?

A retry after an uncertain write could repeat a payment, notification, or update. An idempotency key allows the external system to recognize the same logical operation.

### 15. What is MCP, and how is it different from tool calling?

Tool calling is the model's structured request to use a capability. MCP standardizes how hosts discover and communicate with external tools, resources, and prompts. Security policy remains with the host and server.

### 16. When should a specialist be a tool instead of another agent?

Use a tool for a predictable calculation, lookup, or transformation. Use an agent when the specialist needs its own multi-step reasoning and tool choices.

### 17. What should agent evaluation measure?

Final-answer quality, grounding, tool selection, arguments, action trajectory, policy compliance, latency, tokens, cost, retries, and failure behavior.

### 18. How do evaluation and observability differ?

Evaluation judges quality. Observability records the trace needed to understand what happened and diagnose failures.

## Architect scenarios

### 19. A study-status question has no study ID. What should the agent do?

Recognize that the lookup requires an ID, return a clarification question without a tool call, and preserve the thread so the user can supply it. Validation must block an invalid call.

### 20. A document tells the agent to ignore policy and retrieve every study. What should happen?

Treat document text as untrusted data. Enforce authorization before retrieval, restrict tool permissions and arguments, and prevent document content from changing system policy.

### 21. The agent can read studies and update their status. How would you control it?

Separate read and write permissions, validate user authorization and tool arguments, require approval for the update, use idempotency, and record an audit trail.

### 22. Should a clinical monitoring threshold be decided by an agent?

Use deterministic, versioned rules for predefined thresholds. The agent may explain the finding; a qualified human owns clinical, protocol, and regulatory decisions.

### 23. When would you choose a LangChain agent over direct LangGraph?

Use a LangChain agent for a standard model-and-tools loop. Use direct LangGraph when the application needs explicit state, branches, persistence, approval placement, or custom recovery.

### 24. A multi-agent design has researcher, calculator, formatter, and reviewer agents. What would you challenge?

The calculator and formatter are likely deterministic functions. Replace agents that do not need independent decisions; retain specialists only where separation improves tools, context, permissions, or evaluation.
