from pathlib import Path

from langchain_core.documents import Document


class DocumentLoader:
    def load_directory(
        self,
        directory: Path,
    ) -> list[Document]:

        documents: list[Document] = []

        for file_path in sorted(
            directory.glob("*.txt")
        ):
            document = self.load_file(
                file_path
            )

            documents.append(document)

        return documents


    def load_file(
        self,
        file_path: Path,
    ) -> Document:

        # Read the entire text file.
        content = file_path.read_text(
            encoding="utf-8"
        )

        metadata = {
            "source": file_path.name,
        }

        # Extract stable document-level information.
        study_id = self._extract_study_id(
            content
        )

        treatment = self._extract_treatment(
            content
        )

        if study_id:
            metadata["study_id"] = study_id

        if treatment:
            metadata["treatment"] = treatment

        return Document(
            page_content=content,
            metadata=metadata,
        )


    def _extract_study_id(
        self,
        content: str,
    ) -> str | None:

        for line in content.splitlines():

            if line.startswith("Study ID:"):
                return (
                    line.split(
                        "Study ID:",
                        maxsplit=1,
                    )[1]
                    .strip()
                )

        return None


    def _extract_treatment(
        self,
        content: str,
    ) -> str | None:

        # Our learning documents contain phrases such as:
        #
        # "The study evaluates the effectiveness of Treatment C"
        #
        # We extract Treatment A / B / C from this known
        # document structure.
        for line in content.splitlines():

            marker = "effectiveness of "

            if marker in line:
                treatment_part = line.split(
                    marker,
                    maxsplit=1,
                )[1]

                return treatment_part.strip()

        return None