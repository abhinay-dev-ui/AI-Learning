````md
# LangChain

## Overview

LangChain is a framework for building applications that use Large Language Models together with components such as prompts, retrievers, vector stores, tools, structured outputs, and external services.

In the previous RAG chapter, we intentionally built the retrieval pipeline manually without LangChain.

We implemented and understood components such as:

- Document loading
- Chunking
- Embeddings
- Vector search
- Metadata filtering
- Hybrid retrieval
- Reranking
- Query transformation
- Multi-query retrieval
- Query decomposition
- Context compression
- Prompt building
- LLM generation
- RAG evaluation

This was intentional.

The goal was to understand how RAG works internally before introducing a framework that abstracts many of those responsibilities.

LangChain is therefore introduced here as an **application orchestration and abstraction framework**, not as a replacement for understanding the underlying AI concepts.

---

## Why Learn LangChain?

Without a framework, an LLM application may contain manual orchestration such as:

```text
User Query
    ↓
Retriever
    ↓
Retrieved Documents
    ↓
Context Builder
    ↓
Prompt Builder
    ↓
LLM
    ↓
Output Processing
````

LangChain provides standardized abstractions for many of these components and makes them easier to compose.

For example:

```text
Prompt
  ↓
Model
  ↓
Output Parser
```

can be composed using LangChain Expression Language:

```python
chain = prompt | model | parser
```

LangChain does not provide the intelligence itself.

The intelligence still comes from:

* Large Language Models
* Embedding models
* Reranking models
* Retrieval systems

LangChain mainly helps organize, connect, and execute those components.

---

## Learning Approach

This chapter follows the same concept-first learning approach used throughout the GenAI roadmap.

We will:

1. Understand the LangChain abstraction.
2. Map it to something we already implemented manually.
3. Understand why the abstraction exists.
4. Learn how components are composed.
5. Build one integrated LangChain CodeLab.
6. Compare the LangChain implementation with our manual RAG implementation.
7. Understand when LangChain is useful and when plain Python may be simpler.

We will avoid treating LangChain as a collection of APIs that need to be memorized.

The goal is to understand the architecture behind the framework.

---

## Core Concepts

This chapter covers the following LangChain concepts.

### Document

A `Document` represents content together with metadata.

Conceptually:

```text
Document
├── page_content
└── metadata
```

This is equivalent to the `Document` model created manually in our RAG CodeLab.

---

### Document Loaders

Document loaders read information from external sources and convert it into LangChain `Document` objects.

Sources may include:

* Text files
* PDFs
* CSV files
* Web pages
* Databases
* External services

Conceptually:

```text
External Source
      ↓
Document Loader
      ↓
Documents
```

---

### Text Splitters

Text splitters divide large documents into smaller chunks suitable for retrieval.

```text
Document
   ↓
Text Splitter
   ↓
Chunks
```

This corresponds to the manual `DocumentChunker` used in our RAG implementation.

---

### Embeddings

Embedding integrations convert text into numerical vector representations.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

LangChain provides a common interface for different embedding providers.

---

### Vector Stores

Vector stores hold embeddings and support similarity search.

Examples of vector-store integrations include:

* FAISS
* Chroma
* Pinecone
* Qdrant
* Weaviate

Conceptually:

```text
Embeddings
    ↓
Vector Store
    ↓
Similarity Search
```

---

### Retriever

A Retriever accepts a query and returns relevant documents.

```text
Query
  ↓
Retriever
  ↓
Relevant Documents
```

A Retriever is an abstraction.

Its underlying implementation may use:

* Vector search
* BM25
* Hybrid retrieval
* APIs
* Databases
* Custom enterprise retrieval logic

A Vector Store and a Retriever are therefore not the same thing.

```text
Vector Store
= stores and searches vectors

Retriever
= interface that returns relevant documents
```

---

### PromptTemplate

`PromptTemplate` creates reusable prompts containing dynamic variables.

Example variables:

```text
{context}
{question}
```

This corresponds to the manual `PromptBuilder` used in our RAG CodeLab.

---

### ChatPromptTemplate

`ChatPromptTemplate` represents prompts using chat-message roles.

For example:

```text
System Message
      ↓
Human Message
      ↓
Chat Model
```

This is useful for modern chat models where system and user instructions should remain separate.

---

## Runnable

A Runnable is a LangChain component that follows a standard execution interface.

Common operations include:

```text
invoke()
batch()
stream()
ainvoke()
```

Many LangChain components are Runnables, including prompts, models, parsers, and composed chains.

Conceptually:

```text
Input
  ↓
Runnable
  ↓
Output
```

---

## LCEL

LCEL stands for:

**LangChain Expression Language**

It is the composition syntax used to connect Runnable components.

Example:

```python
chain = prompt | model | parser
```

The distinction is:

```text
Runnable
= executable building block

LCEL
= way of composing Runnable building blocks
```

A composed LCEL chain is itself also a Runnable.

---

## RunnablePassthrough

`RunnablePassthrough` forwards input without changing it.

This is useful when the same input must travel through multiple branches.

Example in RAG:

```text
                  Question
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
      Retriever         RunnablePassthrough
          ↓                     ↓
       Context          Original Question
          └──────────┬──────────┘
                     ↓
                   Prompt
```

---

## RunnableLambda

`RunnableLambda` wraps a regular Python function so that it can participate in a LangChain Runnable pipeline.

Example use:

```text
Retrieved Documents
       ↓
RunnableLambda
       ↓
Format Documents
       ↓
Context
```

The key distinction is:

```text
RunnablePassthrough
= preserve input

RunnableLambda
= execute custom Python transformation
```

---

## Output Parsers

Output parsers process the response returned by a model.

For example:

```text
Chat Model
    ↓
AIMessage
    ↓
StrOutputParser
    ↓
Python String
```

Output parsers can also transform model responses into structured application data.

---

## Structured Output

Structured output defines the expected response schema before the model is called.

For example:

```python
class StudyResult:
    duration_months: int
```

Conceptually:

```text
Output Schema
     ↓
Model
     ↓
Structured Result
```

The important distinction is:

```text
Output Parser
= process model output after generation

Structured Output
= define the expected output contract up front
```

Structured output is especially useful when model responses are consumed by application logic, APIs, workflows, or databases.

---

## Tools

A Tool is a callable capability that an LLM or agent can use to interact with external systems or application logic.

Examples include:

```text
Calculator
Database query
REST API
Retriever
Search service
Internal business service
```

A tool typically defines:

```text
Name
Description
Input schema
Implementation
```

Conceptually:

```text
LLM / Agent
     ↓
Tool Call
     ↓
Application Function / External System
     ↓
Tool Result
     ↓
LLM / Agent
```

Tools form an important bridge between standard LangChain pipelines and agentic systems.

---

## Manual RAG vs LangChain

The concepts implemented manually in the previous chapter map naturally to LangChain abstractions.

| Manual RAG Implementation    | LangChain                               |
| ---------------------------- | --------------------------------------- |
| `Document`                   | `Document`                              |
| `DocumentLoader`             | Document Loader                         |
| `DocumentChunker`            | Text Splitter                           |
| `EmbeddingService`           | Embeddings                              |
| `VectorStore`                | Vector Store                            |
| `Retriever`                  | Retriever                               |
| `PromptBuilder`              | `PromptTemplate` / `ChatPromptTemplate` |
| `LLMService`                 | Chat Model                              |
| Custom Python processing     | `RunnableLambda`                        |
| Pass original input          | `RunnablePassthrough`                   |
| Manual orchestration         | Runnable + LCEL                         |
| Response conversion          | Output Parser                           |
| Typed response contract      | Structured Output                       |
| External function/capability | Tool                                    |

---

## Conceptual LangChain RAG Pipeline

A basic LangChain RAG application may look like:

```text
                    User Question
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
         Retriever          RunnablePassthrough
             │                       │
             ▼                       │
         Documents                   │
             ↓                       │
      Format Documents               │
      RunnableLambda                 │
             ↓                       │
          Context                    │
             └───────────┬───────────┘
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

## CodeLab

After completing the core LangChain concepts, we will build one integrated CodeLab rather than creating many disconnected examples.

The CodeLab will demonstrate:

```text
Document Loading
      ↓
Text Splitting
      ↓
Embeddings
      ↓
Vector Store
      ↓
Retriever
      ↓
Runnable / LCEL Composition
      ↓
ChatPromptTemplate
      ↓
Chat Model
      ↓
Output Parser
      ↓
Answer
```

Where useful, we will also demonstrate:

* Structured output
* Custom Runnable logic
* Tool basics

The CodeLab will then be compared directly against the manual RAG implementation.

---

## What LangChain Does Not Replace

LangChain does not remove the need to understand:

* Chunking strategy
* Embedding quality
* Retrieval quality
* Metadata filtering
* Authorization
* Reranking
* Prompt design
* Evaluation
* Hallucination
* Latency
* Cost
* Security

A poorly designed RAG system remains poorly designed even if it uses LangChain.

LangChain provides abstractions and orchestration; it does not automatically solve architecture or retrieval-quality problems.

---

## Key Mental Model

The most important way to think about LangChain is:

```text
LLMs + Retrieval + Prompts + Tools
            ↓
      Standard Interfaces
            ↓
         Runnables
            ↓
           LCEL
            ↓
      Composed Application
```

LangChain should therefore be understood as an **application framework for composing LLM-related capabilities**, rather than as the source of the AI itself.

---

## Learning Outcome

After completing this chapter, we should be able to:

* Explain what LangChain is and why it exists.
* Understand its major abstractions.
* Explain Runnable vs LCEL.
* Explain Retriever vs Vector Store.
* Explain `RunnableLambda` vs `RunnablePassthrough`.
* Explain Output Parser vs Structured Output.
* Understand how Tools connect LLMs to external capabilities.
* Build an end-to-end LangChain RAG pipeline.
* Compare LangChain with a manual Python implementation.
* Decide when LangChain provides useful abstraction and when plain Python may be preferable.

```
```
