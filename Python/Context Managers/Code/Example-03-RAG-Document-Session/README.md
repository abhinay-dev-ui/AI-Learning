# README.md

# Example 03 - RAG Document Processing Session

## Overview

This example demonstrates how a **Context Manager** can coordinate the lifecycle of multiple resources used during a Retrieval-Augmented Generation (RAG) document ingestion pipeline.

Unlike the previous examples that managed a single resource or behavior, this example manages several dependent components required for document processing.

The Context Manager is responsible for:

- Loading the embedding model
- Connecting to the vector database
- Providing a unified session object
- Cleaning up all resources in the correct order

The business layer focuses solely on document processing and is completely unaware of infrastructure concerns.

---

# Learning Objectives

After completing this example, you should be able to:

- Manage multiple resources within a single Context Manager.
- Understand resource ownership and lifecycle.
- Coordinate initialization and cleanup of AI components.
- Build production-style GenAI session management.
- Apply the Facade pattern using Context Managers.
- Separate AI infrastructure from business logic.

---

# Business Use Case

A Chartered Accountant uploads a document named **Income_Tax_Rules.pdf**.

The application performs the following operations:

- Load the embedding model.
- Connect to the vector database.
- Read the document.
- Generate embeddings.
- Store embeddings.
- Release all allocated resources.

Without a Context Manager, every pipeline would need to manually initialize and clean up these components.

Instead, the entire AI session is managed automatically.

---

# Architecture

```text
Application

        │

        ▼

RagSession Context Manager

        │

 ┌──────┴────────┐
 │               │
 ▼               ▼

Embedding      Vector
Model          Database

        │

        ▼

Business Logic

        │

        ▼

Cleanup Resources

        │

        ▼

Application Continues
```

---

# Project Structure

```text
Example-03-RAG-Document-Session/

│

├── README.md
├── Production-Improvements.md
├── app.py
│
├── ai/
│   ├── embedding_model.py
│   ├── vector_database.py
│   └── rag_session.py
│
├── services/
│   └── document_processing_service.py
│
├── models/
│   └── document.py
│
└── utils/
    └── logger.py
```

---

# Component Responsibilities

## app.py

Application entry point.

Creates the document processing request and starts the RAG session.

---

## ai/embedding_model.py

Simulates an embedding model.

Responsibilities:

- Load model
- Generate embeddings
- Release model

---

## ai/vector_database.py

Simulates a vector database.

Responsibilities:

- Connect
- Store vectors
- Disconnect

---

## ai/rag_session.py

Implements the Context Manager.

Responsibilities:

- Initialize AI resources
- Return the processing session
- Coordinate cleanup
- Manage resource lifecycle

---

## services/document_processing_service.py

Contains business logic.

Responsibilities:

- Read document
- Generate embeddings
- Store embeddings

No infrastructure management exists in this layer.

---

## models/document.py

Represents the uploaded document.

---

## utils/logger.py

Simple application logger.

---

# Execution Flow

```text
Load Embedding Model

↓

Connect Vector Database

↓

Read Document

↓

Generate Embeddings

↓

Store Embeddings

↓

Disconnect Vector Database

↓

Unload Embedding Model
```

---

# Context Manager Lifecycle

```text
RagSession()

↓

__enter__()

↓

Initialize Resources

↓

Return Session

↓

Execute Business Logic

↓

__exit__()

↓

Cleanup Resources
```

---

# Python Concepts Covered

- Context Managers
- Object Composition
- Returning self
- Resource Lifecycle
- Exception-safe cleanup
- Layered Architecture

---

# Production Concepts Covered

- RAG Pipeline
- Embedding Models
- Vector Databases
- Resource Ownership
- Session Management
- AI Infrastructure
- Facade Pattern

---

# Expected Output

```text
Loading embedding model...

Connecting to vector database...

Reading Income_Tax_Rules.pdf...

Generating embeddings...

Saving embeddings...

Disconnecting vector database...

Unloading embedding model...
```

---

# Key Takeaways

- A Context Manager can manage multiple related resources.
- AI infrastructure should be isolated from business logic.
- Resource cleanup should always be deterministic.
- A session object provides a clean interface to complex infrastructure.