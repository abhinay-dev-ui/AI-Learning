"""
Application Entry Point

Author: GenAI Learning Roadmap
"""

from monitoring.performance_timer import PerformanceTimer
from services.pdf_processing_service import PdfProcessingService


def main() -> None:
    service = PdfProcessingService()

    with PerformanceTimer("PDF Processing") as timer:
        service.process_document()

    print(
        f"\nMeasured Duration : {timer.duration:.4f} seconds"
    )


if __name__ == "__main__":
    main()