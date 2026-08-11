from app.models.document import Document
from pathlib import Path

class DocumentLoader:

    @staticmethod
    def extract_study_id(content: str) -> str:
        for line in content.splitlines():
            if line.startswith("Study ID:"):
                return line.split(":", 1)[1].strip()

        raise ValueError("Study ID not found in document")

    def load(self, directory: str) -> list[Document]:
        documents = []

        for file_path in Path(directory).glob("*.txt"):
            content = file_path.read_text(encoding="utf-8")
            study_id = self.extract_study_id(content)
            # document.metadata["study_id"] = study_id
            documents.append(
                Document(
                    content=content,
                    metadata={
                        "source": str(file_path),
                        "filename": file_path.name,
                        "study_id":study_id
                    },
                )
            )

        return documents