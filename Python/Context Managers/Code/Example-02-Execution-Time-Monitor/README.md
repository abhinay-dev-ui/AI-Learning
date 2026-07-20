# README.md

# Example 02 - Execution Time Monitor

## Overview

This example demonstrates how a **Context Manager** can be used to measure the execution time of a business operation without mixing timing logic into the business code.

Unlike database or file Context Managers, this example shows that Context Managers can also manage **cross-cutting concerns** such as performance monitoring, logging, profiling, and observability.

The business logic remains focused on processing a PDF document while the Context Manager transparently measures and reports the execution time.

---

# Learning Objectives

After completing this example, you should be able to:

- Understand Context Managers beyond resource cleanup.
- Measure execution time using a reusable Context Manager.
- Use `time.perf_counter()` for high-precision timing.
- Understand why `__enter__()` returns `self`.
- Separate monitoring logic from business logic.
- Apply Context Managers to cross-cutting concerns.

---

# Business Use Case

Suppose a user uploads a large PDF document for processing.

The application performs several operations:

- Extract text
- Generate embeddings
- Store embeddings

The engineering team wants to know:

- Total processing time
- Performance trends
- Slow operations
- SLA violations

Without a Context Manager, every service would need to manually record start and end times.

Instead, the Context Manager centralizes the timing logic.

---

# Architecture

```text
Application

        │

        ▼

PerformanceTimer

        │

        ▼

Record Start Time

        │

        ▼

Execute Business Logic

        │

        ▼

Calculate Duration

        │

        ▼

Report Metrics

        │

        ▼

Application Continues
```

---

# Project Structure

```text
Example-02-Execution-Time-Monitor/

│

├── README.md
├── Production-Improvements.md
├── app.py
│
├── monitoring/
│   └── performance_timer.py
│
├── reports/
│   └── metrics_reporter.py
│
├── services/
│   └── pdf_processing_service.py
│
└── utils/
    └── logger.py
```

---

# Component Responsibilities

## app.py

Application entry point.

Starts the performance monitoring session and invokes the PDF processing service.

---

## monitoring/performance_timer.py

Implements the Context Manager.

Responsibilities:

- Record start time
- Record end time
- Calculate execution duration
- Report metrics

---

## reports/metrics_reporter.py

Responsible for reporting execution metrics.

Currently prints metrics to the console.

---

## services/pdf_processing_service.py

Contains business logic.

Responsibilities:

- Extract text
- Generate embeddings
- Store embeddings

This layer has no knowledge of performance measurement.

---

## utils/logger.py

Simple logger used throughout the application.

---

# Execution Flow

```text
Start Timer

↓

Extract Text

↓

Generate Embeddings

↓

Store Embeddings

↓

Stop Timer

↓

Calculate Duration

↓

Report Metrics
```

---

# Context Manager Lifecycle

```text
PerformanceTimer()

↓

__enter__()

↓

Record Start Time

↓

Execute Business Logic

↓

__exit__()

↓

Calculate Duration

↓

Report Metrics
```

---

# Python Concepts Covered

- Context Managers
- `__enter__()`
- `__exit__()`
- Returning `self`
- `time.perf_counter()`
- Exception-safe cleanup

---

# Production Concepts Covered

- Performance Monitoring
- Metrics Collection
- Observability
- Cross-cutting Concerns
- Layered Architecture
- Separation of Concerns

---

# Expected Output

```text
[INFO] Extracting text from PDF...

[INFO] Generating embeddings...

[INFO] Storing embeddings...

[SUCCESS] PDF Processing completed in 4.00 seconds.

Measured Duration : 4.00 seconds
```

---

# Key Takeaways

- Context Managers are not limited to resource cleanup.
- Cross-cutting concerns should be centralized.
- Business logic remains clean and focused.
- Performance monitoring becomes reusable across the application.