# Example 2 – API Models

## Objective

This example demonstrates how Python's advanced typing features can be used to model API request and response objects without relying on external frameworks.

The goal is to understand how structured data moves through an application before introducing libraries such as FastAPI or Pydantic.

Rather than building an actual web service, this example simulates the API layer using plain Python.

---

# Learning Objectives

By completing this example, you will learn how to use:

- TypedDict
- NamedTuple
- Annotated
- Literal
- Type Aliases
- Union Types
- Optional Types
- Function Type Hints
- Return Type Hints
- Generic Collections (`list[T]`)

---

# Project Structure

```text
example-2-api-models/

├── models.py
├── validators.py
├── employee_api.py
├── main.py
├── README.md
└── Future-Improvements.md
```

---

# File Overview

## models.py

Contains API data models.

Demonstrates:

- TypedDict
- NamedTuple
- Literal

---

## validators.py

Contains reusable type aliases using `Annotated`.

Demonstrates:

- Annotated
- Metadata attached to type hints

---

## employee_api.py

Simulates a REST API.

Responsibilities:

- Create employee
- Get employee
- List employees

Demonstrates:

- Request models
- Response models
- Function annotations
- Generic collections

---

## main.py

Acts as a client consuming the API layer.

Demonstrates:

- Creating request payloads
- Receiving response objects
- Displaying summaries

---

# Concepts Used

| Concept | Example |
|---------|---------|
| TypedDict | EmployeeRequest |
| TypedDict | EmployeeResponse |
| NamedTuple | EmployeeSummary |
| Annotated | EmployeeName |
| Literal | Department |
| Optional | EmployeeResponse \| None |
| list[T] | Employee collections |
| Function Type Hints | API methods |
| Return Type Hints | API responses |

---

# Application Flow

```text
Client

   │

   ▼

EmployeeRequest (TypedDict)

   │

   ▼

Employee API

   │

   ▼

EmployeeResponse (TypedDict)

   │

   ▼

EmployeeSummary (NamedTuple)
```

---

# How to Run

```bash
python main.py
```

---

# Expected Output

```text
Employee Created

{
    'employee_id': 101,
    'name': 'John',
    'department': 'Engineering',
    'salary': 85000,
    'status': 'Created'
}

Employee Details

{
    'employee_id': 101,
    'name': 'John',
    'department': 'Engineering',
    'salary': 85000,
    'status': 'Created'
}

Employee Summary

EmployeeSummary(employee_id=101, name='John')
```

---

# Production Relevance

Although simplified, this architecture resembles the model layer used in modern backend frameworks.

Similar concepts appear in:

- FastAPI
- Flask
- Django REST Framework
- OpenAI SDK
- LangChain
- LangGraph

Request and response models improve:

- Code readability
- API consistency
- Type safety
- IDE support
- Documentation generation

---

# Interview Questions

## Why use TypedDict?

To represent dictionary objects with a predefined schema while retaining normal dictionary behavior.

---

## Why use NamedTuple?

To represent lightweight immutable objects.

Useful for:

- Database query results
- Read-only DTOs
- Summary objects

---

## Why use Annotated?

To attach metadata to a type.

The metadata itself does not perform validation but can later be consumed by frameworks such as FastAPI and Pydantic.

---

## Why not use normal dictionaries everywhere?

TypedDict provides:

- Better autocomplete
- Static type checking
- Clear documentation
- Safer refactoring

---

# Key Takeaways

- TypedDict models structured dictionary data.
- NamedTuple provides immutable lightweight objects.
- Annotated allows metadata to be attached to types.
- Modern Python frameworks build heavily upon these typing features.
- Understanding these concepts makes learning FastAPI and Pydantic significantly easier.

---

# Next Example

➡️ Example 3 – Notification Framework

Topics covered:

- Protocol
- Structural Typing
- Dependency Inversion
- Pluggable Components

This example demonstrates how Python supports interface-like programming without requiring traditional interfaces.