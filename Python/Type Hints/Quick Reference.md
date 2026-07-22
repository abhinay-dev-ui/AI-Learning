# Python Type Hints - Quick Reference

## Basic Type Hints

| Feature | Use When | Example |
|----------|----------|---------|
| Variable Annotation | Defining variable types | `name: str` |
| Function Parameter | Define expected input | `def greet(name: str)` |
| Return Type | Define expected output | `-> str` |

---

## Collection Types

| Type | Syntax | Example |
|------|--------|---------|
| list | `list[T]` | `list[str]` |
| tuple | `tuple[T1, T2]` | `tuple[int, str]` |
| Variable Tuple | `tuple[T, ...]` | `tuple[int, ...]` |
| dict | `dict[K, V]` | `dict[str, int]` |
| set | `set[T]` | `set[int]` |
| frozenset | `frozenset[T]` | `frozenset[str]` |

---

## Advanced Types

| Feature | Purpose | Example |
|----------|---------|---------|
| Any | Disable type checking | `Any` |
| object | Accept any object while preserving static checking | `object` |
| Union | Multiple possible types | `int | str` |
| Optional | Value may be None | `Employee | None` |
| Literal | Fixed allowed values | `Literal["Admin", "User"]` |
| Final | Constant values | `PI: Final` |
| ClassVar | Class-level variable | `company: ClassVar[str]` |
| Annotated | Add metadata | `Annotated[int, Field(gt=0)]` |

---

## Custom Types

### TypeAlias

**Use when**

- Complex reusable types
- Improve readability
- Follow DRY

Example

```python
type EmployeeRecords = list[dict[str, str]]
```

Avoid

- Business identities

---

### NewType

**Use when**

- Business identifiers
- Prevent mixing similar primitive types

Example

```python
EmployeeId = NewType("EmployeeId", int)
```

Avoid

- Runtime validation

---

### TypedDict

**Use when**

- JSON
- API Request
- API Response
- Dictionary schema

Example

```python
class Employee(TypedDict):
    id: int
    name: str
```

Avoid

- Business logic
- Mutable objects with methods

---

### NamedTuple

**Use when**

- Immutable lightweight objects
- Database results
- Coordinates
- Read-only models

Example

```python
class Employee(NamedTuple):
    id: int
    name: str
```

Avoid

- Rich business objects

---

### Protocol

**Use when**

- Capability matters
- Dependency Injection
- Plugin architecture
- Loose coupling

Example

```python
class NotificationService(Protocol):
    def send(self, message: str) -> None:
        ...
```

Avoid

- IS-A relationships

---

## Decision Guide

| Need | Use |
|------|-----|
| Better readability | TypeAlias |
| Strong business identity | NewType |
| JSON schema | TypedDict |
| Immutable object | NamedTuple |
| Behaviour contract | Protocol |

---

## Enterprise Best Practices

✓ Always annotate public APIs

✓ Prefer explicit return types

✓ Prefer `object` over `Any` whenever possible

✓ Use `TypedDict` for API payloads

✓ Use `NewType` for business identifiers

✓ Prefer `Protocol` over inheritance when modelling behaviour

✓ Keep type hints simple and readable

---

## Common Mistakes

❌ Using `Any` everywhere

❌ Using `dict[str, Any]` for structured data

❌ Using inheritance when Protocol is sufficient

❌ Using `NamedTuple` for mutable business objects

❌ Using `TypeAlias` instead of `NewType`

---

## One-line Memory Guide

| Feature | Remember As |
|----------|-------------|
| TypeAlias | Better name |
| NewType | New identity |
| TypedDict | Typed JSON |
| NamedTuple | Immutable object |
| Protocol | Behaviour contract |

## Type Hint Decision Tree

```
Need to improve readability?
            │
            ▼
      Use TypeAlias
```

```
Need a new business identity?
            │
            ▼
       Use NewType
```

```
Working with JSON/API payloads?
            │
            ▼
      Use TypedDict
```

```
Need an immutable lightweight object?
            │
            ▼
      Use NamedTuple
```

```
Need to describe behaviour instead of inheritance?
            │
            ▼
        Use Protocol
```

---

## Protocol vs Inheritance

| Criteria | Inheritance | Protocol |
|----------|-------------|----------|
| Relationship | IS-A | CAN-DO |
| Requires inheritance | Yes | No |
| Behaviour based | No | Yes |
| Third-party classes | Difficult | Easy |
| Loose coupling | No | Yes |
| Dependency Injection | Possible | Preferred |
| Best for | Domain Models | Service Contracts |

---

## TypeAlias vs NewType

| TypeAlias | NewType |
|------------|---------|
| Alternative name | New business type |
| Same underlying type | Different logical type |
| Improves readability | Prevents mixing business values |
| No additional safety | Additional static safety |

Example

```python
type EmployeeIds = list[int]

EmployeeId = NewType("EmployeeId", int)
```

---

## TypedDict vs dict

| dict | TypedDict |
|------|-----------|
| Keys unknown | Keys defined |
| Values unknown | Values typed |
| No IDE support | Excellent IDE support |
| Runtime only | Static validation |

---

## NamedTuple vs dataclass

| NamedTuple | dataclass |
|------------|-----------|
| Immutable | Mutable by default |
| Lightweight | Rich objects |
| No business logic | Supports business logic |
| Faster | More flexible |

---

## Any vs object

| Any | object |
|------|--------|
| Turns off static checking | Preserves static checking |
| IDE cannot help | IDE can help |
| Use sparingly | Preferred when possible |

---

## Literal vs Enum

| Literal | Enum |
|----------|------|
| Fixed compile-time values | Named constants |
| Small fixed choices | Domain constants |
| Function parameters | Business models |

---

## Optional vs Union

```python
Optional[int]
```

Equivalent to

```python
int | None
```

---

## Production Checklist

Before writing a new function, ask yourself:

□ Have I annotated all parameters?

□ Have I specified the return type?

□ Can I avoid `Any`?

□ Is `TypedDict` better than `dict`?

□ Should I create a `TypeAlias`?

□ Is this a business identifier (`NewType`)?

□ Do I need immutability (`NamedTuple`)?

□ Is this behaviour better represented by a `Protocol`?

---

## Quick Interview Revision

| Question | Answer |
|----------|--------|
| Why use type hints? | Better readability, IDE support, static analysis, maintainability |
| Does Python enforce type hints? | No |
| What performs type checking? | IDE, mypy, pyright |
| Difference between Any and object? | Any disables checking; object preserves checking |
| Difference between TypeAlias and NewType? | Alias vs new business identity |
| Why TypedDict? | Strongly typed dictionaries |
| Why NamedTuple? | Immutable structured object |
| Why Protocol? | Behaviour contract without inheritance |

---

## Key Takeaways

- Type hints improve developer experience, not Python runtime.
- Prefer explicit types over implicit behaviour.
- Use `TypeAlias` to simplify complex type hints.
- Use `NewType` for business-specific identifiers.
- Use `TypedDict` for structured dictionaries and API payloads.
- Use `NamedTuple` for immutable lightweight models.
- Use `Protocol` when behaviour matters more than inheritance.
- Prefer `object` over `Any` whenever possible.
- Treat type hints as part of your API contract.

