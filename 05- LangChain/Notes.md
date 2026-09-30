````md
# LangChain — Notes

## 1. What is LangChain?

LangChain is a framework for building applications that use Large Language Models together with other application components such as:

- Prompts
- Documents
- Embeddings
- Vector stores
- Retrievers
- Output parsers
- Structured output
- Tools
- External APIs and services

LangChain does not provide the intelligence itself.

The intelligence comes from components such as:

- LLMs
- Embedding models
- Reranking models
- Search systems
- External APIs
- Business services

LangChain mainly provides:

```text
Abstractions
+
Standard Interfaces
+
Composition
+
Execution
```

A useful mental model is:

```text
LLM Components
     ↓
LangChain Abstractions
     ↓
Runnable Components
     ↓
LCEL Composition
     ↓
LLM Application
```

---

## 2. Why Did We Learn RAG Before LangChain?

Before learning LangChain, we implemented RAG manually.

Our manual RAG system included:

```text
Documents
   ↓
Loading
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
Metadata Filtering
   ↓
Retrieval
   ↓
Hybrid Search
   ↓
Reranking
   ↓
Context Building
   ↓
Prompt
   ↓
LLM
   ↓
Answer
```

We intentionally avoided LangChain during that phase.

The reason was to understand what actually happens inside a RAG system.

If we had started directly with:

```python
retriever = vector_store.as_retriever()
```

without understanding retrieval first, we might know how to use an API without understanding:

- What is being retrieved?
- How similarity works
- What Top-K means
- Why metadata filtering matters
- Why reranking is needed
- Why chunking quality affects retrieval
- Why authorization must happen before LLM context creation

Now LangChain is easier to understand because we can ask:

> What manual component is this LangChain abstraction replacing or standardizing?

---

# 3. LangChain Document

A LangChain `Document` represents text together with metadata.

Example:

```python
from langchain_core.documents import Document

doc = Document(
    page_content="Treatment C lasted 36 months.",
    metadata={
        "study_id": "STUDY-003",
        "source": "study3.txt"
    }
)
```

Conceptually:

```text
Document
├── page_content
└── metadata
```

`page_content` contains the actual text.

`metadata` contains information about that text.

Example metadata:

```python
{
    "study_id": "STUDY-003",
    "source": "study3.txt",
    "chunk_index": 2
}
```

Metadata is useful for:

- Filtering
- Authorization
- Source tracking
- Citations
- Debugging
- Document versioning
- Retrieval analysis

### Manual RAG Mapping

Our manual implementation:

```text
Document(content, metadata)
```

LangChain:

```text
Document(page_content, metadata)
```

The idea is essentially the same.

---

# 4. Document Loaders

A Document Loader reads information from an external source and converts it into LangChain `Document` objects.

Conceptually:

```text
External Data
     ↓
Document Loader
     ↓
LangChain Documents
```

Possible sources include:

- TXT
- PDF
- CSV
- HTML
- Web pages
- Databases
- APIs
- Cloud storage

Example conceptually:

```python
loader = SomeDocumentLoader("study3.txt")

documents = loader.load()
```

Result:

```python
[
    Document(
        page_content="...",
        metadata={...}
    )
]
```

### Important Point

A loader does not automatically solve data-quality problems.

Production ingestion may still require:

```text
File
 ↓
Validation
 ↓
OCR if required
 ↓
Parsing
 ↓
Cleaning
 ↓
Metadata enrichment
 ↓
Document creation
```

LangChain provides loader abstractions, but production ingestion design is still our responsibility.

---

# 5. Text Splitters

Large documents are usually too large or too broad to embed and retrieve as one unit.

A Text Splitter divides documents into smaller chunks.

```text
Large Document
      ↓
Text Splitter
      ↓
Chunk 1
Chunk 2
Chunk 3
...
```

Example idea:

```python
splitter = SomeTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
```

Each resulting chunk is typically still a `Document`.

Example:

```python
Document(
    page_content="The study duration was 36 months...",
    metadata={
        "study_id": "STUDY-003"
    }
)
```

### Why Chunking Matters

Bad chunking can split an important fact:

```text
Chunk 1:
"The primary success criteri"

Chunk 2:
"on was an improvement in recovery time..."
```

Retrieval may then fail even if the correct information exists in the source.

LangChain provides splitting utilities, but choosing the right strategy is still an architectural decision.

Possible approaches:

```text
Fixed size
Sentence aware
Paragraph aware
Recursive splitting
Semantic splitting
Structure-aware splitting
```

---

# 6. Embeddings

Embeddings convert text into numerical vectors representing semantic information.

Conceptually:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Example:

```text
"Treatment C lasted 36 months."
              ↓
         Embedding Model
              ↓
[0.012, -0.091, 0.323, ...]
```

LangChain provides a common interface for different embedding implementations.

Conceptually:

```python
vector = embeddings.embed_query(
    "How long was Treatment C?"
)
```

For documents:

```python
vectors = embeddings.embed_documents(
    [
        "Treatment C lasted 36 months.",
        "Treatment B lasted 24 months."
    ]
)
```

### Important Point

LangChain does not determine whether an embedding model is good for our use case.

We still need to evaluate:

- Semantic quality
- Domain suitability
- Dimensions
- Latency
- Cost
- Deployment requirements

---

# 7. Vector Store

A Vector Store stores embeddings and allows similarity search.

Conceptually:

```text
Documents
    ↓
Embeddings
    ↓
Vector Store
```

At query time:

```text
Question
   ↓
Query Embedding
   ↓
Similarity Search
   ↓
Relevant Documents
```

Examples of systems commonly integrated with LangChain include:

```text
FAISS
Chroma
Pinecone
Qdrant
Weaviate
```

Example conceptually:

```python
vector_store = SomeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings
)
```

Then:

```python
results = vector_store.similarity_search(
    "How long was Treatment C?"
)
```

---

# 8. Retriever

A Retriever is a higher-level abstraction whose job is:

```text
Query
  ↓
Retriever
  ↓
Relevant Documents
```

Example:

```python
retriever = vector_store.as_retriever()

documents = retriever.invoke(
    "How long was Treatment C?"
)
```

The important point is that a Retriever is an interface.

The underlying strategy may be:

```text
Vector Search
BM25
Hybrid Search
Database Search
External Search API
Custom Retrieval Logic
```

The rest of the application only needs to know:

```text
Query → Documents
```

---

# 9. Vector Store vs Retriever

These are related but not identical.

```text
Vector Store
= stores vectors and performs similarity search
```

```text
Retriever
= abstraction that receives a query and returns relevant Documents
```

A Retriever may use a Vector Store internally:

```text
Retriever
   ↓
Vector Store
```

But a Retriever does not have to use vectors.

For example:

```text
Retriever
   ↓
BM25 Search
```

or:

```text
Retriever
   ↓
Internal Company Search API
```

### Mental Model

Think of Retriever similar to an interface:

```text
Application
    ↓
Retriever
    ↓
Implementation
```

This creates loose coupling.

---

# 10. PromptTemplate

A `PromptTemplate` creates reusable prompts with variables.

Example:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """
    Answer the question using the provided context.

    Context:
    {context}

    Question:
    {question}
    """
)
```

Input:

```python
{
    "context": "Treatment C lasted 36 months.",
    "question": "How long was Treatment C?"
}
```

The template produces a formatted prompt.

Conceptually:

```text
Template
+
Variables
 ↓
Formatted Prompt
```

### Manual RAG Mapping

Our manual:

```text
PromptBuilder
```

LangChain:

```text
PromptTemplate
```

---

# 11. ChatPromptTemplate

Modern LLM applications commonly use chat models.

Chat models work with messages rather than one large string.

Example:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer only from the provided context."
        ),
        (
            "human",
            """
            Context:
            {context}

            Question:
            {question}
            """
        )
    ]
)
```

Conceptually:

```text
SystemMessage
"Answer only from context."

HumanMessage
"Context: ...
 Question: ..."
```

### PromptTemplate vs ChatPromptTemplate

```text
PromptTemplate
= formatted text
```

```text
ChatPromptTemplate
= structured messages with roles
```

For modern chat LLMs, `ChatPromptTemplate` is usually the more natural option.

---

# 12. Runnable

A Runnable is a LangChain component that follows a standard execution interface.

Conceptually:

```text
Input
  ↓
Runnable
  ↓
Output
```

A Runnable can typically support execution methods such as:

```python
invoke()
batch()
stream()
ainvoke()
abatch()
```

Examples of components that can behave as Runnables:

```text
Prompt
Chat Model
Output Parser
Retriever
RunnableLambda
RunnablePassthrough
RunnableSequence
```

### Why Does Runnable Exist?

Imagine every component had completely different APIs.

Example:

```python
prompt.format(...)
model.generate(...)
parser.parse(...)
retriever.search(...)
```

Composition becomes harder.

Runnable gives components a more consistent execution model.

Conceptually:

```python
component.invoke(input)
```

This consistency makes pipeline composition easier.

---

# 13. LCEL

LCEL stands for:

**LangChain Expression Language**

LCEL is used to compose Runnables into pipelines.

Example:

```python
chain = prompt | model | parser
```

Conceptually:

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

The `|` operator means:

```text
Output of left Runnable
          ↓
Input of right Runnable
```

---

# 14. Runnable vs LCEL

Runnable and LCEL are not the same.

```text
Runnable
= executable building block
```

```text
LCEL
= composition syntax/mechanism
```

Example:

```python
prompt | model | parser
```

Here:

```text
prompt → Runnable
model → Runnable
parser → Runnable
```

The composition:

```text
prompt | model | parser
```

is LCEL.

### Important Property

The resulting chain is itself another Runnable.

Conceptually:

```text
Runnable
   +
Runnable
   +
Runnable
   ↓
LCEL Composition
   ↓
Combined Runnable
```

Therefore:

```python
chain.invoke(...)
```

works.

### Simple Mental Model

```text
Runnable
"What can execute?"
```

```text
LCEL
"How do I connect executable components?"
```

---

# 15. invoke()

`invoke()` runs a Runnable for one input.

Example:

```python
result = chain.invoke(
    {
        "question": "What is RAG?"
    }
)
```

Conceptually:

```text
Single Input
    ↓
Runnable
    ↓
Single Output
```

---

# 16. batch()

`batch()` executes the same Runnable for multiple inputs.

Conceptually:

```text
Input 1 ─┐
Input 2 ─┼─→ Runnable → Results
Input 3 ─┘
```

Example:

```python
results = chain.batch(
    [
        {"question": "Question 1"},
        {"question": "Question 2"},
        {"question": "Question 3"}
    ]
)
```

---

# 17. stream()

`stream()` allows output to be consumed incrementally.

Instead of:

```text
Wait
 ↓
Complete Answer
```

we can receive:

```text
Token / Chunk
Token / Chunk
Token / Chunk
...
```

This improves perceived responsiveness in chat applications.

---

# 18. Async Execution

LangChain Runnables may also expose asynchronous variants.

Example:

```python
await chain.ainvoke(...)
```

or:

```python
await chain.abatch(...)
```

Useful when:

- Calling network APIs
- Processing many requests
- Building async web services
- Running concurrent I/O operations

---

# 19. RunnablePassthrough

`RunnablePassthrough` forwards its input unchanged.

Conceptually:

```text
Input
 ↓
RunnablePassthrough
 ↓
Same Input
```

This becomes very useful when branching data.

Consider RAG.

We need the user's question for two purposes:

1. Send it to the Retriever.
2. Preserve it for the final prompt.

Conceptually:

```text
                 Question
                    │
           ┌────────┴────────┐
           ↓                 ↓
       Retriever      RunnablePassthrough
           ↓                 ↓
        Context       Original Question
           └────────┬────────┘
                    ↓
                  Prompt
```

The original question is not modified.

---

# 20. RunnableLambda

`RunnableLambda` wraps a normal Python function so it can participate in a Runnable pipeline.

Example:

```python
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )
```

We may need this because a Retriever returns:

```python
[
    Document(...),
    Document(...),
    Document(...)
]
```

but our prompt expects:

```text
Context:
text...
text...
text...
```

So:

```text
Documents
    ↓
RunnableLambda(format_docs)
    ↓
Context String
```

### RunnableLambda vs RunnablePassthrough

```text
RunnableLambda
= execute custom transformation
```

```text
RunnablePassthrough
= preserve input unchanged
```

---

# 21. Simple LCEL Chain

Consider:

```python
chain = prompt | model | parser
```

Execution:

```python
result = chain.invoke(
    {
        "question": "What is RAG?"
    }
)
```

Internally, conceptually:

```text
Input Dictionary
      ↓
Prompt Runnable
      ↓
Prompt Value
      ↓
Model Runnable
      ↓
AIMessage
      ↓
Parser Runnable
      ↓
String
```

LCEL makes this orchestration declarative.

---

# 22. RAG with Runnable Branching

A RAG pipeline needs both:

```text
Retrieved Context
+
Original Question
```

Conceptually:

```text
                   Question
                      │
           ┌──────────┴──────────┐
           ↓                     ↓
       Retriever         RunnablePassthrough
           ↓                     ↓
       Documents              Question
           ↓
   RunnableLambda
     format_docs()
           ↓
        Context
           └──────────┬──────────┘
                      ↓
             ChatPromptTemplate
                      ↓
                 Chat Model
                      ↓
                Output Parser
                      ↓
                    Answer
```

This is an important LCEL pattern.

---

# 23. Output Parser

A model often returns a LangChain message object.

For example:

```python
AIMessage(
    content="Treatment C lasted 36 months."
)
```

Sometimes the application only wants:

```python
"Treatment C lasted 36 months."
```

We can use:

```python
from langchain_core.output_parsers import StrOutputParser
```

Example:

```python
chain = prompt | model | StrOutputParser()
```

Flow:

```text
Model
 ↓
AIMessage
 ↓
StrOutputParser
 ↓
Python String
```

An Output Parser processes the model output **after generation**.

---

# 24. Other Output Parsing Scenarios

Applications may require something more structured than a string.

For example, the model may generate:

```json
{
    "study_id": "STUDY-003",
    "duration_months": 36
}
```

A parser may convert generated text into:

```python
{
    "study_id": "STUDY-003",
    "duration_months": 36
}
```

Conceptually:

```text
Generated Model Response
          ↓
       Parser
          ↓
Application Representation
```

---

# 25. Structured Output

Structured Output takes a slightly different approach.

Instead of only parsing arbitrary model output afterward, we define the expected structure up front.

Example:

```python
from pydantic import BaseModel


class StudyResult(BaseModel):
    study_id: str
    duration_months: int
```

Then conceptually:

```python
structured_model = model.with_structured_output(
    StudyResult
)
```

Now the model invocation is configured around the expected schema.

Result conceptually:

```python
StudyResult(
    study_id="STUDY-003",
    duration_months=36
)
```

---

# 26. Output Parser vs Structured Output

This distinction is important.

### Output Parser

```text
Prompt
 ↓
Model
 ↓
Generated Output
 ↓
Parser
 ↓
Application Value
```

The parser handles what was generated.

### Structured Output

```text
Schema
  ↓
Configured Model
  ↓
Structured Result
```

The expected output contract is defined before the model is called.

### Easy Mental Model

```text
Output Parser
= post-processing
```

```text
Structured Output
= output contract
```

### Important Nuance

Structured output may internally still involve parsing or validation.

So these concepts are related.

But from an application-design perspective:

```text
Parser
→ "What do I do with the generated response?"
```

```text
Structured Output
→ "What shape of response do I expect the model to produce?"
```

---

# 27. Why Structured Output Matters

Free-form text is fine for a human-facing chatbot.

Example:

```text
Treatment C lasted 36 months.
```

But application logic may need:

```json
{
    "duration_months": 36
}
```

Structured output is particularly useful for:

- APIs
- Database writes
- Classification
- Workflow decisions
- Extracting entities
- Risk categorization
- Application UI
- Tool orchestration

Example:

```text
LLM
 ↓
{
  "study_id": "STUDY-003",
  "risk_level": "HIGH"
}
 ↓
Application Logic
```

---

# 28. Tools

A Tool is a callable capability that an LLM or agent can use.

Examples:

```text
Calculator
REST API
Database
Retriever
Search Service
Internal Business Function
```

Example:

```python
from langchain_core.tools import tool


@tool
def get_study_duration(study_id: str) -> str:
    """Return the duration of a study."""
    
    if study_id == "STUDY-003":
        return "36 months"

    return "Study not found"
```

The tool has information such as:

```text
Name
Description
Input Schema
Implementation
```

---

# 29. Why Tool Descriptions Matter

Suppose an agent has these tools:

```text
get_study_duration
get_study_status
get_incidents
```

The model must determine which tool is appropriate.

Tool descriptions provide semantic information about the capability.

Example:

```text
get_study_duration

Description:
"Returns the configured duration for a clinical research study."
```

The model can use the description when deciding which tool to request.

---

# 30. Does the LLM Execute the Tool?

No.

The LLM does not directly execute Python functions or APIs.

Instead:

```text
User
 ↓
LLM
 ↓
Tool Call Request
 ↓
Application / Agent Runtime
 ↓
Actual Tool Execution
 ↓
Tool Result
 ↓
LLM
```

Example:

```text
LLM says:

Call:
get_study_duration(
    study_id="STUDY-003"
)
```

The application runtime executes:

```python
get_study_duration("STUDY-003")
```

Then returns:

```text
36 months
```

to the model.

---

# 31. Retriever vs Tool

A Retriever has a narrow standardized purpose:

```text
Query
 ↓
Relevant Documents
```

A Tool is more generic:

```text
Input
 ↓
External Capability
 ↓
Result
```

A Retriever can also be exposed as a Tool when agents are introduced.

Example:

```text
Agent
 ├── Research Retriever Tool
 ├── Calculator Tool
 ├── Study Status Tool
 └── Incident Lookup Tool
```

---

# 32. Tool vs Normal Function

A normal Python function:

```python
def calculate_progress(...):
    ...
```

is application code.

A LangChain Tool wraps/exposes a capability in a form that an LLM or agent can understand and request.

Conceptually:

```text
Python Function
      ↓
Tool Metadata
      ↓
LLM-Callable Capability
```

---

# 33. LangChain Chat Models

LangChain provides abstractions around chat-model providers.

Conceptually:

```text
Application
    ↓
LangChain Chat Model Interface
    ↓
Provider
```

This can make it easier to switch providers or integrate models consistently.

Example conceptually:

```python
model = SomeChatModel(...)
```

Then:

```python
response = model.invoke(messages)
```

### Important Point

Provider abstraction does not guarantee complete portability.

Different models may still differ in:

- Tool calling
- Structured output support
- Context windows
- Token behavior
- Pricing
- Capabilities
- System-message handling

---

# 34. Manual RAG vs LangChain Mapping

| Manual RAG | LangChain |
|---|---|
| `Document` | `Document` |
| `DocumentLoader` | Document Loader |
| `DocumentChunker` | Text Splitter |
| `EmbeddingService` | Embeddings |
| `VectorStore` | Vector Store |
| `Retriever` | Retriever |
| `PromptBuilder` | `PromptTemplate` / `ChatPromptTemplate` |
| `LLMService` | Chat Model |
| Custom Python processing | `RunnableLambda` |
| Preserve original input | `RunnablePassthrough` |
| Manual orchestration | Runnable + LCEL |
| Response conversion | Output Parser |
| Typed response | Structured Output |
| External capability | Tool |

---

# 35. Basic LangChain RAG Architecture

Offline ingestion:

```text
Documents
   ↓
Document Loader
   ↓
Text Splitter
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Store
```

Online query:

```text
User Question
      ↓
Retriever
      ↓
Relevant Documents
      ↓
Format Context
      ↓
Prompt
      ↓
Chat Model
      ↓
Output Parser
      ↓
Answer
```

With LCEL:

```text
Question
   │
   ├── Retriever → Documents → Format → Context
   │
   └── Passthrough → Question
                ↓
              Prompt
                ↓
              Model
                ↓
              Parser
                ↓
              Answer
```

---

# 36. LangChain Does Not Automatically Improve RAG

Using LangChain does not automatically improve:

```text
Chunking
Retrieval
Embeddings
Reranking
Authorization
Prompt quality
Groundedness
Evaluation
Latency
Cost
Security
```

For example:

```text
Bad Chunking
     ↓
LangChain Retriever
     ↓
Still Bad Retrieval
```

The framework cannot compensate for poor architecture.

---

# 37. Authorization Still Belongs Outside the LLM

For enterprise systems, authorization must happen before protected information reaches the model.

Correct pattern:

```text
Authenticated User
      ↓
Authorization
      ↓
Allowed Study/Data Scope
      ↓
Retriever / Metadata Filter
      ↓
Authorized Documents
      ↓
LLM
```

Incorrect pattern:

```text
Retrieve Everything
      ↓
Send to LLM
      ↓
Ask LLM to hide unauthorized data
```

LangChain does not change this security requirement.

---

# 38. Why Use LangChain?

LangChain can provide value through:

- Standardized component interfaces
- Easier composition
- Provider integrations
- Runnable execution model
- LCEL pipelines
- Streaming
- Batch execution
- Async execution
- Retriever composition
- Output parsing
- Structured output
- Tool integration

As applications become more complex, common abstractions can reduce repetitive orchestration code.

---

# 39. When LangChain May Be Unnecessary

Consider a simple application:

```text
User
 ↓
Prompt
 ↓
LLM
 ↓
Response
```

Plain Python may be enough.

Adding:

```text
Framework
Runnable
LCEL
Multiple abstractions
```

may increase complexity without providing enough benefit.

LangChain becomes more valuable when the application contains:

```text
Retrieval
Multiple components
Tools
Structured outputs
Branching
Streaming
Async operations
External integrations
Reusable pipelines
```

---

# 40. Advantages of LangChain

Potential advantages include:

```text
Standard abstractions
Reusable components
Composition
Large integration ecosystem
Provider abstraction
Streaming support
Async support
Tool integration
Retriever abstraction
Structured output helpers
```

---

# 41. Possible Disadvantages

Potential disadvantages include:

```text
Additional abstraction layers
Learning framework concepts
Version/API changes
Debugging complexity
Hidden implementation details
Framework dependency
Possible overengineering
```

A developer should understand the underlying architecture rather than treating LangChain APIs as magic.

---

# 42. Important Design Principle

Do not start with:

> How can I use LangChain here?

Start with:

> What problem am I solving?

Then determine:

```text
Problem
 ↓
Architecture
 ↓
Required Components
 ↓
Do LangChain abstractions help?
```

The framework should support the architecture, not define it.

---

# 43. Relationship Between LangChain and Agents

Basic LangChain applications can be deterministic pipelines:

```text
Input
 ↓
Retriever
 ↓
Prompt
 ↓
Model
 ↓
Output
```

Agents introduce model-driven decisions such as:

```text
Which tool should I call?
Do I need another tool?
Do I already have enough information?
```

Conceptually:

```text
LLM
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
LLM
 ↓
Decision
```

Tools are therefore an important bridge from LangChain pipelines toward agentic systems.

Agents will be covered later in the roadmap in more detail.

---

# 44. Deterministic Chain vs Agent

A deterministic chain follows a predefined flow:

```text
A
 ↓
B
 ↓
C
 ↓
D
```

Example:

```text
Retriever
 ↓
Prompt
 ↓
LLM
```

An agent can decide what to do dynamically:

```text
           ┌→ Search Tool
Question → Agent → Calculator
           ├→ Database
           └→ Final Answer
```

This distinction becomes important later when learning LangGraph and Agents.

---

# 45. LangChain Mental Model

The complete conceptual picture:

```text
                    DATA
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
   Documents                 External Systems
        ↓                         ↓
     Loaders                     Tools
        ↓
  Text Splitters
        ↓
   Embeddings
        ↓
  Vector Stores
        ↓
    Retrievers
        │
        └────────────┐
                     ↓
                  Context
                     │
Question ────────────┤
                     ↓
             ChatPromptTemplate
                     ↓
                 Chat Model
                     ↓
        Parser / Structured Output
                     ↓
              Application Result
```

Runnables provide a standard execution interface for many components.

LCEL provides a composition mechanism for connecting them.

---

# 46. Core Distinctions to Remember

## Runnable vs LCEL

```text
Runnable
= executable building block

LCEL
= composition mechanism
```

---

## Vector Store vs Retriever

```text
Vector Store
= stores/searches vectors

Retriever
= query → relevant Documents
```

---

## PromptTemplate vs ChatPromptTemplate

```text
PromptTemplate
= formatted text prompt

ChatPromptTemplate
= role-based chat messages
```

---

## RunnableLambda vs RunnablePassthrough

```text
RunnableLambda
= transform input

RunnablePassthrough
= preserve input
```

---

## Output Parser vs Structured Output

```text
Output Parser
= process response after generation

Structured Output
= define output schema before generation
```

---

## Retriever vs Tool

```text
Retriever
= retrieval-specific abstraction

Tool
= generic external capability
```

---

## RAG vs LangChain

```text
RAG
= architecture pattern

LangChain
= framework that can implement RAG
```

---

# 47. Key Learning Takeaway

The most important takeaway from this chapter is not memorizing LangChain APIs.

It is understanding how familiar LLM application concepts map to standardized framework abstractions.

We already understand:

```text
Documents
Chunking
Embeddings
Vector Search
Retrieval
Prompts
LLMs
Reranking
Context
Evaluation
```

LangChain adds a framework layer:

```text
Documents
Loaders
Splitters
Embeddings
Vector Stores
Retrievers
Prompt Templates
Chat Models
Runnables
LCEL
Output Parsers
Structured Output
Tools
```

Therefore, when reading LangChain code, we should continuously ask:

> What underlying AI/application concept is this abstraction representing?

That keeps the framework understandable and prevents it from becoming a black box.

---

# 48. Next Step

The next step is to build one integrated LangChain CodeLab.

The goal is not to recreate every advanced RAG technique.

The goal is to understand how LangChain composes the core RAG workflow.

Target architecture:

```text
Documents
   ↓
Loader
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retriever
   ↓
RunnableLambda(format_docs)
   │
Question ── RunnablePassthrough
   │
   └─────────────┐
                 ↓
        ChatPromptTemplate
                 ↓
            Chat Model
                 ↓
          StrOutputParser
                 ↓
               Answer
```

During implementation, each LangChain abstraction should be compared directly with the equivalent component from our manual RAG CodeLab.
````
