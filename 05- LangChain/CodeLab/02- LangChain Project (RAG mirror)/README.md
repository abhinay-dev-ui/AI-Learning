# LangChain RAG CodeLab

## Overview

This CodeLab builds a complete Retrieval-Augmented Generation (RAG) pipeline using LangChain while preserving the same architectural concepts previously implemented manually.

The goal of this CodeLab is not simply to "use LangChain."

The goal is to understand:

- What LangChain abstracts
- What LangChain does not abstract
- How LangChain components map to a manually implemented RAG system
- How data flows through each stage
- How metadata filtering works
- How semantic retrieval works
- How reranking improves relevance
- How LCEL and Runnables compose application logic
- How structured output differs from free-form output
- How to evaluate retrieval and generation independently
- What would still be required for a production-grade system

The final pipeline answers questions about internal research studies using:

- Local text documents
- Metadata-aware retrieval
- Context-enriched embeddings
- Hugging Face embeddings
- In-memory vector search
- Cross-encoder reranking
- Ollama + Mistral
- LCEL
- Structured output
- Automated evaluation

---

# Learning Objective

Before this CodeLab, the same RAG concepts were implemented manually.

That manual implementation helped us understand:

```text
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Storage
   ↓
Retrieval
   ↓
Metadata Filtering
   ↓
Reranking
   ↓
Prompt Construction
   ↓
LLM
   ↓
Answer
```

This CodeLab rebuilds the same architecture using LangChain abstractions.

The important principle is:

> LangChain does not replace RAG engineering decisions.  
> It provides reusable abstractions and orchestration around them.

---

# Final Architecture

```text
                        USER QUESTION
                              │
                              ▼
                    Known Metadata Scope
                              │
                              ▼
                     RetrieverService
                              │
                     Metadata Filtering
                              │
                              ▼
                  Vector Similarity Search
                              │
                              ▼
                       Candidate-K
                              │
                              ▼
                   CrossEncoderReranker
                              │
                              ▼
                        Final Top-K
                              │
                              ▼
               StructuredContextFormatter
                              │
                              ▼
                    Runnable / LCEL
                              │
                              ▼
                    ChatPromptTemplate
                              │
                              ▼
                    ChatOllama / Mistral
                              │
                              ▼
                Structured StudyAnswer
                              │
                              ▼
                    EvaluationService
```

Indexing happens separately:

```text
study1.txt
study2.txt
study3.txt
      │
      ▼
DocumentLoader
      │
      ▼
LangChain Documents
      │
      ▼
RecursiveCharacterTextSplitter
      │
      ▼
Chunks
      │
      ▼
SearchContextEnricher
      │
      ▼
HuggingFaceEmbeddings
      │
      ▼
384-dimensional vectors
      │
      ▼
InMemoryVectorStore
```

---

# Dataset

The CodeLab uses three small research study documents.

```text
study1.txt
study2.txt
study3.txt
```

Each study contains:

- Study ID
- Treatment
- Study description
- Study duration
- Primary success criterion

Example:

```text
Study ID: STUDY-003

The study evaluates the effectiveness of Treatment C
for improving patient recovery time.

The target study duration is 36 months.

The primary success criterion is an improvement
in recovery time of at least 30 percent.
```

Important expected facts:

```text
Treatment C
Study ID: STUDY-003
Duration: 36 months
Primary success criterion: 30 percent improvement
```

---

# Project Structure

```text
01-LangChain-RAG/
│
├── main.py
├── requirements.txt
├── .env.example
│
├── data/
│   └── documents/
│       ├── study1.txt
│       ├── study2.txt
│       └── study3.txt
│
└── app/
    │
    ├── __init__.py
    ├── config.py
    │
    ├── ingestion/
    │   ├── __init__.py
    │   ├── loader.py
    │   ├── splitter.py
    │   └── context_enricher.py
    │
    ├── embeddings/
    │   ├── __init__.py
    │   └── embedding_service.py
    │
    ├── retrieval/
    │   ├── __init__.py
    │   ├── vector_store.py
    │   ├── retriever.py
    │   └── reranker.py
    │
    ├── generation/
    │   ├── __init__.py
    │   ├── formatter.py
    │   ├── structured_formatter.py
    │   ├── prompt.py
    │   ├── structured_prompt.py
    │   ├── model.py
    │   └── output_parser.py
    │
    ├── chains/
    │   ├── __init__.py
    │   ├── rag_chain.py
    │   └── structured_rag_chain.py
    │
    ├── evaluation/
    │   ├── __init__.py
    │   ├── cases.py
    │   └── evaluator.py
    │
    └── models/
        ├── __init__.py
        ├── study_answer.py
        ├── evaluation_case.py
        └── evaluation_result.py
```

---

# Dependencies

```text
langchain-core
langchain-text-splitters
langchain-huggingface
langchain-community
langchain-classic
langchain-ollama
sentence-transformers
python-dotenv
pydantic
```

The CodeLab uses local Ollama with:

```text
mistral
```

Verify the model is installed:

```powershell
ollama list
```

---

# Configuration

Example configuration:

```python
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

RERANKER_MODEL = "BAAI/bge-reranker-base"

LLM_MODEL = "mistral"

LLM_TEMPERATURE = 0

CANDIDATE_K = 4

TOP_K = 3
```

Three different models have three different responsibilities:

```text
all-MiniLM-L6-v2
→ semantic embeddings

BAAI/bge-reranker-base
→ query-document relevance reranking

Mistral
→ answer generation
```

---

# Milestone 1 — Document Loading and Chunking

## Goal

Load source files into LangChain `Document` objects and split them into smaller chunks.

Flow:

```text
TXT File
   ↓
DocumentLoader
   ↓
Document
   ↓
RecursiveCharacterTextSplitter
   ↓
Document Chunks
```

---

## LangChain Document

A LangChain `Document` contains:

```python
Document(
    page_content="...",
    metadata={
        ...
    }
)
```

The two important pieces are:

```text
page_content
→ text being processed

metadata
→ information describing the content
```

Example:

```python
Document(
    page_content="The target study duration is 36 months.",
    metadata={
        "source": "study3.txt",
        "study_id": "STUDY-003",
        "treatment": "Treatment C",
        "chunk_index": 2,
    }
)
```

---

## Metadata Extraction

The loader extracts stable document-level metadata:

```text
source
study_id
treatment
```

Example:

```python
{
    "source": "study3.txt",
    "study_id": "STUDY-003",
    "treatment": "Treatment C"
}
```

This metadata is later useful for:

- Authorization scope
- Retrieval filtering
- Debugging
- Citations
- Context enrichment

---

## RecursiveCharacterTextSplitter

The CodeLab uses:

```python
RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)
```

Unlike a naive fixed-character splitter, this splitter tries to preserve logical separators such as:

```text
paragraphs
newlines
spaces
characters
```

This produced cleaner chunks than the manual CodeLab.

The final dataset produced:

```text
3 documents
12 chunks
```

Each study produced approximately four chunks:

```text
Chunk 0 → Study ID
Chunk 1 → Treatment description
Chunk 2 → Duration
Chunk 3 → Success criterion
```

---

## Important Learning

`RecursiveCharacterTextSplitter(...)` creates an object.

```python
splitter = RecursiveCharacterTextSplitter(...)
```

Then:

```python
splitter.split_documents(documents)
```

executes the split.

Input:

```text
list[Document]
```

Output:

```text
list[Document]
```

Metadata is preserved.

---

# Milestone 2 — Embeddings, Vector Store, and Retriever

## Goal

Convert chunks into semantic vectors and make them searchable.

Flow:

```text
Document Chunks
       ↓
HuggingFaceEmbeddings
       ↓
all-MiniLM-L6-v2
       ↓
384-dimensional vectors
       ↓
InMemoryVectorStore
       ↓
VectorStoreRetriever
```

---

## HuggingFaceEmbeddings

LangChain provides:

```python
HuggingFaceEmbeddings
```

as an abstraction over embedding models.

The underlying model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Important methods:

```python
embed_documents(list[str])
```

returns embeddings for documents.

```python
embed_query(str)
```

returns an embedding for one query.

The model produces:

```text
384-dimensional vectors
```

The embedding dimension is determined by the embedding model, not the length of input text.

---

## InMemoryVectorStore

The CodeLab uses:

```python
InMemoryVectorStore
```

It stores:

```text
Document
+
Embedding Vector
```

Conceptually:

```text
Record
├── vector
├── page_content
└── metadata
```

It is useful for learning, but it is not persistent.

Restarting the application means rebuilding the vector store.

---

## Retriever

A vector store and a retriever are related but not identical.

```text
Vector Store
→ stores and searches vectors

Retriever
→ standard query → documents interface
```

The vector store can become a retriever using:

```python
vector_store.as_retriever(...)
```

Then retrieval is executed using:

```python
retriever.invoke(query)
```

Input:

```text
str
```

Output:

```text
list[Document]
```

---

# Initial Retrieval Problem

The first query was:

```text
How long was the study for Treatment C?
```

Initial global vector search produced approximately:

```text
Rank 1
Treatment C description
Score ~0.6466

Rank 2
Treatment B duration
Score ~0.5804

Rank 3
Treatment A duration
Score ~0.5799

Rank 4
Treatment C duration
Score ~0.5657
```

The correct answer existed in the data:

```text
36 months
```

but was only rank 4.

---

# Why Did This Happen?

The duration chunk contained:

```text
The target study duration is 36 months.
```

It did not contain:

```text
Treatment C
```

The query contained two semantic signals:

```text
Treatment C
+
study duration
```

The duration chunk only represented the second part.

Vector similarity does not automatically understand that adjacent chunks belong together.

---

# Milestone 3 — Metadata Filtering and Context Enrichment

## Goal

Improve retrieval in two ways:

```text
Metadata filtering
→ reduce candidate scope

Context enrichment
→ improve semantic meaning
```

---

# Metadata Filtering

Example filter:

```python
{
    "study_id": "STUDY-003"
}
```

Conceptually:

```text
All 12 chunks
     ↓
study_id == STUDY-003
     ↓
4 eligible chunks
```

This prevents unrelated studies from competing in the similarity ranking.

Important principle:

> Metadata filtering is most reliable when the application already knows the scope.

Examples:

```text
Authorization
Selected customer
Selected study
Tenant
Department
Region
Document type
```

Authorization should not be inferred by the LLM.

---

## Callable Filter

A metadata filter is implemented as a function:

```python
def metadata_filter(document):
    return document.metadata.get(
        "study_id"
    ) == "STUDY-003"
```

The retriever receives this callable and evaluates documents against it.

---

# Context Enrichment

Metadata existing on a `Document` does not automatically mean the embedding model sees it.

If:

```python
Document(
    page_content="The target study duration is 36 months.",
    metadata={
        "treatment": "Treatment C"
    }
)
```

the embedding is normally generated from:

```text
page_content
```

not automatically from metadata.

Therefore the CodeLab creates a separate searchable representation:

```text
Study ID: STUDY-003
Treatment: Treatment C

Content:
The target study duration is 36 months.
```

Now the embedding model sees:

```text
STUDY-003
Treatment C
study duration
36 months
```

---

## Preserving Original Content

Search enrichment should not permanently destroy the clean source text.

Therefore the enriched search document contains:

```python
metadata["original_content"]
```

Example:

```python
Document(
    page_content="""
Study ID: STUDY-003
Treatment: Treatment C

Content:
The target study duration is 36 months.
""",
    metadata={
        "study_id": "STUDY-003",
        "treatment": "Treatment C",
        "original_content": (
            "The target study duration is 36 months."
        )
    }
)
```

This creates two representations:

```text
Search Representation
→ optimized for embedding/retrieval

Original Content
→ optimized for LLM context/display
```

---

# Result of Enrichment

Before enrichment:

```text
Correct duration score:
~0.5657
```

After enrichment + filtering:

```text
Correct duration score:
0.8383
```

and:

```text
Rank #1
```

This validated the hypothesis.

---

# Important Tradeoff

All STUDY-003 chunks now contain repeated context:

```text
Study ID: STUDY-003
Treatment: Treatment C
```

This increases similarity among all chunks in the same study.

That is useful in moderation.

Too much repeated context could make all chunks artificially similar.

Therefore context enrichment should be:

```text
small
stable
meaningful
relevant to retrieval
```

---

# Milestone 4 — Candidate Retrieval and Cross-Encoder Reranking

## Goal

Separate retrieval into two stages:

```text
Fast candidate discovery
+
More precise relevance ranking
```

Pipeline:

```text
Query
   ↓
Vector Retrieval
   ↓
Candidate-K = 4
   ↓
Cross Encoder
   ↓
Top-N = 3
```

---

# Bi-Encoder Retrieval

Embedding retrieval uses separate encodings:

```text
Query
   ↓
Embedding Model
   ↓
Query Vector


Document
   ↓
Embedding Model
   ↓
Document Vector
```

Then:

```text
Vector similarity
```

is calculated.

This is fast because document vectors can be precomputed.

---

# Cross-Encoder Reranking

The cross encoder processes:

```text
Query + Document
```

together.

Example:

```text
How long was the study for Treatment C?

+

The target study duration is 36 months.
```

The model directly scores relevance.

The CodeLab uses:

```text
BAAI/bge-reranker-base
```

---

# Why Not Use Cross Encoder for Everything?

Suppose the vector store contains:

```text
1,000,000 chunks
```

A cross encoder would need to evaluate:

```text
Query + Chunk 1
Query + Chunk 2
...
Query + Chunk 1,000,000
```

That is too expensive.

Instead:

```text
1,000,000 chunks
       ↓
Vector Search
       ↓
20–100 candidates
       ↓
Cross Encoder
       ↓
3–10 final documents
```

This architecture is known as:

```text
Retrieve → Rerank
```

---

# Actual Reranker Result

For the duration question:

```text
Duration chunk
0.9990

Success criterion
0.2733

Treatment description
0.2318

Study ID
0.0136
```

The correct evidence was clearly separated from the other candidates.

---

# Reranker Scores

Reranker scores should be treated primarily as relevance ranking signals.

Do not assume:

```text
0.9990
=
99.90% probability
```

Score interpretation depends on the model.

---

# Useful Python Concepts

## `zip()`

Given:

```python
documents = [
    doc1,
    doc2,
]

scores = [
    0.9,
    0.2,
]
```

Then:

```python
zip(documents, scores)
```

pairs corresponding values:

```python
[
    (doc1, 0.9),
    (doc2, 0.2),
]
```

---

## Sorting

```python
scored_documents.sort(
    key=lambda item: item[1],
    reverse=True,
)
```

Each item is:

```text
(document, score)
```

Therefore:

```python
item[1]
```

is the score.

`reverse=True` sorts from highest score to lowest.

---

# Milestone 5 — Prompt, Ollama, and Output Parsing

## Goal

Convert final retrieved evidence into an LLM answer.

Pipeline:

```text
Final Documents
      ↓
ContextFormatter
      ↓
Context String
      ↓
ChatPromptTemplate
      ↓
ChatOllama / Mistral
      ↓
AIMessage
      ↓
StrOutputParser
      ↓
str
```

---

# ContextFormatter

The LLM should receive clean source text rather than search-enrichment headers.

Therefore:

```python
document.metadata.get(
    "original_content",
    document.page_content,
)
```

is used.

Final context example:

```text
The target study duration is 36 months.

The primary success criterion is an improvement
in recovery time of at least 30 percent.

The study evaluates the effectiveness of Treatment C
for improving patient recovery time.
```

---

# ChatPromptTemplate

A chat prompt preserves roles.

Example:

```text
SystemMessage
→ application behavior

HumanMessage
→ context + question
```

The prompt contains placeholders:

```text
{context}
{question}
```

Calling:

```python
prompt.invoke(...)
```

substitutes real values.

It returns:

```text
ChatPromptValue
```

not a plain string.

---

# ChatOllama

The CodeLab uses:

```python
ChatOllama(
    model="mistral",
    temperature=0,
)
```

`temperature=0` is chosen for more deterministic factual responses.

Calling:

```python
model.invoke(prompt_value)
```

performs LLM inference.

Input:

```text
chat messages
```

Output:

```text
AIMessage
```

---

# AIMessage

The raw response contains more than just text.

Example:

```text
content
response_metadata
usage_metadata
tool_calls
model information
```

Example observed token usage:

```text
input_tokens: 153
output_tokens: 14
total_tokens: 167
```

---

# StrOutputParser

`StrOutputParser` converts:

```text
AIMessage
```

into:

```text
Python str
```

Example:

```text
AIMessage(
    content="The study lasted for 36 months."
)
```

becomes:

```text
"The study lasted for 36 months."
```

---

# Milestone 6 — Runnable and LCEL

## Goal

Replace manual orchestration with LangChain composition.

Manual flow:

```python
context = formatter.format(...)
prompt = prompt_service.format_prompt(...)
response = model_service.generate(...)
answer = parser.parse(...)
```

LCEL flow:

```text
Input
  ↓
Runnable branches
  ↓
Prompt
  ↓
Model
  ↓
Parser
```

Composition uses:

```python
|
```

Example:

```python
chain = (
    ...
    | prompt
    | model
    | parser
)
```

---

# Runnable

A Runnable is an executable LangChain abstraction.

Typical methods include:

```text
invoke
ainvoke
batch
stream
```

A complete composed chain is itself a Runnable.

---

# RunnableLambda

`RunnableLambda` converts a normal Python callable into a Runnable.

Example:

```python
RunnableLambda(
    lambda data: data["question"]
)
```

Equivalent normal function:

```python
def get_question(data):
    return data["question"]
```

---

# RunnableParallel

When a dictionary appears inside the LCEL chain:

```python
{
    "context": ...,
    "question": ...,
}
```

LangChain treats those values as parallel branches.

Both receive the same input.

Conceptually:

```text
                  Input
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Context Branch      Question Branch
          │                   │
          └─────────┬─────────┘
                    ▼
       {
         context: "...",
         question: "..."
       }
```

That dictionary then feeds:

```text
ChatPromptTemplate
```

because its variables are:

```text
{context}
{question}
```

---

# LCEL Flow

```text
Input Dict
    ↓
RunnableParallel
    ├── Documents branch
    │       ↓
    │  ContextFormatter
    │
    └── Question branch
            ↓
        Question string
    ↓
{
 context,
 question
}
    ↓
ChatPromptTemplate
    ↓
ChatPromptValue
    ↓
ChatOllama
    ↓
AIMessage
    ↓
StrOutputParser
    ↓
Final str
```

---

# Why LCEL?

LCEL does not change the underlying architecture.

It changes orchestration from imperative:

```text
call this
then call this
then call this
```

to declarative:

```text
this → this → this
```

It also gives components a consistent Runnable interface.

---

# Milestone 7 — Structured Output

## Goal

Replace free-form answer strings with predictable application objects.

Instead of:

```text
"The study lasted for 36 months."
```

return:

```python
StudyAnswer(
    study_id="STUDY-003",
    answer="The study duration for Treatment C is 36 months.",
    evidence_found=True,
)
```

---

# Pydantic Model

```python
class StudyAnswer(BaseModel):
    study_id: str
    answer: str
    evidence_found: bool
```

This defines the output contract.

---

# `Field()`

Fields include descriptions:

```python
answer: str = Field(
    description="A concise factual answer..."
)
```

The description becomes part of the generated schema and helps explain the expected value.

---

# `with_structured_output()`

The model is wrapped:

```python
structured_model = (
    model.with_structured_output(
        StudyAnswer
    )
)
```

Milestone 6:

```text
Model
 ↓
AIMessage
 ↓
StrOutputParser
 ↓
str
```

Milestone 7:

```text
Model.with_structured_output()
 ↓
StudyAnswer
```

Therefore no `StrOutputParser` is required for this path.

---

# Important Structured Output Lesson

Initial structured output returned:

```text
study_id='Treatment_C'
```

instead of:

```text
study_id='STUDY-003'
```

Why?

Because the LLM context contained:

```text
Treatment C
36 months
30 percent
```

but did not contain:

```text
STUDY-003
```

The schema correctly required:

```python
study_id: str
```

and `"Treatment_C"` is technically a valid string.

Therefore:

> Schema correctness does not guarantee factual correctness.

This is one of the most important lessons from the CodeLab.

---

# Structured Context Formatter

The solution was to provide metadata needed by the output schema.

Structured context became:

```text
Study ID: STUDY-003
Treatment: Treatment C
Content: The target study duration is 36 months.
```

After this change:

```text
study_id='STUDY-003'
```

was returned correctly.

---

# Deterministic Data vs LLM Generation

A stronger production design would often avoid asking the LLM to regenerate data already known by the application.

For example:

```text
study_id
→ deterministic metadata
→ application code

answer
→ semantic generation
→ LLM
```

Principle:

```text
Deterministic information
→ deterministic application logic

Semantic interpretation
→ LLM
```

---

# Positive Evidence Test

Question:

```text
How long was the study for Treatment C?
```

Result:

```text
study_id='STUDY-003'
answer='The study duration for Treatment C is 36 months.'
evidence_found=True
```

---

# Negative Evidence Test

Question:

```text
What was the average age of participants in Treatment C?
```

No participant-age information exists.

The retriever still returned documents because Top-K retrieval always returns the best available candidates.

Reranker scores were extremely low:

```text
0.0188
0.0100
0.0072
0.0017
```

Structured result:

```text
study_id='STUDY-003'

answer='The provided context does not contain enough information...'

evidence_found=False
```

---

# Critical RAG Lesson

```text
Retrieved something
≠
Found supporting evidence
```

A Top-K search always tries to return the closest documents.

That does not mean the answer exists.

Possible production safeguards include:

```text
similarity threshold
reranker threshold
evidence classifier
citation verification
LLM evidence check
```

Thresholds should be validated using evaluation data rather than chosen arbitrarily.

---

# Milestone 8 — Evaluation Harness

## Goal

Move from manually testing one question to repeatable automated evaluation.

Evaluation cases:

```text
Case 1
Treatment C duration

Case 2
Treatment C primary success criterion

Case 3
Duration + success criterion
```

---

# EvaluationCase

A Python `dataclass` represents each test:

```python
@dataclass
class EvaluationCase:
    name: str
    question: str
    filters: dict[str, str]
    expected_facts: list[str]
```

Example:

```python
EvaluationCase(
    name="Treatment C Duration",
    question=(
        "How long was the study "
        "for Treatment C?"
    ),
    filters={
        "study_id": "STUDY-003"
    },
    expected_facts=[
        "36 months"
    ],
)
```

---

# Why `@dataclass`?

Instead of manually writing:

```python
__init__()
```

Python generates common data-object behavior automatically.

This is a Python standard-library feature, not a LangChain feature.

---

# Independent Retrieval and Answer Evaluation

The evaluator checks two different things.

## Retrieval Pass

Does the retrieved evidence contain every expected fact?

Example:

```text
Expected:
36 months
```

Retrieved:

```text
The target study duration is 36 months.
```

Result:

```text
PASS
```

---

## Answer Pass

Does the generated answer contain every expected fact?

Example:

```text
Expected:
36 months
```

Answer:

```text
The study duration for Treatment C is 36 months.
```

Result:

```text
PASS
```

This separation helps diagnose failure location.

---

# Why Retrieval and Answer Should Be Evaluated Separately

Possible scenario:

```text
Retrieval: FAIL
Answer: PASS
```

This could indicate:

```text
LLM guessed correctly
or
evaluation mismatch
```

Another scenario:

```text
Retrieval: PASS
Answer: FAIL
```

This means:

```text
Evidence was available
but
generation failed to use it correctly
```

Therefore the two stages should not be collapsed into one metric.

---

# Multi-Fact Evaluation

The combined question:

```text
How long was the study for Treatment C
and what was its primary success criterion?
```

requires:

```text
36 months
+
30 percent
```

These facts occur in different chunks.

This tests:

```text
multi-chunk retrieval
+
reranking
+
context assembly
+
generation
```

---

# `all()` in Evaluation

Suppose:

```python
expected_facts = [
    "36 months",
    "30 percent",
]
```

Then:

```python
all(
    fact.lower() in answer
    for fact in expected_facts
)
```

means:

```text
"36 months" exists
AND
"30 percent" exists
```

Both must be true.

---

# Evaluation Results

Final CodeLab result:

```text
Total Cases: 3

Retrieval Passed: 3/3

Answers Passed: 3/3
```

Individual cases:

```text
Treatment C Duration
Retrieval: PASS
Answer: PASS

Treatment C Success Criterion
Retrieval: PASS
Answer: PASS

Treatment C Duration and Success Criterion
Retrieval: PASS
Answer: PASS
```

---

# What 3/3 Does NOT Mean

The system is not therefore:

```text
100% production accurate
```

The evaluation dataset currently contains:

```text
3 documents
12 chunks
3 positive evaluation cases
```

Production evaluation would require substantially more coverage.

Examples:

```text
paraphrased questions
missing evidence
wrong-study queries
authorization boundaries
ambiguous questions
long documents
conflicting facts
duplicate facts
outdated documents
multi-study comparisons
low-relevance retrieval
adversarial inputs
```

---

# Milestone 9 — Cleanup and Production Review

## Goal

Remove unnecessary runtime noise while preserving debugging tools and historical learning code.

Temporary diagnostics were not deleted.

They were commented with explanations so they can be re-enabled later.

---

# Preserved Diagnostics

## Search Context Enrichment Diagnostic

Used to inspect:

```text
raw content
vs
enriched searchable content
```

Useful if semantic retrieval quality unexpectedly changes.

---

## Embedding Dimension Diagnostic

Used to verify:

```text
all-MiniLM-L6-v2
→ 384 dimensions
```

Useful if the embedding model changes or dimension mismatch errors occur.

---

## Vector Candidate Diagnostic

Used to inspect:

```text
Vector Rank
Metadata
Original Content
```

Useful for debugging:

```text
wrong candidates
metadata filtering
semantic relevance
candidate_k
context enrichment
```

---

## Cross-Encoder Score Diagnostic

Used to inspect raw reranker scores.

Important:

Enabling both:

```text
score_documents()
and
rerank()
```

causes the cross encoder to score documents twice.

Therefore this diagnostic remains disabled during normal execution.

---

## Final Reranked Document Diagnostic

Used to inspect which documents survive:

```text
Candidate-K
→ Top-N
```

Useful when:

```text
retrieval found evidence
but
reranking removed it
```

---

# Recommended Debugging Order

If the final answer becomes incorrect:

```text
Wrong Final Answer
       ↓
Inspect Final Reranked Documents
       ↓
Is expected evidence present?
       │
       ├── YES
       │    ↓
       │  Generation / Prompt problem
       │
       └── NO
            ↓
      Inspect Vector Candidates
            ↓
      Was evidence retrieved?
            │
            ├── YES
            │    ↓
            │ Reranking problem
            │
            └── NO
                 ↓
          Retrieval problem
                 ↓
      Check:
      - metadata filter
      - enrichment
      - embeddings
      - chunking
      - candidate_k
```

This is far better than immediately modifying the prompt whenever an answer is wrong.

---

# Manual RAG vs LangChain

The same conceptual architecture exists in both implementations.

| Capability | Manual Implementation | LangChain Implementation |
|---|---|---|
| Document object | Custom text/metadata structure | `Document` |
| Chunking | Manual chunking logic | `RecursiveCharacterTextSplitter` |
| Embeddings | `SentenceTransformer` directly | `HuggingFaceEmbeddings` |
| Vector storage | Custom vector records | `InMemoryVectorStore` |
| Retrieval | Custom similarity function | `VectorStoreRetriever` |
| Metadata filtering | Custom logic | Retriever filter |
| Context enrichment | Custom | Custom wrapper around `Document` |
| Reranking | CrossEncoder directly | `HuggingFaceCrossEncoder` + `CrossEncoderReranker` |
| Prompt | Manual strings | `ChatPromptTemplate` |
| Model | Ollama invocation | `ChatOllama` |
| Pipeline | Manual function orchestration | Runnable + LCEL |
| Free-text parsing | Custom | `StrOutputParser` |
| Structured output | Manual parsing/schema logic | `.with_structured_output()` |
| Evaluation | Custom | Still custom |

---

# What LangChain Replaced

LangChain reduced repetitive framework-level code around:

```text
documents
embedding interfaces
vector-store interfaces
retriever interfaces
prompt handling
model integrations
output parsing
pipeline composition
structured output
```

---

# What LangChain Did NOT Replace

We still had to decide:

```text
What data should be indexed?

How should it be chunked?

Which metadata should exist?

Which metadata should be embedded?

Which metadata should only be used as filters?

What is the authorization scope?

Which embedding model?

Which reranker?

Candidate-K?

Top-K?

How much context?

What prompt rules?

What structured schema?

How should evidence be validated?

What evaluation cases matter?
```

These are RAG/application architecture decisions.

---

# LangChain Core Concepts Learned

## Document

```text
page_content
+
metadata
```

---

## Loader

Converts external source data into:

```text
Document
```

---

## Text Splitter

Converts:

```text
large Document
```

into:

```text
smaller Documents
```

while preserving metadata.

---

## Embeddings

Convert text into numerical vectors representing semantic meaning.

---

## Vector Store

Stores and searches:

```text
vectors + documents
```

---

## Retriever

Standard abstraction:

```text
query
→ relevant Documents
```

---

## PromptTemplate vs ChatPromptTemplate

```text
PromptTemplate
→ single textual prompt

ChatPromptTemplate
→ role-aware messages
```

---

## Runnable

Executable LangChain component.

Typical operations:

```text
invoke
ainvoke
batch
stream
```

---

## LCEL

LangChain Expression Language.

Used for composition:

```python
component_a | component_b | component_c
```

---

## RunnableLambda

Wraps ordinary Python functions as LangChain Runnables.

---

## RunnableParallel

Runs multiple branches using the same input and combines their outputs.

---

## StrOutputParser

Converts model output such as:

```text
AIMessage
```

to:

```text
str
```

---

## Structured Output

Defines the expected model-output contract before generation.

Example:

```python
StudyAnswer
```

instead of arbitrary prose.

---

# Important Python Concepts Reinforced

## `dict.get()`

```python
metadata.get(
    "original_content",
    fallback,
)
```

Returns:

```text
value if key exists
otherwise fallback
```

---

## Dictionary Unpacking

```python
{
    **document.metadata,
    "original_content": original_content,
}
```

copies existing dictionary values into a new dictionary.

---

## `defaultdict`

Used to maintain independent chunk indexes per source.

---

## Generator Expressions

Example:

```python
(
    document
    for document in documents
    if condition
)
```

generates matching items lazily.

---

## `next()`

Returns the first value from an iterator/generator.

---

## `join()`

```python
"\n\n".join(parts)
```

combines strings with blank lines between them.

---

## `zip()`

Pairs corresponding values from multiple iterables.

---

## `lambda`

Short anonymous function:

```python
lambda data: data["question"]
```

---

## `all()`

Returns true only when every supplied condition is true.

---

## `sum()` with Booleans

In Python:

```text
True  → 1
False → 0
```

Therefore:

```python
sum(
    result.answer_pass
    for result in results
)
```

counts passing results.

---

## Tuple Reminder

Parentheses alone do not create a tuple.

```python
("hello")
```

is:

```text
str
```

while:

```python
("hello",)
```

is:

```text
tuple
```

The comma creates the tuple.

---

# Search Text vs LLM Context

One of the most useful architecture lessons from this CodeLab is that the text used for retrieval does not necessarily need to be identical to the text sent to the LLM.

Example:

```text
SEARCH TEXT

Study ID: STUDY-003
Treatment: Treatment C
Content:
The target study duration is 36 months.
```

can be used for embeddings.

While:

```text
LLM CONTEXT

The target study duration is 36 months.
```

can be used for normal generation.

For structured output requiring study metadata:

```text
STRUCTURED LLM CONTEXT

Study ID: STUDY-003
Treatment: Treatment C
Content:
The target study duration is 36 months.
```

can be used instead.

Different representations serve different purposes.

---

# Metadata Filtering vs Semantic Retrieval

These mechanisms solve different problems.

```text
Metadata Filter
→ Which documents are allowed/eligible?

Semantic Search
→ Which eligible documents are most relevant?
```

Example:

```text
All company research
       ↓
Authorization / Study Scope
       ↓
Allowed documents only
       ↓
Semantic ranking
```

For protected data, authorization should happen before retrieved information reaches the LLM.

---

# Retrieval vs Reranking

```text
Retriever
→ fast candidate discovery

Reranker
→ precise candidate ordering
```

Production example:

```text
Millions of chunks
       ↓
Vector Retrieval
       ↓
Top 50
       ↓
Cross Encoder
       ↓
Top 5
```

---

# Retriever vs Tool

A Retriever is specifically:

```text
query
→ relevant Documents
```

A Tool is a generic callable capability.

Examples:

```text
search_documents
send_email
calculate_risk
query_database
get_weather
```

A retriever may later be exposed as a Tool when building agents.

This becomes especially relevant in the LangGraph/Agents phases.

---

# Output Parser vs Structured Output

## Output Parser

Processes model output after generation.

Example:

```text
AIMessage
↓
StrOutputParser
↓
str
```

---

## Structured Output

Defines the expected structure of model output.

Example:

```text
StudyAnswer schema
↓
Model generation
↓
StudyAnswer object
```

The distinction is:

```text
Parser
→ post-process output

Structured Output
→ output contract
```

---

# RAG Failure Modes Observed

## Correct Answer Chunk Ranked Too Low

Cause:

```text
Chunk lacked parent/entity context
```

Solution:

```text
context enrichment
```

---

## Unrelated Studies Ranked Highly

Cause:

```text
global semantic search
```

Solution:

```text
metadata filtering
```

---

## Retriever Returns Documents for Unanswerable Question

Cause:

```text
Top-K always returns closest available items
```

Solution candidates:

```text
relevance threshold
reranker threshold
evidence validation
```

---

## Structured Field Had Incorrect Value

Cause:

```text
required factual value absent from LLM context
```

Lesson:

```text
Schema validation
≠
semantic correctness
```

---

# Production Gaps

This CodeLab is intentionally production-style but not production-ready.

## Persistent Vector Database

Current:

```text
InMemoryVectorStore
```

Production may use:

```text
Qdrant
Pinecone
Weaviate
Milvus
pgvector
Azure AI Search
Elasticsearch
```

depending on requirements.

---

## Indexing Lifecycle

Missing:

```text
incremental indexing
document updates
deletions
versioning
re-indexing strategy
embedding migrations
```

---

## Authorization

Current:

```text
hardcoded study_id filter
```

Production:

```text
Authenticated User
      ↓
Authorization Rules
      ↓
Allowed Study IDs / Tenant / Department
      ↓
Retriever Filter
      ↓
Only authorized content reaches LLM
```

Critical principle:

> Do not retrieve protected data first and ask the LLM to hide it.

Authorization must happen before LLM context construction.

---

## Relevance Threshold

Currently:

```text
Top-K always returns candidates
```

Production may require:

```text
vector threshold
and/or
reranker threshold
```

Thresholds must be evaluated and calibrated.

---

## Observability

Production systems should track:

```text
query
retrieved document IDs
retrieval scores
reranker scores
latency
token usage
model version
prompt version
errors
evidence/citations
```

while respecting privacy and security requirements.

---

## Error Handling

Current lab does not comprehensively handle:

```text
Ollama unavailable
embedding model unavailable
model timeout
vector-store failure
invalid structured response
missing metadata
empty retrieval
reranker error
```

Production requires explicit failure behavior.

---

## Evaluation

Current:

```text
3 cases
```

Production requires:

```text
larger golden dataset
retrieval metrics
generation metrics
groundedness
hallucination checks
security tests
authorization tests
regression evaluation
```

---

## Retrieval Metrics

Useful metrics include:

```text
Precision@K
Recall@K
Reciprocal Rank
MRR
```

These were explored in the manual RAG CodeLab and remain applicable here.

---

## Generation Evaluation

Potential dimensions:

```text
correctness
groundedness
faithfulness
citation accuracy
completeness
format validity
```

---

## API Layer

Current application runs through:

```text
main.py
```

Production would typically expose:

```text
REST
GraphQL
internal service
event-driven worker
```

depending on architecture.

---

## Caching

Potential cache layers:

```text
document embeddings
query embeddings
retrieval results
LLM responses
```

Caching should only be used where security and freshness constraints permit.

---

# Security Considerations

For an enterprise internal RAG system:

```text
User
 ↓
Authentication
 ↓
Authorization
 ↓
Allowed metadata scope
 ↓
Retriever
 ↓
Authorized documents only
 ↓
LLM
```

Never:

```text
User
 ↓
Retrieve everything
 ↓
LLM
 ↓
"Please hide unauthorized information"
```

The LLM is not the authorization boundary.

---

# Connection to the Future Clinical Research Platform

This CodeLab directly supports the future architecture of the:

```text
AI-Assisted Clinical Research Intelligence
& Monitoring Platform
```

For a researcher:

```text
Question
 ↓
User authorization
 ↓
Allowed studies
 ↓
Metadata-filtered retrieval
 ↓
Reranking
 ↓
Evidence
 ↓
LLM summary/answer
```

For structured monitoring:

```text
Study Data
 ↓
Objective Rules / Analytics
 ↓
Structured Findings
 ↓
LLM explanation where appropriate
 ↓
Human decision
```

Important AI boundary:

```text
AI may:
retrieve
summarize
compare
calculate
classify
identify predefined deviations
explain data

AI should not:
recommend treatment
recommend dosage
change protocols
make clinical decisions
make regulatory decisions
```

Principle:

> AI reports what the data says. Humans decide what to do.

---

# Final CodeLab Result

The final evaluation run produced:

```text
Treatment C Duration
Retrieval: PASS
Answer: PASS

Treatment C Success Criterion
Retrieval: PASS
Answer: PASS

Treatment C Duration and Success Criterion
Retrieval: PASS
Answer: PASS
```

Summary:

```text
Total Cases: 3
Retrieval Passed: 3/3
Answers Passed: 3/3
```

---

# Final Learning Summary

The complete CodeLab evolved through:

```text
Milestone 1
Document Loading + Chunking
        ↓
Milestone 2
Embeddings + Vector Store + Retriever
        ↓
Milestone 3
Metadata Filtering + Context Enrichment
        ↓
Milestone 4
Candidate Retrieval + Cross-Encoder Reranking
        ↓
Milestone 5
Prompt + Ollama + Output Parser
        ↓
Milestone 6
Runnable + LCEL
        ↓
Milestone 7
Structured Output
        ↓
Milestone 8
Evaluation Harness
        ↓
Milestone 9
Cleanup + Production Review
```

All milestones:

```text
Milestone 1   ✅
Milestone 2   ✅
Milestone 3   ✅
Milestone 4   ✅
Milestone 5   ✅
Milestone 6   ✅
Milestone 7   ✅
Milestone 8   ✅
Milestone 9   ✅
```

---

# Key Takeaways

```text
1. LangChain is an orchestration/framework layer,
   not the intelligence itself.

2. RAG quality still depends on architecture decisions.

3. Metadata filtering controls scope.

4. Semantic embeddings rank meaning.

5. Metadata is not automatically embedded.

6. Context enrichment can improve semantic retrieval.

7. Search representation and LLM context may differ.

8. Vector retrieval is good for candidate generation.

9. Cross encoders are better suited for reranking.

10. Retrieved documents do not automatically mean
    supporting evidence exists.

11. ChatPromptTemplate preserves message roles.

12. Chat models return structured AIMessage objects.

13. StrOutputParser converts model output to plain strings.

14. Runnable is LangChain's executable abstraction.

15. LCEL composes Runnables declaratively.

16. RunnableLambda wraps normal Python functions.

17. Structured output provides predictable schemas.

18. Schema correctness does not guarantee factual correctness.

19. Deterministic values should preferably remain
    application-controlled.

20. Retrieval and generation should be evaluated separately.

21. LangChain reduces orchestration code but does not
    eliminate system-design responsibility.

22. Authorization must occur before protected data
    reaches the LLM.

23. Evaluation is part of RAG engineering, not an
    afterthought.

24. Debugging should begin by identifying which pipeline
    stage failed rather than immediately changing prompts.
```

---

# Phase Completion

With this CodeLab completed:

```text
Phase 5 — LangChain
```

is complete from both:

```text
Conceptual Understanding
+
Hands-On Implementation
```

The next learning phase is:

```text
Phase 6 — LangGraph
```

where the focus shifts from linear chains such as:

```text
A → B → C → D
```

toward stateful workflows involving:

```text
State
Nodes
Edges
Conditional Routing
Cycles
Persistence
Human-in-the-loop
Multi-step agent workflows
```

The LangChain concepts learned here—especially:

```text
Runnable
LCEL
Tools
Structured Output
Retrievers
Chat Models
```

form the foundation for that next phase.