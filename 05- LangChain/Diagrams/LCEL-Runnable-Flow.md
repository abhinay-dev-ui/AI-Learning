````md
# LCEL and Runnable Flow — Diagram

## 1. Runnable Mental Model

A Runnable is an executable LangChain component.

```text
Input
  │
  ▼
Runnable
  │
  ▼
Output
```

Examples:

```text
Prompt
Model
Retriever
Output Parser
RunnableLambda
RunnablePassthrough
```

---

## 2. Runnable Execution

A Runnable can commonly support:

```text
invoke()
batch()
stream()
ainvoke()
abatch()
```

Conceptually:

```text
                 Runnable
                    │
      ┌─────────────┼─────────────┐
      │             │             │
      ▼             ▼             ▼
   invoke()       batch()       stream()
      │             │             │
      ▼             ▼             ▼
Single Input   Multiple Inputs   Incremental
Single Output  Multiple Outputs     Output
```

---

## 3. LCEL Mental Model

LCEL stands for:

**LangChain Expression Language**

It connects Runnables.

```python
chain = prompt | model | parser
```

Conceptually:

```text
Input
  │
  ▼
Prompt
  │
  ▼
Model
  │
  ▼
Parser
  │
  ▼
Output
```

---

## 4. Runnable vs LCEL

```text
Runnable
= executable building block
```

```text
LCEL
= way to compose building blocks
```

Visual:

```text
Runnable A
    │
    │
    ▼
Runnable B
    │
    │
    ▼
Runnable C
```

LCEL representation:

```python
A | B | C
```

---

## 5. Composition Creates Another Runnable

This is an important concept.

```text
Runnable A
    +
Runnable B
    +
Runnable C
       │
       ▼
     LCEL
       │
       ▼
Combined Runnable
```

So:

```python
chain = A | B | C
```

can itself be called:

```python
chain.invoke(input)
```

---

## 6. Basic LCEL Execution

Example:

```python
chain = prompt | model | parser
```

Execution:

```text
Input Dictionary
       │
       ▼
Prompt Runnable
       │
       ▼
Prompt Value
       │
       ▼
Model Runnable
       │
       ▼
AIMessage
       │
       ▼
Parser Runnable
       │
       ▼
Python String
```

---

## 7. RunnablePassthrough

`RunnablePassthrough` preserves the input.

```text
Input
  │
  ▼
RunnablePassthrough
  │
  ▼
Same Input
```

Example:

```text
Question
   │
   ▼
Passthrough
   │
   ▼
Question
```

No transformation happens.

---

## 8. RunnableLambda

`RunnableLambda` executes custom Python logic.

```text
Input
  │
  ▼
RunnableLambda
  │
  ▼
Python Function
  │
  ▼
Transformed Output
```

Example:

```text
Documents
    │
    ▼
RunnableLambda(format_docs)
    │
    ▼
Context String
```

---

## 9. RunnableLambda vs RunnablePassthrough

```text
RunnableLambda
Input
  ↓
Transform
  ↓
New Output
```

```text
RunnablePassthrough
Input
  ↓
No Change
  ↓
Same Input
```

Remember:

```text
Lambda
= transform

Passthrough
= preserve
```

---

## 10. Branching Flow

Suppose the input question is:

```text
How long was Treatment C?
```

We need:

- Context
- Original question

So we branch:

```text
                         Question
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
             Retriever         RunnablePassthrough
                 │                     │
                 ▼                     ▼
             Documents             Question
                 │
                 ▼
          RunnableLambda
           format_docs()
                 │
                 ▼
              Context
```

Now we have:

```text
{
    "context": "...",
    "question": "How long was Treatment C?"
}
```

This can be sent to a prompt.

---

## 11. Full RAG Runnable Flow

```text
                            INPUT
                              │
                              ▼
                           Question
                              │
                   ┌──────────┴──────────┐
                   │                     │
                   ▼                     ▼
               Retriever         RunnablePassthrough
                   │                     │
                   ▼                     ▼
               Documents             Question
                   │
                   ▼
            RunnableLambda
             format_docs()
                   │
                   ▼
                Context
                   │
                   └──────────┬──────────┘
                              ▼
                    ChatPromptTemplate
                              │
                              ▼
                         Chat Model
                              │
                              ▼
                      StrOutputParser
                              │
                              ▼
                            Answer
```

---

## 12. Data Transformation Through the Chain

### Step 1

Input:

```python
"How long was Treatment C?"
```

---

### Step 2

Retriever output:

```python
[
    Document(
        page_content="Treatment C lasted 36 months."
    )
]
```

---

### Step 3

RunnableLambda output:

```text
Treatment C lasted 36 months.
```

---

### Step 4

RunnablePassthrough output:

```text
How long was Treatment C?
```

---

### Step 5

Combined input:

```python
{
    "context": "Treatment C lasted 36 months.",
    "question": "How long was Treatment C?"
}
```

---

### Step 6

ChatPromptTemplate output:

```text
System:
Answer only from the provided context.

Human:
Context:
Treatment C lasted 36 months.

Question:
How long was Treatment C?
```

---

### Step 7

Model output:

```python
AIMessage(
    content="Treatment C lasted 36 months."
)
```

---

### Step 8

StrOutputParser output:

```python
"Treatment C lasted 36 months."
```

---

## 13. Sequential vs Branching Composition

### Sequential

```text
A
 ↓
B
 ↓
C
```

LCEL:

```python
A | B | C
```

---

### Branching

```text
        Input
       /     \
      /       \
     A         B
      \       /
       \     /
        Merge
```

RAG commonly needs branching because the same question is used for multiple purposes.

---

## 14. Why Runnable Composition Matters

Without composition:

```python
prompt_value = prompt.invoke(data)

model_response = model.invoke(prompt_value)

result = parser.invoke(model_response)
```

With LCEL:

```python
chain = prompt | model | parser

result = chain.invoke(data)
```

The goal is not only fewer lines of code.

It gives the pipeline a consistent execution abstraction.

That becomes useful for:

```text
Streaming
Batch execution
Async execution
Composition
Reuse
Tracing
Testing
```

---

## 15. Runnable Hierarchy Mental Model

```text
                    Runnable
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
     Prompt          Model         Retriever
        │              │              │
        ▼              ▼              ▼
RunnableLambda   Output Parser   Passthrough
        │
        ▼
Custom Logic
```

Many different components can participate in the same execution model.

---

## 16. LCEL Pipeline Mental Model

```text
                     INPUT
                       │
                       ▼
                  Runnable A
                       │
                       ▼
                  Runnable B
                       │
                       ▼
                  Runnable C
                       │
                       ▼
                    OUTPUT
```

represented as:

```python
A | B | C
```

---

## 17. Most Important Distinction

```text
Runnable
= What can execute?
```

```text
LCEL
= How are executable components connected?
```

---

## 18. Final Runnable + LCEL Mental Model

```text
Components
   │
   ├── Prompt
   ├── Model
   ├── Retriever
   ├── Parser
   ├── Lambda
   └── Passthrough
          │
          ▼
      All behave as
        Runnables
          │
          ▼
      Compose using
          LCEL
          │
          ▼
      Runnable Chain
          │
          ▼
       invoke()
       batch()
       stream()
       ainvoke()
```

---

## Final Takeaway

Remember the simplest explanation:

```text
Runnable
= executable component

LCEL
= composition mechanism

LCEL Chain
= composed Runnable
```

Example:

```python
chain = prompt | model | parser

result = chain.invoke(input)
```

That is the core relationship between Runnable and LCEL.
````
