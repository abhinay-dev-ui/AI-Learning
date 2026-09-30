# Advanced RAG — Revision Notes

## Purpose

This document is a **short revision guide** for the advanced RAG concepts covered in the CodeLab. It is meant for quick review later rather than as a full tutorial.

---

# 1. Reranking

## What it solves

Vector search is good at finding **semantically similar candidates**, but the highest similarity score does not always mean the chunk is the best answer to the exact question.

## Example

Question:

```text
How long was the study for Treatment C?
```

Vector retrieval:

```text
0.6285 → Study ID: STUDY-003
0.5281 → The target study duration is 36 months.
```

The second chunk contains the actual answer, even though its vector score is lower.

A reranker evaluates the **query and candidate together** and gives a new relevance score.

```text
Vector Search
    ↓
Candidate Pool
    ↓
Cross-Encoder Reranker
    ↓
Final Top-K
```

## Bi-Encoder vs Cross-Encoder

### Bi-Encoder

Query and document are embedded separately.

```text
Query → Embedding ─┐
                   ├─ Cosine Similarity
Doc   → Embedding ─┘
```

- Fast
- Suitable for large-scale retrieval
- Used for initial vector search

### Cross-Encoder

Query and document are processed together.

```text
Query + Document
      ↓
Cross-Encoder
      ↓
Relevance Score
```

- Slower
- More accurate for relevance
- Used only on a small candidate pool

### Interview summary

> A bi-encoder independently embeds queries and documents for fast retrieval. A cross-encoder evaluates the query and document together and is typically used to rerank a smaller candidate set.

---

# 2. Hybrid Search

## What it solves

Vector search is strong for **meaning**, but keyword search is strong for **exact identifiers, names, codes, and rare terms**.

Hybrid search combines both.

```text
                 Query
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Vector Search      Keyword / BM25
          │                 │
          └────────┬────────┘
                   ▼
              Merge + Dedupe
                   ↓
                Rerank
```

## Example

Query:

```text
What happened in STUDY-003 for Treatment C?
```

Vector search may find semantically related Treatment C content.

Keyword/BM25 search is useful for the exact identifier:

```text
STUDY-003
```

## BM25

BM25 is a keyword ranking algorithm that considers:

- query-term frequency
- term rarity
- document length
- term saturation

### Interview summary

> Hybrid search combines semantic vector search with keyword/BM25 search so the system can handle both natural-language meaning and exact terms effectively.

---

# 3. Query Transformation

## What it solves

The user's wording may not match the terminology used in the indexed documents.

Query transformation rewrites the question into a retrieval-friendly form.

## Example

Original:

```text
How long was the study for Treatment C?
```

Transformed:

```text
study duration treatment c
```

Pipeline:

```text
User Query
    ↓
Query Transformation
    ↓
Retrieval Query
    ↓
Search
```

Use the transformed query for retrieval, but keep the **original user question** for reranking and final generation.

---

# 4. Multi-Query Retrieval

## What it solves

One transformed query may still miss useful evidence because documents may use different wording.

Multi-query retrieval generates several versions of the same intent.

## Example

Original:

```text
How long was the study for Treatment C?
```

Generated retrieval queries:

```text
study duration treatment c
study length treatment c
trial duration treatment c
```

Each query is searched, then all candidates are merged and deduplicated.

```text
Query 1 ─┐
Query 2 ─┼─→ Retrieval → Merge → Rerank
Query 3 ─┘
```

### Key distinction

> Multi-query = same intent, different wording.

---

# 5. Query Decomposition

## What it solves

A user question may contain multiple independent intents.

Instead of searching the compound question as one unit, decompose it into smaller sub-questions.

## Example

Original:

```text
How long was the study for Treatment C and what was the primary success criterion?
```

Decomposed:

```text
1. How long was the study for Treatment C?
2. What was the primary success criterion for Treatment C?
```

Each sub-question can then use multi-query and hybrid retrieval.

```text
Complex Question
      ↓
Decomposition
   ┌──┴──┐
   ↓     ↓
Sub-Q1  Sub-Q2
   ↓     ↓
Retrieval
   └──┬──┘
      ↓
Merge / Rerank
```

### Key distinction

```text
Multi-query     = same intent, multiple phrasings
Decomposition   = multiple intents, separate questions
```

---

# 6. Context Compression

## What it solves

Retrieved chunks can contain relevant information mixed with unrelated text.

Context compression removes noise before sending context to the LLM.

## Example

Original chunk:

```text
Treatment C was evaluated across multiple sites.
The target study duration is 36 months.
Administrative reviews occurred quarterly.
```

Compressed:

```text
The target study duration is 36 months.
```

Pipeline:

```text
Retrieved Chunks
      ↓
Context Compression
      ↓
Focused Context
      ↓
LLM
```

Benefits:

- fewer tokens
- less noise
- lower cost
- better focus

### Important limitation

Compression cannot repair poor chunk boundaries. If a fact was already split badly during chunking, compression can only work with the text it receives.

---

# 7. RAG Evaluation

RAG should be evaluated in two layers:

```text
Retrieval Evaluation
        ↓
Did we retrieve the right evidence?

Generation Evaluation
        ↓
Did the LLM produce the correct grounded answer?
```

---

## Precision@K

> Of the top K retrieved chunks, how many are relevant?

Example:

```text
Top 3:
Relevant
Irrelevant
Irrelevant
```

```text
Precision@3 = 1 / 3 = 0.3333
```

High precision means **less retrieval noise**.

---

## Recall@K

> Of all expected relevant evidence, how much was found in the top K?

Example:

```text
Expected relevant facts = 2
Found in top 3         = 2
```

```text
Recall@3 = 2 / 2 = 1.0
```

High recall means **we did not miss important evidence**.

---

## Reciprocal Rank

Measures how high the first relevant result appears.

```text
Rank 1 → 1 / 1 = 1.0
Rank 2 → 1 / 2 = 0.5
Rank 3 → 1 / 3 = 0.3333
```

---

## MRR — Mean Reciprocal Rank

Average reciprocal rank across multiple evaluation questions.

```text
MRR = average of reciprocal ranks
```

MRR is useful for measuring whether relevant evidence appears **early in the ranking**.

---

## Answer Correctness

Checks whether the generated answer contains the expected facts.

Example:

```text
Expected: 36 months
Answer: The study lasted 36 months.
```

Correctness: ✅

Our CodeLab uses simple deterministic checks for learning, but production evaluation may use semantic evaluation, numeric validation, structured rules, or an LLM judge.

---

## Faithfulness / Groundedness

> Is every claim in the generated answer supported by the retrieved context?

Example:

Context:

```text
Treatment C lasted 36 months.
```

Answer:

```text
Treatment C lasted 36 months and reduced mortality by 20%.
```

Evaluation:

```text
36 months                → grounded
reduced mortality by 20% → unsupported / hallucinated
```

### Key distinction

```text
Correctness
= Did the answer contain the expected fact?

Groundedness
= Is every answer claim supported by the supplied context?
```

---

# 8. Common RAG Failure Modes

## Poor Chunking

Example:

```text
"The primary success criteri"
"mary success criterion is..."
```

Effects:

- fragmented facts
- weaker retrieval
- reranking difficulty
- context compression problems

Possible improvements:

- sentence-aware chunking
- semantic chunking
- better overlap
- structure-aware splitting

---

## Low Recall

Useful evidence exists but is not retrieved.

Possible fixes:

- increase candidate pool
- hybrid search
- multi-query retrieval
- better query transformation
- better embeddings
- better chunking

---

## Low Precision

Relevant evidence is retrieved, but many irrelevant chunks are also returned.

Possible fixes:

- reranking
- better metadata filters
- context compression
- candidate tuning

---

## Reranker Failure

The reranker may still rank the wrong candidate first.

Important rule:

> A reranker cannot recover a chunk that initial retrieval never found.

---

## Bad Query Transformation

A rewrite can accidentally change the user's intent.

Example:

```text
Original: How long was Treatment C?
Bad rewrite: Treatment C success
```

Production systems often keep the original query, generate multiple variants, and provide fallback behavior.

---

## Multi-Query Explosion

Too many generated queries increase:

- latency
- cost
- duplicate candidates
- noise

Limit query count in production.

---

## Context Overload

More context is not always better.

Too many chunks can cause:

- higher token cost
- higher latency
- conflicting facts
- distraction
- lost-in-the-middle behavior

Use reranking, deduplication, compression, and sensible Top-K values.

---

## Hallucination

The LLM may add unsupported information even when retrieval works correctly.

Use:

- strong grounding prompts
- evidence checks
- citations
- faithfulness evaluation
- insufficient-evidence fallback

---

## Authorization Failure

This is a security problem, not just a retrieval-quality problem.

Wrong:

```text
Search all data
    ↓
Retrieve unauthorized chunk
    ↓
Filter later
```

Correct:

```text
Authentication
    ↓
Authorization
    ↓
Allowed scope
    ↓
Retrieval only inside allowed data
```

Unauthorized data should never reach the LLM context.

---

## Stale Data

Old embeddings or documents can cause outdated answers.

Production concerns:

- versioning
- re-indexing
- timestamps
- freshness metadata
- update/delete pipelines

---

## Duplicate Chunks

Chunk overlap can produce near-duplicates.

```text
Chunk A
Chunk A'
Chunk A''
```

Possible fixes:

- deduplication
- diversity ranking
- document grouping
- MMR-style approaches

---

## Empty Retrieval

If no sufficient evidence is found, the system should not guess.

Preferred behavior:

```text
Insufficient evidence is available in the retrieved context.
```

---

# 9. RAG Debugging Flow

When an answer is wrong:

```text
Wrong Answer
    ↓
Was correct evidence retrieved?
    │
    ├── NO
    │    ↓
    │ Retrieval problem
    │
    │ Check:
    │ - chunking
    │ - embeddings
    │ - metadata filters
    │ - query rewriting
    │ - hybrid search
    │ - candidate_k
    │
    └── YES
         ↓
      Generation problem

      Check:
      - context compression
      - context ordering
      - prompt
      - LLM behavior
      - groundedness
```

This is one of the most useful production debugging patterns.

---

# 10. Production RAG Architecture

## Offline / Ingestion Pipeline

```text
Documents
    ↓
Validation / OCR
    ↓
Parsing
    ↓
Chunking
    ↓
Metadata Enrichment
    ↓
Embeddings
    ↓
Vector Database
    ↓
Keyword / BM25 Index
```

## Online / Query Pipeline

```text
User
 ↓
Authentication
 ↓
Authorization
 ↓
Allowed Data Scope
 ↓
Query Transformation / Decomposition
 ↓
Multi-Query Generation
 ↓
┌─────────────────────────┐
│ Vector Search           │
│ Keyword / BM25 Search   │
└─────────────────────────┘
 ↓
Merge + Dedupe
 ↓
Cross-Encoder Reranking
 ↓
Context Compression
 ↓
Context Builder
 ↓
Prompt Builder
 ↓
LLM
 ↓
Grounded Answer + Sources
```

---

# 11. Production Principle: Do Not Use Every Technique Blindly

Not every query needs the full advanced pipeline.

Simple query:

```text
Vector Search
    ↓
Rerank
    ↓
Answer
```

Complex query:

```text
Decomposition
    ↓
Multi-Query
    ↓
Hybrid Retrieval
    ↓
Rerank
    ↓
Compression
    ↓
Answer
```

The goal is not to use every advanced technique.

> Use the minimum retrieval pipeline necessary to achieve acceptable quality, security, latency, and cost.

---

# 12. Final Advanced RAG Cheat Sheet

```text
Authorization
    ↓
Query Understanding
    ├─ Transformation
    ├─ Multi-Query
    └─ Decomposition
    ↓
Hybrid Retrieval
    ├─ Vector Search
    └─ Keyword / BM25
    ↓
Merge + Dedupe
    ↓
Cross-Encoder Reranking
    ↓
Context Compression
    ↓
Context + Prompt
    ↓
LLM
    ↓
Grounded Answer
    ↓
Evaluation
    ├─ Precision@K
    ├─ Recall@K
    ├─ MRR
    ├─ Correctness
    └─ Faithfulness
```

---

# 13. Quick Interview Questions

### Why is reranking required after vector search?

Vector similarity finds semantically related candidates, but the highest similarity score may not be the chunk that best answers the exact query. A reranker re-evaluates the candidate pool for query-specific relevance.

### Why use hybrid search?

Vector search handles semantic meaning well, while keyword/BM25 search handles exact identifiers, names, codes, and rare terms. Hybrid search combines both strengths.

### Multi-query vs decomposition?

Multi-query generates different phrasings of the same intent. Decomposition splits a complex multi-intent question into smaller independent questions.

### Why compress context?

To remove irrelevant text before sending retrieved context to the LLM, reducing noise, tokens, latency, and cost.

### Precision vs Recall?

Precision measures how much of what we retrieved was relevant. Recall measures how much of the relevant evidence we successfully retrieved.

### What is MRR?

Mean Reciprocal Rank measures how early the first relevant result appears across a set of queries.

### What is groundedness?

Groundedness measures whether the answer's claims are supported by the retrieved context rather than invented by the LLM.

### Where should authorization happen in RAG?

Before retrieval. The retriever should search only the user's authorized data scope so unauthorized content never reaches the LLM.

---

# Revision Checkpoint

Advanced RAG topics covered:

```text
Reranking                     ✅
Bi-Encoder vs Cross-Encoder   ✅
Hybrid Search                 ✅
BM25 Concept                  ✅
Query Transformation          ✅
Multi-Query Retrieval         ✅
Query Decomposition           ✅
Context Compression           ✅
Precision@K                   ✅
Recall@K                      ✅
Reciprocal Rank / MRR         ✅
Answer Correctness            ✅
Faithfulness / Groundedness   ✅
Failure Modes                 ✅
Production RAG Architecture   ✅
```
