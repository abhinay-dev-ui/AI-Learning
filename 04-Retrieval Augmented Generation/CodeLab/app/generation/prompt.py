class PromptBuilder:

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""
You are a helpful research assistant.

Answer the question using only the provided context.

If the answer cannot be found in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}

Answer:
""".strip()