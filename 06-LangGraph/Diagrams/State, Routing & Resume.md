# State, Routing, and Resume — Diagram

## State updates

```mermaid
flowchart LR
    A[Current state] --> N[Node reads state]
    N --> U[Partial update]
    U --> D{Field reducer?}
    D -- No --> R[Replace field value]
    D -- Yes --> C[Combine values]
    R --> B[Next state]
    C --> B
```

`MessagesState` uses message-aware update behavior for the `messages` field. Other fields can use their own reducers or normal replacement.

## Thread and review

```mermaid
sequenceDiagram
    participant App as Application
    participant Graph as Compiled graph
    participant Store as Checkpointer
    participant Human as Reviewer
    App->>Graph: invoke(input, thread_id)
    Graph->>Store: Save state for thread
    Graph-->>App: interrupt(review request)
    App->>Human: Show draft
    Human-->>App: Decision
    App->>Graph: invoke(Command(resume=decision), same thread_id)
    Graph->>Store: Load saved position
    Graph-->>App: Continue to result
```

An interrupted node starts again on resume. Keep actions before the interrupt repeatable.
