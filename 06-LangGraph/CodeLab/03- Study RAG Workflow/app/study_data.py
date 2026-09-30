"""A small LangChain tool over the existing LangChain CodeLab documents."""

import os
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.tools import tool


# Four parents above this file is the AI-Learning repository root.
REPOSITORY = Path(__file__).resolve().parents[4]

# Reuse the source documents from the preceding LangChain CodeLab. We read
# them in place so this project does not create a second copy of the data.
DEFAULT_DATA_DIR = (
    REPOSITORY
    / "05- LangChain"
    / "CodeLab"
    / "02- LangChain Project (RAG mirror)"
    / "data"
    / "documents"
)
# The environment override makes the example easy to run from a copied folder.
DATA_DIR = Path(os.environ.get("STUDY_DATA_DIR", DEFAULT_DATA_DIR))

# Removing common words makes the learning search score easier to understand.
STOP_WORDS = {"a", "an", "did", "for", "how", "in", "is", "of", "the", "was", "what"}


def load_documents() -> list[Document]:
    """Read the earlier project's sample files without modifying them."""
    files = sorted(DATA_DIR.glob("study*.txt"))
    if not files:
        raise FileNotFoundError(f"No study documents found in {DATA_DIR}")

    # A LangChain Document keeps the text and searchable metadata together.
    documents: list[Document] = []
    for path in files:
        content = path.read_text(encoding="utf-8")
        match = re.search(r"Study ID:\s*(STUDY-\d{3})", content)
        if match is None:
            raise ValueError(f"Study ID missing from {path.name}")
        documents.append(
            Document(
                page_content=content,
                metadata={"study_id": match.group(1), "source": path.name},
            )
        )
    return documents


def keywords(text: str) -> set[str]:
    """Normalize text into the meaningful words used by the demo scorer."""
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


@tool
def search_studies(query: str, study_id: str = "") -> list[dict]:
    """Find the best matching local study document, optionally limited to a study ID."""
    # Prefer a stable study ID. When it is absent, a named treatment provides
    # enough identity to select one study without guessing.
    treatment = None
    if not study_id:
        match = re.search(r"\btreatment\s+([a-z])\b", query, flags=re.I)
        if match is None:
            return []  # A study identity is needed to avoid choosing an arbitrary file.
        treatment = match.group(1).upper()

    query_terms = keywords(query)
    ranked: list[tuple[int, Document]] = []
    for document in load_documents():
        if study_id and document.metadata["study_id"] != study_id:
            continue
        if treatment and f"Treatment {treatment}" not in document.page_content:
            continue
        # The overlap count is transparent and deterministic. A production RAG
        # system would replace this with the earlier vector search + reranker.
        score = len(query_terms & keywords(document.page_content))
        if score:
            ranked.append((score, document))

    # Highest score first; study ID makes equal scores deterministic.
    ranked.sort(key=lambda pair: (-pair[0], pair[1].metadata["study_id"]))
    return [
        {
            "content": document.page_content,
            "source": document.metadata["source"],
            "study_id": document.metadata["study_id"],
            "score": score,
        }
        for score, document in ranked[:1]
    ]
