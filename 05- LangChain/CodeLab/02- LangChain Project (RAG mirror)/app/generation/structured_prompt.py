from langchain_core.prompts import (
    ChatPromptTemplate,
)


class StructuredPromptService:
    def __init__(self):
        self.prompt = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are a research information assistant.

Answer the user's question using only the provided context.

Rules:
- Do not use information that is not present in the context.
- If the context contains enough information, set evidence_found to true.
- If the context does not contain enough information, set evidence_found to false.
- When evidence_found is false, clearly state in the answer that the provided context does not contain enough information.
- Use the study identifier supported by the provided context.
- Keep the answer concise and factual.
""".strip(),
                    ),
                    (
                        "human",
                        """
Context:
{context}

Question:
{question}
""".strip(),
                    ),
                ]
            )
        )

    def get_prompt(self):
        return self.prompt