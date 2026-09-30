````md
# Why LangChain? — Storytelling

## The Starting Point

Imagine we are building an LLM application.

At first, the application is simple.

```text
User
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

We can write this easily with plain Python.

There is no need for a framework.

---

## The Application Starts Growing

Now the application needs retrieval.

```text
User Question
      ↓
Retriever
      ↓
Documents
      ↓
Prompt
      ↓
LLM
      ↓
Answer
```

Still manageable.

We write:

```python
documents = retriever.search(question)

context = format_documents(documents)

prompt = build_prompt(
    context=context,
    question=question
)

response = model.generate(prompt)
```

This works.

---

## More Requirements Arrive

Now the product team asks for:

- Vector search
- Keyword search
- Multiple LLM providers
- Streaming
- Async execution
- Structured output
- External APIs
- Database tools
- Reusable chains
- Different prompt templates
- Different retrievers

Our application starts looking like:

```text
                   User Question
                         │
               Query Processing
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
       Vector Search            Keyword Search
             ↓                       ↓
             └───────────┬───────────┘
                         ↓
                    Documents
                         ↓
                  Format Context
                         ↓
                      Prompt
                         ↓
                       LLM
                         ↓
                  Output Parsing
                         ↓
                Application Result
```

And some requests may also require:

```text
Database
API
Calculator
Search
Other Internal Services
```

At this point, the problem is no longer only:

> How do I call an LLM?

The new problem becomes:

> How do I organize and connect all these components?

---

# The Manual Approach

Without a framework, every component may have a different interface.

Imagine:

```python
prompt.format(...)
model.generate(...)
retriever.search(...)
parser.parse(...)
vector_store.similarity_search(...)
```

Each component behaves differently.

We then manually connect them:

```python
docs = retriever.search(question)

context = format_docs(docs)

prompt_text = prompt.format(
    context=context,
    question=question
)

response = model.generate(prompt_text)

answer = parser.parse(response)
```

There is nothing wrong with this.

In fact, for small applications this may be the best approach.

But as the system grows, orchestration code becomes larger.

---

# The LangChain Idea

LangChain introduces standard abstractions around common LLM application components.

Instead of thinking about:

```text
Different APIs
Different calling styles
Different providers
Different execution methods
```

LangChain tries to make components behave more consistently.

Conceptually:

```text
Input
 ↓
Runnable
 ↓
Output
```

Many components follow the same execution model.

For example:

```text
Prompt
Model
Retriever
Parser
Custom Function
```

can participate in Runnable pipelines.

---

# Enter Runnable

A Runnable is essentially LangChain saying:

> If something can receive input and produce output, let's give it a common execution interface.

Conceptually:

```python
component.invoke(input)
```

Now different components can be treated more uniformly.

```text
Prompt
 ↓
invoke()

Model
 ↓
invoke()

Retriever
 ↓
invoke()

Parser
 ↓
invoke()
```

This makes composition easier.

---

# Enter LCEL

Once components behave like Runnables, LangChain needs a convenient way to connect them.

That is where LCEL comes in.

LCEL stands for:

**LangChain Expression Language**

Instead of manually writing:

```python
prompt_value = prompt.invoke(data)

response = model.invoke(prompt_value)

answer = parser.invoke(response)
```

we can write:

```python
chain = prompt | model | parser
```

Conceptually:

```text
Prompt
  ↓
Model
  ↓
Parser
```

The output of one Runnable becomes the input of the next.

So the mental model is:

```text
Runnable
= building block

LCEL
= way to connect the building blocks
```

---

# Now Add RAG

Suppose we want to build a RAG pipeline.

We need two things from the same question:

1. Use it to retrieve context.
2. Keep the original question for the prompt.

Conceptually:

```text
                  Question
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
      Retriever          Original Question
          ↓
       Documents
          ↓
     Format Context
          ↓
        Context
          └──────────┬──────────┘
                     ↓
                   Prompt
                     ↓
                    LLM
                     ↓
                   Answer
```

LangChain provides components such as:

```text
Retriever
RunnableLambda
RunnablePassthrough
ChatPromptTemplate
Chat Model
Output Parser
```

to compose this workflow.

---

# RunnablePassthrough Story

Imagine the user's question is:

```text
How long was Treatment C?
```

We send it to the Retriever.

```text
Question
 ↓
Retriever
 ↓
Documents
```

But after retrieval, we still need the original question.

Instead of manually storing and forwarding it everywhere, LangChain can use:

```text
RunnablePassthrough
```

Conceptually:

```text
Question
   │
   ├── Retriever → Context
   │
   └── Passthrough → Question
```

The same input travels through two branches.

---

# RunnableLambda Story

The Retriever returns:

```python
[
    Document(...),
    Document(...),
    Document(...)
]
```

But the prompt expects something like:

```text
Context:

Treatment C lasted 36 months.

The primary success criterion...
```

So we need a normal Python transformation.

```python
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )
```

LangChain can wrap this function using:

```text
RunnableLambda
```

Now our custom Python code becomes part of the Runnable pipeline.

```text
Documents
 ↓
RunnableLambda
 ↓
Context String
```

---

# PromptTemplate Story

In our manual RAG implementation, we built prompt strings ourselves.

For example:

```text
Answer only from the context.

Context:
...

Question:
...
```

LangChain provides prompt abstractions so that the structure becomes reusable.

```text
Template
+
Variables
 ↓
Final Prompt
```

For chat models, `ChatPromptTemplate` also preserves roles.

```text
System
 ↓
Human
 ↓
Chat Model
```

---

# Retriever Story

Suppose today we use vector search.

```text
Retriever
 ↓
Vector Store
```

Tomorrow we decide to use:

```text
BM25
```

or:

```text
Hybrid Search
```

or:

```text
Internal Enterprise Search API
```

If the rest of our application depends only on the Retriever contract:

```text
Query
 ↓
Relevant Documents
```

then we can replace the underlying implementation more easily.

This is the value of abstraction.

---

# Output Parser Story

Models often return objects such as:

```python
AIMessage(
    content="Treatment C lasted 36 months."
)
```

But our application may only need:

```python
"Treatment C lasted 36 months."
```

An Output Parser handles the response after generation.

```text
Model
 ↓
AIMessage
 ↓
Parser
 ↓
Application Value
```

---

# Structured Output Story

Now imagine we are not building only a chatbot.

An API needs:

```json
{
    "study_id": "STUDY-003",
    "duration_months": 36
}
```

A free-form answer such as:

```text
Treatment C lasted approximately 36 months.
```

is inconvenient for application logic.

So instead we define a response contract.

```python
class StudyResult(BaseModel):
    study_id: str
    duration_months: int
```

Now the model is configured around that expected structure.

This is Structured Output.

The simple distinction is:

```text
Output Parser
= what should I do with the response?

Structured Output
= what shape should the response have?
```

---

# Tools Story

Eventually the application needs real-world capabilities.

The model may need to:

```text
Check study status
Query a database
Call an API
Perform a calculation
Search internal research
```

The LLM cannot directly execute our backend code.

Instead, we expose capabilities as Tools.

Conceptually:

```text
User
 ↓
LLM / Agent
 ↓
"I need study status"
 ↓
Tool Call
 ↓
Backend Function
 ↓
Tool Result
 ↓
LLM
 ↓
Answer
```

The actual business logic remains in the application.

The LLM chooses or requests the capability.

---

# The Important Architectural Boundary

LangChain should not become the place where all business rules live.

For example:

```text
Authorization
Business Validation
Clinical Rules
Security
Database Transactions
Critical Threshold Logic
```

should remain deterministic application logic.

The LLM and LangChain orchestration should operate inside those boundaries.

Example:

```text
User
 ↓
Authentication
 ↓
Authorization
 ↓
Allowed Data
 ↓
LangChain Retrieval Pipeline
 ↓
LLM
```

Not:

```text
Retrieve All Data
 ↓
LLM
 ↓
"Please decide what this user is allowed to see"
```

---

# So Why Does LangChain Exist?

LangChain exists because modern LLM applications are often not just:

```text
Prompt → LLM
```

They become:

```text
Prompts
Models
Retrievers
Vector Stores
Documents
Tools
Structured Outputs
Custom Functions
Streaming
Async Processing
External Systems
```

LangChain provides common abstractions and composition mechanisms for organizing these parts.

---

# But Do We Always Need LangChain?

No.

Imagine this application:

```python
response = model.invoke(
    "Summarize this text."
)
```

Adding:

```text
LangChain
Runnables
LCEL
Custom Chains
Multiple abstractions
```

may be unnecessary.

Plain Python may be clearer.

---

# When LangChain Starts Making Sense

LangChain becomes more useful when we need:

```text
Multiple Components
      +
Reusable Pipelines
      +
Retrieval
      +
Structured Output
      +
Tools
      +
Streaming
      +
Async Workflows
```

At this point, common abstractions reduce repetitive orchestration.

---

# The Framework Trap

There is one important danger.

Someone may learn LangChain first and think:

```python
vector_store.as_retriever()
```

means they understand retrieval.

But they may not understand:

```text
Top-K
Similarity
Chunking
Metadata Filtering
Authorization
Reranking
Recall
Precision
```

This is why we intentionally built RAG manually first.

Now when we see:

```python
retriever = vector_store.as_retriever()
```

we know what kind of work is hidden behind that abstraction.

---

# Our Learning Story

Our learning path is therefore:

```text
Understand the Problem
        ↓
Build the Concepts Manually
        ↓
Understand the Architecture
        ↓
Learn LangChain Abstractions
        ↓
Use LangChain Where It Helps
```

Not:

```text
Install LangChain
      ↓
Copy Framework Code
      ↓
Hope It Works
```

---

# Final Mental Story

Imagine building a house.

The underlying engineering concepts are:

```text
Foundation
Structure
Electrical
Plumbing
Materials
Safety
```

LangChain is not the house and it is not the engineering knowledge.

It is closer to a **construction framework and set of standardized connectors** that help different parts work together.

If the foundation is bad, the framework cannot save the building.

Similarly:

```text
Bad Chunking
Bad Retrieval
Bad Authorization
Bad Prompting
Bad Evaluation
```

will still produce a bad LLM application.

LangChain simply makes the components easier to organize and compose.

---

# One-Minute Story

If someone asks:

> Why does LangChain exist?

A concise explanation is:

LangChain exists because production LLM applications usually involve much more than calling a model. They combine prompts, retrievers, documents, vector stores, structured outputs, tools, and external services. Without a framework, developers must manually orchestrate these components using different interfaces. LangChain provides standardized abstractions such as Runnables and composition mechanisms such as LCEL, making complex LLM pipelines easier to organize and reuse. However, it does not replace understanding of the underlying concepts such as retrieval, chunking, embeddings, security, or evaluation.

---

# Final Takeaway

Remember:

```text
LangChain is NOT the intelligence.

LangChain is NOT RAG.

LangChain is NOT an agent.

LangChain is NOT required for every LLM app.
```

LangChain is:

```text
A framework
     ↓
that standardizes
     ↓
LLM application components
     ↓
and helps compose them
     ↓
into reusable workflows
```

The most useful question when reading LangChain code is:

> What underlying component or piece of orchestration is this abstraction representing?
````
