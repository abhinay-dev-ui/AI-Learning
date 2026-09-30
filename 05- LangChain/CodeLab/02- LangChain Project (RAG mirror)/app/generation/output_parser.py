from langchain_core.messages import AIMessage
from langchain_core.output_parsers import (
    StrOutputParser,
)


class OutputParserService:
    def __init__(self):
        self.parser = StrOutputParser()

    def parse(
        self,
        message: AIMessage,
    ) -> str:

        # ChatOllama returns AIMessage.
        #
        # StrOutputParser extracts/converts the model
        # output into a plain Python string.
        return self.parser.invoke(
            message
        )

    def get_parser(self):
        return self.parser