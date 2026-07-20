# Example 01 - Database Transaction Manager

# Overview

This example demonstrates how a **class-based Context Manager** can be used to manage the complete lifecycle of a database transaction in a production-style application.

Instead of requiring developers to manually open connections, commit transactions, roll back on failures, and close connections, the Context Manager encapsulates all these responsibilities.

The business logic only focuses on processing employee data, while the Context Manager guarantees deterministic resource management.

---

# Learning Objectives

By completing this example, you will learn:

- How to build a class-based Context Manager.
- How `__enter__()` and `__exit__()` work together.
- How transactions are committed automatically.
- How rollback occurs when an exception is raised.
- How resource cleanup is guaranteed.
- How production applications separate business logic from infrastructure code.
- How enterprise applications structure transaction management.

---

# Business Use Case

Imagine an HR application that registers a new employee.

The registration process performs multiple database operations:

- Insert employee information
- Create payroll record
- Create access credentials
- Create audit log

These operations must succeed as a single unit.

If any operation fails:

- All previous changes should be rolled back.
- The database should remain in a consistent state.
- The connection should always be released.

Without a Context Manager, developers must remember to:

- Open the connection
- Begin the transaction
- Commit the transaction
- Roll back if an exception occurs
- Close the connection

This repetitive code is error-prone and difficult to maintain.

A Context Manager centralizes these responsibilities.

---

# Architecture

```text
Application

        │

        ▼

DatabaseTransaction Context Manager

        │

        ▼

Acquire Database Connection

        │

        ▼

Begin Transaction

        │

        ▼

Execute Business Logic

        │

        ▼

Exception?

   │             │

 No            Yes

   │             │

Commit      Rollback

        │

        ▼

Release Connection

        │

        ▼

Application Continues
```

---

# Project Structure

```text
Example-01-Database-Transaction-Manager/

│

├── README.md
├── app.py
│
├── database/
│   ├── connection.py
│   ├── context_manager.py
│   └── transaction.py
│
├── services/
│   └── employee_service.py
│
├── models/
│   └── employee.py
│
└── utils/
    └── logger.py
```

---

# Component Responsibilities

## app.py

Application entry point.

Creates the employee registration request and invokes the service layer.

---

## database/connection.py

Simulates a production database connection.

Responsibilities:

- Open connection
- Close connection
- Commit transaction
- Rollback transaction
- Execute SQL statements

---

## database/context_manager.py

Implements the Context Manager.

Responsibilities:

- Acquire connection
- Return connection
- Commit transaction
- Roll back transaction
- Release connection

---

## database/transaction.py

Provides helper methods related to transaction management.

This layer keeps transaction-specific logic separate from the Context Manager.

---

## services/employee_service.py

Contains business logic.

Responsibilities:

- Register employee
- Save payroll
- Save audit information

Notice that this layer never commits or rolls back the transaction.

---

## models/employee.py

Represents the Employee domain object.

---

## utils/logger.py

Simple logger used to visualize execution flow.

---

# Execution Flow

## Successful Transaction

```text
Open Connection

↓

Begin Transaction

↓

Insert Employee

↓

Insert Payroll

↓

Insert Audit Log

↓

Commit Transaction

↓

Close Connection
```

---

## Failed Transaction

```text
Open Connection

↓

Begin Transaction

↓

Insert Employee

↓

Insert Payroll

↓

Exception

↓

Rollback Transaction

↓

Close Connection
```

---

# Context Manager Lifecycle

```text
DatabaseTransaction()

↓

__enter__()

↓

Return Database Connection

↓

Business Logic Executes

↓

__exit__()

↓

Commit / Rollback

↓

Close Connection
```

---

# Python Concepts Covered

- Context Managers
- Context Manager Protocol
- `__enter__()`
- `__exit__()`
- Exception Handling
- Deterministic Resource Management
- Separation of Concerns
- Layered Architecture
- Transaction Management

---

# Production Concepts Covered

- Transaction Lifecycle
- Database Connection Management
- Commit vs Rollback
- Resource Cleanup
- Exception Safety
- Service Layer Pattern
- Infrastructure Layer
- Domain Model
- Logging

---

# Expected Output

## Successful Execution

```text
Opening database connection...

Beginning transaction...

Inserting Employee...

Creating Payroll...

Creating Audit Log...

Transaction committed.

Closing database connection...
```

---

## Failed Execution

```text
Opening database connection...

Beginning transaction...

Inserting Employee...

Creating Payroll...

Error occurred.

Rolling back transaction...

Closing database connection...
```

---

# Key Takeaways

- Context Managers manage the lifecycle of resources.
- Business logic should never manage transactions directly.
- Cleanup should be deterministic.
- Resource management should be centralized.
- Production applications separate infrastructure from business logic.
- Context Managers reduce boilerplate code and improve maintainability.
