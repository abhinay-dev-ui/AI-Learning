# AI Agents Resources

## Official LangChain and LangGraph documentation

- [LangChain and LangGraph learning guide](https://docs.langchain.com/oss/python/learn) — agent tutorials, custom LangGraph agents, memory, and multi-agent patterns.
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents) — current high-level agent concepts and APIs.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — lower-level orchestration for long-running, stateful agents.
- [LangGraph memory](https://docs.langchain.com/oss/python/concepts/memory) — short-term and long-term memory concepts.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — pause, human review, and resume.
- [LangSmith evaluation types](https://docs.langchain.com/langsmith/evaluation-types) — offline and online evaluation approaches.

## MCP

- [Model Context Protocol documentation](https://modelcontextprotocol.io/docs) — protocol overview and concepts.
- [MCP server primitives](https://modelcontextprotocol.io/specification/draft/server/index) — tools, resources, and prompts.

## Suggested reading order

1. Start with the LangChain agent guide after reading [Notes.md](Notes.md).
2. Revisit LangGraph memory and interrupts for stateful agents and approval.
3. Read MCP after tool calling is comfortable; MCP standardizes access to capabilities but does not replace the agent loop.
4. Read evaluation types before creating the CodeLab test cases.

Framework APIs evolve. Confirm current signatures in official documentation when implementing the CodeLabs.
