from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)

from app.generation.formatter import (
    ContextFormatter,
)
from app.generation.model import (
    ModelService,
)
from app.generation.output_parser import (
    OutputParserService,
)
from app.generation.prompt import (
    PromptService,
)


class RAGChain:
    def __init__(
        self,
        context_formatter: ContextFormatter,
        prompt_service: PromptService,
        model_service: ModelService,
        output_parser_service: OutputParserService,
    ):
        self.context_formatter = context_formatter

        prompt = prompt_service.get_prompt()
        model = model_service.get_model()
        parser = output_parser_service.get_parser()

        # RunnableLambda converts our normal Python function
        # into a Runnable.
        format_context = RunnableLambda(
            self._format_context
        )

        # This chain expects input:
        #
        # {
        #     "documents": [...],
        #     "question": "..."
        # }
        #
        # The dictionary below creates parallel branches.
        #
        # context:
        #   extract documents
        #   -> format them
        #
        # question:
        #   extract the original question
        self.chain = (
            {
                "context": (
                    RunnableLambda(
                        lambda data: data["documents"]
                    )
                    | format_context
                ),
                "question": (
                    RunnableLambda(
                        lambda data: data["question"]
                    )
                ),
            }
            | prompt
            | model
            | parser
        )

    def _format_context(
        self,
        documents,
    ) -> str:
        return self.context_formatter.format(
            documents
        )

    def invoke(
        self,
        documents,
        question: str,
    ) -> str:
        return self.chain.invoke(
            {
                "documents": documents,
                "question": question,
            }
        )