# RAG (Retrieval-Augmented Generation) - Quick Reference

A quick revision guide for Retrieval-Augmented Generation (RAG).

---

# 1. Retrieval-Augmented Generation (RAG)

### Definition

Retrieves relevant information from external knowledge before generating a response.

### Why?

Allows LLMs to answer using up-to-date and private data without retraining.

### Use Cases

- PDF Chatbots
- Enterprise Search
- Healthcare Assistants
- Legal AI
- Customer Support

### Key Points

- No model retraining
- Uses external knowledge
- Reduces hallucinations
- Improves factual accuracy

---

# 2. Chunking

### Definition

Splitting large documents into smaller meaningful pieces.

### Why?

LLMs cannot process very large documents efficiently.

### Key Points

- Improves retrieval
- Better semantic search
- Avoids context overflow

---

# 3. Embedding Models

### Definition

Convert document chunks into vector embeddings representing semantic meaning.

### Why?

Semantic search compares meaning instead of exact words.

### Key Points

- Chunk → Vector
- Query → Vector
- Similar meaning → Similar vectors

---

# 4. Vector Database

### Definition

A database optimized for storing and searching vector embeddings.

### Why?

Enables fast semantic retrieval from large document collections.

### Common Options

- ChromaDB
- FAISS
- Pinecone
- Weaviate
- Milvus
- Qdrant

---

# 5. Similarity Search

### Definition

Finds document chunks whose embeddings are closest to the query embedding.

### Why?

Retrieves relevant information based on meaning.

### Key Points

- Semantic search
- Returns Top-K results
- Works on vectors

---

# 6. Retrieval Pipeline

### Definition

The complete process of retrieving relevant information before sending it to the LLM.

### Two Phases

**Indexing**

Documents → Chunking → Embeddings → Vector Database

**Retrieval**

Question → Embedding → Similarity Search → Top-K Chunks

---

# 7. Context Injection

### Definition

Adding retrieved chunks to the user's prompt before sending it to the LLM.

### Why?

Provides external knowledge for answer generation.

### Also Known As

- Prompt Augmentation

---

# 8. RAG Challenges

### Common Challenges

- Poor chunking
- Poor embeddings
- Incorrect retrieval
- Context window limitations
- Hallucinations
- Outdated knowledge
- Conflicting documents

---

# 9. Types of RAG

### Naive RAG

Basic retrieval pipeline.

### Advanced RAG

Improved retrieval using filtering, query optimization, and re-ranking.

### Modular RAG

Independent retrieval components.

### Agentic RAG

AI Agents control retrieval and reasoning.

---

# 10. Production Best Practices

### Best Practices

- Choose appropriate chunk size
- Select suitable embedding model
- Store metadata
- Retrieve relevant chunks only
- Keep knowledge updated
- Write clear prompts
- Return source citations
- Monitor and improve

---

# End-to-End RAG Pipeline

Documents
↓
Chunking
↓
Embedding Model
↓
Vector Database

═══════════════════════════

User Question
↓
Embedding Model
↓
Similarity Search
↓
Top-K Chunks
↓
Context Injection
↓
LLM
↓
Answer + Sources

---

# One-Liners Revision

• RAG combines retrieval with LLM generation.
• Chunking divides documents into meaningful sections.
• Embedding Models convert text into semantic vectors.
• Vector Databases store and search embeddings efficiently.
• Similarity Search retrieves information based on meaning.
• Retrieval consists of Indexing and Query-time Retrieval.
• Context Injection augments the prompt with retrieved information.
• RAG reduces hallucinations but cannot eliminate them.
• Naive RAG is ideal for learning; Modular RAG is common in production.
• Better retrieval generally produces better answers.
• Metadata improves filtering and traceability.
• Source citations increase user trust.
• Production RAG focuses on reliability, scalability, and maintainability.