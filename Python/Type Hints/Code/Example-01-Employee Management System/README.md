# Example 1 – Employee Management System

## Objective

This example demonstrates the practical use of Python **Type Hints** in a simple, production-style application. Instead of using isolated code snippets, the concepts are applied in a small Employee Management System similar to what you might build in a real project.

---

## Learning Objectives

By completing this example, you will learn how to use:

- Basic Type Hints
- Function Parameter Type Hints
- Return Type Hints
- Variable Type Hints
- `list[T]`
- Union Types (`|`)
- Optional Types (`T | None`)
- `Literal`
- `ClassVar`
- `Final`
- `TypeAlias`
- `NewType`

---

## Project Structure

```text
example-1-employee-management/
│
├── employee.py
├── employee_service.py
├── main.py
└── README.md
```

---

## File Overview

### employee.py

Contains the `Employee` model.

Demonstrates:

- Class attributes
- Type aliases
- Literal types
- Final constants
- NewType
- Method return annotations

---

### employee_service.py

Contains business logic for managing employees.

Demonstrates:

- Generic collections (`list[Employee]`)
- Optional return values
- Union parameter types
- Function annotations

---

### main.py

Application entry point.

Demonstrates:

- Creating objects
- Calling service methods
- Searching employees
- Displaying results

---

## Concepts Used

| Concept | Example |
|---------|---------|
| Basic Type Hints | `name: str` |
| Return Type | `-> None` |
| Optional | `Employee \| None` |
| Union | `int \| str` |
| Literal | Department values |
| NewType | `EmployeeId` |
| TypeAlias | `SearchValue` |
| Final | Default bonus |
| ClassVar | Company name |
| Generic Collection | `list[Employee]` |

---

## How to Run

From the project directory:

```bash
python main.py
```

---

## Expected Output

```text
----- All Employees -----

101 | John | Engineering | 85000
102 | Alice | HR | 65000

Searching by ID

101 | John | Engineering | 85000

Searching by Name

102 | Alice | HR | 65000
```

---

## Production Relevance

Although this is a simplified example, the same concepts are used in production applications such as:

- REST APIs
- FastAPI applications
- Internal business services
- CRUD systems
- Employee Management Systems
- ERP applications

Using type hints improves:

- Code readability
- IDE autocomplete
- Static analysis
- Refactoring safety
- Team collaboration

---

## Interview Questions

### Why use `NewType` instead of `int`?

It creates a distinct type for better type safety while having no runtime overhead.

Example:

```python
EmployeeId = NewType("EmployeeId", int)
```

---

### Why use `Literal`?

To restrict a value to a predefined set of valid options.

Example:

```python
Department = Literal[
    "Engineering",
    "HR",
    "Finance",
    "Sales",
]
```

---

### Why use `Final`?

To indicate that a constant should not be reassigned.

```python
DEFAULT_BONUS: Final = 5000
```

---

### Why use `ClassVar`?

To declare attributes shared across all instances of a class.

```python
COMPANY: ClassVar[str] = "OpenAI Technologies"
```

---

## Key Takeaways

- Type hints improve code quality without affecting runtime performance.
- Custom types (`NewType`) make APIs safer and more expressive.
- `Literal` helps prevent invalid values.
- `Final` and `ClassVar` clearly communicate developer intent.
- Well-typed code is easier to maintain, refactor, and understand.
- These concepts are heavily used in frameworks such as FastAPI, Pydantic, LangChain, and many modern Python libraries.

---

## Next Example

➡️ **Example 2 – API Models**

Topics covered:

- `TypedDict`
- `NamedTuple`
- `Annotated`

This example demonstrates how typed models are used in API requests, responses, and data validation.