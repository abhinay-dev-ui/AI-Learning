from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore


class VectorStoreService:
    def __init__(
        self,
        embeddings: Embeddings,
    ):
        # Create an in-memory vector store.
        #
        # We pass the embedding object into the vector store because
        # the store needs it for:
        #
        # - embedding documents during indexing
        # - embedding queries during search
        self.vector_store = InMemoryVectorStore(
            embeddings
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> list[str]:

        # add_documents() receives LangChain Document objects.
        #
        # Internally, the vector store:
        # 1. reads Document.page_content
        # 2. asks the embedding model to create vectors
        # 3. stores vector + document + metadata
        #
        # It returns IDs for the indexed documents.
        return self.vector_store.add_documents(
            documents=documents
        )

    def get_store(self) -> InMemoryVectorStore:
        return self.vector_store