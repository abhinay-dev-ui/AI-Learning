# RAG Interview Questions

## Basic

### Q1. What is RAG?

**Answer:**  
RAG (Retrieval-Augmented Generation) is a technique where relevant information is retrieved from an external knowledge source and provided to an LLM as context before generating the answer.

---

### Q2. Why do we need RAG?

**Answer:**  
RAG allows an LLM to use external, current, or domain-specific information without modifying the model's weights. It is useful when the required knowledge is not available in the model or needs to be updated frequently.

---

### Q3. What are the main components of a RAG system?

**Answer:**  
A typical RAG system contains:

- Document ingestion
- Chunking
- Embedding model
- Vector database
- Retrieval
- Context preparation
- LLM

---

### Q4. What is document ingestion in RAG?

**Answer:**  
Document ingestion is the process of loading source documents, extracting their content, processing them, and preparing them for storage and retrieval.

---

### Q5. Why do we split documents into chunks?

**Answer:**  
Large documents are divided into smaller chunks so that relevant portions can be retrieved independently and passed to the LLM as focused context.

---

### Q6. What happens if chunks are too small?

**Answer:**  
Important context may be separated across multiple chunks, causing retrieval to return incomplete information.

---

### Q7. What happens if chunks are too large?

**Answer:**  
Large chunks may contain too much unrelated information, reducing retrieval precision and increasing token usage.

---

### Q8. What is an embedding in RAG?

**Answer:**  
An embedding is a numerical vector representation of text that captures its semantic meaning. Embeddings allow text to be compared based on meaning rather than only exact words.

---

### Q9. Why are embeddings required in RAG?

**Answer:**  
Embeddings allow the system to represent both documents and user queries in the same vector space so that semantically relevant information can be retrieved.

---

### Q10. What is a vector database?

**Answer:**  
A vector database stores embeddings and provides efficient operations for finding vectors that are similar to a query vector.

---

### Q11. What is similarity search?

**Answer:**  
Similarity search compares the query embedding with stored document embeddings and returns the most relevant results based on their similarity.

---

### Q12. What is Top-K retrieval?

**Answer:**  
Top-K specifies how many of the highest-ranked results should be returned from the retrieval process.

For example:

```text
Top-K = 5
```

means the five highest-ranked results are selected.

---

### Q13. What is metadata in RAG?

**Answer:**  
Metadata is additional information stored with a document or chunk, such as:

- Document ID
- Source
- Category
- Page number
- Date
- Access level

---

### Q14. Why is metadata filtering useful?

**Answer:**  
Metadata filtering restricts retrieval based on business or application requirements.

For example:

```text
category = "pharmacy"
year = 2026
```

This prevents the system from searching irrelevant or unauthorized documents.

---

### Q15. What is context injection?

**Answer:**  
Context injection is the process of adding retrieved information to the prompt before sending the request to the LLM.

```text
User Question
      +
Retrieved Context
      ↓
     LLM
      ↓
    Answer
```

---

### Q16. Does RAG modify the LLM's weights?

**Answer:**  
No.

RAG provides additional information during inference. It does not permanently modify the model's weights or train the model.

---

### Q17. What is the difference between RAG and fine-tuning?

**Answer:**  

**RAG:**

- Retrieves external information at inference time.
- Does not modify model weights.
- Useful for changing or domain-specific knowledge.

**Fine-tuning:**

- Trains the model further on additional data.
- Modifies model weights.
- Useful for changing behavior, style, or specialized capabilities.

---

### Q18. What is hybrid search?

**Answer:**  
Hybrid search combines multiple retrieval strategies, commonly keyword search and vector search.

```text
             Query
               ↓
       ┌───────┴───────┐
       ↓               ↓
Keyword Search    Vector Search
       ↓               ↓
       └───────┬───────┘
               ↓
        Combined Results
```

It combines the strengths of exact matching and semantic search.

---

### Q19. Why can a RAG system still hallucinate?

**Answer:**  
RAG reduces hallucination by providing relevant context, but it does not guarantee that the LLM will always use that information correctly.

The model may still:

- Misinterpret the context
- Combine information incorrectly
- Generate unsupported information

---

### Q20. What makes a RAG system production-ready?

**Answer:**  
A production-ready RAG system should consider:

- Reliable source data
- Good chunking
- Appropriate embeddings
- High-quality retrieval
- Metadata and access control
- Context management
- Evaluation
- Observability
- Security
- Cost and latency
- Document lifecycle management

## Intermediate

### Q21. What is the difference between keyword search and vector search?

**Answer:**

**Keyword search** looks for matching words or terms.

**Vector search** looks for semantic similarity between embeddings.

```text
Keyword Search → Exact / lexical matching
Vector Search  → Meaning / semantic matching
```

---

### Q22. Why would you use hybrid search instead of only vector search?

**Answer:**

Vector search is good at semantic meaning, while keyword search is better for exact terms such as:

- Drug names
- Product codes
- IDs
- Technical terms

Hybrid search combines both approaches to improve retrieval quality.

---

### Q23. What is re-ranking in RAG?

**Answer:**

Re-ranking is the process of taking initially retrieved results and ordering them again using a more sophisticated relevance model.

```text
Query
  ↓
Initial Retrieval
  ↓
Candidate Results
  ↓
Re-ranker
  ↓
Better Ranked Results
  ↓
LLM
```

It helps ensure that the most relevant chunks are placed first.

---

### Q24. Why is re-ranking useful if vector search already ranks results?

**Answer:**

Initial vector retrieval is optimized for efficiently finding candidate results.

A re-ranker can perform a more detailed relevance comparison between the query and retrieved chunks.

This can improve the quality of the final context provided to the LLM.

---

### Q25. What is query transformation in RAG?

**Answer:**

Query transformation modifies or expands the user's original query before retrieval to improve the chances of finding relevant information.

For example:

```text
Original Query
      ↓
Query Transformation
      ↓
Improved Search Query
      ↓
Retrieval
```

---

### Q26. Why might query rewriting be required?

**Answer:**

Users may ask vague, incomplete, or conversational questions.

For example:

```text
User:
"What about its side effects?"
```

The system may need the previous conversation context to understand what "its" refers to before performing retrieval.

Query rewriting can transform it into a more complete search query.

---

### Q27. What is the difference between retrieval and generation in RAG?

**Answer:**

**Retrieval** finds relevant information from the external knowledge source.

**Generation** uses the retrieved information and the user's question to produce the final answer.

```text
Retrieval → Find relevant information
Generation → Produce the answer
```

---

### Q28. Does the vector database generate the final answer?

**Answer:**

No.

The vector database retrieves relevant information.

The LLM is responsible for generating the final natural-language response.

```text
Vector Database → Retrieval
LLM             → Generation
```

---

### Q29. What happens if the required information is not present in the knowledge base?

**Answer:**

The retrieval system cannot retrieve information that does not exist in the knowledge base.

A properly designed RAG system should be able to recognize insufficient context and avoid confidently inventing an answer.

---

### Q30. How does RAG help reduce hallucinations?

**Answer:**

RAG provides relevant external information to the LLM as context.

This gives the model a reliable knowledge source to use while generating the answer.

However, RAG does **not completely eliminate hallucinations**.

---

### Q31. What is grounding in RAG?

**Answer:**

Grounding means generating an answer based on the information provided in the retrieved context rather than unsupported model knowledge.

```text
Retrieved Evidence
       ↓
      LLM
       ↓
Grounded Answer
```

---

### Q32. What is the relationship between chunking and retrieval quality?

**Answer:**

Chunking directly affects what the retrieval system can find.

```text
Poor Chunking
     ↓
Poor Retrieval
     ↓
Poor Context
     ↓
Poor Answer
```

Good chunk boundaries help preserve meaningful information and improve retrieval precision.

---

### Q33. How do you choose the right chunk size?

**Answer:**

There is no universal chunk size.

It depends on:

- Document structure
- Content type
- Query patterns
- Embedding model
- Context window
- Retrieval requirements

The strategy should be evaluated using representative data and queries.

---

### Q34. What is chunk overlap and why is it used?

**Answer:**

Chunk overlap means repeating a small portion of content between consecutive chunks.

```text
Chunk 1:
A B C D E

Chunk 2:
        D E F G H
        ↑
      overlap
```

It helps preserve context when important information spans a chunk boundary.

---

### Q35. What is the difference between document-level and chunk-level retrieval?

**Answer:**

**Document-level retrieval** identifies relevant documents.

**Chunk-level retrieval** identifies specific sections or portions within those documents.

Chunk-level retrieval generally provides more focused context to the LLM.

---

### Q36. Why is metadata important in enterprise RAG?

**Answer:**

Metadata allows the system to apply business rules to retrieval.

It can support:

- Access control
- Tenant isolation
- Department filtering
- Document type filtering
- Date filtering
- Source filtering

For example:

```text
User
 ↓
Permissions
 ↓
Metadata Filter
 ↓
Allowed Chunks
 ↓
Retrieval
```

---

### Q37. How can RAG support access control?

**Answer:**

Access permissions can be represented through metadata and applied during retrieval.

```text
User
  ↓
Authorization
  ↓
Metadata Filter
  ↓
Allowed Documents
  ↓
Retrieval
  ↓
LLM
```

The system should prevent unauthorized documents from entering the LLM context.

---

### Q38. What is the difference between similarity search and metadata filtering?

**Answer:**

**Similarity search** determines which content is semantically relevant.

**Metadata filtering** determines which content is allowed or applicable based on predefined attributes.

They can work together:

```text
Metadata Filter
      ↓
Eligible Documents
      ↓
Similarity Search
      ↓
Relevant Documents
```

---

### Q39. What factors affect RAG latency?

**Answer:**

RAG latency can be affected by:

- Query processing
- Embedding generation
- Vector search
- Metadata filtering
- Re-ranking
- Context preparation
- LLM inference
- Network calls

Adding more retrieval stages can improve quality but may increase latency.

---

### Q40. How can you reduce RAG cost?

**Answer:**

Cost can be controlled by:

- Retrieving only relevant chunks
- Controlling Top-K
- Avoiding unnecessary context
- Using appropriate embedding models
- Controlling prompt size
- Choosing suitable LLMs
- Caching where appropriate
- Monitoring token usage

The goal is to balance **quality, latency, and cost**.

## Scenario Based

### Q41. A RAG system retrieves irrelevant chunks even though the user query is clear. How would you troubleshoot it?

**Answer:**

Check the retrieval pipeline step by step:

1. Verify the document content.
2. Review the chunking strategy.
3. Check the embedding model.
4. Inspect similarity scores.
5. Review Top-K.
6. Check metadata filters.
7. Consider hybrid search.
8. Add re-ranking if required.

```text
Data
 ↓
Chunking
 ↓
Embeddings
 ↓
Retrieval
 ↓
Ranking
```

The goal is to identify which stage is causing the irrelevant retrieval.

---

### Q42. A RAG system retrieves the correct document but the LLM still gives an incorrect answer. What could be wrong?

**Answer:**

Possible causes include:

- Retrieved chunk does not contain enough information.
- Too much irrelevant context was included.
- Context was poorly structured.
- The LLM misunderstood the retrieved information.
- The answer is not grounded in the retrieved context.

Check the complete flow:

```text
Correct Document
      ↓
Correct Chunk?
      ↓
Useful Context?
      ↓
Correct Prompt?
      ↓
LLM
      ↓
Answer
```

---

### Q43. Your RAG system works well with 100 documents but performs poorly with 1 million documents. What would you investigate?

**Answer:**

Investigate:

- Vector database scalability
- Indexing strategy
- Metadata filtering
- Retrieval latency
- Chunk count
- Embedding storage
- Top-K configuration
- Query performance
- Partitioning or sharding if required

The architecture must scale with the size of the knowledge base.

---

### Q44. Users complain that the RAG application is slow. How would you identify the bottleneck?

**Answer:**

Measure latency at each stage:

```text
Query
 ↓
Embedding ──────── 100 ms
 ↓
Retrieval ──────── 200 ms
 ↓
Re-ranking ─────── 300 ms
 ↓
LLM ────────────── 2 sec
```

This allows the team to identify the slowest component instead of optimizing the entire system blindly.

---

### Q45. Your healthcare RAG system retrieves documents from the wrong department. How would you prevent this?

**Answer:**

Use metadata-based access control and filtering.

For example:

```text
User
 ↓
Department = Pharmacy
 ↓
Metadata Filter
 ↓
Pharmacy Documents Only
 ↓
Similarity Search
 ↓
LLM
```

Authorization should be applied before unauthorized information reaches the LLM context.

---

### Q46. A document is updated, but the RAG system continues returning the old information. What could be the problem?

**Answer:**

The knowledge base may contain stale chunks.

The updated document needs to go through the ingestion pipeline again:

```text
Updated Document
      ↓
Re-process
      ↓
Re-chunk
      ↓
Re-embed
      ↓
Update Vector Store
      ↓
Retrieve Latest Information
```

The document lifecycle must support updates and removal of outdated content.

---

### Q47. A user asks a question using terminology different from the documents. Keyword search fails. What would you consider?

**Answer:**

Use semantic/vector search because it can identify conceptually related content even when the exact words differ.

If exact terms are also important, use hybrid search:

```text
User Query
     │
 ┌───┴────┐
 ↓        ↓
Keyword  Vector
Search   Search
 ↓        ↓
 └───┬────┘
     ↓
Combined Results
```

---

### Q48. Your RAG system retrieves 20 chunks, but only 3 are actually useful. What would you improve?

**Answer:**

Consider:

- Reducing Top-K
- Improving chunking
- Improving embeddings
- Applying metadata filters
- Adding re-ranking
- Filtering low-similarity results
- Improving query transformation

The objective is not to retrieve the maximum number of chunks, but to provide the LLM with the **most useful context**.

---

### Q49. How would you design a secure multi-user RAG system?

**Answer:**

A high-level design would be:

```text
User
 ↓
Authentication
 ↓
Authorization
 ↓
User / Tenant Permissions
 ↓
Metadata Filtering
 ↓
Retrieval
 ↓
Relevant Authorized Context
 ↓
LLM
 ↓
Response
```

The system should ensure that unauthorized documents never enter the retrieved context.

---

### Q50. How would you design a production RAG system for a pharmacy knowledge assistant?

**Answer:**

A high-level architecture could be:

```text
                    Documents
                        ↓
               Document Ingestion
                        ↓
                   Chunking
                        ↓
                   Embeddings
                        ↓
                Vector Database
                        │
                        │
User ──→ Authentication ──→ Authorization
                        ↓
                   User Query
                        ↓
              Query Transformation
                        ↓
             Metadata / ACL Filter
                        ↓
              Hybrid / Vector Search
                        ↓
                    Re-ranking
                        ↓
                Relevant Context
                        ↓
                       LLM
                        ↓
              Grounded Response
                        ↓
             Monitoring / Evaluation
```

Key production considerations:

- Approved and trusted sources
- Good document processing
- Appropriate chunking
- Reliable embeddings
- Secure retrieval
- Metadata and access control
- Hybrid search where appropriate
- Re-ranking when needed
- Context management
- Evaluation
- Observability
- Cost and latency monitoring
- Document update lifecycle

The architecture should start simple and evolve as the application's requirements grow.
