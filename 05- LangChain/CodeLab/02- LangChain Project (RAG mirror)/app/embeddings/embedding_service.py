from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    def __init__(self, model_name: str):
        # HuggingFaceEmbeddings is LangChain's embedding abstraction
        # around Hugging Face / sentence-transformers models.
        #
        # This creates/configures the embedding object.
        # It does NOT embed our documents yet.
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
        )

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        # Return the configured LangChain embedding object.
        #
        # The vector store will later use this object to embed:
        # 1. documents during indexing
        # 2. user queries during retrieval
        return self.embeddings