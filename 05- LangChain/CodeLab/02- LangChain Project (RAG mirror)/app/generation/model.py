from langchain_ollama import ChatOllama


class ModelService:
    def __init__(
        self,
        model_name: str,
        temperature: float,
    ):
        # Creates/configures the LangChain ChatOllama object.
        #
        # It does NOT call the model yet.
        self.model = ChatOllama(
            model=model_name,
            temperature=temperature,
        )

    def generate(
        self,
        prompt_value,
    ):
        # invoke() sends the formatted chat messages
        # to the local Ollama server.
        #
        # Input:
        #   ChatPromptValue / messages
        #
        # Output:
        #   AIMessage
        return self.model.invoke(
            prompt_value
        )

    def get_model(self) -> ChatOllama:
        return self.model