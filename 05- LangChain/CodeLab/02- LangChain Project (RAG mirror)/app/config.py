from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "documents"


CHUNK_SIZE = 100
CHUNK_OVERLAP = 20


EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Cross-encoder model used in our manual RAG CodeLab.
RERANKER_MODEL = "BAAI/bge-reranker-base"


# Retrieve more documents than we ultimately need.
CANDIDATE_K = 4


# Final number of documents after reranking.
TOP_K = 3

# Local LLM used for answer generation.
LLM_MODEL = "mistral"


# Keep generation deterministic for our RAG CodeLab.
LLM_TEMPERATURE = 0