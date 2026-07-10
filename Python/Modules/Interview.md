# Python Modules - Interview Questions

> **Topic:** Python Modules & Packages  
> **Category:** Python Fundamentals  
> **Difficulty:** Beginner → Architect  
> **Total Questions:** 50

---

# Introduction

This document contains curated interview questions covering the **Python Modules** topic.

The questions progress from fundamental concepts to advanced architectural discussions and production scenarios. Every question includes:

- Answer
- Interviewer's Expectation
- Common Mistakes
- Follow-up Questions

The goal is not to memorize answers but to understand the reasoning behind them.

---

# Question Distribution

| Section | Questions |
|----------|----------:|
| 1. Fundamental Questions | 10 |
| 2. Intermediate Questions | 10 |
| 3. Advanced Questions | 10 |
| 4. Architecture & Design Questions | 8 |
| 5. Production Scenario Questions | 5 |
| 6. GenAI Engineering Questions | 4 |
| 7. Coding Questions | 3 |

**Total Questions: 50**

---

# 1. Fundamental Questions

---

## Q1. What is a Python Module?

### Answer

A Python module is a single `.py` file containing related variables, functions, classes, constants, and executable statements. Modules improve code organization, reusability, maintainability, and separation of concerns.

### Interviewer's Expectation

The interviewer wants to verify that you understand the basic unit of code organization in Python.

### Common Mistakes

- Confusing modules with packages.
- Saying modules only contain functions.
- Ignoring executable statements.

### Follow-up Questions

- Why were modules introduced?
- Can modules contain classes?
- Can one module import another module?

---

## Q2. Why were Modules introduced?

### Answer

Modules solve several software engineering problems:

- Code organization
- Code reuse
- Separation of concerns
- Reduced duplication
- Easier maintenance
- Better collaboration

Without modules, applications would become difficult to maintain as they grow.

### Interviewer's Expectation

To assess whether you understand the engineering motivation behind modules.

### Common Mistakes

- Mentioning only code reuse.

### Follow-up Questions

- What problems arise without modules?
- How do modules improve team productivity?

---

## Q3. What can a Python module contain?

### Answer

A module can contain:

- Variables
- Constants
- Functions
- Classes
- Executable statements
- Imports
- Documentation

Everything defined at the module level belongs to that module's namespace.

### Interviewer's Expectation

To verify that you understand a module is more than just a collection of functions.

### Common Mistakes

- Forgetting executable statements.
- Thinking modules contain only functions.

### Follow-up Questions

- What is top-level code?
- When does module-level code execute?

---

## Q4. What is the difference between a Module and a Package?

### Answer

| Module | Package |
|---------|----------|
| Single `.py` file | Directory containing related modules |
| Smallest reusable unit | Collection of related modules |
| Contains Python code | Organizes modules and subpackages |

### Interviewer's Expectation

To evaluate whether you can distinguish between these two fundamental concepts.

### Common Mistakes

- Calling every directory a package.
- Confusing folders with Python packages.

### Follow-up Questions

- Can a package contain another package?
- What is `__init__.py`?

---

## Q5. What happens when Python executes an `import` statement?

### Answer

Python:

1. Checks `sys.modules`.
2. Returns the cached module if found.
3. Searches directories listed in `sys.path`.
4. Creates a module object.
5. Adds it to `sys.modules`.
6. Executes the module.
7. Returns the module object.

### Interviewer's Expectation

To evaluate your understanding of Python's import mechanism.

### Common Mistakes

- Forgetting `sys.modules`.
- Thinking Python always searches the filesystem first.

### Follow-up Questions

- Why is the module cached?
- Why is it added before execution?

---

## Q6. What is `__name__`?

### Answer

`__name__` is a built-in module variable.

- `"__main__"` when executed directly.
- Module name when imported.

It helps differentiate between execution and import.

### Interviewer's Expectation

To test understanding of module execution.

### Common Mistakes

- Assuming it is always `"__main__"`.

### Follow-up Questions

- Why use `if __name__ == "__main__"`?
- What happens when a module is imported?

---

## Q7. Why is `if __name__ == "__main__"` used?

### Answer

It ensures certain code executes only when the module is run directly, not when imported.

Typical uses:

- Testing
- Demonstrations
- Debugging
- CLI entry points

### Interviewer's Expectation

To verify understanding of reusable modules.

### Common Mistakes

- Using it for application logic.

### Follow-up Questions

- Can production modules use it?
- Why is it considered a best practice?

---

## Q8. What is module namespace?

### Answer

Every module has its own namespace containing variables, functions, classes, and imported objects defined within that module.

Namespaces prevent naming conflicts between modules.

### Interviewer's Expectation

To assess understanding of object organization.

### Follow-up Questions

- Can two modules have variables with the same name?
- How are namespaces isolated?

---

## Q9. How do you import specific functions from a module?

### Answer

```python
from math import sqrt
```

Or import the entire module:

```python
import math

math.sqrt(25)
```

Explicit imports are generally preferred over wildcard imports.

### Follow-up Questions

- What is a wildcard import?
- Why should wildcard imports be avoided?

---

## Q10. What is module documentation?

### Answer

Module documentation is typically provided using a module-level docstring.

Example:

```python
"""
Utilities for payment processing.
"""
```

It explains the module's purpose and is accessible through `help()`.

### Interviewer's Expectation

To verify awareness of documentation practices.

---

# 2. Intermediate Questions

**Questions Q11 – Q20**

Topics covered:

- `sys.path`
- `sys.modules`
- Module caching
- Module shadowing
- Lazy loading
- Absolute imports
- Relative imports
- `__init__.py`
- Package initialization
- Import search order

---

# 3. Advanced Questions

**Questions Q21 – Q30**

Topics covered:

- Circular imports
- Import internals
- Bytecode compilation
- Namespace packages
- Import hooks
- Dynamic imports
- Module execution lifecycle
- Memory considerations
- Performance optimization
- Python import architecture

---

# 4. Architecture & Design Questions

**Questions Q31 – Q38**

Topics covered:

- Package organization
- Dependency direction
- Single Responsibility Principle
- Public APIs
- Stable interfaces
- Layered architecture
- Modular design
- Enterprise project structure

---

# 5. Production Scenario Questions

**Questions Q39 – Q43**

Example topics:

- Designing package structures
- Refactoring circular dependencies
- Sharing configuration
- Lazy loading LLMs
- Debugging import failures

---

# 6. GenAI Engineering Questions

**Questions Q44 – Q47**

Example topics:

- Why module caching matters for LLMs
- Organizing RAG projects
- Packaging AI agents
- Structuring enterprise GenAI applications

---

# 7. Coding Questions

---

## Q48. Demonstrate module caching.

### Task

Create two modules and demonstrate that top-level code executes only once despite multiple imports.

---

## Q49. Build a package.

### Task

Create a package with multiple modules and expose a public API using `__init__.py`.

---

## Q50. Resolve a Circular Import.

### Task

Given two modules with circular dependencies:

- Explain why the error occurs.
- Refactor the code.
- Explain your architectural decisions.

---

# Self Assessment

Rate yourself honestly before marking this topic as complete.

| Area | Rating (1–5) |
|------|:------------:|
| Fundamentals | ⭐⭐⭐⭐⭐ |
| Import System | ⭐⭐⭐⭐⭐ |
| Packages | ⭐⭐⭐⭐⭐ |
| Module Cache | ⭐⭐⭐⭐⭐ |
| Architecture | ⭐⭐⭐⭐⭐ |
| Production Usage | ⭐⭐⭐⭐⭐ |
| GenAI Relevance | ⭐⭐⭐⭐⭐ |

---

# Completion Checklist

Mark this topic as complete only when:

- [ ] I can answer all interview questions without referring to notes.
- [ ] I understand Python's import system.
- [ ] I can explain module caching.
- [ ] I can explain package organization.
- [ ] I understand production usage.
- [ ] I can relate these concepts to GenAI applications.
- [ ] I have completed all exercises.
- [ ] I have reviewed the runnable code examples.

---

# Notes

This is a living document.

As new interview questions arise during future learning or mock interviews, they should be added to the appropriate section while preserving the overall structure.