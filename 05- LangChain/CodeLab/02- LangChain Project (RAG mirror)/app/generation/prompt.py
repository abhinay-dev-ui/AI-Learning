from langchain_core.prompts import ChatPromptTemplate


class PromptService:
    def __init__(self):

        # ChatPromptTemplate preserves message roles.
        #
        # System:
        # defines application-level behavior.
        #
        # Human:
        # provides context + user's actual question.
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
- If the answer cannot be determined from the context, say:
  "The provided context does not contain enough information."
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

    def format_prompt(
        self,
        context: str,
        question: str,
    ):
        # invoke() substitutes:
        #
        # {context}
        # {question}
        #
        # and returns a ChatPromptValue containing
        # the structured messages.
        return self.prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

    def get_prompt(self):
        return self.prompt