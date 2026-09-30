````md
# LangChain — Interview Questions

## 1. What is LangChain?

LangChain is a framework for building LLM applications by providing standardized abstractions for:

- Prompts
- Models
- Documents
- Retrievers
- Vector stores
- Output handling
- Tools
- Workflow composition

It helps developers organize and compose these components into reusable pipelines.

LangChain itself does not provide the intelligence. The intelligence comes from the underlying LLMs, embedding models, retrievers, and external systems.

---

## 2. Why use LangChain?

LangChain is useful when an application contains multiple LLM-related components that need to be composed together.

For example:

```text
User Query
    ↓
Retriever
    ↓
Prompt
    ↓
LLM
    ↓
Output Parser
```

Instead of manually wiring every component, LangChain provides common interfaces and composition mechanisms.

Benefits include:

- Standardized interfaces
- Easier component composition
- Provider abstraction
- Reusable pipelines
- Streaming and async support
- Retriever integration
- Tool integration
- Structured output support

---

## 3. Does LangChain replace RAG?

No.

RAG is an architecture pattern.

LangChain is a framework that can help implement a RAG pipeline.

```text
RAG
= architecture/pattern

LangChain
= framework that can implement the pattern
```

You can build RAG without LangChain, as we did in our manual RAG CodeLab.

---

## 4. What is a LangChain Document?

A `Document` represents content together with metadata.

Example:

```python
Document(
    page_content="Treatment C lasted 36 months.",
    metadata={
        "study_id": "STUDY-003"
    }
)
```

Conceptually:

```text
Document
├── page_content
└── metadata
```

Metadata can later support filtering, authorization, citations, source tracking, and retrieval.

---

## 5. What is a Document Loader?

A Document Loader reads data from an external source and converts it into LangChain `Document` objects.

Examples of sources:

- Text files
- PDFs
- CSV
- Web pages
- Databases
- External services

Flow:

```text
Source
  ↓
Loader
  ↓
Documents
```

---

## 6. What is a Text Splitter?

A Text Splitter divides large documents into smaller chunks suitable for embeddings and retrieval.

```text
Document
   ↓
Text Splitter
   ↓
Chunks
```

Chunking strategy is still important even when LangChain is used.

LangChain provides the abstraction, but the developer still needs to choose:

- Chunk size
- Overlap
- Sentence-aware splitting
- Semantic splitting
- Structure-aware splitting

---

## 7. What are Embeddings in LangChain?

Embeddings convert text into numerical vectors that represent semantic meaning.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

LangChain provides a common interface around different embedding providers.

This allows the application to change embedding implementations without changing the entire pipeline.

---

## 8. What is a Vector Store?

A Vector Store stores embeddings and performs similarity search.

Examples include:

- FAISS
- Chroma
- Pinecone
- Qdrant
- Weaviate

Flow:

```text
Documents
    ↓
Embeddings
    ↓
Vector Store
    ↓
Similarity Search
```

---

## 9. What is a Retriever?

A Retriever is an abstraction that accepts a query and returns relevant documents.

```text
Query
  ↓
Retriever
  ↓
Documents
```

The retrieval mechanism may internally use:

- Vector search
- BM25
- Hybrid retrieval
- APIs
- Databases
- Custom search logic

The rest of the application does not need to know how retrieval is implemented.

---

## 10. Retriever vs Vector Store

A Vector Store is responsible for storing and searching embeddings.

A Retriever is a higher-level interface that returns relevant documents.

```text
Vector Store
= storage + similarity search

Retriever
= query → relevant Documents
```

A Retriever may use a Vector Store internally, but it does not have to.

---

## 11. What is PromptTemplate?

`PromptTemplate` creates reusable prompts with dynamic variables.

Example:

```python
PromptTemplate.from_template(
    """
    Context:
    {context}

    Question:
    {question}
    """
)
```

It produces a formatted text prompt.

---

## 12. PromptTemplate vs ChatPromptTemplate

`PromptTemplate` creates a single formatted text prompt.

`ChatPromptTemplate` creates structured chat messages with roles.

Example:

```text
System Message
      ↓
Human Message
      ↓
Chat Model
```

For modern chat models, `ChatPromptTemplate` is generally more natural because system and user instructions remain separated.

---

## 13. What is a Runnable?

A Runnable is a LangChain component that follows a standard execution interface.

Conceptually:

```text
Input
  ↓
Runnable
  ↓
Output
```

Common methods include:

```python
invoke()
batch()
stream()
ainvoke()
```

Examples of components that behave as Runnables:

- Prompt templates
- Chat models
- Output parsers
- Retrievers
- RunnableLambda
- RunnablePassthrough
- Composed chains

---

## 14. What is LCEL?

LCEL stands for:

**LangChain Expression Language**

It is the syntax used to compose Runnable components.

Example:

```python
chain = prompt | model | parser
```

The output of one Runnable becomes the input of the next.

---

## 15. Runnable vs LCEL

They are related but not the same.

```text
Runnable
= executable building block

LCEL
= composition syntax for connecting Runnables
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

The `|` composition is LCEL.

The resulting chain is itself also a Runnable.

---

## 16. Why is LCEL useful?

LCEL provides a consistent way to compose LLM application components.

Instead of manually writing:

```python
prompt_value = prompt.invoke(data)
model_response = model.invoke(prompt_value)
result = parser.invoke(model_response)
```

we can compose:

```python
chain = prompt | model | parser
result = chain.invoke(data)
```

This improves:

- Readability
- Reusability
- Composition
- Streaming support
- Async execution
- Pipeline consistency

---

## 17. What is RunnablePassthrough?

`RunnablePassthrough` forwards an input without changing it.

It is useful when the same input needs to be preserved while another branch transforms it.

Example in RAG:

```text
             Question
              /    \
             /      \
      Retriever   Passthrough
          ↓            ↓
       Context      Question
```

The retriever uses the question for search while the original question is preserved for the final prompt.

---

## 18. What is RunnableLambda?

`RunnableLambda` wraps a normal Python function and makes it usable inside a Runnable pipeline.

Example:

```python
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )
```

This function can be wrapped and inserted into LCEL.

Conceptually:

```text
Documents
    ↓
RunnableLambda(format_docs)
    ↓
Context String
```

---

## 19. RunnableLambda vs RunnablePassthrough

```text
RunnableLambda
= transform/process the input

RunnablePassthrough
= forward input unchanged
```

Example:

```text
Question
   ├── Retriever → Documents → Lambda → Context
   │
   └── Passthrough → Original Question
```

---

## 20. What is an Output Parser?

An Output Parser processes the response returned by a model.

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

Example chain:

```python
chain = prompt | model | StrOutputParser()
```

Output parsers can also transform model-generated JSON or other formats into application-friendly objects.

---

## 21. What is Structured Output?

Structured Output defines the expected response schema before the model is called.

Example:

```python
class StudyResult(BaseModel):
    duration_months: int
```

Then:

```python
structured_model = model.with_structured_output(
    StudyResult
)
```

The application expects a structured result rather than arbitrary free-form text.

---

## 22. Output Parser vs Structured Output

An Output Parser processes the model response after generation.

Structured Output defines the expected response contract before generation.

```text
Output Parser
= post-processing

Structured Output
= output contract/schema
```

Example:

```text
Output Parser

Model
  ↓
Generated Response
  ↓
Parser
  ↓
Application Object
```

versus:

```text
Structured Output

Schema
  ↓
Model
  ↓
Structured Object
```

---

## 23. What is a Tool in LangChain?

A Tool is a callable capability that an LLM or agent can use.

Examples:

- Calculator
- REST API
- Database query
- Search
- Retriever
- Internal business service

A tool normally contains:

```text
Name
Description
Input Schema
Implementation
```

The description helps the model understand when the tool should be used.

---

## 24. Retriever vs Tool

A Retriever has a specific purpose:

```text
Query → Relevant Documents
```

A Tool is a generic callable capability.

```text
Input → Function/API/System → Result
```

A Retriever can itself be exposed as a Tool when used by an agent.

---

## 25. What is the role of Tools in Agents?

Tools allow an agent to perform actions or retrieve information outside the LLM.

Example:

```text
User
  ↓
Agent
  ↓
Decides to call tool
  ↓
Database Tool
  ↓
Result
  ↓
Agent
  ↓
Final Response
```

Without Tools, the model can only reason over the information already available in its context.

---

## 26. Does the LLM execute a Tool itself?

No.

The LLM usually generates a tool-call request.

The application or agent runtime executes the actual function.

```text
LLM
 ↓
"Call get_study_status(STUDY-003)"
 ↓
Application Runtime
 ↓
Actual Function/API
 ↓
Result
 ↓
LLM
```

The business implementation remains outside the model.

---

## 27. What is the advantage of LangChain's abstractions?

The main advantage is loose coupling.

For example, an application can depend on the Retriever abstraction rather than directly depending on a specific Vector Store.

```text
Application
    ↓
Retriever Interface
    ↓
FAISS / Chroma / BM25 / API / Custom Search
```

This improves modularity and makes components easier to replace.

---

## 28. What are the disadvantages of LangChain?

Potential disadvantages include:

- Additional abstraction
- Framework complexity
- Version/API changes
- Harder debugging when abstractions hide behavior
- Unnecessary overhead for simple applications
- Developers may use components without understanding the underlying concepts

For small LLM applications, plain Python may sometimes be simpler.

---

## 29. When would you avoid LangChain?

LangChain may not be necessary when:

- The workflow is very small
- Only one or two model calls are required
- The application has simple custom orchestration
- Framework abstractions create more complexity than value
- Very strict low-level control is required

Example:

```text
Prompt
  ↓
LLM
  ↓
Response
```

may not require a framework.

---

## 30. When is LangChain useful?

LangChain becomes useful when the application contains multiple interacting components such as:

```text
Retrieval
Prompting
Multiple models
Structured output
Tools
Branching
Streaming
Async processing
External integrations
```

The benefit increases as the orchestration becomes more complex.

---

## 31. Does LangChain automatically make RAG better?

No.

LangChain does not automatically fix:

- Poor chunking
- Poor embeddings
- Wrong retrieval
- Bad metadata
- Authorization problems
- Hallucination
- Bad prompts
- Low-quality evaluation

A poorly designed RAG pipeline remains poorly designed even if LangChain is used.

---

## 32. How would you build a basic RAG pipeline using LangChain?

Conceptually:

```text
Documents
   ↓
Document Loader
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retriever
   ↓
Context Formatting
   ↓
ChatPromptTemplate
   ↓
Chat Model
   ↓
Output Parser
   ↓
Answer
```

LCEL can compose much of the online pipeline.

---

## 33. How does LangChain compare to a manual RAG implementation?

Manual implementation gives complete control and helps understand the underlying behavior.

LangChain provides abstractions around many of those components.

```text
Manual RAG                LangChain

Document model        →   Document
Loader                →   Document Loader
Chunker               →   Text Splitter
Embedding service     →   Embeddings
Vector store          →   Vector Store
Retriever             →   Retriever
Prompt builder        →   PromptTemplate
LLM service           →   Chat Model
Custom functions      →   RunnableLambda
Manual orchestration  →   LCEL
Response conversion   →   Output Parser
```

Understanding the manual implementation first makes it easier to understand what LangChain is actually abstracting.

---

## 34. What is the most important mental model for LangChain?

Think of LangChain as:

```text
LLMs + Retrieval + Prompts + Tools
              ↓
       Standard Interfaces
              ↓
          Runnables
              ↓
             LCEL
              ↓
       LLM Application
```

LangChain organizes and orchestrates LLM application components.

It does not replace the need to understand the underlying AI architecture.

---

# Rapid-Fire Interview Answers

## What is LangChain?

> LangChain is a framework that provides abstractions and composition mechanisms for building applications using LLMs, prompts, retrieval, tools, and external systems.

---

## What is a Runnable?

> A Runnable is a standard executable LangChain component that accepts input, performs an operation, and produces output.

---

## What is LCEL?

> LCEL is LangChain Expression Language, the syntax used to compose Runnable components into executable pipelines.

---

## Runnable vs LCEL?

> Runnable is the executable building block; LCEL is the mechanism used to compose those building blocks.

---

## Retriever vs Vector Store?

> A Vector Store stores and searches embeddings, while a Retriever is the interface that accepts a query and returns relevant documents.

---

## RunnableLambda vs RunnablePassthrough?

> RunnableLambda executes custom transformation logic, while RunnablePassthrough forwards the input unchanged.

---

## Output Parser vs Structured Output?

> An Output Parser processes a model response after generation, while Structured Output defines the expected response schema up front.

---

## Retriever vs Tool?

> A Retriever specifically returns relevant documents, while a Tool is a generic callable capability such as an API, database function, calculator, or retriever.

---

## Does LangChain perform AI itself?

> No. LangChain orchestrates AI-related components. The actual intelligence comes from LLMs, embedding models, rerankers, and retrieval systems.

---

## Why use LangChain after learning manual RAG?

> Building RAG manually helps understand the underlying architecture. LangChain can then be understood as an abstraction layer that standardizes and composes those same components rather than hiding concepts we do not understand.

---

# Final Interview Mental Model

```text
Data
 ↓
Documents
 ↓
Load / Split
 ↓
Embeddings
 ↓
Vector Store
 ↓
Retriever
 ↓
Context
 ↓
Prompt
 ↓
Model
 ↓
Parser / Structured Output
 ↓
Application Response

            +

Tools
 ↓
External capabilities

            +

Runnable
= executable component

LCEL
= composition mechanism
```
````
