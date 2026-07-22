# Example 3 – Notification Framework

## Objective

This example demonstrates how Python's **Protocol** enables interface-like programming through structural typing without requiring inheritance.

The goal is to build a flexible notification system where the business logic depends only on a contract rather than concrete implementations. This approach allows new notification providers to be added without modifying existing application logic.

Although the example uses notification providers, the same architecture is widely used in enterprise applications, plugin systems, and modern GenAI frameworks.

---

# Learning Objectives

By completing this example, you will learn how to use:

- Protocol
- Structural Typing
- Duck Typing
- Polymorphism
- Type Hints
- Generic Collections (`list[T]`)
- Optional Types (`T | None`)
- Separation of Concerns

---

# Project Structure

```text
example-3-notification-framework/

├── notification.py
├── providers.py
├── notification_service.py
├── main.py
├── README.md
└── Future-Improvements.md
```

---

# File Overview

## notification.py

Defines the notification contract using `Protocol`.

Demonstrates:

- Protocol
- Interface-like programming
- Structural typing

---

## providers.py

Contains concrete notification providers.

Current providers:

- EmailProvider
- SMSProvider

Demonstrates:

- Duck Typing
- Independent implementations
- Polymorphism

---

## notification_service.py

Coordinates notification delivery.

Responsibilities:

- Select notification provider
- Send notifications
- Hide implementation details from clients

Demonstrates:

- Protocol usage
- Separation of concerns
- Business layer abstraction

---

## main.py

Application entry point.

Demonstrates:

- Creating notification services
- Sending notifications
- Switching providers

---

# Concepts Used

| Concept | Example |
|---------|---------|
| Protocol | NotificationProvider |
| Structural Typing | EmailProvider, SMSProvider |
| Duck Typing | Provider implementations |
| Polymorphism | NotificationService |
| Type Hints | Function signatures |
| Return Type Hints | Service methods |
| Generic Collections | Future provider lists |

---

# Application Flow

```text
Application

      │

      ▼

NotificationService

      │

      ▼

NotificationProvider (Protocol)

      │

 ┌────┴───────────────┐
 │                    │
 ▼                    ▼

EmailProvider     SMSProvider
```

---

# How to Run

```bash
python main.py
```

---

# Expected Output

```text
[Email] Sending email to john@example.com: Welcome to the company!

[SMS] Sending SMS to +91 9876543210: Your salary has been credited.
```

---

# Production Relevance

This architecture is extremely common in enterprise software.

Examples include:

- Notification systems
- Payment gateways
- Authentication providers
- Cloud storage providers
- Database drivers
- Logging frameworks

The same design principle is also heavily used in GenAI applications where different providers expose a common interface.

Examples:

- OpenAI
- Ollama
- Anthropic
- Gemini
- Mistral

Using protocols provides:

- Loose coupling
- Better maintainability
- Easier extensibility
- Improved testability
- Cleaner architecture

---

# Interview Questions

## What is a Protocol?

A Protocol defines a contract that specifies the required methods and attributes an object must provide.

Unlike traditional inheritance, a class does not need to explicitly inherit from a Protocol to satisfy it.

---

## What is Structural Typing?

Structural typing determines compatibility based on an object's structure rather than its inheritance hierarchy.

If a class implements the required members, it satisfies the protocol automatically.

---

## How is Protocol different from an Abstract Base Class (ABC)?

Protocols rely on structural typing.

Abstract Base Classes rely on explicit inheritance.

Protocols provide greater flexibility and are particularly useful for loosely coupled architectures.

---

## What is Duck Typing?

Duck typing follows the principle:

> "If it walks like a duck and quacks like a duck, it is a duck."

Protocols formalize this concept by allowing static type checkers to verify compatibility.

---

# Key Takeaways

- Protocol provides interface-like behavior without inheritance.
- Structural typing reduces coupling between components.
- Business logic depends on contracts rather than implementations.
- New providers can be introduced with minimal changes.
- This design forms the foundation of many enterprise and GenAI architectures.

---

# Next Example

➡️ Phase 6 – Generic Types

Topics covered:

- TypeVar
- Generic Classes
- Generic Functions
- Reading Generic Type Annotations

These concepts build upon Protocol and complete the practical Python typing toolkit before moving into static type checking and production design patterns.