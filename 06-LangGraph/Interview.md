# LangGraph — Interview Questions

## Basic

### 1. Why use LangGraph after LangChain?

LangChain provides reusable LLM application components and straightforward composition. LangGraph adds explicit state and control flow for branches, loops, persistence, and pause/resume.

### 2. What are state, nodes, and edges?

State holds workflow data. Nodes read it and return updates. Edges determine which node runs next; `START` enters the graph and `END` completes it.

### 3. What do `compile()` and `invoke()` do?

`compile()` makes the graph definition executable. `invoke()` runs that graph with input state and optional configuration.

### 4. What is conditional routing?

A routing function inspects state and selects a destination, such as “generate” for sufficient evidence or “rewrite” for weak evidence.

### 5. What is a reducer?

A reducer combines updates to one state field. Without one, an update normally replaces the field; `operator.add` can accumulate list entries.

### 6. Why use `MessagesState`?

It provides a `messages` field with message-aware update behavior, useful for conversation and tool-call histories.

## Intermediate

### 7. How do you stop a rewrite loop?

Track a retry count or other explicit limit in state and route to a fallback or `END` when the limit is reached.

### 8. What is the relationship between checkpointers and threads?

The checkpointer stores snapshots; `thread_id` identifies which workflow instance those snapshots belong to. A durable backend is needed across process restarts.

### 9. How does human review resume?

`interrupt()` pauses the graph. The application later invokes it with `Command(resume=...)` and the same thread ID. The interrupted node executes again from its start.

### 10. How does a tool differ from a node?

A tool is a callable capability. A node is a step in the graph; it may invoke a tool directly or execute a model's tool request.

### 11. When is a subgraph useful?

When a reusable or complex segment has its own steps and state concerns, such as retrieval with rewrite and quality checking.

## Architect scenarios

### 12. A retrieval API times out, but a second search returns weak evidence. How do you handle each?

Retry the transient API failure with a node retry policy. For weak evidence, change the query and follow a bounded graph loop; repeated identical API calls will not improve relevance.

### 13. A node sends a notification before an interrupt. What could happen on resume?

The node starts again, so it could send the notification twice. Move the action after review or make it idempotent.

### 14. Must every graph be an agent?

No. A graph can run a fully defined route. It becomes agentic where the model decides the next action or tool.
