# Context Managers - Quick Reference

# What is a Context Manager?

A Context Manager is an object that manages the lifecycle of a resource by automatically acquiring it before use and releasing it after use.

Python implements Context Managers using the **with** statement.

---

# Why do we need Context Managers?

Without Context Managers:

- Resources may not be released.
- File handles remain open.
- Database connections remain active.
- Locks may never be released.
- Memory and performance issues can occur.
- Exceptions can skip cleanup code.

Context Managers guarantee resource cleanup.

---

# Resource Lifecycle

```
Acquire Resource
       │
       ▼
Use Resource
       │
       ▼
Release Resource
```

---

# Context Manager Protocol

A class becomes a Context Manager by implementing:

```python
__enter__()

__exit__(exc_type, exc_value, traceback)
```

---

# with Statement

```python
with expression as variable:
    ...
```

Python automatically calls:

1. `__enter__()`
2. Executes the block
3. `__exit__()`

---

# Internal Execution Flow

```
Evaluate Expression
        │
        ▼
Create Context Manager
        │
        ▼
Call __enter__()
        │
        ▼
Assign returned object
        │
        ▼
Execute Block
        │
        ▼
Call __exit__()
        │
        ▼
Continue Execution
```

---

# __enter__()

Purpose:

- Acquire resource
- Initialize resource
- Validate resource
- Return object for use

Common Return Values:

- self
- underlying resource
- wrapper object
- proxy object

---

# __exit__()

Purpose:

- Cleanup resources
- Close files
- Release locks
- Commit/Rollback transactions
- Handle exceptions (optional)

Signature:

```python
def __exit__(self,
             exc_type,
             exc_value,
             traceback):
```

---

# Exception Parameters

| Parameter | Meaning |
|------------|---------|
| exc_type | Exception Class |
| exc_value | Exception Object |
| traceback | Stack Trace |

No exception:

```python
(None, None, None)
```

---

# Return Value of __exit__()

Return False

- Cleanup performed
- Exception propagates

Return True

- Cleanup performed
- Exception suppressed

Production Recommendation:

Return **False** unless suppressing an exception is intentional.

---

# Context Manager vs Returned Object

```
Context Manager

│
├── __enter__()
├── __exit__()
│
▼

Returns

▼

Object used inside with block
```

The returned object may or may not be the Context Manager itself.

---

# Mental Model

```python
with resource as obj:
    work(obj)
```

Conceptually behaves like:

```python
manager = resource

obj = manager.__enter__()

try:
    work(obj)
finally:
    manager.__exit__(...)
```

---

# Common Use Cases

- File Handling
- Database Transactions
- HTTP Sessions
- Network Sockets
- Locks
- Temporary Files
- Performance Timers
- Logging
- AI Model Sessions
- GPU Resources

---

# Production Examples

```python
with open(...)
```

```python
with sqlite3.connect(...)
```

```python
with requests.Session(...)
```

```python
with tempfile.TemporaryDirectory(...)
```

```python
with ThreadPoolExecutor(...)
```

---

# Common Mistakes

❌ Forgetting to use `with`

❌ Returning True from `__exit__()` unnecessarily

❌ Placing business logic inside Context Managers

❌ Assuming every object supports `with`

❌ Forgetting that `as variable` receives the return value of `__enter__()`

---

# Best Practices

✔ Keep Context Managers focused on resource lifecycle.

✔ Keep business logic outside Context Managers.

✔ Use `with` whenever deterministic cleanup is required.

✔ Propagate exceptions unless suppression is intentional.

✔ Design reusable Context Managers.

---

# Enterprise Applications

- Banking
- Payment Systems
- Healthcare
- Cloud Applications
- ETL Pipelines
- Distributed Systems
- Background Workers
- Microservices

---

# GenAI Applications

- PDF Processing
- Dataset Loading
- Vector Database Connections
- Temporary Embedding Files
- GPU Memory Management
- Model Loading
- Prompt Logging
- Batch Processing

---

# Interview Keywords

- Resource Lifecycle
- Deterministic Cleanup
- Context Manager Protocol
- `with` Statement
- `__enter__()`
- `__exit__()`
- Exception Propagation
- Exception Suppression
- RAII
- Resource Management

---

# One-Line Summary

> A Context Manager is an object implementing the Context Manager Protocol that guarantees deterministic resource acquisition and cleanup through Python's `with` statement.