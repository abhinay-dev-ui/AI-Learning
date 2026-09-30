# LangGraph Resources

## Official documentation

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — purpose and relationship to LangChain.
- [Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api) — state, reducers, nodes, edges, routing, loops, and retries.
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — checkpointers and thread IDs.
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — human review and resume behavior.
- [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) — composing parent and child workflows.

## Suggested reading order

1. Read the overview and Graph API while using [Notes.md](Notes.md) as a map.
2. Read persistence and interrupts together; pause/resume depends on saved state and a stable thread ID.
3. Use subgraphs after the basic graph is comfortable.

The [master context](../Master%20Context.md) also lists the Krish Naik LangGraph playlist. Check official documentation for current Python API details when moving to the CodeLab.
