# 📌 File Handling - Quick Reference

> A one-page revision sheet for interviews and quick recall.

---

# File Handling Flow

```
Application
    │
    ▼
Python File Object
    │
    ▼
Python Buffer
    │
    ▼
Operating System
    │
    ▼
OS Buffer (Page Cache)
    │
    ▼
Disk
```

---

# Reading Flow

```
Disk
    │
    ▼
Bytes
    │
    ▼
Python
    │
Decode (UTF-8)
    ▼
String
```

---

# Writing Flow

```
String
    │
Encode (UTF-8)
    ▼
Bytes
    │
    ▼
Python Buffer
    │
    ▼
Operating System
    │
    ▼
Disk
```

---

# File Modes

| Mode | Purpose |
|------|---------|
| r | Read text |
| rb | Read binary |
| w | Write (overwrite) |
| wb | Write binary |
| a | Append |
| x | Create only if file doesn't exist |

---

# Reading Methods

| Method | Returns | Best Use |
|---------|----------|-----------|
| read() | Entire file | Small files |
| read(size) | Fixed number of characters | Chunk processing |
| readline() | Single line | Manual line reading |
| readlines() | List of lines | Small files |
| for line in file | One line at a time | Large files |

---

# Writing Methods

| Method | Purpose |
|---------|----------|
| write() | Write a string |
| writelines() | Write multiple strings |
| flush() | Push Python buffer to OS |
| close() | Flush and release resources |

---

# Text vs Binary

| Text Mode | Binary Mode |
|-----------|-------------|
| Returns String | Returns Bytes |
| Decodes UTF-8 | No decoding |
| Human-readable | Raw data |
| txt, csv | pdf, images, videos |

---

# Common Exceptions

- FileNotFoundError
- PermissionError
- IsADirectoryError
- UnicodeDecodeError

---

# pathlib

```python
from pathlib import Path

path = Path("data") / "reports" / "file.pdf"

path.exists()
path.is_file()
path.is_dir()
path.parent
path.name
path.suffix
path.mkdir()
```

---

# Production Best Practices

✅ Always use `with`

✅ Prefer `pathlib`

✅ Read large files using iteration

✅ Use binary mode for structured files

✅ Handle specific exceptions

✅ Don't load huge files into memory

---

# Performance Tips

Small Files

```
read()
```

Large Files

```
for line in file
```

Binary Streams

```
read(size)
```

---

# Key Concepts

- File Object
- Encoding
- Decoding
- Buffering
- File Lifecycle
- Resource Management
- Performance
- Durability
- Portability

---

# Architecture Principles

- Reading = Decode
- Writing = Encode
- File Object = Interface between Python and OS
- Buffering improves performance
- Durability and Performance are trade-offs
- Process data incrementally for scalability