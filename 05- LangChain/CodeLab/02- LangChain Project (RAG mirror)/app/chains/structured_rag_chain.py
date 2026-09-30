from langchain_core.documents import Document
from langchain_core.runnables import (
    RunnableLambda,
)

from app.generation.formatter import (
    ContextFormatter,
)
from app.generation.model import (
    ModelService,
)
from app.generation.structured_prompt import (
    StructuredPromptService,
)
from app.models.study_answer import (
    StudyAnswer,
)
from app.generation.structured_formatter import (
    StructuredContextFormatter,
)


class StructuredRAGChain:
    def __init__(
        self,
        context_formatter: StructuredContextFormatter,
        prompt_service: StructuredPromptService,
        model_service: ModelService,
    ):
        self.context_formatter = (
            context_formatter
        )

        prompt = prompt_service.get_prompt()

        model = model_service.get_model()

        # -------------------------------------------------
        # STRUCTURED OUTPUT
        # -------------------------------------------------
        #
        # Milestone 6:
        #
        # model
        #   ↓
        # AIMessage
        #   ↓
        # StrOutputParser
        #   ↓
        # str
        #
        # Milestone 7:
        #
        # model.with_structured_output(...)
        #   ↓
        # validated StudyAnswer object
        #
        structured_model = (
            model.with_structured_output(
                StudyAnswer,
                method="json_schema",
            )
        )

        format_context = RunnableLambda(
            self._format_context
        )

        # Same LCEL idea from Milestone 6.
        #
        # Input:
        #
        # {
        #     "documents": [...],
        #     "question": "..."
        # }
        #
        # Output of branches:
        #
        # {
        #     "context": "...",
        #     "question": "..."
        # }
        self.chain = (
            {
                "context": (
                    RunnableLambda(
                        lambda data:
                        data["documents"]
                    )
                    | format_context
                ),
                "question": (
                    RunnableLambda(
                        lambda data:
                        data["question"]
                    )
                ),
            }
            | prompt
            | structured_model
        )

    def _format_context(
        self,
        documents: list[Document],
    ) -> str:
        return self.context_formatter.format(
            documents
        )

    def invoke(
        self,
        documents: list[Document],
        question: str,
    ) -> StudyAnswer:

        result = self.chain.invoke(
            {
                "documents": documents,
                "question": question,
            }
        )

        return result