# RAG Complete CodeLab

## Purpose

A simple production-style RAG implementation built without
LangChain.

The purpose is to understand how each RAG component works
and how the components interact inside an application.

## What We Will Build

Documents
    ↓
Document Loader
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Store
    ↓
Retriever
    ↓
Context Construction
    ↓
LLM
    ↓
Answer

## Concepts Covered

- Document loading
- Document chunking
- Embeddings
- Vector storage
- Similarity search
- Metadata
- Retrieval
- Context construction
- Prompt construction
- LLM generation
- Complete RAG pipeline

## Dependencies

We will document the libraries used here as we introduce them.

Example:

Dependencies

- Python
- sentence-transformers
- ...
- ...

## Why No LangChain?

This CodeLab intentionally implements the RAG
pipeline without LangChain.

The goal is to understand the underlying mechanics
before learning framework abstractions.

## Production-Style Principles

- Separation of responsibilities
- Small focused modules
- Dependency isolation
- Reusable services
- Clear pipeline orchestration

## Running the Code

...

## Learning Outcome

By completing this CodeLab, we should be able to explain:

1. How documents enter a RAG system.
2. How documents are converted into chunks.
3. How embeddings represent text.
4. How similarity search works.
5. How relevant context is retrieved.
6. How context is provided to an LLM.
7. How the complete RAG pipeline works.
8. Where each responsibility belongs in an application.

## Architecture Seperation
- models       → data structures
- ingestion    → prepare documents
- embeddings   → convert text → vectors
- vectorstore  → store/search vectors
- retrieval    → decide what context to retrieve
- generation   → build context/prompt + call LLM
- main.py      → orchestrate everything

## main.py structure


def main():

    # 1. Prepare dependencies
    ...

    # 2. Ingest documents
    ...

    # 3. Retrieve relevant context
    ...

    # 4. Build prompt
    ...

    # 5. Generate answer
    ...

    # 6. Display result
    ...



## Diagram of what we built in RAG

                 ┌─────────────────────┐
                 │    Documents        │
                 └──────────┬──────────┘
                            │
                         Ingestion
                            │
                            ▼
                     ┌─────────────┐
                     │   Chunks    │
                     └──────┬──────┘
                            │
                        Embedding
                            │
                            ▼
                     ┌─────────────┐
                     │Vector Store │
                     └──────┬──────┘
                            │
              ──────────────┼──────────────
                            │
                         Query
                            │
                            ▼
                       Retrieval
                            │
                            ▼
                        Context
                            │
                            ▼
                         Prompt
                            │
                            ▼
                         LLM
                            │
                            ▼
                         Answer

                         
