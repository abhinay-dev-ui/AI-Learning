# Example 03 - PDF Document Ingestion Pipeline

## Overview

The **PDF Document Ingestion Pipeline** demonstrates how production applications begin processing uploaded documents before extracting any content.

Unlike text files, PDF documents are **binary files** that contain structured data such as text, images, fonts, metadata, annotations, and digital signatures. Because of this, they cannot be opened using Python's text mode (`"r"`). Instead, they must be opened in **binary mode (`"rb"`)** so that the raw bytes can be passed to a PDF parser.

This example simulates the **first stage of a Generative AI document processing pipeline**, where a PDF is validated before being sent for text extraction.

---

# Business Use Case

Imagine you're building an AI-powered assistant for a Chartered Accountant.

A user uploads the following document:

```text
Income_Tax_Rules.pdf
```

Before the AI can answer questions from this document, the application must:

1. Verify the file exists.
2. Verify the file extension.
3. Open the document in binary mode.
4. Read the file signature (Magic Bytes).
5. Confirm that it is a valid PDF.
6. Pass the binary data to a PDF parser.

Only after these steps can text extraction begin.

---

# Application Workflow

```text
                  Income_Tax_Rules.pdf
                           │
                           ▼
                 Validate File Exists
                           │
                           ▼
               Validate File Extension
                           │
                           ▼
                Open File (Binary Mode)
                           │
                           ▼
                  Read PDF Signature
                           │
                           ▼
                 Verify Magic Bytes
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
            Valid PDF         Invalid PDF
                  │
                  ▼
           Read Remaining Bytes
                  │
                  ▼
          Pass Bytes to PDF Parser
                  │
                  ▼
         Ready for Text Extraction
```

---

# Folder Structure

```text
Example-03-PDF-Document-Ingestion/

│
├── README.md
├── main.py
├── pdf_service.py
├── file_utils.py
│
├── input/
│   └── Income_Tax_Rules.pdf
│
├── output/
│
└── logs/
    └── execution.log
```

---

# Concepts Covered

## File Handling

- Binary Mode (`rb`)
- Reading Raw Bytes
- `read(size)`
- File Signatures (Magic Bytes)
- Binary File Processing
- Exception Handling

---

## Python

- Bytes
- Byte Comparison
- Pathlib
- Functions
- Separation of Concerns

---

## Generative AI

- Document Ingestion
- PDF Validation
- Parser Pipeline
- AI Document Processing
- Foundation of RAG Systems

---

# Learning Objectives

After completing this example, you should be able to:

- Explain why PDFs are opened using `"rb"` instead of `"r"`.
- Understand the difference between text files and binary files.
- Read and inspect raw bytes from a file.
- Verify a file using its Magic Bytes instead of relying only on its extension.
- Explain the first stage of a Document Ingestion Pipeline used in Generative AI applications.

---

# Production Perspective

Document ingestion is the first step in almost every enterprise AI application.

Examples include:

- ChatGPT File Upload
- Claude Projects
- Google NotebookLM
- Microsoft Copilot
- Enterprise Knowledge Management Systems
- Financial Document Analysis
- Legal Document Processing
- Insurance Claim Processing

Every one of these systems validates uploaded documents before extracting text.

---

# Files in this Example

| File | Responsibility |
|------|----------------|
| `main.py` | Application entry point |
| `pdf_service.py` | PDF validation workflow |
| `file_utils.py` | Reusable binary file operations |
| `Income_Tax_Rules.pdf` | Input document |
| `execution.log` | Application execution log |

---

# Expected Output

```text
PDF Document Validation
========================================

✓ File Found

✓ PDF Extension Verified

✓ PDF Signature Verified

✓ Binary Data Read Successfully

✓ Ready for PDF Parser

Document ingestion completed successfully.
```

---

# Why This Example Matters

Many beginners believe a PDF is simply a text document with a different extension.

In reality, a PDF is a **structured binary format**.

Python cannot automatically interpret the contents of a PDF. Instead, it reads the document as raw bytes and passes those bytes to a specialized PDF parser, which understands the PDF specification and extracts readable text.

This same workflow is used by modern AI applications before chunking documents, generating embeddings, and storing them in a Vector Database.

---

# Things to Try

- Rename a `.txt` file to `.pdf` and verify that the Magic Byte validation fails.
- Compare opening the same PDF using `"r"` and `"rb"`.
- Read the first 4, 8, and 16 bytes and inspect the binary output.
- Validate other binary file formats such as PNG or JPEG using their file signatures.
- Integrate a PDF parser (such as `pypdf`) in a future module to extract text.
- Extend the application to support multiple document formats.

---

# Looking Ahead

This example focuses only on **document validation and ingestion**.

In the upcoming modules, we'll extend this pipeline to include:

```text
PDF

↓

Binary Reader

↓

PDF Parser

↓

Extract Text

↓

Clean Text

↓

Chunk Text

↓

Generate Embeddings

↓

Store in Vector Database

↓

Retrieval (RAG)

↓

LLM Response
```

By the end of the GenAI roadmap, you'll have built this complete pipeline from scratch, understanding every stage rather than relying solely on high-level frameworks.