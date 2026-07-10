# Python Modules - Quick Reference

> *"Master the import system, and you'll understand the foundation of every Python application."*

---

# Document Information

| Property | Value |
|----------|-------|
| **Version** | 1.0 |
| **Last Updated** | 10-Jul-2026 |
| **Maintained By** | Abhinay |
| **Category** | Python Fundamentals |
| **Topic** | Modules |
| **Level** | Beginner → Intermediate |
| **Interview Importance** | ⭐⭐⭐⭐⭐ |
| **Production Relevance** | ⭐⭐⭐⭐⭐ |
| **GenAI Relevance** | ⭐⭐⭐⭐⭐ |

---

# 1. Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| **Module** | A single Python file containing code. | `math.py`, `employee.py` |
| **Package** | A directory containing related modules. | `utils/`, `services/` |
| **Import** | Makes code from another module available. | `import math` |
| **Package Initialization** | Code executed when a package is imported. | `__init__.py` |

---

# 2. Import Styles

| Syntax | Purpose |
|---------|---------|
| `import math` | Import entire module |
| `import math as m` | Module alias |
| `from math import sqrt` | Import specific object |
| `from math import *` | Import everything *(Avoid)* |

💡 **Best Practice**

Prefer:

```python
import math

math.sqrt(25)
```

or

```python
from math import sqrt

sqrt(25)
```

Avoid:

```python
from math import *
```

---

# 3. Import Execution Flow

```text
import employee
        │
        ▼
Check sys.modules
        │
   ┌────┴─────┐
   │          │
Found?       Not Found
   │          │
Return     Search sys.path
Cached         │
Module         ▼
         Create Module Object
                 │
                 ▼
      Add to sys.modules
                 │
                 ▼
       Execute Module Code
                 │
                 ▼
          Return Module
```

---

# 4. `sys.path`

## Purpose

List of locations Python searches while importing modules.

## Search Order

```text
Current Directory
        ↓
PYTHONPATH
        ↓
Standard Library
        ↓
site-packages
```

Example

```python
import sys

print(sys.path)
```

⚠️ **Common Mistake**

Naming your file:

```text
os.py
math.py
json.py
```

This shadows Python's standard library modules.

---

# 5. `sys.modules`

## Purpose

Python's module cache.

Every imported module is stored here.

```python
import sys

print(sys.modules.keys())
```

Flow

```text
Import

↓

Already Cached?

│

├── Yes → Return Cached Module

│

└── No

↓

Execute Module

↓

Cache Module

↓

Return Module
```

💡 **Remember**

A module executes **only once** per Python process.

---

# 6. `__name__`

Every module has a special variable.

```python
print(__name__)
```

When executed directly:

```text
__main__
```

When imported:

```text
module_name
```

---

# 7. `if __name__ == "__main__"`

Purpose

Run code **only when the file is executed directly**.

```python
def main():
    print("Application Started")

if __name__ == "__main__":
    main()
```

Use for

- Testing
- Demo code
- CLI applications

---

# 8. Packages & `__init__.py`

Package

```text
company/

employee/

finance/

__init__.py
```

Purpose of `__init__.py`

- Marks a directory as a package
- Package initialization
- Export public APIs
- Package metadata

Example

```python
from .employee import Employee
```

---

# 9. Absolute vs Relative Imports

| Absolute | Relative |
|------------|-----------|
| Starts from root package | Starts from current package |
| Easy to read | Easier to move packages |
| Preferred across packages | Preferred within same package |

Example

Absolute

```python
from app.services.email import send_email
```

Relative

```python
from .email import send_email
```

---

# 10. Circular Imports

Problem

```text
A imports B

↓

B imports A

↓

Partially Initialized Module

↓

ImportError
```

Symptoms

- ImportError
- Partially initialized module
- Missing attributes

Solutions

- Move common code
- Introduce abstraction
- Reduce coupling
- Lazy import (when appropriate)

🏛️ **Architecture Note**

Circular imports are often an indication of poor module boundaries rather than just a Python issue.

---

# 11. Decision Guide

| Situation | Recommended Approach |
|------------|---------------------|
| Import from same package | Relative Import |
| Import from another package | Absolute Import |
| Expensive initialization | Lazy Loading |
| Shared configuration | Module Singleton |
| Debug import issue | Check `sys.path` |
| Module loads twice? | Check `sys.modules` |
| Circular dependency | Refactor module responsibilities |

---

# 12. Production Best Practices

✅ One responsibility per module

✅ Use meaningful module names

✅ Prefer absolute imports across packages

✅ Keep package hierarchy shallow

✅ Avoid wildcard imports

✅ Load expensive resources lazily

✅ Hide internal implementation using `__init__.py`

---

# 13. Common Mistakes

❌ Naming a file `os.py`, `json.py`, `math.py`

❌ Using `from module import *`

❌ Putting heavy initialization code at module level unnecessarily

❌ Creating circular dependencies

❌ Deeply nested package structures

❌ Executing package modules directly when they rely on relative imports

---

# 14. Interview Nuggets

✔ Difference between a module and a package

✔ Purpose of `__init__.py`

✔ Difference between `sys.path` and `sys.modules`

✔ Why modules execute only once

✔ How Python resolves imports

✔ Why circular imports occur

✔ Absolute vs Relative imports

✔ Purpose of `__name__`

✔ Why use `if __name__ == "__main__"`

✔ How lazy loading improves startup performance

---

# 15. 🤖 GenAI Engineering Connection

| Concept | AI Engineering Usage |
|----------|----------------------|
| Modules | Organize AI applications |
| Packages | Structure FastAPI & LangChain projects |
| Module Cache | Singleton LLM instances |
| Lazy Loading | Load LLMs only when required |
| `__init__.py` | Clean package APIs |
| Absolute Imports | Large enterprise AI systems |
| Relative Imports | Internal package organization |

---

# 16. 🧠 Visual Memory Map

```text
                     Python Modules
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
       Module            Package           Import
          │                 │                  │
          └──────────────┬──┘                  │
                         ▼                     ▼
                   Import Statement      Search sys.path
                                              │
                                              ▼
                                      Check sys.modules
                                              │
                                  ┌───────────┴───────────┐
                                  │                       │
                               Cached                Not Cached
                                  │                       │
                           Return Module          Execute Module
                                                          │
                                                          ▼
                                                   Cache & Return
```

---

# 17. 🔟 Things Never to Forget

1. A module is simply a Python file.
2. A package is a collection of related modules.
3. Python searches for modules using `sys.path`.
4. Imported modules are cached in `sys.modules`.
5. A module executes only once per Python process.
6. `__name__ == "__main__"` is true only for the entry script.
7. `__init__.py` initializes packages and can expose a clean public API.
8. Prefer absolute imports across packages.
9. Use relative imports within the same package.
10. Circular imports usually indicate an architectural design issue, not just a Python error.

---

# Navigation

**← Previous:** README.md

**→ Next:** Notes.md