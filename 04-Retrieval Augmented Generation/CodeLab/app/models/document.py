from dataclasses import dataclass


@dataclass
class Document:
    content: str
    metadata: dict


@dataclass
class VectorRecord:
    content: str
    embedding: list[float]
    metadata: dict