# Example 1 - Core Module Concepts

## Overview

This example demonstrates the fundamental concepts of **Python Modules** using a small, easy-to-follow project.

Rather than showing isolated examples for each concept, this project combines multiple related concepts into a single runnable application. The goal is to observe how Python's import system behaves in practice.

---

# Learning Objectives

After completing this example, you should be able to:

- Create and import Python modules.
- Understand top-level code execution.
- Explain the purpose of `__name__`.
- Use `if __name__ == "__main__"` correctly.
- Explain why Python executes a module only once.
- Understand module caching using `sys.modules`.
- Observe how module state is shared across imports.
- Explain the order in which Python imports modules.

---

# Concepts Covered

- ✅ Creating Modules
- ✅ Import Statements
- ✅ Top-Level Code Execution
- ✅ `__name__`
- ✅ `if __name__ == "__main__"`
- ✅ Module Caching
- ✅ Shared Module State
- ✅ `sys.modules`
- ✅ Multiple Imports
- ✅ Import Execution Order

---

# Project Structure

```text
Example-1-Core-Concepts/
│
├── main.py
├── config.py
├── employee.py
└── README.md
```

---

# File Description

| File | Purpose |
|------|---------|
| **main.py** | Entry point of the application. Demonstrates module imports, caching, and shared state. |
| **config.py** | Configuration module used to demonstrate top-level execution, module caching, and shared variables. |
| **employee.py** | Imports another module, updates shared state, and demonstrates module interaction. |

---

# How to Run

Navigate to the example directory and execute:

```bash
python main.py
```

---

# Expected Output

```text
==================================================
Main Program Started
==================================================

Loading Configuration...
Configuration Loaded
__name__ = config
config.py imported as module

Loading Employee Module
Current Counter = 0
Counter Updated = 5
__name__ = employee
employee.py imported

Importing config again...

Counter : 5
Counter after update : 6

Is config cached?

True

Main Program Finished
```

> **Note:** The exact formatting may vary slightly depending on your Python version or any additional print statements you add during experimentation.

---

# Expected Learning Outcome

By the end of this example, you should understand:

- Why imported modules execute only once.
- How Python caches imported modules in `sys.modules`.
- Why module-level variables behave like shared state.
- The difference between executing a file directly and importing it.
- How the import order affects program execution.

---

# Things to Try

### Experiment 1 – Multiple Imports

Import `config` multiple times in `main.py`.

**Question**

Does `Loading Configuration...` print more than once?

---

### Experiment 2 – Execute a Module Directly

Run:

```bash
python config.py
```

Observe the value of:

```python
__name__
```

How is it different from importing the module?

---

### Experiment 3 – Execute Another Module

Run:

```bash
python employee.py
```

Observe:

- The execution order.
- The value of `__name__`.
- Which statements execute.

---

### Experiment 4 – Verify Shared Module State

Print the following in both `main.py` and `employee.py`:

```python
id(config)
```

**Question**

Is the object ID the same?

What does this tell you about module caching?

---

### Experiment 5 – Inspect Python's Module Cache

Add the following to `main.py`:

```python
import sys

print(sys.modules.keys())
```

Observe how many modules Python has already loaded before your application starts.

Can you find:

- `config`
- `employee`

inside the cache?

---

# Summary

This example demonstrates the core behavior of Python's module system in a practical and interactive way. It forms the foundation for understanding packages, imports, and application structure, which are essential concepts for building larger Python applications and future GenAI projects.