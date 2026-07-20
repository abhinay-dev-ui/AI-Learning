"""
Application Logger

Author: GenAI Learning Roadmap
"""


class Logger:
    """Simple application logger."""

    @staticmethod
    def info(message: str) -> None:
        print(f"[INFO] {message}")

    @staticmethod
    def success(message: str) ->None:
        print(f"[SUCCESS] {message}")

    @staticmethod
    def warning(message: str) -> None:
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message: str) -> None:
        print(f"[ERROR] {message}")


logger = Logger()