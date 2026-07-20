"""
Simple Logger

Author: GenAI Learning Roadmap
"""


class Logger:

    @staticmethod
    def info(message: str) -> None:
        print(f"[INFO] {message}")

    @staticmethod
    def success(message: str) -> None:
        print(f"[SUCCESS] {message}")

    @staticmethod
    def error(message: str) -> None:
        print(f"[ERROR] {message}")


logger = Logger()