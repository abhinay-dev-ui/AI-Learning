# LLM Fundamentals

## Overview

LLM Fundamentals introduces the core concepts behind Large Language Models (LLMs) and explains how modern transformer-based AI systems understand and generate human language. This phase focuses on building a strong conceptual foundation without diving into advanced mathematics or research-level implementation details.

The objective is to understand how an LLM processes text—from tokenization to response generation—and how concepts such as embeddings, attention, context windows, sampling, hallucinations, quantization, and model families fit together.

---

## Learning Objectives

After completing this phase, you will be able to:

- Understand the evolution from traditional NLP models to Transformers.
- Explain how Large Language Models process text.
- Differentiate between Tokens, Embeddings, and Contextual Embeddings.
- Understand the difference between Training and Inference.
- Explain how Context Windows affect model performance.
- Understand Sampling techniques (Temperature, Top-k, Top-p).
- Identify why hallucinations occur and how they can be reduced.
- Explain Quantization and its impact on memory, speed, and model quality.
- Differentiate between Open-Weight and Closed Models.
- Compare major LLM model families and choose an appropriate model for different use cases.

---

## Topics Covered

1. Transformers
2. Attention & Self-Attention
3. Tokenization & Tokens
4. Embeddings
5. Training vs Inference
6. Context Window
7. Sampling
   - Temperature
   - Top-k
   - Top-p
8. Hallucinations
9. Quantization
10. Model Families

---

## Prerequisites

Before starting this phase, you should be familiar with:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Artificial Neural Networks
- Natural Language Processing
- Language Models
- Large Language Models
- Generative AI

These concepts are covered in the **02-AI-Foundations** phase.

---

## Learning Outcome

After completing this phase, you will have a clear understanding of:

- How modern LLMs work internally at a high level.
- The complete inference pipeline used by Transformer-based models.
- Why embeddings, attention, context windows, and sampling are fundamental to LLMs.
- Why models hallucinate and how retrieval-based techniques help mitigate it.
- How quantization enables efficient local deployment.
- How to select an appropriate LLM for real-world applications.

This knowledge forms the foundation for building production GenAI applications.

---

## What's Next?

The next phase is **04-RAG (Retrieval-Augmented Generation)**.

In the RAG phase, you'll learn how to extend an LLM with external knowledge using embeddings, vector databases, semantic search, and document retrieval to build more accurate and context-aware AI applications.

---

## Deferred Topics

The following advanced topics are intentionally deferred to **11-Research-And-Advanced-Topics**:

- Query, Key, and Value (QKV)
- Attention Mathematics
- Gradient Descent
- Backpropagation
- Loss Functions
- Optimizers
- Learning Rate
- Fine-Tuning
- LoRA / QLoRA
- RLHF
- Mixture of Experts (MoE)
- Distributed Training
- AI Safety

---

## Repository Position

```
AI Foundations
        │
        ▼
LLM Fundamentals   ← You are here
        │
        ▼
RAG
        │
        ▼
LangChain
        │
        ▼
LangGraph
        │
        ▼
MCP
        │
        ▼
AI Agents
```