````md
# LangChain — Quick Reference

## What is LangChain?

LangChain is an application framework for connecting LLMs with:

- Prompts
- Documents
- Embeddings
- Vector stores
- Retrievers
- Output handling
- Tools
- External systems

LangChain provides **abstractions and orchestration**. It does not provide the intelligence itself.

```text
LLM + Retrieval + Prompts + Tools
              ↓
        LangChain
              ↓
     LLM Application
```

---

## Core Abstractions

| Concept | Purpose |
|---|---|
| `Document` | Content + metadata |
| Document Loader | Load external data into Documents |
| Text Splitter | Split Documents into chunks |
| Embeddings | Convert text → vectors |
| Vector Store | Store/search vectors |
| Retriever | Query → relevant Documents |
| `PromptTemplate` | Reusable text prompt |
| `ChatPromptTemplate` | Role-based chat prompt |
| Runnable | Standard executable component |
| LCEL | Compose Runnables |
| `RunnablePassthrough` | Pass input unchanged |
| `RunnableLambda` | Wrap custom Python logic |
| Output Parser | Process model response |
| Structured Output | Define expected output schema |
| Tool | Expose external capability to LLM/agent |

---

## Document

```python
Document(
    page_content="Treatment C lasted 36 months.",
    metadata={
        "study_id": "STUDY-003"
    }
)
```

Think:

```text
Document
├── page_content
└── metadata
```

---

## Vector Store vs Retriever

```text
Vector Store
= stores/searches embeddings

Retriever
= takes a query and returns relevant Documents
```

A Retriever may internally use:

```text
Vector Search
BM25
Hybrid Search
Database
API
Custom Search
```

Think of Retriever as the **retrieval interface**.

---

## PromptTemplate vs ChatPromptTemplate

### PromptTemplate

Creates one formatted text prompt.

```text
Context: {context}
Question: {question}
```

### ChatPromptTemplate

Preserves chat roles.

```text
System
  ↓
Human
  ↓
Chat Model
```

Use `ChatPromptTemplate` naturally with modern chat models.

---

## Runnable

A Runnable is an executable LangChain building block.

Conceptually:

```text
Input
  ↓
Runnable
  ↓
Output
```

Common operations:

```python
invoke()
batch()
stream()
ainvoke()
```

Prompts, models, parsers, retrievers, and chains can all behave as Runnables.

---

## LCEL

LCEL = **LangChain Expression Language**

Used to compose Runnables.

```python
chain = prompt | model | parser
```

Remember:

```text
Runnable
= building block

LCEL
= composition syntax
```

A composed chain is itself another Runnable.

---

## RunnablePassthrough

Pass input forward unchanged.

```text
            Question
             /    \
            /      \
     Retriever    Passthrough
         ↓             ↓
      Context       Question
```

Useful when the original query must remain available while another branch processes it.

---

## RunnableLambda

Wrap custom Python logic as a Runnable.

```python
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )
```

Conceptually:

```text
Documents
    ↓
RunnableLambda(format_docs)
    ↓
Context String
```

Remember:

```text
Passthrough
→ keep input

Lambda
→ transform input
```

---

## Output Parser

Processes the model response **after generation**.

Example:

```text
Chat Model
    ↓
AIMessage
    ↓
StrOutputParser
    ↓
Python String
```

Typical LCEL:

```python
prompt | model | StrOutputParser()
```

---

## Structured Output

Defines the expected schema **before model execution**.

Example:

```python
class StudyResult(BaseModel):
    duration_months: int
```

Then conceptually:

```python
model.with_structured_output(
    StudyResult
)
```

Remember:

```text
Output Parser
= post-processing

Structured Output
= output contract
```

---

## Tools

A Tool exposes an external capability to an LLM or agent.

Examples:

```text
Calculator
REST API
Database
Retriever
Search
Internal service
```

A tool normally has:

```text
Name
Description
Input Schema
Implementation
```

Flow:

```text
LLM / Agent
     ↓
Tool Call
     ↓
External Function
     ↓
Result
     ↓
LLM / Agent
```

---

## Basic LCEL Chain

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Output
```

```python
chain = (
    prompt
    | model
    | parser
)

result = chain.invoke(input)
```

---

## Basic LangChain RAG Flow

```text
                    Question
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
         Retriever        Passthrough
             ↓                   ↓
         Documents           Question
             ↓
     RunnableLambda
      format_docs()
             ↓
          Context
             └─────────┬─────────┘
                       ↓
              ChatPromptTemplate
                       ↓
                  Chat Model
                       ↓
                 Output Parser
                       ↓
                     Answer
```

---

## Manual RAG → LangChain

| Manual Implementation | LangChain |
|---|---|
| `Document` | `Document` |
| `DocumentLoader` | Document Loader |
| `DocumentChunker` | Text Splitter |
| `EmbeddingService` | Embeddings |
| `VectorStore` | Vector Store |
| `Retriever` | Retriever |
| `PromptBuilder` | PromptTemplate |
| `LLMService` | Chat Model |
| Python helper | RunnableLambda |
| Preserve input | RunnablePassthrough |
| Manual orchestration | LCEL |
| Response conversion | Output Parser |
| Typed response | Structured Output |
| External capability | Tool |

---

## Important Distinctions

### Runnable vs LCEL

```text
Runnable = executable component
LCEL     = way to connect components
```

### Vector Store vs Retriever

```text
Vector Store = vector storage/search
Retriever    = query → Documents interface
```

### RunnableLambda vs RunnablePassthrough

```text
Lambda      = transform input
Passthrough = preserve input
```

### Output Parser vs Structured Output

```text
Parser     = process generated response
Structured = define schema up front
```

### Retriever vs Tool

```text
Retriever = retrieval-specific abstraction
Tool      = generic callable capability
```

---

## What LangChain Does NOT Solve Automatically

LangChain does not automatically fix:

```text
Bad chunking
Bad embeddings
Poor retrieval
Authorization problems
Hallucination
Bad prompts
Low-quality context
Latency
Cost
Security
Evaluation
```

Framework abstraction ≠ good architecture.

---

## Interview One-Liners

### What is LangChain?

> A framework that provides standardized abstractions and composition mechanisms for building LLM applications involving prompts, models, retrieval, tools, and external systems.

### What is a Runnable?

> A standard executable LangChain component supporting operations such as invoke, batch, and stream.

### What is LCEL?

> LangChain Expression Language is the composition syntax used to connect Runnable components into executable pipelines.

### Retriever vs Vector Store?

> A vector store stores and searches embeddings, while a Retriever is the abstraction that takes a query and returns relevant documents.

### RunnableLambda vs RunnablePassthrough?

> RunnableLambda executes custom transformation logic, while RunnablePassthrough forwards the input unchanged.

### Output Parser vs Structured Output?

> An output parser processes a model response after generation, while structured output defines the expected response schema up front.

### What is a Tool?

> A Tool is a callable external capability with a name, description, input schema, and implementation that can be invoked by an LLM or agent.

---

## Mental Model

```text
Documents / APIs / Tools
          ↓
    LangChain Abstractions
          ↓
       Runnables
          ↓
         LCEL
          ↓
   Composed LLM Application
```

**Remember:** LangChain organizes and orchestrates components; the LLM, embeddings, retrieval models, and external systems provide the actual capabilities.
````
