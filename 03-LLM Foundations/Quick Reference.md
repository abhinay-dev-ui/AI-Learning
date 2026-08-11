# LLM Fundamentals - Quick Reference

## Purpose

This document provides a concise revision guide for the core concepts of Large Language Models (LLMs). It is intended for quick review before interviews, project implementation, or revisiting key concepts.

---

# 1. Transformers

**Definition**

A Transformer is a deep learning architecture that processes all input tokens in parallel using the Self-Attention mechanism.

**Why Introduced**

To overcome the limitations of sequential models like RNNs and LSTMs.

**Key Points**

- Parallel processing
- Better long-range dependency handling
- Foundation of modern LLMs

---

# 2. Attention & Self-Attention

**Definition**

Attention helps the model focus on the most relevant information.

Self-Attention allows each token to understand its meaning by considering every other token in the same input.

**Why Introduced**

To capture contextual relationships between words.

**Key Points**

- Every token attends to every other token
- Builds contextual understanding
- Core mechanism of Transformers

---

# 3. Tokenization & Tokens

**Definition**

Tokenization converts text into smaller units called tokens before processing by the model.

**Why Introduced**

LLMs understand tokens, not raw text.

**Key Points**

- Token ≠ Word
- Tokens are converted to Token IDs
- Context window is measured in tokens
- API pricing is usually token-based

---

# 4. Embeddings

**Definition**

Embeddings convert Token IDs into dense numerical vectors representing semantic meaning.

**Why Introduced**

Token IDs contain no semantic information.

**Key Points**

- Similar words have similar embeddings
- Foundation of Semantic Search and RAG
- Static Embeddings → Contextual Embeddings after Self-Attention

---

# 5. Training vs Inference

## Training

The process of learning patterns by adjusting billions of model weights using large datasets.

## Inference

The process of generating responses using already learned weights.

**Key Points**

- Training learns
- Inference predicts
- GenAI Engineers primarily work with inference

---

# 6. Context Window

**Definition**

The maximum number of tokens an LLM can process in a single request.

**Why Important**

It determines how much information the model can remember during inference.

**Key Points**

- Measured in tokens
- Larger context retains more information
- Context overflow causes earlier information to be forgotten
- One motivation for RAG

---

# 7. Sampling

**Definition**

Sampling selects the next token from the probability distribution predicted by the LLM.

### Temperature

Controls randomness.

- Lower → More deterministic
- Higher → More creative

### Top-k

Limits selection to the top *k* most probable tokens.

### Top-p (Nucleus Sampling)

Selects the smallest group of tokens whose cumulative probability reaches *p*.

**Key Points**

- Temperature adjusts probabilities
- Sampling selects the next token
- Top-k limits candidates by count
- Top-p limits candidates by cumulative probability

---

# 8. Hallucinations

**Definition**

Hallucinations occur when an LLM generates information that is incorrect, fabricated, or unsupported.

**Common Causes**

- Missing knowledge
- Ambiguous prompts
- Limited context
- Probabilistic prediction

**Mitigation**

- Better prompting
- RAG
- Lower temperature (improves consistency, not factual correctness)
- Human verification

---

# 9. Quantization

**Definition**

Quantization stores model weights using lower numerical precision to reduce memory usage and improve inference efficiency.

**Key Points**

- Same architecture
- Same number of parameters
- Lower precision weights
- Faster inference
- Smaller model size
- Slight quality trade-off

**Examples**

- FP32
- FP16
- INT8 / Q8
- Q4

---

# 10. Model Families

**Definition**

A model family is a collection of related LLMs developed using the same core architecture and design philosophy.

**Open-Weight Model**

Model weights are publicly available for download and deployment (subject to license).

**Closed Model**

Model weights are not publicly available. Users interact through a hosted service or API.

**Key Points**

- Different families optimize for different goals
- Architecture is often similar
- Model selection depends on the use case, hardware, privacy, cost, and performance requirements

---

# LLM Processing Pipeline

```text
User Prompt
      │
      ▼
Tokenization
      │
      ▼
Token IDs
      │
      ▼
Embeddings
      │
      ▼
Transformer
(Self-Attention)
      │
      ▼
Contextual Embeddings
      │
      ▼
Probability Distribution
      │
      ▼
Sampling
      │
      ▼
Generated Response
```

---

# One-Line Revision

- **Transformer** → Processes all tokens in parallel.
- **Self-Attention** → Understands relationships between tokens.
- **Tokenization** → Converts text into tokens.
- **Embeddings** → Give semantic meaning to tokens.
- **Training** → Learns model weights.
- **Inference** → Uses learned weights to generate responses.
- **Context Window** → Maximum tokens the model can process.
- **Sampling** → Chooses the next token.
- **Hallucination** → Confident but incorrect output.
- **Quantization** → Smaller weights, faster inference.
- **Model Families** → Different LLMs optimized for different use cases.