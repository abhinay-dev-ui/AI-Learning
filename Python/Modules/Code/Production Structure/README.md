# Example 2 - Production Project Structure

## Overview

This example demonstrates how Python modules and packages are organized in a real-world application.

Unlike **Example 1**, which focused on understanding how modules work internally, this example focuses on **application structure**, **package organization**, and **writing maintainable code**.

The project is intentionally designed to resemble the architecture of a production GenAI application. As we progress through the roadmap, this structure will gradually evolve into a complete RAG and AI Agent application.

---

# Learning Objectives

After completing this example, you should be able to:

- Organize code using packages and modules.
- Understand the purpose of `__init__.py`.
- Differentiate between modules and packages.
- Use absolute imports correctly.
- Understand when relative imports are appropriate.
- Explain how Python initializes packages.
- Design a scalable folder structure for Python applications.
- Apply Separation of Concerns when organizing code.

---

# Concepts Covered

- ✅ Python Packages
- ✅ Modules
- ✅ `__init__.py`
- ✅ Package Initialization
- ✅ Absolute Imports
- ✅ Relative Imports
- ✅ Import Resolution
- ✅ Root Package
- ✅ Project Organization
- ✅ Separation of Concerns
- ✅ Layered Architecture

---

# Project Structure

```text
Example-2-Production-Structure/
│
├── app.py
├── config.py
│
├── database/
│   ├── __init__.py
│   └── connection.py
│
├── services/
│   ├── __init__.py
│   ├── embedding.py
│   └── llm.py
│
├── models/
│   ├── __init__.py
│   └── document.py
│
└── README.md
```

---

# Folder Responsibilities

| Folder | Responsibility |
|---------|----------------|
| **app.py** | Application entry point responsible for orchestrating the application. |
| **config.py** | Stores application configuration and shared constants. |
| **database/** | Contains database connection and data access logic. |
| **services/** | Implements business logic such as LLM and embedding services. |
| **models/** | Defines domain models and business entities. |

---

# Architecture Overview

```text
                app.py
                   │
        ┌──────────┴──────────┐
        │                     │
   services/              config.py
        │
        │
   database/
        │
        │
     models/
```

Each package has a single responsibility and communicates through well-defined interfaces.

---

# How to Run

Navigate to the project directory and execute:

```bash
python app.py
```

---

# Expected Output

```text
Application Started

Database Connected
LLM Loaded

Database Connected
Embedding Generated

Application Finished
```

> The exact output may vary depending on additional logging or print statements added during experimentation.

---

# Expected Learning Outcome

By the end of this example, you should understand:

- How packages help organize larger applications.
- Why large projects are divided into multiple modules.
- The role of `__init__.py` during package initialization.
- Why absolute imports improve readability in production code.
- How Separation of Concerns leads to maintainable software.
- How this project structure scales to enterprise applications.

---

# Things to Try

### Experiment 1 – Add a New Service

Create a new module:

```text
services/
    summarizer.py
```

Implement a simple function and import it into `app.py`.

---

### Experiment 2 – Use Relative Imports

Replace an absolute import with a relative import.

Example:

```python
from database.connection import connect
```

becomes

```python
from ..database.connection import connect
```

Observe the behavior and identify when relative imports work correctly.

---

### Experiment 3 – Package Initialization

Add the following to `services/__init__.py`:

```python
print("Initializing Services Package")
```

Run the application and observe when this message is printed.

---

### Experiment 4 – Add Another Package

Create a new package:

```text
utils/
    __init__.py
    logger.py
```

Import the logger into multiple modules and observe how package organization improves readability.

---

### Experiment 5 – Refactor the Project

Move all configuration values into `config.py`.

Update every module to import configuration from a single location.

Discuss why centralizing configuration improves maintainability.

---

# Production Perspective

Although this project is intentionally small, it follows the same architectural principles used in enterprise applications.

As we progress through the roadmap, this structure will evolve to include:

- LLM Integration
- Embedding Models
- Vector Databases
- RAG Pipelines
- AI Agents
- LangChain
- LangGraph
- REST APIs
- Configuration Management
- Logging
- Testing

The goal is to build a foundation that scales naturally as new features are introduced.

---

# Summary

This example introduces the principles of organizing Python applications using packages and modules. Rather than focusing on individual language features, it demonstrates how to structure code for readability, maintainability, and scalability.

The architecture shown here serves as the foundation for the larger GenAI applications that will be developed throughout this learning roadmap.