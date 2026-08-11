# RAG - Notes

## Learning Journey

This phase explains how Retrieval-Augmented Generation (RAG) enables an LLM to use external knowledge to generate more relevant and grounded responses.

---

# 1. Introduction to RAG

## Definition

**Retrieval-Augmented Generation (RAG)** is a technique where relevant information is retrieved from an external knowledge source and provided to an LLM as context before generating a response.

Instead of relying only on the knowledge stored in the model's weights:

```text
User Question
      │
      ▼
Retrieve Relevant Information
      │
      ▼
Provide Context to LLM
      │
      ▼
Generate Answer
```

---

## Why was it introduced?

LLMs have limitations when working with:

- Private organizational data
- Frequently changing information
- Domain-specific documents
- Knowledge that was not available during model training

RAG allows an application to provide this information to the LLM at query time without modifying the model.

---

## Problems It Tries to Solve

### 1. External Knowledge

Allows an LLM to answer using information outside its training data.

### 2. Private Data

Allows applications to use internal documents and knowledge bases.

### 3. Outdated Knowledge

New or updated information can be made available through the knowledge base without retraining the LLM.

### 4. Hallucinations

Providing relevant context can reduce the likelihood of unsupported answers.

RAG reduces hallucinations but does not completely eliminate them.

---

## High-Level Working

RAG consists of two major flows.

### Indexing

Documents are prepared and stored for retrieval.

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Embedding Model
    │
    ▼
Vector Database
```

### Retrieval + Generation

When the user asks a question:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Context Injection
      │
      ▼
LLM
      │
      ▼
Answer
```

---

## Key Concepts

### Retrieval

Finding relevant information from an external knowledge source.

### Augmentation

Adding the retrieved information to the prompt as context.

### Generation

The LLM generates the final response using the question and retrieved context.

```text
Retrieval
    +
Augmentation
    +
Generation
    =
RAG
```

---

## Real-World Analogy

Imagine asking a doctor a question.

Instead of relying only on memory, the doctor:

```text
Question
   │
   ▼
Find Relevant Medical Reference
   │
   ▼
Read Relevant Information
   │
   ▼
Provide Answer
```

RAG follows a similar approach:

**Retrieve → Read Context → Generate Answer**

---

## GenAI Engineering Relevance

RAG is commonly used for:

- Chat with PDFs
- Enterprise knowledge assistants
- Healthcare and pharmacy assistants
- Legal document systems
- Customer support
- Internal company search
- Research assistants

It is one of the core techniques for building applications that connect LLMs with external knowledge.

---

## Important Points

- RAG does not modify the LLM's weights.
- External knowledge is supplied at query time.
- RAG does not require model retraining when documents change.
- Retrieval quality directly affects the final response.
- RAG reduces hallucinations but cannot guarantee factual correctness.
- The LLM generates the answer; the retrieval system provides the context.

---

## Interview Insight

A useful distinction to remember:

> **RAG does not teach the model new knowledge. It gives the model relevant information at inference time.**

---

## Key Takeaways

- RAG connects LLMs with external knowledge.
- It consists of Retrieval, Augmentation, and Generation.
- Documents are prepared before they can be retrieved.
- Retrieved information is provided to the LLM as context.
- RAG is especially useful for private, domain-specific, and frequently changing information.

---

# 2. Chunking

## Definition

**Chunking** is the process of splitting a large document into smaller, meaningful pieces called **chunks**.

Example:

```text
Large Document
      │
      ▼
 ┌──────────────┐
 │   Chunk 1    │
 ├──────────────┤
 │   Chunk 2    │
 ├──────────────┤
 │   Chunk 3    │
 ├──────────────┤
 │   Chunk 4    │
 └──────────────┘
```

Each chunk can later be converted into an embedding and stored for retrieval.

---

## Why was it introduced?

Documents can be much larger than the amount of information we need for a particular question.

Sending an entire document to the LLM for every question would:

- Consume unnecessary tokens
- Increase processing cost
- Make retrieval less precise
- Potentially exceed the context window

Chunking allows the system to work with smaller, relevant portions of the document.

---

## Problems It Tries to Solve

### 1. Large Documents

Breaks large documents into manageable pieces.

### 2. Retrieval Precision

Allows the system to retrieve the specific section relevant to the user's question instead of the entire document.

### 3. Context Usage

Only relevant chunks need to be provided to the LLM.

### 4. Embedding

Embeddings are generated for chunks so they can be independently searched.

---

## High-Level Working

```text
Document
    │
    ▼
Chunking Strategy
    │
    ├── Chunk 1
    ├── Chunk 2
    ├── Chunk 3
    └── Chunk 4
         │
         ▼
    Embedding Model
         │
         ▼
    Vector Database
```

Later, when a user asks a question, the system can retrieve only the relevant chunks.

---

## Key Concepts

### Chunk Size

The amount of content contained in one chunk.

### Overlap

A portion of one chunk can be repeated in the next chunk to preserve context between boundaries.

Example:

```text
Chunk 1:
A B C D E

Chunk 2:
        D E F G H
        ↑
      overlap
```

### Chunking Strategy

The way documents are divided.

Possible approaches include:

- Fixed-size chunking
- Sentence-based chunking
- Paragraph-based chunking
- Semantic/document-structure-based chunking

The appropriate strategy depends on the document and application.

---

## Real-World Analogy

Imagine a large textbook.

Instead of giving the entire textbook to someone whenever they ask a question, divide it into:

```text
Textbook
   │
   ├── Chapter 1
   ├── Chapter 2
   ├── Chapter 3
   └── Chapter 4
```

If someone asks about Chapter 3, only the relevant section needs to be retrieved.

Chunking applies the same principle to RAG.

---

## GenAI Engineering Relevance

Chunking is one of the first major decisions when building a RAG system.

It directly affects:

- Retrieval quality
- Embedding quality
- Context size
- Response quality
- Cost

Poor chunking can cause good documents to produce poor RAG results.

---

## Important Points

- Chunking happens during the indexing stage.
- A document can contain many chunks.
- Each chunk can have its own embedding.
- Smaller chunks improve retrieval precision but may lose context.
- Larger chunks preserve more context but may reduce retrieval precision.
- Overlap can help preserve information across chunk boundaries.
- There is no single chunk size that works for every application.

---

## Interview Insight

A common interview discussion is:

> **What happens if chunks are too large or too small?**

**Too large:**

- Less precise retrieval
- More unnecessary context
- Higher token usage

**Too small:**

- Important context may be separated
- Retrieved information may be incomplete
- More chunks may be required to answer one question

Therefore, chunking should be chosen based on the document structure and retrieval requirements.

---

## Key Takeaways

- Chunking divides large documents into meaningful pieces.
- It makes documents easier to embed and retrieve.
- Chunk size directly affects RAG quality.
- Overlap can preserve context between chunks.
- Chunking strategy should depend on the type of data and use case.

# RAG - Notes

## Learning Journey

This phase explains how Retrieval-Augmented Generation (RAG) enables an LLM to use external knowledge to generate more relevant and grounded responses.

---

# 1. Introduction to RAG

## Definition

**Retrieval-Augmented Generation (RAG)** is a technique where relevant information is retrieved from an external knowledge source and provided to an LLM as context before generating a response.

Instead of relying only on the knowledge stored in the model's weights:

```text
User Question
      │
      ▼
Retrieve Relevant Information
      │
      ▼
Provide Context to LLM
      │
      ▼
Generate Answer
```

---

## Why was it introduced?

LLMs have limitations when working with:

- Private organizational data
- Frequently changing information
- Domain-specific documents
- Knowledge that was not available during model training

RAG allows an application to provide this information to the LLM at query time without modifying the model.

---

## Problems It Tries to Solve

### 1. External Knowledge

Allows an LLM to answer using information outside its training data.

### 2. Private Data

Allows applications to use internal documents and knowledge bases.

### 3. Outdated Knowledge

New or updated information can be made available through the knowledge base without retraining the LLM.

### 4. Hallucinations

Providing relevant context can reduce the likelihood of unsupported answers.

RAG reduces hallucinations but does not completely eliminate them.

---

## High-Level Working

RAG consists of two major flows.

### Indexing

Documents are prepared and stored for retrieval.

```text
Documents
    │
    ▼
Chunking
    │
    ▼
Embedding Model
    │
    ▼
Vector Database
```

### Retrieval + Generation

When the user asks a question:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Context Injection
      │
      ▼
LLM
      │
      ▼
Answer
```

---

## Key Concepts

### Retrieval

Finding relevant information from an external knowledge source.

### Augmentation

Adding the retrieved information to the prompt as context.

### Generation

The LLM generates the final response using the question and retrieved context.

```text
Retrieval
    +
Augmentation
    +
Generation
    =
RAG
```

---

## Real-World Analogy

Imagine asking a doctor a question.

Instead of relying only on memory, the doctor:

```text
Question
   │
   ▼
Find Relevant Medical Reference
   │
   ▼
Read Relevant Information
   │
   ▼
Provide Answer
```

RAG follows a similar approach:

**Retrieve → Read Context → Generate Answer**

---

## GenAI Engineering Relevance

RAG is commonly used for:

- Chat with PDFs
- Enterprise knowledge assistants
- Healthcare and pharmacy assistants
- Legal document systems
- Customer support
- Internal company search
- Research assistants

It is one of the core techniques for building applications that connect LLMs with external knowledge.

---

## Important Points

- RAG does not modify the LLM's weights.
- External knowledge is supplied at query time.
- RAG does not require model retraining when documents change.
- Retrieval quality directly affects the final response.
- RAG reduces hallucinations but cannot guarantee factual correctness.
- The LLM generates the answer; the retrieval system provides the context.

---

## Interview Insight

A useful distinction to remember:

> **RAG does not teach the model new knowledge. It gives the model relevant information at inference time.**

---

## Key Takeaways

- RAG connects LLMs with external knowledge.
- It consists of Retrieval, Augmentation, and Generation.
- Documents are prepared before they can be retrieved.
- Retrieved information is provided to the LLM as context.
- RAG is especially useful for private, domain-specific, and frequently changing information.

---

# 2. Chunking

## Definition

**Chunking** is the process of splitting a large document into smaller, meaningful pieces called **chunks**.

Example:

```text
Large Document
      │
      ▼
 ┌──────────────┐
 │   Chunk 1    │
 ├──────────────┤
 │   Chunk 2    │
 ├──────────────┤
 │   Chunk 3    │
 ├──────────────┤
 │   Chunk 4    │
 └──────────────┘
```

Each chunk can later be converted into an embedding and stored for retrieval.

---

## Why was it introduced?

Documents can be much larger than the amount of information we need for a particular question.

Sending an entire document to the LLM for every question would:

- Consume unnecessary tokens
- Increase processing cost
- Make retrieval less precise
- Potentially exceed the context window

Chunking allows the system to work with smaller, relevant portions of the document.

---

## Problems It Tries to Solve

### 1. Large Documents

Breaks large documents into manageable pieces.

### 2. Retrieval Precision

Allows the system to retrieve the specific section relevant to the user's question instead of the entire document.

### 3. Context Usage

Only relevant chunks need to be provided to the LLM.

### 4. Embedding

Embeddings are generated for chunks so they can be independently searched.

---

## High-Level Working

```text
Document
    │
    ▼
Chunking Strategy
    │
    ├── Chunk 1
    ├── Chunk 2
    ├── Chunk 3
    └── Chunk 4
         │
         ▼
    Embedding Model
         │
         ▼
    Vector Database
```

Later, when a user asks a question, the system can retrieve only the relevant chunks.

---

## Key Concepts

### Chunk Size

The amount of content contained in one chunk.

### Overlap

A portion of one chunk can be repeated in the next chunk to preserve context between boundaries.

Example:

```text
Chunk 1:
A B C D E

Chunk 2:
        D E F G H
        ↑
      overlap
```

### Chunking Strategy

The way documents are divided.

Possible approaches include:

- Fixed-size chunking
- Sentence-based chunking
- Paragraph-based chunking
- Semantic/document-structure-based chunking

The appropriate strategy depends on the document and application.

---

## Real-World Analogy

Imagine a large textbook.

Instead of giving the entire textbook to someone whenever they ask a question, divide it into:

```text
Textbook
   │
   ├── Chapter 1
   ├── Chapter 2
   ├── Chapter 3
   └── Chapter 4
```

If someone asks about Chapter 3, only the relevant section needs to be retrieved.

Chunking applies the same principle to RAG.

---

## GenAI Engineering Relevance

Chunking is one of the first major decisions when building a RAG system.

It directly affects:

- Retrieval quality
- Embedding quality
- Context size
- Response quality
- Cost

Poor chunking can cause good documents to produce poor RAG results.

---

## Important Points

- Chunking happens during the indexing stage.
- A document can contain many chunks.
- Each chunk can have its own embedding.
- Smaller chunks improve retrieval precision but may lose context.
- Larger chunks preserve more context but may reduce retrieval precision.
- Overlap can help preserve information across chunk boundaries.
- There is no single chunk size that works for every application.

---

## Interview Insight

A common interview discussion is:

> **What happens if chunks are too large or too small?**

**Too large:**

- Less precise retrieval
- More unnecessary context
- Higher token usage

**Too small:**

- Important context may be separated
- Retrieved information may be incomplete
- More chunks may be required to answer one question

Therefore, chunking should be chosen based on the document structure and retrieval requirements.

---

## Key Takeaways

- Chunking divides large documents into meaningful pieces.
- It makes documents easier to embed and retrieve.
- Chunk size directly affects RAG quality.
- Overlap can preserve context between chunks.
- Chunking strategy should depend on the type of data and use case.

---

# 3. Embedding Models

## Definition

An **Embedding Model** converts text into a numerical vector that represents its semantic meaning.

In RAG, embeddings are used to represent both:

- Document chunks
- User queries

This allows the system to compare their meaning.

---

## Why was it introduced?

Traditional keyword search mainly looks for matching words.

For example:

```text
Query:
"How can I reduce my blood sugar?"

Document:
"Methods for controlling glucose levels..."
```

The words may be different, but the meaning is related.

Embedding models allow RAG systems to perform **semantic search** based on meaning rather than exact word matching.

---

## Problems It Tries to Solve

### 1. Keyword Dependency

Finds semantically related content even when the exact words are different.

### 2. Semantic Search

Allows the system to compare the meaning of a query with document chunks.

### 3. RAG Retrieval

Provides the vector representation required for similarity-based retrieval.

---

## High-Level Working

### During Indexing

```text
Document
    │
    ▼
Chunking
    │
    ▼
Text Chunk
    │
    ▼
Embedding Model
    │
    ▼
Vector
    │
    ▼
Vector Database
```

### During Retrieval

```text
User Question
      │
      ▼
Embedding Model
      │
      ▼
Query Vector
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
```

The same embedding model is typically used to represent both document chunks and queries so their vectors can be compared consistently.

---

## Key Concepts

### Embedding

A numerical representation of the semantic meaning of text.

### Embedding Model

The model responsible for converting text into embeddings.

### Query Embedding

The vector representation of the user's question.

### Document Embedding

The vector representation of a document chunk.

### Vector Dimension

The number of values in an embedding vector.

For example:

```text
Text
  ↓
Embedding Model
  ↓
[0.12, -0.45, 0.78, ...]
  ↑
Vector
```

The exact dimension depends on the embedding model.

---

## Real-World Analogy

Imagine a library where every book is assigned a location based on its subject.

```text
Medicine → Medical Section
Finance  → Finance Section
History  → History Section
```

A question about diabetes would be directed toward the medical section even if the word "diabetes" does not appear in every relevant book.

Embeddings work similarly by placing semantically related content closer together in vector space.

---

## GenAI Engineering Relevance

Embedding models are a core component of RAG because they enable:

- Semantic search
- Document retrieval
- Query matching
- Recommendation systems
- Similarity-based information retrieval

Choosing an appropriate embedding model can significantly affect RAG retrieval quality.

---

## Important Points

- Embeddings represent meaning numerically.
- Both documents and queries can be converted into embeddings.
- Embeddings enable semantic search.
- The embedding model is different from the LLM that generates the final answer.
- Different embedding models can produce different vector dimensions and retrieval quality.
- The embedding model used for indexing should be compatible with the one used for querying.

---

## Interview Insight

A common distinction:

> **The embedding model retrieves relevant information; the LLM uses that information to generate the answer.**

The embedding model does not generate the final natural-language response.

---

## Key Takeaways

- Embedding models convert text into vectors.
- RAG uses embeddings for semantic retrieval.
- Document chunks and user queries are both embedded.
- Similar meanings can produce similar vector representations.
- Embedding quality directly affects retrieval quality.

---

# 4. Vector Databases

## Definition

A **Vector Database** is a database designed to store, index, and efficiently search vector embeddings.

In RAG, it stores embeddings of document chunks along with useful metadata.

```text
Document Chunk
      │
      ▼
Embedding Model
      │
      ▼
Vector + Metadata
      │
      ▼
Vector Database
```

---

## Why was it introduced?

Traditional databases are optimized for structured values such as:

```text
ID
Name
Date
Category
```

RAG needs to search high-dimensional vectors based on similarity.

Vector databases are designed to perform this type of search efficiently.

---

## Problems It Tries to Solve

### 1. Efficient Vector Storage

Stores large numbers of embeddings.

### 2. Semantic Search

Finds vectors that are similar to a query vector.

### 3. Metadata Filtering

Allows retrieval to be restricted using metadata.

For example:

```text
Department = "Cardiology"
Document Type = "Guideline"
Year = 2026
```

### 4. Scalability

Supports efficient retrieval when the knowledge base grows.

---

## High-Level Working

### During Indexing

```text
Document
    │
    ▼
Chunking
    │
    ▼
Embedding Model
    │
    ▼
Vector + Metadata
    │
    ▼
Vector Database
```

### During Retrieval

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Vector Database
      │
      ▼
Similarity Search
      │
      ▼
Top-K Relevant Chunks
```

---

## Key Concepts

### Vector Storage

Stores embeddings representing document chunks.

### Vector Index

A data structure used to make similarity search efficient.

The specific indexing algorithms are implementation details and will be covered separately when we study vector search in more depth.

### Similarity Search

Finds vectors that are most similar to the query vector.

### Metadata

Additional information stored with a vector.

Example:

```text
Vector
+
{
  document: "drug-guidelines.pdf",
  page: 12,
  category: "Pharmacy",
  year: 2026
}
```

### Top-K

The number of most relevant results returned by the search.

For example:

```text
Top-K = 5
```

means the system retrieves the five highest-ranked results.

---

## Real-World Analogy

Imagine a large library.

A normal database is like the library's catalog:

```text
Book ID → Book Name → Author
```

A vector database is more like a smart librarian who can answer:

> "Find books that are most similar in topic to this question."

It can then return the most relevant books or sections.

---

## GenAI Engineering Relevance

Vector databases are widely used in:

- RAG systems
- Semantic search
- Recommendation systems
- Document retrieval
- Enterprise knowledge bases
- AI assistants

Common technologies include:

- ChromaDB
- FAISS
- Qdrant
- Weaviate
- Milvus
- Pinecone

We will use a suitable local vector database during the RAG lab and later evaluate the appropriate choice for the production project.

---

## Important Points

- Vector databases store embeddings and associated metadata.
- They enable efficient similarity search.
- They are not the LLM and do not generate answers.
- Metadata enables filtering and traceability.
- Top-K determines how many results are retrieved.
- Vector databases are especially useful when the knowledge base contains many embeddings.

---

## Interview Insight

A common question is:

> **Why can't we simply store embeddings in a normal database?**

A normal database can store vectors, but vector databases are specifically optimized for efficient similarity search and vector indexing at scale.

The choice depends on the application's scale and requirements.

---

## Key Takeaways

- A vector database stores and searches embeddings.
- It enables semantic retrieval in RAG.
- Metadata can be stored alongside embeddings.
- Similarity search identifies relevant chunks.
- Top-K controls how many results are returned.
- The vector database retrieves information; the LLM generates the final answer.

# 5. Similarity Search

## Definition

**Similarity Search** finds the document chunks whose embeddings are most similar to the embedding of the user's query.

It is the mechanism that allows RAG to identify **relevant information based on meaning**.

---

## Why was it introduced?

After converting text into embeddings, the system needs a way to determine:

> "Which stored chunks are most relevant to this question?"

Similarity search compares the query vector with stored document vectors and ranks them based on similarity.

---

## Problem It Solves

Without similarity search, the system would have embeddings but no efficient way to identify the most relevant information.

It solves:

- Finding semantically relevant chunks
- Ranking retrieved information
- Supporting Top-K retrieval
- Enabling semantic search

---

## High-Level Working

```text
User Question
      │
      ▼
Embedding Model
      │
      ▼
Query Vector
      │
      ▼
Compare with Stored Vectors
      │
      ▼
Calculate Similarity
      │
      ▼
Rank Results
      │
      ▼
Top-K Chunks
```

Example:

```text
Query:
"What are the symptoms of diabetes?"

       │
       ▼

Similarity Search

       │
       ├── Chunk A → High similarity
       ├── Chunk B → Medium similarity
       ├── Chunk C → Low similarity
       └── Chunk D → Low similarity

       │
       ▼

Top-K relevant chunks
```

---

## Key Concepts

### Similarity Score

A numerical value representing how similar two vectors are.

Higher similarity generally means the content is more relevant to the query.

### Cosine Similarity

A commonly used method for measuring similarity between embedding vectors.

The mathematical details are intentionally deferred and will be covered with vector-search implementation concepts later.

### Top-K

Defines how many of the highest-ranked results should be returned.

```text
Top-K = 3
```

means the three most relevant chunks are returned.

### Ranking

Retrieved chunks are ordered based on their similarity scores.

---

## Real-World Analogy

Imagine asking a librarian:

> "Find books related to diabetes management."

The librarian searches the library and ranks the results:

```text
1. Diabetes Management → Very Relevant
2. Blood Sugar Control → Relevant
3. Endocrinology → Somewhat Relevant
4. General Medicine → Less Relevant
```

Similarity search performs a similar ranking using vector representations.

---

## GenAI Engineering Relevance

Similarity search is critical to RAG because:

```text
Better Retrieval
      ↓
Better Context
      ↓
Better LLM Response
```

Poor similarity search can result in irrelevant context being sent to the LLM.

---

## Important Points

- Similarity search operates on embeddings.
- It compares the query embedding with stored document embeddings.
- Results are ranked by similarity.
- Top-K determines how many results are returned.
- Similarity search is a retrieval mechanism, not a generation mechanism.
- Retrieval quality directly affects the quality of the final LLM response.

---

## Interview Insight

### Why convert the query into an embedding?

Because the stored documents are represented as embeddings.

The query must also be represented in the same vector space so the system can compare the query with document chunks based on semantic similarity.

---

## Key Takeaways

- Similarity search finds semantically relevant chunks.
- It compares query and document embeddings.
- Results are ranked according to similarity.
- Top-K controls the number of retrieved chunks.
- It is a core part of the RAG retrieval process.

---

# 6. Retrieval Pipeline

## Definition

The **Retrieval Pipeline** is the sequence of steps used to convert a user's question into relevant information that can be provided to the LLM.

It connects the user's query with the knowledge stored during indexing.

---

## Why was it introduced?

RAG needs more than a vector database.

The system must:

1. Understand the user's query.
2. Convert it into a searchable representation.
3. Find relevant information.
4. Select the useful results.
5. Pass them to the LLM.

The retrieval pipeline coordinates these steps.

---

## High-Level Working

```text
User Question
      │
      ▼
Query Processing
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Metadata Filtering
      │
      ▼
Top-K Results
      │
      ▼
Relevant Context
      │
      ▼
LLM
      │
      ▼
Final Answer
```

---

## Key Concepts

### Query Processing

The user question may be cleaned, transformed, or rewritten before retrieval.

For simple RAG systems, the original question may be used directly.

### Query Embedding

The question is converted into an embedding using the embedding model.

```text
User Question
      ↓
Embedding Model
      ↓
Query Vector
```

### Retrieval

The query vector is used to search the vector database.

### Filtering

Metadata can be used to restrict the search.

Example:

```text
Query:
"What are the dosage guidelines?"

Filters:
Category = "Pharmacy"
Year = 2026
```

### Top-K Selection

Only the highest-ranked results are selected.

### Context Preparation

The retrieved chunks are prepared to be passed to the LLM.

---

## Real-World Analogy

Imagine a pharmacist answering a question using a large reference library.

```text
Question
   │
   ▼
Identify Topic
   │
   ▼
Search Reference Material
   │
   ▼
Filter Relevant Information
   │
   ▼
Select Best References
   │
   ▼
Read Information
   │
   ▼
Answer Question
```

The retrieval pipeline performs the same overall process programmatically.

---

## GenAI Engineering Relevance

The retrieval pipeline is one of the most important areas to understand when building production RAG systems.

It determines what information reaches the LLM.

A simplified principle is:

```text
User Query
    ↓
Good Retrieval
    ↓
Relevant Context
    ↓
Better Answer
```

Even a powerful LLM can produce a poor answer if the retrieval pipeline provides irrelevant or incomplete context.

---

## Important Points

- Retrieval happens before generation.
- The user query is converted into an embedding.
- Similarity search identifies relevant chunks.
- Metadata filtering can improve retrieval precision.
- Top-K controls the number of retrieved results.
- Retrieved chunks become context for the LLM.
- The retrieval pipeline does not generate the final answer.

---

## Interview Insight

### What happens if retrieval returns irrelevant chunks?

The LLM may use incorrect or unrelated information when generating the response.

Therefore, improving RAG quality is not only about choosing a better LLM.

It also requires improving:

- Chunking
- Embedding model
- Similarity search
- Filtering
- Ranking
- Retrieval strategy

---

## Key Takeaways

- The retrieval pipeline connects a user query to relevant knowledge.
- Query embedding converts the question into a searchable vector.
- Similarity search identifies relevant chunks.
- Filtering and Top-K improve result selection.
- Retrieved chunks are eventually passed to the LLM as context.
- Retrieval quality is a major factor in overall RAG quality.

# 7. Context Injection

## Definition

**Context Injection** is the process of adding the relevant information retrieved from the knowledge base to the user's prompt before sending it to the LLM.

The LLM then generates the answer using:

- User question
- Retrieved context
- System instructions

---

## Why was it introduced?

Retrieval alone does not provide an answer.

The retrieved information must be given to the LLM so it can use that information while generating the response.

```text
User Question
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Add Chunks to Prompt
      │
      ▼
LLM
      │
      ▼
Answer
```

---

## Problem It Solves

Context injection solves the problem of connecting **retrieved knowledge** with **LLM generation**.

Without context injection:

```text
User Question
      │
      ▼
LLM
      │
      ▼
Answer based mainly on model knowledge
```

With context injection:

```text
User Question
      │
      ├───────────────┐
      │               │
      ▼               ▼
Retrieved Context   User Question
      │               │
      └───────┬───────┘
              ▼
             LLM
              │
              ▼
            Answer
```

---

## High-Level Working

A simplified prompt may look like:

```text
System Instructions

Context:
[Retrieved Chunk 1]

[Retrieved Chunk 2]

[Retrieved Chunk 3]

Question:
"What are the storage requirements?"

Answer:
```

The LLM uses the retrieved context as additional information when generating the answer.

---

## Key Concepts

### Retrieved Context

The relevant chunks returned by the retrieval pipeline.

### Prompt Construction

Combining the user's question, retrieved context, and system instructions into a prompt.

### Context Relevance

Only useful retrieved information should ideally be included.

Irrelevant context can make the response less accurate.

### Context Size

The amount of information passed to the LLM must fit within its context window.

---

## Real-World Analogy

Imagine asking a pharmacist a question and handing them three relevant pages from a drug reference guide.

```text
Question
   +
Relevant Reference Pages
   ↓
Pharmacist
   ↓
Answer
```

The reference pages are equivalent to the retrieved context provided to the LLM.

---

## GenAI Engineering Relevance

Context injection is where the retrieval and generation parts of RAG are connected.

```text
Retrieval
    ↓
Relevant Context
    ↓
Context Injection
    ↓
LLM
    ↓
Generated Answer
```

The quality and structure of the injected context can significantly affect the final response.

---

## Important Points

- Retrieved information is provided to the LLM as context.
- Context is usually included as part of the prompt.
- The LLM still performs the generation.
- Context does not modify the model's weights.
- Too much irrelevant context can reduce response quality.
- Context must fit within the model's context window.

---

## Interview Insight

### Does context injection train the LLM?

**No.**

The retrieved information is provided only for the current inference request.

It does not modify the model's weights or permanently teach the model the retrieved information.

---

## Key Takeaways

- Context injection connects retrieval with generation.
- Retrieved chunks are added to the prompt.
- The LLM uses the context to generate the answer.
- Context injection happens at inference time.
- The retrieved information does not become permanent model knowledge.


---

# 8. RAG Challenges

## Definition

**RAG Challenges** are the practical problems that can affect the quality, reliability, performance, and cost of a RAG system.

A RAG system can fail even when the underlying LLM is powerful.

---

## Why was this important?

RAG is not simply:

```text
Documents → Vector Database → LLM
```

The quality of the final answer depends on multiple stages.

```text
Document
   ↓
Chunking
   ↓
Embedding
   ↓
Retrieval
   ↓
Context
   ↓
LLM
   ↓
Answer
```

A problem at any stage can affect the final result.

---

## Major Challenges

### 1. Poor Chunking

Incorrect chunk sizes or boundaries can separate information that belongs together.

```text
Too Small
   ↓
Lost Context

Too Large
   ↓
Poor Retrieval Precision
```

---

### 2. Poor Embeddings

An unsuitable embedding model may fail to capture the semantic relationship between queries and documents.

```text
Query
  ↓
Poor Embedding
  ↓
Wrong Retrieval
  ↓
Poor Context
  ↓
Poor Answer
```

---

### 3. Irrelevant Retrieval

The system may retrieve chunks that are related to the query but do not actually contain the required information.

This can cause the LLM to generate an incorrect or incomplete answer.

---

### 4. Missing Information

The required information may not exist in the knowledge base.

In this situation, retrieval cannot provide useful context.

A good RAG system should be able to recognize when the available context is insufficient rather than confidently inventing an answer.

---

### 5. Context Limitations

The retrieved context must fit within the LLM's context window.

Too much retrieved information can:

- Increase token usage
- Increase latency
- Increase cost
- Introduce irrelevant information

---

### 6. Stale Knowledge

The knowledge base may contain outdated documents.

```text
Old Document
     ↓
Stored in Knowledge Base
     ↓
Retrieved by RAG
     ↓
Potentially Outdated Answer
```

The knowledge base therefore needs appropriate update and document lifecycle strategies.

---

### 7. Latency

A RAG request contains additional processing compared with a simple LLM request.

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Context Preparation
   ↓
LLM
   ↓
Answer
```

Each step can add latency.

---

### 8. Cost

RAG can increase cost because:

- Embeddings must be generated.
- Vector storage is required.
- Retrieved context consumes LLM tokens.
- Additional processing may be required.

---

### 9. Security and Access Control

Sensitive documents should not be retrieved for users who do not have permission to access them.

For example:

```text
User A
   ↓
Allowed Documents
   ↓
Retrieval
```

must not accidentally become:

```text
User A
   ↓
All Documents
   ↓
Retrieval
```

Access control should therefore be considered during retrieval, not only after the LLM generates the answer.

---

### 10. Hallucination

RAG can reduce hallucinations by providing relevant context, but it does not completely eliminate them.

The LLM may still:

- Misinterpret retrieved information
- Combine information incorrectly
- Generate unsupported statements

---

## Key Concepts

### Retrieval Quality

How accurately the system finds relevant information.

### Context Quality

How useful and complete the retrieved information is for answering the question.

### Grounding

Constraining the answer to information available in the provided context.

### Freshness

How current the information in the knowledge base is.

### Latency

The time required to retrieve information and generate the response.

### Cost

The resources required for embedding, storage, retrieval, and LLM inference.

---

## Real-World Analogy

Imagine a pharmacist answering a question using a large reference library.

Problems can occur if:

```text
Wrong Book
   ↓
Wrong Page
   ↓
Incomplete Information
   ↓
Incorrect Answer
```

The pharmacist may be highly knowledgeable, but poor reference material can still lead to a poor answer.

RAG has the same dependency on retrieval quality.

---

## GenAI Engineering Relevance

Production RAG systems require optimization across the entire pipeline.

```text
Document Quality
      ↓
Chunking
      ↓
Embedding
      ↓
Retrieval
      ↓
Context
      ↓
LLM
      ↓
Answer Quality
```

Improving only the LLM does not necessarily solve RAG problems.

---

## Important Points

- RAG quality depends on the entire pipeline.
- Poor chunking can cause poor retrieval.
- Poor retrieval can provide irrelevant context.
- Missing knowledge cannot be recovered through retrieval.
- Too much context can increase cost and latency.
- Knowledge bases must be kept current.
- Access control must be applied during retrieval.
- RAG reduces hallucinations but does not eliminate them.

---

## Interview Insight

### If the LLM is very powerful, why can a RAG system still give a bad answer?

Because the LLM can only work with the context it receives.

If the retrieval system provides:

- Wrong information
- Incomplete information
- Irrelevant information
- Outdated information

the final answer can still be poor.

Therefore:

> **RAG quality is heavily dependent on retrieval quality.**

---

## Key Takeaways

- RAG introduces additional engineering challenges beyond the LLM.
- Chunking, embeddings, retrieval, context, and data quality all matter.
- Security and access control are critical for enterprise RAG.
- Latency and cost must be considered in production.
- A powerful LLM cannot compensate for consistently poor retrieval.

# 9. Types of RAG

## Definition

RAG can be implemented in different ways depending on how information is retrieved, processed, and provided to the LLM.

The main approaches range from simple retrieval to more advanced multi-step retrieval systems.

---

## Why was it introduced?

Different applications have different retrieval requirements.

A simple document chatbot may need:

```text
Question
   ↓
Retrieve Chunks
   ↓
LLM
```

A complex enterprise system may require:

- Query transformation
- Multiple retrieval strategies
- Re-ranking
- Metadata filtering
- Multiple retrieval steps

Therefore, RAG can evolve based on application requirements.

---

## Key Concepts

### 1. Naive / Basic RAG

The simplest RAG architecture.

```text
User Query
    ↓
Embedding
    ↓
Vector Search
    ↓
Top-K Chunks
    ↓
LLM
    ↓
Answer
```

It is easy to implement and is useful for understanding the basic RAG workflow.

### 2. Advanced RAG

Improves the basic retrieval pipeline with additional techniques.

Examples include:

- Query transformation
- Metadata filtering
- Re-ranking
- Better chunking
- Hybrid search
- Context optimization

```text
User Query
    ↓
Query Processing
    ↓
Retrieval
    ↓
Re-ranking / Filtering
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer
```

### 3. Hybrid RAG

Combines multiple retrieval methods.

A common combination is:

```text
              User Query
                  │
          ┌───────┴───────┐
          ▼               ▼
     Keyword Search   Vector Search
          │               │
          └───────┬───────┘
                  ▼
             Combine Results
                  │
                  ▼
                Ranking
                  │
                  ▼
                  LLM
```

This can provide better retrieval than relying only on keyword or vector search.

### 4. Agentic / Multi-Step RAG

The system can perform multiple retrieval steps based on the question and intermediate results.

```text
User Query
    ↓
LLM / Agent
    ↓
Decide What to Retrieve
    ↓
Retrieve Information
    ↓
Analyze Results
    ↓
Retrieve More Information
    ↓
Final Context
    ↓
LLM
    ↓
Answer
```

This is useful for complex questions that cannot be answered using a single retrieval operation.

---

## Real-World Analogy

Consider a pharmacy assistant.

### Basic RAG

```text
Question
   ↓
Search Drug Reference
   ↓
Answer
```

### Advanced RAG

```text
Question
   ↓
Identify Drug
   ↓
Filter by Drug Category
   ↓
Search Guidelines
   ↓
Rank Relevant Information
   ↓
Answer
```

### Multi-Step RAG

```text
Question
   ↓
Find Drug
   ↓
Find Interaction Information
   ↓
Check Clinical Guidelines
   ↓
Combine Information
   ↓
Answer
```

---

## GenAI Engineering Relevance

The choice of RAG architecture should depend on:

- Complexity of queries
- Data size
- Retrieval quality requirements
- Latency requirements
- Cost
- Security requirements

A production system should not automatically use the most complex RAG architecture.

Start simple and introduce additional retrieval capabilities when the application requires them.

---

## Important Points

- Basic RAG is the simplest retrieval architecture.
- Advanced RAG adds retrieval and context optimization techniques.
- Hybrid RAG combines multiple search strategies.
- Agentic RAG can perform multiple retrieval steps.
- More complex RAG can improve capabilities but also increases complexity, latency, and cost.
- RAG architecture should be selected based on application requirements.

---

## Interview Insight

### Is advanced RAG always better than basic RAG?

**No.**

Basic RAG may be sufficient for simple document-question answering.

Advanced approaches should be introduced when the application requires better retrieval, complex queries, multiple search strategies, or multi-step retrieval.

---

## Key Takeaways

- RAG is not a single fixed architecture.
- Basic RAG provides the foundation.
- Advanced RAG improves retrieval quality.
- Hybrid RAG combines retrieval strategies.
- Agentic RAG supports multi-step retrieval.
- Production systems should use the simplest architecture that meets their requirements.

---

# 10. Production Best Practices

## Definition

**Production RAG** focuses on making a RAG system reliable, secure, scalable, observable, and maintainable beyond a basic proof of concept.

A production system must consider the complete lifecycle:

```text
Documents
    ↓
Ingestion
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Storage
    ↓
Retrieval
    ↓
Context
    ↓
LLM
    ↓
Answer
```

---

## Why was it introduced?

A basic RAG implementation may work with a few documents, but production systems must handle:

- Large document collections
- Changing documents
- Multiple users
- Access control
- Failures
- Performance
- Monitoring
- Cost

---

## Key Concepts

### 1. Document Quality

Ensure documents are:

- Relevant
- Valid
- Up to date
- Correctly processed

Poor source data results in poor answers.

### 2. Chunking Strategy

Choose chunking based on document structure.

Consider:

- Chunk size
- Chunk overlap
- Document sections
- Tables
- Headings
- Semantic boundaries

Avoid assuming one chunking strategy works for every document.

### 3. Embedding Model

Choose an embedding model based on:

- Retrieval quality
- Domain
- Language requirements
- Vector dimensions
- Performance
- Infrastructure constraints

The same compatible embedding approach should be used during indexing and querying.

### 4. Metadata

Store useful metadata with each chunk.

Example:

```text
Chunk
+
{
  document_id,
  document_name,
  page_number,
  category,
  source,
  created_at
}
```

Metadata helps with:

- Filtering
- Traceability
- Debugging
- Citations
- Access control

### 5. Access Control

Users should retrieve only information they are authorized to access.

```text
User
  ↓
Authorization
  ↓
Filtered Retrieval
  ↓
Allowed Documents
  ↓
LLM
```

Security must be part of the retrieval design.

### 6. Retrieval Quality

Monitor and improve:

- Top-K
- Similarity thresholds
- Filtering
- Hybrid search
- Re-ranking
- Query transformation

The goal is to provide the LLM with the most relevant context possible.

### 7. Context Management

Avoid sending unnecessary information to the LLM.

```text
Retrieved Chunks
      ↓
Filter / Rank
      ↓
Relevant Context
      ↓
LLM
```

This helps control:

- Token usage
- Cost
- Latency
- Context-window usage

### 8. Evaluation

A production RAG system should be evaluated using representative questions.

Measure areas such as:

- Retrieval relevance
- Context relevance
- Answer correctness
- Groundedness
- Latency
- Cost

Evaluation should be repeatable so changes to the RAG pipeline can be compared.

### 9. Observability

Monitor the complete pipeline.

```text
User Query
    ↓
Retrieval
    ↓
Context
    ↓
LLM
    ↓
Answer
```

Useful information to capture includes:

- Request latency
- Retrieval results
- Token usage
- Errors
- Model response
- Retrieval scores

Sensitive information should be handled according to the application's security and privacy requirements.

### 10. Document Lifecycle

Documents change over time.

A production system should support:

```text
New Document
     ↓
Process
     ↓
Embed
     ↓
Store
```

and:

```text
Updated Document
     ↓
Re-process
     ↓
Replace / Update Existing Chunks
```

Outdated information should not remain available unintentionally.

---

## Real-World Analogy

A production pharmacy knowledge assistant is not simply:

```text
PDF → Vector DB → LLM
```

It needs:

```text
Approved Documents
       ↓
Document Processing
       ↓
Secure Storage
       ↓
Access Control
       ↓
High-Quality Retrieval
       ↓
Relevant Context
       ↓
LLM
       ↓
Grounded Response
       ↓
Monitoring & Evaluation
```

---

## GenAI Engineering Relevance

Production RAG requires more than selecting an LLM and vector database.

The engineer must consider the entire system:

```text
Data
 ↓
Retrieval
 ↓
Security
 ↓
Generation
 ↓
Evaluation
 ↓
Observability
 ↓
Maintenance
```

This is where RAG moves from a learning exercise to a production GenAI system.

---

## Important Points

- Production RAG requires reliable source data.
- Chunking and embeddings directly affect retrieval quality.
- Metadata improves filtering, traceability, and security.
- Access control must be applied during retrieval.
- Context should be relevant and controlled.
- RAG systems require evaluation and observability.
- Documents need a lifecycle for updates and removal.
- Cost and latency should be monitored.
- Security and privacy are first-class requirements.

---

## Interview Insight

### What makes a RAG system production-ready?

A production-ready RAG system should have:

```text
Reliable Data
     +
Good Retrieval
     +
Security
     +
Evaluation
     +
Observability
     +
Performance
     +
Maintainability
```

It is not enough for the system to simply return an answer.

---

## Key Takeaways

- Production RAG is an end-to-end engineering system.
- Retrieval quality is as important as LLM quality.
- Security and access control must be designed into retrieval.
- Evaluation is required to measure RAG quality.
- Observability helps diagnose retrieval and generation problems.
- Document updates and lifecycle management are essential.
- Production RAG should balance quality, cost, latency, security, and maintainability.

# 11. Metadata Filtering

## Definition

**Metadata Filtering** is the process of using additional information stored with document chunks to restrict which chunks can be retrieved.

Instead of searching the entire vector database, the system can first apply filters and then perform similarity search.

---

## Why was it introduced?

Semantic similarity alone may not be enough.

For example, a pharmacy knowledge base may contain documents from:

- Different years
- Different departments
- Different drug categories
- Different sources
- Different access levels

A query may be semantically relevant to many documents, but only a subset should be considered.

---

## Problem It Solves

Metadata filtering helps with:

- Improving retrieval precision
- Restricting results to relevant categories
- Enforcing access control
- Filtering outdated information
- Reducing unnecessary search space

---

## High-Level Working

During indexing, metadata is stored along with each chunk:

```text
Document Chunk
      │
      ├── Embedding
      │
      └── Metadata
             │
             ├── Category
             ├── Year
             ├── Source
             ├── Document ID
             └── Access Level
```

During retrieval:

```text
User Query
      │
      ├───────────────┐
      │               │
      ▼               ▼
Query Embedding   Metadata Filters
      │               │
      └───────┬───────┘
              ▼
        Filtered Search
              │
              ▼
        Similarity Search
              │
              ▼
          Top-K Chunks
```

---

## Key Concepts

### Metadata

Additional information associated with a document or chunk.

Example:

```text
{
  "document_id": "drug-guide-2026",
  "category": "pharmacy",
  "year": 2026,
  "source": "official-guideline",
  "access_level": "pharmacist"
}
```

### Metadata Filter

A condition used to restrict which records can participate in retrieval.

Example:

```text
year = 2026
```

or:

```text
category = "pharmacy"
```

### Filtered Retrieval

Retrieval performed only against documents that satisfy the specified metadata conditions.

---

## Real-World Analogy

Imagine a large pharmacy library.

A pharmacist asks:

> "What are the latest guidelines for this drug?"

Instead of searching every book:

```text
All Books
   ↓
Filter:
Year = 2026
Category = Pharmacy
   ↓
Relevant Books
   ↓
Search
```

Metadata filtering works in a similar way.

---

## GenAI Engineering Relevance

Metadata filtering is especially useful in enterprise RAG systems where documents have attributes such as:

- Department
- Tenant
- User
- Region
- Document type
- Date
- Access level
- Source

It can also be an important part of **security-aware retrieval**.

For example:

```text
User
  ↓
User Permissions
  ↓
Metadata Filter
  ↓
Allowed Documents
  ↓
Similarity Search
```

---

## Important Points

- Metadata is stored alongside document chunks.
- Metadata can be used to restrict retrieval.
- Filtering can improve retrieval precision.
- Filtering can reduce the search space.
- Metadata can support access control.
- Metadata filtering and similarity search can be used together.
- Metadata must be designed carefully during document ingestion.

---

## Interview Insight

### Why use metadata filtering if vector search already finds relevant documents?

Because semantic relevance and business relevance are different.

A document can be semantically relevant but still be:

- Outdated
- From the wrong department
- From the wrong tenant
- Unauthorized
- From an incorrect source

Metadata filtering adds these business constraints to retrieval.

---

## Key Takeaways

- Metadata provides additional information about stored chunks.
- Metadata filtering restricts retrieval based on those attributes.
- It improves precision and supports business rules.
- It is important for enterprise and multi-user RAG systems.
- It can be combined with vector similarity search.


---

# 12. Hybrid Search

## Definition

**Hybrid Search** combines multiple search techniques to improve retrieval quality.

A common approach is combining:

- Keyword search
- Semantic/vector search

Instead of depending on only one retrieval method, the system uses both.

---

## Why was it introduced?

Vector search is good at understanding semantic meaning, but it may not always perform well for exact terms.

Keyword search is good at finding exact matches, but it may miss semantically related content.

For example:

```text
Query:
"Drug ABC-123 interactions"
```

An exact product code such as `ABC-123` may be better handled by keyword search, while the concept of "drug interactions" may benefit from semantic search.

Hybrid search combines both strengths.

---

## Problem It Solves

Hybrid search helps address limitations of relying on only one retrieval method.

### Keyword Search

Good for:

- Exact terms
- Product names
- Drug codes
- IDs
- Technical terms
- Names

### Vector Search

Good for:

- Semantic meaning
- Related concepts
- Different wording
- Natural-language questions

Hybrid search combines these capabilities.

---

## High-Level Working

```text
                 User Query
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Keyword Search          Vector Search
          │                     │
          ▼                     ▼
   Keyword Results        Semantic Results
          │                     │
          └──────────┬──────────┘
                     ▼
              Combine Results
                     │
                     ▼
                  Ranking
                     │
                     ▼
                Top-K Chunks
                     │
                     ▼
                    LLM
```

---

## Key Concepts

### Keyword Search

Searches for exact or closely matching terms.

A common approach is **BM25**, which ranks documents based on term relevance.

The underlying ranking mathematics is not required at this stage.

### Vector Search

Uses embeddings to retrieve semantically similar content.

```text
Query
  ↓
Embedding
  ↓
Vector Search
  ↓
Similar Meaning
```

### Hybrid Search

Combines keyword and vector search results.

```text
Keyword Search
       +
Vector Search
       ↓
Combined Retrieval
```

### Result Fusion

Results from multiple retrieval methods need to be combined and ranked.

The exact ranking/fusion techniques can be explored during implementation.

---

## Real-World Analogy

Imagine searching a pharmacy database.

You ask:

> "What are the interactions of drug ABC-123?"

Two searches may happen.

### Keyword Search

Finds:

```text
ABC-123
```

### Vector Search

Finds documents discussing:

```text
Drug interactions
Medication interactions
Drug-drug interactions
```

Combining both gives a stronger retrieval result.

---

## GenAI Engineering Relevance

Hybrid search is useful when the knowledge base contains both:

- Natural-language content
- Exact identifiers or terminology

Examples include:

- Healthcare
- Pharmacy
- Legal documents
- Technical documentation
- Enterprise knowledge bases
- Product catalogs

For our future healthcare/pharmacy production project, hybrid retrieval can be particularly useful because drug names, codes, medical terminology, and natural-language questions may all appear together.

---

## Important Points

- Hybrid search combines multiple retrieval strategies.
- Keyword search is strong for exact terms.
- Vector search is strong for semantic meaning.
- Hybrid search can improve recall and retrieval robustness.
- Results from different search methods need to be combined and ranked.
- Hybrid search adds complexity compared with basic vector search.

---

## Interview Insight

### Why not use only vector search?

Because vector search may not always handle exact identifiers effectively.

For example:

```text
Drug Code: ABC-123
Patient ID: P-98472
Policy ID: POL-2026-001
```

Exact-match retrieval can be important for such values.

Therefore:

> **Vector search provides semantic understanding, while keyword search provides exact matching. Hybrid search combines both.**

---

## Key Takeaways

- Hybrid search combines keyword and vector retrieval.
- Keyword search is useful for exact terms.
- Vector search is useful for semantic similarity.
- Combining both can improve retrieval quality.
- Hybrid search is especially useful for enterprise and domain-specific knowledge bases.
- It introduces additional retrieval and ranking complexity.
