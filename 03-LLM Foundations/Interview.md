# LLM Fundamentals - Interview Questions

This document contains interview questions and concise answers covering the fundamental concepts of Large Language Models (LLMs). The questions progress from basic concepts to practical engineering scenarios and are intended for interview preparation and self-assessment.

---

# Basic

## Transformers

### Q1. What is a Transformer?

**Answer**

A Transformer is a deep learning architecture that processes all input tokens in parallel using the Self-Attention mechanism. It is the foundation of modern Large Language Models (LLMs) and enables efficient contextual understanding of text.

---

### Q2. Why were Transformers introduced?

**Answer**

Transformers were introduced to overcome the limitations of sequential models like RNNs and LSTMs. They process tokens in parallel, capture long-range dependencies more effectively, and scale efficiently for large datasets.

---

### Q3. What problems do Transformers solve compared to RNNs and LSTMs?

**Answer**

Transformers solve several limitations of RNNs and LSTMs, including:

- Sequential processing, which slows training.
- Difficulty capturing long-range relationships.
- Limited scalability for large datasets.

By processing all tokens simultaneously, Transformers improve both efficiency and contextual understanding.

---

### Q4. What is the primary advantage of parallel processing in Transformers?

**Answer**

Parallel processing allows all tokens in a sequence to be processed simultaneously instead of one at a time. This significantly speeds up training and improves scalability for modern LLMs.

---

### Q5. Why are Transformers considered the foundation of modern LLMs?

**Answer**

Transformers introduced the Self-Attention mechanism, enabling models to understand relationships between all tokens in a sequence. Nearly all modern LLMs, such as GPT, Llama, Mistral, Gemma, and Qwen, are based on the Transformer architecture.

---

## Attention & Self-Attention

### Q6. What is Attention?

**Answer**

Attention is a mechanism that allows a model to focus on the most relevant parts of the input while processing information, improving contextual understanding.

---

### Q7. What is Self-Attention?

**Answer**

Self-Attention is a type of Attention where each token considers every other token in the same input sequence to determine its contextual meaning.

---

### Q8. How does Self-Attention help an LLM understand context?

**Answer**

Self-Attention enables each token to evaluate its relationship with all other tokens in the sentence. This helps the model understand context, resolve ambiguities, and generate more accurate responses.

---

### Q9. What is the difference between Attention and Self-Attention?

**Answer**

| Attention | Self-Attention |
|-----------|----------------|
| Can operate between different inputs or sequences. | Operates within the same input sequence. |
| Focuses on relevant external information. | Determines relationships among tokens in the same input. |

---

### Q10. Why is Self-Attention important in Transformers?

**Answer**

Self-Attention enables Transformers to understand context, capture long-range relationships, and process all tokens simultaneously, making it the core mechanism behind modern LLMs.

---

## Tokenization

### Q11. What is Tokenization?

**Answer**

Tokenization is the process of converting input text into smaller units called tokens before processing by an LLM.

---

### Q12. What is a Token?

**Answer**

A token is the smallest unit of text processed by an LLM. A token may represent a word, part of a word, punctuation, or a special symbol.

---

### Q13. Is a token always equal to a word?

**Answer**

No. A token is not always a word. Depending on the tokenizer, a token can be a complete word, part of a word, multiple words, punctuation, or special characters.

---

### Q14. What is a Token ID?

**Answer**

A Token ID is a unique numerical identifier assigned to each token in the model's vocabulary. It identifies the token but does not represent its meaning.

---

## Embeddings

### Q15. What are Embeddings?

**Answer**

Embeddings are dense numerical vectors that represent the semantic meaning of tokens, enabling the model to understand relationships and similarities between words.

---

### Q16. Why can't an LLM use Token IDs directly?

**Answer**

Token IDs are only numerical identifiers and do not contain semantic information. Embeddings convert Token IDs into meaningful vector representations that capture relationships between tokens.

---

### Q17. What is the difference between Static and Contextual Embeddings?

**Answer**

| Static Embeddings | Contextual Embeddings |
|-------------------|-----------------------|
| Generated before the Transformer. | Generated after Self-Attention. |
| Same representation for a token. | Changes based on surrounding context. |
| Represents semantic meaning. | Represents semantic meaning within context. |

---

### Q18. Why are Embeddings important for semantic understanding?

**Answer**

Embeddings place semantically similar words closer together in vector space, enabling the model to understand meaning, similarity, and relationships between different words.

---

## Training & Inference

### Q19. What is Training?

**Answer**

Training is the process of teaching an LLM by learning patterns from large datasets and adjusting billions of model weights to improve prediction accuracy.

---

### Q20. What is Inference?

**Answer**

Inference is the process of generating responses using the model's learned weights. During inference, the model predicts the next token without modifying its learned knowledge.

# Intermediate

## Training vs Inference

### Q21. What is the difference between Training and Inference?

**Answer**

| Training | Inference |
|----------|-----------|
| Learns from data by adjusting model weights. | Uses learned weights to generate responses. |
| Computationally expensive. | Comparatively efficient. |
| Performed during model development. | Performed whenever users interact with the model. |

---

### Q22. Where is an LLM's knowledge stored?

**Answer**

An LLM's knowledge is stored in its learned **weights**, which are numerical parameters saved inside the model file (for example, `.gguf` or `.safetensors`). During inference, these weights are loaded into memory to generate responses.

---

### Q23. What are model weights?

**Answer**

Model weights are learned numerical parameters that encode language patterns, grammar, reasoning, and relationships between concepts. They are adjusted during training and remain unchanged during inference.

---

### Q24. Why don't model weights change during inference?

**Answer**

Inference uses the learned weights only for prediction. Since no learning takes place, the weights remain unchanged. Updating weights requires a separate training or fine-tuning process.

---

## Context Window

### Q25. What is a Context Window?

**Answer**

A Context Window is the maximum number of tokens an LLM can process in a single request. It determines how much information the model can consider while generating a response.

---

### Q26. Why do LLMs forget earlier parts of long conversations?

**Answer**

When the total number of tokens exceeds the model's context window, older tokens are removed from the active context to make room for newer ones.

---

### Q27. Does a larger Context Window make an LLM more intelligent?

**Answer**

No. A larger context window increases the amount of information the model can process, but it does not improve the model's reasoning ability or knowledge.

---

### Q28. Why is the Context Window measured in tokens instead of words?

**Answer**

LLMs process tokens rather than words. Since words can be split into multiple tokens, measuring the context window in tokens provides a consistent way to define model capacity.

---

## Sampling

### Q29. What is Sampling?

**Answer**

Sampling is the process of selecting the next token from the probability distribution predicted by the LLM. It determines the final output token during text generation.

---

### Q30. What is Temperature?

**Answer**

Temperature controls the randomness of the predicted probability distribution before sampling. Lower values produce more deterministic responses, while higher values increase creativity.

---

### Q31. What is the difference between Temperature and Sampling?

**Answer**

| Temperature | Sampling |
|------------|----------|
| Adjusts the probability distribution. | Selects the next token. |
| Controls randomness. | Performs the final token selection. |
| Applied before sampling. | Applied after probabilities are adjusted. |

---

### Q32. What is Top-k Sampling?

**Answer**

Top-k sampling limits token selection to the **k** most probable tokens. The final token is then randomly selected from this reduced set.

---

### Q33. What is Top-p (Nucleus Sampling)?

**Answer**

Top-p sampling selects the smallest group of tokens whose cumulative probability reaches a specified threshold (such as 0.9). The next token is then sampled from this dynamic set.

---

### Q34. When would you use a lower Temperature versus a higher Temperature?

**Answer**

Use a lower temperature for tasks requiring accuracy and consistency, such as code generation or legal summaries. Use a higher temperature for creative tasks like storytelling or brainstorming.

---

## Hallucinations

### Q35. What are Hallucinations?

**Answer**

Hallucinations occur when an LLM generates incorrect or fabricated information while presenting it as if it were accurate.

---

### Q36. Why do Hallucinations occur?

**Answer**

LLMs predict the most probable next token based on learned patterns. They do not verify facts or access reliable information unless explicitly provided.

---

### Q37. Can Hallucinations be completely eliminated?

**Answer**

No. Hallucinations cannot be completely eliminated, but they can be significantly reduced using techniques such as RAG, better prompts, grounding with trusted data, and human verification.

---

### Q38. How does RAG help reduce Hallucinations?

**Answer**

RAG retrieves relevant information from external knowledge sources and provides it to the LLM as context, allowing responses to be grounded in actual data instead of relying solely on the model's learned knowledge.

---

## Quantization

### Q39. What is Quantization?

**Answer**

Quantization reduces the precision of model weights to decrease memory usage and improve inference efficiency while keeping the same model architecture and number of parameters.

---

### Q40. What is the trade-off between FP16 and Q4 models?

**Answer**

| FP16 | Q4 |
|------|----|
| Higher precision | Lower precision |
| Larger memory usage | Smaller memory usage |
| Better response quality | Slight quality reduction |
| Slower inference | Faster inference |

# Scenario-Based

### Q41. You need to deploy an LLM on a laptop with 16 GB RAM. Which type of model would you choose and why?

**Suggested Interview Approach**

- Assess the available hardware (RAM and GPU).
- Prefer a quantized model (Q4/Q5) to reduce memory usage.
- Choose an open-weight model if local deployment and privacy are required.
- Balance inference speed, response quality, and hardware limitations.

---

### Q42. Your chatbot starts generating incorrect facts even though the prompts are clear. What could be the possible reasons, and how would you reduce them?

**Suggested Interview Approach**

Possible reasons:

- Hallucinations due to lack of factual context.
- Missing or outdated knowledge.
- High temperature leading to more randomness.
- Poor prompt design.

Possible solutions:

- Use RAG to provide relevant context.
- Lower the temperature for factual tasks.
- Improve prompt instructions.
- Validate responses using trusted data sources.

---

### Q43. A user uploads a 500-page document. What challenge does the Context Window introduce, and how would you address it?

**Suggested Interview Approach**

Challenges:

- The entire document cannot fit into the context window.
- Older information may be discarded if the limit is exceeded.

Solution:

- Split the document into smaller chunks.
- Store embeddings in a vector database.
- Retrieve only relevant chunks using RAG before sending them to the LLM.

---

### Q44. You need highly consistent responses for a legal document summarization system. Which Sampling parameters would you adjust and why?

**Suggested Interview Approach**

- Use a low Temperature (e.g., 0.1–0.3) for deterministic outputs.
- Keep Top-p close to 1.0 or use a moderate Top-k.
- Prioritize consistency and factual accuracy over creativity.

---

### Q45. A company requires all sensitive data to remain on-premises due to compliance requirements. Would you recommend an Open-Weight Model or a Closed Model?

**Suggested Interview Approach**

Recommend an **Open-Weight Model** because:

- It can be deployed entirely within the organization's infrastructure.
- Sensitive data never leaves the company's environment.
- It provides greater control over deployment and data privacy.

---

### Q46. Your application needs creative marketing content. Which Temperature setting would you recommend?

**Suggested Interview Approach**

- Use a higher Temperature (around 0.7–1.0).
- Allow more randomness and diverse token selection.
- Review outputs manually to ensure quality and brand consistency.

---

### Q47. A user asks the same question multiple times but receives slightly different responses. Is this expected?

**Suggested Interview Approach**

Yes, this is expected.

- Sampling introduces randomness.
- Temperature, Top-k, and Top-p influence token selection.
- Lowering the Temperature produces more consistent responses.

---

### Q48. A customer wants to run an LLM completely offline. What factors would you consider before selecting a model?

**Suggested Interview Approach**

Consider:

- Available RAM and GPU.
- Model size and quantization level.
- Required response quality.
- Licensing and deployment restrictions.
- Expected inference speed.

---

### Q49. A team wants the highest-quality responses and has access to powerful GPUs. Would you recommend FP16 or Q4?

**Suggested Interview Approach**

Recommend **FP16** because:

- It preserves higher numerical precision.
- Provides better response quality.
- The available hardware can handle the additional memory requirements.

---

### Q50. As a GenAI Engineer, what factors would you evaluate before selecting an LLM for a production application?

**Suggested Interview Approach**

Evaluate:

- Use case and business requirements.
- Model quality and reasoning capability.
- Hardware availability.
- Memory and latency requirements.
- Quantization options.
- Context window size.
- Privacy and security requirements.
- Licensing (Open-Weight vs Closed Model).
- Cost of deployment and maintenance.
