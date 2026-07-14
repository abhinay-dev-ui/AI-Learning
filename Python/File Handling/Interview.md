# File Handling Interview Questions

## Beginner Level

### Q1. What is file handling?

**Answer**

File handling is the process of reading data from and writing data to files stored on persistent storage. It enables applications to store information permanently beyond the lifetime of a running program.

---

### Q2. Why do we need file handling?

**Answer**

Without file handling, all data would exist only in memory (RAM) and would be lost once the application terminates. File handling allows applications to persist configuration, logs, reports, datasets, and user data.

---

### Q3. What does `open()` do?

**Answer**

`open()` establishes a connection between Python and a file by creating a File Object. It does not immediately read or write any file contents.

---

### Q4. What is a File Object?

**Answer**

A File Object is a Python object representing an open connection to a file. It acts as an interface between the application and the Operating System and provides methods for reading, writing, and managing the file.

---

### Q5. Why doesn't `open()` read the file immediately?

**Answer**

The application may not require the file contents immediately. Separating opening from reading improves flexibility, efficiency, and resource management.

---

### Q6. What are the most common file modes?

**Answer**

- `r` – Read text
- `rb` – Read binary
- `w` – Write (overwrite)
- `a` – Append
- `x` – Create only if the file does not already exist

---

### Q7. What is the difference between `r` and `rb`?

**Answer**

`r` opens the file in text mode and returns strings after decoding the bytes. `rb` opens the file in binary mode and returns raw bytes without decoding.

---

### Q8. What happens if you open a PDF using `r` mode?

**Answer**

Python attempts to decode the PDF bytes as text (UTF-8 by default), which usually results in a `UnicodeDecodeError` because PDFs contain structured binary data.

---

### Q9. Why should PDFs be opened using binary mode?

**Answer**

Binary mode returns the raw bytes without attempting to decode them. These bytes can then be interpreted by a PDF parser such as PyPDF2 or pdfplumber.

---

### Q10. What happens when a file is opened using `w` mode?

**Answer**

If the file exists, its contents are immediately truncated before the File Object is returned. If it does not exist, Python creates a new file.

---

### Q11. What is the difference between `w` and `a` mode?

**Answer**

`w` overwrites the existing file, while `a` preserves the existing contents and writes new data at the end of the file.

---

### Q12. Why is `with` preferred over manually calling `close()`?

**Answer**

The `with` statement automatically closes the file even if an exception occurs, preventing resource leaks and making the code cleaner.

---

### Q13. What happens if a file is not closed?

**Answer**

Resources remain allocated, buffered data may not be written, and other applications may be unable to access the file correctly.

---

### Q14. What is the default file mode in Python?

**Answer**

The default mode is `"r"` (read text mode).

Example:

```python
with open("employees.txt") as file:
    ...
```

is equivalent to:

```python
with open("employees.txt", "r") as file:
    ...
```

---

### Q15. Why are binary files treated differently from text files?

**Answer**

Text files contain encoded characters that Python can decode into strings. Binary files may contain images, compressed data, metadata, fonts, or other non-text structures that require specialized parsers instead of text decoding.

## Intermediate Level

### Q16. What happens internally when `read()` is called?

**Answer**

When `read()` is called:

1. Python asks the Operating System to read data from the file.
2. The Operating System retrieves bytes from disk (or its cache).
3. Python stores the bytes in its internal buffer.
4. If the file is opened in text mode, Python decodes the bytes into a string.
5. The resulting string is returned to the application.

---

### Q17. Why does Python use buffering while reading files?

**Answer**

Disk I/O is significantly slower than accessing memory. Instead of reading one byte at a time from the disk, Python reads a larger block of data into memory (buffer). Subsequent reads are served from the buffer, reducing expensive disk operations and improving performance.

---

### Q18. What is the difference between `read()` and `read(size)`?

**Answer**

`read()` loads the remaining contents of the file into memory.

`read(size)` reads only the specified number of characters (text mode) or bytes (binary mode), making it suitable for processing large files incrementally.

---

### Q19. When would you use `read(size)` instead of `read()`?

**Answer**

Use `read(size)` when:

- Processing very large files.
- Streaming data.
- Memory usage needs to remain low.
- Reading binary files in chunks.

---

### Q20. What is the difference between `readline()` and `readlines()`?

**Answer**

`readline()` returns one line at a time.

`readlines()` reads the entire file and returns a list containing all lines.

`readline()` is more memory efficient for large files.

---

### Q21. Why is iterating over a file using a `for` loop considered Pythonic?

**Answer**

The file object is an iterator.

A `for` loop reads one line at a time using Python's internal buffering, making it clean, memory efficient, and easy to read.

Example:

```python
with open("employees.txt") as file:
    for line in file:
        print(line)
```

---

### Q22. Does a `for` loop read the entire file into memory?

**Answer**

No.

The file object reads data incrementally using an internal buffer. Only a small portion of the file is kept in memory at a time.

---

### Q23. What happens when `write()` is called?

**Answer**

Python:

1. Receives a string.
2. Encodes it into bytes.
3. Stores the bytes in an internal buffer.
4. Eventually sends the buffered data to the Operating System.
5. The Operating System writes it to disk.

---

### Q24. Why doesn't `write()` immediately write to the disk?

**Answer**

Immediate disk writes are expensive.

Python uses buffering to batch multiple write operations together, significantly improving performance.

---

### Q25. What is the purpose of `flush()`?

**Answer**

`flush()` forces Python to immediately transfer its buffered data to the Operating System.

It improves durability but may reduce performance if called too frequently.

---

### Q26. Does `flush()` guarantee the data is physically written to the disk?

**Answer**

No.

`flush()` empties Python's internal buffer and sends the data to the Operating System.

The Operating System may still keep the data in its own buffer before writing it to the physical disk.

---

### Q27. What does `close()` do?

**Answer**

`close()`:

- Flushes any remaining buffered data.
- Releases the underlying file descriptor.
- Frees operating system resources.

After a file is closed, it should no longer be used.

---

### Q28. Why is `close()` still important if `flush()` exists?

**Answer**

`flush()` only transfers buffered data.

`close()` performs a final flush (if necessary) and releases all resources associated with the file.

---

### Q29. What is a `UnicodeDecodeError`?

**Answer**

It occurs when Python attempts to decode bytes into text using an encoding (UTF-8 by default), but the bytes do not represent valid text.

This commonly happens when opening binary files in text mode.

---

### Q30. What is the difference between encoding and decoding?

**Answer**

Encoding converts:

```
String → Bytes
```

Decoding converts:

```
Bytes → String
```

Reading performs decoding.

Writing performs encoding.

---

### Q31. Why is `pathlib` preferred over string paths?

**Answer**

`pathlib` provides:

- Cross-platform compatibility.
- Better readability.
- Object-oriented APIs.
- Built-in methods for common file operations.

It reduces platform-specific bugs and improves maintainability.

---

### Q32. How does `Path("data") / "reports"` work?

**Answer**

The `/` operator is overloaded by the `Path` class.

Instead of performing division, it joins path components and returns a new `Path` object.

---

### Q33. What is the difference between text mode and binary mode?

**Answer**

| Text Mode | Binary Mode |
|-----------|-------------|
| Returns strings | Returns bytes |
| Performs decoding | No decoding |
| Used for text files | Used for structured/binary files |

---

### Q34. Why shouldn't you use `read()` for very large files?

**Answer**

`read()` loads the remaining contents of the file into memory.

For very large files, this can consume excessive memory and may impact application performance or even cause memory exhaustion.

---

### Q35. What is the most memory-efficient way to process a large text file?

**Answer**

Use file iteration:

```python
with open("large.log") as file:
    for line in file:
        process(line)
```

This processes one line at a time while using Python's internal buffering, keeping memory usage low regardless of the file size.

## Advanced & Production Level

### Q36. You need to process a 20 GB log file. How would you approach it?

**Answer**

Loading the entire file using `read()` would consume excessive memory and could cause the application to crash.

A better approach is to process the file incrementally:

```python
with open("application.log") as file:
    for line in file:
        process(line)
```

For binary data, `read(size)` can be used to process fixed-size chunks.

This approach is memory-efficient and scales regardless of the file size.

---

### Q37. Why is buffering considered a performance optimization?

**Answer**

Disk I/O is one of the slowest operations performed by an application.

Without buffering:

- Every `read()` or `write()` would require a separate disk access.

With buffering:

- Multiple operations are grouped together.
- The number of disk accesses is reduced.
- Overall application performance improves significantly.

Buffering trades a small amount of memory for much better I/O performance.

---

### Q38. When would you call `flush()` manually?

**Answer**

`flush()` should be used when data must reach the Operating System immediately.

Examples include:

- Audit logs
- Financial transaction logs
- Progress tracking
- Long-running applications
- Debugging critical failures

It should not be called after every write unless durability is more important than performance.

---

### Q39. Why shouldn't `flush()` be called after every `write()`?

**Answer**

Calling `flush()` after every write defeats the purpose of buffering.

Advantages:
- Data becomes available sooner.

Disadvantages:
- Increased disk I/O.
- Reduced performance.
- Higher CPU utilization.

A balance should be chosen based on business requirements.

---

### Q40. How would you safely process user-uploaded PDF files?

**Answer**

A production workflow would include:

1. Validate the file exists.
2. Validate the file extension.
3. Verify the file signature (magic bytes).
4. Open using binary mode (`rb`).
5. Parse using a PDF library.
6. Handle parsing exceptions.
7. Close the file automatically using `with`.

This approach improves reliability and security.

---

### Q41. Why is checking only the file extension not sufficient?

**Answer**

File extensions can be renamed.

For example:

```
virus.exe
```

can be renamed to:

```
invoice.pdf
```

A production system should verify both:

- File extension.
- File signature (magic bytes).

This helps prevent invalid or malicious files from being processed.

---

### Q42. How does file handling relate to Generative AI applications?

**Answer**

Most GenAI systems begin by reading documents.

Examples include:

- Reading PDFs.
- Reading Word documents.
- Loading datasets.
- Processing CSV files.
- Chunking documents.
- Creating embeddings.
- Building RAG pipelines.

Efficient file handling is the foundation of document ingestion.

---

### Q43. Why is binary mode commonly used in AI applications?

**Answer**

Most AI pipelines process structured files such as:

- PDFs
- Images
- Audio
- Videos

These files contain binary data rather than plain text.

Opening them using binary mode returns raw bytes, which can then be interpreted by specialized parsers or machine learning libraries.

---

### Q44. How would you design a reliable logging system?

**Answer**

A reliable logging system should:

- Use append mode (`a`).
- Keep the file open only when required.
- Buffer writes for performance.
- Flush periodically or for critical events.
- Rotate log files when they become large.
- Handle write failures gracefully.

This balances performance, durability, and maintainability.

---

### Q45. What are the advantages of using `pathlib` in enterprise applications?

**Answer**

`pathlib` provides:

- Cross-platform compatibility.
- Cleaner and more readable code.
- Object-oriented path manipulation.
- Built-in helper methods.
- Reduced platform-specific bugs.

It is the recommended approach for modern Python development.

---

### Q46. How would you make file processing portable across Windows, Linux, and macOS?

**Answer**

Use:

- `pathlib.Path` for path manipulation.
- Relative paths where appropriate.
- Platform-independent APIs.
- Avoid hardcoding path separators.

This ensures the application behaves consistently across operating systems.

---

### Q47. What common mistakes do developers make when working with files?

**Answer**

Common mistakes include:

- Forgetting to close files.
- Using `read()` on very large files.
- Opening binary files in text mode.
- Ignoring exceptions.
- Hardcoding file paths.
- Assuming files always exist.
- Calling `flush()` unnecessarily.

---

### Q48. Explain the complete lifecycle of reading a text file.

**Answer**

```
Application

↓

open()

↓

File Object

↓

read()

↓

Operating System

↓

Raw Bytes

↓

Python Buffer

↓

Decode (UTF-8)

↓

Python String

↓

Application

↓

close()
```

This sequence highlights the interaction between the application, Python runtime, the Operating System, and storage.

---

### Q49. Explain the complete lifecycle of writing to a text file.

**Answer**

```
Application

↓

write()

↓

Python String

↓

Encode

↓

Bytes

↓

Python Buffer

↓

Operating System

↓

OS Buffer

↓

Disk

↓

close()
```

Understanding this lifecycle explains why buffering, `flush()`, and `close()` are necessary.

---

### Q50. If you had to summarize File Handling in one sentence during an interview, what would you say?

**Answer**

> File handling is the process of efficiently and safely transferring data between persistent storage and an application by using file objects, buffering, encoding/decoding, and operating system services while balancing performance, reliability, and resource management.
